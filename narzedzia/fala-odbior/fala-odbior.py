#!/usr/bin/env python3
"""Odbiór fali briefów: zakres względem zapisanej bazy, sprawdzenia, werdykt.

Wywołanie 1 (baza przed falą):
  python fala-odbior.py --repo <ścieżka> --zapisz-baze <plik.json>

Wywołanie 2 (odbiór po fali):
  python fala-odbior.py --repo <ścieżka> --baza <plik.json> --pakiet <pakiet.json>
      [--brief <id>] [--pelny] [--katalog-logow <katalog>]

Kody wyjścia: 0 = OK lub ostrzeżenia, 1 = błędy, 2 = błąd użycia.
"""

import argparse
import json
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone

LIMIT_POLECENIA = 7000
LIMIT_WIERSZY = 40
LIMIT_BRIEFOW_WERDYKT = 12

I18N_PL = "src/assets/i18n/pl.json"
I18N_EN = "src/assets/i18n/en.json"


class BladUzycia(Exception):
    """Błąd kończący się kodem wyjścia 2."""


class Runner:
    """Uruchamianie poleceń zewnętrznych (git, npx, npm, dotnet)."""

    def __init__(self, limit_sekund: float = 3600) -> None:
        self.limit_sekund = limit_sekund

    def run(
        self,
        args: list[str],
        cwd: str | None = None,
        input: bytes | str | None = None,
    ) -> tuple[int, str, str]:
        if isinstance(input, bytes):
            input = input.decode("utf-8", "replace")
        stdin_zrodlo = subprocess.DEVNULL if input is None else subprocess.PIPE
        extra: dict = {}
        if os.name != "nt":
            extra["start_new_session"] = True
        try:
            p = subprocess.Popen(
                list(args),
                cwd=cwd,
                stdin=stdin_zrodlo,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                shell=False,
                **extra,
            )
        except OSError as e:
            nazwa = args[0] if args else "?"
            return (127, "", f"nie można uruchomić {nazwa}: {e}")
        limit = self.limit_sekund
        try:
            if limit is None:
                out, err = p.communicate(input)
            else:
                out, err = p.communicate(input, timeout=limit)
        except subprocess.TimeoutExpired:
            if os.name == "nt":
                try:
                    subprocess.run(
                        ["taskkill", "/F", "/T", "/PID", str(p.pid)],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                except OSError:
                    pass
            else:
                try:
                    os.killpg(p.pid, signal.SIGKILL)
                except (ProcessLookupError, PermissionError, OSError):
                    try:
                        p.kill()
                    except OSError:
                        pass
            # Wnuk, którego taskkill/killpg nie zabił, trzyma potoki otwarte —
            # bez limitu odbiór zawisłby mimo przekroczenia czasu.
            try:
                out, err = p.communicate(timeout=30)
            except subprocess.TimeoutExpired:
                p.kill()
                out, err = "", ""
            out = out or ""
            err = err or ""
            try:
                minuty = limit / 60 if limit else 0
            except TypeError:
                minuty = 0
            if isinstance(minuty, float) and minuty.is_integer():
                txt = str(int(minuty))
            elif isinstance(minuty, (int, float)):
                txt = f"{minuty:g}"
            else:
                txt = str(minuty)
            msg = f"przekroczony limit czasu {txt} min"
            if err:
                if not err.endswith("\n"):
                    err += "\n"
                err += msg
            else:
                err = msg
            return (124, out, err)
        return (p.returncode, out, err)


def _odmien(n: int, jeden: str, dwa: str, piec: str) -> str:
    if n == 1:
        return jeden
    if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
        return dwa
    return piec


def odmien_plik(n: int) -> str:
    return _odmien(n, "plik", "pliki", "plików")


def odmien_klucz(n: int) -> str:
    return _odmien(n, "klucz", "klucze", "kluczy")


def odmien_commit(n: int) -> str:
    return _odmien(n, "commit", "commity", "commitów")


# --------------------------------------------------------------------------- #
# Globy


def glob_na_regex(glob: str) -> str:
    """Własne dopasowanie: ** przechodzi przez /, * i ? nie przechodzą."""
    i = 0
    n = len(glob)
    w: list[str] = []
    while i < n:
        c = glob[i]
        if c == "*":
            if i + 1 < n and glob[i + 1] == "*":
                po = i + 2
                if po < n and glob[po] == "/":
                    w.append("(?:.*/)?")
                    i = po + 1
                else:
                    w.append(".*")
                    i = po
            else:
                w.append("[^/]*")
                i += 1
        elif c == "?":
            w.append("[^/]")
            i += 1
        elif c in ".^$+{}[]|()\\":
            w.append("\\" + c)
            i += 1
        else:
            w.append(c)
            i += 1
    return "".join(w)


def dopasuj_glob(glob: str, sciezka: str) -> bool:
    return re.fullmatch(glob_na_regex(glob), sciezka) is not None


# --------------------------------------------------------------------------- #
# Git


@dataclass
class StanGit:
    sciezki: set[str]
    niesledzone: set[str]
    zmiany_nazw: list[tuple[str, str]]


def parsuj_status_z(wyjscie: str) -> StanGit:
    sciezki: set[str] = set()
    niesledzone: set[str] = set()
    zmiany: list[tuple[str, str]] = []
    tokeny = wyjscie.split("\0")
    i = 0
    while i < len(tokeny):
        tok = tokeny[i]
        i += 1
        if not tok or len(tok) < 4:
            continue
        x, y, sciezka = tok[0], tok[1], tok[3:]
        if not sciezka:
            continue
        if x == "R":
            nowa = sciezka
            stara = tokeny[i] if i < len(tokeny) else ""
            i += 1
            if stara:
                sciezki.add(stara)
                sciezki.add(nowa)
                zmiany.append((stara, nowa))
            else:
                sciezki.add(nowa)
        else:
            sciezki.add(sciezka)
            if x == "?" and y == "?":
                niesledzone.add(sciezka)
    return StanGit(sciezki, niesledzone, zmiany)


def git_status(runner: Runner, repo: str) -> StanGit:
    kod, out, err = runner.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=repo,
    )
    if kod != 0:
        raise BladUzycia(f"git status nie powiódł się w {repo}: {err.strip()}")
    return parsuj_status_z(out)


def git_head(runner: Runner, repo: str) -> str:
    kod, out, err = runner.run(["git", "rev-parse", "HEAD"], cwd=repo)
    if kod != 0:
        szczegol = (err.strip() or out.strip()) or "nieznany błąd"
        raise BladUzycia(f"nie można odczytać HEAD w {repo}: {szczegol}")
    return out.strip()


def git_rev_parse_sciezka(
    runner: Runner, repo: str, head: str, sciezka: str
) -> str | None:
    kod, out, _err = runner.run(["git", "rev-parse", f"{head}:{sciezka}"], cwd=repo)
    if kod != 0:
        return None
    return out.strip() or None


def git_hashe(runner: Runner, repo: str, sciezki: set[str]) -> dict[str, str | None]:
    """Identyfikatory blobów plików z drzewa roboczego; None gdy pliku nie ma."""
    wynik: dict[str, str | None] = {p: None for p in sciezki}
    istniejace = sorted(p for p in sciezki if os.path.isfile(os.path.join(repo, p)))
    if not istniejace:
        return wynik
    dane = "\n".join(istniejace) + "\n"
    kod, out, _err = runner.run(
        ["git", "hash-object", "--stdin-paths"], cwd=repo, input=dane
    )
    wiersze = [w.strip() for w in out.splitlines() if w.strip()]
    if kod == 0 and len(wiersze) == len(istniejace):
        for p, h in zip(istniejace, wiersze):
            wynik[p] = h
        return wynik
    for p in istniejace:
        kod1, out1, _e1 = runner.run(
            ["git", "hash-object", "--stdin-paths"],
            cwd=repo,
            input=p + "\n",
        )
        wynik[p] = out1.strip().splitlines()[0].strip() if kod1 == 0 and out1.strip() else None
    return wynik


def git_diff_nazwy(runner: Runner, repo: str, baza_head: str, head: str) -> set[str]:
    kod, out, err = runner.run(
        ["git", "diff", "--no-renames", "--name-only", "-z", baza_head, head],
        cwd=repo,
    )
    if kod != 0:
        raise BladUzycia(f"git diff {baza_head}..HEAD nie powiódł się: {err.strip()}")
    return {t for t in out.split("\0") if t}


def git_liczba_commitow(
    runner: Runner, repo: str, baza_head: str, head: str
) -> int | None:
    kod, out, _err = runner.run(
        ["git", "rev-list", "--count", f"{baza_head}..{head}"], cwd=repo
    )
    if kod != 0:
        return None
    try:
        return int(out.strip())
    except ValueError:
        return None


# --------------------------------------------------------------------------- #
# Baza i zakres fali


@dataclass
class Baza:
    repo: str
    head: str
    czas: str
    pliki: dict[str, str | None]


@dataclass
class ZakresFali:
    pliki_fali: set[str]
    zniknely: set[str]
    status: StanGit
    head: str
    head_zmieniony: bool
    commitow_przybylo: int | None


def zapisz_baze(repo: str, dokad: str, runner: Runner) -> int:
    head = git_head(runner, repo)
    status = git_status(runner, repo)
    hashe = git_hashe(runner, repo, status.sciezki)
    baza = Baza(
        repo=os.path.abspath(repo),
        head=head,
        czas=datetime.now(timezone.utc).isoformat(),
        pliki={p: hashe[p] for p in sorted(status.sciezki)},
    )
    try:
        with open(dokad, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "repo": baza.repo,
                    "head": baza.head,
                    "czas": baza.czas,
                    "pliki": baza.pliki,
                },
                f,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
    except OSError as e:
        raise BladUzycia(f"nie można zapisać bazy {dokad}: {e}")
    return len(baza.pliki)


def wczytaj_baze(sciezka: str) -> Baza:
    try:
        with open(sciezka, encoding="utf-8") as f:
            dane = json.load(f)
    except FileNotFoundError:
        raise BladUzycia(f"brak pliku bazy: {sciezka}")
    except (OSError, ValueError) as e:
        raise BladUzycia(f"nieprawidłowy plik bazy {sciezka}: {e}")
    if (
        not isinstance(dane, dict)
        or not isinstance(dane.get("pliki"), dict)
        or not dane.get("head")
    ):
        raise BladUzycia(f"plik bazy {sciezka} nie ma pól head/pliki")
    pliki: dict[str, str | None] = {}
    for k, v in dane["pliki"].items():
        if v is not None and not isinstance(v, str):
            raise BladUzycia(f"plik bazy {sciezka}: nieprawidłowy identyfikator dla {k}")
        pliki[str(k)] = v
    return Baza(
        repo=str(dane.get("repo", "")),
        head=str(dane["head"]),
        czas=str(dane.get("czas", "")),
        pliki=pliki,
    )


def oblicz_zakres(repo: str, baza: Baza, runner: Runner) -> ZakresFali:
    status = git_status(runner, repo)
    head = git_head(runner, repo)
    head_zmieniony = head != baza.head
    kandydaci = set(baza.pliki) | set(status.sciezki)
    commitow: int | None = None
    if head_zmieniony:
        kandydaci |= git_diff_nazwy(runner, repo, baza.head, head)
        commitow = git_liczba_commitow(runner, repo, baza.head, head)
    biezace = git_hashe(runner, repo, kandydaci)
    pliki_fali: set[str] = set()
    zniknely: set[str] = set()
    for sciezka in sorted(kandydaci):
        if sciezka in baza.pliki:
            bazowa = baza.pliki[sciezka]
        else:
            bazowa = git_rev_parse_sciezka(runner, repo, baza.head, sciezka)
        if bazowa != biezace[sciezka]:
            pliki_fali.add(sciezka)
        elif sciezka in baza.pliki and sciezka not in status.sciezki:
            zniknely.add(sciezka)
    return ZakresFali(pliki_fali, zniknely, status, head, head_zmieniony, commitow)


# --------------------------------------------------------------------------- #
# Pakiet i stos


@dataclass
class Brief:
    id: str
    autor: str
    pliki: list[str]


@dataclass
class Pakiet:
    stos: str | None
    briefy: list[Brief]


def wczytaj_pakiet(sciezka: str) -> Pakiet:
    try:
        with open(sciezka, encoding="utf-8") as f:
            dane = json.load(f)
    except FileNotFoundError:
        raise BladUzycia(f"brak pliku pakietu: {sciezka}")
    except (OSError, ValueError) as e:
        raise BladUzycia(f"nieprawidłowy plik pakietu {sciezka}: {e}")
    if not isinstance(dane, dict):
        raise BladUzycia(f"plik pakietu {sciezka} nie zawiera obiektu")
    stos = dane.get("stos")
    if stos is not None and stos not in ("fe", "be"):
        raise BladUzycia(f"pakiet {sciezka}: stos musi być fe albo be")
    briefy_dane = dane.get("briefy")
    if not isinstance(briefy_dane, list):
        raise BladUzycia(f"pakiet {sciezka}: brak listy briefy")
    briefy: list[Brief] = []
    for i, b in enumerate(briefy_dane):
        if not isinstance(b, dict) or not b.get("id"):
            raise BladUzycia(f"pakiet {sciezka}: brief #{i} nie ma id")
        globy = b.get("pliki", [])
        if not isinstance(globy, list) or not all(isinstance(g, str) for g in globy):
            raise BladUzycia(f"pakiet {sciezka}: brief {b.get('id')} ma nieprawidłowe pliki")
        briefy.append(
            Brief(id=str(b["id"]), autor=str(b.get("autor", "?")), pliki=list(globy))
        )
    return Pakiet(stos=stos, briefy=briefy)


def wykryj_stos(repo: str, stos_pakietu: str | None) -> str:
    if stos_pakietu:
        return stos_pakietu
    pj = os.path.join(repo, "package.json")
    if os.path.isfile(pj):
        try:
            with open(pj, encoding="utf-8") as f:
                dane = json.load(f)
        except (OSError, ValueError):
            dane = None
        if isinstance(dane, dict):
            for pole in ("dependencies", "devDependencies"):
                zaleznosci = dane.get(pole)
                if isinstance(zaleznosci, dict) and "@angular/core" in zaleznosci:
                    return "fe"
    try:
        wpisy = os.listdir(repo)
    except OSError:
        wpisy = []
    for wpis in wpisy:
        nn = wpis.lower()
        if (nn.endswith(".slnx") or nn.endswith(".sln")) and os.path.isfile(
            os.path.join(repo, wpis)
        ):
            return "be"
    raise BladUzycia(
        "nie można wykryć stosu: brak @angular/core w package.json "
        "i brak pliku .slnx/.sln w korzeniu (podaj stos w pakiecie)"
    )


def pasuje_do_briefu(sciezka: str, brief: Brief) -> bool:
    return any(dopasuj_glob(g, sciezka) for g in brief.pliki)


# --------------------------------------------------------------------------- #
# Statystyka


@dataclass
class StatBriefu:
    brief: Brief
    pliki: list[str]
    dodane: int
    usuniete: int
    gwiazdka: bool


def statystyki(
    repo: str,
    baza_head: str,
    baza_pliki: dict[str, str | None],
    briefy: list[Brief],
    wlasciciele: dict[str, list[str]],
    niesledzone: set[str],
    runner: Runner,
) -> list[StatBriefu]:
    stats: list[StatBriefu] = []
    for brief in briefy:
        pliki = sorted(p for p, ids in wlasciciele.items() if brief.id in ids)
        dodane = 0
        usuniete = 0
        sledzone = [p for p in pliki if p not in niesledzone]
        if sledzone:
            baza_cmd = ["git", "diff", "--numstat", baza_head, "--"]
            pathspecy = [f":(literal){p}" for p in sledzone]
            try:
                porcje = porcjuj(baza_cmd, pathspecy, LIMIT_POLECENIA)
            except ValueError as e:
                raise BladUzycia(str(e))
            for porcja in porcje:
                kod, out, err = runner.run(baza_cmd + porcja, cwd=repo)
                if kod != 0:
                    raise BladUzycia(f"git diff --numstat nie powiódł się: {err.strip()}")
                for wiersz in out.splitlines():
                    m = re.match(r"^(\d+|-)\t(\d+|-)\t", wiersz)
                    if m:
                        if m.group(1) != "-":
                            dodane += int(m.group(1))
                        if m.group(2) != "-":
                            usuniete += int(m.group(2))
        for p in pliki:
            if p in niesledzone:
                try:
                    with open(os.path.join(repo, p), encoding="utf-8", errors="replace") as f:
                        dodane += len(f.read().splitlines())
                except OSError:
                    pass
        stats.append(
            StatBriefu(
                brief=brief,
                pliki=pliki,
                dodane=dodane,
                usuniete=usuniete,
                gwiazdka=any(p in baza_pliki for p in pliki),
            )
        )
    return stats


# --------------------------------------------------------------------------- #
# Porcjowanie poleceń


def dlugosc_polecenia(args: list[str]) -> int:
    def dl(a: str) -> int:
        if a == "" or any(c in a for c in " \t\""):
            return len(a) + 2 + a.count('"')
        return len(a)

    return sum(dl(a) for a in args) + max(0, len(args) - 1)


def porcjuj(
    baza: list[str], pliki: list[str], limit: int = LIMIT_POLECENIA
) -> list[list[str]]:
    porcje: list[list[str]] = []
    biezaca: list[str] = []
    for p in pliki:
        if dlugosc_polecenia([*baza, p]) > limit:
            raise ValueError(
                f"ścieżka przekracza limit {limit} znaków polecenia "
                f"i nie może być sprawdzona: {p}"
            )
        if biezaca and dlugosc_polecenia([*baza, *biezaca, p]) > limit:
            porcje.append(biezaca)
            biezaca = []
        biezaca.append(p)
    if biezaca:
        porcje.append(biezaca)
    return porcje


# --------------------------------------------------------------------------- #
# i18n


def splaszcz_json(wartosc: dict) -> set[str]:
    klucze: set[str] = set()

    def rek(w: object, pref: str) -> None:
        if isinstance(w, dict):
            for k, v in w.items():
                rek(v, k if not pref else f"{pref}.{k}")
        elif pref:
            klucze.add(pref)

    rek(wartosc, "")
    return klucze


@dataclass
class RaportI18n:
    ok: bool
    tekst: str
    pl_kluczy: int | None = None
    en_kluczy: int | None = None
    tylko_pl: list[str] = field(default_factory=list)
    tylko_en: list[str] = field(default_factory=list)


def sprawdz_i18n(repo: str) -> RaportI18n:
    klucze: dict[str, set[str]] = {}
    for nazwa, rel in (("pl", I18N_PL), ("en", I18N_EN)):
        pelna = os.path.join(repo, rel)
        if not os.path.isfile(pelna):
            return RaportI18n(ok=False, tekst=f"i18n: brak pliku {rel}")
        try:
            with open(pelna, encoding="utf-8") as f:
                dane = json.load(f)
        except (OSError, ValueError):
            return RaportI18n(ok=False, tekst=f"i18n: nieprawidłowy JSON w {rel}")
        if not isinstance(dane, dict):
            return RaportI18n(ok=False, tekst=f"i18n: korzeń {rel} nie jest obiektem")
        klucze[nazwa] = splaszcz_json(dane)
    tylko_pl = sorted(klucze["pl"] - klucze["en"])
    tylko_en = sorted(klucze["en"] - klucze["pl"])
    lp, le = len(klucze["pl"]), len(klucze["en"])
    if not tylko_pl and not tylko_en:
        return RaportI18n(ok=True, tekst="", pl_kluczy=lp, en_kluczy=le)
    pokaz_pl = tylko_pl[:10]
    pokaz_en = tylko_en[: max(0, 10 - len(pokaz_pl))]
    pominieto = len(tylko_pl) + len(tylko_en) - len(pokaz_pl) - len(pokaz_en)

    def strona(nazwa: str, lista: list[str], pokaz: list[str]) -> str:
        if not lista:
            return f"tylko w {nazwa}: brak"
        if not pokaz:
            return f"tylko w {nazwa} ({len(lista)}): (w logu)"
        return f"tylko w {nazwa} ({len(lista)}): " + ", ".join(pokaz)

    tekst = (
        f"i18n: pl {lp} {odmien_klucz(lp)}, en {le} {odmien_klucz(le)}; "
        f"{strona('pl', tylko_pl, pokaz_pl)}; {strona('en', tylko_en, pokaz_en)}"
    )
    if pominieto:
        tekst += f" (+{pominieto} kolejnych w logu)"
    return RaportI18n(
        ok=False,
        tekst=tekst,
        pl_kluczy=lp,
        en_kluczy=le,
        tylko_pl=tylko_pl,
        tylko_en=tylko_en,
    )


# --------------------------------------------------------------------------- #
# Parsery podsumowań


@dataclass
class RaportVitest:
    pliki_fail: int = 0
    pliki_pass: int = 0
    testy_fail: int = 0
    testy_pass: int = 0
    testy_skip: int = 0
    znaleziono_pliki: bool = False
    znaleziono_testy: bool = False
    nieudane: list[str] = field(default_factory=list)


_LICZNIKI_VITEST = re.compile(r"(\d+)\s+(failed|passed|skipped)")


def parsuj_vitest(tekst: str) -> RaportVitest:
    r = RaportVitest()
    for wiersz in tekst.splitlines():
        s = wiersz.strip()
        if "Test Files" in s:
            r.znaleziono_pliki = True
            for liczba, rodzaj in _LICZNIKI_VITEST.findall(s):
                if rodzaj == "failed":
                    r.pliki_fail = int(liczba)
                elif rodzaj == "passed":
                    r.pliki_pass = int(liczba)
        elif s.startswith("Tests ") or s == "Tests":
            r.znaleziono_testy = True
            for liczba, rodzaj in _LICZNIKI_VITEST.findall(s):
                if rodzaj == "failed":
                    r.testy_fail = int(liczba)
                elif rodzaj == "passed":
                    r.testy_pass = int(liczba)
                elif rodzaj == "skipped":
                    r.testy_skip = int(liczba)
        if (
            s.startswith("FAIL")
            or s.startswith("×")
            or s.startswith("✗")
            or (s.startswith("❯") and ">" in s)
        ):
            r.nieudane.append(s)
    return r


@dataclass
class RaportDotnetTest:
    fail: int = 0
    passed: int = 0
    skipped: int = 0
    total: int = 0
    znaleziono: bool = False
    nieudane: list[str] = field(default_factory=list)


_PODSUM_EN = re.compile(
    r"Failed:\s*(\d+)\s*,\s*Passed:\s*(\d+)\s*,\s*Skipped:\s*(\d+)\s*,\s*Total:\s*(\d+)"
)
_PODSUM_DOWOLNE = re.compile(
    r"[^:,]{1,60}:\s*(\d+)\s*,\s*[^:,]{1,60}:\s*(\d+)\s*,"
    r"\s*[^:,]{1,60}:\s*(\d+)\s*,\s*[^:,]{1,60}:\s*(\d+)"
)


def parsuj_dotnet_test(tekst: str) -> RaportDotnetTest:
    r = RaportDotnetTest()
    for wiersz in tekst.splitlines():
        s = wiersz.strip()
        m = _PODSUM_EN.search(s) or _PODSUM_DOWOLNE.search(s)
        if m:
            r.znaleziono = True
            f, p, sk, t = (int(g) for g in m.groups())
            r.fail += f
            r.passed += p
            r.skipped += sk
            r.total += t
            continue
        if s.startswith("Failed ") or s.startswith("Niepowodzenie "):
            r.nieudane.append(s)
    return r


_BLAD_Z_KODEM = re.compile(r"\b(error|warning)\s+([A-Z]{1,12}\d[\dA-Za-z]*)")


def wyciagnij_dotnet_build(tekst: str) -> list[tuple[bool, str]]:
    """Unikalne linie error/warning z kodem; (czy_błąd, linia)."""
    wynik: list[tuple[bool, str]] = []
    widziane: set[str] = set()
    for wiersz in tekst.splitlines():
        s = wiersz.strip()
        m = _BLAD_Z_KODEM.search(s)
        if m and s not in widziane:
            widziane.add(s)
            wynik.append((m.group(1) == "error", s))
    return wynik


def wyciagnij_fe_build(tekst: str) -> list[tuple[bool, str]]:
    """Linie błędów i ostrzeżeń budowania FE; (czy_błąd, linia)."""
    wynik: list[tuple[bool, str]] = []
    for wiersz in tekst.splitlines():
        s = wiersz.strip()
        if "✘ [ERROR]" in s or "▲ [WARNING]" in s or "ERROR" in s or "Error:" in s:
            ostrzezenie = ("▲ [WARNING]" in s or "WARNING" in s) and (
                "✘ [ERROR]" not in s and "ERROR" not in s and "Error:" not in s
            )
            wynik.append((not ostrzezenie, s))
    return wynik


# --------------------------------------------------------------------------- #
# Logi i pozycje werdyktu


@dataclass
class Pozycja:
    blad: bool
    tekst: str
    log: str

    def linia(self) -> str:
        rodzaj = "BŁĄD" if self.blad else "OSTRZEŻENIE"
        return f"{rodzaj}: {self.tekst} [log: {self.log}]"


@dataclass
class WpisSprawdzenia:
    log: str
    opis: str
    kod: int


class Logi:
    def __init__(self, katalog: str) -> None:
        self.katalog = katalog
        os.makedirs(katalog, exist_ok=True)
        self.nr = 0
        self.sciezka00 = os.path.join(katalog, "00-werdykt-pelny.log")

    def zapisz(
        self,
        nazwa: str,
        polecenie: list[str],
        cwd: str,
        kod: int,
        out: str,
        err: str,
    ) -> str:
        self.nr += 1
        sciezka = os.path.join(self.katalog, f"{self.nr:02d}-{nazwa}.log")
        with open(sciezka, "w", encoding="utf-8") as f:
            f.write(f"polecenie: {shlex.join(polecenie)}\n")
            f.write(f"katalog: {cwd}\n")
            f.write(f"kod wyjścia: {kod}\n\n--- stdout ---\n{out}")
            if not out.endswith("\n"):
                f.write("\n")
            f.write(f"--- stderr ---\n{err}")
            if not err.endswith("\n"):
                f.write("\n")
        return sciezka


def domyslny_katalog_logow() -> str:
    kat = os.path.join(
        tempfile.gettempdir(), "fala-odbior", time.strftime("%Y%m%d-%H%M%S")
    )
    if not os.path.exists(kat):
        return kat
    i = 1
    while os.path.exists(f"{kat}-{i}"):
        i += 1
    return f"{kat}-{i}"


# --------------------------------------------------------------------------- #
# Uruchamianie sprawdzeń


def uruchom_porcjami(
    opis: str,
    baza: list[str],
    pliki: list[str],
    repo: str,
    runner: Runner,
    logi: Logi,
    prefiks_logu: str,
) -> tuple[list[Pozycja], list[WpisSprawdzenia]]:
    bledy: list[Pozycja] = []
    wpisy: list[WpisSprawdzenia] = []
    dobre: list[str] = []
    for p in pliki:
        if dlugosc_polecenia([*baza, p]) > LIMIT_POLECENIA:
            bledy.append(
                Pozycja(
                    True,
                    f"{opis}: ścieżka przekracza limit {LIMIT_POLECENIA} znaków "
                    f"polecenia i nie została sprawdzona: {p}",
                    logi.sciezka00,
                )
            )
        else:
            dobre.append(p)
    porcje = porcjuj(baza, dobre)
    for i, porcja in enumerate(porcje, 1):
        polecenie = [*baza, *porcja]
        kod, out, err = runner.run(polecenie, cwd=repo)
        nazwa = prefiks_logu if len(porcje) == 1 else f"{prefiks_logu}-{i}"
        sciezka = logi.zapisz(nazwa, polecenie, repo, kod, out, err)
        tytul = opis if len(porcje) == 1 else f"{opis} (porcja {i}/{len(porcje)})"
        wpisy.append(WpisSprawdzenia(os.path.basename(sciezka), tytul, kod))
        if kod != 0:
            bledy.append(Pozycja(True, f"{tytul}: kod wyjścia {kod}", sciezka))
    return bledy, wpisy


def uruchom_jedno(
    opis: str,
    polecenie: list[str],
    repo: str,
    runner: Runner,
    logi: Logi,
    nazwa_logu: str,
) -> tuple[int, str, str, str, WpisSprawdzenia]:
    kod, out, err = runner.run(polecenie, cwd=repo)
    sciezka = logi.zapisz(nazwa_logu, polecenie, repo, kod, out, err)
    return kod, out, err, sciezka, WpisSprawdzenia(
        os.path.basename(sciezka), opis, kod
    )


def znajdz_program(which, *nazwy: str) -> str | None:
    for n in nazwy:
        p = which(n)
        if p:
            return p
    return None


def znajdz_rozwiazanie(repo: str) -> str | None:
    try:
        wpisy = os.listdir(repo)
    except OSError:
        return None
    slnx = sorted(
        w
        for w in wpisy
        if w.lower().endswith(".slnx") and os.path.isfile(os.path.join(repo, w))
    )
    sln = sorted(
        w
        for w in wpisy
        if w.lower().endswith(".sln") and os.path.isfile(os.path.join(repo, w))
    )
    return (slnx + sln or [None])[0]


# --------------------------------------------------------------------------- #
# Odbiór


def wiersz_briefu(s: StatBriefu) -> str:
    n = len(s.pliki)
    g = " *" if s.gwiazdka else ""
    return (
        f"{s.brief.id} ({s.brief.autor}): {n} {odmien_plik(n)}, "
        f"+{s.dodane} \u2212{s.usuniete}{g}"
    )


def cmd_zapisz_baze(args: argparse.Namespace, runner: Runner) -> int:
    repo = args.repo
    if not os.path.isdir(repo):
        raise BladUzycia(f"brak repozytorium: {repo}")
    n = zapisz_baze(os.path.abspath(repo), args.zapisz_baze, runner)
    print(f"Zapisano bazę: {n} {odmien_plik(n)} → {args.zapisz_baze}")
    return 0


def cmd_odbior(args: argparse.Namespace, runner: Runner, which) -> int:
    t0 = time.monotonic()
    if not os.path.isdir(args.repo):
        raise BladUzycia(f"brak repozytorium: {args.repo}")
    repo = os.path.abspath(args.repo)
    baza = wczytaj_baze(args.baza)
    pakiet = wczytaj_pakiet(args.pakiet)
    stos = wykryj_stos(repo, pakiet.stos)
    briefy = pakiet.briefy
    if args.brief:
        wybrane = [b for b in briefy if b.id == args.brief]
        if not wybrane:
            raise BladUzycia(f"nieznany brief: {args.brief}")
        briefy = wybrane

    logi = Logi(args.katalog_logow or domyslny_katalog_logow())
    bledy: list[Pozycja] = []
    ostrzezenia: list[Pozycja] = []
    wpisy_sprawdzen: list[WpisSprawdzenia] = []

    zakres = oblicz_zakres(repo, baza, runner)
    if args.brief:
        pliki_w_zakresie = {
            p for p in zakres.pliki_fali if pasuje_do_briefu(p, briefy[0])
        }
        poza_zakresem = zakres.pliki_fali - pliki_w_zakresie
    else:
        pliki_w_zakresie = set(zakres.pliki_fali)
        poza_zakresem = set()
    wlasciciele = {
        p: [b.id for b in briefy if pasuje_do_briefu(p, b)]
        for p in pliki_w_zakresie
    }

    if zakres.head_zmieniony:
        n = zakres.commitow_przybylo
        tekst = (
            f"HEAD przesunięty o {n} {odmien_commit(n)} względem bazy"
            if n is not None
            else "HEAD różni się od bazy (nieznana liczba commitów)"
        )
        ostrzezenia.append(Pozycja(False, tekst, logi.sciezka00))
    for p in sorted(p for p, w in wlasciciele.items() if not w):
        bledy.append(
            Pozycja(
                True,
                f"plik spoza briefów (fala albo inna sesja): {p}",
                logi.sciezka00,
            )
        )
    for p in sorted(p for p, w in wlasciciele.items() if len(w) > 1):
        ostrzezenia.append(
            Pozycja(
                False,
                f"plik wspólny dla briefów {','.join(wlasciciele[p])}: {p}",
                logi.sciezka00,
            )
        )
    for b in briefy:
        if not any(b.id in w for w in wlasciciele.values()):
            ostrzezenia.append(
                Pozycja(
                    False,
                    f"brief {b.id} ({b.autor}) nie ma plików w fali",
                    logi.sciezka00,
                )
            )

    stats = statystyki(
        repo,
        baza.head,
        baza.pliki,
        briefy,
        wlasciciele,
        zakres.status.niesledzone,
        runner,
    )

    raport_i18n: RaportI18n | None = None
    pelny_wiersze: list[str] = []
    pelny_uruchomiony = bool(args.pelny and not args.brief)

    if stos == "fe":
        istniejace = sorted(
            p for p in pliki_w_zakresie if os.path.isfile(os.path.join(repo, p))
        )
        if os.name == "nt":
            npx = znajdz_program(which, "npx.cmd")
        else:
            npx = znajdz_program(which, "npx")
        if istniejace and npx is None:
            bledy.append(
                Pozycja(
                    True,
                    "nie znaleziono npx — pominięto eslint/stylelint/prettier",
                    logi.sciezka00,
                )
            )
        elif npx is not None:
            ts = [
                p
                for p in istniejace
                if os.path.splitext(p)[1].lower() in (".ts", ".html", ".js", ".mjs")
            ]
            if ts:
                be, wp = uruchom_porcjami(
                    "eslint",
                    [npx, "--no-install", "eslint", "--max-warnings", "0"],
                    ts,
                    repo,
                    runner,
                    logi,
                    "eslint",
                )
                bledy += be
                wpisy_sprawdzen += wp
            scss = [
                p
                for p in istniejace
                if os.path.splitext(p)[1].lower() == ".scss"
            ]
            if scss:
                be, wp = uruchom_porcjami(
                    "stylelint",
                    [npx, "--no-install", "stylelint"],
                    scss,
                    repo,
                    runner,
                    logi,
                    "stylelint",
                )
                bledy += be
                wpisy_sprawdzen += wp
            if istniejace:
                be, wp = uruchom_porcjami(
                    "prettier",
                    [npx, "--no-install", "prettier", "--check", "--ignore-unknown"],
                    istniejace,
                    repo,
                    runner,
                    logi,
                    "prettier",
                )
                bledy += be
                wpisy_sprawdzen += wp
        raport_i18n = sprawdz_i18n(repo)
        if not raport_i18n.ok:
            bledy.append(Pozycja(True, raport_i18n.tekst, logi.sciezka00))

    if pelny_uruchomiony and stos == "fe":
        if os.name == "nt":
            npm = znajdz_program(which, "npm.cmd")
        else:
            npm = znajdz_program(which, "npm")
        if npm is None:
            bledy.append(
                Pozycja(
                    True,
                    "nie znaleziono npm — pominięto przebiegi --pelny",
                    logi.sciezka00,
                )
            )
        else:
            kod, _o, _e, sciezka, wpis = uruchom_jedno(
                "npm run lint", [npm, "run", "lint"], repo, runner, logi, "lint"
            )
            wpisy_sprawdzen.append(wpis)
            pelny_wiersze.append(f"npm run lint: kod {kod}")
            if kod != 0:
                bledy.append(
                    Pozycja(True, f"npm run lint: kod wyjścia {kod}", sciezka)
                )
            kod, _o, _e, sciezka, wpis = uruchom_jedno(
                "npm run format:check",
                [npm, "run", "format:check"],
                repo,
                runner,
                logi,
                "format-check",
            )
            wpisy_sprawdzen.append(wpis)
            pelny_wiersze.append(f"npm run format:check: kod {kod}")
            if kod != 0:
                bledy.append(
                    Pozycja(True, f"npm run format:check: kod wyjścia {kod}", sciezka)
                )
            kod, out, err, sciezka, wpis = uruchom_jedno(
                "npm test",
                [npm, "test", "--", "--watch=false"],
                repo,
                runner,
                logi,
                "test",
            )
            wpisy_sprawdzen.append(wpis)
            vitest = parsuj_vitest(out + "\n" + err)
            if vitest.znaleziono_testy or vitest.znaleziono_pliki:
                pelny_wiersze.append(
                    f"npm test: kod {kod}; pliki {vitest.pliki_fail}/"
                    f"{vitest.pliki_fail + vitest.pliki_pass} nieudane; testy "
                    f"{vitest.testy_fail}/"
                    f"{vitest.testy_fail + vitest.testy_pass + vitest.testy_skip} "
                    f"nieudane"
                )
            else:
                pelny_wiersze.append(f"npm test: kod {kod} (brak podsumowania Vitest)")
            for nazwa in vitest.nieudane:
                pelny_wiersze.append(f"  nieudany: {nazwa}")
            if kod != 0 or vitest.testy_fail > 0 or vitest.pliki_fail > 0:
                if vitest.znaleziono_testy or vitest.znaleziono_pliki:
                    razem_t = (
                        vitest.testy_fail + vitest.testy_pass + vitest.testy_skip
                    )
                    razem_p = vitest.pliki_fail + vitest.pliki_pass
                    bledy.append(
                        Pozycja(
                            True,
                            f"npm test: {vitest.testy_fail} z {razem_t} testów "
                            f"nieudanych (pliki: {vitest.pliki_fail} z {razem_p})",
                            sciezka,
                        )
                    )
                else:
                    bledy.append(
                        Pozycja(True, f"npm test: kod wyjścia {kod}", sciezka)
                    )
            kod, out, err, sciezka, wpis = uruchom_jedno(
                "npm run build", [npm, "run", "build"], repo, runner, logi, "build"
            )
            wpisy_sprawdzen.append(wpis)
            linie = wyciagnij_fe_build(out + "\n" + err)
            pelny_wiersze.append(f"npm run build: kod {kod}")
            for czy_blad, linia in linie:
                pelny_wiersze.append(f"  {'błąd' if czy_blad else 'ostrzeżenie'}: {linia}")
            _znaleziska_budowania(
                linie, kod, "npm run build", sciezka, bledy, ostrzezenia
            )

    if pelny_uruchomiony and stos == "be":
        dotnet = znajdz_program(which, "dotnet")
        rozwiazanie = znajdz_rozwiazanie(repo)
        if dotnet is None:
            bledy.append(
                Pozycja(
                    True,
                    "nie znaleziono dotnet — pominięto przebiegi --pelny",
                    logi.sciezka00,
                )
            )
        elif rozwiazanie is None:
            bledy.append(
                Pozycja(
                    True,
                    "nie znaleziono pliku rozwiązania .slnx/.sln w korzeniu",
                    logi.sciezka00,
                )
            )
        else:
            kod, out, err, sciezka, wpis = uruchom_jedno(
                "dotnet build",
                [dotnet, "build", rozwiazanie, "-warnaserror", "-nologo", "-v", "q"],
                repo,
                runner,
                logi,
                "build",
            )
            wpisy_sprawdzen.append(wpis)
            linie = wyciagnij_dotnet_build(out + "\n" + err)
            pelny_wiersze.append(f"dotnet build {rozwiazanie}: kod {kod}")
            for czy_blad, linia in linie:
                pelny_wiersze.append(f"  {'błąd' if czy_blad else 'ostrzeżenie'}: {linia}")
            _znaleziska_budowania(
                linie, kod, "dotnet build", sciezka, bledy, ostrzezenia
            )
            kod, out, err, sciezka, wpis = uruchom_jedno(
                "dotnet test",
                [dotnet, "test", rozwiazanie, "--no-build", "-nologo", "-v", "q"],
                repo,
                runner,
                logi,
                "test",
            )
            wpisy_sprawdzen.append(wpis)
            rap = parsuj_dotnet_test(out + "\n" + err)
            if rap.znaleziono:
                pelny_wiersze.append(
                    f"dotnet test: kod {kod}; Failed: {rap.fail}, "
                    f"Passed: {rap.passed}, Skipped: {rap.skipped}, Total: {rap.total}"
                )
            else:
                pelny_wiersze.append(f"dotnet test: kod {kod} (brak podsumowania)")
            for nazwa in rap.nieudane:
                pelny_wiersze.append(f"  nieudany: {nazwa}")
            if kod != 0 or (rap.znaleziono and rap.fail > 0):
                if rap.znaleziono:
                    bledy.append(
                        Pozycja(
                            True,
                            f"dotnet test: Failed {rap.fail}, Passed {rap.passed}, "
                            f"Skipped {rap.skipped}, Total {rap.total}",
                            sciezka,
                        )
                    )
                else:
                    bledy.append(
                        Pozycja(True, f"dotnet test: kod wyjścia {kod}", sciezka)
                    )
            if rap.znaleziono and rap.skipped > 100:
                ustawiona = "ZEBRANI_TEST_SQLSERVER" in os.environ
                stan = "ustawiona" if ustawiona else "brak"
                ostrzezenia.append(
                    Pozycja(
                        False,
                        f"pominięto {rap.skipped} testów — czy ustawiono "
                        f"ZEBRANI_TEST_SQLSERVER? (zmienna: {stan})",
                        sciezka,
                    )
                )
            pelny_wiersze.append(
                "ZEBRANI_TEST_SQLSERVER: "
                + ("ustawiona" if "ZEBRANI_TEST_SQLSERVER" in os.environ else "brak")
            )

    poziom = "BŁĘDY" if bledy else ("OSTRZEŻENIA" if ostrzezenia else "OK")
    pozycje = bledy + ostrzezenia
    czas_s = time.monotonic() - t0
    n = len(pliki_w_zakresie)
    wiersz_werdyktu = f"WERDYKT: {poziom} ({stos}, {n} {odmien_plik(n)} fali, {czas_s:.1f}s)"

    wiersze = [wiersz_werdyktu]
    wiersze_briefow = [wiersz_briefu(s) for s in stats]
    if len(wiersze_briefow) > LIMIT_BRIEFOW_WERDYKT:
        pokaz = LIMIT_BRIEFOW_WERDYKT - 1
        wiersze_briefow = wiersze_briefow[:pokaz] + [
            f"+{len(stats) - pokaz} briefów — szczegóły w logu"
        ]
    wiersze += wiersze_briefow
    miejsce = LIMIT_WIERSZY - len(wiersze) - 1
    if len(pozycje) > miejsce:
        pokaz = max(0, miejsce - 1)
        wiersze += [p.linia() for p in pozycje[:pokaz]]
        wiersze.append(f"+{len(pozycje) - pokaz} kolejnych pozycji w {logi.sciezka00}")
    else:
        wiersze += [p.linia() for p in pozycje]
    wiersze.append(f"logi: {logi.katalog}")
    assert len(wiersze) <= LIMIT_WIERSZY

    pelny = _buduj_werdykt_pelny(
        wiersz_werdyktu=wiersz_werdyktu,
        args=args,
        repo=repo,
        baza=baza,
        stos=stos,
        zakres=zakres,
        briefy=briefy,
        stats=stats,
        wlasciciele=wlasciciele,
        pliki_w_zakresie=pliki_w_zakresie,
        poza_zakresem=poza_zakresem,
        bledy=bledy,
        ostrzezenia=ostrzezenia,
        raport_i18n=raport_i18n,
        wpisy_sprawdzen=wpisy_sprawdzen,
        pelny_wiersze=pelny_wiersze,
        pelny_uruchomiony=pelny_uruchomiony,
        pelny_pominiety=bool(args.pelny and args.brief),
    )
    with open(logi.sciezka00, "w", encoding="utf-8") as f:
        f.write(pelny)
    print("\n".join(wiersze))
    return 1 if bledy else 0


def _znaleziska_budowania(
    linie: list[tuple[bool, str]],
    kod: int,
    opis: str,
    sciezka_logu: str,
    bledy: list[Pozycja],
    ostrzezenia: list[Pozycja],
) -> None:
    if kod == 0:
        for czy_blad, linia in linie[:10]:
            if not czy_blad:
                ostrzezenia.append(
                    Pozycja(False, f"{opis}: {linia}", sciezka_logu)
                )
        return
    wybrane = [(True, l) for c, l in linie if c] + [
        (False, l) for c, l in linie if not c
    ]
    wybrane = wybrane[:10]
    for czy_blad, linia in wybrane:
        (bledy if czy_blad else ostrzezenia).append(
            Pozycja(czy_blad, f"{opis}: {linia}", sciezka_logu)
        )
    if not any(czy_blad for czy_blad, _linia in wybrane):
        bledy.append(Pozycja(True, f"{opis}: kod wyjścia {kod}", sciezka_logu))


def _buduj_werdykt_pelny(
    wiersz_werdyktu: str,
    args: argparse.Namespace,
    repo: str,
    baza: Baza,
    stos: str,
    zakres: ZakresFali,
    briefy: list[Brief],
    stats: list[StatBriefu],
    wlasciciele: dict[str, list[str]],
    pliki_w_zakresie: set[str],
    poza_zakresem: set[str],
    bledy: list[Pozycja],
    ostrzezenia: list[Pozycja],
    raport_i18n: RaportI18n | None,
    wpisy_sprawdzen: list[WpisSprawdzenia],
    pelny_wiersze: list[str],
    pelny_uruchomiony: bool,
    pelny_pominiety: bool,
) -> str:
    s: list[str] = [wiersz_werdyktu]
    s.append(f"repo: {repo}")
    s.append(f"baza: {args.baza} (HEAD {baza.head}, zapis {baza.czas})")
    if zakres.head_zmieniony:
        n = zakres.commitow_przybylo
        s.append(
            f"HEAD bieżący: {zakres.head} "
            f"(+{n} {odmien_commit(n)} względem bazy)"
            if n is not None
            else f"HEAD bieżący: {zakres.head} (różni się od bazy)"
        )
    else:
        s.append(f"HEAD bieżący: {zakres.head} (bez zmian)")
    s.append(f"stos: {stos}")
    s.append(f"filtr brief: {args.brief if args.brief else '—'}")
    n = len(pliki_w_zakresie)
    s.append(f"plików w fali: {n}")
    s.append("")
    s.append("[BRIEFY]")
    for st in stats:
        s.append(wiersz_briefu(st))
        if not st.pliki:
            s.append("  (brak plików w fali)")
        for p in st.pliki:
            adnotacje: list[str] = []
            if p in baza.pliki:
                adnotacje.append("*")
            if not os.path.isfile(os.path.join(repo, p)):
                adnotacje.append("(usunięty)")
            elif p in zakres.status.niesledzone:
                adnotacje.append("(nowy)")
            wsp = wlasciciele.get(p, [])
            if len(wsp) > 1:
                adnotacje.append(f"(wspólny: {','.join(wsp)})")
            s.append(f"  {p}" + (" " + " ".join(adnotacje) if adnotacje else ""))
    if any(st.gwiazdka for st in stats):
        s.append("* statystyka obejmuje zmiany sprzed fali")
    s.append("")
    s.append("[PLIKI SPOZA BRIEFÓW]")
    bez = sorted(p for p, w in wlasciciele.items() if not w)
    s.append("  (brak)" if not bez else "\n".join(f"  {p}" for p in bez))
    s.append("")
    s.append("[BŁĘDY]")
    s.append("  (brak)" if not bledy else "\n".join(f"  {p.linia()}" for p in bledy))
    s.append("")
    s.append("[OSTRZEŻENIA]")
    s.append(
        "  (brak)"
        if not ostrzezenia
        else "\n".join(f"  {p.linia()}" for p in ostrzezenia)
    )
    s.append("")
    s.append("[ZNIKNĘŁY Z LISTY ZMIAN BEZ ZMIANY TREŚCI]")
    if not zakres.zniknely:
        s.append("  (brak)")
    else:
        for p in sorted(zakres.zniknely):
            s.append(f"  {p} — zniknął z listy zmian bez zmiany treści")
    if args.brief:
        s.append("")
        s.append(f"[POZA ZAKRESEM --brief {args.brief}]")
        s.append(
            "  (brak)"
            if not poza_zakresem
            else "\n".join(f"  {p}" for p in sorted(poza_zakresem))
        )
    if raport_i18n is not None:
        s.append("")
        s.append("[I18N]")
        if raport_i18n.pl_kluczy is None or raport_i18n.en_kluczy is None:
            s.append(f"  {raport_i18n.tekst}")
        else:
            lp, le = raport_i18n.pl_kluczy, raport_i18n.en_kluczy
            s.append(f"  pl.json: {lp} {odmien_klucz(lp)}; en.json: {le} {odmien_klucz(le)}")
            if raport_i18n.ok:
                s.append("  klucze zgodne")
            else:
                s.append(f"  tylko w pl ({len(raport_i18n.tylko_pl)}):")
                for k in raport_i18n.tylko_pl:
                    s.append(f"    {k}")
                s.append(f"  tylko w en ({len(raport_i18n.tylko_en)}):")
                for k in raport_i18n.tylko_en:
                    s.append(f"    {k}")
    s.append("")
    s.append("[SPRAWDZENIA]")
    if not wpisy_sprawdzen:
        s.append("  (brak uruchomionych sprawdzeń)")
    for w in wpisy_sprawdzen:
        s.append(f"  {w.log}: {w.opis}: kod {w.kod}")
    if pelny_uruchomiony or pelny_pominiety:
        s.append("")
        s.append("[PEŁNY]")
        if pelny_pominiety:
            s.append("  (pominięto — aktywny filtr --brief)")
        for wiersz in pelny_wiersze:
            s.append(f"  {wiersz}" if not wiersz.startswith("  ") else wiersz)
    return "\n".join(s) + "\n"


# --------------------------------------------------------------------------- #
# CLI


def parser_argumentow() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="fala-odbior.py",
        description="Odbiór fali briefów: zakres względem bazy, sprawdzenia, werdykt.",
    )
    p.add_argument("--repo", required=True, help="ścieżka repozytorium")
    p.add_argument(
        "--zapisz-baze", metavar="PLIK", default=None, help="zapisz bazę fali do pliku JSON"
    )
    p.add_argument("--baza", metavar="PLIK", default=None, help="plik JSON z bazą fali")
    p.add_argument("--pakiet", metavar="PLIK", default=None, help="plik JSON z pakietem briefów")
    p.add_argument("--brief", metavar="ID", default=None, help="odbiór tylko plików jednego briefu")
    p.add_argument(
        "--pelny",
        action="store_true",
        help="pełne przebiegi (lint/test/build); pomijane z --brief",
    )
    p.add_argument("--katalog-logow", metavar="KAT", default=None, help="katalog logów")
    p.add_argument(
        "--limit-czasu",
        metavar="MINUTY",
        type=float,
        default=60,
        help="limit czasu na każde polecenie w minutach (domyślnie 60)",
    )
    return p


def main(
    argv: list[str] | None = None, runner: Runner | None = None, which=None
) -> int:
    args = parser_argumentow().parse_args(argv)
    which = which or shutil.which
    try:
        if args.limit_czasu is None or args.limit_czasu <= 0:
            raise BladUzycia("--limit-czasu musi być dodatnie")
        runner = runner or Runner(limit_sekund=args.limit_czasu * 60)
        if args.zapisz_baze is not None:
            if args.baza is not None or args.pakiet is not None:
                raise BladUzycia("nie łącz --zapisz-baze z --baza/--pakiet")
            return cmd_zapisz_baze(args, runner)
        if args.baza is None or args.pakiet is None:
            raise BladUzycia("odbiór wymaga --baza i --pakiet")
        return cmd_odbior(args, runner, which)
    except BladUzycia as e:
        print(f"Błąd: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    # Windows z przekierowanym wyjściem koduje stdout w stronie kodowej
    # konsoli (np. cp1250), która nie ma znaków „→” i „−” z werdyktu.
    for _strumien in (sys.stdout, sys.stderr):
        if hasattr(_strumien, "reconfigure"):
            _strumien.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
