import json
import re
import sys
import threading
import unittest
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).parents[1]))

from app import build_handler  # noqa: E402
from config import Account, Settings  # noqa: E402
from graph import GraphClient  # noqa: E402

_ACCOUNT = Account("Damian", "Damian.Dziura@DTCode.pl", "16d86420-aaaa-bbbb-cccc-1234567890ab")
_TOKEN = "secret-damian-token"

_VTT_TEXT = (
    "WEBVTT\n"
    "\n"
    "00:00:07.153 --> 00:00:08.593\n"
    "<v Damian Dziura>To jest testowe spotkanie.</v>\n"
    "\n"
    "00:00:12.713 --> 00:00:20.033\n"
    "<v Damian Dziura>Chcę, żebyś utworzył notatki z tego spotkania.</v>\n"
)

_METADATA_TEXT = (
    "WEBVTT\n"
    "\n"
    "00:00:07.153 --> 00:00:08.593\n"
    '{"speakerName": "Damian Dziura", "spokenText": "To jest testowe spotkanie.", '
    '"spokenLanguage": "pl-pl", "startDateTime": "2026-09-18T09:36:35.0000000Z", '
    '"endDateTime": "2026-09-18T09:36:36.0000000Z"}\n'
)

_MEETING_ID = "MSoxNmQ4NjQyMC1hYWFhLWJiYmItY2NjYy0xMjM0NTY3ODkwYWIqMCoq"


def _meeting_payload() -> dict:
    return {
        "id": _MEETING_ID,
        "subject": "test",
        "startDateTime": "2026-09-18T10:00:00Z",
        "endDateTime": "2026-09-18T10:30:00Z",
        "joinWebUrl": (
            "https://teams.microsoft.com/l/meetup-join/19%3ameeting_xxxx%40thread.v2/0"
            "?context=%7b%22Tid%22%3a%22tenant-guid%22%2c%22Oid%22%3a%22oid-guid%22%7d"
        ),
        "joinMeetingIdSettings": {"joinMeetingId": "391328174033204"},
        "participants": {"organizer": {"identity": {"user": {"id": _ACCOUNT.id}}}},
    }


def _transcripts_payload() -> dict:
    return {
        "value": [
            {
                "id": "ktViz-transcript-1",
                "createdDateTime": "2026-09-18T09:36:28Z",
                "endDateTime": "2026-09-18T09:37:00Z",
                "meetingOrganizer": {},
            }
        ]
    }


def _route(url: str) -> str:
    if "onlineMeetings?$filter=" in url:
        return "lookup"
    if re.search(r"/transcripts/[^/]+/content\?\$format=text/vtt$", url):
        return "content"
    if url.endswith("/metadataContent"):
        return "metadata"
    if url.endswith("/transcripts"):
        return "transcripts"
    if re.search(r"/onlineMeetings/[^/]+$", url):
        return "meeting"
    return "unknown"


def _stub_transport_empty_transcripts(url, headers):
    kind = _route(url)
    if kind == "lookup":
        return 200, json.dumps({"value": [_meeting_payload()]}).encode("utf-8"), {"Content-Type": "application/json"}
    if kind == "transcripts":
        return 200, json.dumps({"value": []}).encode("utf-8"), {"Content-Type": "application/json"}
    if kind == "meeting":
        return 200, json.dumps(_meeting_payload()).encode("utf-8"), {"Content-Type": "application/json"}
    raise AssertionError(f"nieobsłużone żądanie testowe: {url}")


def _stub_transport(url, headers):
    kind = _route(url)
    if kind == "lookup":
        return 200, json.dumps({"value": [_meeting_payload()]}).encode("utf-8"), {"Content-Type": "application/json"}
    if kind == "transcripts":
        return 200, json.dumps(_transcripts_payload()).encode("utf-8"), {"Content-Type": "application/json"}
    if kind == "content":
        return 200, _VTT_TEXT.encode("utf-8"), {"Content-Type": "text/vtt"}
    if kind == "metadata":
        return 200, _METADATA_TEXT.encode("utf-8"), {"Content-Type": "text/vtt"}
    if kind == "meeting":
        return 200, json.dumps(_meeting_payload()).encode("utf-8"), {"Content-Type": "application/json"}
    raise AssertionError(f"nieobsłużone żądanie testowe: {url}")


def _settings() -> Settings:
    return Settings(
        tenant_id="tenant",
        client_id="client",
        cert_path=Path("cert.pem"),
        key_path=Path("key.pem"),
        accounts=(_ACCOUNT,),
        tokens={_TOKEN: "damian"},
        port=8080,
        timezone=ZoneInfo("Europe/Warsaw"),
        timezone_name="Europe/Warsaw",
    )


class _ServerTestCase(unittest.TestCase):
    transport = staticmethod(_stub_transport)

    @classmethod
    def setUpClass(cls):
        client = GraphClient(transport=cls.transport, token_provider=lambda: "graph-token")
        handler_cls = build_handler(_settings(), client)
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), handler_cls)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def _request(self, method: str, path: str, body: bytes | None = None, headers: dict[str, str] | None = None):
        connection = HTTPConnection(*self.server.server_address)
        try:
            send_headers = dict(headers or {})
            if body is not None:
                send_headers.setdefault("Content-Length", str(len(body)))
            connection.request(method, path, body=body, headers=send_headers)
            response = connection.getresponse()
            raw = response.read()
            return response.status, response.getheader("Content-Type"), raw
        finally:
            connection.close()

    def _auth_headers(self, token: str = _TOKEN) -> dict[str, str]:
        return {"Authorization": f"Bearer {token}"}


class HealthEndpointTests(_ServerTestCase):
    def test_health_returns_byte_identical_body_without_auth(self):
        status, content_type, raw = self._request("GET", "/health")
        self.assertEqual(status, 200)
        self.assertEqual(raw, b'{"status":"ok","service":"teams-transcript-bridge"}')
        self.assertEqual(content_type, "application/json")

    def test_health_wrong_method_is_405(self):
        status, _content_type, raw = self._request("POST", "/health", body=b"{}")
        self.assertEqual(status, 405)
        self.assertEqual(json.loads(raw)["error"]["code"], "method_not_allowed")


class AuthTests(_ServerTestCase):
    def test_missing_token_on_resolve_is_401(self):
        status, _ct, raw = self._request("POST", "/meetings/resolve", body=b"{}")
        self.assertEqual(status, 401)
        self.assertEqual(json.loads(raw)["error"]["code"], "unauthorized")

    def test_wrong_token_on_resolve_is_401(self):
        status, _ct, raw = self._request(
            "POST", "/meetings/resolve", body=b"{}", headers={"Authorization": "Bearer wrong-token"}
        )
        self.assertEqual(status, 401)
        self.assertEqual(json.loads(raw)["error"]["code"], "unauthorized")

    def test_missing_token_on_transcript_endpoint_is_401(self):
        status, _ct, raw = self._request("GET", f"/meetings/{_ACCOUNT.id}/{_MEETING_ID}/transcript")
        self.assertEqual(status, 401)
        self.assertEqual(json.loads(raw)["error"]["code"], "unauthorized")


class RoutingErrorTests(_ServerTestCase):
    def test_unknown_path_is_404_not_found(self):
        status, _ct, raw = self._request("GET", "/anything", headers=self._auth_headers())
        self.assertEqual(status, 404)
        self.assertEqual(json.loads(raw)["error"]["code"], "not_found")

    def test_health_path_never_requires_auth_even_when_unknown_method_style(self):
        status, _ct, _raw = self._request("GET", "/health")
        self.assertEqual(status, 200)

    def test_oversized_body_is_413(self):
        body = json.dumps({"link": "x" * (65 * 1024)}).encode("utf-8")
        status, _ct, raw = self._request("POST", "/meetings/resolve", body=body, headers=self._auth_headers())
        self.assertEqual(status, 413)
        self.assertEqual(json.loads(raw)["error"]["code"], "payload_too_large")

    def test_unparsable_json_is_400(self):
        status, _ct, raw = self._request(
            "POST", "/meetings/resolve", body=b"{not json", headers=self._auth_headers()
        )
        self.assertEqual(status, 400)
        self.assertEqual(json.loads(raw)["error"]["code"], "bad_request")

    def test_resolve_without_link_date_or_title_is_400(self):
        status, _ct, raw = self._request(
            "POST", "/meetings/resolve", body=b"{}", headers=self._auth_headers()
        )
        self.assertEqual(status, 400)
        self.assertEqual(json.loads(raw)["error"]["code"], "bad_request")


class ResolveByLinkFlowTests(_ServerTestCase):
    def test_resolve_by_link_returns_candidate_matching_context_shapes(self):
        body = json.dumps({"link": "https://teams.microsoft.com/meet/391328174033204?p=GBQvD2H3Gm5XAdUnBp"}).encode(
            "utf-8"
        )
        status, _ct, raw = self._request(
            "POST", "/meetings/resolve", body=body, headers=self._auth_headers()
        )
        self.assertEqual(status, 200)
        payload = json.loads(raw)
        self.assertEqual(payload["skipped_without_teams_link"], 0)
        candidate = payload["candidates"][0]
        self.assertEqual(candidate["meetingId"], _MEETING_ID)
        self.assertEqual(candidate["account"], {"label": "Damian", "upn": _ACCOUNT.upn, "id": _ACCOUNT.id})
        self.assertEqual(candidate["subject"], "test")
        self.assertEqual(candidate["start"], "2026-09-18T10:00:00Z")
        self.assertEqual(candidate["end"], "2026-09-18T10:30:00Z")
        self.assertEqual(candidate["organizer"], {"name": "Damian", "email": _ACCOUNT.upn})
        self.assertEqual(candidate["joinMeetingId"], "391328174033204")
        self.assertEqual(
            candidate["transcripts"],
            [{"id": "ktViz-transcript-1", "createdDateTime": "2026-09-18T09:36:28Z", "endDateTime": "2026-09-18T09:37:00Z"}],
        )

    def test_invalid_link_value_is_400_invalid_link(self):
        body = json.dumps({"link": "to nie jest link"}).encode("utf-8")
        status, _ct, raw = self._request(
            "POST", "/meetings/resolve", body=body, headers=self._auth_headers()
        )
        self.assertEqual(status, 400)
        self.assertEqual(json.loads(raw)["error"]["code"], "invalid_link")


class TranscriptFlowTests(_ServerTestCase):
    def test_transcript_json_matches_context_vtt_content(self):
        status, _ct, raw = self._request(
            "GET", f"/meetings/{_ACCOUNT.id}/{_MEETING_ID}/transcript", headers=self._auth_headers()
        )
        self.assertEqual(status, 200)
        payload = json.loads(raw)
        self.assertEqual(payload["meeting"]["meetingId"], _MEETING_ID)
        self.assertEqual(payload["meeting"]["joinMeetingId"], "391328174033204")
        transcript = payload["transcript"]
        self.assertEqual(transcript["id"], "ktViz-transcript-1")
        self.assertEqual(transcript["language"], "pl-pl")
        self.assertEqual(transcript["speakers"], ["Damian Dziura"])
        self.assertEqual(
            transcript["segments"][0],
            {"start": "00:00:07.153", "end": "00:00:08.593", "speaker": "Damian Dziura", "text": "To jest testowe spotkanie."},
        )
        self.assertEqual(transcript["vtt"], _VTT_TEXT)

    def test_transcript_format_vtt_returns_raw_text(self):
        status, content_type, raw = self._request(
            "GET",
            f"/meetings/{_ACCOUNT.id}/{_MEETING_ID}/transcript?format=vtt",
            headers=self._auth_headers(),
        )
        self.assertEqual(status, 200)
        self.assertEqual(content_type, "text/vtt; charset=utf-8")
        self.assertEqual(raw.decode("utf-8"), _VTT_TEXT)

    def test_unknown_account_id_is_400(self):
        status, _ct, raw = self._request(
            "GET", f"/meetings/not-a-configured-account/{_MEETING_ID}/transcript", headers=self._auth_headers()
        )
        self.assertEqual(status, 400)
        self.assertEqual(json.loads(raw)["error"]["code"], "unknown_account")


class TranscriptNotFoundTests(_ServerTestCase):
    transport = staticmethod(_stub_transport_empty_transcripts)

    def test_empty_transcript_list_is_404_transcript_not_found(self):
        status, _ct, raw = self._request(
            "GET", f"/meetings/{_ACCOUNT.id}/{_MEETING_ID}/transcript", headers=self._auth_headers()
        )
        self.assertEqual(status, 404)
        self.assertEqual(json.loads(raw)["error"]["code"], "transcript_not_found")


_CALL_ID = "a16d2948-e3f1-4e16-8dc1-eaf4edad4c14"


def _adhoc_route(url: str) -> str:
    if "getAllTranscripts" in url:
        return "adhoc_list"
    if re.search(r"/transcripts/[^/]+/content\?\$format=text/vtt$", url):
        return "content"
    if url.endswith("/metadataContent"):
        return "metadata"
    if re.search(r"/adhocCalls/[^/]+/transcripts/[^/]+$", url):
        return "adhoc_meta"
    return "unknown"


def _adhoc_item_payload() -> dict:
    return {
        "id": "ktViz-adhoc-1",
        "meetingId": None,
        "callId": _CALL_ID,
        "createdDateTime": "2026-09-18T12:00:00Z",
        "endDateTime": "2026-09-18T12:05:00Z",
        "meetingOrganizer": {"user": {"id": _ACCOUNT.id, "displayName": None, "tenantId": "tenant"}},
    }


def _stub_transport_adhoc(url, headers):
    kind = _adhoc_route(url)
    if kind == "adhoc_list":
        return 200, json.dumps({"value": [_adhoc_item_payload()]}).encode("utf-8"), {"Content-Type": "application/json"}
    if kind == "adhoc_meta":
        return 200, json.dumps(_adhoc_item_payload()).encode("utf-8"), {"Content-Type": "application/json"}
    if kind == "content":
        return 200, _VTT_TEXT.encode("utf-8"), {"Content-Type": "text/vtt"}
    if kind == "metadata":
        return 200, _METADATA_TEXT.encode("utf-8"), {"Content-Type": "text/vtt"}
    raise AssertionError(f"nieobsłużone żądanie testowe: {url}")


def _stub_transport_adhoc_empty(url, headers):
    if _adhoc_route(url) == "adhoc_list":
        return 200, json.dumps({"value": []}).encode("utf-8"), {"Content-Type": "application/json"}
    raise AssertionError(f"nieobsłużone żądanie testowe: {url}")


class AdhocCallTranscriptFlowTests(_ServerTestCase):
    transport = staticmethod(_stub_transport_adhoc)

    def test_call_transcript_json_matches_context_vtt_content(self):
        status, _ct, raw = self._request(
            "GET", f"/calls/{_ACCOUNT.id}/{_CALL_ID}/transcript", headers=self._auth_headers()
        )
        self.assertEqual(status, 200)
        payload = json.loads(raw)
        self.assertEqual(payload["meeting"]["kind"], "adhocCall")
        self.assertEqual(payload["meeting"]["callId"], _CALL_ID)
        self.assertIsNone(payload["meeting"]["meetingId"])
        transcript = payload["transcript"]
        self.assertEqual(transcript["id"], "ktViz-adhoc-1")
        self.assertEqual(transcript["language"], "pl-pl")
        self.assertEqual(transcript["speakers"], ["Damian Dziura"])
        self.assertEqual(transcript["vtt"], _VTT_TEXT)

    def test_call_transcript_format_vtt_returns_raw_text(self):
        status, content_type, raw = self._request(
            "GET",
            f"/calls/{_ACCOUNT.id}/{_CALL_ID}/transcript?format=vtt",
            headers=self._auth_headers(),
        )
        self.assertEqual(status, 200)
        self.assertEqual(content_type, "text/vtt; charset=utf-8")
        self.assertEqual(raw.decode("utf-8"), _VTT_TEXT)

    def test_call_transcript_with_transcript_id_uses_metadata_endpoint(self):
        status, _ct, raw = self._request(
            "GET",
            f"/calls/{_ACCOUNT.id}/{_CALL_ID}/transcript?transcriptId=ktViz-adhoc-1",
            headers=self._auth_headers(),
        )
        self.assertEqual(status, 200)
        payload = json.loads(raw)
        self.assertEqual(payload["transcript"]["id"], "ktViz-adhoc-1")

    def test_call_transcript_unknown_account_id_is_400(self):
        status, _ct, raw = self._request(
            "GET", f"/calls/not-a-configured-account/{_CALL_ID}/transcript", headers=self._auth_headers()
        )
        self.assertEqual(status, 400)
        self.assertEqual(json.loads(raw)["error"]["code"], "unknown_account")


class AdhocCallTranscriptNotFoundTests(_ServerTestCase):
    transport = staticmethod(_stub_transport_adhoc_empty)

    def test_empty_adhoc_list_is_404_transcript_not_found(self):
        status, _ct, raw = self._request(
            "GET", f"/calls/{_ACCOUNT.id}/{_CALL_ID}/transcript", headers=self._auth_headers()
        )
        self.assertEqual(status, 404)
        self.assertEqual(json.loads(raw)["error"]["code"], "transcript_not_found")


if __name__ == "__main__":
    unittest.main()
