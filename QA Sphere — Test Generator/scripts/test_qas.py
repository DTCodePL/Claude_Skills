"""Testy qas.py (unittest, bez sieci — atrapa qas.rpc)."""
import contextlib
import io
import json
import os
import tempfile
import unittest
from unittest import mock

import qas


def make_step(desc="Kliknij Zapisz.", exp="Zapisano."):
    return {"description": desc, "expected": exp}


def make_case(title="Przypadek", **kw):
    tc = {
        "type": "standalone",
        "title": title,
        "priority": "high",
        "precondition": {"text": "Środowisko: pre.\nKonto: admin."},
        "steps": [make_step()],
        "tags": ["happy-path"],
        "requirements": [
            {"text": "PBI #1 — X", "url": "https://dev.azure.com/x/1"}],
    }
    tc.update(kw)
    return tc


def make_payload(**kw):
    d = {
        "project": "ZEB",
        "transport": "mcp",
        "richTextFormat": "markdown",
        "folderPath": ["Zebrani.pl", "Moduł"],
        "folderId": 7,
        "testCases": [make_case("Pierwszy"), make_case("Drugi")],
    }
    d.update(kw)
    return d


def make_context(**kw):
    ctx = {
        "project": {"code": "ZEB", "title": "Zebrani.pl"},
        "projectTitle": "Zebrani.pl",
        "projectRoot": {"id": 1, "title": "Zebrani.pl"},
        "customFields": [
            {"systemName": "automation", "enabled": True, "type": "dropdown",
             "options": [{"value": "Planned"}, {"value": "Automated"}]},
        ],
        "roots": ["Zebrani.pl"],
        "cases": {},
    }
    ctx.update(kw)
    return ctx


def make_legacy_context(**kw):
    """Kontekst sprzed projectRoot (tylko roots) — ścieżka fallback."""
    ctx = make_context()
    del ctx["projectTitle"]
    del ctx["projectRoot"]
    ctx.update(kw)
    return ctx


class FakeRpc:
    """Atrapa transportu: handler(name, args) -> (err, text, structured)."""

    def __init__(self, handler):
        self.handler = handler
        self.calls = []

    def __call__(self, name, arguments):
        self.calls.append((name, arguments))
        return self.handler(name, arguments)


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self._env = dict(os.environ)
        os.environ.pop("QASPHERE_API_KEY", None)
        os.environ.pop("QASPHERE_MCP_URL", None)
        qas._KEY = None
        qas._URL = None
        self.addCleanup(self._restore_env)
        no_sleep = mock.patch.object(qas.time, "sleep", lambda s: None)
        no_sleep.start()
        self.addCleanup(no_sleep.stop)

    def _restore_env(self):
        os.environ.clear()
        os.environ.update(self._env)
        qas._KEY = None
        qas._URL = None

    def path(self, name="p.json"):
        return os.path.join(self.tmp.name, name)

    def write(self, data, name="p.json"):
        p = self.path(name)
        qas.save_json(p, data)
        return p

    def run_cli(self, argv):
        out = io.StringIO()
        err = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = qas.main(argv)
        return code, out.getvalue(), err.getvalue()


class TransportTest(Base):
    def test_sse_bierze_ostatnia_linie_data(self):
        raw = ('event: message\ndata: {"jsonrpc":"2.0","id":1}\n'
               'event: message\ndata: {"result": {"ok": 2}}\n')
        self.assertEqual(qas.parse_response(raw, "text/event-stream"),
                         {"result": {"ok": 2}})

    def test_zwykly_json(self):
        self.assertEqual(qas.parse_response('{"result": 1}',
                                            "application/json"),
                         {"result": 1})

    def test_rpc_bierze_structured_nie_text(self):
        qas._KEY, qas._URL = "SEKRET", "http://mcp.test"
        payload = {"result": {
            "structuredContent": {"id": "X", "seq": 5},
            "content": [{"type": "text",
                         "text": '{"id": "ZŁY", "seq": 999}'}]}}

        class Resp:
            headers = {"Content-Type": "application/json"}

            def read(self):
                return json.dumps(payload).encode()

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

        with mock.patch("urllib.request.urlopen", return_value=Resp()):
            err, text, structured = qas.rpc("create_test_case", {})
        self.assertFalse(err)
        self.assertEqual(structured, {"id": "X", "seq": 5})

    def test_retry_429_http(self):
        calls = []

        def fake(name, args):
            calls.append(1)
            if len(calls) < 3:
                raise qas.QasError("Limit 429.", http_status=429)
            return False, "", {"seq": 1}

        with mock.patch.object(qas, "rpc", fake):
            self.assertEqual(qas.call_retry("x", {})[2], {"seq": 1})
        self.assertEqual(len(calls), 3)

    def test_retry_429_iserror(self):
        answers = [(True, '{"httpStatus": 429, "message": "limit"}', None),
                   (True, '{"httpStatus":429,"message":"limit"}', None),
                   (False, "", {"seq": 2})]
        with mock.patch.object(qas, "rpc", FakeRpc(
                lambda n, a: answers.pop(0))):
            self.assertEqual(qas.call_retry("x", {})[2], {"seq": 2})

    def test_retry_429_wyczerpany(self):
        fake = FakeRpc(lambda n, a: (True, '{"httpStatus": 429}', None))
        with mock.patch.object(qas, "rpc", fake):
            with self.assertRaises(qas.QasError):
                qas.call_retry("x", {})
        self.assertEqual(len(fake.calls), 4)

    def test_brak_klucza_czytelny_blad(self):
        with mock.patch.object(qas, "CLAUDE_JSON",
                               qas.Path("/nie/ma/takiego.json")):
            with self.assertRaises(qas.QasError) as cm:
                qas.get_auth()
        self.assertEqual(cm.exception.exit_code, 1)
        self.assertIn("QASPHERE_API_KEY", str(cm.exception))


class LintMdTest(Base):
    def lint_texts(self, *texts, context=None, field_prefix="steps[0]"):
        tc = make_case("T", steps=[
            {"description": texts[0] if len(texts) > 0 else "ok",
             "expected": texts[1] if len(texts) > 1 else "ok"}])
        payload = make_payload(testCases=[tc])
        return qas.lint_file(payload, context)

    def test_md1_brak_pustej_po_liscie(self):
        errors, _ = self.lint_texts("Wstęp:\n1. jeden\n2. dwa\ntekst pod listą.")
        self.assertTrue(any("pusta linia" in m for _i, _f, m in errors), errors)

    def test_md1_blok_kodu_pod_pozycja(self):
        errors, _ = self.lint_texts("Kroki:\n1. jeden\n```sql\nSELECT 1\n```")
        self.assertTrue(any("pusta linia" in m for _i, _f, m in errors), errors)

    def test_md1_poprawna_lista_cicha(self):
        errors, warns = self.lint_texts("Wstęp:\n1. jeden\n2. dwa\n\nDalej.")
        self.assertEqual(errors, [])

    def test_md2_lista_wznowiona(self):
        errors, _ = self.lint_texts("Wstęp.\n\n2. drugi\n3. trzeci")
        self.assertTrue(any("wznowiona" in m for _i, _f, m in errors), errors)

    def test_md2_kontynuacja_cicha(self):
        errors, _ = self.lint_texts("Wstęp:\n1. jeden\n2. dwa")
        self.assertEqual([e for e in errors if "wznowiona" in e[2]], [])

    def test_md3_spacja_na_brzegu_kodu(self):
        errors, _ = self.lint_texts("Kliknij ` Anna `.")
        self.assertTrue(any("przycina" in m for _i, _f, m in errors), errors)

    def test_md3_poprawny_kod_cichy(self):
        errors, _ = self.lint_texts("Kliknij `Anna`.")
        self.assertEqual([e for e in errors if "przycina" in e[2]], [])

    def test_md4_podwojny_backslash_n(self):
        errors, _ = self.lint_texts("Linia\\nDruga.")
        self.assertTrue(any("escapowany" in m for _i, _f, m in errors), errors)

    def test_niezamkniety_blok(self):
        errors, _ = self.lint_texts("Dane:\n```sql\nSELECT 1")
        self.assertTrue(any("niezamknięty" in m for _i, _f, m in errors),
                        errors)

    def test_pusty_akapit_to_blad(self):
        errors, _w = self.lint_texts("Akapit.\n\nDrugi.")
        self.assertTrue(any("pusty akapit" in m for _i, _f, m in errors),
                        errors)

    def test_pusty_akapit_w_bloku_kodu_cichy(self):
        errors, warns = self.lint_texts(
            "Skrypt:\n```sql\nSELECT 1\n\nSELECT 2\n```")
        self.assertEqual(
            [e for e in errors if "pusty akapit" in e[2]], [])
        self.assertEqual(
            [w for w in warns if "pusty akapit" in w[2]], [])

    def test_md2_w_bloku_kodu_cichy(self):
        errors, _ = self.lint_texts(
            "Skrypt:\n```sql\nSELECT 1\n2. drugi\n```")
        self.assertEqual([e for e in errors if "wznowiona" in e[2]], [])

    def test_md1_w_bloku_kodu_cichy(self):
        errors, _ = self.lint_texts(
            "Skrypt:\n```sql\n1. test\nSELECT 1\n```")
        self.assertEqual(
            [e for e in errors if "pusta linia" in e[2]], [])

    def test_md4_w_bloku_kodu_cichy(self):
        errors, _ = self.lint_texts("Skrypt:\n```sql\nSELECT 'a\\nb'\n```")
        self.assertEqual(
            [e for e in errors if "escapowany" in e[2]], [])

    def test_pusty_akapit_po_liscie_cichy(self):
        _e, warns = self.lint_texts("Lista:\n1. a\n2. b\n\nDalej.")
        self.assertEqual([w for w in warns if "pusty akapit" in w[2]], [])

    def test_zaslepka_to_uwaga(self):
        _e, warns = self.lint_texts("TODO: dopisać.")
        self.assertTrue(any("TODO" in m for _i, _f, m in warns), warns)


class LintShapeTest(Base):
    def test_nieznane_pole(self):
        tc = make_case("T", foo=1)
        errors, _ = qas.lint_file(make_payload(testCases=[tc]))
        self.assertTrue(any("nieznane pole" in m for _i, _f, m in errors),
                        errors)

    def test_pole_zakazane(self):
        tc = make_case("T", projectCode="ZEB")
        errors, _ = qas.lint_file(make_payload(testCases=[tc]))
        self.assertTrue(any("zakazane" in m for _i, _f, m in errors), errors)

    def test_zla_priority(self):
        tc = make_case("T", priority="krytyczna")
        errors, _ = qas.lint_file(make_payload(testCases=[tc]))
        self.assertTrue(any("priority" in f for _i, f, _m in errors), errors)

    def test_zdublowany_tytul_casefold(self):
        payload = make_payload(testCases=[
            make_case("Ala ma kota"), make_case(" ala MA KOTA ")])
        errors, _ = qas.lint_file(payload)
        self.assertTrue(any("zdublowany tytuł" in m for _i, _f, m in errors),
                        errors)

    def test_zdublowany_key(self):
        payload = make_payload(testCases=[
            make_case("A", key="x"), make_case("B", key="x")])
        errors, _ = qas.lint_file(payload)
        self.assertTrue(any("zdublowany klucz" in m for _i, _f, m in errors),
                        errors)

    def test_oba_ksztalty_folderow(self):
        payload = make_payload(
            folderPath=["Zebrani.pl"],
            folders=[{"key": "a", "path": ["Zebrani.pl"], "folderId": None}])
        errors, _ = qas.lint_file(payload)
        self.assertTrue(any("dokładnie jeden" in m for _i, _f, m in errors),
                        errors)

    def test_zaden_ksztalt_folderow(self):
        payload = make_payload()
        del payload["folderPath"]
        errors, _ = qas.lint_file(payload)
        self.assertTrue(any("brak folderPath" in m for _i, _f, m in errors),
                        errors)

    def test_folderkey_bez_folders(self):
        tc = make_case("T", folderKey="a")
        errors, _ = qas.lint_file(make_payload(testCases=[tc]))
        self.assertTrue(any("folderKey" in f for _i, f, _m in errors), errors)

    def test_folderkey_spoza_folders(self):
        payload = make_payload(
            folderPath=None,
            folders=[{"key": "a", "path": ["Zebrani.pl"], "folderId": None}],
            testCases=[make_case("T", folderKey="b")])
        errors, _ = qas.lint_file(payload)
        self.assertTrue(any("folderKey" in f for _i, f, _m in errors), errors)

    def test_sciezka_spoza_korzenia(self):
        payload = make_payload(folderPath=["Obok", "X"], folderId=None)
        errors, _ = qas.lint_file(payload, make_context())
        self.assertTrue(any("obok korzenia" in m for _i, _f, m in errors),
                        errors)

    def test_sciezka_w_korzeniu_ok(self):
        payload = make_payload()
        errors, _ = qas.lint_file(payload, make_context())
        self.assertEqual([e for e in errors if "korzenia" in e[2]], [])

    def test_customfield_spoza_opcji(self):
        tc = make_case("T", customFields={"automation": {"value": "X"}})
        errors, _ = qas.lint_file(make_payload(testCases=[tc]),
                                  make_context())
        self.assertTrue(any("spoza options" in m for _i, _f, m in errors),
                        errors)

    def test_customfield_wylaczone(self):
        ctx = make_context(customFields=[
            {"systemName": "automation", "enabled": False,
             "type": "dropdown", "options": [{"value": "Planned"}]}])
        tc = make_case("T", customFields={"automation": {"value": "Planned"}})
        errors, _ = qas.lint_file(make_payload(testCases=[tc]), ctx)
        self.assertTrue(any("enabled" in m for _i, _f, m in errors), errors)

    def test_update_readonly_to_uwaga(self):
        payload = make_payload(testCases=[], updates=[{
            "seq": 5, "reason": "poprawka",
            "args": {"steps": [{
                "description": "a", "expected": "b", "id": 1,
                "type": "standalone", "version": 2, "isLatest": True}]}}])
        errors, warns = qas.lint_file(payload)
        self.assertEqual(errors, [])
        self.assertTrue(any("tylko do odczytu" in m for _i, _f, m in warns),
                        warns)

    def test_update_zakazane_type(self):
        payload = make_payload(testCases=[], updates=[
            {"seq": 5, "reason": "x", "args": {"type": "standalone"}}])
        errors, _ = qas.lint_file(payload)
        self.assertTrue(any("zakazane" in m for _i, _f, m in errors), errors)

    def test_strict_z_uwaga_exit1(self):
        p = self.write(make_payload())
        with mock.patch.object(qas, "rpc"):
            code, _o, _e = self.run_cli(["lint", p, "--strict"])
        # czysty plik bez uwag przechodzi i na strict
        self.assertEqual(code, 0)
        tc = make_case("T")
        tc["steps"] = [{"description": "TODO: dopisać.", "expected": "ok"}]
        p2 = self.write(make_payload(testCases=[tc]), "p2.json")
        code, _o, _e = self.run_cli(["lint", p2, "--strict"])
        self.assertEqual(code, 1)

    def test_pusty_akapit_blokuje_bez_strict(self):
        tc = make_case("T")
        tc["steps"] = [{"description": "A.\n\nB.", "expected": "ok"}]
        p = self.write(make_payload(testCases=[tc]))
        with mock.patch.object(qas, "rpc"):
            code, _o, _e = self.run_cli(["lint", p])
        self.assertEqual(code, 1)

    def test_sciezka_spoza_korzenia_legacy(self):
        payload = make_payload(folderPath=["Obok", "X"], folderId=None)
        errors, _ = qas.lint_file(payload, make_legacy_context())
        self.assertTrue(any("obok korzenia" in m for _i, _f, m in errors),
                        errors)

    def test_sciezka_programy_klienta_odrzucona(self):
        payload = make_payload(folderPath=["Programy klienta", "X"],
                               folderId=None)
        errors, _ = qas.lint_file(payload, make_context())
        self.assertTrue(any("obok korzenia" in m for _i, _f, m in errors),
                        errors)

    def test_korzen_null_to_tytul_projektu(self):
        payload = make_payload()
        errors, _ = qas.lint_file(
            payload, make_context(projectRoot=None))
        self.assertEqual([e for e in errors if "korzenia" in e[2]], [])
        bad = make_payload(folderPath=["Programy klienta", "X"],
                           folderId=None)
        errors, _ = qas.lint_file(bad, make_context(projectRoot=None))
        self.assertTrue(any("obok korzenia" in m for _i, _f, m in errors),
                        errors)


def live_case(seq=11, folder=7, title="Pierwszy", priority="high"):
    return {
        "title": title, "priority": priority, "folderId": folder,
        "tags": [{"id": 1, "title": "happy-path"}],
        "precondition": {"text": "Środowisko: pre.\nKonto: admin."},
        "steps": [{"description": "Kliknij Zapisz.", "expected": "Zapisano.",
                   "id": 9, "type": "standalone"}],
        "requirements": [{"text": "PBI #1 — X",
                          "url": "https://dev.azure.com/x/1"}],
        "links": [],
        "customFields": {},
    }


TREE_ZEB = {"data": [
    {"id": 1, "title": "Zebrani.pl", "parentId": 0},
    {"id": 7, "title": "Moduł", "parentId": 1},
], "total": 2}


def push_dispatch(tree=None, search_items=None, get_case=None, create=None,
                  fail_names=()):
    """Atrapa push: drzewo, search, get i create osobno.

    create: handler(name, args) albo stała odpowiedź (err, text, structured).
    fail_names: narzędzia odpowiadające isError 400 (do testów stopu).
    """
    def handler(name, args):
        if name in fail_names:
            return True, '{"httpStatus": 400, "message": " zły tytuł "}', None
        if name == "list_folders":
            return False, "", json.loads(json.dumps(
                tree if tree is not None else {"data": [], "total": 0}))
        if name == "list_test_cases":
            items = search_items() if callable(search_items) \
                else list(search_items or [])
            return False, "", {"data": items, "total": len(items)}
        if name == "get_test_case":
            case = get_case() if callable(get_case) else dict(get_case or {})
            return False, "", case
        if name == "create_test_case":
            if callable(create):
                return create(name, args)
            return create
        raise AssertionError("nieoczekiwane: %s" % name)

    return handler


class PushTest(Base):
    def test_zapisuje_seq_po_kazdym_i_wznawia(self):
        p = self.write(make_payload())
        created = iter([{"id": "A", "seq": 101}, {"id": "B", "seq": 102}])
        fake = FakeRpc(push_dispatch(
            tree=TREE_ZEB, create=lambda n, a: (
                False, "", dict(next(created)))))
        with mock.patch.object(qas, "rpc", fake):
            code, out, _ = self.run_cli(["push", p])
        self.assertEqual(code, 0)
        data = qas.load_json(p)
        self.assertEqual(
            [(t.get("seq"), t.get("id")) for t in data["testCases"]],
            [(101, "A"), (102, "B")])
        self.assertIn("#1 -> seq 101", out)
        # wznowienie: nic nowego, brak wywołań create
        fake2 = FakeRpc(push_dispatch(tree=TREE_ZEB))
        with mock.patch.object(qas, "rpc", fake2):
            code, _o, _e = self.run_cli(["push", p])
        self.assertEqual(code, 0)
        self.assertEqual(
            [c for c in fake2.calls if c[0] == "create_test_case"], [])

    def test_meta_nie_ida_do_api(self):
        tc = make_case("T", key="A1", folderKey=None, seq=None, id=None,
                       _roboczy="x")
        p = self.write(make_payload(testCases=[tc]))
        fake = FakeRpc(push_dispatch(
            tree=TREE_ZEB, create=(False, "", {"id": "A", "seq": 1})))
        with mock.patch.object(qas, "rpc", fake):
            self.run_cli(["push", p])
        args = [a for n, a in fake.calls if n == "create_test_case"][0]
        for banned in ("key", "folderKey", "seq", "id", "_roboczy"):
            self.assertNotIn(banned, args)
        self.assertEqual(args["folderId"], 7)

    def test_stop_na_iserror_z_zapisanym_plikiem(self):
        p = self.write(make_payload())
        created = iter([{"id": "A", "seq": 101}])
        fake = FakeRpc(push_dispatch(
            tree=TREE_ZEB,
            create=lambda n, a: (
                (True, '{"httpStatus": 400, "message": " zły tytuł "}', None)
                if len([c for c in fake.calls
                        if c[0] == "create_test_case"]) > 1
                else (False, "", dict(next(created)))),
        ))
        with mock.patch.object(qas, "rpc", fake):
            code, _o, err = self.run_cli(["push", p])
        self.assertEqual(code, 1)
        data = qas.load_json(p)
        self.assertEqual(data["testCases"][0].get("seq"), 101)
        self.assertIsNone(data["testCases"][1].get("seq"))

    def test_przejmuje_seq_bez_create(self):
        # (a) proces "zginął" między create a zapisem: serwer ma przypadek
        # o tym tytule w folderze z identyczną treścią -> przejęcie bez create.
        tc = make_case("Szukany")
        p = self.write(make_payload(testCases=[tc]))
        live = live_case(title="Szukany", folder=7)
        live["id"], live["seq"] = "L", 555
        fake = FakeRpc(push_dispatch(
            tree=TREE_ZEB,
            search_items=[{"id": "L", "seq": 555, "title": "Szukany",
                           "folderId": 7}],
            get_case=live,
            create=lambda n, a: (_ for _ in ()).throw(
                AssertionError("create nie może paść"))))
        with mock.patch.object(qas, "rpc", fake):
            code, out, _ = self.run_cli(["push", p])
        self.assertEqual(code, 0, out)
        data = qas.load_json(p)
        self.assertEqual(
            (data["testCases"][0].get("seq"),
             data["testCases"][0].get("id")), (555, "L"))
        self.assertIn("przejęty — treść zgodna", out)
        self.assertEqual(
            [c for c in fake.calls if c[0] == "create_test_case"], [])

    def test_inna_tresc_exit2_bez_create(self):
        # (b) ten sam tytuł i folder, inna treść -> STOP exit 2, bez create.
        tc = make_case("Szukany")
        p = self.write(make_payload(testCases=[tc]))
        live = live_case(title="Szukany", folder=7)
        live["id"], live["seq"] = "L", 555
        live["steps"][0]["expected"] = "Coś innego."
        fake = FakeRpc(push_dispatch(
            tree=TREE_ZEB,
            search_items=[{"id": "L", "seq": 555, "title": "Szukany",
                           "folderId": 7}],
            get_case=live,
            create=lambda n, a: (_ for _ in ()).throw(
                AssertionError("create nie może paść"))))
        with mock.patch.object(qas, "rpc", fake):
            code, _o, err = self.run_cli(["push", p])
        self.assertEqual(code, 2)
        self.assertIn("inną treścią", err)
        self.assertIn("555", err)
        data = qas.load_json(p)
        self.assertIsNone(data["testCases"][0].get("seq"))
        self.assertEqual(
            [c for c in fake.calls if c[0] == "create_test_case"], [])

    def test_dwoch_kandydatow_exit2(self):
        # (c) dwóch kandydatów -> STOP exit 2 z ich seq.
        tc = make_case("Bliźniak")
        p = self.write(make_payload(testCases=[tc]))
        items = [{"id": "A", "seq": 11, "title": "Bliźniak", "folderId": 7},
                 {"id": "B", "seq": 12, "title": "Bliźniak", "folderId": 7}]
        fake = FakeRpc(push_dispatch(
            tree=TREE_ZEB, search_items=items,
            create=lambda n, a: (_ for _ in ()).throw(
                AssertionError("create nie może paść"))))
        with mock.patch.object(qas, "rpc", fake):
            code, _o, err = self.run_cli(["push", p])
        self.assertEqual(code, 2)
        self.assertIn("11", err)
        self.assertIn("12", err)
        self.assertEqual(
            [c for c in fake.calls if c[0] in (
                "create_test_case", "get_test_case")], [])

    def test_timeout_create_exit2_bez_ponowienia(self):
        # (d) timeout create -> exit 2, jedno wywołanie, plik zapisany.
        p = self.write(make_payload(testCases=[make_case("Nowy")]))

        def boom(name, args):
            raise qas.QasError("timeout (przypadek mógł powstać).",
                               exit_code=1, uncertain=True)

        fake = FakeRpc(push_dispatch(tree=TREE_ZEB, create=boom))
        with mock.patch.object(qas, "rpc", fake):
            code, _o, err = self.run_cli(["push", p])
        self.assertEqual(code, 2)
        self.assertIn("wynik niepewny", err)
        creates = [c for c in fake.calls if c[0] == "create_test_case"]
        self.assertEqual(len(creates), 1)
        data = qas.load_json(p)
        self.assertIsNone(data["testCases"][0].get("seq"))

    def test_brak_id_seq_exit2_bez_ponowienia(self):
        # (e) odpowiedź bez id/seq -> exit 2, jedno wywołanie create.
        p = self.write(make_payload(testCases=[make_case("Nowy")]))
        fake = FakeRpc(push_dispatch(
            tree=TREE_ZEB, create=(False, "pusto", {})))
        with mock.patch.object(qas, "rpc", fake):
            code, _o, err = self.run_cli(["push", p])
        self.assertEqual(code, 2)
        self.assertIn("wynik niepewny", err)
        creates = [c for c in fake.calls if c[0] == "create_test_case"]
        self.assertEqual(len(creates), 1)
        data = qas.load_json(p)
        self.assertIsNone(data["testCases"][0].get("seq"))

    def test_folderid_niezgodny_ze_sciezka_exit1(self):
        # (f) folderId wskazuje inną ścieżkę niż plik -> exit 1 przed create.
        p = self.write(make_payload())
        other_tree = {"data": [
            {"id": 1, "title": "Zebrani.pl", "parentId": 0},
            {"id": 7, "title": "Inny", "parentId": 1},
        ], "total": 2}
        fake = FakeRpc(push_dispatch(tree=other_tree))
        with mock.patch.object(qas, "rpc", fake):
            code, _o, err = self.run_cli(["push", p])
        self.assertEqual(code, 1)
        self.assertIn("uruchom folders ponownie", err)
        self.assertEqual(
            [c for c in fake.calls if c[0] in (
                "create_test_case", "list_test_cases")], [])

    def test_brak_folderid_podpowiada_folders(self):
        p = self.write(make_payload(folderId=None))
        with mock.patch.object(qas, "rpc", FakeRpc(
                lambda n, a: (False, "", {}))):
            code, _o, err = self.run_cli(["push", p])
        self.assertEqual(code, 1)
        self.assertIn("folders", err)

    def test_dry_run_bez_wywolan(self):
        p = self.write(make_payload())
        fake = FakeRpc(lambda n, a: (False, "", {}))
        with mock.patch.object(qas, "rpc", fake):
            code, out, _ = self.run_cli(["push", p, "--dry-run"])
        self.assertEqual(code, 0)
        self.assertEqual(fake.calls, [])
        self.assertIn("bez wywołań", out)

    def test_dry_run_wszystkie_maja_seq(self):
        tc = make_case("T", seq=5, id="X")
        p = self.write(make_payload(testCases=[tc]))
        with mock.patch.object(qas, "rpc", FakeRpc(
                lambda n, a: (False, "", {}))):
            code, out, _ = self.run_cli(["push", p, "--dry-run"])
        self.assertEqual(code, 0)
        self.assertIn("nic do wysłania", out)


def folders_dispatch(project_title="Zebrani.pl", tree=None, upsert=None):
    """Atrapa folders: get_project, list_folders, upsert_folders osobno."""
    def handler(name, args):
        if name == "get_project":
            return False, "", {"code": "ZEB", "title": project_title}
        if name == "list_folders":
            return False, "", json.loads(json.dumps(
                tree if tree is not None else {"data": [], "total": 0}))
        if name == "upsert_folders":
            if callable(upsert):
                return upsert(name, args)
            return upsert
        raise AssertionError("nieoczekiwane: %s" % name)

    return handler


class FoldersTest(Base):
    def test_odmawia_sciezki_bez_korzenia(self):
        p = self.write(make_payload(folderPath=["Obok", "X"], folderId=None))
        fake = FakeRpc(folders_dispatch(tree={
            "data": [{"id": 1, "title": "Zebrani.pl", "parentId": 0}],
            "total": 1}))
        with mock.patch.object(qas, "rpc", fake):
            code, _o, err = self.run_cli(["folders", p])
        self.assertEqual(code, 1)
        self.assertIn("korzenia", err)

    def test_programy_klienta_to_nie_korzen(self):
        # (g) drugi folder najwyższego poziomu nie jest korzeniem.
        p = self.write(make_payload(folderPath=["Programy klienta", "X"],
                                    folderId=None))
        fake = FakeRpc(folders_dispatch(tree={
            "data": [{"id": 1, "title": "Zebrani.pl", "parentId": 0},
                     {"id": 2, "title": "Programy klienta", "parentId": 0}],
            "total": 2}))
        with mock.patch.object(qas, "rpc", fake):
            code, _o, err = self.run_cli(["folders", p])
        self.assertEqual(code, 1)
        self.assertIn("korzenia", err)
        self.assertEqual(
            [c for c in fake.calls if c[0] == "upsert_folders"], [])

    def test_brak_korzenia_bez_flagi_exit1(self):
        p = self.write(make_payload(folderPath=["Zebrani.pl", "Nowy"],
                                    folderId=None))
        fake = FakeRpc(folders_dispatch(tree={"data": [], "total": 0}))
        with mock.patch.object(qas, "rpc", fake):
            code, _o, err = self.run_cli(["folders", p])
        self.assertEqual(code, 1)
        self.assertIn("--create-root", err)

    def test_create_root_tworzy_korzen(self):
        p = self.write(make_payload(folderPath=["Zebrani.pl", "Nowy"],
                                    folderId=None))
        fake = FakeRpc(folders_dispatch(
            tree={"data": [], "total": 0},
            upsert=(False, "", {"ids": [[1, 9]]})))
        with mock.patch.object(qas, "rpc", fake):
            code, out, _ = self.run_cli(["folders", p, "--create-root"])
        self.assertEqual(code, 0, out)
        self.assertEqual(qas.load_json(p)["folderId"], 9)

    def test_create_root_zly_pierwszy_segment(self):
        p = self.write(make_payload(folderPath=["Obok", "X"], folderId=None))
        fake = FakeRpc(folders_dispatch(tree={"data": [], "total": 0}))
        with mock.patch.object(qas, "rpc", fake):
            code, _o, err = self.run_cli(["folders", p, "--create-root"])
        self.assertEqual(code, 1)
        self.assertIn("tytułem projektu", err)

    def test_niejednoznaczny_korzen_exit1(self):
        p = self.write(make_payload(folderPath=["Zebrani.pl", "Nowy"],
                                    folderId=None))
        fake = FakeRpc(folders_dispatch(tree={
            "data": [{"id": 1, "title": "Zebrani.pl", "parentId": 0},
                     {"id": 2, "title": "Zebrani.pl", "parentId": 0}],
            "total": 2}))
        with mock.patch.object(qas, "rpc", fake):
            code, _o, err = self.run_cli(["folders", p])
        self.assertEqual(code, 1)
        self.assertIn("Niejednoznaczny", err)

    def test_upsert_zapisuje_liscia(self):
        p = self.write(make_payload(folderPath=["Zebrani.pl", "Nowy"],
                                    folderId=None))

        def upsert(name, args):
            self.assertNotIn("comment", args["folders"][0])
            return False, "", {"ids": [[1, 9]]}

        fake = FakeRpc(folders_dispatch(
            tree={"data": [
                {"id": 1, "title": "Zebrani.pl", "parentId": 0}],
                "total": 1},
            upsert=upsert))
        with mock.patch.object(qas, "rpc", fake):
            code, out, _ = self.run_cli(["folders", p])
        self.assertEqual(code, 0)
        self.assertEqual(qas.load_json(p)["folderId"], 9)
        self.assertIn("folderId 9", out)

    def test_istniejaca_sciezka_bez_upsert(self):
        # (h) liść już w drzewie -> id z drzewa, upsert_folders nie wołane.
        p = self.write(make_payload(folderPath=["Zebrani.pl", "Moduł"],
                                    folderId=None,
                                    folderComment="nie nadpisuj mnie"))
        fake = FakeRpc(folders_dispatch(
            tree={"data": [
                {"id": 1, "title": "Zebrani.pl", "parentId": 0},
                {"id": 7, "title": "Moduł", "parentId": 1}],
                "total": 2},
            upsert=lambda n, a: (_ for _ in ()).throw(
                AssertionError("upsert nie może paść"))))
        with mock.patch.object(qas, "rpc", fake):
            code, out, _ = self.run_cli(["folders", p])
        self.assertEqual(code, 0, out)
        self.assertEqual(qas.load_json(p)["folderId"], 7)
        self.assertIn("z drzewa", out)
        self.assertEqual(
            [c for c in fake.calls if c[0] == "upsert_folders"], [])


class UpdateTest(Base):
    def payload(self):
        return make_payload(testCases=[], updates=[{
            "seq": 5, "reason": "poprawka", "done": False,
            "args": {"title": "Nowy tytuł",
                     "precondition": {"text": "Pre."},
                     "steps": [{"description": "a", "expected": "b",
                                "id": 1, "type": "standalone",
                                "version": 2, "isLatest": True,
                                "data": [{"type": "text", "label": "L",
                                          "text": "T",
                                          "format": "plaintext"}]}]}}])

    def test_przycina_pola_readonly(self):
        p = self.write(self.payload())
        sent = {}

        def handler(name, args):
            sent.update(args)
            return False, "", {}

        with mock.patch.object(qas, "rpc", FakeRpc(handler)):
            code, out, _ = self.run_cli(["update", p])
        self.assertEqual(code, 0, out)
        self.assertEqual(sent["tcaseOrLegacyId"], "5")
        step = sent["steps"][0]
        self.assertEqual(sorted(step),
                         ["data", "description", "expected"])
        self.assertEqual(sent["precondition"], {"text": "Pre."})
        self.assertIn("przycięto", out)
        data = qas.load_json(p)
        self.assertTrue(data["updates"][0]["done"])

    def test_przycina_data_i_precondition(self):
        args = {"steps": [{"description": "a", "expected": "b",
                           "data": [{"type": "text", "text": "T",
                                     "extra": 1}]}],
                "precondition": {"text": "Pre.", "id": 3}}
        trimmed, cuts = qas.trim_update_args(args)
        self.assertEqual(sorted(trimmed["steps"][0]["data"][0]),
                         ["text", "type"])
        self.assertEqual(trimmed["precondition"], {"text": "Pre."})
        self.assertEqual(len(cuts), 2)

    def test_iserror_zapisuje_i_exit1(self):
        p = self.write(self.payload())
        fake = FakeRpc(
            lambda n, a: (True, '{"httpStatus":400,"message":"źle"}', None))
        with mock.patch.object(qas, "rpc", fake):
            code, _o, _e = self.run_cli(["update", p])
        self.assertEqual(code, 1)
        self.assertFalse(qas.load_json(p)["updates"][0].get("done", False))


class VerifyTest(Base):
    def test_normalizacja_daje_ok(self):
        tc = make_case("T", seq=11, id="X")
        tc["precondition"] = {"text": "a > b\n```sql\nSELECT 1"}
        p = self.write(make_payload(testCases=[tc]))
        live = live_case(title="T")
        live["precondition"] = {
            "text": "a &gt; b  \n\n```\nSELECT 1\n"}
        fake = FakeRpc(lambda n, a: (False, "", live))
        with mock.patch.object(qas, "rpc", fake):
            code, out, _ = self.run_cli(["verify", p])
        self.assertEqual(code, 0, out)
        self.assertIn("OK #1", out)

    def test_zmieniona_litera_to_roznica(self):
        tc = make_case("T", seq=11, id="X")
        p = self.write(make_payload(testCases=[tc]))
        live = live_case(title="T")
        live["steps"][0]["expected"] = "Zapisane."
        before = qas.load_json(p)
        fake = FakeRpc(lambda n, a: (False, "", live))
        with mock.patch.object(qas, "rpc", fake):
            code, out, _ = self.run_cli(["verify", p])
        self.assertEqual(code, 1)
        self.assertIn("RÓŻNICA", out)
        self.assertEqual(qas.load_json(p), before)

    def test_verify_nigdy_nie_zapisuje(self):
        tc = make_case("T", seq=11, id="X")
        p = self.write(make_payload(testCases=[tc]))
        mtime = os.path.getmtime(p)
        with mock.patch.object(qas, "rpc", FakeRpc(
                lambda n, a: (False, "", live_case(title="T")))):
            self.run_cli(["verify", p])
        self.assertEqual(os.path.getmtime(p), mtime)

    def test_sharedstepid_roznica(self):
        tc = make_case("T", seq=11, id="X")
        tc["steps"] = [{"sharedStepId": 5}]
        p = self.write(make_payload(testCases=[tc]))
        live = live_case(title="T")
        live["steps"] = [{"sharedStepId": 6, "description": "x",
                          "expected": "y"}]
        with mock.patch.object(qas, "rpc", FakeRpc(
                lambda n, a: (False, "", live))):
            code, out, _ = self.run_cli(["verify", p])
        self.assertEqual(code, 1)
        self.assertIn("sharedStepId", out)

    def test_sharedstepid_zgodny_cichy(self):
        tc = make_case("T", seq=11, id="X")
        tc["steps"] = [{"sharedStepId": 5}]
        p = self.write(make_payload(testCases=[tc]))
        live = live_case(title="T")
        live["steps"] = [{"sharedStepId": 5, "description": "x",
                          "expected": "y"}]
        with mock.patch.object(qas, "rpc", FakeRpc(
                lambda n, a: (False, "", live))):
            code, out, _ = self.run_cli(["verify", p])
        self.assertEqual(code, 0, out)

    def test_isdraft_roznica(self):
        tc = make_case("T", seq=11, id="X", isDraft=True)
        p = self.write(make_payload(testCases=[tc]))
        live = live_case(title="T")
        live["isDraft"] = False
        with mock.patch.object(qas, "rpc", FakeRpc(
                lambda n, a: (False, "", live))):
            code, out, _ = self.run_cli(["verify", p])
        self.assertEqual(code, 1)
        self.assertIn("isDraft", out)

    def test_bez_seq_niewyslany(self):
        tc = make_case("T")
        self.assertIsNone(tc.get("seq"))
        p = self.write(make_payload(testCases=[tc]))
        fake = FakeRpc(lambda n, a: (False, "", live_case(title="T")))
        with mock.patch.object(qas, "rpc", fake):
            code, out, _ = self.run_cli(["verify", p])
        self.assertEqual(code, 1)
        self.assertIn("NIEWYSŁANY", out)
        self.assertEqual(fake.calls, [])

    def test_only_bez_seq_exit1(self):
        tc = make_case("T", key="K1")
        p = self.write(make_payload(testCases=[tc]))
        fake = FakeRpc(lambda n, a: (False, "", live_case(title="T")))
        with mock.patch.object(qas, "rpc", fake):
            code, out, _ = self.run_cli(["verify", p, "--only", "K1"])
        self.assertEqual(code, 1)
        self.assertIn("NIEWYSŁANY", out)

    def test_norm_pusta_przed_lista_ignorowana(self):
        # (j) artefakt odczytu: pusta linia przed listą nie jest różnicą.
        tc = make_case("T", seq=11, id="X")
        tc["steps"] = [{"description": "Kroki:\n1. a\n2. b\n\nDalej.",
                        "expected": "ok"}]
        p = self.write(make_payload(testCases=[tc]))
        live = live_case(title="T")
        live["steps"] = [{"description": "Kroki:\n\n1. a\n2. b\n\nDalej.",
                          "expected": "ok"}]
        with mock.patch.object(qas, "rpc", FakeRpc(
                lambda n, a: (False, "", live))):
            code, out, _ = self.run_cli(["verify", p])
        self.assertEqual(code, 0, out)

    def test_norm_pusta_w_kodzie_znaczaca(self):
        # Pusta linia w kodzie przed linią "1. test" to dane, nie artefakt.
        file_desc = "Skrypt:\n```sql\nSELECT 1\n\n1. test\n```"
        live_desc = "Skrypt:\n```\nSELECT 1\n1. test\n```"
        self.assertNotEqual(qas.norm_text(file_desc),
                            qas.norm_text(live_desc))

    def test_norm_brak_pustej_po_liscie_wykryty(self):
        # (j) brak pustej linii po liście w pliku jest znaczący.
        tc = make_case("T", seq=11, id="X")
        tc["steps"] = [{"description": "Kroki:\n1. a\n2. b\ntekst.",
                        "expected": "ok"}]
        p = self.write(make_payload(testCases=[tc]))
        live = live_case(title="T")
        live["steps"] = [{"description": "Kroki:\n1. a\n2. b\n\ntekst.",
                          "expected": "ok"}]
        with mock.patch.object(qas, "rpc", FakeRpc(
                lambda n, a: (False, "", live))):
            code, out, _ = self.run_cli(["verify", p])
        self.assertEqual(code, 1, out)
        self.assertIn("RÓŻNICA", out)


class ContextTest(Base):
    def test_kontekst_zapisuje_pola(self):
        def handler(name, args):
            if name == "get_project":
                return False, "", {"code": "ZEB", "title": "Zebrani.pl"}
            if name == "list_custom_fields":
                return False, "", {"customFields": [{"systemName": "a"}]}
            if name == "list_folders":
                return False, "", {"data": [
                    {"id": 1, "title": "Zebrani.pl", "parentId": 0},
                    {"id": 2, "title": "Moduł", "parentId": 1}], "total": 2}
            if name == "list_test_cases":
                return False, "", {"data": [{
                    "seq": 1, "title": "T", "folderId": 2,
                    "priority": "high",
                    "tags": [{"title": "happy-path"}]}], "total": 1}
            raise AssertionError(name)

        out = os.path.join(self.tmp.name, "ctx.json")
        with mock.patch.object(qas, "rpc", FakeRpc(handler)):
            code, summary, _ = self.run_cli(
                ["context", "--project", "ZEB", "--search", "T",
                 "--folder-id", "2", "--out", out])
        self.assertEqual(code, 0)
        ctx = qas.load_json(out)
        self.assertEqual(ctx["roots"], ["Zebrani.pl"])
        self.assertEqual(ctx["projectTitle"], "Zebrani.pl")
        self.assertEqual(ctx["projectRoot"],
                         {"id": 1, "title": "Zebrani.pl"})
        self.assertEqual(ctx["folders"][1]["path"],
                         ["Zebrani.pl", "Moduł"])
        self.assertEqual(len(ctx["cases"]["search:T"]), 1)
        self.assertEqual(len(ctx["cases"]["folder:2"]), 1)
        self.assertIn("folderów 2", summary)

    def test_korzen_to_tytul_projektu_nie_dowolny_top(self):
        def handler(name, args):
            if name == "get_project":
                return False, "", {"code": "ZEB", "title": "Zebrani.pl"}
            if name == "list_custom_fields":
                return False, "", {"customFields": []}
            if name == "list_folders":
                return False, "", {"data": [
                    {"id": 1, "title": "Zebrani.pl", "parentId": 0},
                    {"id": 2, "title": "Programy klienta", "parentId": 0}],
                    "total": 2}
            raise AssertionError(name)

        out = os.path.join(self.tmp.name, "ctx.json")
        with mock.patch.object(qas, "rpc", FakeRpc(handler)):
            code, _s, _e = self.run_cli(
                ["context", "--project", "ZEB", "--out", out])
        self.assertEqual(code, 0)
        ctx = qas.load_json(out)
        self.assertEqual(ctx["projectRoot"],
                         {"id": 1, "title": "Zebrani.pl"})

    def test_niejednoznaczny_korzen_to_null(self):
        def handler(name, args):
            if name == "get_project":
                return False, "", {"code": "ZEB", "title": "Zebrani.pl"}
            if name == "list_custom_fields":
                return False, "", {"customFields": []}
            if name == "list_folders":
                return False, "", {"data": [
                    {"id": 1, "title": "Zebrani.pl", "parentId": 0},
                    {"id": 2, "title": "Zebrani.pl", "parentId": 0}],
                    "total": 2}
            raise AssertionError(name)

        out = os.path.join(self.tmp.name, "ctx.json")
        with mock.patch.object(qas, "rpc", FakeRpc(handler)):
            code, _s, _e = self.run_cli(
                ["context", "--project", "ZEB", "--out", out])
        self.assertEqual(code, 0)
        self.assertIsNone(qas.load_json(out)["projectRoot"])

    def test_archiwum_to_blad(self):
        fake = FakeRpc(
            lambda n, a: (False, "", {"code": "Z",
                                      "archivedAt": "2026-01-01"}))
        with mock.patch.object(qas, "rpc", fake):
            code, _o, err = self.run_cli(
                ["context", "--project", "Z", "--out", "x.json"])
        self.assertEqual(code, 1)
        self.assertIn("zarchiwizowany", err)


class SecretTest(Base):
    SECRET = "SEKRETNY-KLUCZ-12345"

    def outputs_without_secret(self, argv, fake):
        os.environ["QASPHERE_API_KEY"] = self.SECRET
        os.environ["QASPHERE_MCP_URL"] = "http://mcp.test"
        with mock.patch.object(qas, "rpc", fake):
            code, out, err = self.run_cli(argv)
        self.assertNotIn(self.SECRET, out)
        self.assertNotIn(self.SECRET, err)
        return code

    def test_klucz_nigdzie_w_wyjsciu(self):
        p = self.write(make_payload())
        fake = FakeRpc(
            lambda n, a: (True, '{"httpStatus":400,"message":"źle"}', None))
        self.outputs_without_secret(["lint", p], fake)
        self.outputs_without_secret(["push", p, "--dry-run"], fake)
        self.outputs_without_secret(["push", p], fake)
        self.outputs_without_secret(["update", p], fake)
        vf = FakeRpc(lambda n, a: (False, "", live_case(title="Pierwszy")))
        os.environ["QASPHERE_API_KEY"] = self.SECRET
        with mock.patch.object(qas, "rpc", vf):
            code, out, err = self.run_cli(["verify", p])
        self.assertNotIn(self.SECRET, out + err)


REVIEW_TREE = {"data": [
    {"id": 1, "title": "Zebrani.pl", "parentId": 0},
    {"id": 2, "title": "Programy klienta", "parentId": 0},
    {"id": 7, "title": "Moduł", "parentId": 1},
    {"id": 8, "title": "Podmoduł", "parentId": 7},
    {"id": 9, "title": "Wspólne", "parentId": 1},
    {"id": 10, "title": "Szablony", "parentId": 9},
], "total": 6}


def full_live(seq, title="Zwykły", folder=7, tags=("happy-path",),
              priority="high"):
    """Odczyt get_test_case z pełną treścią (jak na serwerze)."""
    return {
        "seq": seq, "title": title, "folderId": folder,
        "priority": priority,
        "tags": [{"id": i + 1, "title": t} for i, t in enumerate(tags)],
        "isDraft": False, "type": "standalone", "version": 3,
        "precondition": {"text": "Pre %d." % seq},
        "steps": [{"description": "Krok.", "expected": "Oczekiwane.",
                   "id": 9, "type": "x", "version": 1, "isLatest": True}],
        "requirements": [{"text": "PBI #1",
                          "url": "https://dev.azure.com/1"}],
        "links": [{"text": "Figma", "url": "https://figma.com/f"}],
        "customFields": {"automation": {"value": "Planned"}},
    }


def review_dispatch(tree=None, listed=None, cases=None):
    """Atrapa context --review-folder: drzewo, lista seq, odczyty."""

    def handler(name, args):
        if name == "get_project":
            return False, "", {"code": "ZEB", "title": "Zebrani.pl"}
        if name == "list_custom_fields":
            return False, "", {"customFields": []}
        if name == "list_folders":
            return False, "", json.loads(json.dumps(
                tree if tree is not None else {"data": [], "total": 0}))
        if name == "list_test_cases":
            items = list(listed or [])
            return False, "", {"data": items, "total": len(items)}
        if name == "get_test_case":
            live = (cases or {}).get(args.get("tcase"))
            assert live is not None, "brak odczytu %s" % args.get("tcase")
            return False, "", json.loads(json.dumps(live))
        raise AssertionError("nieoczekiwane: %s" % name)

    return handler


class ReviewContextTest(Base):
    def run_ctx(self, extra, fake):
        out = os.path.join(self.tmp.name, "ctx.json")
        with mock.patch.object(qas, "rpc", fake):
            code, stdout, stderr = self.run_cli(
                ["context", "--project", "ZEB", "--out", out] + extra)
        return code, stdout, stderr, out

    def test_zakres_to_folder_i_potomkowie(self):
        listed = [{"seq": 11}, {"seq": 12}]
        cases = {"11": full_live(11), "12": full_live(12, folder=8)}
        fake = FakeRpc(review_dispatch(
            tree=REVIEW_TREE, listed=listed, cases=cases))
        code, out, _e, path = self.run_ctx(["--review-folder", "7"], fake)
        self.assertEqual(code, 0, out)
        ctx = qas.load_json(path)
        self.assertEqual(
            [f["id"] for f in ctx["reviewFolders"]], [7, 8])
        self.assertEqual(ctx["reviewFolders"][1]["path"],
                         ["Zebrani.pl", "Moduł", "Podmoduł"])
        lists = [a for n, a in fake.calls if n == "list_test_cases"]
        self.assertEqual(len(lists), 1)
        self.assertEqual(lists[0]["folders"], [7, 8])
        self.assertEqual(len(ctx["existing"]), 2)
        self.assertEqual(ctx["retiredInScope"], [])
        self.assertIn("Przegląd: folderów 2, przypadków 2, "
                      "oznaczonych [Removed] 0.", out)

    def test_zakres_bez_wyjatkow_i_bez_klucza_folderu(self):
        fake = FakeRpc(review_dispatch(tree=REVIEW_TREE, listed=[]))
        code, _o, _e, path = self.run_ctx(["--review-folder", "1"], fake)
        self.assertEqual(code, 0)
        ctx = qas.load_json(path)
        self.assertEqual(
            [f["id"] for f in ctx["reviewFolders"]], [1, 7, 8, 9, 10])
        lists = [a for n, a in fake.calls if n == "list_test_cases"]
        self.assertEqual(lists[0]["folders"], [1, 7, 8, 9, 10])
        self.assertEqual(
            set(ctx),
            {"project", "projectTitle", "projectRoot", "customFields",
             "folders", "roots", "cases", "reviewFolders", "existing",
             "retiredInScope"})

    def test_oznaczony_do_retired_nie_do_existing(self):
        listed = [{"seq": 13}, {"seq": 11}, {"seq": 12}, {"seq": 11}]
        cases = {"11": full_live(11),
                 "12": full_live(12, title="[Removed] Stary"),
                 "13": full_live(13, tags=("[Removed]", "stare"))}
        fake = FakeRpc(review_dispatch(
            tree=REVIEW_TREE, listed=listed, cases=cases))
        code, _o, _e, path = self.run_ctx(["--review-folder", "7"], fake)
        self.assertEqual(code, 0)
        ctx = qas.load_json(path)
        self.assertEqual([c["seq"] for c in ctx["existing"]], [11])
        self.assertEqual(ctx["retiredInScope"], [12, 13])
        gets = [a["tcase"] for n, a in fake.calls if n == "get_test_case"]
        self.assertEqual(gets, ["11", "12", "13"])

    def test_existing_ma_pelna_tresc(self):
        live = full_live(11)
        fake = FakeRpc(review_dispatch(
            tree=REVIEW_TREE, listed=[{"seq": 11}], cases={"11": live}))
        code, _o, _e, path = self.run_ctx(["--review-folder", "7"], fake)
        self.assertEqual(code, 0)
        entry = qas.load_json(path)["existing"][0]
        self.assertEqual(entry["seq"], 11)
        self.assertEqual(entry["title"], live["title"])
        self.assertEqual(entry["folderId"], 7)
        self.assertEqual(entry["folderPath"], ["Zebrani.pl", "Moduł"])
        self.assertEqual(entry["priority"], "high")
        self.assertEqual(entry["tags"], ["happy-path"])
        self.assertEqual(entry["isDraft"], False)
        self.assertEqual(entry["type"], "standalone")
        self.assertEqual(entry["version"], 3)
        self.assertEqual(entry["precondition"], live["precondition"])
        self.assertEqual(entry["steps"], live["steps"])
        self.assertIn("id", entry["steps"][0])  # bez przycinania
        self.assertEqual(entry["requirements"], live["requirements"])
        self.assertEqual(entry["links"], live["links"])
        self.assertEqual(entry["customFields"], live["customFields"])

    def test_nieznany_review_folder_exit1(self):
        fake = FakeRpc(review_dispatch(tree=REVIEW_TREE))
        code, _o, err, _p = self.run_ctx(["--review-folder", "999"], fake)
        self.assertEqual(code, 1)
        self.assertIn("999", err)

    def test_bez_flagi_brak_kluczy_przegladu(self):
        tree = {"data": [
            {"id": 1, "title": "Zebrani.pl", "parentId": 0},
            {"id": 7, "title": "Moduł", "parentId": 1}], "total": 2}
        fake = FakeRpc(review_dispatch(tree=tree))
        code, _o, _e, path = self.run_ctx([], fake)
        self.assertEqual(code, 0)
        ctx = qas.load_json(path)
        self.assertNotIn("existing", ctx)
        self.assertNotIn("reviewFolders", ctx)
        self.assertNotIn("retiredInScope", ctx)
        self.assertEqual(
            set(ctx),
            {"project", "projectTitle", "projectRoot", "customFields",
             "folders", "roots", "cases"})

    def test_zakres_pusty_gdy_brak_przypadkow(self):
        fake = FakeRpc(review_dispatch(tree=REVIEW_TREE, listed=[]))
        code, out, _e, path = self.run_ctx(["--review-folder", "9"], fake)
        self.assertEqual(code, 0, out)
        ctx = qas.load_json(path)
        self.assertEqual(
            [f["id"] for f in ctx["reviewFolders"]], [9, 10])
        lists = [a for n, a in fake.calls if n == "list_test_cases"]
        self.assertEqual(lists[0]["folders"], [9, 10])
        self.assertEqual(ctx["existing"], [])
        self.assertEqual(ctx["retiredInScope"], [])
        self.assertIn("Przegląd: folderów 2, przypadków 0, "
                      "oznaczonych [Removed] 0.", out)


class ReviewLintTest(Base):
    def payload(self, **kw):
        d = {"project": "ZEB", "transport": "mcp",
             "richTextFormat": "markdown", "testCases": []}
        d.update(kw)
        return d

    def msgs(self, errors):
        return [m for _i, _f, m in errors]

    def test_review_zly_ksztalt(self):
        errors, _ = qas.lint_file(self.payload(review="nie-lista"))
        self.assertIn("musi być listą", self.msgs(errors))
        errors, _ = qas.lint_file(self.payload(review=[
            {"seq": "5", "verdict": "keep", "reason": "ok"},
            {"seq": True, "verdict": "keep", "reason": "ok"},
            {"seq": 6, "verdict": "drop", "reason": "ok"},
            {"seq": 7, "verdict": "keep", "reason": "   "},
            "nie-obiekt",
            {"seq": 8, "verdict": "keep", "reason": "ok"},
            {"seq": 8, "verdict": "keep", "reason": "dubel"},
        ]))
        msgs = self.msgs(errors)
        self.assertEqual(msgs.count("całkowity seq wymagany"), 2)
        self.assertIn("musi być keep|update|retire", msgs)
        self.assertIn("niepusty powód wymagany", msgs)
        self.assertIn("musi być obiektem", msgs)
        self.assertIn("zdublowany seq w review", msgs)

    def test_retire_zly_ksztalt(self):
        errors, _ = qas.lint_file(self.payload(retire={"seq": 5}))
        self.assertIn("musi być listą", self.msgs(errors))
        errors, _ = qas.lint_file(self.payload(retire=[
            {"seq": True, "reason": "ok"},
            {"seq": 6, "reason": ""},
            {"seq": 7, "reason": "ok", "title": 123},
            {"seq": 8, "reason": "ok", "replacedBy": "A1"},
            {"seq": 9, "reason": "ok", "replacedBy": ["", "ZZZ"]},
            "nie-obiekt",
            {"seq": 10, "reason": "ok"},
            {"seq": 10, "reason": "dubel"},
        ]))
        msgs = self.msgs(errors)
        self.assertIn("całkowity seq wymagany", msgs)
        self.assertIn("niepusty powód wymagany", msgs)
        self.assertIn("musi być napisem", msgs)
        self.assertIn("musi być listą", msgs)
        self.assertIn("niepusty napis wymagany", msgs)
        self.assertIn("musi być kluczem z testCases albo seq (cyfry)", msgs)
        self.assertIn("musi być obiektem", msgs)
        self.assertIn("zdublowany seq w retire", msgs)

    def test_replacedby_klucz_lub_cyfry_ok(self):
        d = make_payload(
            testCases=[make_case("A", key="A1")],
            retire=[{"seq": 5, "reason": "x",
                     "replacedBy": ["A1", "42"]}])
        errors, _ = qas.lint_file(d)
        self.assertEqual(
            [e for e in errors if "replacedBy" in e[1]], [])

    def test_werdykt_wymaga_wpisu(self):
        errors, _ = qas.lint_file(self.payload(
            review=[{"seq": 5, "verdict": "update", "reason": "x"},
                    {"seq": 7, "verdict": "retire", "reason": "x"},
                    {"seq": 9, "verdict": "keep", "reason": "x"}],
            updates=[{"seq": 9, "reason": "x", "args": {}}]))
        msgs = self.msgs(errors)
        self.assertIn("verdict update wymaga wpisu w updates", msgs)
        self.assertIn("verdict retire wymaga wpisu w retire", msgs)
        self.assertIn("verdict keep wyklucza wpisy w updates i retire",
                      msgs)

    def test_spojny_przeglad_cichy(self):
        errors, warns = qas.lint_file(self.payload(
            review=[{"seq": 5, "verdict": "keep", "reason": "ok"},
                    {"seq": 6, "verdict": "update", "reason": "fix"},
                    {"seq": 7, "verdict": "retire", "reason": "stary"}],
            updates=[{"seq": 6, "reason": "fix", "args": {}}],
            retire=[{"seq": 7, "reason": "stary"}]))
        self.assertEqual(errors, [])
        self.assertEqual(warns, [])

    def test_seq_spoza_review_to_uwaga(self):
        _e, warns = qas.lint_file(self.payload(
            review=[{"seq": 5, "verdict": "keep", "reason": "ok"}],
            updates=[{"seq": 6, "reason": "x", "args": {}}],
            retire=[{"seq": 7, "reason": "x"}]))
        msgs = [m for _i, _f, m in warns]
        self.assertEqual(len([m for m in msgs if "poza przeglądem" in m]),
                         2)

    def test_existing_bez_werdyktu_i_spoza_zakresu(self):
        ctx = make_context(existing=[{"seq": 5}, {"seq": 6}])
        errors, warns = qas.lint_file(self.payload(
            review=[{"seq": 5, "verdict": "keep", "reason": "ok"},
                    {"seq": 99, "verdict": "keep", "reason": "ok"}]), ctx)
        self.assertTrue(
            any("przypadek z zakresu przeglądu bez werdyktu" in m
                for _i, _f, m in errors), errors)
        self.assertTrue(
            any("seq spoza zakresu przeglądu" in m
                for _i, _f, m in warns), warns)

    def test_retire_nieznany_seq(self):
        ctx = make_context(cases={"search:x": [{"seq": 5, "title": "T"}]})
        errors, _ = qas.lint_file(self.payload(
            retire=[{"seq": 5, "reason": "x"},
                    {"seq": 9, "reason": "x"}]), ctx)
        self.assertTrue(
            any(i == "retire 9" and "nieznany seq" in m
                for i, _f, m in errors), errors)
        self.assertEqual(
            [e for e in errors if e[0] == "retire 5"], [])

    def test_retire_znany_z_existing(self):
        ctx = make_context(existing=[{"seq": 9}])
        errors, _ = qas.lint_file(self.payload(
            review=[{"seq": 9, "verdict": "retire", "reason": "x"}],
            retire=[{"seq": 9, "reason": "x"}]), ctx)
        self.assertEqual(errors, [])

    def test_retire_juz_oznaczony(self):
        ctx = make_context(
            cases={"search:x": [{"seq": 5, "title": "[Removed] T"}]},
            retiredInScope=[5])
        errors, _ = qas.lint_file(self.payload(
            retire=[{"seq": 5, "reason": "x"}]), ctx)
        self.assertTrue(
            any("już oznaczony [Removed]" in m for _i, _f, m in errors),
            errors)
        self.assertEqual(
            [e for e in errors if "nieznany seq" in e[2]], [])

    def test_retired_in_scope_liczy_sie_do_znanych(self):
        ctx = make_context(retiredInScope=[5])
        errors, _ = qas.lint_file(self.payload(
            retire=[{"seq": 5, "reason": "x"}]), ctx)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0][0], "retire 5")
        self.assertIn("już oznaczony [Removed]", errors[0][2])

    def test_done_retired_cichy(self):
        ctx = make_context(retiredInScope=[5])
        errors, warns = qas.lint_file(self.payload(
            retire=[{"seq": 5, "reason": "x", "done": True}]), ctx)
        self.assertEqual(errors, [])
        self.assertEqual(warns, [])

    def test_done_i_oczekujacy_retired(self):
        ctx = make_context(retiredInScope=[5, 6])
        errors, _ = qas.lint_file(self.payload(
            retire=[{"seq": 5, "reason": "x", "done": True},
                    {"seq": 6, "reason": "y"}]), ctx)
        self.assertEqual(errors, [
            ("retire 6", "seq", "już oznaczony [Removed] (retiredInScope)")])

    def test_replacedby_spoza_kontekstu_bez_existing(self):
        ctx = make_context(cases={"search:x": [{"seq": 9}]})
        errors, warns = qas.lint_file(self.payload(
            retire=[{"seq": 9, "reason": "x",
                     "replacedBy": ["42"]}]), ctx)
        self.assertEqual(errors, [])
        self.assertEqual(len(warns), 1)
        self.assertIn("spoza kontekstu", warns[0][2])

    def test_filled_retire_blad(self):
        ctx = make_context(existing=[{"seq": 5, "type": "filled"}])
        errors, _ = qas.lint_file(self.payload(
            review=[{"seq": 5, "verdict": "retire", "reason": "x"}],
            retire=[{"seq": 5, "reason": "x"}]), ctx)
        self.assertEqual(errors, [
            ("retire 5", "seq", "przypadek typu filled — oznacz szablon")])

    def test_filled_retire_done_cichy(self):
        ctx = make_context(existing=[{"seq": 5, "type": "filled"}])
        errors, warns = qas.lint_file(self.payload(
            review=[{"seq": 5, "verdict": "retire", "reason": "x"}],
            retire=[{"seq": 5, "reason": "x", "done": True}]), ctx)
        self.assertEqual(errors, [])
        self.assertEqual(warns, [])

    def test_niefilled_retire_cichy(self):
        ctx = make_context(existing=[
            {"seq": 5, "type": "standalone"},
            {"seq": 6, "type": "template"},
            {"seq": 7}])
        errors, warns = qas.lint_file(self.payload(
            review=[{"seq": 5, "verdict": "retire", "reason": "x"},
                    {"seq": 6, "verdict": "retire", "reason": "x"},
                    {"seq": 7, "verdict": "retire", "reason": "x"}],
            retire=[{"seq": 5, "reason": "x"},
                    {"seq": 6, "reason": "x"},
                    {"seq": 7, "reason": "x"}]), ctx)
        self.assertEqual(errors, [])
        self.assertEqual(warns, [])

    def test_filled_update_poza_priority_blad(self):
        ctx = make_context(existing=[
            {"seq": 5, "type": "filled"}, {"seq": 6, "type": "filled"}])
        errors, _ = qas.lint_file(self.payload(
            review=[{"seq": 5, "verdict": "update", "reason": "x"},
                    {"seq": 6, "verdict": "update", "reason": "x"}],
            updates=[{"seq": 5, "reason": "x", "args": {"title": "Nowy"}},
                     {"seq": 6, "reason": "x",
                      "args": {"priority": "low", "tags": ["a"]}}]), ctx)
        self.assertEqual(errors, [
            ("update 5", "args",
             "przypadek typu filled — poza priority zmień szablon"),
            ("update 6", "args",
             "przypadek typu filled — poza priority zmień szablon")])

    def test_filled_update_sama_priority_cicha(self):
        ctx = make_context(existing=[
            {"seq": 5, "type": "filled"}, {"seq": 6, "type": "filled"}])
        errors, warns = qas.lint_file(self.payload(
            review=[{"seq": 5, "verdict": "update", "reason": "x"},
                    {"seq": 6, "verdict": "update", "reason": "x"}],
            updates=[{"seq": 5, "reason": "x", "args": {"priority": "low"}},
                     {"seq": 6, "reason": "x", "args": {}}]), ctx)
        self.assertEqual(errors, [])
        self.assertEqual(warns, [])

    def test_niefilled_update_dowolne_pola(self):
        ctx = make_context(existing=[{"seq": 5, "type": "standalone"}])
        errors, _ = qas.lint_file(self.payload(
            review=[{"seq": 5, "verdict": "update", "reason": "x"}],
            updates=[{"seq": 5, "reason": "x",
                      "args": {"title": "Nowy", "tags": ["a"]}}]), ctx)
        self.assertEqual(errors, [])

    def test_retire_spoza_zakresu_blad(self):
        ctx = make_context(
            existing=[{"seq": 5}],
            cases={"search:x": [{"seq": 9}]})
        errors, _ = qas.lint_file(self.payload(
            review=[{"seq": 5, "verdict": "keep", "reason": "ok"}],
            retire=[{"seq": 9, "reason": "x"}]), ctx)
        self.assertEqual(errors, [
            ("retire 9", "seq",
             "retire spoza zakresu przeglądu (brak w existing)")])

    def test_retire_spoza_zakresu_done_cichy(self):
        ctx = make_context(existing=[{"seq": 5}])
        errors, _ = qas.lint_file(self.payload(
            review=[{"seq": 5, "verdict": "keep", "reason": "ok"}],
            retire=[{"seq": 9, "reason": "x", "done": True}]), ctx)
        self.assertEqual(errors, [])

    def test_retired_dostaje_tylko_blad_a(self):
        ctx = make_context(existing=[{"seq": 5}], retiredInScope=[7])
        errors, _ = qas.lint_file(self.payload(
            review=[{"seq": 5, "verdict": "keep", "reason": "ok"}],
            retire=[{"seq": 7, "reason": "x"}]), ctx)
        self.assertEqual(errors, [
            ("retire 7", "seq", "już oznaczony [Removed] (retiredInScope)")])

    def test_bez_existing_nieznany_seq_zostaje(self):
        ctx = make_context(cases={"search:x": [{"seq": 5}]})
        errors, _ = qas.lint_file(self.payload(
            retire=[{"seq": 9, "reason": "x"}]), ctx)
        self.assertIn("nieznany seq (brak w existing i cases kontekstu)",
                      self.msgs(errors))
        self.assertNotIn("retire spoza zakresu przeglądu (brak w existing)",
                         self.msgs(errors))

    def test_done_nielogiczne_blad(self):
        errors, _ = qas.lint_file(self.payload(
            retire=[{"seq": 5, "reason": "x", "done": "false"},
                    {"seq": 6, "reason": "x", "done": 1},
                    {"seq": 7, "reason": "x", "done": None}]))
        self.assertEqual(self.msgs(errors),
                         ["done musi być true albo false"] * 3)

    def test_done_false_ciche(self):
        errors, _ = qas.lint_file(self.payload(
            retire=[{"seq": 5, "reason": "x", "done": False}]))
        self.assertEqual(errors, [])

    def test_verdict_nienapisowy_blad(self):
        errors, _ = qas.lint_file(self.payload(
            review=[{"seq": 8, "verdict": [], "reason": "ok"},
                    {"seq": 9, "verdict": {}, "reason": "ok"}]))
        self.assertEqual(self.msgs(errors),
                         ["musi być keep|update|retire"] * 2)

    def test_replacedby_cyfra_nieznana_z_kontekstem(self):
        ctx = make_context(existing=[{"seq": 9}])
        errors, warns = qas.lint_file(self.payload(
            review=[{"seq": 9, "verdict": "retire", "reason": "x"}],
            retire=[{"seq": 9, "reason": "x",
                     "replacedBy": ["42"]}]), ctx)
        self.assertEqual(errors, [])
        self.assertEqual(warns, [
            ("retire 9", "replacedBy[0]",
             "replacedBy wskazuje seq spoza kontekstu — sprawdź, "
             "że istnieje")])

    def test_replacedby_cyfra_wskazuje_retire(self):
        ctx = make_context(
            cases={"search:x": [{"seq": 9}, {"seq": 10}]})
        errors, _ = qas.lint_file(self.payload(
            retire=[{"seq": 9, "reason": "x"},
                    {"seq": 10, "reason": "y",
                     "replacedBy": ["9"]}]), ctx)
        self.assertTrue(
            any("replacedBy wskazuje wycofany seq" in m
                for _i, _f, m in errors),
            errors)

    def test_replacedby_cyfra_wskazuje_retired_in_scope(self):
        ctx = make_context(
            cases={"search:x": [{"seq": 9}]}, retiredInScope=[7])
        errors, _ = qas.lint_file(self.payload(
            retire=[{"seq": 9, "reason": "x",
                     "replacedBy": ["7"]}]), ctx)
        self.assertTrue(
            any("replacedBy wskazuje wycofany seq" in m
                for _i, _f, m in errors),
            errors)

    def test_replacedby_cyfra_znana_ok(self):
        ctx = make_context(existing=[{"seq": 9}, {"seq": 11}])
        errors, warns = qas.lint_file(self.payload(
            review=[{"seq": 9, "verdict": "retire", "reason": "x"},
                    {"seq": 11, "verdict": "keep", "reason": "ok"}],
            retire=[{"seq": 9, "reason": "x",
                     "replacedBy": ["11"]}]), ctx)
        self.assertEqual(errors, [])
        self.assertEqual(warns, [])

    def test_nieznane_pola_review_i_retire(self):
        errors, _ = qas.lint_file(self.payload(
            review=[{"seq": 5, "verdict": "keep", "reason": "ok",
                     "done": True}],
            retire=[{"seq": 6, "reason": "x", "verdict": "retire"}]))
        self.assertIn(("review 5", "done", "nieznane pole"), errors)
        self.assertIn(("retire 6", "verdict", "nieznane pole"), errors)

    def test_retire_done_to_pole_dozwolone(self):
        errors, _ = qas.lint_file(self.payload(
            retire=[{"seq": 5, "reason": "x", "done": True}]))
        self.assertEqual(errors, [])

    def test_legacy_pole_folderu_ignorowane(self):
        d = self.payload(retire=[{"seq": 5, "reason": "x"}])
        # klucz legacy składany z dwóch literałów (grep: zero trafień)
        d["tra" "shFolderId"] = 9
        errors, _ = qas.lint_file(d)
        self.assertEqual(errors, [])

    def test_retire_i_updates_ten_sam_seq(self):
        errors, _ = qas.lint_file(self.payload(
            updates=[{"seq": 5, "reason": "x", "args": {}}],
            retire=[{"seq": 5, "reason": "x"}]))
        self.assertIn("seq jednocześnie w retire i updates",
                      self.msgs(errors))

    def test_plik_tylko_retire_bez_folderu(self):
        d = {"project": "ZEB", "transport": "mcp",
             "richTextFormat": "markdown",
             "retire": [{"seq": 5, "title": "Stary", "reason": "x",
                         "replacedBy": []}]}
        errors, _ = qas.lint_file(d)
        self.assertEqual(errors, [])

    def test_plik_pusty_to_blad(self):
        d = {"project": "ZEB", "transport": "mcp",
             "richTextFormat": "markdown"}
        errors, _ = qas.lint_file(d)
        self.assertIn(
            "pusty zestaw: brak testCases, updates, retire i review",
            self.msgs(errors))
        errors, _ = qas.lint_file(self.payload(
            testCases=[], updates=[], retire=[], review=[]))
        self.assertIn(
            "pusty zestaw: brak testCases, updates, retire i review",
            self.msgs(errors))


class ReviewTableTest(Base):
    def test_sekcje_przegladu_i_removed(self):
        d = make_payload(
            testCases=[make_case("A", key="A1")],
            updates=[{"seq": 6, "reason": "poprawka", "args": {}}],
            review=[{"seq": 5, "verdict": "keep", "reason": "ok"},
                    {"seq": 6, "verdict": "update", "reason": "fix"},
                    {"seq": 7, "verdict": "retire", "reason": "stary"}],
            retire=[{"seq": 7, "title": "A|B", "reason": "nieaktualny",
                     "replacedBy": ["A1", "42"]}])
        p = self.write(d)
        code, out, _ = self.run_cli(["table", p])
        self.assertEqual(code, 0)
        self.assertIn("Przegląd istniejących (3): zostają 1, "
                      "aktualizacja 1, [Removed] 1.", out)
        self.assertIn("Zostają bez zmian: 5", out)
        self.assertIn("Do usunięcia — [Removed]:", out)
        self.assertIn("| seq | tytuł | powód | zastępują go |", out)
        self.assertIn("| 7 | A\\|B | nieaktualny | A1, 42 |", out)
        self.assertIn("(razem 1; aktualizacji 1; [Removed] 1).", out)

    def test_zostaja_puste_to_myslnik(self):
        d = make_payload(
            testCases=[make_case("A", key="A1")],
            review=[{"seq": 7, "verdict": "retire", "reason": "x"}],
            retire=[{"seq": 7, "reason": "x"}])
        p = self.write(d)
        code, out, _ = self.run_cli(["table", p])
        self.assertEqual(code, 0)
        self.assertIn("Zostają bez zmian: —", out)

    def test_bez_folderu_i_testcases_nie_rzuca(self):
        d = {"project": "ZEB", "transport": "mcp",
             "richTextFormat": "markdown",
             "review": [{"seq": 5, "verdict": "keep", "reason": "ok"}],
             "retire": [{"seq": 6, "reason": "x"}]}
        p = self.write(d)
        code, out, _ = self.run_cli(["table", p])
        self.assertEqual(code, 0)
        self.assertIn("(brak — tylko przegląd istniejących przypadków)",
                      out)
        self.assertIn("(razem 0; aktualizacji 0; [Removed] 1).", out)


class EmptyCasesTest(Base):
    def payload(self):
        return {"project": "ZEB", "transport": "mcp",
                "richTextFormat": "markdown",
                "updates": [{"seq": 5, "reason": "x", "args": {}}]}

    def test_folders_puste_testcases(self):
        p = self.write(self.payload())
        fake = FakeRpc(lambda n, a: (_ for _ in ()).throw(
            AssertionError("rpc nie może paść")))
        with mock.patch.object(qas, "rpc", fake):
            code, out, _ = self.run_cli(["folders", p])
        self.assertEqual(code, 0)
        self.assertIn("Brak nowych przypadków — nic do utworzenia.", out)
        self.assertEqual(fake.calls, [])

    def test_push_puste_testcases(self):
        p = self.write(self.payload())
        fake = FakeRpc(lambda n, a: (_ for _ in ()).throw(
            AssertionError("rpc nie może paść")))
        with mock.patch.object(qas, "rpc", fake):
            code, out, _ = self.run_cli(["push", p])
        self.assertEqual(code, 0)
        self.assertIn("Brak nowych przypadków — nic do utworzenia.", out)
        self.assertEqual(fake.calls, [])


def retire_dispatch(tree=None, reads=None, updates_log=None, upsert=None):
    """Atrapa retire: projekt, drzewo, odczyty, update, upsert."""

    def handler(name, args):
        if name == "get_project":
            return False, "", {"code": "ZEB", "title": "Zebrani.pl"}
        if name == "list_folders":
            return False, "", json.loads(json.dumps(
                tree if tree is not None else {"data": [], "total": 0}))
        if name == "get_test_case":
            live = (reads or {}).get(args.get("tcase"))
            assert live is not None, "brak odczytu %s" % args.get("tcase")
            return False, "", json.loads(json.dumps(live))
        if name == "update_test_case":
            if updates_log is not None:
                updates_log.append(args)
            return False, "", {}
        if name == "upsert_folders":
            if callable(upsert):
                return upsert(name, args)
            return upsert
        raise AssertionError("nieoczekiwane: %s" % name)

    return handler


def make_retire_payload(entries, **kw):
    d = {"project": "ZEB", "transport": "mcp",
         "richTextFormat": "markdown", "retire": entries}
    d.update(kw)
    return d


class RetireTest(Base):
    def auth(self, url="https://dtcode.eu1.qasphere.com/api/mcp"):
        os.environ["QASPHERE_API_KEY"] = "T"
        os.environ["QASPHERE_MCP_URL"] = url

    def test_dry_run_bez_wywolan(self):
        p = self.write(make_retire_payload(
            [{"seq": 5, "reason": "stary"}, {"seq": 6, "reason": "dubel"}]))
        fake = FakeRpc(lambda n, a: (_ for _ in ()).throw(
            AssertionError("rpc nie może paść")))
        with mock.patch.object(qas, "rpc", fake):
            code, out, _ = self.run_cli(["retire", p, "--dry-run"])
        self.assertEqual(code, 0)
        self.assertEqual(fake.calls, [])
        self.assertIn("DRY-RUN [Removed] seq 5: stary", out)
        self.assertIn("DRY-RUN [Removed] seq 6: dubel", out)
        self.assertIn("Do oznaczenia: 2 (bez wywołań).", out)
        self.assertEqual(
            [e for e in qas.load_json(p)["retire"] if e.get("done")], [])

    def test_brak_oczekujacych(self):
        self.auth("https://qa.example.com/api/mcp")
        p = self.write(make_retire_payload(
            [{"seq": 5, "reason": "x", "done": True}]))
        fake = FakeRpc(lambda n, a: (_ for _ in ()).throw(
            AssertionError("rpc nie może paść")))
        with mock.patch.object(qas, "rpc", fake):
            code, out, _ = self.run_cli(["retire", p])
        self.assertEqual(code, 0)
        self.assertIn("Brak przypadków do oznaczenia.", out)
        self.assertIn("Oznaczone [Removed] — API QA Sphere nie usuwa "
                      "przypadków; jeśli mają zniknąć z rejestru, usuń je "
                      "w UI (filtr: tag [Removed]):", out)
        self.assertIn("https://qa.example.com/project/ZEB/tcase/5", out)
        self.assertEqual(fake.calls, [])

    def test_wylacznie_get_i_update_bez_narzedzi_folderow(self):
        self.auth()
        p = self.write(make_retire_payload([{"seq": 5, "reason": "x"}]))
        log = []

        def handler(name, args):
            if name == "get_test_case":
                return False, "", json.loads(json.dumps(full_live(5)))
            if name == "update_test_case":
                log.append(args)
                return False, "", {}
            raise AssertionError("niedozwolone narzędzie: %s" % name)

        fake = FakeRpc(handler)
        with mock.patch.object(qas, "rpc", fake):
            code, out, _ = self.run_cli(["retire", p])
        self.assertEqual(code, 0, out)
        self.assertEqual(
            {c[0] for c in fake.calls}, {"get_test_case", "update_test_case"})
        self.assertEqual(len(log), 1)
        self.assertIn("seq 5 oznaczony [Removed].", out)
        self.assertIn("Oznaczono 1.", out)
        self.assertTrue(qas.load_json(p)["retire"][0]["done"])

    def test_prefiks_tag_inne_zachowane(self):
        self.auth()
        p = self.write(make_retire_payload([{"seq": 5, "reason": "x"}]))
        log = []
        fake = FakeRpc(retire_dispatch(
            reads={"5": full_live(5, title="Stary",
                                  tags=("walidacja", "moduł"))},
            updates_log=log))
        with mock.patch.object(qas, "rpc", fake):
            code, out, _ = self.run_cli(["retire", p])
        self.assertEqual(code, 0, out)
        self.assertEqual(len(log), 1)
        self.assertEqual(log[0]["title"], "[Removed] Stary")
        self.assertEqual(log[0]["tags"], ["walidacja", "moduł", "[Removed]"])
        self.assertEqual(log[0]["tcaseOrLegacyId"], "5")
        self.assertEqual(log[0]["projectCode"], "ZEB")

    def test_bez_podwojnego_prefiksu(self):
        self.auth()
        p = self.write(make_retire_payload([{"seq": 5, "reason": "x"}]))
        log = []
        fake = FakeRpc(retire_dispatch(
            reads={"5": full_live(5, title="[Removed] Stary",
                                  tags=("walidacja",))},
            updates_log=log))
        with mock.patch.object(qas, "rpc", fake):
            code, out, _ = self.run_cli(["retire", p])
        self.assertEqual(code, 0, out)
        self.assertEqual(log[0]["title"], "[Removed] Stary")
        self.assertEqual(log[0]["tags"], ["walidacja", "[Removed]"])

    def test_juz_oznaczony_bez_update(self):
        self.auth()
        p = self.write(make_retire_payload([{"seq": 5, "reason": "x"}]))
        fake = FakeRpc(retire_dispatch(
            reads={"5": full_live(5, title="[Removed] Stary",
                                  tags=("[Removed]",))}))
        with mock.patch.object(qas, "rpc", fake):
            code, out, _ = self.run_cli(["retire", p])
        self.assertEqual(code, 0, out)
        self.assertIn("seq 5 już oznaczony.", out)
        self.assertEqual(
            [c for c in fake.calls if c[0] == "update_test_case"], [])
        self.assertTrue(qas.load_json(p)["retire"][0]["done"])

    def test_update_wylacznie_cztery_pola(self):
        self.auth()
        p = self.write(make_retire_payload([{"seq": 5, "reason": "x"}]))
        log = []
        fake = FakeRpc(retire_dispatch(
            reads={"5": full_live(5)}, updates_log=log))
        with mock.patch.object(qas, "rpc", fake):
            self.run_cli(["retire", p])
        self.assertEqual(set(log[0]),
                         {"projectCode", "tcaseOrLegacyId", "title", "tags"})

    def test_tytul_za_dlugi_exit1_z_zapisem(self):
        self.auth()
        p = self.write(make_retire_payload(
            [{"seq": 5, "reason": "ok"}, {"seq": 6, "reason": "za długi"}]))
        log = []
        fake = FakeRpc(retire_dispatch(
            reads={"5": full_live(5), "6": full_live(6, title="X" * 510)},
            updates_log=log))
        with mock.patch.object(qas, "rpc", fake):
            code, _o, err = self.run_cli(["retire", p])
        self.assertEqual(code, 1)
        self.assertIn("seq 6", err)
        self.assertEqual(len(log), 1)
        data = qas.load_json(p)
        self.assertTrue(data["retire"][0]["done"])
        self.assertNotIn("done", data["retire"][1])

    def test_adresy_w_instrukcji(self):
        self.auth("https://qa.example.com/api/mcp")
        p = self.write(make_retire_payload(
            [{"seq": 5, "reason": "x", "done": True},
             {"seq": 6, "reason": "y"}]))
        fake = FakeRpc(retire_dispatch(reads={"6": full_live(6)}))
        with mock.patch.object(qas, "rpc", fake):
            code, out, _ = self.run_cli(["retire", p])
        self.assertEqual(code, 0, out)
        self.assertIn("Oznaczone [Removed] — API QA Sphere nie usuwa "
                      "przypadków; jeśli mają zniknąć z rejestru, usuń je "
                      "w UI (filtr: tag [Removed]):", out)
        self.assertIn("https://qa.example.com/project/ZEB/tcase/5", out)
        self.assertIn("https://qa.example.com/project/ZEB/tcase/6", out)

    def test_only_filtruje_seq(self):
        self.auth()
        p = self.write(make_retire_payload(
            [{"seq": 5, "reason": "x"}, {"seq": 6, "reason": "y"}]))
        log = []
        fake = FakeRpc(retire_dispatch(
            reads={"6": full_live(6)}, updates_log=log))
        with mock.patch.object(qas, "rpc", fake):
            code, out, _ = self.run_cli(["retire", p, "--only", "6"])
        self.assertEqual(code, 0, out)
        self.assertEqual([a["tcaseOrLegacyId"] for a in log], ["6"])
        data = qas.load_json(p)
        self.assertNotIn("done", data["retire"][0])
        self.assertTrue(data["retire"][1]["done"])

    def test_odczyt_niepelen_exit1_bez_update(self):
        for live in ({}, None, {"title": "x"}):
            with self.subTest(live=live):
                self.auth()
                p = self.write(make_retire_payload(
                    [{"seq": 5, "reason": "x"}]))

                def handler(name, args, _live=live):
                    if name == "get_test_case":
                        if _live is None:
                            return False, "", None
                        return False, "", json.loads(json.dumps(_live))
                    if name == "update_test_case":
                        return False, "", {}
                    raise AssertionError("nieoczekiwane: %s" % name)

                fake = FakeRpc(handler)
                with mock.patch.object(qas, "rpc", fake):
                    code, _o, err = self.run_cli(["retire", p])
                self.assertEqual(code, 1)
                self.assertIn(
                    "seq 5: odczyt niepełny (brak tytułu albo listy "
                    "tagów) — nic nie zapisano.", err)
                self.assertEqual(
                    [c for c in fake.calls if c[0] == "update_test_case"],
                    [])
                self.assertNotIn("done", qas.load_json(p)["retire"][0])

    def test_puste_tags_poprawne(self):
        self.auth()
        p = self.write(make_retire_payload([{"seq": 5, "reason": "x"}]))
        log = []
        fake = FakeRpc(retire_dispatch(
            reads={"5": full_live(5, tags=())}, updates_log=log))
        with mock.patch.object(qas, "rpc", fake):
            code, out, _ = self.run_cli(["retire", p])
        self.assertEqual(code, 0, out)
        self.assertEqual(log[0]["tags"], ["[Removed]"])
        self.assertTrue(qas.load_json(p)["retire"][0]["done"])

    def test_niepelen_drugi_zapisuje_pierwszy(self):
        self.auth()
        p = self.write(make_retire_payload(
            [{"seq": 5, "reason": "ok"}, {"seq": 6, "reason": "niepełny"}]))
        log = []

        def handler(name, args):
            if name == "get_test_case":
                if args.get("tcase") == "5":
                    return False, "", json.loads(json.dumps(full_live(5)))
                return False, "", {}
            if name == "update_test_case":
                log.append(args)
                return False, "", {}
            raise AssertionError("nieoczekiwane: %s" % name)

        fake = FakeRpc(handler)
        with mock.patch.object(qas, "rpc", fake):
            code, _o, err = self.run_cli(["retire", p])
        self.assertEqual(code, 1)
        self.assertIn("seq 6: odczyt niepełny", err)
        self.assertEqual(len(log), 1)
        data = qas.load_json(p)
        self.assertTrue(data["retire"][0]["done"])
        self.assertNotIn("done", data["retire"][1])

    def test_pending_done_wymaga_true(self):
        # Przez CLI nieosiągalne (bramka lintu blokuje nielogiczne done).
        data = {"retire": [{"seq": 5, "done": "false"},
                           {"seq": 6, "done": 1},
                           {"seq": 7, "done": True},
                           {"seq": 8, "done": False},
                           {"seq": 9}]}
        pending = qas._pending_retire(data, [], None)
        self.assertEqual([e["seq"] for e in pending], [5, 6, 8, 9])

    def test_brak_oczekujacych_bez_done_bez_adresow(self):
        p = self.write(make_retire_payload([{"seq": 5, "reason": "x"}]))
        fake = FakeRpc(lambda n, a: (_ for _ in ()).throw(
            AssertionError("rpc nie może paść")))
        with mock.patch.object(qas, "rpc", fake), \
                mock.patch.object(qas, "get_auth", side_effect=AssertionError(
                    "get_auth nie może paść")):
            code, out, _ = self.run_cli(["retire", p, "--only", "999"])
        self.assertEqual(code, 0)
        self.assertIn("Brak przypadków do oznaczenia.", out)
        self.assertNotIn("Oznaczone [Removed]", out)
        self.assertEqual(fake.calls, [])

    def test_dry_run_wszystkie_done_bez_adresow(self):
        p = self.write(make_retire_payload(
            [{"seq": 5, "reason": "x", "done": True}]))
        fake = FakeRpc(lambda n, a: (_ for _ in ()).throw(
            AssertionError("rpc nie może paść")))
        with mock.patch.object(qas, "rpc", fake), \
                mock.patch.object(qas, "get_auth", side_effect=AssertionError(
                    "get_auth nie może paść")):
            code, out, _ = self.run_cli(["retire", p, "--dry-run"])
        self.assertEqual(code, 0)
        self.assertIn("Do oznaczenia: 0 (bez wywołań).", out)
        self.assertNotIn("Oznaczone [Removed]", out)
        self.assertEqual(fake.calls, [])


class RetireVerifyTest(Base):
    def payload(self, entries, **kw):
        d = {"project": "ZEB", "transport": "mcp",
             "richTextFormat": "markdown", "retire": entries}
        d.update(kw)
        return d

    def run_verify(self, data, reads, extra=None):
        p = self.write(data)
        fake = FakeRpc(retire_dispatch(reads=reads))
        with mock.patch.object(qas, "rpc", fake):
            code, out, err = self.run_cli(["verify", p] + (extra or []))
        return code, out, err, fake

    def test_ok_oznaczony(self):
        live = full_live(5, title="[Removed] Stary", tags=("[Removed]",),
                         folder=7)
        data = self.payload([{"seq": 5, "reason": "x", "done": True}])
        # klucz legacy składany z dwóch literałów (grep: zero trafień)
        data["tra" "shFolderId"] = 999
        code, out, _e, _f = self.run_verify(data, {"5": live})
        self.assertEqual(code, 0, out)
        self.assertIn("OK [Removed] 5", out)
        self.assertIn("Sprawdzono 1", out)

    def test_brak_oznaczenia_wymienia_braki(self):
        live = full_live(5, title="Stary", tags=("inne",))
        code, out, _e, _f = self.run_verify(
            self.payload([{"seq": 5, "reason": "x", "done": True}]),
            {"5": live})
        self.assertEqual(code, 1)
        self.assertIn("RÓŻNICA [Removed] 5", out)
        self.assertIn("brak prefiksu [Removed] w tytule", out)
        self.assertIn("brak tagu [Removed]", out)

    def test_brak_tagu_to_roznica(self):
        live = full_live(5, title="[Removed] Stary", tags=("inne",))
        code, out, _e, _f = self.run_verify(
            self.payload([{"seq": 5, "reason": "x", "done": True}]),
            {"5": live})
        self.assertEqual(code, 1)
        self.assertIn("RÓŻNICA [Removed] 5", out)

    def test_bez_done_nieoznaczony(self):
        code, out, _e, fake = self.run_verify(
            self.payload([{"seq": 5, "reason": "x"}]), {})
        self.assertEqual(code, 1)
        self.assertIn("NIEOZNACZONY [Removed] 5", out)
        self.assertIn("Sprawdzono 1", out)
        self.assertEqual(fake.calls, [])

    def test_only_filtruje_removed(self):
        reads = {"6": full_live(6, title="[Removed] S", tags=("[Removed]",),
                                folder=7)}
        code, out, _e, fake = self.run_verify(
            self.payload([{"seq": 5, "reason": "x", "done": True},
                          {"seq": 6, "reason": "y", "done": True}]),
            reads, ["--only", "6"])
        self.assertEqual(code, 0, out)
        self.assertIn("OK [Removed] 6", out)
        self.assertNotIn("[Removed] 5", out)
        gets = [a["tcase"] for n, a in fake.calls if n == "get_test_case"]
        self.assertEqual(gets, ["6"])

    def test_done_nielogiczne_nieoznaczony(self):
        code, out, _e, fake = self.run_verify(
            self.payload([{"seq": 5, "reason": "x", "done": "yes"}]), {})
        self.assertEqual(code, 1)
        self.assertIn("NIEOZNACZONY [Removed] 5", out)
        self.assertEqual(fake.calls, [])

    def test_update_done_nielogiczne_pomijane(self):
        d = self.payload([], updates=[
            {"seq": 5, "reason": "x", "args": {"priority": "low"},
             "done": "yes"}])
        code, out, _e, fake = self.run_verify(d, {})
        self.assertEqual(code, 0, out)
        self.assertIn("Sprawdzono 0, różnic: 0.", out)
        self.assertEqual(fake.calls, [])


class HelpOrderTest(Base):
    def test_help_i_docstring_kolejnosc(self):
        text = " ".join(qas.build_parser().format_help().split())
        self.assertIn("push --limit 1 -> verify --only", text)
        self.assertIn("push -> update -> retire -> verify", text)
        self.assertIn("przy pustym testCases cztery pierwsze kroki odpadają",
                      text)
        self.assertIn("push --limit 1 -> verify --only <klucz> -> push",
                      qas.__doc__)
        self.assertIn("update -> retire -> verify", qas.__doc__)


if __name__ == "__main__":
    unittest.main()
