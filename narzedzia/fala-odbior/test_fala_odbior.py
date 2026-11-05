"""Testy skryptu fala-odbior.py (unittest, tylko biblioteka standardowa)."""

import contextlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

TUTAJ = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(TUTAJ, ".tmp-test")

_spec = importlib.util.spec_from_file_location(
    "fala_odbior", os.path.join(TUTAJ, "fala-odbior.py")
)
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)

MINUS = "\u2212"


def git(repo, *args):
    p = subprocess.run(
        ["git", *args],
        cwd=repo,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert p.returncode == 0, f"git {args}: {p.stderr}"
    return p.stdout.strip()


def fake_which(nazwa):
    return "C:\\narzedzia-fake\\" + nazwa


class FakeRunner:
    """Git prawdziwy, reszta poleceń z gotowych odpowiedzi."""

    def __init__(self, odpowiedzi=None):
        self.odpowiedzi = odpowiedzi or {}
        self.wywolania = []

    def _klucz(self, args):
        prog = os.path.basename(args[0]).lower()
        rest = list(args[1:])
        if prog in ("npm", "npm.cmd"):
            if rest[:1] == ["run"] and len(rest) > 1:
                return "npm run " + rest[1]
            if rest[:1] == ["test"]:
                return "npm test"
            return "npm " + " ".join(rest)
        if prog in ("npx", "npx.cmd"):
            for znany in ("eslint", "stylelint", "prettier"):
                if znany in rest:
                    return "npx " + znany
            return "npx"
        if prog in ("dotnet", "dotnet.exe"):
            return "dotnet " + (rest[0] if rest else "")
        return prog

    def run(self, args, cwd=None, input=None):
        self.wywolania.append(list(args))
        if os.path.basename(args[0]).lower() in ("git", "git.exe"):
            return mod.Runner().run(args, cwd=cwd, input=input)
        if self._klucz(args) in self.odpowiedzi:
            return self.odpowiedzi[self._klucz(args)]
        return (0, "", "")


def _usun_drzewo(sciezka):
    def przy_bledzie(funkcja, cel, _info):
        try:
            os.chmod(cel, 0o700)
            funkcja(cel)
        except OSError:
            pass

    shutil.rmtree(sciezka, onerror=przy_bledzie)


class BazaTestow(unittest.TestCase):
    def setUp(self):
        os.makedirs(TMP, exist_ok=True)

    def tearDown(self):
        _usun_drzewo(TMP)

    def nowe_repo(self):
        repo = tempfile.mkdtemp(prefix="repo-", dir=TMP)
        git(repo, "init", "-q", "-b", "main")
        git(repo, "config", "user.email", "test@test.pl")
        git(repo, "config", "user.name", "test")
        git(repo, "config", "commit.gpgsign", "false")
        return repo

    def pisz(self, repo, rel, tresc):
        pelna = os.path.join(repo, rel)
        os.makedirs(os.path.dirname(pelna), exist_ok=True)
        with open(pelna, "w", encoding="utf-8", newline="") as f:
            f.write(tresc)
        return pelna

    def commituj(self, repo, komunikat="x"):
        git(repo, "add", "-A")
        git(repo, "commit", "-qm", komunikat)

    def dodaj_i18n(self, repo, pl=None, en=None):
        self.pisz(
            repo,
            "src/assets/i18n/pl.json",
            json.dumps(pl if pl is not None else {"a": {"b": 1}}, ensure_ascii=False),
        )
        self.pisz(
            repo,
            "src/assets/i18n/en.json",
            json.dumps(en if en is not None else {"a": {"b": 1}}, ensure_ascii=False),
        )

    def uruchom(self, argv, runner=None):
        runner = runner or FakeRunner()
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            kod = mod.main(argv, runner=runner, which=fake_which)
        return kod, out.getvalue(), err.getvalue(), runner

    def zapisz_baze(self, repo):
        baza = os.path.join(TMP, f"baza-{os.path.basename(repo)}.json")
        kod, out, err, _r = self.uruchom(["--repo", repo, "--zapisz-baze", baza])
        self.assertEqual(kod, 0, err)
        return baza, out

    def pakiet(self, repo, briefy, stos="be"):
        sciezka = os.path.join(TMP, f"pakiet-{os.path.basename(repo)}.json")
        with open(sciezka, "w", encoding="utf-8") as f:
            json.dump({"stos": stos, "briefy": briefy}, f, ensure_ascii=False)
        return sciezka

    def odbior(self, repo, baza, pakiet, extra=None, runner=None):
        logi = tempfile.mkdtemp(prefix="logi-", dir=TMP)
        argv = [
            "--repo", repo, "--baza", baza, "--pakiet", pakiet,
            "--katalog-logow", logi,
        ] + (extra or [])
        kod, out, err, runner = self.uruchom(argv, runner=runner)
        with open(os.path.join(logi, "00-werdykt-pelny.log"), encoding="utf-8") as f:
            pelny = f.read()
        return kod, out, err, pelny, logi, runner

    def zakres(self, repo, baza):
        return mod.oblicz_zakres(repo, mod.wczytaj_baze(baza), mod.Runner())


class TestZakresu(BazaTestow):
    def test_zmiana_sprzed_bazy_nie_nalezy_do_fali(self):
        repo = self.nowe_repo()
        self.pisz(repo, "a.txt", "v1\n")
        self.commituj(repo)
        self.pisz(repo, "a.txt", "v2\n")
        baza, _o = self.zapisz_baze(repo)
        z = self.zakres(repo, baza)
        self.assertNotIn("a.txt", z.pliki_fali)
        self.assertFalse(z.head_zmieniony)

    def test_commit_bez_zmiany_tresci_nie_nalezy_do_fali(self):
        repo = self.nowe_repo()
        self.pisz(repo, "a.txt", "v1\n")
        self.commituj(repo)
        self.pisz(repo, "a.txt", "v2\n")
        baza, _o = self.zapisz_baze(repo)
        self.commituj(repo, "cudzy commit")
        z = self.zakres(repo, baza)
        self.assertNotIn("a.txt", z.pliki_fali)
        self.assertIn("a.txt", z.zniknely)
        self.assertTrue(z.head_zmieniony)
        self.assertEqual(z.commitow_przybylo, 1)

    def test_zmiana_i_commit_w_fali_nalezy_do_fali(self):
        repo = self.nowe_repo()
        self.pisz(repo, "a.txt", "v1\n")
        self.commituj(repo)
        baza, _o = self.zapisz_baze(repo)
        self.pisz(repo, "a.txt", "v2\n")
        self.commituj(repo, "fala")
        z = self.zakres(repo, baza)
        self.assertIn("a.txt", z.pliki_fali)
        self.assertTrue(z.head_zmieniony)

    def test_rename_commit_w_fali_obie_sciezki_naleza(self):
        repo = self.nowe_repo()
        self.pisz(repo, "stary.txt", "tresc\n")
        self.commituj(repo)
        baza, _o = self.zapisz_baze(repo)
        git(repo, "mv", "stary.txt", "nowy.txt")
        self.commituj(repo, "rename")
        z = self.zakres(repo, baza)
        self.assertIn("stary.txt", z.pliki_fali)
        self.assertIn("nowy.txt", z.pliki_fali)

    def test_rename_widoczny_w_odbiorze(self):
        repo = self.nowe_repo()
        self.pisz(repo, "stary.txt", "tresc\n")
        self.commituj(repo)
        baza, _o = self.zapisz_baze(repo)
        git(repo, "mv", "stary.txt", "nowy.txt")
        self.commituj(repo, "rename")
        pakiet = self.pakiet(repo, [{"id": "B1", "autor": "t", "pliki": ["*.txt"]}])
        kod, out, _e, pelny, _l, _r = self.odbior(repo, baza, pakiet)
        self.assertEqual(kod, 0)
        self.assertIn("stary.txt", pelny)
        self.assertIn("nowy.txt", pelny)
        self.assertIn("(usunięty)", pelny)
        self.assertIn("przesunięty o 1 commit", out)

    def test_autocrlf_nie_daje_falszywej_zmiany(self):
        repo = self.nowe_repo()
        git(repo, "config", "core.autocrlf", "true")
        self.pisz(repo, "a.txt", "l1\r\nl2\r\n")
        self.commituj(repo)
        os.remove(os.path.join(repo, "a.txt"))
        git(repo, "checkout", "--", "a.txt")
        with open(os.path.join(repo, "a.txt"), "rb") as f:
            self.assertIn(b"\r\n", f.read())
        self.assertEqual(git(repo, "status", "--porcelain"), "")
        baza, _o = self.zapisz_baze(repo)
        z = self.zakres(repo, baza)
        self.assertEqual(z.pliki_fali, set())
        runner = mod.Runner()
        head = git(repo, "rev-parse", "HEAD")
        self.assertEqual(
            runner.run(["git", "hash-object", "--stdin-paths"], cwd=repo, input="a.txt\n")[1].strip(),
            runner.run(["git", "rev-parse", f"{head}:a.txt"], cwd=repo)[1].strip(),
        )

    def test_ponowna_zmiana_w_fali_nalezy(self):
        repo = self.nowe_repo()
        self.pisz(repo, "a.txt", "v1\n")
        self.commituj(repo)
        self.pisz(repo, "a.txt", "v2\n")
        baza, _o = self.zapisz_baze(repo)
        self.pisz(repo, "a.txt", "v3\n")
        z = self.zakres(repo, baza)
        self.assertIn("a.txt", z.pliki_fali)

    def test_nowy_niesledzony_nalezy(self):
        repo = self.nowe_repo()
        self.pisz(repo, "a.txt", "v1\n")
        self.commituj(repo)
        baza, _o = self.zapisz_baze(repo)
        self.pisz(repo, "nowy.txt", "n\n")
        z = self.zakres(repo, baza)
        self.assertIn("nowy.txt", z.pliki_fali)

    def test_usuniecie_w_fali_nalezy(self):
        repo = self.nowe_repo()
        self.pisz(repo, "a.txt", "l1\nl2\nl3\n")
        self.commituj(repo)
        baza, _o = self.zapisz_baze(repo)
        os.remove(os.path.join(repo, "a.txt"))
        z = self.zakres(repo, baza)
        self.assertIn("a.txt", z.pliki_fali)

    def test_usuniecie_statystyka_minus(self):
        repo = self.nowe_repo()
        self.pisz(repo, "a.txt", "l1\nl2\nl3\n")
        self.commituj(repo)
        baza, _o = self.zapisz_baze(repo)
        os.remove(os.path.join(repo, "a.txt"))
        pakiet = self.pakiet(repo, [{"id": "B1", "autor": "t", "pliki": ["a.txt"]}])
        kod, out, _e, _p, _l, _r = self.odbior(repo, baza, pakiet)
        self.assertEqual(kod, 0)
        self.assertIn(f"+0 {MINUS}3", out)


class TestPrzypisania(BazaTestow):
    def test_bez_wlasciciela_blad_i_kod_1(self):
        repo = self.nowe_repo()
        self.pisz(repo, "a.txt", "v1\n")
        self.commituj(repo)
        baza, _o = self.zapisz_baze(repo)
        self.pisz(repo, "obcy.txt", "x\n")
        pakiet = self.pakiet(repo, [{"id": "B1", "autor": "t", "pliki": ["src/**"]}])
        kod, out, _e, pelny, logi, _r = self.odbior(repo, baza, pakiet)
        self.assertEqual(kod, 1)
        self.assertIn("WERDYKT: BŁĘDY", out)
        self.assertIn("plik spoza briefów (fala albo inna sesja): obcy.txt", out)
        self.assertIn("obcy.txt", pelny)
        self.assertEqual(os.listdir(logi), ["00-werdykt-pelny.log"])

    def test_w_dwoch_briefach_ostrzezenie(self):
        repo = self.nowe_repo()
        self.pisz(repo, "a.txt", "v1\n")
        self.commituj(repo)
        baza, _o = self.zapisz_baze(repo)
        self.pisz(repo, "f.ts", "x\n")
        pakiet = self.pakiet(
            repo,
            [
                {"id": "B1", "autor": "a1", "pliki": ["*.ts"]},
                {"id": "B2", "autor": "a2", "pliki": ["f.*"]},
            ],
        )
        kod, out, _e, _p, _l, _r = self.odbior(repo, baza, pakiet)
        self.assertEqual(kod, 0)
        self.assertIn("WERDYKT: OSTRZEŻENIA", out)
        self.assertIn("plik wspólny dla briefów B1,B2: f.ts", out)

    def test_brief_zweza_zakres(self):
        repo = self.nowe_repo()
        self.pisz(repo, "a.txt", "v1\n")
        self.commituj(repo)
        baza, _o = self.zapisz_baze(repo)
        self.pisz(repo, "b1.txt", "x\n")
        self.pisz(repo, "b2.txt", "x\n")
        self.pisz(repo, "obcy.txt", "x\n")
        pakiet = self.pakiet(
            repo,
            [
                {"id": "B1", "autor": "a1", "pliki": ["b1*"]},
                {"id": "B2", "autor": "a2", "pliki": ["b2*"]},
            ],
        )
        kod, _o, _e, _p, _l, _r = self.odbior(repo, baza, pakiet)
        self.assertEqual(kod, 1)
        kod, out, _e, pelny, _l, _r = self.odbior(
            repo, baza, pakiet, extra=["--brief", "B1"]
        )
        self.assertEqual(kod, 0)
        self.assertIn("B1 (a1)", out)
        self.assertNotIn("B2 (a2)", out)
        self.assertIn("[POZA ZAKRESEM --brief B1]", pelny)
        self.assertIn("b2.txt", pelny)
        self.assertIn("obcy.txt", pelny)

    def test_brief_bez_plikow_ostrzezenie(self):
        repo = self.nowe_repo()
        self.pisz(repo, "a.txt", "v1\n")
        self.commituj(repo)
        baza, _o = self.zapisz_baze(repo)
        self.pisz(repo, "f.txt", "x\n")
        pakiet = self.pakiet(
            repo,
            [
                {"id": "B1", "autor": "a1", "pliki": ["f.txt"]},
                {"id": "B2", "autor": "a2", "pliki": ["nie-ma/**"]},
            ],
        )
        kod, out, _e, _p, _l, _r = self.odbior(repo, baza, pakiet)
        self.assertEqual(kod, 0)
        self.assertIn("brief B2 (a2) nie ma plików w fali", out)

    def test_zniknal_z_listy_zmian_w_logu(self):
        repo = self.nowe_repo()
        self.pisz(repo, "a.txt", "v1\n")
        self.commituj(repo)
        self.pisz(repo, "a.txt", "v2\n")
        baza, _o = self.zapisz_baze(repo)
        self.commituj(repo, "cudzy")
        pakiet = self.pakiet(repo, [{"id": "B1", "autor": "t", "pliki": ["zzz/**"]}])
        kod, out, _e, pelny, _l, _r = self.odbior(repo, baza, pakiet)
        self.assertEqual(kod, 0)
        self.assertIn("WERDYKT: OSTRZEŻENIA", out)
        self.assertIn("a.txt — zniknął z listy zmian bez zmiany treści", pelny)


class TestGloby(unittest.TestCase):
    def test_gwiazdka_nie_przechodzi_przez_ukosnik(self):
        g = "src/app/logged/contacts/components/list/*"
        self.assertTrue(
            mod.dopasuj_glob(g, "src/app/logged/contacts/components/list/X.ts")
        )
        self.assertFalse(
            mod.dopasuj_glob(g, "src/app/logged/contacts/components/list/sub/X.ts")
        )
        self.assertTrue(mod.dopasuj_glob("src/assets/i18n/*.json", "src/assets/i18n/pl.json"))
        self.assertFalse(
            mod.dopasuj_glob("src/assets/i18n/*.json", "src/assets/i18n/a/pl.json")
        )
        self.assertTrue(mod.dopasuj_glob("*.ts", "a.ts"))
        self.assertFalse(mod.dopasuj_glob("*.ts", "d/a.ts"))

    def test_dwie_gwiazdki_przechodza(self):
        g = "src/app/logged/dashboard/**"
        self.assertTrue(mod.dopasuj_glob(g, "src/app/logged/dashboard/a.ts"))
        self.assertTrue(mod.dopasuj_glob(g, "src/app/logged/dashboard/a/b/c.ts"))
        self.assertFalse(mod.dopasuj_glob(g, "src/app/logged/inne/a.ts"))
        self.assertTrue(mod.dopasuj_glob("**/*.json", "x.json"))
        self.assertTrue(mod.dopasuj_glob("**/*.json", "a/b/x.json"))
        self.assertTrue(mod.dopasuj_glob("**", "a/b/c.ts"))


class TestI18n(BazaTestow):
    def test_brakujacy_klucz_w_en_daje_blad(self):
        repo = self.nowe_repo()
        self.dodaj_i18n(repo, pl={"a": {"b": 1}, "c": 2}, en={"a": {}})
        self.pisz(repo, "a.txt", "v1\n")
        self.commituj(repo)
        baza, _o = self.zapisz_baze(repo)
        self.pisz(repo, "f.txt", "x\n")
        pakiet = self.pakiet(
            repo, [{"id": "B1", "autor": "t", "pliki": ["f.txt"]}], stos="fe"
        )
        kod, out, _e, pelny, _l, _r = self.odbior(repo, baza, pakiet)
        self.assertEqual(kod, 1)
        self.assertIn("BŁĄD: i18n:", out)
        self.assertIn("a.b", out)
        self.assertIn("c", out)
        self.assertIn("    a.b", pelny)
        self.assertIn("    c", pelny)

    def test_zgodne_klucze_ok(self):
        repo = self.nowe_repo()
        self.dodaj_i18n(repo, pl={"a": {"b": 1}}, en={"a": {"b": 2}})
        self.pisz(repo, "a.txt", "v1\n")
        self.commituj(repo)
        baza, _o = self.zapisz_baze(repo)
        self.pisz(repo, "f.txt", "x\n")
        pakiet = self.pakiet(
            repo, [{"id": "B1", "autor": "t", "pliki": ["f.txt"]}], stos="fe"
        )
        kod, out, _e, pelny, _l, _r = self.odbior(repo, baza, pakiet)
        self.assertEqual(kod, 0)
        self.assertIn("WERDYKT: OK", out)
        self.assertIn("klucze zgodne", pelny)

    def test_brak_pliku_i18n_daje_blad(self):
        repo = self.nowe_repo()
        self.pisz(repo, "a.txt", "v1\n")
        self.commituj(repo)
        baza, _o = self.zapisz_baze(repo)
        pakiet = self.pakiet(repo, [{"id": "B1", "autor": "t", "pliki": ["f.txt"]}], stos="fe")
        kod, out, _e, _p, _l, _r = self.odbior(repo, baza, pakiet)
        self.assertEqual(kod, 1)
        self.assertIn("i18n: brak pliku", out)


class TestParsery(unittest.TestCase):
    VITEST = (
        "RUN  v3.2.4 /repo\n"
        "❯ src/a.spec.ts (2 tests | 1 failed)\n"
        "× powinno sumować\n"
        "✓ powinno odejmować\n"
        "FAIL  src/b.spec.ts > kalkulator > powinno mnożyć\n"
        "❯ src/c.spec.ts > s > t nieudany\n"
        " Test Files  2 failed | 3 passed (5)\n"
        "      Tests  3 failed | 10 passed | 1 skipped (14)\n"
    )

    def test_vitest(self):
        r = mod.parsuj_vitest(self.VITEST)
        self.assertTrue(r.znaleziono_pliki)
        self.assertTrue(r.znaleziono_testy)
        self.assertEqual((r.pliki_fail, r.pliki_pass), (2, 3))
        self.assertEqual((r.testy_fail, r.testy_pass, r.testy_skip), (3, 10, 1))
        self.assertEqual(
            r.nieudane,
            [
                "× powinno sumować",
                "FAIL  src/b.spec.ts > kalkulator > powinno mnożyć",
                "❯ src/c.spec.ts > s > t nieudany",
            ],
        )

    DOTNET = (
        "  Passed! - Failed: 0, Passed: 5, Skipped: 0, Total: 5, Duration: 1 s\n"
        "  Failed! - Failed: 2, Passed: 20, Skipped: 1, Total: 23, Duration: 5 s\n"
        "Failed MyNs.Klasa.Test1\n"
        "Failed MyNs.Klasa.Test2 [1 ms]\n"
    )

    def test_dotnet_test_sumuje(self):
        r = mod.parsuj_dotnet_test(self.DOTNET)
        self.assertTrue(r.znaleziono)
        self.assertEqual((r.fail, r.passed, r.skipped, r.total), (2, 25, 1, 28))
        self.assertEqual(
            r.nieudane, ["Failed MyNs.Klasa.Test1", "Failed MyNs.Klasa.Test2 [1 ms]"]
        )

    def test_dotnet_test_wariant_po_polsku(self):
        r = mod.parsuj_dotnet_test("Niepowodzenie: 1, Zaliczone: 5, Pominięte: 0, Razem: 6\n")
        self.assertTrue(r.znaleziono)
        self.assertEqual((r.fail, r.passed, r.skipped, r.total), (1, 5, 0, 6))

    def test_dotnet_build_unikalne(self):
        tekst = (
            "src/A.cs(10,5): error CS1234: coś\n"
            "src/A.cs(10,5): error CS1234: coś\n"
            "src/B.cs(1,1): warning CA1000: coś\n"
        )
        self.assertEqual(
            mod.wyciagnij_dotnet_build(tekst),
            [
                (True, "src/A.cs(10,5): error CS1234: coś"),
                (False, "src/B.cs(1,1): warning CA1000: coś"),
            ],
        )

    def test_fe_build_klasyfikacja(self):
        tekst = (
            "✘ [ERROR] Could not resolve 'x'\n"
            "▲ [WARNING] chunk duży\n"
            "Error: build nieudany\n"
        )
        self.assertEqual(
            mod.wyciagnij_fe_build(tekst),
            [
                (True, "✘ [ERROR] Could not resolve 'x'"),
                (False, "▲ [WARNING] chunk duży"),
                (True, "Error: build nieudany"),
            ],
        )


class TestWyjscie(BazaTestow):
    def _sprawdz_werdykt(self, out):
        wiersze = out.splitlines()
        self.assertLessEqual(len(wiersze), 40)
        self.assertTrue(wiersze[0].startswith("WERDYKT:"))
        self.assertTrue(wiersze[-1].startswith("logi:"))
        return wiersze

    def test_100_plikow(self):
        repo = self.nowe_repo()
        self.pisz(repo, "a.txt", "v1\n")
        self.commituj(repo)
        baza, _o = self.zapisz_baze(repo)
        for i in range(100):
            self.pisz(repo, f"f{i:03d}.txt", "x\n")
        pakiet = self.pakiet(repo, [{"id": "B1", "autor": "t", "pliki": ["*.txt"]}])
        kod, out, _e, _p, _l, _r = self.odbior(repo, baza, pakiet)
        self.assertEqual(kod, 0)
        self._sprawdz_werdykt(out)
        self.assertIn("100 plików fali", out)
        self.assertIn(f"+100 {MINUS}0", out)

    def test_20_briefow(self):
        repo = self.nowe_repo()
        self.pisz(repo, "a.txt", "v1\n")
        self.commituj(repo)
        baza, _o = self.zapisz_baze(repo)
        briefy = []
        for i in range(20):
            self.pisz(repo, f"f{i:02d}.txt", "x\n")
            briefy.append({"id": f"B{i:02d}", "autor": "t", "pliki": [f"f{i:02d}.txt"]})
        pakiet = self.pakiet(repo, briefy)
        kod, out, _e, _p, _l, _r = self.odbior(repo, baza, pakiet)
        self.assertEqual(kod, 0)
        wiersze = self._sprawdz_werdykt(out)
        self.assertIn("+9 briefów — szczegóły w logu", wiersze)

    def test_60_bledow(self):
        repo = self.nowe_repo()
        self.pisz(repo, "a.txt", "v1\n")
        self.commituj(repo)
        baza, _o = self.zapisz_baze(repo)
        for i in range(60):
            self.pisz(repo, f"e{i:02d}.txt", "x\n")
        pakiet = self.pakiet(repo, [{"id": "B1", "autor": "t", "pliki": ["nic/**"]}])
        kod, out, _e, _p, _l, _r = self.odbior(repo, baza, pakiet)
        self.assertEqual(kod, 1)
        wiersze = self._sprawdz_werdykt(out)
        self.assertTrue(any("kolejnych pozycji w" in w for w in wiersze[:-1]))
        self.assertEqual(wiersze[-2].split()[0], "+25")


class TestPorcjowanie(BazaTestow):
    def test_porcjuj_dzial(self):
        baza = ["npx", "--no-install", "eslint"]
        pliki = [f"plik-{i:03d}.ts" for i in range(50)]
        porcje = mod.porcjuj(baza, pliki)
        self.assertGreaterEqual(len(porcje), 1)
        for porcja in porcje:
            self.assertLessEqual(mod.dlugosc_polecenia([*baza, *porcja]), 7000)
        laczenie = [p for porcja in porcje for p in porcja]
        self.assertEqual(laczenie, pliki)

    def test_porcjuj_wiele_porcji(self):
        baza = ["npx", "--no-install", "eslint"]
        pliki = [f"{'x' * 100}-{i:03d}.ts" for i in range(100)]
        porcje = mod.porcjuj(baza, pliki)
        self.assertGreaterEqual(len(porcje), 2)
        for porcja in porcje:
            self.assertLessEqual(mod.dlugosc_polecenia([*baza, *porcja]), 7000)

    def test_porcjuj_za_dluga_sciezka(self):
        with self.assertRaises(ValueError) as cm:
            mod.porcjuj(["npx", "eslint"], ["x" * 8000 + ".ts"])
        self.assertIn("przekracza limit 7000 znaków", str(cm.exception))

    def test_eslint_wywolania_mieszcza_sie_w_limicie(self):
        repo = self.nowe_repo()
        self.dodaj_i18n(repo)
        self.pisz(repo, "a.txt", "v1\n")
        self.commituj(repo)
        baza, _o = self.zapisz_baze(repo)
        nazwy = [f"m-{'x' * 88}-{i:03d}.ts" for i in range(100)]
        for n in nazwy:
            self.pisz(repo, n, "x\n")
        pakiet = self.pakiet(
            repo, [{"id": "B1", "autor": "t", "pliki": ["*.ts"]}], stos="fe"
        )
        runner = FakeRunner()
        kod, _o, _e, _p, _l, _r = self.odbior(repo, baza, pakiet, runner=runner)
        eslint = [c for c in runner.wywolania if "eslint" in c]
        self.assertGreaterEqual(len(eslint), 2)
        znalezione = []
        for wywolanie in eslint:
            self.assertLessEqual(mod.dlugosc_polecenia(wywolanie), 7000)
            znalezione += wywolanie[5:]
        self.assertEqual(set(znalezione), set(nazwy))


class TestStatystyka(BazaTestow):
    def test_commit_w_fali_ma_statystyke(self):
        repo = self.nowe_repo()
        self.pisz(repo, "a.txt", "l1\nl2\n")
        self.commituj(repo)
        baza, _o = self.zapisz_baze(repo)
        self.pisz(repo, "a.txt", "l1\nl2\nl3\n")
        self.commituj(repo, "fala")
        pakiet = self.pakiet(repo, [{"id": "B1", "autor": "t", "pliki": ["a.txt"]}])
        kod, out, _e, _p, _l, _r = self.odbior(repo, baza, pakiet)
        self.assertEqual(kod, 0)
        self.assertIn(f"+1 {MINUS}0", out)
        self.assertNotIn(" *", out.splitlines()[1])

    def test_brudny_w_bazie_ma_gwiazdke(self):
        repo = self.nowe_repo()
        self.pisz(repo, "a.txt", "v1\n")
        self.commituj(repo)
        self.pisz(repo, "a.txt", "v2\n")
        baza, _o = self.zapisz_baze(repo)
        self.pisz(repo, "a.txt", "v3\n")
        pakiet = self.pakiet(repo, [{"id": "B1", "autor": "t", "pliki": ["a.txt"]}])
        kod, _o, _e, pelny, _l, _r = self.odbior(repo, baza, pakiet)
        self.assertEqual(kod, 0)
        self.assertIn("a.txt *", pelny)
        self.assertIn("* statystyka obejmuje zmiany sprzed fali", pelny)


class TestStos(BazaTestow):
    def test_wykrywanie(self):
        kat = tempfile.mkdtemp(prefix="stos-", dir=TMP)
        with self.assertRaises(mod.BladUzycia):
            mod.wykryj_stos(kat, None)
        with open(os.path.join(kat, "package.json"), "w", encoding="utf-8") as f:
            json.dump({"dependencies": {"@angular/core": "^19.0.0"}}, f)
        self.assertEqual(mod.wykryj_stos(kat, None), "fe")
        with open(os.path.join(kat, "package.json"), "w", encoding="utf-8") as f:
            json.dump({"devDependencies": {"@angular/core": "^19.0.0"}}, f)
        self.assertEqual(mod.wykryj_stos(kat, None), "fe")

        kat2 = tempfile.mkdtemp(prefix="stos2-", dir=TMP)
        open(os.path.join(kat2, "App.slnx"), "w").close()
        self.assertEqual(mod.wykryj_stos(kat2, None), "be")
        kat3 = tempfile.mkdtemp(prefix="stos3-", dir=TMP)
        open(os.path.join(kat3, "App.sln"), "w").close()
        self.assertEqual(mod.wykryj_stos(kat3, None), "be")
        self.assertEqual(mod.wykryj_stos(kat3, "fe"), "fe")

    def test_wykrywanie_e2e_fe(self):
        repo = self.nowe_repo()
        self.pisz(repo, "package.json", json.dumps({"dependencies": {"@angular/core": "1"}}))
        self.dodaj_i18n(repo)
        self.pisz(repo, "a.txt", "v1\n")
        self.commituj(repo)
        baza, _o = self.zapisz_baze(repo)
        self.pisz(repo, "f.txt", "x\n")
        sciezka = os.path.join(TMP, "pakiet-bez-stosu.json")
        with open(sciezka, "w", encoding="utf-8") as f:
            json.dump({"briefy": [{"id": "B1", "autor": "t", "pliki": ["f.txt"]}]}, f)
        kod, out, _e, _p, _l, _r = self.odbior(repo, baza, sciezka)
        self.assertEqual(kod, 0)
        self.assertIn("(fe,", out)


class TestBaza(BazaTestow):
    def test_format_bazy(self):
        repo = self.nowe_repo()
        self.pisz(repo, "a.txt", "v1\n")
        self.commituj(repo)
        self.pisz(repo, "a.txt", "v2\n")
        self.pisz(repo, "n.txt", "n\n")
        baza, out = self.zapisz_baze(repo)
        self.assertEqual(len(out.splitlines()), 1)
        self.assertIn(baza, out)
        with open(baza, encoding="utf-8") as f:
            dane = json.load(f)
        self.assertEqual(dane["repo"], os.path.abspath(repo))
        self.assertEqual(dane["head"], git(repo, "rev-parse", "HEAD"))
        self.assertIn("czas", dane)
        self.assertEqual(set(dane["pliki"]), {"a.txt", "n.txt"})

    def test_baza_liczy_obie_sciezki_rename(self):
        repo = self.nowe_repo()
        self.pisz(repo, "stary.txt", "x\n")
        self.commituj(repo)
        git(repo, "mv", "stary.txt", "nowy.txt")
        baza, _o = self.zapisz_baze(repo)
        with open(baza, encoding="utf-8") as f:
            dane = json.load(f)
        self.assertEqual(set(dane["pliki"]), {"stary.txt", "nowy.txt"})
        self.assertIsNone(dane["pliki"]["stary.txt"])
        self.assertIsNotNone(dane["pliki"]["nowy.txt"])

    def test_wyjscie_utf8_przy_stronie_kodowej_cp1250(self):
        repo = self.nowe_repo()
        self.pisz(repo, "a.txt", "v1\n")
        self.commituj(repo)
        baza = os.path.join(TMP, "baza-cp1250.json")
        env = dict(os.environ, PYTHONIOENCODING="cp1250", PYTHONUTF8="0")
        p = subprocess.run(
            [sys.executable, os.path.join(TUTAJ, "fala-odbior.py"),
             "--repo", repo, "--zapisz-baze", baza],
            capture_output=True, env=env,
        )
        self.assertEqual(p.returncode, 0, p.stderr.decode("utf-8", "replace"))
        self.assertIn("→", p.stdout.decode("utf-8"))


class TestUzycie(BazaTestow):
    def test_brak_repo(self):
        kod, _o, err, _r = self.uruchom(
            ["--repo", os.path.join(TMP, "nie-ma"), "--zapisz-baze", "x.json"]
        )
        self.assertEqual(kod, 2)
        self.assertIn("brak repozytorium", err)

    def test_brak_bazy(self):
        repo = self.nowe_repo()
        pakiet = self.pakiet(repo, [])
        logi = tempfile.mkdtemp(prefix="logi-", dir=TMP)
        kod, _o, err, _r = self.uruchom(
            ["--repo", repo, "--baza", os.path.join(TMP, "nie-ma.json"),
             "--pakiet", pakiet, "--katalog-logow", logi]
        )
        self.assertEqual(kod, 2)
        self.assertIn("brak pliku bazy", err)

    def test_brak_pakietu(self):
        repo = self.nowe_repo()
        self.pisz(repo, "a.txt", "v1\n")
        self.commituj(repo)
        baza, _o = self.zapisz_baze(repo)
        logi = tempfile.mkdtemp(prefix="logi-", dir=TMP)
        kod, _o, err, _r = self.uruchom(
            ["--repo", repo, "--baza", baza, "--pakiet", os.path.join(TMP, "nie-ma.json"),
             "--katalog-logow", logi]
        )
        self.assertEqual(kod, 2)
        self.assertIn("brak pliku pakietu", err)

    def test_nieznany_brief(self):
        repo = self.nowe_repo()
        self.pisz(repo, "a.txt", "v1\n")
        self.commituj(repo)
        baza, _o = self.zapisz_baze(repo)
        pakiet = self.pakiet(repo, [{"id": "B1", "autor": "t", "pliki": ["*"]}])
        logi = tempfile.mkdtemp(prefix="logi-", dir=TMP)
        kod, _o, err, _r = self.uruchom(
            ["--repo", repo, "--baza", baza, "--pakiet", pakiet,
             "--katalog-logow", logi, "--brief", "B9"]
        )
        self.assertEqual(kod, 2)
        self.assertIn("nieznany brief", err)

    def test_zly_stos(self):
        repo = self.nowe_repo()
        self.pisz(repo, "a.txt", "v1\n")
        self.commituj(repo)
        baza, _o = self.zapisz_baze(repo)
        sciezka = os.path.join(TMP, "pakiet-zly.json")
        with open(sciezka, "w", encoding="utf-8") as f:
            json.dump({"stos": "py", "briefy": []}, f)
        logi = tempfile.mkdtemp(prefix="logi-", dir=TMP)
        kod, _o, err, _r = self.uruchom(
            ["--repo", repo, "--baza", baza, "--pakiet", sciezka, "--katalog-logow", logi]
        )
        self.assertEqual(kod, 2)


class TestSprawdzeniaFE(BazaTestow):
    def _repo_fe(self):
        repo = self.nowe_repo()
        self.dodaj_i18n(repo)
        self.pisz(repo, "a.txt", "v1\n")
        self.commituj(repo)
        baza, _o = self.zapisz_baze(repo)
        self.pisz(repo, "f.ts", "const x = 1;\n")
        pakiet = self.pakiet(
            repo, [{"id": "B1", "autor": "t", "pliki": ["*.ts"]}], stos="fe"
        )
        return repo, baza, pakiet

    def test_eslint_blad(self):
        repo, baza, pakiet = self._repo_fe()
        runner = FakeRunner({"npx eslint": (1, "problem", "")})
        kod, out, _e, _p, logi, _r = self.odbior(repo, baza, pakiet, runner=runner)
        self.assertEqual(kod, 1)
        self.assertIn("BŁĄD: eslint: kod wyjścia 1", out)
        self.assertIn("01-eslint.log", os.listdir(logi))
        with open(os.path.join(logi, "01-eslint.log"), encoding="utf-8") as f:
            self.assertIn("problem", f.read())

    def test_kolejnosc_eslint_stylelint_prettier(self):
        repo = self.nowe_repo()
        self.dodaj_i18n(repo)
        self.pisz(repo, "a.txt", "v1\n")
        self.commituj(repo)
        baza, _o = self.zapisz_baze(repo)
        self.pisz(repo, "f.ts", "x\n")
        self.pisz(repo, "s.scss", "x\n")
        pakiet = self.pakiet(
            repo, [{"id": "B1", "autor": "t", "pliki": ["*.*"]}], stos="fe"
        )
        runner = FakeRunner()
        kod, _o, _e, _p, _l, r = self.odbior(repo, baza, pakiet, runner=runner)
        self.assertEqual(kod, 0)
        kolejnosc = [
            next(x for x in ("eslint", "stylelint", "prettier") if x in c)
            for c in r.wywolania
            if os.path.basename(c[0]).lower().startswith("npx")
        ]
        self.assertEqual(kolejnosc, ["eslint", "stylelint", "prettier"])

    def test_brak_istniejacych_plikow_pomija_npx(self):
        repo = self.nowe_repo()
        self.dodaj_i18n(repo)
        self.pisz(repo, "a.ts", "x\n")
        self.commituj(repo)
        baza, _o = self.zapisz_baze(repo)
        os.remove(os.path.join(repo, "a.ts"))
        pakiet = self.pakiet(
            repo, [{"id": "B1", "autor": "t", "pliki": ["a.ts"]}], stos="fe"
        )
        runner = FakeRunner()
        kod, _o, _e, _p, _l, r = self.odbior(repo, baza, pakiet, runner=runner)
        self.assertEqual(kod, 0)
        self.assertFalse(
            [c for c in r.wywolania if os.path.basename(c[0]).lower().startswith("npx")]
        )

    def test_pelny_niezalezne_przebiegi(self):
        repo, baza, pakiet = self._repo_fe()
        runner = FakeRunner(
            {
                "npm run lint": (1, "", "blad lint"),
                "npm run format:check": (0, "ok", ""),
                "npm test": (
                    1,
                    "",
                    " Test Files  1 failed | 2 passed (3)\n"
                    " Tests  2 failed | 8 passed (10)\n"
                    "FAIL  src/x.spec.ts > s > t1\n"
                    "× s > t2\n",
                ),
                "npm run build": (1, "✘ [ERROR] Could not resolve 'x'\nError: nieudany", ""),
            }
        )
        kod, out, _e, pelny, _l, r = self.odbior(
            repo, baza, pakiet, extra=["--pelny"], runner=runner
        )
        self.assertEqual(kod, 1)
        npm_calls = [c for c in r.wywolania if os.path.basename(c[0]).lower().startswith("npm")]
        self.assertEqual(len(npm_calls), 4)
        self.assertIn("npm run lint: kod wyjścia 1", out)
        self.assertIn("npm test: 2 z 10 testów nieudanych (pliki: 1 z 3)", out)
        self.assertIn("npm run build: ✘ [ERROR] Could not resolve 'x'", out)
        self.assertIn("FAIL  src/x.spec.ts > s > t1", pelny)
        self.assertIn("× s > t2", pelny)

    def test_pelny_build_do_10_linii_w_werdykcie(self):
        repo, baza, pakiet = self._repo_fe()
        build_out = "".join(f"✘ [ERROR] blad numer {i}\n" for i in range(15))
        runner = FakeRunner(
            {
                "npm run lint": (0, "", ""),
                "npm run format:check": (0, "", ""),
                "npm test": (0, " Tests  3 passed (3)\n", ""),
                "npm run build": (1, build_out, ""),
            }
        )
        kod, out, _e, pelny, _l, _r = self.odbior(
            repo, baza, pakiet, extra=["--pelny"], runner=runner
        )
        self.assertEqual(kod, 1)
        self.assertEqual(out.count("npm run build: ✘ [ERROR]"), 10)
        self.assertEqual(pelny.count("błąd: ✘ [ERROR]"), 15)

    def test_pelny_build_ostrzezenia_przy_kodzie_0(self):
        repo, baza, pakiet = self._repo_fe()
        runner = FakeRunner(
            {
                "npm run lint": (0, "", ""),
                "npm run format:check": (0, "", ""),
                "npm test": (0, " Tests  3 passed (3)\n", ""),
                "npm run build": (0, "▲ [WARNING] chunk duży", ""),
            }
        )
        kod, out, _e, _p, _l, _r = self.odbior(
            repo, baza, pakiet, extra=["--pelny"], runner=runner
        )
        self.assertEqual(kod, 0)
        self.assertIn("WERDYKT: OSTRZEŻENIA", out)
        self.assertIn("▲ [WARNING] chunk duży", out)

    def test_brief_pomija_pelny(self):
        repo, baza, pakiet = self._repo_fe()
        runner = FakeRunner()
        kod, _o, _e, pelny, _l, r = self.odbior(
            repo, baza, pakiet, extra=["--pelny", "--brief", "B1"], runner=runner
        )
        self.assertEqual(kod, 0)
        self.assertFalse(
            [c for c in r.wywolania if os.path.basename(c[0]).lower().startswith("npm")]
        )
        self.assertIn("(pominięto — aktywny filtr --brief)", pelny)


class TestSprawdzeniaBE(BazaTestow):
    def _repo_be(self):
        repo = self.nowe_repo()
        self.pisz(repo, "App.slnx", "<slnx/>\n")
        self.pisz(repo, "a.txt", "v1\n")
        self.commituj(repo)
        baza, _o = self.zapisz_baze(repo)
        self.pisz(repo, "f.cs", "class X {}\n")
        pakiet = self.pakiet(repo, [{"id": "B1", "autor": "t", "pliki": ["*.cs"]}])
        return repo, baza, pakiet

    def test_bez_pelny_brak_dotnet(self):
        repo, baza, pakiet = self._repo_be()
        runner = FakeRunner()
        kod, out, _e, _p, _l, r = self.odbior(repo, baza, pakiet, runner=runner)
        self.assertEqual(kod, 0)
        self.assertIn("WERDYKT: OK", out)
        self.assertFalse(
            [c for c in r.wywolania if os.path.basename(c[0]).lower().startswith("dotnet")]
        )

    def test_pelny(self):
        repo, baza, pakiet = self._repo_be()
        runner = FakeRunner(
            {
                "dotnet build": (
                    1,
                    "",
                    "src/A.cs(10,5): error CS1234: coś\n"
                    "src/A.cs(10,5): error CS1234: coś\n"
                    "src/B.cs(1,1): warning CA1000: coś\n",
                ),
                "dotnet test": (
                    1,
                    "Failed: 2, Passed: 10, Skipped: 150, Total: 162",
                    "Failed N.T.X",
                ),
            }
        )
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("ZEBRANI_TEST_SQLSERVER", None)
            kod, out, _e, pelny, _l, _r = self.odbior(
                repo, baza, pakiet, extra=["--pelny"], runner=runner
            )
        self.assertEqual(kod, 1)
        self.assertIn("error CS1234", out)
        self.assertIn("warning CA1000", out)
        self.assertIn("dotnet test: Failed 2, Passed 10, Skipped 150, Total 162", out)
        self.assertIn(
            "pominięto 150 testów — czy ustawiono ZEBRANI_TEST_SQLSERVER? "
            "(zmienna: brak)",
            out,
        )
        self.assertIn("Failed N.T.X", pelny)

    def test_pelny_zmienna_srodowiskowa_ustawiona(self):
        repo, baza, pakiet = self._repo_be()
        runner = FakeRunner(
            {
                "dotnet build": (0, "", ""),
                "dotnet test": (0, "Failed: 0, Passed: 1, Skipped: 150, Total: 151", ""),
            }
        )
        with mock.patch.dict(os.environ, {"ZEBRANI_TEST_SQLSERVER": "1"}):
            kod, out, _e, _p, _l, _r = self.odbior(
                repo, baza, pakiet, extra=["--pelny"], runner=runner
            )
        self.assertEqual(kod, 0)
        self.assertIn("(zmienna: ustawiona)", out)


class TestKorektaB1K1(BazaTestow):
    def _repo_be_cs(self):
        repo = self.nowe_repo()
        self.pisz(repo, "App.slnx", "<slnx/>\n")
        self.pisz(repo, "a.txt", "v1\n")
        self.commituj(repo)
        baza, _o = self.zapisz_baze(repo)
        self.pisz(repo, "f.cs", "class X {}\n")
        pakiet = self.pakiet(repo, [{"id": "B1", "autor": "t", "pliki": ["*.cs"]}])
        return repo, baza, pakiet

    def test_build_11_ostrzezen_potem_blad(self):
        repo, baza, pakiet = self._repo_be_cs()
        ostrzezenia = "".join(
            f"src/B{i}.cs(1,1): warning CA1000: ostrzeżenie {i}\n" for i in range(11)
        )
        build_out = ostrzezenia + "src/A.cs(10,5): error CS1234: coś\n"
        runner = FakeRunner(
            {
                "dotnet build": (1, "", build_out),
                "dotnet test": (
                    0, "Failed: 0, Passed: 1, Skipped: 0, Total: 1", "",
                ),
            }
        )
        kod, out, _e, _p, _l, _r = self.odbior(
            repo, baza, pakiet, extra=["--pelny"], runner=runner
        )
        self.assertEqual(kod, 1)
        self.assertIn("WERDYKT: BŁĘDY", out)
        self.assertIn("error CS1234", out)
        self.assertLess(out.index("BŁĄD:"), out.index("OSTRZEŻENIE:"))
        self.assertLess(out.index("error CS1234"), out.index("warning CA1000"))

    def test_build_kod_1_bez_bledu_daje_kod_wyjscia(self):
        repo, baza, pakiet = self._repo_be_cs()
        runner = FakeRunner(
            {
                "dotnet build": (1, "", "src/B.cs(1,1): warning CA1000: coś\n"),
                "dotnet test": (
                    0, "Failed: 0, Passed: 1, Skipped: 0, Total: 1", "",
                ),
            }
        )
        kod, out, _e, _p, _l, _r = self.odbior(
            repo, baza, pakiet, extra=["--pelny"], runner=runner
        )
        self.assertEqual(kod, 1)
        self.assertIn("WERDYKT: BŁĘDY", out)
        self.assertIn("kod wyjścia 1", out)

    def test_statystyka_porcjowanie_daje_te_same_sumy(self):
        repo = self.nowe_repo()
        for i in range(10):
            self.pisz(repo, f"f{i:02d}.txt", "l1\nl2\n")
        self.commituj(repo)
        baza_sciezka, _o = self.zapisz_baze(repo)
        baza = mod.wczytaj_baze(baza_sciezka)
        for i in range(10):
            self.pisz(repo, f"f{i:02d}.txt", "l1\nl2\nl3\ndodatkowa\n")
        zakres = mod.oblicz_zakres(repo, baza, mod.Runner())
        brief = mod.Brief(id="B1", autor="t", pliki=["*.txt"])
        wlasc = {p: ["B1"] for p in zakres.pliki_fali}
        runner1 = FakeRunner()
        stats1 = mod.statystyki(
            repo, baza.head, baza.pliki, [brief], wlasc,
            zakres.status.niesledzone, runner1,
        )
        numstat1 = [
            c for c in runner1.wywolania
            if len(c) >= 3 and c[:3] == ["git", "diff", "--numstat"]
        ]
        self.assertEqual(len(numstat1), 1)
        self.assertGreater(stats1[0].dodane, 0)
        baza_cmd = ["git", "diff", "--numstat", baza.head, "--"]
        pathspecy = [f":(literal){p}" for p in sorted(wlasc)]
        limit_maly = mod.dlugosc_polecenia(baza_cmd + pathspecy[:2])
        with mock.patch.object(mod, "LIMIT_POLECENIA", limit_maly):
            runner2 = FakeRunner()
            stats2 = mod.statystyki(
                repo, baza.head, baza.pliki, [brief], wlasc,
                zakres.status.niesledzone, runner2,
            )
            numstat2 = [
                c for c in runner2.wywolania
                if len(c) >= 3 and c[:3] == ["git", "diff", "--numstat"]
            ]
            self.assertGreater(len(numstat2), 1)
        self.assertEqual(
            (stats1[0].dodane, stats1[0].usuniete),
            (stats2[0].dodane, stats2[0].usuniete),
        )

    def test_limit_czasu_kod_124(self):
        runner = mod.Runner(limit_sekund=1)
        t0 = time.monotonic()
        kod, _out, err = runner.run(
            [sys.executable, "-c", "import time; time.sleep(30)"]
        )
        dt = time.monotonic() - t0
        self.assertEqual(kod, 124)
        self.assertLess(dt, 10)
        self.assertIn("przekroczony limit czasu", err)
        self.assertIn("min", err)

    def test_limit_czasu_zabija_drzewo(self):
        runner = mod.Runner(limit_sekund=1)
        dziecko = (
            "import subprocess, sys, time; "
            "subprocess.Popen([sys.executable, '-c', "
            "'import time; time.sleep(30)']); time.sleep(30)"
        )
        t0 = time.monotonic()
        kod, _out, err = runner.run([sys.executable, "-c", dziecko])
        dt = time.monotonic() - t0
        self.assertEqual(kod, 124)
        self.assertLess(dt, 10)
        self.assertIn("przekroczony limit czasu", err)

    def test_npm_test_kod_0_z_fail_daje_blad(self):
        repo = self.nowe_repo()
        self.dodaj_i18n(repo)
        self.pisz(repo, "a.txt", "v1\n")
        self.commituj(repo)
        baza, _o = self.zapisz_baze(repo)
        self.pisz(repo, "f.ts", "const x = 1;\n")
        pakiet = self.pakiet(
            repo, [{"id": "B1", "autor": "t", "pliki": ["*.ts"]}], stos="fe"
        )
        runner = FakeRunner(
            {
                "npm test": (
                    0,
                    "",
                    " Test Files  1 failed | 1 passed (2)\n"
                    " Tests  1 failed | 2 passed (3)\n"
                    "FAIL  src/x.spec.ts > s > t1\n",
                ),
            }
        )
        kod, out, _e, _p, _l, _r = self.odbior(
            repo, baza, pakiet, extra=["--pelny"], runner=runner
        )
        self.assertEqual(kod, 1)
        self.assertIn("WERDYKT: BŁĘDY", out)
        self.assertIn("npm test:", out)
        self.assertIn("nieudanych", out)

    def test_dotnet_test_kod_0_z_fail_daje_blad(self):
        repo, baza, pakiet = self._repo_be_cs()
        runner = FakeRunner(
            {
                "dotnet build": (0, "", ""),
                "dotnet test": (
                    0,
                    "Failed: 1, Passed: 5, Skipped: 0, Total: 6",
                    "Failed N.T.X",
                ),
            }
        )
        kod, out, _e, _p, _l, _r = self.odbior(
            repo, baza, pakiet, extra=["--pelny"], runner=runner
        )
        self.assertEqual(kod, 1)
        self.assertIn("WERDYKT: BŁĘDY", out)
        self.assertIn("dotnet test:", out)


if __name__ == "__main__":
    unittest.main()
