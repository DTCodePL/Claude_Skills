#!/usr/bin/env python3
"""CLI mostka transkrypcji Teams (`teams-notatki`).

Wyłącznie biblioteka standardowa. Python >= 3.10.

Komendy:
  health                                    — sprawdza dostępność mostka
  resolve --link <link>                     — szuka spotkania po linku Teams
  resolve --date YYYY-MM-DD [--time HH:MM] [--title "..."] [--window-days N]
  resolve --title "..."                     — szuka po dacie/godzinie/tytule
  transcript --account <guid> --meeting <id> [--transcript-id <id>] [--out <ścieżka>]
  transcript --account <guid> --call <callId> [--transcript-id <id>] [--out <ścieżka>]
  parse-vtt --file <plik.vtt> --out <ścieżka.md>   — tryb awaryjny, bez mostka

Konfiguracja (bez wymaganego setupu — działa "z pudełka"):
  TEAMS_NOTATKI_URL   — nadpisuje adres mostka (domyślnie DEFAULT_URL)
  TEAMS_NOTATKI_TOKEN — nadpisuje token (domyślnie DEFAULT_TOKEN)
"""

from __future__ import annotations

import argparse
import datetime
import html
import json
import os
import re
import sys
import urllib.error
import urllib.request
from urllib.parse import quote, urlencode

try:
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
except ImportError:  # pragma: no cover - Python < 3.9, nieoczekiwane przy wymaganiu >=3.10
    ZoneInfo = None  # type: ignore[assignment]

    class ZoneInfoNotFoundError(Exception):  # type: ignore[no-redef]
        pass


# --------------------------------------------------------------------------
# Stałe / konfiguracja
# --------------------------------------------------------------------------

DEFAULT_URL = "https://teamsnotes.tojest.dev"
DEFAULT_TOKEN = "362a87cf8e5d6560e80f074082667f9569cf0073f4768c43"

USER_AGENT = "teams-notatki-cli"
REQUEST_TIMEOUT = 60


def get_base_url() -> str:
    """Adres mostka: env var ma pierwszeństwo, inaczej stała wbudowana w skrypt."""
    return os.environ.get("TEAMS_NOTATKI_URL", DEFAULT_URL).rstrip("/")


def get_token() -> str:
    """Token mostka: env var ma pierwszeństwo, inaczej stała wbudowana w skrypt."""
    return os.environ.get("TEAMS_NOTATKI_TOKEN", DEFAULT_TOKEN)


# --------------------------------------------------------------------------
# Błędy
# --------------------------------------------------------------------------


class BridgeConnectionError(Exception):
    """Mostek nie odpowiedział (sieć, DNS, timeout) — brak jakiejkolwiek odpowiedzi HTTP."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class _UsageError(Exception):
    """Błąd użycia CLI (argparse) — mapowany na kod wyjścia 1, nie 2."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class _ArgParser(argparse.ArgumentParser):
    """ArgumentParser, który zgłasza wyjątek zamiast robić sys.exit(2) na błędzie użycia."""

    def error(self, message: str) -> None:  # type: ignore[override]
        raise _UsageError(message)


# --------------------------------------------------------------------------
# Transport (wstrzykiwalny do testów)
# --------------------------------------------------------------------------

# Sygnatura: (method, url, headers, body: bytes|None) -> (status: int, content: bytes, content_type: str)
Transport = "Callable[[str, str, dict, bytes | None], tuple[int, bytes, str]]"

_TRANSPORT = None  # ustawiane w main(); patrz default_transport() poniżej


def default_transport(method, url, headers, body):
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            content = resp.read()
            content_type = resp.headers.get("Content-Type", "") if resp.headers else ""
            return resp.status, content, content_type
    except urllib.error.HTTPError as exc:
        content = exc.read()
        content_type = exc.headers.get("Content-Type", "") if exc.headers is not None else ""
        return exc.code, content, content_type
    # urllib.error.URLError (brak połączenia, DNS, timeout) celowo NIE jest tu łapany —
    # request() go łapie i zamienia na BridgeConnectionError.


def request(method: str, path: str, body=None):
    """Wykonuje wywołanie do mostka. Zwraca (status, dict|str)."""
    url = get_base_url() + path
    headers = {
        "Authorization": f"Bearer {get_token()}",
        "User-Agent": USER_AGENT,
    }
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json; charset=utf-8"

    transport = _TRANSPORT or default_transport
    try:
        status, content, content_type = transport(method, url, headers, data)
    except urllib.error.URLError as exc:
        raise BridgeConnectionError(str(exc.reason if hasattr(exc, "reason") else exc)) from exc

    text = content.decode("utf-8") if isinstance(content, (bytes, bytearray)) else content

    if content_type and "vtt" in content_type.lower():
        return status, text

    if not text:
        return status, {}

    try:
        return status, json.loads(text)
    except json.JSONDecodeError:
        return status, text


# --------------------------------------------------------------------------
# Pomocnicze: czas
# --------------------------------------------------------------------------


def parse_iso_utc(value):
    """"2026-09-18T10:00:00Z" -> datetime świadomy strefy (UTC). None jeśli brak/niepoprawne."""
    if not value:
        return None
    v = value.strip()
    if v.endswith("Z"):
        v = v[:-1] + "+00:00"
    try:
        dt = datetime.datetime.fromisoformat(v)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    return dt


def to_warsaw(dt_utc: datetime.datetime):
    """Zwraca (datetime w Europe/Warsaw, etykieta strefy). Fallback do UTC gdy brak bazy stref (Windows)."""
    if ZoneInfo is None:
        return dt_utc.astimezone(datetime.timezone.utc), "UTC"
    try:
        tz = ZoneInfo("Europe/Warsaw")
        return dt_utc.astimezone(tz), "PL"
    except ZoneInfoNotFoundError:
        return dt_utc.astimezone(datetime.timezone.utc), "UTC"


def format_timestamp(ts: str) -> str:
    """"00:00:07.153" -> "[00:07]". Minuty nie są ucinane do 59 (spotkania > 1h)."""
    try:
        h_str, m_str, s_str = ts.split(":")
        total_seconds = int(h_str) * 3600 + int(m_str) * 60 + float(s_str)
    except (ValueError, AttributeError):
        return "[??:??]"
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    return f"[{minutes:02d}:{seconds:02d}]"


def _duration_minutes(created, ended):
    start = parse_iso_utc(created)
    end = parse_iso_utc(ended)
    if not start or not end:
        return "nieznany"
    delta = end - start
    minutes = int(delta.total_seconds() // 60)
    return f"{minutes} min"


def _truncate(value: str, length: int = 4) -> str:
    if not value:
        return ""
    if len(value) <= length:
        return value
    return value[:length] + "…"  # "…"


def _format_date_range(start_iso, end_iso):
    start_dt = parse_iso_utc(start_iso)
    if not start_dt:
        return "(brak danych)"
    local_start, tz_label = to_warsaw(start_dt)
    date_str = local_start.strftime("%Y-%m-%d")
    start_str = local_start.strftime("%H:%M")
    end_dt = parse_iso_utc(end_iso)
    if end_dt:
        local_end, _ = to_warsaw(end_dt)
        end_str = local_end.strftime("%H:%M")
        return f"{date_str}, {start_str}–{end_str} ({tz_label})"
    return f"{date_str}, {start_str} ({tz_label})"


# --------------------------------------------------------------------------
# Renderowanie markdown transkrypcji
# --------------------------------------------------------------------------

_MISSING = object()


def render_segments(segments) -> str:
    """Segmenty tego samego mówcy pod rząd -> jeden akapit z czasem PIERWSZEGO segmentu."""
    lines = []
    current_speaker = _MISSING
    current_start = None
    current_parts = []

    def flush():
        if not current_parts:
            return
        label = current_speaker if current_speaker else "Nieznany mówca"
        text = " ".join(p for p in current_parts if p).strip()
        lines.append(f"**{format_timestamp(current_start)} {label}:** {text}")

    for seg in segments:
        speaker = seg.get("speaker")
        if speaker != current_speaker:
            flush()
            current_speaker = speaker
            current_start = seg.get("start")
            current_parts = []
        elif current_start is None:
            current_start = seg.get("start")
        current_parts.append((seg.get("text") or "").strip())
    flush()

    return "\n\n".join(lines)


def render_markdown(meeting, transcript) -> str:
    """Czytelny zapis transkrypcji (.md pośredni — nie mylić z szablonem notatki)."""
    meeting = meeting or {}
    transcript = transcript or {}

    is_adhoc = meeting.get("kind") == "adhocCall"
    if meeting.get("subject"):
        subject = meeting["subject"]
    elif is_adhoc:
        subject = "(połączenie ad hoc)"
    else:
        subject = "(brak tytułu)"
    date_line = _format_date_range(meeting.get("start"), meeting.get("end"))

    # Uwaga: endpoint /transcript zwraca tylko `organizerId` (nie imię i nazwisko) —
    # patrz references/api.md. Jeśli meeting pochodzi z resolve i ma "organizer"
    # (dict z "name"), użyj go; w przeciwnym razie pokaż surowe ID.
    organizer_field = meeting.get("organizer")
    if isinstance(organizer_field, dict) and organizer_field.get("name"):
        organizer_line = organizer_field["name"]
    elif meeting.get("organizerId"):
        organizer_line = f"ID {meeting['organizerId']}"
    else:
        organizer_line = "(brak danych)"

    speakers = transcript.get("speakers")
    if not speakers:
        speakers = sorted({seg.get("speaker") for seg in transcript.get("segments", []) if seg.get("speaker")})
    language = transcript.get("language") or "nieznany"

    header_lines = [
        f"# Transkrypcja: {subject}",
        "",
        f"**Data:** {date_line}  ",
        f"**Organizator:** {organizer_line}  ",
    ]
    if is_adhoc:
        header_lines.append(f"**Połączenie (callId):** {meeting.get('callId') or '(brak)'}  ")
    header_lines += [
        f"**Mówcy:** {', '.join(speakers) if speakers else '(brak)'}  ",
        f"**Język:** {language}",
        "",
        "---",
        "",
    ]
    body = render_segments(transcript.get("segments", []))
    return "\n".join(header_lines) + body + "\n"


# --------------------------------------------------------------------------
# Parser VTT (tryb awaryjny, bez mostka)
# --------------------------------------------------------------------------

_CUE_TIME_RE = re.compile(r"(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})")
_VOICE_RE = re.compile(r"^<v\s+([^>]+)>(.*)$", re.DOTALL)


def _extract_voice(cue_text: str):
    match = _VOICE_RE.match(cue_text)
    if not match:
        return None, cue_text
    speaker = match.group(1).strip()
    content = match.group(2)
    if content.endswith("</v>"):
        content = content[: -len("</v>")]
    return speaker, content


def parse_vtt(text: str) -> list:
    """Parsuje plik VTT w formacie Teams (`<v Mówca>tekst</v>`, cue wieloliniowe, encje HTML)."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = normalized.split("\n")
    segments = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        match = _CUE_TIME_RE.search(line)
        if not match:
            i += 1
            continue
        start, end = match.group(1), match.group(2)
        i += 1
        text_lines = []
        while i < n and lines[i].strip() != "":
            text_lines.append(lines[i].strip())
            i += 1
        cue_text = " ".join(text_lines).strip()
        speaker, content = _extract_voice(cue_text)
        content = html.unescape(content).strip()
        if speaker:
            speaker = html.unescape(speaker).strip()
        segments.append({"start": start, "end": end, "speaker": speaker, "text": content})
    return segments


# --------------------------------------------------------------------------
# Wyjście / błędy mostka
# --------------------------------------------------------------------------


def _print_result(payload, args, text_renderer=None) -> None:
    if args.output_format == "text" and text_renderer is not None:
        print(text_renderer(payload))
    elif args.output_format == "text":
        print(payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))


def _handle_error(status, payload) -> int:
    code = f"http_{status}"
    message = "Nieznany błąd mostka."
    if isinstance(payload, dict):
        err = payload.get("error") or {}
        code = err.get("code", code)
        message = err.get("message", message)
    elif isinstance(payload, str) and payload:
        message = payload

    print(f"BŁĄD {code}: {message}", file=sys.stderr)

    if code == "unauthorized":
        return 4
    if code in ("meeting_not_found", "transcript_not_found"):
        return 3
    return 5


# --------------------------------------------------------------------------
# Komendy
# --------------------------------------------------------------------------


def cmd_health(args) -> int:
    status, payload = request("GET", "/health")
    if 200 <= status < 300:
        _print_result(
            payload,
            args,
            text_renderer=lambda p: f"OK — status={p.get('status')}, service={p.get('service')}",
        )
        return 0
    return _handle_error(status, payload)


def _render_resolve_text(payload) -> str:
    candidates = payload.get("candidates") or []
    if not candidates:
        return "Brak kandydatów."
    return "\n".join(_format_candidate_line(i + 1, c) for i, c in enumerate(candidates))


def _format_candidate_line(index: int, candidate: dict) -> str:
    start_dt = parse_iso_utc(candidate.get("start"))
    end_dt = parse_iso_utc(candidate.get("end"))
    if start_dt:
        local_start, tz_label = to_warsaw(start_dt)
        date_str = local_start.strftime("%Y-%m-%d")
        start_str = local_start.strftime("%H:%M")
    else:
        date_str, start_str, tz_label = "brak daty", "??:??", "UTC"
    if end_dt:
        local_end, _ = to_warsaw(end_dt)
        end_str = local_end.strftime("%H:%M")
    else:
        end_str = "??:??"

    organizer = (candidate.get("organizer") or {}).get("name") or "nieznany"
    transcripts_count = len(candidate.get("transcripts") or [])
    account_id = (candidate.get("account") or {}).get("id") or ""
    if candidate.get("kind") == "adhocCall":
        subject = candidate.get("subject") or "(połączenie ad hoc)"
        call_id = candidate.get("callId") or ""
        id_part = f"połączenie ad hoc · callId: {_truncate(call_id, 8)}"
    else:
        subject = candidate.get("subject") or "(brak tytułu)"
        meeting_id = candidate.get("meetingId") or ""
        id_part = f"meetingId={_truncate(meeting_id)}"

    return (
        f"{index}. {date_str} {start_str}–{end_str} ({tz_label}) | {subject} | "
        f"organizator: {organizer} | transkrypcje: {transcripts_count} | "
        f"konto={_truncate(account_id)}  {id_part}"
    )


def cmd_resolve(args) -> int:
    if args.link:
        body = {"link": args.link}
    elif args.date or args.title:
        body = {}
        if args.date:
            body["date"] = args.date
        if args.time:
            body["time"] = args.time
        if args.title:
            body["title"] = args.title
        if args.window_days is not None:
            body["window_days"] = args.window_days
    else:
        print("BŁĄD bad_usage: podaj --link albo --date/--title.", file=sys.stderr)
        return 1

    status, payload = request("POST", "/meetings/resolve", body)
    if 200 <= status < 300:
        _print_result(payload, args, text_renderer=_render_resolve_text)
        return 0
    return _handle_error(status, payload)


def _transcript_summary_text(out_path, transcript) -> str:
    segments = transcript.get("segments") or []
    speakers = transcript.get("speakers") or []
    language = transcript.get("language") or "nieznany"
    duration = _duration_minutes(transcript.get("createdDateTime"), transcript.get("endDateTime"))
    return (
        f"Zapisano: {out_path}\n"
        f"Segmentów: {len(segments)}\n"
        f"Mówcy: {', '.join(speakers) if speakers else '(brak)'}\n"
        f"Język: {language}\n"
        f"Czas trwania: {duration}"
    )


def _transcript_summary_dict(out_path, transcript) -> dict:
    segments = transcript.get("segments") or []
    speakers = transcript.get("speakers") or []
    return {
        "path": out_path,
        "segments": len(segments),
        "speakers": speakers,
        "language": transcript.get("language") or "nieznany",
        "duration": _duration_minutes(transcript.get("createdDateTime"), transcript.get("endDateTime")),
    }


def _write_file(path: str, content: str) -> None:
    directory = os.path.dirname(os.path.abspath(path))
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)


def _write_transcript_output(out_path, meeting, transcript, markdown) -> None:
    ext = os.path.splitext(out_path)[1].lower()
    if ext == ".json":
        content = json.dumps({"meeting": meeting, "transcript": transcript}, ensure_ascii=False, indent=2)
    elif ext == ".vtt":
        content = transcript.get("vtt", "")
    else:
        content = markdown
    _write_file(out_path, content)


def cmd_transcript(args) -> int:
    if getattr(args, "call", None):
        path = f"/calls/{quote(args.account, safe='')}/{quote(args.call, safe='')}/transcript"
    else:
        path = f"/meetings/{quote(args.account, safe='')}/{quote(args.meeting, safe='')}/transcript"
    query = {}
    if args.transcript_id:
        query["transcriptId"] = args.transcript_id
    if query:
        path += "?" + urlencode(query)

    status, payload = request("GET", path)
    if not (200 <= status < 300):
        return _handle_error(status, payload)

    meeting = payload.get("meeting", {}) if isinstance(payload, dict) else {}
    transcript = payload.get("transcript", {}) if isinstance(payload, dict) else {}
    markdown = render_markdown(meeting, transcript)

    if args.out:
        _write_transcript_output(args.out, meeting, transcript, markdown)
        if args.output_format == "text":
            print(_transcript_summary_text(args.out, transcript))
        else:
            print(json.dumps(_transcript_summary_dict(args.out, transcript), ensure_ascii=False, indent=2))
    else:
        print(markdown)
    return 0


def cmd_parse_vtt(args) -> int:
    with open(args.file, "r", encoding="utf-8") as handle:
        text = handle.read()

    segments = parse_vtt(text)
    speakers = sorted({seg["speaker"] for seg in segments if seg.get("speaker")})
    transcript = {"segments": segments, "speakers": speakers, "language": None}
    markdown = render_markdown({}, transcript)
    _write_file(args.out, markdown)

    if args.output_format == "text":
        print(
            f"Zapisano: {args.out}\n"
            f"Segmentów: {len(segments)}\n"
            f"Mówcy: {', '.join(speakers) if speakers else '(brak)'}"
        )
    else:
        print(
            json.dumps(
                {"path": args.out, "segments": len(segments), "speakers": speakers},
                ensure_ascii=False,
                indent=2,
            )
        )
    return 0


# --------------------------------------------------------------------------
# Argumenty
# --------------------------------------------------------------------------


def _add_format_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--json", action="store_const", const="json", dest="output_format")
    parser.add_argument("--text", action="store_const", const="text", dest="output_format")


def parse_args(argv):
    parser = _ArgParser(
        prog="bridge.py",
        description="CLI mostka transkrypcji Teams (teams-notatki). Wyjście domyślnie JSON, --text dla czytelnego formatu.",
    )
    sub = parser.add_subparsers(dest="command")

    p_health = sub.add_parser("health", help="Sprawdza dostępność mostka (GET /health).")
    _add_format_args(p_health)

    p_resolve = sub.add_parser(
        "resolve",
        help="Znajduje spotkanie po linku Teams albo po dacie/godzinie/tytule (POST /meetings/resolve).",
    )
    p_resolve.add_argument("--link", help="Link Teams (meet/... , meetup-join/... albo gołe ID).")
    p_resolve.add_argument("--date", help="YYYY-MM-DD (czas lokalny PL).")
    p_resolve.add_argument("--time", help="HH:MM, okno ±90 min (wymaga --date).")
    p_resolve.add_argument("--title", help="Podciąg tytułu spotkania.")
    p_resolve.add_argument("--window-days", dest="window_days", type=int, help="±N dni od --date.")
    _add_format_args(p_resolve)

    p_transcript = sub.add_parser(
        "transcript",
        help="Pobiera transkrypcję spotkania (GET /meetings/{account}/{meeting}/transcript) "
        "albo połączenia ad hoc (GET /calls/{account}/{call}/transcript).",
    )
    p_transcript.add_argument("--account", required=True, help="account.id z wyniku resolve.")
    target = p_transcript.add_mutually_exclusive_group(required=True)
    target.add_argument("--meeting", help="meetingId z wyniku resolve (spotkanie planowane).")
    target.add_argument("--call", help="callId z wyniku resolve (połączenie ad hoc z czatu).")
    p_transcript.add_argument("--transcript-id", dest="transcript_id", help="ID konkretnej transkrypcji.")
    p_transcript.add_argument("--out", help="Ścieżka zapisu: .md / .json / .vtt. Bez --out: .md na stdout.")
    _add_format_args(p_transcript)

    p_parse = sub.add_parser(
        "parse-vtt",
        help="Tryb awaryjny bez mostka: parsuje lokalny plik .vtt pobrany ręcznie z Teams.",
    )
    p_parse.add_argument("--file", required=True, help="Ścieżka do pliku .vtt.")
    p_parse.add_argument("--out", required=True, help="Ścieżka zapisu .md.")
    _add_format_args(p_parse)

    args = parser.parse_args(argv)

    if getattr(args, "output_format", None) is None:
        args.output_format = "json"

    if not args.command:
        parser.error("Podaj polecenie: health | resolve | transcript | parse-vtt")

    return args


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

_COMMANDS = {
    "health": cmd_health,
    "resolve": cmd_resolve,
    "transcript": cmd_transcript,
    "parse-vtt": cmd_parse_vtt,
}


def main(argv=None, transport=None) -> int:
    global _TRANSPORT
    _TRANSPORT = transport or default_transport

    try:
        args = parse_args(list(argv) if argv is not None else sys.argv[1:])
    except _UsageError as exc:
        print(f"BŁĄD bad_usage: {exc.message}", file=sys.stderr)
        return 1

    handler = _COMMANDS.get(args.command)
    if handler is None:
        print(f"BŁĄD bad_usage: nieznane polecenie {args.command!r}", file=sys.stderr)
        return 1

    try:
        return handler(args)
    except BridgeConnectionError as exc:
        base = get_base_url()
        print(
            f"BŁĄD connection_error: mostek {base} nie odpowiada ({exc.message}). "
            "Podaj plik .vtt pobrany ręcznie z Teams (Teams → nagranie → Transkrypcja → "
            "Pobierz jako .vtt) i użyj: parse-vtt --file <plik.vtt> --out <notatka.md>.",
            file=sys.stderr,
        )
        return 5
    except FileNotFoundError as exc:
        print(f"BŁĄD file_not_found: {exc}", file=sys.stderr)
        return 5
    except OSError as exc:
        print(f"BŁĄD io_error: {exc}", file=sys.stderr)
        return 5


def _configure_streams() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except (ValueError, OSError):
                pass


if __name__ == "__main__":
    _configure_streams()
    sys.exit(main())
