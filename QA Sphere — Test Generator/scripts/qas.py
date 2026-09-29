"""QA Sphere — deterministyczny skrypt transportu i kontroli (MCP, Markdown).

Podkomendy (zalecana kolejność):
  context -> (generator pisze plik) -> lint --context -> table (brama)
  -> folders -> push --limit 1 -> verify --only <klucz> -> push -> verify
  (+ update -> verify dla poprawek istniejących przypadków)

context --project P [--search T]... [--folder-id N]... --out PLIK
  Odczyty read-only (get_project, list_custom_fields, list_folders,
  list_test_cases) do pliku-kontekstu dla generatora.
lint PLIK [--context CTX] [--strict]
  Błędy (exit 1) i uwagi (exit 0; z --strict exit 1) dot. kształtu pliku,
  pól przypadków i recepty Markdown z Kroku 4c SKILL.md.
table PLIK
  Podgląd Markdown dla bramy użytkownika (projekt, foldery, pokrycie,
  tabela przypadków i aktualizacji, liczniki priorytetów).
folders PLIK [--dry-run] [--create-root]
  upsert_folders dla ścieżek z folderId null (istniejące liście bierzemy
  z drzewa bez upsert). Nigdy nie tworzy folderu obok korzenia projektu
  (pierwszy segment ścieżki musi być korzeniem == tytułowi projektu).
push PLIK [--only KLUCZ]... [--limit N] [--dry-run]
  Uzgodnienie stanu przed zapisem + seryjne create_test_case z zapisem
  seq/id po każdym przypadku. Bez automatycznych ponowień create.
update PLIK [--only SEQ]... [--limit N] [--dry-run]
  update_test_case dla wpisów updates bez done:true (pełna podmiana list).
verify PLIK [--only KLUCZ_LUB_SEQ]...
  Porównanie pliku z odczytem get_test_case. Nigdy nie zapisuje pliku.

Na żywym serwerze skrypt woła wyłącznie narzędzia odczytu, z wyjątkiem
trybów folders/push/update, które po bramce lint wołają narzędzia zapisu.
"""

import argparse
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

DEFAULT_MCP_URL = "https://dtcode.eu1.qasphere.com/api/mcp"
CLAUDE_JSON = Path.home() / ".claude.json"
RETRY_429_ATTEMPTS = 4
RETRY_429_WAIT = 1.5
WRITE_GAP = 0.15
REQUEST_TIMEOUT = 90

# Biała lista argumentów create_test_case ze schematu MCP (2026-09-22).
CREATE_ARGS = {
    "projectCode", "title", "type", "folderId", "priority", "pos",
    "precondition", "steps", "tags", "requirements", "links",
    "customFields", "isDraft", "parameterValues", "richTextFormat",
    "filledTCaseTitleSuffixParams",
}
# Biała lista argumentów update_test_case ze schematu MCP (2026-09-22).
UPDATE_ARGS = {
    "projectCode", "tcaseOrLegacyId", "title", "priority",
    "precondition", "steps", "tags", "requirements", "links",
    "customFields", "isDraft", "parameterValues", "richTextFormat",
    "filledTCaseTitleSuffixParams",
}
# Klucze meta pliku payloadów — nigdy nie idą do API.
META_KEYS = {"key", "folderKey", "seq", "id"}
# Pola jawnie zakazane w pliku payloadów (uzupełnia je push).
FORBIDDEN_CASE_FIELDS = {
    "projectCode", "folderId", "richTextFormat",
    "parameterValues", "templateTCaseId",
}
# Pola jawnie zakazane w updates[].args (uzupełnia je update).
FORBIDDEN_UPDATE_FIELDS = {
    "type", "parameterValues", "projectCode", "tcaseOrLegacyId",
}
STEP_KEYS = {"description", "expected", "data", "sharedStepId"}
DATA_KEYS = {"type", "text", "label", "format", "url", "file"}
DATA_TYPES = {"text", "link", "file"}
FILE_KEYS = {"id", "fileName", "mimeType", "size"}
# Pola tylko do odczytu w krokach z odczytu (update je przycina).
READONLY_STEP_FIELDS = {"id", "type", "version", "isLatest"}

LIST_ITEM_RE = re.compile(r"^\s*(\d+\.|[-*])\s")
PLACEHOLDER_RE = re.compile(r"\b(todo|tbd|xxx|lorem)\b", re.IGNORECASE)
FENCE_LANG_RE = re.compile(r"```[A-Za-z0-9_+#-]+")
INLINE_CODE_RE = re.compile(r"(?<!`)`([^`\n]+?)`(?!`)")


class QasError(Exception):
    """Błąd skryptu z kodem wyjścia. Nigdy nie zawiera klucza API."""

    def __init__(self, message, exit_code=1, http_status=None, uncertain=False):
        super().__init__(message)
        self.message = message
        self.exit_code = exit_code
        self.http_status = http_status
        self.uncertain = uncertain


_KEY = None
_URL = None


def get_auth():
    """Klucz i adres MCP: env, inaczej ~/.claude.json. Klucza nie wypisuje."""
    global _KEY, _URL
    if _KEY and _URL:
        return _KEY, _URL
    key = os.environ.get("QASPHERE_API_KEY") or None
    url = os.environ.get("QASPHERE_MCP_URL") or None
    if key and key.startswith("Bearer "):
        key = key[len("Bearer "):]
    if not key or not url:
        try:
            cfg = json.loads(CLAUDE_JSON.read_text(encoding="utf-8"))
            srv = (cfg.get("mcpServers") or {}).get("qasphere") or {}
            if not key:
                auth = (srv.get("headers") or {}).get("Authorization") or ""
                if auth.startswith("Bearer "):
                    auth = auth[len("Bearer "):]
                key = auth or None
            if not url:
                url = srv.get("url") or None
        except (OSError, ValueError, AttributeError):
            pass
    if not key:
        raise QasError(
            "Brak klucza API QA Sphere: ustaw QASPHERE_API_KEY "
            "albo uzupełnij ~/.claude.json (mcpServers.qasphere).",
            exit_code=1,
        )
    if not url:
        url = DEFAULT_MCP_URL
    _KEY, _URL = key, url
    return key, url


def parse_response(raw, content_type):
    """Wyciąga komunikat JSON-RPC ze zwykłego JSON albo z SSE (ostatnie data:)."""
    if "text/event-stream" in (content_type or ""):
        chunks = [
            line[5:].strip()
            for line in raw.splitlines()
            if line.startswith("data:")
        ]
        if not chunks:
            raise QasError("Pusta odpowiedź SSE serwera MCP.", exit_code=1)
        return json.loads(chunks[-1])
    return json.loads(raw)


def rpc(name, arguments):
    """Jedno wywołanie tools/call. Zwraca (is_error, text, structured).

    Punkt wstrzyknięcia atrapy w testach. Nigdy nie parsuje
    result.content[].text jako JSON ani nie wypisuje klucza.
    """
    key, url = get_auth()
    body = json.dumps(
        {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
         "params": {"name": name, "arguments": arguments}},
        ensure_ascii=False,
    ).encode("utf-8")
    req = urllib.request.Request(
        url, data=body, method="POST",
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json, text/event-stream",
            "Authorization": "Bearer " + key,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            raw = resp.read().decode("utf-8")
            content_type = resp.headers.get("Content-Type", "")
    except urllib.error.HTTPError as exc:
        status = exc.code
        if 500 <= status <= 599:
            raise QasError(
                "Serwer zwrócił HTTP %d (przypadek mógł powstać)." % status,
                exit_code=1, http_status=status, uncertain=True,
            )
        if status == 429:
            raise QasError("Limit 429.", exit_code=1, http_status=429)
        raise QasError("Błąd HTTP %d." % status, exit_code=1,
                       http_status=status)
    except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as exc:
        raise QasError(
            "Przerwane połączenie/timeout (przypadek mógł powstać): %s."
            % exc.__class__.__name__,
            exit_code=1, uncertain=True,
        )
    try:
        msg = parse_response(raw, content_type)
    except (ValueError, KeyError) as exc:
        raise QasError("Nieznana odpowiedź serwera MCP (%s)."
                       % exc.__class__.__name__, exit_code=1)
    if "error" in msg:
        raise QasError("Błąd JSON-RPC: %s."
                       % str(msg["error"])[:200], exit_code=1)
    res = msg.get("result") or {}
    text = "".join(
        c.get("text", "") for c in res.get("content", [])
        if c.get("type") == "text"
    )
    return res.get("isError", False), text, res.get("structuredContent")


def is_429_text(text):
    """429 w isError: httpStatus 429 w JSON {httpStatus, message}."""
    try:
        data = json.loads(text)
    except ValueError:
        return '"httpStatus":429' in text.replace(" ", "")
    return isinstance(data, dict) and data.get("httpStatus") == 429


def call_retry(name, arguments, attempts=RETRY_429_ATTEMPTS):
    """rpc z ponowieniami 429 (1,5 s, do 4 prób)."""
    for attempt in range(attempts):
        try:
            err, text, structured = rpc(name, arguments)
        except QasError as exc:
            if exc.http_status == 429 and attempt < attempts - 1:
                time.sleep(RETRY_429_WAIT)
                continue
            if exc.http_status == 429:
                raise QasError("Limit 429: wyczerpano ponowienia.",
                               exit_code=1, http_status=429)
            raise
        if err and is_429_text(text):
            if attempt < attempts - 1:
                time.sleep(RETRY_429_WAIT)
                continue
            raise QasError("Limit 429: wyczerpano ponowienia.",
                           exit_code=1, http_status=429)
        return err, text, structured
    raise QasError("Limit 429: wyczerpano ponowienia.", exit_code=1,
                   http_status=429)


def parse_api_error(text):
    """(httpStatus, message) z tekstu isError; gdy to nie JSON — (None, text)."""
    try:
        data = json.loads(text)
    except ValueError:
        return None, text
    if isinstance(data, dict):
        return data.get("httpStatus"), str(data.get("message", text))
    return None, text


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def save_json(path, data):
    """Zapis atomowy UTF-8: ensure_ascii=False, indent=2, newline LF."""
    tmp = str(path) + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    os.replace(tmp, path)


def case_ident(tc, idx):
    key = tc.get("key")
    if isinstance(key, str) and key.strip():
        return key
    return "#%d" % idx


def norm_text(text):
    """Normalizacja treści do verify (różnice odczytu; treść w bazie poprawna).

    Zmierzone artefakty odczytu Markdown: język bloku kodu ginie
    (```` ```sql ```` -> ```` ``` ````) i odczyt wstawia pustą linię
    bezpośrednio przed pozycją listy albo otwarciem bloku ```` ``` ````.
    Serie pustych linii zwijamy do jednej, taką wstawioną linię usuwamy;
    pozostałe puste linie są znaczące.
    """
    if not isinstance(text, str):
        return ""
    text = html.unescape(text)
    text = FENCE_LANG_RE.sub("```", text)
    lines = [line.rstrip() for line in text.split("\n")]
    collapsed = []
    prev_blank = False
    for line in lines:
        if not line.strip():
            if prev_blank:
                continue
            prev_blank = True
            collapsed.append("")
        else:
            prev_blank = False
            collapsed.append(line)
    # Parzystość ogrodzeń: które linie ``` otwierają blok i co leży w kodzie
    # (treść kodu to dane — artefakt wstawiania dotyczy tylko Markdowna).
    opens = []
    in_code = []
    inside = False
    for line in collapsed:
        if line.strip().startswith("```"):
            opens.append(not inside)
            in_code.append(False)
            inside = not inside
        else:
            opens.append(False)
            in_code.append(inside)
    kept = []
    for i, line in enumerate(collapsed):
        if line.strip() or in_code[i]:
            kept.append(line)
            continue
        next_is_list = (
            i + 1 < len(collapsed) and not in_code[i + 1]
            and LIST_ITEM_RE.match(collapsed[i + 1]))
        next_is_open = i + 1 < len(collapsed) and opens[i + 1]
        if next_is_list or next_is_open:
            continue
        kept.append(line)
    return "\n".join(kept).strip()


# ---------------------------------------------------------------- lint ---

def _is_nonempty_str(value):
    return isinstance(value, str) and bool(value.strip())


def _strip_fenced_blocks(text):
    """Usuwa bloki ```...``` (do kontroli MD3/MD4 poza kodem)."""
    parts = text.split("```")
    if len(parts) % 2 == 0:
        return parts[0], False  # niezamknięty blok
    return "".join(parts[::2]), True


def _code_mask(lines):
    """Dla każdej linii: czy leży wewnątrz bloku ``` (dane, nie Markdown).

    Linie samych ogrodzeń to znacznik (False); przełączają stan.
    """
    mask = []
    in_code = False
    for line in lines:
        if line.strip().startswith("```"):
            mask.append(False)
            in_code = not in_code
        else:
            mask.append(in_code)
    return mask


def check_markdown(text, errors, warnings, ident, field):
    """Recepta z Kroku 4c SKILL.md: MD1-MD4 to błędy, pusty akapit to błąd.

    MD1/MD2, MD4 (\\\\n) i puste akapity wykrywamy wyłącznie poza blokami
    ```` ``` ```` — linia w rodzaju `1. test` wewnątrz bloku SQL to dane.
    Pusta linia jest dozwolona tylko po pozycji listy albo po linii
    ogrodzenia (zamknięciu bloku kodu); między zwykłymi akapitami to błąd.
    """
    if not isinstance(text, str) or not text:
        return
    if text.count("```") % 2 == 1:
        errors.append((ident, field, "niezamknięty blok ```"))
    lines = text.split("\n")
    mask = _code_mask(lines)
    outside = "\n".join(
        line for line, in_code in zip(lines, mask) if not in_code)
    if "\\n" in outside:
        errors.append(
            (ident, field, "podwójnie escapowany znak nowej linii (\\\\n)"))
    for i, line in enumerate(lines):
        if mask[i] or not LIST_ITEM_RE.match(line):
            continue
        if i + 1 < len(lines):
            nxt = lines[i + 1]
            if nxt.strip() and not LIST_ITEM_RE.match(nxt):
                errors.append((
                    ident, field,
                    "po ostatniej pozycji listy wymagana pusta linia "
                    "(linia %d)" % (i + 1)))
                break
    for i, line in enumerate(lines):
        if mask[i]:
            continue
        match = re.match(r"^\s*(\d+)\.\s", line)
        if not match or int(match.group(1)) == 1:
            continue
        prev = None
        for j in range(i - 1, -1, -1):
            if mask[j] or not lines[j].strip():
                continue
            prev = lines[j]
            break
        if prev is None or not LIST_ITEM_RE.match(prev):
            errors.append((
                ident, field,
                "lista wznowiona po przerwie (pozycja %s.) — "
                "blok kodu dawaj pod listą" % match.group(1)))
            break
    body, _closed = _strip_fenced_blocks(text)
    for span in INLINE_CODE_RE.findall(body):
        if span[:1] in (" ", "\t") or span[-1:] in (" ", "\t"):
            errors.append((
                ident, field,
                "QA Sphere przycina spacje na brzegach kodu "
                "(np. ` Anna `)"))
            break
    if "\n\n" in text:
        for i, line in enumerate(lines):
            if line.strip() or mask[i]:
                continue
            if i == 0:
                warnings.append((ident, field, "pusty akapit na początku"))
                break
            prev = lines[i - 1]
            if LIST_ITEM_RE.match(prev):
                continue
            if prev.strip().startswith("```"):
                continue
            errors.append((ident, field, "pusty akapit"))
            break
    for span in PLACEHOLDER_RE.findall(text):
        warnings.append(
            (ident, field, "zaślepka %s" % span.upper()))
        break


def _check_url_list(items, field, errors, ident):
    if not isinstance(items, list):
        errors.append((ident, field, "musi być listą"))
        return
    for i, item in enumerate(items):
        where = "%s[%d]" % (field, i)
        if not isinstance(item, dict):
            errors.append((ident, where, "musi być obiektem {text, url}"))
            continue
        if not _is_nonempty_str(item.get("text")):
            errors.append((ident, where + ".text", "niepusty tekst wymagany"))
        url = item.get("url")
        if not isinstance(url, str) or not url.startswith("http"):
            errors.append(
                (ident, where + ".url", "url musi zaczynać się od http"))


def _check_data(items, errors, warnings, ident, field):
    if not isinstance(items, list):
        errors.append((ident, field, "musi być listą"))
        return
    if len(items) > 20:
        errors.append((ident, field, "za dużo pozycji (max 20)"))
    for i, item in enumerate(items):
        where = "%s[%d]" % (field, i)
        if not isinstance(item, dict):
            errors.append((ident, where, "musi być obiektem"))
            continue
        for k in item:
            if k not in DATA_KEYS:
                errors.append(
                    (ident, where + "." + k, "nieznane pole danych"))
        dtype = item.get("type")
        if dtype not in DATA_TYPES:
            errors.append(
                (ident, where + ".type", "musi być text|link|file"))
            continue
        if dtype == "text" and not _is_nonempty_str(item.get("text")):
            errors.append((ident, where + ".text", "text wymaga text"))
        if dtype == "link" and not _is_nonempty_str(item.get("url")):
            errors.append((ident, where + ".url", "link wymaga url"))
        if dtype == "file":
            file = item.get("file")
            if not isinstance(file, dict):
                errors.append((ident, where + ".file", "file wymaga file"))
            else:
                for req in sorted(FILE_KEYS):
                    if req not in file or file[req] is None:
                        errors.append((
                            ident, where + ".file." + req,
                            "file wymaga id, fileName, mimeType, size"))
        if isinstance(item.get("text"), str) and "\\n" in item["text"]:
            warnings.append((ident, where + ".text", "\\n w data[].text"))
        if isinstance(item.get("text"), str):
            for span in PLACEHOLDER_RE.findall(item["text"]):
                warnings.append((ident, where + ".text",
                                 "zaślepka %s" % span.upper()))
                break


def _check_precondition(pre, errors, ident):
    field = "precondition"
    if not isinstance(pre, dict):
        errors.append((ident, field, "musi być obiektem"))
        return None
    for k in pre:
        if k not in ("text", "sharedPreconditionId"):
            errors.append((ident, field + "." + k, "nieznane pole"))
    has_text = "text" in pre and pre["text"] is not None
    has_shared = ("sharedPreconditionId" in pre
                  and pre["sharedPreconditionId"] is not None)
    if has_text and has_shared:
        errors.append(
            (ident, field, "text albo sharedPreconditionId (nie oba)"))
        return None
    if has_text:
        if not _is_nonempty_str(pre["text"]):
            errors.append((ident, field + ".text", "niepusty tekst wymagany"))
            return None
        return pre["text"]
    if has_shared:
        if (not isinstance(pre["sharedPreconditionId"], int)
                or isinstance(pre["sharedPreconditionId"], bool)):
            errors.append(
                (ident, field + ".sharedPreconditionId",
                 "musi być liczbą całkowitą"))
        return None
    errors.append(
        (ident, field, "musi mieć text albo sharedPreconditionId"))
    return None


def _check_steps(steps, errors, warnings, ident, md=True, readonly_warn=False):
    if not isinstance(steps, list) or not steps:
        errors.append((ident, "steps", "niepusta lista wymagana"))
        return
    for i, step in enumerate(steps):
        where = "steps[%d]" % i
        if not isinstance(step, dict):
            errors.append((ident, where, "musi być obiektem"))
            continue
        for k in step:
            if k not in STEP_KEYS:
                if readonly_warn and k in READONLY_STEP_FIELDS:
                    warnings.append((
                        ident, where + "." + k,
                        "pole tylko do odczytu — update je przytnie"))
                else:
                    errors.append(
                        (ident, where + "." + k, "nieznane pole kroku"))
        if step.get("sharedStepId") is not None:
            continue
        for k in ("description", "expected"):
            if not _is_nonempty_str(step.get(k)):
                errors.append(
                    (ident, where + "." + k, "niepusty tekst wymagany"))
            elif md:
                check_markdown(step[k], errors, warnings, ident, where + "." + k)
        if "data" in step and step["data"] is not None:
            _check_data(step["data"], errors, warnings, ident, where + ".data")


def _check_case_fields(tc, errors, ident, whitelist, forbidden):
    for k in tc:
        if k in META_KEYS or k.startswith("_"):
            continue
        if k in forbidden:
            errors.append(
                (ident, k, "pole zakazane w pliku (uzupełnia je wysyłka)"))
        elif k not in whitelist:
            errors.append((ident, k, "nieznane pole"))


def lint_file(data, context=None):
    """Zwraca (błędy, uwagi): listy (identyfikator, pole, opis)."""
    errors = []
    warnings = []
    if not isinstance(data, dict):
        return [("plik", "-", "plik musi być obiektem JSON")], []
    project = data.get("project")
    if not _is_nonempty_str(project):
        errors.append(("plik", "project", "niepusty kod projektu wymagany"))
    if data.get("transport") != "mcp":
        errors.append(("plik", "transport", "musi być 'mcp'"))
    if data.get("richTextFormat") != "markdown":
        errors.append(("plik", "richTextFormat", "musi być 'markdown'"))
    has_path = "folderPath" in data and data["folderPath"] is not None
    has_folders = "folders" in data and data["folders"] is not None
    if has_path and has_folders:
        errors.append(
            ("plik", "folderPath/folders",
             "dokładnie jeden: skrót folderPath albo folders"))
    elif not has_path and not has_folders:
        errors.append(
            ("plik", "folderPath/folders",
             "brak folderPath i folders (jeden wymagany)"))
    folder_keys = {}
    paths = []
    if has_path:
        path = data["folderPath"]
        if (not isinstance(path, list) or not path
                or not all(_is_nonempty_str(s) for s in path)):
            errors.append(
                ("plik", "folderPath",
                 "niepusta lista niepustych tytułów wymagana"))
        else:
            paths.append(("folderPath", path))
    if has_folders:
        folders = data["folders"]
        if not isinstance(folders, list) or not folders:
            errors.append(
                ("plik", "folders", "niepusta lista folderów wymagana"))
            folders = []
        for i, folder in enumerate(folders):
            where = "folders[%d]" % i
            if not isinstance(folder, dict):
                errors.append(("plik", where, "musi być obiektem"))
                continue
            fkey = folder.get("key")
            if not _is_nonempty_str(fkey):
                errors.append(("plik", where + ".key",
                               "niepusty klucz wymagany"))
            elif fkey in folder_keys:
                errors.append(("plik", where + ".key",
                               "zdublowany klucz folderu"))
            else:
                folder_keys[fkey] = folder
            path = folder.get("path")
            if (not isinstance(path, list) or not path
                    or not all(_is_nonempty_str(s) for s in path)):
                errors.append(
                    (plik_id(where), where + ".path",
                     "niepusta lista niepustych tytułów wymagana"))
            else:
                paths.append((where, path))
    if len({path[0] for _where, path in paths}) > 1:
        errors.append(
            ("plik", "folders", "wszystkie ścieżki muszą mieć ten sam "
             "pierwszy segment"))
    ctx_roots = []
    ctx_fields = {}
    if context is not None:
        ctx_roots = list(context.get("roots") or [])
        raw_fields = context.get("customFields") or []
        if isinstance(raw_fields, dict):
            raw_fields = raw_fields.get("customFields") or []
        for field in raw_fields:
            if isinstance(field, dict) and field.get("systemName"):
                ctx_fields[field["systemName"]] = field
        if paths and ("projectRoot" in context or "projectTitle" in context):
            root = context.get("projectRoot") or {}
            expected = (root.get("title") if isinstance(root, dict) else None)
            if not expected:
                # Korzeń jeszcze nie istnieje — powstanie przy folders.
                expected = context.get("projectTitle")
            if expected:
                for _where, path in paths:
                    if path[0] != expected:
                        errors.append((
                            "plik", "folderPath",
                            "folder obok korzenia projektu: '%s' nie jest "
                            "korzeniem '%s' (parentId: 0)"
                            % (path[0], expected)))
                        break
        elif paths and ctx_roots:
            for _where, path in paths:
                if path[0] not in ctx_roots:
                    errors.append((
                        "plik", "folderPath",
                        "folder obok korzenia projektu: '%s' nie jest "
                        "korzeniem (parentId: 0)" % path[0]))
                    break
    cases = data.get("testCases") or []
    seen_titles = {}
    seen_keys = {}
    req_sets = []
    ctx_titles = set()
    if context is not None:
        for _name, items in (context.get("cases") or {}).items():
            for item in items or []:
                title = item.get("title")
                if isinstance(title, str):
                    ctx_titles.add(title.strip().casefold())
    for idx, tc in enumerate(cases, 1):
        ident = case_ident(tc, idx) if isinstance(tc, dict) else "#%d" % idx
        if not isinstance(tc, dict):
            errors.append((ident, "-", "musi być obiektem"))
            continue
        _check_case_fields(tc, errors, ident, CREATE_ARGS,
                           FORBIDDEN_CASE_FIELDS)
        if has_folders:
            fkey = tc.get("folderKey")
            if fkey not in folder_keys:
                errors.append(
                    (ident, "folderKey", "musi wskazywać klucz z folders"))
        else:
            if "folderKey" in tc and tc["folderKey"] is not None:
                errors.append(
                    (ident, "folderKey", "zakazany przy skrócie folderPath"))
        if tc.get("type") != "standalone":
            errors.append((ident, "type", "musi być 'standalone'"))
        title = tc.get("title")
        if not _is_nonempty_str(title):
            errors.append((ident, "title", "niepusty tytuł wymagany (1–511)"))
        else:
            if len(title) > 511:
                errors.append(
                    (ident, "title", "za długi (max 511 znaków)"))
            norm = title.strip().casefold()
            if norm in seen_titles:
                errors.append(
                    (ident, "title",
                     "zdublowany tytuł (jak %s)" % seen_titles[norm]))
            else:
                seen_titles[norm] = ident
            if ctx_titles and norm in ctx_titles:
                warnings.append(
                    (ident, "title", "tytuł identyczny z istniejącym"))
        ckey = tc.get("key")
        if ckey is not None:
            if not _is_nonempty_str(ckey):
                errors.append((ident, "key", "niepusty klucz wymagany"))
            elif ckey in seen_keys:
                errors.append(
                    (ident, "key",
                     "zdublowany klucz (jak %s)" % seen_keys[ckey]))
            else:
                seen_keys[ckey] = ident
        if tc.get("priority") not in ("high", "medium", "low"):
            errors.append(
                (ident, "priority", "musi być high|medium|low"))
        if "precondition" in tc and tc["precondition"] is not None:
            text = _check_precondition(tc["precondition"], errors, ident)
            if text:
                check_markdown(text, errors, warnings, ident,
                               "precondition.text")
        _check_steps(tc.get("steps"), errors, warnings, ident)
        tags = tc.get("tags")
        if (not isinstance(tags, list) or not tags
                or not all(_is_nonempty_str(t) for t in tags)):
            errors.append(
                (ident, "tags", "niepusta lista niepustych napisów wymagana"))
        if "requirements" in tc and tc["requirements"] is not None:
            _check_url_list(tc["requirements"], "requirements", errors, ident)
        if "links" in tc and tc["links"] is not None:
            _check_url_list(tc["links"], "links", errors, ident)
        cfields = tc.get("customFields")
        if cfields is not None:
            if not isinstance(cfields, dict):
                errors.append((ident, "customFields", "musi być obiektem"))
            else:
                for name, entry in cfields.items():
                    _check_custom_field(name, entry, errors, warnings,
                                        ident, ctx_fields if context else None)
        req = tc.get("requirements")
        if isinstance(req, list):
            req_sets.append(
                tuple(sorted(
                    (str(r.get("text")), str(r.get("url")))
                    for r in req if isinstance(r, dict))))
    if len(set(req_sets)) > 1:
        warnings.append(
            ("plik", "requirements", "requirements różne między przypadkami"))
    for idx, upd in enumerate(data.get("updates") or [], 1):
        _check_update(upd, idx, errors, warnings,
                      ctx_fields if context else None)
    return errors, warnings


def _check_custom_field(name, entry, errors, warnings, ident, ctx_fields):
    where = "customFields." + str(name)
    if not isinstance(entry, dict):
        errors.append((ident, where, "musi być obiektem {value}"))
        return
    if ctx_fields is None:
        return
    field = ctx_fields.get(name)
    if field is None or not field.get("enabled"):
        errors.append(
            (ident, where, "pole nie istnieje albo ma enabled: false"))
        return
    if field.get("type") == "dropdown" and "value" in entry:
        options = [o.get("value") for o in field.get("options") or []]
        if entry["value"] not in options:
            errors.append(
                (ident, where + ".value",
                 "wartość spoza options pola"))


def _check_update(upd, idx, errors, warnings, ctx_fields):
    seq = upd.get("seq") if isinstance(upd, dict) else None
    ident = "update %s" % seq if isinstance(seq, int) else "update #%d" % idx
    if not isinstance(upd, dict):
        errors.append((ident, "-", "musi być obiektem"))
        return
    if (not isinstance(seq, int) or isinstance(seq, bool)):
        errors.append((ident, "seq", "całkowity seq wymagany"))
    if not _is_nonempty_str(upd.get("reason")):
        errors.append((ident, "reason", "niepusty powód wymagany"))
    args = upd.get("args")
    if not isinstance(args, dict):
        errors.append((ident, "args", "obiekt argumentów wymagany"))
        return
    for k in args:
        if k in FORBIDDEN_UPDATE_FIELDS:
            errors.append(
                (ident, "args." + k,
                 "pole zakazane w update (uzupełnia je wysyłka)"))
        elif k not in UPDATE_ARGS:
            errors.append((ident, "args." + k, "nieznane pole"))
    if "priority" in args and args["priority"] not in (
            "high", "medium", "low", None):
        errors.append((ident, "args.priority", "musi być high|medium|low"))
    if "title" in args and args["title"] is not None:
        if not _is_nonempty_str(args["title"]) or len(args["title"]) > 511:
            errors.append((ident, "args.title", "1–511 znaków"))
    if "precondition" in args and args["precondition"] is not None:
        text = _check_precondition(args["precondition"], errors,
                                   ident + " args")
        if text:
            check_markdown(text, errors, warnings, ident, "args.precondition")
    if "steps" in args and args["steps"] is not None:
        _check_steps(args["steps"], errors, warnings, ident + " args",
                     readonly_warn=True)
    if "tags" in args and args["tags"] is not None:
        tags = args["tags"]
        if (not isinstance(tags, list) or not tags
                or not all(_is_nonempty_str(t) for t in tags)):
            errors.append(
                (ident, "args.tags",
                 "niepusta lista niepustych napisów wymagana"))
    for f in ("requirements", "links"):
        if f in args and args[f] is not None:
            _check_url_list(args[f], "args." + f, errors, ident)
    cfields = args.get("customFields")
    if isinstance(cfields, dict):
        for name, entry in cfields.items():
            _check_custom_field(name, entry, errors, warnings, ident,
                                ctx_fields)


def print_lint(errors, warnings):
    for ident, field, msg in errors:
        print("BŁĄD %s %s: %s" % (ident, field, msg))
    for ident, field, msg in warnings:
        print("UWAGA %s %s: %s" % (ident, field, msg))
    print("Błędy: %d, uwagi: %d." % (len(errors), len(warnings)))


def run_lint_gate(data):
    """Lint przed zapisem. Błędy -> QasError; uwagi wypisuje. Zwraca (e, w)."""
    errors, warnings = lint_file(data)
    print_lint(errors, warnings)
    if errors:
        raise QasError("Lint: popraw błędy (%d)." % len(errors), exit_code=1)
    return errors, warnings


def paged_list(tool, base_args):
    """Wszystkie strony list_folders/list_test_cases (limit 100)."""
    items = []
    offset = 0
    total = None
    while True:
        args = dict(base_args)
        args["offset"] = offset
        args["limit"] = 100
        err, text, structured = call_retry(tool, args)
        if err:
            status, message = parse_api_error(text)
            raise QasError("Błąd %s: %s %s."
                           % (tool, status, message[:200]), exit_code=1)
        structured = structured or {}
        batch = structured.get("data") or []
        total = structured.get("total", len(batch))
        items.extend(batch)
        if offset + len(batch) >= total or not batch:
            break
        offset += 100
    return items


def folder_paths(raw_folders):
    """(by_id, id -> pełna ścieżka tytułów) z list_folders.

    Ścieżkę budujemy w górę przez parentId; pętle przerywamy (seen).
    """
    by_id = {f.get("id"): f for f in raw_folders if isinstance(f, dict)}

    def full_path(folder):
        titles = []
        seen = set()
        cur = folder
        while isinstance(cur, dict) and cur.get("id") not in seen:
            seen.add(cur.get("id"))
            titles.append(cur.get("title"))
            parent = cur.get("parentId")
            cur = by_id.get(parent)
            if not parent:
                break
        return list(reversed(titles))

    return by_id, {fid: full_path(f) for fid, f in by_id.items()}


def find_project_root(raw_folders, project_title):
    """Korzeń = folder z parentId 0 o tytule == tytułowi projektu.

    Inne foldery najwyższego poziomu NIE są korzeniem. Zwraca listę
    pasujących folderów (0 = brak, >1 = niejednoznaczność).
    """
    return [f for f in raw_folders
            if isinstance(f, dict) and f.get("parentId") == 0
            and f.get("title") == project_title]


def slim_case(item):
    tags = item.get("tags") or []
    return {
        "seq": item.get("seq"),
        "title": item.get("title"),
        "folderId": item.get("folderId"),
        "priority": item.get("priority"),
        "tags": [t.get("title") for t in tags if isinstance(t, dict)],
    }


def cmd_context(ns):
    project = ns.project
    err, text, structured = call_retry("get_project", {"projectCode": project})
    if err:
        status, message = parse_api_error(text)
        raise QasError("Błąd get_project: %s %s."
                       % (status, message[:200]), exit_code=1)
    proj = structured or {}
    if proj.get("archivedAt"):
        raise QasError("Projekt %s jest zarchiwizowany (archivedAt)." % project,
                       exit_code=1)
    err, text, structured = call_retry(
        "list_custom_fields", {"projectCode": project})
    if err:
        status, message = parse_api_error(text)
        raise QasError("Błąd list_custom_fields: %s %s."
                       % (status, message[:200]), exit_code=1)
    custom_fields = (structured or {}).get("customFields") or []
    raw_folders = paged_list("list_folders", {
        "projectCode": project, "sortField": "id", "sortOrder": "asc"})
    _by_id, id_path = folder_paths(raw_folders)
    folders = []
    for folder in raw_folders:
        if not isinstance(folder, dict):
            continue
        folders.append({
            "id": folder.get("id"),
            "title": folder.get("title"),
            "parentId": folder.get("parentId"),
            "path": id_path.get(folder.get("id"), []),
        })
    roots = sorted({f["title"] for f in folders if f["parentId"] == 0})
    project_title = proj.get("title")
    root_hits = find_project_root(raw_folders, project_title)
    if len(root_hits) == 1:
        project_root = {"id": root_hits[0].get("id"),
                        "title": root_hits[0].get("title")}
    else:
        project_root = None
    cases = {}
    for search in ns.search or []:
        items = paged_list("list_test_cases",
                           {"projectCode": project, "search": search})
        cases["search:" + search] = [slim_case(i) for i in items]
    for folder_id in ns.folder_id or []:
        items = paged_list("list_test_cases",
                           {"projectCode": project, "folders": [folder_id]})
        cases["folder:%d" % folder_id] = [slim_case(i) for i in items]
    out = {
        "project": proj,
        "projectTitle": project_title,
        "projectRoot": project_root,
        "customFields": custom_fields,
        "folders": folders,
        "roots": roots,
        "cases": cases,
    }
    save_json(ns.out, out)
    print("Projekt %s: folderów %d, korzeni %d, pól custom %d."
          % (project, len(folders), len(roots), len(custom_fields)))
    for name, items in cases.items():
        print("%s: przypadków %d." % (name, len(items)))
    print("Zapisano %s." % ns.out)
    return 0


def _payload_folders(data):
    """Normalizuje kształt jedno-/wielofolderowy do listy roboczej."""
    if "folders" in data and data["folders"] is not None:
        return [
            {"key": f.get("key"),
             "path": f.get("path"),
             "comment": f.get("comment"),
             "folderId": f.get("folderId"),
             "ref": f}
            for f in data["folders"]
        ]
    return [{
        "key": None,
        "path": data.get("folderPath"),
        "comment": data.get("folderComment"),
        "folderId": data.get("folderId"),
        "ref": None,
    }]


def cmd_table(ns):
    data = load_json(ns.plik)
    project = data.get("project")
    print("# QA Sphere — podgląd: %s" % project)
    print()
    print("Foldery:")
    for entry in _payload_folders(data):
        path = entry["path"] or []
        label = entry["key"] or "(skrót)"
        print("- `%s` → %s (folderId %s)"
              % (label, " / ".join(str(s) for s in path),
                 entry["folderId"]))
    print()
    coverage = data.get("coverage") or {}
    print("Pokrycie — objęte (%d):" % len(coverage.get("covered") or []))
    for item in coverage.get("covered") or []:
        print("- %s" % item)
    print("Pokrycie — pominięte (%d):" % len(coverage.get("skipped") or []))
    for item in coverage.get("skipped") or []:
        print("- %s" % item)
    print()
    print("| # | klucz | tytuł | priorytet | tagi | folder | seq |")
    print("| --- | --- | --- | --- | --- | --- | --- |")
    counts = {"high": 0, "medium": 0, "low": 0}
    folder_of = {}
    if data.get("folders") is not None:
        for f in data["folders"]:
            folder_of[f.get("key")] = "/".join(f.get("path") or [])
    else:
        folder_of[None] = "/".join(data.get("folderPath") or [])
    for idx, tc in enumerate(data.get("testCases") or [], 1):
        counts[tc.get("priority", "")] = counts.get(tc.get("priority"), 0) + 1
        folder = folder_of.get(tc.get("folderKey"),
                               folder_of.get(None, ""))
        print("| %d | %s | %s | %s | %s | %s | %s |"
              % (idx, tc.get("key") or "", (tc.get("title") or "").replace(
                  "|", "\\|"),
                 tc.get("priority") or "", ", ".join(tc.get("tags") or []),
                 folder, tc.get("seq") or ""))
    print()
    updates = data.get("updates") or []
    if updates:
        print("Aktualizacje:")
        print("| seq | powód | zmieniane pola |")
        print("| --- | --- | --- |")
        for upd in updates:
            args = upd.get("args") or {}
            print("| %s | %s | %s |"
                  % (upd.get("seq"), (upd.get("reason") or "").replace(
                      "|", "\\|"), ", ".join(sorted(args))))
    print()
    print("Liczniki: high %d, medium %d, low %d (razem %d; aktualizacji %d)."
          % (counts.get("high", 0), counts.get("medium", 0),
             counts.get("low", 0), len(data.get("testCases") or []),
             len(updates)))
    return 0


def cmd_folders(ns):
    data = load_json(ns.plik)
    run_lint_gate(data)
    project = data.get("project")
    entries = _payload_folders(data)
    todo = [e for e in entries if not e["folderId"]]
    if ns.dry_run:
        for entry in entries:
            print("DRY-RUN folder `%s`: %s (folderId %s)" % (
                entry["key"] or "(skrót)",
                " / ".join(entry["path"] or []), entry["folderId"]))
        print("Do utworzenia: %d z %d (bez wywołań)." % (
            len(todo), len(entries)))
        return 0
    err, text, structured = call_retry("get_project", {"projectCode": project})
    if err:
        status, message = parse_api_error(text)
        raise QasError("Błąd get_project: %s %s."
                       % (status, message[:200]), exit_code=1)
    project_title = (structured or {}).get("title")
    raw_folders = paged_list("list_folders", {
        "projectCode": project, "sortField": "id", "sortOrder": "asc"})
    root_hits = find_project_root(raw_folders, project_title)
    if len(root_hits) > 1:
        raise QasError(
            "Niejednoznaczny korzeń projektu '%s': %d foldery najwyższego "
            "poziomu o tym tytule (parentId: 0)."
            % (project_title, len(root_hits)), exit_code=1)
    root = root_hits[0] if root_hits else None
    for entry in entries:
        first = (entry["path"] or [None])[0]
        if root is not None:
            if first != root.get("title"):
                raise QasError(
                    "Folder obok korzenia projektu: '%s' nie jest "
                    "korzeniem '%s' (parentId: 0). Przerywam — QA Sphere "
                    "nie ma delete." % (first, root.get("title")),
                    exit_code=1)
        elif not ns.create_root:
            raise QasError(
                "Brak korzenia projektu '%s' na serwerze (parentId: 0) — "
                "podaj --create-root, aby go utworzyć."
                % project_title, exit_code=1)
        elif first != project_title:
            raise QasError(
                "Z --create-root pierwszy segment musi być tytułem "
                "projektu '%s', jest '%s'." % (project_title, first),
                exit_code=1)
    _by_id, id_path = folder_paths(raw_folders)
    leaf_of = {}
    for fid, path in id_path.items():
        leaf_of.setdefault(tuple(path), fid)
    for entry in todo:
        key = tuple(entry["path"] or [])
        if key in leaf_of:
            # Ścieżka już istnieje — bierzemy id liścia z drzewa, bez
            # upsert_folders (żeby nie nadpisać opisu komentarzem z pliku).
            entry_id = leaf_of[key]
            if entry["ref"] is not None:
                entry["ref"]["folderId"] = entry_id
            else:
                data["folderId"] = entry_id
            save_json(ns.plik, data)
            print("folder `%s` -> folderId %s (istniał — wzięty z drzewa)"
                  % (entry["key"] or "(skrót)", entry_id))
            continue
        payload = {"path": entry["path"]}
        if entry["comment"]:
            payload["comment"] = entry["comment"]
        err, text, structured = call_retry(
            "upsert_folders",
            {"projectCode": project, "folders": [payload]})
        if err:
            status, message = parse_api_error(text)
            save_json(ns.plik, data)
            raise QasError("Błąd upsert_folders: %s %s."
                           % (status, message[:500]), exit_code=1)
        ids = (structured or {}).get("ids") or []
        if not ids or not ids[0]:
            save_json(ns.plik, data)
            raise QasError("upsert_folders nie zwrócił ids.", exit_code=1)
        entry_id = ids[0][-1]
        if entry["ref"] is not None:
            entry["ref"]["folderId"] = entry_id
        else:
            data["folderId"] = entry_id
        save_json(ns.plik, data)
        print("folder `%s` -> folderId %s"
              % (entry["key"] or "(skrót)", entry_id))
        time.sleep(WRITE_GAP)
    print("Foldery gotowe: %d (nowych %d)." % (len(entries), len(todo)))
    return 0


def _strip_meta(tc):
    return {k: v for k, v in tc.items()
            if k not in META_KEYS and not k.startswith("_")}


def _match_only(ident, seq, only):
    if not only:
        return True
    for want in only:
        if want == ident or want == str(seq or ""):
            return True
    return False


def _find_same_title(project, title, folder_id):
    """Kandydaci do przejęcia: identyczny tytuł (dokładnie, bez normalizacji)
    i folderId równy docelowemu. Szukamy przez search z paginacją."""
    items = paged_list("list_test_cases",
                       {"projectCode": project, "search": title})
    return [item for item in items
            if isinstance(item, dict)
            and item.get("title") == title
            and item.get("folderId") == folder_id]


def _get_live_case(project, seq, ident):
    """Odczyt przypadku do uzgodnienia. Błąd odczytu to exit 1."""
    try:
        err, text, structured = call_retry(
            "get_test_case",
            {"projectCode": project, "tcase": str(seq)})
    except QasError as exc:
        raise QasError("%s: odczyt seq %s niepewny (%s)."
                       % (ident, seq, exc.message), exit_code=1)
    if err:
        status, message = parse_api_error(text)
        raise QasError("%s: odczyt seq %s: %s %s."
                       % (ident, seq, status, message[:200]), exit_code=1)
    return structured or {}


def cmd_push(ns):
    data = load_json(ns.plik)
    run_lint_gate(data)
    project = data.get("project")
    entries = _payload_folders(data)
    folder_ids = {e["key"]: e["folderId"] for e in entries}
    paths_of = {e["key"]: e["path"] for e in entries}
    pending = []
    for idx, tc in enumerate(data.get("testCases") or [], 1):
        if tc.get("seq"):
            continue
        ident = case_ident(tc, idx)
        if ns.only and not _match_only(ident, None, ns.only):
            continue
        folder_id = folder_ids.get(tc.get("folderKey"), data.get("folderId"))
        if not folder_id:
            raise QasError(
                "Brak folderId dla %s — uruchom najpierw: "
                "python qas.py folders %s." % (ident, ns.plik), exit_code=1)
        pending.append((idx, ident, tc, folder_id))
    if ns.limit is not None:
        pending = pending[:ns.limit]
    if ns.dry_run:
        if not pending:
            print("DRY-RUN: wszystkie pasujące przypadki mają seq "
                  "(nic do wysłania).")
        else:
            idx, ident, tc, folder_id = pending[0]
            args = _strip_meta(tc)
            args["projectCode"] = project
            args["folderId"] = folder_id
            print(json.dumps(args, ensure_ascii=False, indent=2))
            print("DRY-RUN: %s + jeszcze %d (bez wywołań)."
                  % (ident, len(pending) - 1))
        return 0
    if pending:
        # folderId ma wskazywać dokładnie zadeklarowaną ścieżkę — sprawdzamy
        # raz na drzewie, zanim cokolwiek utworzymy.
        _by_id, id_path = folder_paths(paged_list("list_folders", {
            "projectCode": project, "sortField": "id", "sortOrder": "asc"}))
        for idx, ident, tc, folder_id in pending:
            declared = paths_of.get(tc.get("folderKey"),
                                    data.get("folderPath"))
            actual = id_path.get(folder_id)
            if actual is None:
                raise QasError(
                    "folderId %s nie istnieje na serwerze (plik deklaruje "
                    "%s) — uruchom folders ponownie po wyzerowaniu "
                    "folderId." % (folder_id,
                                   " / ".join(declared or [])),
                    exit_code=1)
            if actual != (declared or []):
                raise QasError(
                    "folderId %s wskazuje %s, plik deklaruje %s — uruchom "
                    "folders ponownie po wyzerowaniu folderId."
                    % (folder_id, " / ".join(actual),
                       " / ".join(declared or [])), exit_code=1)
    sent = 0
    for idx, ident, tc, folder_id in pending:
        # Uzgodnienie PRZED zapisem: create co najwyżej raz na przypadek
        # w jednym uruchomieniu, nigdy automatycznego ponowienia.
        candidates = _find_same_title(project, tc.get("title"), folder_id)
        if len(candidates) >= 2:
            save_json(ns.plik, data)
            raise QasError(
                "%s: w folderze istnieje %d przypadków o tym tytule "
                "(seq %s) — rozstrzygnij ręcznie."
                % (ident, len(candidates), ", ".join(
                    str(c.get("seq")) for c in candidates)),
                exit_code=2)
        if len(candidates) == 1:
            live = _get_live_case(project, candidates[0].get("seq"), ident)
            probe = dict(tc)
            probe["_folderId"] = folder_id
            diffs = compare_case(probe, live, ident)
            if not diffs:
                tc["id"], tc["seq"] = live.get("id"), live.get("seq")
                save_json(ns.plik, data)
                print("%s -> seq %s (przejęty — treść zgodna)."
                      % (ident, tc["seq"]))
                sent += 1
                continue
            save_json(ns.plik, data)
            raise QasError(
                "%s: w folderze istnieje przypadek o tym tytule z inną "
                "treścią (seq %s) — rozstrzygnij ręcznie."
                % (ident, live.get("seq")), exit_code=2)
        args = _strip_meta(tc)
        args["projectCode"] = project
        args["folderId"] = folder_id
        try:
            err, text, structured = call_retry("create_test_case", args)
        except QasError as exc:
            save_json(ns.plik, data)
            if exc.uncertain:
                raise QasError(
                    "%s: wynik niepewny — przypadek mógł powstać. "
                    "Uruchom ponownie `push`: przed wysłaniem sprawdzi "
                    "stan na serwerze." % ident, exit_code=2)
            raise QasError("%s: %s." % (ident, exc.message),
                           exit_code=exc.exit_code)
        if err:
            save_json(ns.plik, data)
            status, message = parse_api_error(text)
            raise QasError("%s: %s %s." % (ident, status, message[:500]),
                           exit_code=1)
        structured = structured or {}
        if "id" in structured and "seq" in structured:
            tc["id"], tc["seq"] = structured["id"], structured["seq"]
            save_json(ns.plik, data)
            print("%s -> seq %s." % (ident, tc["seq"]))
            sent += 1
            time.sleep(WRITE_GAP)
            continue
        save_json(ns.plik, data)
        raise QasError(
            "%s: wynik niepewny — przypadek mógł powstać. Uruchom ponownie "
            "`push`: przed wysłaniem sprawdzi stan na serwerze." % ident,
            exit_code=2)
    print("Wysłano %d (pominięto z seq: reszta)." % sent)
    return 0


def trim_update_args(args):
    """Przycina kroki/precondition do pól wejściowych. Zwraca (nowe, cięcia)."""
    trimmed = []
    out = dict(args)
    steps = out.get("steps")
    if isinstance(steps, list):
        new_steps = []
        for step in steps:
            if not isinstance(step, dict):
                new_steps.append(step)
                continue
            if step.get("sharedStepId") is not None:
                keep = {"sharedStepId": step["sharedStepId"]}
            else:
                keep = {k: step[k] for k in
                        ("description", "expected", "data", "sharedStepId")
                        if k in step}
            dropped = sorted(set(step) - set(keep))
            if dropped:
                trimmed.append("krok: %s" % ", ".join(dropped))
            data = keep.get("data")
            if isinstance(data, list):
                new_data = []
                for item in data:
                    if not isinstance(item, dict):
                        new_data.append(item)
                        continue
                    keep_item = {k: item[k] for k in
                                 ("type", "text", "label", "format",
                                  "url", "file") if k in item}
                    dropped_item = sorted(set(item) - set(keep_item))
                    if dropped_item:
                        trimmed.append("data: %s" % ", ".join(dropped_item))
                    new_data.append(keep_item)
                keep["data"] = new_data
            new_steps.append(keep)
        out["steps"] = new_steps
    pre = out.get("precondition")
    if isinstance(pre, dict):
        if pre.get("text") is not None:
            keep_pre = {"text": pre["text"]}
        else:
            keep_pre = {k: pre[k] for k in ("sharedPreconditionId",)
                        if k in pre}
        dropped = sorted(set(pre) - set(keep_pre))
        if dropped:
            trimmed.append("precondition: %s" % ", ".join(dropped))
        out["precondition"] = keep_pre
    return out, trimmed


def cmd_update(ns):
    data = load_json(ns.plik)
    run_lint_gate(data)
    project = data.get("project")
    pending = []
    for upd in data.get("updates") or []:
        if not isinstance(upd, dict) or upd.get("done"):
            continue
        if ns.only and str(upd.get("seq")) not in ns.only:
            continue
        pending.append(upd)
    if ns.limit is not None:
        pending = pending[:ns.limit]
    if ns.dry_run:
        for upd in pending:
            _args, trimmed = trim_update_args(upd.get("args") or {})
            print("DRY-RUN update seq %s: pola %s%s (bez wywołań)." % (
                upd.get("seq"), ", ".join(sorted((upd.get("args") or {}))),
                "; przycięto: %s" % "; ".join(trimmed) if trimmed else ""))
        print("Do aktualizacji: %d (bez wywołań)." % len(pending))
        return 0
    done = 0
    for upd in pending:
        seq = upd.get("seq")
        args, trimmed = trim_update_args(upd.get("args") or {})
        for cut in trimmed:
            print("seq %s: przycięto %s." % (seq, cut))
        call_args = dict(args)
        call_args["projectCode"] = project
        call_args["tcaseOrLegacyId"] = str(seq)
        try:
            err, text, _structured = call_retry("update_test_case", call_args)
        except QasError as exc:
            if not exc.uncertain:
                save_json(ns.plik, data)
                raise QasError("seq %s: %s." % (seq, exc.message),
                               exit_code=exc.exit_code)
            err, text, _structured = _update_once(call_args)
            if err:
                save_json(ns.plik, data)
                raise QasError("seq %s: zapis niepewny (%s)." % (seq, text),
                               exit_code=1)
        if err:
            save_json(ns.plik, data)
            status, message = parse_api_error(text)
            raise QasError("seq %s: %s %s." % (seq, status, message[:500]),
                           exit_code=1)
        upd["done"] = True
        save_json(ns.plik, data)
        print("seq %s zaktualizowany." % seq)
        done += 1
        time.sleep(WRITE_GAP)
    print("Zaktualizowano %d." % done)
    return 0


def _update_once(call_args):
    """Jedno bezpieczne ponowienie update (pełna podmiana)."""
    try:
        return call_retry("update_test_case", call_args)
    except QasError as exc:
        return True, exc.message, None


def _short(text, width=160):
    text = str(text).replace("\n", " ⏎ ")
    if len(text) > width:
        return text[:width] + "…"
    return text


def _diff_field(diffs, ident, field, file_val, live_val):
    fnorm = norm_text(file_val) if isinstance(file_val, str) else file_val
    lnorm = norm_text(live_val) if isinstance(live_val, str) else live_val
    if fnorm != lnorm:
        file_lines = (fnorm if isinstance(fnorm, str) else str(fnorm or "")
                      ).split("\n")
        live_lines = (lnorm if isinstance(lnorm, str) else str(lnorm or "")
                      ).split("\n")
        first = next(
            ((a, b) for a, b in zip(file_lines, live_lines) if a != b),
            (file_lines[0] if file_lines else "",
             live_lines[0] if live_lines else ""))
        diffs.append((ident, field, _short(first[0]), _short(first[1])))


def compare_case(tc, live, ident, partial=False):
    """Porównuje przypadek z pliku z odczytem. Zwraca listę różnic.

    partial=True (wpisy updates): porównuje tylko pola obecne w tc.
    """
    diffs = []

    def present(key):
        return not partial or key in tc

    if present("title"):
        _diff_field(diffs, ident, "title", tc.get("title"), live.get("title"))
    if present("priority") and tc.get("priority") != live.get("priority"):
        diffs.append((ident, "priority", str(tc.get("priority")),
                      str(live.get("priority"))))
    if "_folderId" in tc and live.get("folderId") != tc["_folderId"]:
        diffs.append((ident, "folderId", str(tc["_folderId"]),
                      str(live.get("folderId"))))
    if present("tags"):
        file_tags = sorted(tc.get("tags") or [])
        live_tags = sorted(t.get("title") for t in live.get("tags") or [])
        if file_tags != live_tags:
            diffs.append((ident, "tags", ", ".join(file_tags),
                          ", ".join(live_tags)))
    if present("precondition"):
        file_pre = tc.get("precondition") or {}
        live_pre = live.get("precondition") or {}
        if file_pre.get("sharedPreconditionId") is not None:
            if (file_pre.get("sharedPreconditionId")
                    != live_pre.get("sharedPreconditionId")):
                diffs.append((
                    ident, "precondition.sharedPreconditionId",
                    str(file_pre.get("sharedPreconditionId")),
                    str(live_pre.get("sharedPreconditionId"))))
        else:
            _diff_field(diffs, ident, "precondition.text",
                        file_pre.get("text", ""), live_pre.get("text", ""))
    if present("isDraft") and "isDraft" in tc:
        if tc.get("isDraft") != live.get("isDraft"):
            diffs.append((ident, "isDraft", str(tc.get("isDraft")),
                          str(live.get("isDraft"))))
    file_steps = tc.get("steps") or []
    live_steps = live.get("steps") or []
    if present("steps") and len(file_steps) != len(live_steps):
        diffs.append((ident, "steps", "kroków %d" % len(file_steps),
                      "kroków %d" % len(live_steps)))
    if present("steps"):
        for i, (fst, lst) in enumerate(zip(file_steps, live_steps)):
            if not isinstance(fst, dict) or not isinstance(lst, dict):
                continue
            if fst.get("sharedStepId") is not None:
                if fst.get("sharedStepId") != lst.get("sharedStepId"):
                    diffs.append((
                        ident, "steps[%d].sharedStepId" % i,
                        str(fst.get("sharedStepId")),
                        str(lst.get("sharedStepId"))))
                continue
            _diff_field(diffs, ident, "steps[%d].description" % i,
                        fst.get("description", ""),
                        lst.get("description", ""))
            _diff_field(diffs, ident, "steps[%d].expected" % i,
                        fst.get("expected", ""), lst.get("expected", ""))
            fdata = fst.get("data") or []
            ldata = lst.get("data") or []
            if len(fdata) != len(ldata):
                diffs.append((ident, "steps[%d].data" % i,
                              "pozycji %d" % len(fdata),
                              "pozycji %d" % len(ldata)))
            for j, (fitem, litem) in enumerate(zip(fdata, ldata)):
                where = "steps[%d].data[%d]" % (i, j)
                for k in ("type", "label", "text", "format", "url"):
                    _diff_field(diffs, ident, where + "." + k,
                                (fitem or {}).get(k, ""),
                                (litem or {}).get(k, ""))
                _diff_field(diffs, ident, where + ".file.id",
                            ((fitem or {}).get("file") or {}).get("id", ""),
                            ((litem or {}).get("file") or {}).get("id", ""))
    for f in ("requirements", "links"):
        if not present(f):
            continue
        file_list = [{"text": r.get("text", ""), "url": r.get("url", "")}
                     for r in (tc.get(f) or []) if isinstance(r, dict)]
        live_list = [{"text": r.get("text", ""), "url": r.get("url", "")}
                     for r in (live.get(f) or []) if isinstance(r, dict)]
        if file_list != live_list:
            diffs.append((ident, f, _short(json.dumps(file_list,
                                                      ensure_ascii=False)),
                          _short(json.dumps(live_list, ensure_ascii=False))))
    file_cf = tc.get("customFields") or {}
    live_cf = live.get("customFields") or {}
    for name, entry in file_cf.items():
        file_val = entry.get("value") if isinstance(entry, dict) else entry
        live_entry = live_cf.get(name) or {}
        live_val = live_entry.get("value")
        if file_val != live_val:
            diffs.append((ident, "customFields." + name, str(file_val),
                          str(live_val)))
    return diffs


def cmd_verify(ns):
    data = load_json(ns.plik)
    project = data.get("project")
    entries = _payload_folders(data)
    folder_ids = {e["key"]: e["folderId"] for e in entries}
    jobs = []
    for idx, tc in enumerate(data.get("testCases") or [], 1):
        ident = case_ident(tc, idx) if isinstance(tc, dict) else "#%d" % idx
        seq = tc.get("seq") if isinstance(tc, dict) else None
        if ns.only and not _match_only(ident, seq, ns.only):
            continue
        if not seq:
            jobs.append((ident, None, None, None))
            continue
        probe = dict(tc)
        probe["_folderId"] = folder_ids.get(tc.get("folderKey"),
                                            data.get("folderId"))
        jobs.append((ident, str(tc["seq"]), probe, None))
    for upd in data.get("updates") or []:
        if not isinstance(upd, dict) or not upd.get("done"):
            continue
        if ns.only and str(upd.get("seq")) not in (ns.only or []):
            continue
        args, _trimmed = trim_update_args(upd.get("args") or {})
        jobs.append(("update %s" % upd.get("seq"), str(upd.get("seq")),
                     args, "update"))
    bad = 0
    for ident, seq, probe, kind in jobs:
        if seq is None:
            print("NIEWYSŁANY %s" % ident)
            bad += 1
            continue
        err, text, structured = call_retry(
            "get_test_case", {"projectCode": project, "tcase": seq})
        if err:
            status, message = parse_api_error(text)
            print("BŁĄD %s: odczyt seq %s: %s %s."
                  % (ident, seq, status, message[:200]))
            bad += 1
            continue
        diffs = compare_case(probe, structured or {}, ident,
                             partial=(kind == "update"))
        if not diffs:
            print("OK %s" % ident)
        else:
            bad += 1
            for _i, field, file_val, live_val in diffs:
                print("RÓŻNICA %s %s:\n  plik: %s\n  live: %s"
                      % (ident, field, file_val, live_val))
    print("Sprawdzono %d, różnic: %d." % (len(jobs), bad))
    return 1 if bad else 0


def cmd_lint(ns):
    data = load_json(ns.plik)
    context = load_json(ns.context) if ns.context else None
    errors, warnings = lint_file(data, context)
    print_lint(errors, warnings)
    if errors or (ns.strict and warnings):
        return 1
    return 0


def build_parser():
    parser = argparse.ArgumentParser(
        prog="qas.py",
        description="QA Sphere: kontekst, lint, tabela, wysyłka, weryfikacja.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("context", help="Odczyty read-only do pliku-kontekstu.")
    p.add_argument("--project", required=True, help="Kod projektu.")
    p.add_argument("--search", action="append", default=[],
                   help="Fraza do list_test_cases (powtarzalne).")
    p.add_argument("--folder-id", action="append", type=int, default=[],
                   help="ID folderu do list_test_cases (powtarzalne).")
    p.add_argument("--out", required=True, help="Plik kontekstu (JSON).")
    p.set_defaults(func=cmd_context)

    p = sub.add_parser("lint", help="Kontrola pliku payloadów.")
    p.add_argument("plik", help="Plik payloadów (JSON).")
    p.add_argument("--context", default=None,
                   help="Plik kontekstu z context.")
    p.add_argument("--strict", action="store_true",
                   help="Uwagi też kończą exit 1.")
    p.set_defaults(func=cmd_lint)

    p = sub.add_parser("table", help="Podgląd Markdown dla bramy.")
    p.add_argument("plik", help="Plik payloadów (JSON).")
    p.set_defaults(func=cmd_table)

    p = sub.add_parser("folders", help="Utwórz foldery (upsert_folders).")
    p.add_argument("plik", help="Plik payloadów (JSON).")
    p.add_argument("--dry-run", action="store_true",
                   help="Pokaż plan bez wywołań.")
    p.add_argument("--create-root", action="store_true",
                   help="Gdy korzeń projektu nie istnieje, utwórz go "
                   "(pierwszy segment musi być tytułem projektu).")
    p.set_defaults(func=cmd_folders)

    p = sub.add_parser("push", help="Utwórz przypadki (create_test_case).")
    p.add_argument("plik", help="Plik payloadów (JSON).")
    p.add_argument("--only", action="append", default=[],
                   help="Klucz lub #nr (powtarzalne).")
    p.add_argument("--limit", type=int, default=None,
                   help="Max liczba do wysłania.")
    p.add_argument("--dry-run", action="store_true",
                   help="Pokaż argumenty bez wywołań.")
    p.set_defaults(func=cmd_push)

    p = sub.add_parser("update", help="Popraw przypadki (update_test_case).")
    p.add_argument("plik", help="Plik payloadów (JSON).")
    p.add_argument("--only", action="append", default=[],
                   help="SEQ (powtarzalne).")
    p.add_argument("--limit", type=int, default=None,
                   help="Max liczba do wysłania.")
    p.add_argument("--dry-run", action="store_true",
                   help="Pokaż plan bez wywołań.")
    p.set_defaults(func=cmd_update)

    p = sub.add_parser("verify", help="Porównaj plik z serwerem (read-only).")
    p.add_argument("plik", help="Plik payloadów (JSON).")
    p.add_argument("--only", action="append", default=[],
                   help="Klucz, #nr albo seq (powtarzalne).")
    p.set_defaults(func=cmd_verify)
    return parser


def main(argv=None):
    parser = build_parser()
    ns = parser.parse_args(argv)
    try:
        return ns.func(ns)
    except QasError as exc:
        print("BŁĄD: %s" % exc.message, file=sys.stderr)
        return exc.exit_code
    except FileNotFoundError as exc:
        print("BŁĄD: brak pliku %s." % exc.filename, file=sys.stderr)
        return 1
    except json.JSONDecodeError as exc:
        print("BŁĄD: zły JSON (%s)." % exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
