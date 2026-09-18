import json
import sys
import unittest
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


if __name__ == "__main__":
    unittest.main()
