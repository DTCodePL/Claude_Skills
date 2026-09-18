"""Testy `scripts/bridge.py` — unittest, bez sieci.

Stub transportu naśladuje kształty odpowiedzi z references/api.md.
Uruchomienie:
    cd D:\\projects\\DTCode\\Claude_Skills\\teams-notatki
    PYTHONIOENCODING=utf-8 python -m unittest discover -s tests -v
"""

from __future__ import annotations

import io
import json
import os
import sys
import tempfile
import unittest
import urllib.error
from contextlib import redirect_stderr, redirect_stdout

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import bridge  # noqa: E402


def make_response(status, payload, content_type="application/json"):
    """(status, payload) -> (status, bytes, content_type) tak jak default_transport."""
    if isinstance(payload, (dict, list)):
        content = json.dumps(payload).encode("utf-8")
    elif isinstance(payload, str):
        content = payload.encode("utf-8")
    else:
        content = payload
    return status, content, content_type


class StubTransport:
    """Kolejka zaprogramowanych odpowiedzi/wyjątków; zapamiętuje każde wywołanie."""

    def __init__(self, responses):
        self._responses = list(responses)
        self.calls = []

    def __call__(self, method, url, headers, body):
        self.calls.append({"method": method, "url": url, "headers": dict(headers), "body": body})
        if not self._responses:
            raise AssertionError("StubTransport: brak zaprogramowanej odpowiedzi na kolejne wywołanie")
        item = self._responses.pop(0)
        if callable(item):
            return item(method, url, headers, body)
        return item


def raise_connection_error(*_args, **_kwargs):
    raise urllib.error.URLError("Connection refused")


def run_main(argv, transport=None):
    """Wywołuje bridge.main() przechwytując stdout/stderr. Zwraca (kod, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = bridge.main(argv, transport=transport)
    return code, out.getvalue(), err.getvalue()


class EnvVarCleanupMixin:
    def setUp(self):
        super().setUp()
        self._saved_env = {
            "TEAMS_NOTATKI_URL": os.environ.get("TEAMS_NOTATKI_URL"),
            "TEAMS_NOTATKI_TOKEN": os.environ.get("TEAMS_NOTATKI_TOKEN"),
        }
        os.environ.pop("TEAMS_NOTATKI_URL", None)
        os.environ.pop("TEAMS_NOTATKI_TOKEN", None)

    def tearDown(self):
        for key, value in self._saved_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        super().tearDown()


class HeadersAndUserAgentTests(EnvVarCleanupMixin, unittest.TestCase):
    def test_health_sends_authorization_and_user_agent(self):
        stub = StubTransport([make_response(200, {"status": "ok", "service": "teams-transcript-bridge"})])
        code, _out, _err = run_main(["health"], transport=stub)

        self.assertEqual(code, 0)
        self.assertEqual(len(stub.calls), 1)
        headers = stub.calls[0]["headers"]
        self.assertEqual(headers["Authorization"], f"Bearer {bridge.DEFAULT_TOKEN}")
        self.assertEqual(headers["User-Agent"], "teams-notatki-cli")

    def test_resolve_sends_authorization_and_user_agent(self):
        stub = StubTransport([make_response(200, {"candidates": [], "skipped_without_teams_link": 0})])
        code, _out, _err = run_main(["resolve", "--title", "status"], transport=stub)

        self.assertEqual(code, 0)
        headers = stub.calls[0]["headers"]
        self.assertEqual(headers["Authorization"], f"Bearer {bridge.DEFAULT_TOKEN}")
        self.assertEqual(headers["User-Agent"], "teams-notatki-cli")


class ResolveRequestBodyTests(EnvVarCleanupMixin, unittest.TestCase):
    def test_resolve_link_builds_correct_body(self):
        stub = StubTransport([make_response(200, {"candidates": [], "skipped_without_teams_link": 0})])
        code, _out, _err = run_main(
            ["resolve", "--link", "https://teams.microsoft.com/meet/391328174033204?p=abc"],
            transport=stub,
        )

        self.assertEqual(code, 0)
        call = stub.calls[0]
        self.assertEqual(call["method"], "POST")
        self.assertTrue(call["url"].endswith("/meetings/resolve"))
        body = json.loads(call["body"])
        self.assertEqual(body, {"link": "https://teams.microsoft.com/meet/391328174033204?p=abc"})

    def test_resolve_date_time_title_window_days_builds_correct_body(self):
        stub = StubTransport([make_response(200, {"candidates": [], "skipped_without_teams_link": 0})])
        code, _out, _err = run_main(
            [
                "resolve",
                "--date", "2026-09-18",
                "--time", "10:00",
                "--title", "status projektu",
                "--window-days", "3",
            ],
            transport=stub,
        )

        self.assertEqual(code, 0)
        body = json.loads(stub.calls[0]["body"])
        self.assertEqual(
            body,
            {"date": "2026-09-18", "time": "10:00", "title": "status projektu", "window_days": 3},
        )

    def test_resolve_without_link_date_or_title_is_usage_error(self):
        code, _out, err = run_main(["resolve"], transport=StubTransport([]))
        self.assertEqual(code, 1)
        self.assertIn("BŁĄD", err)


class ResolveTextRenderingTests(EnvVarCleanupMixin, unittest.TestCase):
    def test_text_mode_renders_list_with_warsaw_time(self):
        payload = {
            "candidates": [
                {
                    "meetingId": "MSoxNjZmYWJjZA==",
                    "account": {"label": "Damian", "upn": "damian@dtcode.pl", "id": "16d8f2b0-0000-0000-0000-000000000000"},
                    "subject": "Status projektu",
                    "start": "2026-09-18T10:00:00Z",
                    "end": "2026-09-18T10:30:00Z",
                    "organizer": {"name": "Damian Dziura", "email": "damian@dtcode.pl"},
                    "joinMeetingId": "391 328 174 033 204",
                    "joinWebUrl": "https://teams.microsoft.com/l/meetup-join/...",
                    "transcripts": [{"id": "t1", "createdDateTime": "2026-09-18T10:31:00Z", "endDateTime": "2026-09-18T10:31:30Z"}],
                }
            ],
            "skipped_without_teams_link": 0,
        }
        stub = StubTransport([make_response(200, payload)])
        code, out, _err = run_main(["resolve", "--title", "status", "--text"], transport=stub)

        self.assertEqual(code, 0)
        # 2026-09-18T10:00:00Z (UTC) -> 12:00 w Europie/Warszawie (CEST, wrzesień).
        # Gdy na maszynie brak bazy stref IANA (typowe na Windows, patrz SKILL.md/api.md),
        # bridge.py celowo spada na UTC z dopiskiem "(UTC)" — sprawdzamy oba warianty,
        # bo test nie może zależeć od tego, czy pakiet tzdata jest zainstalowany.
        if bridge.ZoneInfo is not None:
            try:
                bridge.ZoneInfo("Europe/Warsaw")
                has_tzdata = True
            except bridge.ZoneInfoNotFoundError:
                has_tzdata = False
        else:
            has_tzdata = False

        if has_tzdata:
            self.assertIn("12:00", out)
            self.assertIn("(PL)", out)
        else:
            self.assertIn("10:00", out)
            self.assertIn("(UTC)", out)
        self.assertIn("Status projektu", out)
        self.assertIn("organizator: Damian Dziura", out)
        self.assertIn("transkrypcje: 1", out)

    def test_text_mode_no_candidates(self):
        stub = StubTransport([make_response(200, {"candidates": [], "skipped_without_teams_link": 0})])
        code, out, _err = run_main(["resolve", "--title", "cokolwiek", "--text"], transport=stub)
        self.assertEqual(code, 0)
        self.assertIn("Brak kandydatów", out)


class TranscriptMarkdownTests(EnvVarCleanupMixin, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)

    def _transcript_payload(self):
        return {
            "meeting": {
                "meetingId": "MSoxNjZm",
                "subject": "Status projektu",
                "start": "2026-09-18T10:00:00Z",
                "end": "2026-09-18T10:30:00Z",
                "organizerId": "16d8f2b0-0000-0000-0000-000000000000",
                "joinMeetingId": "391 328 174 033 204",
            },
            "transcript": {
                "id": "t1",
                "createdDateTime": "2026-09-18T10:00:07Z",
                "endDateTime": "2026-09-18T10:15:00Z",
                "language": "pl-PL",
                "speakers": ["Damian Dziura", "Piotr Tuński"],
                "segments": [
                    {"start": "00:00:07.153", "end": "00:00:08.593", "speaker": "Damian Dziura", "text": "Cześć,"},
                    {"start": "00:00:08.700", "end": "00:00:09.500", "speaker": "Damian Dziura", "text": "zaczynamy."},
                    {"start": "00:00:12.500", "end": "00:00:15.000", "speaker": "Piotr Tuński", "text": "Jasne."},
                ],
                "vtt": "WEBVTT\n\n1\n00:00:07.153 --> 00:00:08.593\n<v Damian Dziura>Cześć,</v>\n",
            },
        }

    def test_transcript_out_md_merges_same_speaker_segments(self):
        out_path = os.path.join(self.tmpdir.name, "test.md")
        stub = StubTransport([make_response(200, self._transcript_payload())])
        code, _out, _err = run_main(
            ["transcript", "--account", "16d8f2b0-0000-0000-0000-000000000000", "--meeting", "MSoxNjZm", "--out", out_path],
            transport=stub,
        )

        self.assertEqual(code, 0)
        with open(out_path, "r", encoding="utf-8") as handle:
            content = handle.read()

        # 00:00:07.153 -> [00:07]; dwa segmenty Damiana sklejone w jeden akapit z czasem PIERWSZEGO
        self.assertIn("**[00:07] Damian Dziura:** Cześć, zaczynamy.", content)
        self.assertNotIn("[00:08]", content)  # drugi segment nie ma własnej linii
        self.assertIn("**[00:12] Piotr Tuński:** Jasne.", content)

    def test_transcript_out_json_uses_quoted_url_path(self):
        out_path = os.path.join(self.tmpdir.name, "test.json")
        stub = StubTransport([make_response(200, self._transcript_payload())])
        code, _out, _err = run_main(
            ["transcript", "--account", "16d8f2b0-0000-0000-0000-000000000000", "--meeting", "MSox*NjZm=", "--out", out_path],
            transport=stub,
        )

        self.assertEqual(code, 0)
        # meetingId z '*' i '=' musi być zakodowany w URL-u
        self.assertIn("MSox%2ANjZm%3D", stub.calls[0]["url"])
        with open(out_path, "r", encoding="utf-8") as handle:
            saved = json.load(handle)
        self.assertEqual(saved["meeting"]["subject"], "Status projektu")
        self.assertEqual(len(saved["transcript"]["segments"]), 3)

    def test_transcript_out_vtt_writes_vtt_field(self):
        out_path = os.path.join(self.tmpdir.name, "test.vtt")
        payload = self._transcript_payload()
        stub = StubTransport([make_response(200, payload)])
        code, _out, _err = run_main(
            ["transcript", "--account", "acc", "--meeting", "m1", "--out", out_path],
            transport=stub,
        )

        self.assertEqual(code, 0)
        with open(out_path, "r", encoding="utf-8") as handle:
            content = handle.read()
        self.assertEqual(content, payload["transcript"]["vtt"])


class ParseVttEquivalenceTests(EnvVarCleanupMixin, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)

    def test_parse_vtt_matches_bridge_path_for_same_segments(self):
        vtt_text = (
            "WEBVTT\n\n"
            "1\n"
            "00:00:07.153 --> 00:00:09.500\n"
            "<v Damian Dziura>Cze&#347;&#263;, zaczynamy &amp; kontynuujemy.</v>\n\n"
            "2\n"
            "00:00:09.600 --> 00:00:12.000\n"
            "<v Damian Dziura>Dzi&#281;kuj&#281; za przyj&#347;cie.</v>\n\n"
            "3\n"
            "00:00:12.500 --> 00:00:15.000\n"
            "<v Piotr Tu&#324;ski>Jasne, mo&#380;emy zaczyna&#263;.</v>\n"
        )

        # Ścieżka 1: parse-vtt (bez mostka)
        vtt_path = os.path.join(self.tmpdir.name, "spotkanie.vtt")
        with open(vtt_path, "w", encoding="utf-8") as handle:
            handle.write(vtt_text)
        md_from_parse_vtt = os.path.join(self.tmpdir.name, "przez-parse-vtt.md")
        code1, _out1, _err1 = run_main(["parse-vtt", "--file", vtt_path, "--out", md_from_parse_vtt])
        self.assertEqual(code1, 0)

        # Ścieżka 2: mostek zwraca transkrypcję z segmentami wynikającymi z tego samego VTT
        expected_segments = bridge.parse_vtt(vtt_text)
        speakers = sorted({seg["speaker"] for seg in expected_segments if seg.get("speaker")})
        bridge_payload = {
            "meeting": {},
            "transcript": {
                "id": "t1",
                "createdDateTime": None,
                "endDateTime": None,
                "language": None,
                "speakers": speakers,
                "segments": expected_segments,
                "vtt": vtt_text,
            },
        }
        md_from_bridge = os.path.join(self.tmpdir.name, "przez-mostek.md")
        stub = StubTransport([make_response(200, bridge_payload)])
        code2, _out2, _err2 = run_main(
            ["transcript", "--account", "acc", "--meeting", "m1", "--out", md_from_bridge],
            transport=stub,
        )
        self.assertEqual(code2, 0)

        with open(md_from_parse_vtt, "r", encoding="utf-8") as handle:
            content_parse_vtt = handle.read()
        with open(md_from_bridge, "r", encoding="utf-8") as handle:
            content_bridge = handle.read()

        self.assertEqual(content_parse_vtt, content_bridge)
        # I encje HTML zostały poprawnie odkodowane po obu stronach
        self.assertIn("Cześć, zaczynamy & kontynuujemy.", content_parse_vtt)
        self.assertIn("Piotr Tuński", content_parse_vtt)


class ExitCodeTests(EnvVarCleanupMixin, unittest.TestCase):
    def test_unauthorized_exits_4(self):
        stub = StubTransport(
            [make_response(401, {"error": {"code": "unauthorized", "message": "Token nieaktualny"}})]
        )
        code, _out, err = run_main(["health"], transport=stub)
        self.assertEqual(code, 4)
        self.assertIn("unauthorized", err)

    def test_meeting_not_found_exits_3(self):
        stub = StubTransport(
            [make_response(404, {"error": {"code": "meeting_not_found", "message": "Nie znaleziono spotkania"}})]
        )
        code, _out, err = run_main(["resolve", "--title", "cokolwiek"], transport=stub)
        self.assertEqual(code, 3)
        self.assertIn("meeting_not_found", err)

    def test_transcript_not_found_exits_3(self):
        stub = StubTransport(
            [make_response(404, {"error": {"code": "transcript_not_found", "message": "Transkrypcji jeszcze nie ma"}})]
        )
        code, _out, err = run_main(["transcript", "--account", "acc", "--meeting", "m1"], transport=stub)
        self.assertEqual(code, 3)

    def test_connection_error_exits_5_and_mentions_vtt_fallback(self):
        stub = StubTransport([raise_connection_error])
        code, _out, err = run_main(["health"], transport=stub)
        self.assertEqual(code, 5)
        self.assertIn("connection_error", err)
        self.assertIn(bridge.DEFAULT_URL, err)
        self.assertIn(".vtt", err)
        self.assertIn("parse-vtt", err)


class EnvOverrideTests(EnvVarCleanupMixin, unittest.TestCase):
    def test_env_vars_override_url_and_token(self):
        os.environ["TEAMS_NOTATKI_URL"] = "https://example.test"
        os.environ["TEAMS_NOTATKI_TOKEN"] = "tok-z-env"

        stub = StubTransport([make_response(200, {"status": "ok", "service": "teams-transcript-bridge"})])
        code, _out, _err = run_main(["health"], transport=stub)

        self.assertEqual(code, 0)
        call = stub.calls[0]
        self.assertTrue(call["url"].startswith("https://example.test/"))
        self.assertEqual(call["headers"]["Authorization"], "Bearer tok-z-env")

    def test_default_url_and_token_used_without_env(self):
        stub = StubTransport([make_response(200, {"status": "ok", "service": "teams-transcript-bridge"})])
        code, _out, _err = run_main(["health"], transport=stub)

        self.assertEqual(code, 0)
        call = stub.calls[0]
        self.assertTrue(call["url"].startswith(bridge.DEFAULT_URL))
        self.assertEqual(call["headers"]["Authorization"], f"Bearer {bridge.DEFAULT_TOKEN}")


if __name__ == "__main__":
    unittest.main()
