#!/usr/bin/env python3
"""Niezalezne wersjonowanie SemVer repozytoriow aplikacji Zebrani (FE/BE).

Kwalifikacje semantyczna (major/minor/patch/none) wykonuje agent wedlug
procedury w SKILL.md na podstawie faktycznego diffa — ten skrypt wykonuje
wyłącznie deterministyczną arytmetykę wersji i synchronizację manifestów.
Skrypt NIE wykrywa sam z diffa, czy zmiana jest breaking; nie zgaduje
poziomu bump ani wersji początkowej.

Użycie:
    release_version.py --repo ABS_DIR --work-item N \
        --bump major|minor|patch|none [--initial X.Y.Z] [--write]

Bez --write: podgląd (preview), nie zmienia żadnych plików.
Z --write: zapisuje version.json oraz manifesty repo (FE/BE).

Kontrakt version.json (repo/version.json):
    {"version": "X.Y.Z",
     "lastRelease": {"workItem": 2290, "baseVersion": "X.Y.Z", "bump": "minor"}}

SemVer: dokładnie X.Y.Z, liczby całkowite bez zer wiodących, precyzja
dowolna (int), bez prerelease/build.
"""

import argparse
import codecs
import json
import os
import re
import sys
import tempfile
import xml.etree.ElementTree as ET

# Bez kotwic ^$: walidacja przez fullmatch. Kotwica $ w match() akceptuje
# końcowy newline ("1.2.3\n"), więc wersja z newline nie może przechodzić.
SEMVER_RE = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")
BUMPS = ("major", "minor", "patch", "none")
BUMP_RANK = {"none": 0, "patch": 1, "minor": 2, "major": 3}

VERSION_JSON_NAME = "version.json"
FE_PACKAGE = "package.json"
FE_LOCK = "package-lock.json"
BE_CSPROJ = os.path.join("ZebraniBE", "ZebraniBE.csproj")


def fail(message):
    print("error: %s" % message, file=sys.stderr)
    raise SystemExit(1)


def parse_semver(text):
    """Zwraca krotkę (x, y, z) albo None dla niepoprawnego SemVer."""
    if not isinstance(text, str):
        return None
    match = SEMVER_RE.fullmatch(text)
    if not match:
        return None
    return (int(match.group(1)), int(match.group(2)), int(match.group(3)))


def format_semver(triple):
    return "%d.%d.%d" % triple


def apply_bump(base, bump):
    x, y, z = base
    if bump == "major":
        return (x + 1, 0, 0)
    if bump == "minor":
        return (x, y + 1, 0)
    if bump == "patch":
        return (x, y, z + 1)
    return (x, y, z)  # none


def max_bump(first, second):
    if BUMP_RANK[second] > BUMP_RANK[first]:
        return second
    return first


def relposix(repo, absolute):
    return os.path.relpath(absolute, repo).replace(os.sep, "/")


def load_json_file(path):
    # utf-8-sig: pliki moga miec BOM (np. po edycji w Windows) — BOM nie
    # jest danymi i nie moze psuc odczytu ani podgladu. Zapis zostaje
    # czystym UTF-8 bez BOM.
    try:
        with open(path, encoding="utf-8-sig") as handle:
            return json.load(handle)
    except FileNotFoundError:
        fail("nie znaleziono pliku: %s" % path)
    except json.JSONDecodeError as exc:
        fail("niepoprawny JSON w %s: %s" % (path, exc))
    except OSError as exc:
        fail("odczyt %s: %s" % (path, exc))


def atomic_write_bytes(path, data):
    directory = os.path.dirname(path)
    fd, tmp = tempfile.mkstemp(dir=directory, prefix=".tmp-release-")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def atomic_write_text(path, text):
    atomic_write_bytes(path, text.encode("utf-8"))


def detect_kind(repo):
    has_fe = os.path.isfile(os.path.join(repo, FE_PACKAGE))
    has_be = os.path.isfile(os.path.join(repo, BE_CSPROJ))
    if has_fe and has_be:
        fail("niejednoznaczne repo: zawiera i package.json, i %s" % BE_CSPROJ)
    if has_fe:
        return "fe"
    if has_be:
        return "be"
    fail("nieznane repo: brak package.json ani %s w %s" % (BE_CSPROJ, repo))


def validate_state(state):
    if not isinstance(state, dict):
        return "version.json musi być obiektem JSON"
    allowed = {"version", "lastRelease", "initialized"}
    unknown = set(state) - allowed
    if unknown:
        return "version.json: nieznane klucze: %s" % sorted(unknown)
    version = parse_semver(state.get("version"))
    if version is None:
        return "version.json: niepoprawne version %r" % (state.get("version"),)
    last = state.get("lastRelease")
    if not isinstance(last, dict):
        return "version.json: brak lastRelease"
    if set(last) != {"workItem", "baseVersion", "bump"}:
        return "version.json: lastRelease wymaga workItem/baseVersion/bump"
    work_item = last.get("workItem")
    if not isinstance(work_item, int) or isinstance(work_item, bool) or work_item <= 0:
        return "version.json: lastRelease.workItem musi być dodatnią liczbą"
    base = parse_semver(last.get("baseVersion"))
    if base is None:
        return "version.json: niepoprawne lastRelease.baseVersion %r" % (last.get("baseVersion"),)
    if last.get("bump") not in BUMP_RANK:
        return "version.json: niepoprawne lastRelease.bump %r" % (last.get("bump"),)
    if "initialized" in state and state["initialized"] is not True:
        return "version.json: initialized może być tylko true"
    if state.get("initialized", False) is True:
        # Marker inicjalizujący: wyłącznie bump none i version == baseVersion.
        # Inicjalizacja jest pierwszym wydaniem tego PBI, nie bazą do bumpa.
        if last["bump"] != "none" or state["version"] != last["baseVersion"]:
            return (
                "version.json: initialized dozwolone tylko dla markera "
                "inicjalizującego (bump none, version=baseVersion)"
            )
    expected = apply_bump(base, last["bump"])
    if version != expected:
        return (
            "version.json niespójny: version %s nie wynika z baseVersion %s + bump %s"
            % (state["version"], last["baseVersion"], last["bump"])
        )
    return None


def validate_fe(repo):
    pkg_path = os.path.join(repo, FE_PACKAGE)
    lock_path = os.path.join(repo, FE_LOCK)
    if not os.path.isfile(lock_path):
        fail("repo FE wymaga %s" % FE_LOCK)
    pkg = load_json_file(pkg_path)
    lock = load_json_file(lock_path)
    if not isinstance(pkg, dict) or parse_semver(pkg.get("version")) is None:
        fail("%s: brak poprawnego pola version" % FE_PACKAGE)
    if not isinstance(lock, dict) or parse_semver(lock.get("version")) is None:
        fail("%s: brak poprawnego pola version" % FE_LOCK)
    if "packages" in lock:
        packages = lock["packages"]
        if not isinstance(packages, dict):
            fail("%s: packages musi być obiektem" % FE_LOCK)
        if "" in packages:
            root_pkg = packages[""]
            if not isinstance(root_pkg, dict) or parse_semver(root_pkg.get("version")) is None:
                fail("%s: packages[\"\"] wymaga poprawnego pola version" % FE_LOCK)
    return pkg, lock


def read_csproj(repo):
    path = os.path.join(repo, BE_CSPROJ)
    try:
        with open(path, "rb") as handle:
            raw = handle.read()
    except OSError as exc:
        fail("odczyt %s: %s" % (BE_CSPROJ, exc))
    bom = raw.startswith(codecs.BOM_UTF8)
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        fail("%s nie jest poprawnym UTF-8" % BE_CSPROJ)
    newline = "\r\n" if b"\r\n" in raw else "\n"
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return path, normalized, newline, bom


PROPERTY_GROUP_RE = re.compile(r"<PropertyGroup\b[^>]*>(.*?)</PropertyGroup>", re.DOTALL)
VERSION_EL_RE = re.compile(r"<Version(\s[^>]*)?>(.*?)</Version>")


def local_name(tag):
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) else tag


def validate_csproj_scope(normalized):
    """Waliduje XML (ElementTree stdlib) i zakres edycji PRZED modyfikacją.

    Błąd (bez zapisu) przy: niepoprawnym XML, warunkowym pierwszym
    <PropertyGroup>, wielu <Version> w pierwszym <PropertyGroup>,
    warunkowym <Version> albo <Version> poza pierwszym <PropertyGroup>.
    Celowo bez ogólnego parsera MSBuild — tylko strażnik zakresu.
    """
    try:
        # Bytes, nie str: deklaracja encoding w prologu XML jest legalna.
        root = ET.fromstring(normalized.encode("utf-8"))
    except ET.ParseError as exc:
        fail("%s: niepoprawny XML: %s" % (BE_CSPROJ, exc))
    groups = [el for el in root.iter() if local_name(el.tag) == "PropertyGroup"]
    if not groups:
        fail("%s: brak bloku <PropertyGroup>" % BE_CSPROJ)
    first = groups[0]
    if "Condition" in first.attrib:
        fail("%s: pierwszy <PropertyGroup> ma Condition — odmowa modyfikacji" % BE_CSPROJ)
    first_versions = [child for child in first if local_name(child.tag) == "Version"]
    if len(first_versions) > 1:
        fail("%s: wiele <Version> w pierwszym <PropertyGroup> — odmowa modyfikacji" % BE_CSPROJ)
    for node in first_versions:
        if "Condition" in node.attrib:
            fail("%s: warunkowy <Version> — odmowa modyfikacji" % BE_CSPROJ)
    for parent in root.iter():
        for child in parent:
            if local_name(child.tag) == "Version" and parent is not first:
                fail(
                    "%s: <Version> poza pierwszym <PropertyGroup> — odmowa modyfikacji"
                    % BE_CSPROJ
                )


def plan_csproj_change(normalized, new_version):
    validate_csproj_scope(normalized)
    match = PROPERTY_GROUP_RE.search(normalized)
    if not match:
        fail("%s: brak bloku <PropertyGroup>" % BE_CSPROJ)
    block = match.group(0)
    version_match = VERSION_EL_RE.search(block)
    if version_match:
        updated_block = (
            block[: version_match.start()]
            + "<Version%s>%s</Version>" % (version_match.group(1) or "", new_version)
            + block[version_match.end():]
        )
    else:
        open_tag_end = block.index(">") + 1
        updated_block = (
            block[:open_tag_end]
            + "\n    <Version>%s</Version>" % new_version
            + block[open_tag_end:]
        )
    updated = normalized[: match.start()] + updated_block + normalized[match.end():]
    # Kontrola po transformacji: serializacja nadal regex (zachowuje tekst,
    # BOM, newline), ale wynik musi mieć dokładnie jeden <Version> z nową
    # wersją — inaczej regex trafił w inny zakres niż strażnik.
    try:
        root = ET.fromstring(updated.encode("utf-8"))
    except ET.ParseError as exc:
        fail("%s: wynik transformacji to niepoprawny XML: %s" % (BE_CSPROJ, exc))
    versions = [el for el in root.iter() if local_name(el.tag) == "Version"]
    if len(versions) != 1 or (versions[0].text or "") != new_version:
        fail("%s: transformacja dała niejednoznaczny <Version> — odmowa zapisu" % BE_CSPROJ)
    return updated


def encode_csproj(normalized, newline, bom):
    out = normalized.replace("\n", newline)
    data = out.encode("utf-8")
    if bom:
        data = codecs.BOM_UTF8 + data
    return data


def build_parser():
    parser = argparse.ArgumentParser(
        description="Deterministyczna arytmetyka SemVer i synchronizacja manifestów FE/BE."
    )
    parser.add_argument("--repo", required=True, help="absolutny katalog repo aplikacji")
    parser.add_argument("--work-item", required=True, type=int, help="dodatni numer PBI/Buga")
    parser.add_argument("--bump", required=True, choices=BUMPS)
    parser.add_argument("--initial", default=None, help="wersja startowa X.Y.Z (tylko gdy brak version.json)")
    parser.add_argument("--write", action="store_true", help="zapis; bez flagi tylko podgląd")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    repo = args.repo
    if not os.path.isabs(repo):
        fail("--repo musi być katalogiem absolutnym")
    if not os.path.isdir(repo):
        fail("--repo nie jest katalogiem: %s" % repo)
    if args.work_item is None or args.work_item <= 0:
        fail("--work-item musi być dodatnią liczbą")
    if args.initial is not None and parse_semver(args.initial) is None:
        fail("--initial musi być poprawnym SemVer X.Y.Z")

    kind = detect_kind(repo)
    state_path = os.path.join(repo, VERSION_JSON_NAME)
    state_exists = os.path.isfile(state_path)

    if not state_exists and args.initial is None:
        fail("brak %s; podaj --initial X.Y.Z zamiast zgadywać" % VERSION_JSON_NAME)
    if state_exists and args.initial is not None:
        fail("--initial dozwolone tylko gdy brak %s" % VERSION_JSON_NAME)
    if not state_exists and args.bump != "none":
        # Inicjalizacja jest pierwszym wydaniem tego PBI: zapisuje wersję
        # bazową bez kolejnego bumpa. Powtórzenie tego PBI z dowolnym bumpem
        # zostaje przy tej wersji; następny bump robi dopiero nowe PBI.
        fail("przy --initial bump musi być none (inicjalizacja jest pierwszym wydaniem tego PBI)")

    initialized = False
    if not state_exists:
        new_version = args.initial
        base_version = args.initial
        effective = "none"
        old_version = None
        marker = {"workItem": args.work_item, "baseVersion": base_version, "bump": "none"}
        initialized = True
    else:
        state = load_json_file(state_path)
        problem = validate_state(state)
        if problem is not None:
            fail(problem)
        old_version = state["version"]
        last = state["lastRelease"]
        initialized = state.get("initialized", False) is True
        if args.bump == "none":
            report = {
                "repo": repo,
                "workItem": args.work_item,
                "bumpRequested": "none",
                "bumpEffective": "none",
                "baseVersion": last["baseVersion"],
                "oldVersion": old_version,
                "newVersion": old_version,
                "write": bool(args.write),
                "files": [],
                "initialized": initialized,
            }
            print(json.dumps(report, indent=2))
            return 0
        if args.work_item == last["workItem"] and initialized:
            # Marker inicjalizujący to pierwsze wydanie tego PBI: powtórzenie
            # z dowolnym bumpem zostaje przy wersji bazowej.
            effective = "none"
            base_version = last["baseVersion"]
            new_version = old_version
            marker = {"workItem": args.work_item, "baseVersion": base_version, "bump": "none"}
        elif args.work_item == last["workItem"]:
            # To samo PBI przed wydaniem: przelicz od baseVersion, nigdy w dół.
            effective = max_bump(last["bump"], args.bump)
            base_version = last["baseVersion"]
            new_version = format_semver(apply_bump(parse_semver(base_version), effective))
            marker = {"workItem": args.work_item, "baseVersion": base_version, "bump": effective}
        else:
            # Inne PBI zaczyna od bieżącej wersji i gubi marker initialized.
            effective = args.bump
            base_version = old_version
            new_version = format_semver(apply_bump(parse_semver(base_version), effective))
            initialized = False
            marker = {"workItem": args.work_item, "baseVersion": base_version, "bump": effective}

    # Weryfikacja wszystkich danych PRZED jakimkolwiek zapisem.
    planned = {}  # relpath -> bytes do zapisu
    if kind == "fe":
        pkg, lock = validate_fe(repo)
        if new_version != pkg.get("version"):
            pkg["version"] = new_version
            planned[FE_PACKAGE] = (json.dumps(pkg, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
        lock_changed = False
        if new_version != lock.get("version"):
            lock["version"] = new_version
            lock_changed = True
        if isinstance(lock.get("packages"), dict) and "" in lock["packages"]:
            if new_version != lock["packages"][""].get("version"):
                lock["packages"][""]["version"] = new_version
                lock_changed = True
        if lock_changed:
            planned[FE_LOCK] = (json.dumps(lock, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    else:
        csproj_path, normalized, newline, bom = read_csproj(repo)
        updated = plan_csproj_change(normalized, new_version)
        if updated != normalized:
            planned[BE_CSPROJ] = encode_csproj(updated, newline, bom)

    state_doc = {"version": new_version, "lastRelease": marker}
    if initialized:
        state_doc["initialized"] = True
    state_changed = True
    if state_exists:
        with open(state_path, encoding="utf-8-sig") as handle:
            state_changed = json.load(handle) != state_doc
    if state_changed:
        planned[VERSION_JSON_NAME] = (json.dumps(state_doc, indent=2) + "\n").encode("utf-8")

    files = sorted(planned)
    report = {
        "repo": repo,
        "workItem": args.work_item,
        "bumpRequested": args.bump,
        "bumpEffective": effective,
        "baseVersion": base_version,
        "oldVersion": old_version,
        "newVersion": new_version,
        "write": bool(args.write),
        "files": files,
        "initialized": initialized,
    }
    if args.write:
        # Zapis atomowy pojedynczych plików (os.replace); to NIE jest
        # transakcja obejmująca wiele plików — po zapisie weryfikujemy
        # każdy plik ponownym odczytem.
        for relpath in files:
            atomic_write_bytes(os.path.join(repo, relpath), planned[relpath])
        verify_error = verify_after_write(repo, kind, new_version, marker)
        if verify_error is not None:
            fail("weryfikacja po zapisie: %s" % verify_error)
    print(json.dumps(report, indent=2))
    return 0


def verify_after_write(repo, kind, new_version, marker):
    try:
        with open(os.path.join(repo, VERSION_JSON_NAME), encoding="utf-8-sig") as handle:
            written = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        return "version.json nieczytelny po zapisie: %s" % exc
    if written.get("version") != new_version or written.get("lastRelease") != marker:
        return "version.json niezgodny po zapisie"
    if kind == "fe":
        try:
            pkg, lock = validate_fe(repo)
        except SystemExit:
            return "manifest FE nieczytelny po zapisie"
        if pkg.get("version") != new_version or lock.get("version") != new_version:
            return "manifest FE niezgodny po zapisie"
        if isinstance(lock.get("packages"), dict) and "" in lock["packages"]:
            if lock["packages"][""].get("version") != new_version:
                return "package-lock packages[\"\"] niezgodny po zapisie"
    else:
        # Weryfikacja przez sparsowany XML (ElementTree, jak straznik
        # zakresu), nie przez literal "<Version>tekst</Version>": element
        # moze legalnie niesc atrybut (np. Label="release"), ktory straznik
        # dopuszcza — literalny match dalby wowczas falszywy blad dopiero
        # po zapisie.
        _path, normalized, _newline, _bom = read_csproj(repo)
        try:
            root = ET.fromstring(normalized.encode("utf-8"))
        except ET.ParseError as exc:
            return "csproj nieczytelny po zapisie: %s" % exc
        versions = [el for el in root.iter() if local_name(el.tag) == "Version"]
        if len(versions) != 1 or (versions[0].text or "") != new_version:
            return "csproj niezgodny po zapisie"
    return None


if __name__ == "__main__":
    sys.exit(main())
