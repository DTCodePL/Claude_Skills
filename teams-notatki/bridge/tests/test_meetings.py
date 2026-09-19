import json
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).parents[1]))

import meetings  # noqa: E402
from config import Account, Settings  # noqa: E402
from graph import GraphClient, GraphError, GraphTransportError, graph_error_response  # noqa: E402


def _settings(accounts: list[Account]) -> Settings:
    return Settings(
        tenant_id="tenant",
        client_id="client",
        cert_path=Path("cert.pem"),
        key_path=Path("key.pem"),
        accounts=tuple(accounts),
        tokens={},
        port=8080,
        timezone=ZoneInfo("Europe/Warsaw"),
        timezone_name="Europe/Warsaw",
    )


def _json_response(payload: object) -> tuple[int, bytes, dict[str, str]]:
    return 200, json.dumps(payload).encode("utf-8"), {"Content-Type": "application/json"}


def _error_response(status: int, code: str, message: str) -> tuple[int, bytes, dict[str, str]]:
    payload = {"error": {"code": code, "message": message}}
    return status, json.dumps(payload).encode("utf-8"), {"Content-Type": "application/json"}


class RoutedTransport:
    """Transport testowy: dopasowuje URL do zarejestrowanych reguł, w kolejności rejestracji."""

    def __init__(self) -> None:
        self.calls: list[str] = []
        self._rules: list[tuple[Callable[[str], bool], object]] = []

    def rule(self, predicate: Callable[[str], bool], response: object) -> None:
        self._rules.append((predicate, response))

    def __call__(self, url: str, headers: dict[str, str]) -> tuple[int, bytes, dict[str, str]]:
        self.calls.append(url)
        for predicate, response in self._rules:
            if predicate(url):
                return response(url) if callable(response) else response
        raise AssertionError(f"nieobsłużone żądanie testowe: {url}")


def _client(transport: RoutedTransport) -> GraphClient:
    return GraphClient(transport=transport, token_provider=lambda: "test-token")


def _online_meeting(
    meeting_id: str,
    join_meeting_id: str,
    join_web_url: str,
    organizer_id: str = "organizer-guid",
    subject: str = "test",
) -> dict:
    return {
        "id": meeting_id,
        "subject": subject,
        "startDateTime": "2026-09-18T10:00:00Z",
        "endDateTime": "2026-09-18T10:30:00Z",
        "joinWebUrl": join_web_url,
        "joinMeetingIdSettings": {"joinMeetingId": join_meeting_id},
        "participants": {"organizer": {"identity": {"user": {"id": organizer_id}}}},
    }


class ParseLinkTests(unittest.TestCase):
    def test_meet_url_with_query_param(self):
        query = meetings.parse_link("https://teams.microsoft.com/meet/391328174033204?p=GBQvD2H3Gm5XAdUnBp")
        self.assertEqual(query.kind, "joinMeetingId")
        self.assertEqual(query.value, "391328174033204")

    def test_digits_with_spaces(self):
        query = meetings.parse_link("391 328 174 033 204")
        self.assertEqual(query.kind, "joinMeetingId")
        self.assertEqual(query.value, "391328174033204")

    def test_plain_digits(self):
        query = meetings.parse_link("391328174033204")
        self.assertEqual(query.kind, "joinMeetingId")
        self.assertEqual(query.value, "391328174033204")

    def test_unrecognized_value_raises_invalid_link_error(self):
        with self.assertRaises(meetings.InvalidLinkError):
            meetings.parse_link("to nie jest link")

    def test_encoded_and_decoded_meetup_join_produce_identical_filter_value(self):
        encoded = (
            "https://teams.microsoft.com/l/meetup-join/19%3ameeting_abc%40thread.v2/0"
            "?context=%7b%22Tid%22%3a%22t1%22%2c%22Oid%22%3a%22o1%22%7d"
        )
        decoded = (
            'https://teams.microsoft.com/l/meetup-join/19:meeting_abc@thread.v2/0'
            '?context={"Tid":"t1","Oid":"o1"}'
        )
        q_encoded = meetings.parse_link(encoded)
        q_decoded = meetings.parse_link(decoded)
        self.assertEqual(q_encoded.kind, "joinWebUrl")
        self.assertEqual(q_encoded.value, encoded)
        self.assertEqual(q_encoded.value, q_decoded.value)

    def test_meetup_join_with_html_escaped_ampersand_between_query_params(self):
        raw = (
            "https://teams.microsoft.com/l/meetup-join/19%3ameeting_abc%40thread.v2/0"
            "?context=%7b%22Tid%22%3a%22t1%22%7d&amp;anchor=1"
        )
        query = meetings.parse_link(raw)
        self.assertEqual(query.kind, "joinWebUrl")
        self.assertNotIn("&amp;", query.value)
        self.assertIn("context=%7b%22Tid%22%3a%22t1%22%7d", query.value)
        self.assertIn("anchor=1", query.value)


class NormalizePlTests(unittest.TestCase):
    def test_strips_polish_diacritics_and_lowercases(self):
        self.assertEqual(meetings.normalize_pl("Żółć ĄĆĘŁŃÓŚŹŻ"), "zolc acelnoszz")

    def test_title_matches_regardless_of_case_and_diacritics(self):
        needle = meetings.normalize_pl("status projektu")
        self.assertIn(needle, meetings.normalize_pl("Status Projektu — Zebrani"))
        self.assertIn(needle, meetings.normalize_pl("STATUS PROJEKTU"))


class ResolveWindowTests(unittest.TestCase):
    def test_local_midnight_to_midnight_converts_to_utc(self):
        start_utc, end_utc = meetings._resolve_query_window("2026-09-18", 0, ZoneInfo("Europe/Warsaw"))
        self.assertEqual(start_utc.strftime("%Y-%m-%dT%H:%M:%SZ"), "2026-09-17T22:00:00Z")
        self.assertEqual(end_utc.strftime("%Y-%m-%dT%H:%M:%SZ"), "2026-09-18T22:00:00Z")

    def test_window_days_extends_both_directions(self):
        start_utc, end_utc = meetings._resolve_query_window("2026-09-18", 2, ZoneInfo("Europe/Warsaw"))
        self.assertEqual(start_utc.strftime("%Y-%m-%dT%H:%M:%SZ"), "2026-09-15T22:00:00Z")
        self.assertEqual(end_utc.strftime("%Y-%m-%dT%H:%M:%SZ"), "2026-09-20T22:00:00Z")

    def test_no_date_falls_back_to_last_30_days(self):
        start_utc, end_utc = meetings._resolve_query_window(None, 0, ZoneInfo("Europe/Warsaw"))
        self.assertAlmostEqual((end_utc - start_utc).days, 30)


class ResolveByLinkTests(unittest.TestCase):
    def test_tries_accounts_in_order_and_stops_at_first_hit(self):
        damian = Account("Damian", "damian@x.pl", "acc-damian")
        piotr = Account("Piotr", "piotr@x.pl", "acc-piotr")
        settings = _settings([damian, piotr])
        meeting = _online_meeting("meeting-1", "391328174033204", "https://teams.microsoft.com/l/meetup-join/x", organizer_id="acc-piotr")

        transport = RoutedTransport()
        transport.rule(lambda u: "acc-damian/onlineMeetings?" in u, _json_response({"value": []}))
        transport.rule(lambda u: "acc-piotr/onlineMeetings?" in u, _json_response({"value": [meeting]}))
        transport.rule(lambda u: u.endswith("/transcripts"), _json_response({"value": []}))

        link_query = meetings.parse_link("391328174033204")
        candidate, accounts_tried = meetings.resolve_by_link(_client(transport), settings, link_query)

        self.assertEqual(accounts_tried, 2)
        self.assertEqual(candidate["account"]["id"], "acc-piotr")
        self.assertEqual(candidate["organizerId"], "acc-piotr")
        self.assertEqual(candidate["organizer"], {"name": "Piotr", "email": "piotr@x.pl"})
        self.assertEqual(candidate["joinMeetingId"], "391328174033204")
        self.assertEqual(candidate["transcripts"], [])

    def test_no_hits_on_any_account_raises_meeting_not_found(self):
        settings = _settings([Account("Damian", "damian@x.pl", "acc-damian")])
        transport = RoutedTransport()
        transport.rule(lambda u: "onlineMeetings?" in u, _json_response({"value": []}))

        with self.assertRaises(meetings.MeetingNotFoundError) as ctx:
            meetings.resolve_by_link(_client(transport), settings, meetings.parse_link("391328174033204"))
        self.assertIn("Damian", str(ctx.exception))

    def test_organizer_left_null_when_id_does_not_match_any_configured_account(self):
        settings = _settings([Account("Damian", "damian@x.pl", "acc-damian")])
        meeting = _online_meeting("meeting-1", "391328174033204", "https://x", organizer_id="unknown-guid")
        transport = RoutedTransport()
        transport.rule(lambda u: "onlineMeetings?" in u, _json_response({"value": [meeting]}))
        transport.rule(lambda u: u.endswith("/transcripts"), _json_response({"value": []}))

        candidate, _ = meetings.resolve_by_link(_client(transport), settings, meetings.parse_link("391328174033204"))
        self.assertEqual(candidate["organizer"], {"name": None, "email": None})
        self.assertEqual(candidate["organizerId"], "unknown-guid")

    def test_graph_400_on_lookup_is_treated_as_no_hit_and_falls_through_to_next_account(self):
        # Zmierzone na żywym tenancie: Graph odpowiada 400 "1025: An error has occurred."
        # dla joinMeetingId, który po prostu nie istnieje — to nie błąd serwera.
        damian = Account("Damian", "damian@x.pl", "acc-damian")
        piotr = Account("Piotr", "piotr@x.pl", "acc-piotr")
        settings = _settings([damian, piotr])
        meeting = _online_meeting("meeting-1", "999999999999999", "https://x", organizer_id="acc-piotr")

        transport = RoutedTransport()
        transport.rule(
            lambda u: "acc-damian/onlineMeetings?" in u,
            _error_response(400, "BadRequest", "1025: An error has occurred."),
        )
        transport.rule(lambda u: "acc-piotr/onlineMeetings?" in u, _json_response({"value": [meeting]}))
        transport.rule(lambda u: u.endswith("/transcripts"), _json_response({"value": []}))

        link_query = meetings.parse_link("999999999999999")
        candidate, accounts_tried = meetings.resolve_by_link(_client(transport), settings, link_query)

        self.assertEqual(accounts_tried, 2)
        self.assertEqual(candidate["account"]["id"], "acc-piotr")

    def test_graph_400_on_every_account_raises_meeting_not_found_not_a_502(self):
        settings = _settings([Account("Damian", "damian@x.pl", "acc-damian"), Account("Piotr", "piotr@x.pl", "acc-piotr")])
        transport = RoutedTransport()
        transport.rule(
            lambda u: "onlineMeetings?" in u,
            _error_response(400, "BadRequest", "1025: An error has occurred."),
        )

        with self.assertRaises(meetings.MeetingNotFoundError):
            meetings.resolve_by_link(_client(transport), settings, meetings.parse_link("999999999999999"))

    def test_non_400_graph_error_on_lookup_still_propagates(self):
        settings = _settings([Account("Damian", "damian@x.pl", "acc-damian")])
        transport = RoutedTransport()
        transport.rule(
            lambda u: "onlineMeetings?" in u,
            _error_response(403, "Forbidden", "brak dostępu"),
        )

        with self.assertRaises(GraphError) as ctx:
            meetings.resolve_by_link(_client(transport), settings, meetings.parse_link("391328174033204"))
        self.assertEqual(ctx.exception.status, 403)


class FetchCalendarViewPaginationTests(unittest.TestCase):
    def test_follows_odata_next_link_until_exhausted(self):
        account = Account("Damian", "damian@x.pl", "acc-damian")
        page_two_url = "https://graph.microsoft.com/v1.0/users/acc-damian/calendarView?$skip=50"

        transport = RoutedTransport()
        transport.rule(
            lambda u: u.startswith("https://graph.microsoft.com/v1.0/users/acc-damian/calendarView?startDateTime"),
            _json_response({"value": [{"subject": "page1"}], "@odata.nextLink": page_two_url}),
        )
        transport.rule(lambda u: u == page_two_url, _json_response({"value": [{"subject": "page2"}]}))

        from datetime import datetime, timezone

        events = meetings._fetch_calendar_view(
            _client(transport), account, datetime(2026, 9, 17, 22, tzinfo=timezone.utc), datetime(2026, 9, 18, 22, tzinfo=timezone.utc)
        )
        self.assertEqual([e["subject"] for e in events], ["page1", "page2"])


class LinkFromEventBodyTests(unittest.TestCase):
    def test_extracts_numeric_link_from_body_when_online_meeting_is_null(self):
        event = {
            "onlineMeeting": None,
            "body": {"content": '<a href="https://teams.microsoft.com/meet/333222111000999?p=abc">Join</a>'},
        }
        query = meetings._link_query_from_event(event)
        self.assertEqual(query.kind, "joinMeetingId")
        self.assertEqual(query.value, "333222111000999")

    def test_extracts_meetup_join_link_from_html_encoded_body(self):
        event = {
            "onlineMeeting": None,
            "body": {
                "content": (
                    '<a href="https://teams.microsoft.com/l/meetup-join/19%3ameeting_abc%40thread.v2/0'
                    '?context=%7b%22Tid%22%3a%22t1%22%7d&amp;anchor=0">Join</a>'
                )
            },
        }
        query = meetings._link_query_from_event(event)
        self.assertEqual(query.kind, "joinWebUrl")
        self.assertIn("context=%7b%22Tid%22%3a%22t1%22%7d", query.value)

    def test_returns_none_when_no_teams_link_present(self):
        event = {"onlineMeeting": None, "body": {"content": "<p>brak linku</p>"}}
        self.assertIsNone(meetings._link_query_from_event(event))


class ResolveByDateTitleTests(unittest.TestCase):
    def _calendar_event(self, subject: str, start_iso: str, meet_id: str) -> dict:
        return {
            "subject": subject,
            "start": {"dateTime": start_iso, "timeZone": "UTC"},
            "end": {"dateTime": start_iso, "timeZone": "UTC"},
            "organizer": {"emailAddress": {"name": "Ktoś Tam", "address": "ktos@x.pl"}},
            "isOnlineMeeting": True,
            "onlineMeeting": {"joinUrl": f"https://teams.microsoft.com/meet/{meet_id}"},
            "body": {"content": ""},
        }

    def _stub_lookup_and_transcripts(self, transport: RoutedTransport, meet_ids: list[str], account_id: str) -> None:
        for meet_id in meet_ids:
            meeting = _online_meeting(f"meeting-{meet_id}", meet_id, "https://x", organizer_id="nobody")
            transport.rule(
                lambda u, meet_id=meet_id, meeting=meeting: f"'{meet_id}'" in u,
                _json_response({"value": [meeting]}),
            )
        transport.rule(lambda u: u.endswith("/transcripts"), _json_response({"value": []}))
        transport.rule(lambda u: "getAllTranscripts" in u, _json_response({"value": []}))

    def test_title_filter_matches_regardless_of_case_and_polish_diacritics(self):
        account = Account("Damian", "damian@x.pl", "acc-damian")
        settings = _settings([account])
        events = [
            self._calendar_event("Status Projektu — Zebrani", "2026-09-18T08:00:00.0000000", "111111111"),
            self._calendar_event("STATUS PROJEKTU", "2026-09-18T09:00:00.0000000", "222222222"),
            self._calendar_event("Coś zupełnie innego", "2026-09-18T10:00:00.0000000", "333333333"),
        ]
        transport = RoutedTransport()
        transport.rule(lambda u: "/calendarView?" in u, _json_response({"value": events}))
        self._stub_lookup_and_transcripts(transport, ["111111111", "222222222", "333333333"], account.id)

        candidates, skipped = meetings.resolve_by_date_title(
            _client(transport), settings, "2026-09-18", None, "status projektu", 0
        )
        self.assertEqual({c["joinMeetingId"] for c in candidates}, {"111111111", "222222222"})
        self.assertEqual(skipped, 0)

    def test_time_window_keeps_events_within_90_minutes_and_drops_others(self):
        account = Account("Damian", "damian@x.pl", "acc-damian")
        settings = _settings([account])
        events = [
            self._calendar_event("W oknie", "2026-09-18T08:50:00.0000000", "111111111"),  # 50 min od 08:00Z
            self._calendar_event("Poza oknem", "2026-09-18T09:35:00.0000000", "222222222"),  # 95 min od 08:00Z
        ]
        transport = RoutedTransport()
        transport.rule(lambda u: "/calendarView?" in u, _json_response({"value": events}))
        self._stub_lookup_and_transcripts(transport, ["111111111", "222222222"], account.id)

        candidates, _skipped = meetings.resolve_by_date_title(
            _client(transport), settings, "2026-09-18", "10:00", None, 0
        )
        self.assertEqual([c["joinMeetingId"] for c in candidates], ["111111111"])

    def test_events_without_teams_link_are_counted_as_skipped(self):
        account = Account("Damian", "damian@x.pl", "acc-damian")
        settings = _settings([account])
        event = {
            "subject": "Brak linku",
            "start": {"dateTime": "2026-09-18T08:00:00.0000000", "timeZone": "UTC"},
            "end": {"dateTime": "2026-09-18T08:30:00.0000000", "timeZone": "UTC"},
            "organizer": {"emailAddress": {"name": "X", "address": "x@x.pl"}},
            "isOnlineMeeting": True,
            "onlineMeeting": None,
            "body": {"content": "<p>brak linku</p>"},
        }
        transport = RoutedTransport()
        transport.rule(lambda u: "/calendarView?" in u, _json_response({"value": [event]}))
        transport.rule(lambda u: "getAllTranscripts" in u, _json_response({"value": []}))

        candidates, skipped = meetings.resolve_by_date_title(_client(transport), settings, "2026-09-18", None, None, 0)
        self.assertEqual(candidates, [])
        self.assertEqual(skipped, 1)

    def test_same_meeting_seen_on_two_accounts_is_deduplicated_and_looked_up_once(self):
        damian = Account("Damian", "damian@x.pl", "acc-damian")
        piotr = Account("Piotr", "piotr@x.pl", "acc-piotr")
        settings = _settings([damian, piotr])
        shared_event = self._calendar_event("Spotkanie wspólne", "2026-09-18T08:00:00.0000000", "111111111")

        transport = RoutedTransport()
        transport.rule(lambda u: "/calendarView?" in u, _json_response({"value": [shared_event]}))
        self._stub_lookup_and_transcripts(transport, ["111111111"], damian.id)

        candidates, _skipped = meetings.resolve_by_date_title(_client(transport), settings, "2026-09-18", None, None, 0)
        self.assertEqual(len(candidates), 1)
        lookup_calls = [c for c in transport.calls if "'111111111'" in c]
        self.assertEqual(len(lookup_calls), 1)


class GraphErrorMappingTests(unittest.TestCase):
    def test_transcript_access_disabled_maps_to_502(self):
        err = GraphError(403, "Forbidden", "access denied", inner_code="GraphAccessToTranscriptsDisabled")
        status, code, message = graph_error_response(err)
        self.assertEqual(status, 502)
        self.assertEqual(code, "transcript_access_disabled")
        self.assertIn("Teams Admin Center", message)

    def test_other_403_maps_to_graph_forbidden(self):
        err = GraphError(403, "AccessDenied", "nope")
        status, code, _message = graph_error_response(err)
        self.assertEqual(status, 502)
        self.assertEqual(code, "graph_forbidden")

    def test_404_maps_to_supplied_not_found_tuple(self):
        err = GraphError(404, "NotFound", "brak")
        status, code, message = graph_error_response(err, not_found=("meeting_not_found", "nie ma spotkania"))
        self.assertEqual(status, 404)
        self.assertEqual(code, "meeting_not_found")
        self.assertEqual(message, "nie ma spotkania")

    def test_timeout_or_network_failure_maps_to_graph_error(self):
        err = GraphTransportError("timed out after 30s")
        status, code, message = graph_error_response(err)
        self.assertEqual(status, 502)
        self.assertEqual(code, "graph_error")
        self.assertIn("timed out after 30s", message)


def _adhoc_item(
    transcript_id: str,
    call_id: str,
    created: str,
    ended: str,
    organizer_id: str | None = "16d86420-7e4e-49f1-818d-76e5d2a099d0",
) -> dict:
    item: dict = {
        "id": transcript_id,
        "meetingId": None,
        "callId": call_id,
        "contentCorrelationId": "7cc3ae2a-0000-0000-0000-000000000000",
        "transcriptContentUrl": "https://graph.microsoft.com/v1.0/users/x/adhocCalls/y/transcripts/z/content",
        "createdDateTime": created,
        "endDateTime": ended,
    }
    if organizer_id is not None:
        item["meetingOrganizer"] = {"user": {"id": organizer_id, "displayName": None, "tenantId": "tenant"}}
    return item


_RECAP_LINK = (
    "https://teams.microsoft.com/l/meetingrecap?"
    "driveId=b%21hz5Uabc&driveItemId=0124GBabc"
    "&sitePath=https%3A%2F%2Fdtcode342-my.sharepoint.com%2F%3Av%3A%2Fg%2Fpersonal%2Fabc"
    "&fileUrl=https%3A%2F%2Fdtcode342-my.sharepoint.com%2Fpersonal%2Fdamian_dziura_dtcode_pl"
    "%2FDocuments%2FNagrania%2FPo%C5%82%C4%85czenie+z+Piotr+Tu%C5%84ski-20260919_122000-Transkrypcja+spotkania.mp4%3Fweb%3D1"
    "&threadId=19%3A16d86420-7e4e-49f1-818d-76e5d2a099d0_28dea859-afcd-4aca-8376-6d457eb3273d%40unq.gbl.spaces"
    "&organizerId=16d86420-7e4e-49f1-818d-76e5d2a099d0"
    "&tenantId=bd513bba-9c10-4393-9616-a237c0ba7bf2"
    "&callId=a16d2948-e3f1-4e16-8dc1-eaf4edad4c14"
    "&threadType=OneOnOneChat&meetingType=Unknown&subType=RecapSharingLink_RecapCore&recapType=ODSPTranscript"
)


class ParseRecapLinkTests(unittest.TestCase):
    def test_full_recap_link_extracts_call_organizer_subject_and_time(self):
        query = meetings.parse_link(_RECAP_LINK)
        self.assertEqual(query.kind, "adhocCall")
        self.assertEqual(query.value, "a16d2948-e3f1-4e16-8dc1-eaf4edad4c14")
        self.assertEqual(query.organizer_id, "16d86420-7e4e-49f1-818d-76e5d2a099d0")
        self.assertEqual(query.subject, "Połączenie z Piotr Tuński")
        self.assertEqual(query.recorded_at_local, datetime(2026, 9, 19, 12, 20, 0))

    def test_recap_link_without_file_url_has_no_subject_or_time(self):
        link = "https://teams.microsoft.com/l/meetingrecap?callId=a16d2948-e3f1-4e16-8dc1-eaf4edad4c14&organizerId=16d86420-7e4e-49f1-818d-76e5d2a099d0"
        query = meetings.parse_link(link)
        self.assertEqual(query.kind, "adhocCall")
        self.assertEqual(query.value, "a16d2948-e3f1-4e16-8dc1-eaf4edad4c14")
        self.assertEqual(query.organizer_id, "16d86420-7e4e-49f1-818d-76e5d2a099d0")
        self.assertIsNone(query.subject)
        self.assertIsNone(query.recorded_at_local)

    def test_recap_link_without_call_id_raises_invalid_link_error(self):
        link = "https://teams.microsoft.com/l/meetingrecap?organizerId=16d86420-7e4e-49f1-818d-76e5d2a099d0"
        with self.assertRaises(meetings.InvalidLinkError):
            meetings.parse_link(link)

    def test_recap_link_with_malformed_call_id_raises_invalid_link_error(self):
        link = "https://teams.microsoft.com/l/meetingrecap?callId=nie-guid"
        with self.assertRaises(meetings.InvalidLinkError):
            meetings.parse_link(link)


class AdhocGetAllPathTests(unittest.TestCase):
    def test_path_with_window_matches_exact_string(self):
        path = meetings._adhoc_get_all_path(
            "acc-damian",
            datetime(2026, 9, 17, 22, tzinfo=timezone.utc),
            datetime(2026, 9, 18, 22, tzinfo=timezone.utc),
        )
        self.assertEqual(
            path,
            "/users/acc-damian/adhocCalls/getAllTranscripts("
            "userId='acc-damian',startDateTime=2026-09-17T22:00:00Z,endDateTime=2026-09-18T22:00:00Z)",
        )

    def test_path_without_window_lists_user_only(self):
        self.assertEqual(
            meetings._adhoc_get_all_path("acc-damian", None, None),
            "/users/acc-damian/adhocCalls/getAllTranscripts(userId='acc-damian')",
        )


class ResolveAdhocByLinkTests(unittest.TestCase):
    _CALL_ID = "a16d2948-e3f1-4e16-8dc1-eaf4edad4c14"
    _ORGANIZER_ID = "16d86420-7e4e-49f1-818d-76e5d2a099d0"

    def _settings(self) -> Settings:
        damian = Account("Damian", "damian@x.pl", "acc-damian")
        organizer = Account("Organizator", "org@x.pl", self._ORGANIZER_ID)
        return _settings([damian, organizer])

    def _link_query(self, **overrides) -> meetings.LinkQuery:
        params = {
            "organizer_id": self._ORGANIZER_ID,
            "subject": "Połączenie z Piotr Tuński",
            "recorded_at_local": None,
        }
        params.update(overrides)
        return meetings.LinkQuery("adhocCall", self._CALL_ID, **params)

    def test_organizer_account_is_asked_first(self):
        settings = self._settings()
        item = _adhoc_item("t1", self._CALL_ID, "2026-09-19T10:20:00Z", "2026-09-19T10:25:00Z", self._ORGANIZER_ID)
        transport = RoutedTransport()
        transport.rule(lambda u: "getAllTranscripts" in u, _json_response({"value": [item]}))

        candidate, accounts_tried = meetings.resolve_by_link(_client(transport), settings, self._link_query())

        self.assertEqual(candidate["kind"], "adhocCall")
        self.assertEqual(candidate["callId"], self._CALL_ID)
        self.assertEqual(candidate["account"]["id"], self._ORGANIZER_ID)
        self.assertEqual(candidate["subject"], "Połączenie z Piotr Tuński")
        self.assertIn(self._ORGANIZER_ID, transport.calls[0])
        self.assertEqual(accounts_tried, 1)

    def test_filters_by_call_id_when_response_lists_several_calls(self):
        settings = self._settings()
        other = _adhoc_item("t-other", "11111111-2222-3333-4444-555555555555", "2026-09-19T10:20:00Z", "2026-09-19T10:25:00Z")
        wanted = _adhoc_item("t-wanted", self._CALL_ID, "2026-09-19T11:20:00Z", "2026-09-19T11:25:00Z")
        transport = RoutedTransport()
        transport.rule(lambda u: "getAllTranscripts" in u, _json_response({"value": [other, wanted]}))

        candidate, _ = meetings.resolve_by_link(
            _client(transport), settings, self._link_query(organizer_id=None)
        )

        self.assertEqual(candidate["callId"], self._CALL_ID)
        self.assertEqual(candidate["transcripts"], [
            {"id": "t-wanted", "createdDateTime": "2026-09-19T11:20:00Z", "endDateTime": "2026-09-19T11:25:00Z"}
        ])

    def test_follows_odata_next_link(self):
        settings = self._settings()
        next_url = "https://graph.microsoft.com/v1.0/users/x/adhocCalls/getAllTranscripts?$skip=1"
        wanted = _adhoc_item("t-wanted", self._CALL_ID, "2026-09-19T11:20:00Z", "2026-09-19T11:25:00Z")
        transport = RoutedTransport()
        transport.rule(
            lambda u: "getAllTranscripts" in u and "$skip" not in u,
            _json_response({"value": [], "@odata.nextLink": next_url}),
        )
        transport.rule(lambda u: u == next_url, _json_response({"value": [wanted]}))

        candidate, _ = meetings.resolve_by_link(
            _client(transport), settings, self._link_query(organizer_id=None)
        )

        self.assertEqual(candidate["transcripts"][0]["id"], "t-wanted")

    def test_recorded_time_selects_plus_minus_one_day_window(self):
        settings = self._settings()
        transport = RoutedTransport()
        transport.rule(lambda u: "getAllTranscripts" in u, _json_response({"value": []}))

        with self.assertRaises(meetings.MeetingNotFoundError):
            meetings.resolve_by_link(
                _client(transport),
                settings,
                self._link_query(recorded_at_local=datetime(2026, 9, 19, 12, 20, 0)),
            )

        # 2026-09-19 12:20 w Europe/Warsaw (CEST) = 10:20 UTC; okno ±1 dzień.
        self.assertIn("startDateTime=2026-09-18T10:20:00Z", transport.calls[0])
        self.assertIn("endDateTime=2026-09-20T10:20:00Z", transport.calls[0])

    def test_no_hit_on_any_account_raises_meeting_not_found(self):
        settings = self._settings()
        transport = RoutedTransport()
        transport.rule(lambda u: "getAllTranscripts" in u, _json_response({"value": []}))

        with self.assertRaises(meetings.MeetingNotFoundError) as ctx:
            meetings.resolve_by_link(_client(transport), settings, self._link_query())

        message = str(ctx.exception)
        self.assertIn(self._CALL_ID, message)
        self.assertIn("CallTranscripts.Read.All", message)
        self.assertIn("Damian", message)

    def test_graph_400_on_first_account_falls_through_to_next_account(self):
        settings = self._settings()
        wanted = _adhoc_item("t-wanted", self._CALL_ID, "2026-09-19T11:20:00Z", "2026-09-19T11:25:00Z")
        transport = RoutedTransport()
        transport.rule(
            lambda u: "getAllTranscripts" in u and "acc-damian" in u,
            _error_response(400, "BadRequest", "nieprawidłowe zapytanie"),
        )
        transport.rule(
            lambda u: "getAllTranscripts" in u and self._ORGANIZER_ID in u,
            _json_response({"value": [wanted]}),
        )

        candidate, accounts_tried = meetings.resolve_by_link(
            _client(transport), settings, self._link_query(organizer_id=None)
        )

        self.assertEqual(accounts_tried, 2)
        self.assertEqual(candidate["account"]["id"], self._ORGANIZER_ID)


class ResolveByDateTitleAdhocTests(unittest.TestCase):
    def _settings(self) -> Settings:
        return _settings([Account("Damian", "damian@x.pl", "acc-damian")])

    def _calendar_event(self, subject: str, start_iso: str, meet_id: str) -> dict:
        return {
            "subject": subject,
            "start": {"dateTime": start_iso, "timeZone": "UTC"},
            "end": {"dateTime": start_iso, "timeZone": "UTC"},
            "organizer": {"emailAddress": {"name": "Ktoś Tam", "address": "ktos@x.pl"}},
            "isOnlineMeeting": True,
            "onlineMeeting": {"joinUrl": f"https://teams.microsoft.com/meet/{meet_id}"},
            "body": {"content": ""},
        }

    def _transport_with(self, events: list[dict], adhoc: list[dict]) -> RoutedTransport:
        meeting = _online_meeting("meeting-111", "111111111", "https://x", organizer_id="nobody")
        transport = RoutedTransport()
        transport.rule(lambda u: "/calendarView?" in u, _json_response({"value": events}))
        transport.rule(lambda u: "getAllTranscripts" in u, _json_response({"value": adhoc}))
        transport.rule(lambda u: "'111111111'" in u, _json_response({"value": [meeting]}))
        transport.rule(lambda u: u.endswith("/transcripts"), _json_response({"value": []}))
        return transport

    def test_date_returns_calendar_and_adhoc_candidates_sorted_descending(self):
        settings = self._settings()
        events = [self._calendar_event("Spotkanie planowane", "2026-09-18T08:00:00.0000000", "111111111")]
        adhoc = [
            _adhoc_item("t-adhoc", "a16d2948-e3f1-4e16-8dc1-eaf4edad4c14", "2026-09-18T12:00:00Z", "2026-09-18T12:05:00Z")
        ]
        transport = self._transport_with(events, adhoc)

        candidates, _skipped = meetings.resolve_by_date_title(
            _client(transport), settings, "2026-09-18", None, None, 0
        )

        self.assertEqual(len(candidates), 2)
        self.assertEqual(candidates[0]["kind"], "adhocCall")
        self.assertEqual(candidates[1]["kind"], "onlineMeeting")
        self.assertGreater(candidates[0]["start"], candidates[1]["start"])
        self.assertIsNone(candidates[0]["subject"])

    def test_title_filters_adhoc_candidates_out(self):
        settings = self._settings()
        events = [self._calendar_event("Status projektu", "2026-09-18T08:00:00.0000000", "111111111")]
        adhoc = [
            _adhoc_item("t-adhoc", "a16d2948-e3f1-4e16-8dc1-eaf4edad4c14", "2026-09-18T12:00:00Z", "2026-09-18T12:05:00Z")
        ]
        transport = self._transport_with(events, adhoc)

        candidates, _skipped = meetings.resolve_by_date_title(
            _client(transport), settings, "2026-09-18", None, "status projektu", 0
        )

        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0]["kind"], "onlineMeeting")

    def test_title_only_mode_never_calls_get_all_transcripts(self):
        settings = self._settings()
        events = [self._calendar_event("Status projektu", "2026-09-18T08:00:00.0000000", "111111111")]
        transport = self._transport_with(events, [])

        candidates, _skipped = meetings.resolve_by_date_title(
            _client(transport), settings, None, None, "status projektu", 0
        )

        self.assertEqual(len(candidates), 1)
        self.assertFalse(any("getAllTranscripts" in url for url in transport.calls))

    def test_same_call_id_from_two_accounts_is_deduplicated(self):
        damian = Account("Damian", "damian@x.pl", "acc-damian")
        piotr = Account("Piotr", "piotr@x.pl", "acc-piotr")
        settings = _settings([damian, piotr])
        item = _adhoc_item("t-adhoc", "a16d2948-e3f1-4e16-8dc1-eaf4edad4c14", "2026-09-18T12:00:00Z", "2026-09-18T12:05:00Z")
        transport = RoutedTransport()
        transport.rule(lambda u: "/calendarView?" in u, _json_response({"value": []}))
        transport.rule(lambda u: "getAllTranscripts" in u, _json_response({"value": [item]}))

        candidates, _skipped = meetings.resolve_by_date_title(
            _client(transport), settings, "2026-09-18", None, None, 0
        )

        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0]["account"]["id"], "acc-damian")


_VTT_ADHOC = (
    "WEBVTT\n"
    "\n"
    "00:00:07.153 --> 00:00:08.593\n"
    "<v Damian Dziura>Cześć, słyszymy się?</v>\n"
)

_METADATA_ADHOC = (
    "WEBVTT\n"
    "\n"
    "00:00:07.153 --> 00:00:08.593\n"
    '{"speakerName": "Damian Dziura", "spokenText": "Cześć.", '
    '"spokenLanguage": "pl-pl", "startDateTime": "2026-09-18T09:36:35.0000000Z", '
    '"endDateTime": "2026-09-18T09:36:36.0000000Z"}\n'
)


class FetchAdhocTranscriptTests(unittest.TestCase):
    _CALL_ID = "a16d2948-e3f1-4e16-8dc1-eaf4edad4c14"
    _ACCOUNT_ID = "16d86420-7e4e-49f1-818d-76e5d2a099d0"

    def _settings(self) -> Settings:
        return _settings([Account("Damian", "damian@x.pl", self._ACCOUNT_ID)])

    def _transport(self, adhoc: list[dict], metadata_ok: bool = True) -> RoutedTransport:
        transport = RoutedTransport()
        transport.rule(lambda u: "getAllTranscripts" in u, _json_response({"value": adhoc}))
        transport.rule(
            lambda u: "/transcripts/" in u and u.endswith("/content?$format=text/vtt"),
            (200, _VTT_ADHOC.encode("utf-8"), {"Content-Type": "text/vtt"}),
        )
        if metadata_ok:
            transport.rule(
                lambda u: u.endswith("/metadataContent"),
                (200, _METADATA_ADHOC.encode("utf-8"), {"Content-Type": "text/vtt"}),
            )
        else:
            transport.rule(
                lambda u: u.endswith("/metadataContent"),
                _error_response(500, "InternalError", "brak metadanych"),
            )
        transport.rule(
            lambda u: f"/adhocCalls/{self._CALL_ID}/transcripts/" in u,
            _json_response({
                "id": "t-meta",
                "callId": self._CALL_ID,
                "createdDateTime": "2026-09-18T12:00:00Z",
                "endDateTime": "2026-09-18T12:05:00Z",
                "meetingOrganizer": {"user": {"id": self._ACCOUNT_ID}},
            }),
        )
        return transport

    def test_without_transcript_id_selects_newest(self):
        settings = self._settings()
        adhoc = [
            _adhoc_item("t-old", self._CALL_ID, "2026-09-18T12:00:00Z", "2026-09-18T12:01:00Z"),
            _adhoc_item("t-new", self._CALL_ID, "2026-09-18T12:03:00Z", "2026-09-18T12:05:00Z"),
        ]
        result = meetings.fetch_adhoc_transcript(
            _client(self._transport(adhoc)), settings, self._ACCOUNT_ID, self._CALL_ID, None
        )

        self.assertEqual(result["transcript"]["id"], "t-new")
        self.assertEqual(result["meeting"]["kind"], "adhocCall")
        self.assertEqual(result["meeting"]["callId"], self._CALL_ID)
        self.assertIsNone(result["meeting"]["meetingId"])
        self.assertIsNone(result["meeting"]["subject"])
        self.assertEqual(result["transcript"]["language"], "pl-pl")
        self.assertEqual(result["transcript"]["speakers"], ["Damian Dziura"])

    def test_with_transcript_id_uses_metadata_endpoint(self):
        settings = self._settings()
        transport = self._transport([])
        result = meetings.fetch_adhoc_transcript(
            _client(transport), settings, self._ACCOUNT_ID, self._CALL_ID, "t-meta"
        )

        self.assertEqual(result["transcript"]["id"], "t-meta")
        self.assertEqual(result["meeting"]["start"], "2026-09-18T12:00:00Z")
        self.assertEqual(result["meeting"]["end"], "2026-09-18T12:05:00Z")
        self.assertEqual(result["meeting"]["organizerId"], self._ACCOUNT_ID)
        self.assertTrue(any(url.endswith("/transcripts/t-meta") for url in transport.calls))

    def test_metadata_content_error_means_language_none(self):
        settings = self._settings()
        adhoc = [_adhoc_item("t-new", self._CALL_ID, "2026-09-18T12:03:00Z", "2026-09-18T12:05:00Z")]
        result = meetings.fetch_adhoc_transcript(
            _client(self._transport(adhoc, metadata_ok=False)), settings, self._ACCOUNT_ID, self._CALL_ID, None
        )

        self.assertIsNone(result["transcript"]["language"])
        self.assertEqual(result["transcript"]["speakers"], ["Damian Dziura"])

    def test_missing_transcripts_raise_transcript_not_found(self):
        settings = self._settings()
        with self.assertRaises(meetings.TranscriptNotFoundError):
            meetings.fetch_adhoc_transcript(
                _client(self._transport([])), settings, self._ACCOUNT_ID, self._CALL_ID, None
            )

    def test_unknown_account_raises_unknown_account_error(self):
        settings = self._settings()
        with self.assertRaises(meetings.UnknownAccountError):
            meetings.fetch_adhoc_transcript(
                _client(self._transport([])), settings, "nieznane-konto", self._CALL_ID, None
            )


if __name__ == "__main__":
    unittest.main()
