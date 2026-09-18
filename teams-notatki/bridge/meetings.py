"""Logika domenowa: parsowanie linku, resolve po linku/dacie/tytule, pobranie transkrypcji."""

from __future__ import annotations

import html
import json
import re
import urllib.parse
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

from config import Account, Settings
from graph import GraphClient, GraphError
from vtt import parse_vtt

_MEET_ID_RE = re.compile(r"^\d{9,20}$")
_MEET_URL_RE = re.compile(r"teams\.microsoft\.com/meet/(\d{9,20})", re.IGNORECASE)
_MEETUP_JOIN_RE = re.compile(r"teams\.microsoft\.com/l/meetup-join/", re.IGNORECASE)
_MEET_LINK_IN_BODY_RE = re.compile(r"https://teams\.microsoft\.com/meet/(\d{9,20})", re.IGNORECASE)
_MEETUP_JOIN_LINK_IN_BODY_RE = re.compile(
    r"https://teams\.microsoft\.com/l/meetup-join/[^\s\"'<>]+", re.IGNORECASE
)
_ISO_RE = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2})T(?P<time>\d{2}:\d{2}:\d{2})(?P<frac>\.\d+)?(?P<tz>Z|[+-]\d{2}:\d{2})?$"
)
_POLISH_TRANSLATION = str.maketrans(
    {
        "ą": "a",
        "ć": "c",
        "ę": "e",
        "ł": "l",
        "ń": "n",
        "ó": "o",
        "ś": "s",
        "ź": "z",
        "ż": "z",
    }
)
_MAX_CANDIDATES = 10
_MAX_EVENTS = 200
_TITLE_FALLBACK_WINDOW_DAYS = 30


class InvalidLinkError(Exception):
    """Podana wartość `link` nie jest rozpoznawaną formą linku/identyfikatora Teams."""


class MeetingNotFoundError(Exception):
    """Spotkanie nie zostało znalezione w żadnym ze skonfigurowanych kont."""


class TranscriptNotFoundError(Exception):
    """Spotkanie istnieje, ale nie ma (jeszcze) transkrypcji."""


class UnknownAccountError(Exception):
    """`accountId` nie jest jednym ze skonfigurowanych BRIDGE_ACCOUNTS."""


@dataclass(frozen=True)
class LinkQuery:
    kind: str  # "joinMeetingId" | "joinWebUrl"
    value: str


# --------------------------------------------------------------------------------------
# Normalizacja tekstu / dat
# --------------------------------------------------------------------------------------


def normalize_pl(text: str) -> str:
    """Lowercase + usunięcie polskich znaków diakrytycznych, do dopasowania tytułu."""

    return text.lower().translate(_POLISH_TRANSLATION)


def parse_graph_datetime(value: str) -> datetime:
    """Parsuje datę zwróconą przez Graph (dowolna liczba cyfr ułamka sekundy, Z albo offset)."""

    match = _ISO_RE.match(value)
    if not match:
        raise ValueError(f"nieobsługiwany format daty Graph: {value}")
    frac = match.group("frac") or ""
    micro = (frac[1:7].ljust(6, "0"))[:6] if frac else "000000"
    tz = match.group("tz") or "Z"
    base = f"{match.group('date')}T{match.group('time')}.{micro}"
    naive = datetime.strptime(base, "%Y-%m-%dT%H:%M:%S.%f")
    if tz == "Z":
        dt = naive.replace(tzinfo=timezone.utc)
    else:
        sign = 1 if tz[0] == "+" else -1
        hours, minutes = tz[1:].split(":")
        offset = timedelta(hours=int(hours), minutes=int(minutes)) * sign
        dt = naive.replace(tzinfo=timezone(offset))
    return dt.astimezone(timezone.utc)


def format_utc(value: str) -> str:
    """Normalizuje datę Graph do UTC ISO-8601 z `Z`, bez ułamków sekund."""

    dt = parse_graph_datetime(value).replace(microsecond=0)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def _event_datetime_utc(field: dict) -> datetime:
    value = field.get("dateTime", "")
    tz_name = field.get("timeZone") or "UTC"
    if tz_name.upper() == "UTC":
        if not value.endswith("Z") and "+" not in value:
            value = f"{value}Z"
        return parse_graph_datetime(value)
    naive = datetime.strptime(value[:19], "%Y-%m-%dT%H:%M:%S")
    localized = naive.replace(tzinfo=ZoneInfo(tz_name))
    return localized.astimezone(timezone.utc)


# --------------------------------------------------------------------------------------
# Parsowanie / normalizacja linku
# --------------------------------------------------------------------------------------


def _encode_meetup_join_url(raw: str) -> str:
    """Normalizuje link meetup-join do postaci zakodowanej tak, jak zwraca ją Graph
    (`19:meeting_...@thread.v2` -> `19%3ameeting_...%40thread.v2`,
    `context={...}` -> `context=%7b%22...%22%7d`)."""

    text = html.unescape(raw)
    if "%3a" in text.lower() or "%40" in text.lower():
        text = urllib.parse.unquote(text)

    if "?" in text:
        base, _, query = text.partition("?")
    else:
        base, query = text, ""

    # Koduj ':' i '@' tylko w segmencie identyfikatora spotkania (po "meetup-join/"),
    # nigdy w schemacie/hoście — inaczej "https://" straciłoby swoje ':'.
    marker = "meetup-join/"
    marker_index = base.lower().find(marker)
    if marker_index != -1:
        split_at = marker_index + len(marker)
        prefix, remainder = base[:split_at], base[split_at:]
        base = prefix + remainder.replace(":", "%3a").replace("@", "%40")

    if not query:
        return base

    encoded_params = []
    for param in query.split("&"):
        if "=" not in param:
            encoded_params.append(param)
            continue
        key, _, value = param.partition("=")
        if key == "context":
            value = (
                value.replace("{", "%7b")
                .replace("}", "%7d")
                .replace('"', "%22")
                .replace(":", "%3a")
                .replace(",", "%2c")
            )
        encoded_params.append(f"{key}={value}")
    return f"{base}?{'&'.join(encoded_params)}"


def parse_link(link: str) -> LinkQuery:
    """Rozpoznaje formę linku/identyfikatora Teams. Rzuca InvalidLinkError, gdy nierozpoznana."""

    candidate = link.strip()
    digits_only = candidate.replace(" ", "")
    if _MEET_ID_RE.match(digits_only):
        return LinkQuery("joinMeetingId", digits_only)

    match = _MEET_URL_RE.search(candidate)
    if match:
        return LinkQuery("joinMeetingId", match.group(1))

    if _MEETUP_JOIN_RE.search(candidate):
        return LinkQuery("joinWebUrl", _encode_meetup_join_url(candidate))

    raise InvalidLinkError(f"nierozpoznana forma linku/identyfikatora: {candidate!r}")


def _link_query_from_event(event: dict) -> LinkQuery | None:
    online_meeting = event.get("onlineMeeting")
    if online_meeting and online_meeting.get("joinUrl"):
        try:
            return parse_link(online_meeting["joinUrl"])
        except InvalidLinkError:
            pass

    body = (event.get("body") or {}).get("content") or ""
    unescaped = html.unescape(body)
    match = _MEET_LINK_IN_BODY_RE.search(unescaped)
    if match:
        return LinkQuery("joinMeetingId", match.group(1))
    match = _MEETUP_JOIN_LINK_IN_BODY_RE.search(unescaped)
    if match:
        return LinkQuery("joinWebUrl", _encode_meetup_join_url(match.group(0)))
    return None


# --------------------------------------------------------------------------------------
# Wspólne pomocnicze wywołania Graph
# --------------------------------------------------------------------------------------


def _account_by_id(settings: Settings, account_id: str | None) -> Account | None:
    if not account_id:
        return None
    for account in settings.accounts:
        if account.id == account_id:
            return account
    return None


def _extract_meeting_fields(meeting: dict) -> dict:
    return {
        "meetingId": meeting["id"],
        "subject": meeting.get("subject"),
        "start": format_utc(meeting["startDateTime"]),
        "end": format_utc(meeting["endDateTime"]),
        "joinMeetingId": (meeting.get("joinMeetingIdSettings") or {}).get("joinMeetingId"),
        "joinWebUrl": meeting.get("joinWebUrl"),
        "organizerId": (
            ((meeting.get("participants") or {}).get("organizer") or {}).get("identity", {}).get("user", {}).get("id")
        ),
    }


def _fetch_transcripts_summary(client: GraphClient, account_id: str, meeting_id: str) -> list[dict]:
    data, _ = client.get(f"/users/{account_id}/onlineMeetings/{meeting_id}/transcripts")
    items = data.get("value", []) if isinstance(data, dict) else []
    return [
        {
            "id": item["id"],
            "createdDateTime": format_utc(item["createdDateTime"]),
            "endDateTime": format_utc(item["endDateTime"]),
        }
        for item in items
    ]


def _meeting_not_found_message(accounts: list[Account]) -> str:
    labels = ", ".join(account.label for account in accounts) if accounts else "skonfigurowanych kont"
    return (
        f"Spotkanie nie jest widoczne z żadnego ze skonfigurowanych kont ({labels}) "
        "— prawdopodobnie znajduje się w innym tenancie. Transkrypcję można podać ręcznie jako plik .vtt."
    )


def _lookup_online_meeting(
    client: GraphClient, ordered_accounts: list[Account], link_query: LinkQuery
) -> tuple[dict, Account, int]:
    filter_field = "joinMeetingIdSettings/joinMeetingId" if link_query.kind == "joinMeetingId" else "JoinWebUrl"
    filter_expr = f"{filter_field} eq '{link_query.value}'"
    encoded_filter = urllib.parse.quote(filter_expr, safe="'")

    accounts_tried = 0
    for account in ordered_accounts:
        accounts_tried += 1
        try:
            data, _ = client.get(f"/users/{account.id}/onlineMeetings?$filter={encoded_filter}")
        except GraphError as exc:
            if exc.status == 400:
                # Graph odpowiada 400 ("1025: An error has occurred.") dla joinMeetingId/joinWebUrl,
                # które po prostu nie istnieje — to nie błąd serwera, tylko "brak trafienia w tym
                # koncie", identycznie jak {"value": []}. Każdy inny status (403/404/5xx/sieć)
                # propagujemy dalej — to prawdziwy błąd Graph, nie brak wyniku.
                continue
            raise
        values = data.get("value", []) if isinstance(data, dict) else []
        if values:
            return values[0], account, accounts_tried
    raise MeetingNotFoundError(_meeting_not_found_message(ordered_accounts))


# --------------------------------------------------------------------------------------
# Resolve po linku
# --------------------------------------------------------------------------------------


def resolve_by_link(client: GraphClient, settings: Settings, link_query: LinkQuery) -> tuple[dict, int]:
    meeting, account, accounts_tried = _lookup_online_meeting(client, list(settings.accounts), link_query)
    fields = _extract_meeting_fields(meeting)
    organizer_id = fields.pop("organizerId")

    organizer = {"name": None, "email": None}
    matched = _account_by_id(settings, organizer_id)
    if matched is not None:
        organizer = {"name": matched.label, "email": matched.upn}

    transcripts = _fetch_transcripts_summary(client, account.id, fields["meetingId"])

    candidate = {
        "meetingId": fields["meetingId"],
        "account": {"label": account.label, "upn": account.upn, "id": account.id},
        "subject": fields["subject"],
        "start": fields["start"],
        "end": fields["end"],
        "organizer": organizer,
        "organizerId": organizer_id,
        "joinMeetingId": fields["joinMeetingId"],
        "joinWebUrl": fields["joinWebUrl"],
        "transcripts": transcripts,
    }
    return candidate, accounts_tried


# --------------------------------------------------------------------------------------
# Resolve po dacie / tytule
# --------------------------------------------------------------------------------------


def _resolve_query_window(date_str: str | None, window_days: int, tz: ZoneInfo) -> tuple[datetime, datetime]:
    if date_str is not None:
        day = date.fromisoformat(date_str)
        start_local = datetime.combine(day - timedelta(days=window_days), time.min, tzinfo=tz)
        end_local = datetime.combine(day + timedelta(days=window_days + 1), time.min, tzinfo=tz)
        return start_local.astimezone(timezone.utc), end_local.astimezone(timezone.utc)
    end_utc = datetime.now(timezone.utc)
    start_utc = end_utc - timedelta(days=_TITLE_FALLBACK_WINDOW_DAYS)
    return start_utc, end_utc


def _within_time_window(event_start_utc: datetime, date_str: str, time_str: str, tz: ZoneInfo) -> bool:
    target_local = datetime.combine(date.fromisoformat(date_str), datetime.strptime(time_str, "%H:%M").time(), tzinfo=tz)
    target_utc = target_local.astimezone(timezone.utc)
    return abs((event_start_utc - target_utc).total_seconds()) <= 90 * 60


def _fetch_calendar_view(client: GraphClient, account: Account, start_utc: datetime, end_utc: datetime) -> list[dict]:
    query = urllib.parse.urlencode(
        {
            "startDateTime": start_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "endDateTime": end_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "$top": "50",
            "$orderby": "start/dateTime desc",
            "$select": "subject,start,end,organizer,isOnlineMeeting,onlineMeeting,body",
        },
        quote_via=urllib.parse.quote,
    )
    next_path: str | None = f"/users/{account.id}/calendarView?{query}"
    events: list[dict] = []
    while next_path and len(events) < _MAX_EVENTS:
        data, _ = client.get(next_path)
        events.extend(data.get("value", []) if isinstance(data, dict) else [])
        next_path = data.get("@odata.nextLink") if isinstance(data, dict) else None
    return events[:_MAX_EVENTS]


def resolve_by_date_title(
    client: GraphClient,
    settings: Settings,
    date_str: str | None,
    time_str: str | None,
    title: str | None,
    window_days: int,
) -> tuple[list[dict], int]:
    start_utc, end_utc = _resolve_query_window(date_str, window_days, settings.timezone)

    seen: set[tuple[str, str]] = set()
    collected: list[tuple[datetime, dict, Account, LinkQuery]] = []
    skipped = 0

    for account in settings.accounts:
        events = _fetch_calendar_view(client, account, start_utc, end_utc)
        for event in events:
            subject = event.get("subject") or ""
            if title and normalize_pl(title) not in normalize_pl(subject):
                continue

            event_start = _event_datetime_utc(event.get("start") or {})
            if date_str is not None and time_str and not _within_time_window(event_start, date_str, time_str, settings.timezone):
                continue

            link_query = _link_query_from_event(event)
            if link_query is None:
                skipped += 1
                continue

            key = (link_query.kind, link_query.value)
            if key in seen:
                continue
            seen.add(key)
            collected.append((event_start, event, account, link_query))

    collected.sort(key=lambda item: item[0], reverse=True)
    collected = collected[:_MAX_CANDIDATES]

    candidates: list[dict] = []
    for _event_start, event, found_in_account, link_query in collected:
        ordered_accounts = [found_in_account] + [a for a in settings.accounts if a.id != found_in_account.id]
        try:
            meeting, account, _accounts_tried = _lookup_online_meeting(client, ordered_accounts, link_query)
        except MeetingNotFoundError:
            skipped += 1
            continue

        fields = _extract_meeting_fields(meeting)
        organizer_field = (event.get("organizer") or {}).get("emailAddress") or {}
        organizer = {"name": organizer_field.get("name"), "email": organizer_field.get("address")}
        transcripts = _fetch_transcripts_summary(client, account.id, fields["meetingId"])

        candidates.append(
            {
                "meetingId": fields["meetingId"],
                "account": {"label": account.label, "upn": account.upn, "id": account.id},
                "subject": fields["subject"],
                "start": fields["start"],
                "end": fields["end"],
                "organizer": organizer,
                "joinMeetingId": fields["joinMeetingId"],
                "joinWebUrl": fields["joinWebUrl"],
                "transcripts": transcripts,
            }
        )

    return candidates, skipped


# --------------------------------------------------------------------------------------
# Transkrypcja pojedynczego spotkania
# --------------------------------------------------------------------------------------


def _extract_language(metadata_text: str) -> str | None:
    for segment in parse_vtt(metadata_text):
        try:
            payload = json.loads(segment.text)
        except (json.JSONDecodeError, TypeError):
            continue
        language = payload.get("spokenLanguage") if isinstance(payload, dict) else None
        if language:
            return language
    return None


def fetch_transcript(
    client: GraphClient,
    settings: Settings,
    account_id: str,
    meeting_id: str,
    transcript_id: str | None,
) -> dict:
    account = _account_by_id(settings, account_id)
    if account is None:
        raise UnknownAccountError(f"{account_id!r} nie jest jednym ze skonfigurowanych BRIDGE_ACCOUNTS")

    meeting, _ = client.get(f"/users/{account_id}/onlineMeetings/{meeting_id}")
    fields = _extract_meeting_fields(meeting)

    transcripts_data, _ = client.get(f"/users/{account_id}/onlineMeetings/{meeting_id}/transcripts")
    items = transcripts_data.get("value", []) if isinstance(transcripts_data, dict) else []
    if not items:
        raise TranscriptNotFoundError(
            "Spotkanie istnieje, ale nie ma transkrypcji — Teams udostępnia ją kilka minut po "
            "zakończeniu spotkania i tylko gdy transkrypcja była włączona"
        )

    if transcript_id is None:
        chosen = max(items, key=lambda item: parse_graph_datetime(item["createdDateTime"]))
    else:
        matching = [item for item in items if item["id"] == transcript_id]
        if not matching:
            raise TranscriptNotFoundError(f"nie znaleziono transkrypcji {transcript_id!r} dla tego spotkania")
        chosen = matching[0]

    transcript_id = chosen["id"]
    vtt_text, _ = client.get(
        f"/users/{account_id}/onlineMeetings/{meeting_id}/transcripts/{transcript_id}/content?$format=text/vtt",
        raw=True,
    )

    language: str | None = None
    try:
        metadata_text, _ = client.get(
            f"/users/{account_id}/onlineMeetings/{meeting_id}/transcripts/{transcript_id}/metadataContent",
            raw=True,
        )
        language = _extract_language(metadata_text)
    except GraphError:
        language = None

    segments = parse_vtt(vtt_text)
    speakers: list[str] = []
    for segment in segments:
        if segment.speaker and segment.speaker not in speakers:
            speakers.append(segment.speaker)

    return {
        "meeting": {
            "meetingId": fields["meetingId"],
            "subject": fields["subject"],
            "start": fields["start"],
            "end": fields["end"],
            "organizerId": fields["organizerId"],
            "joinMeetingId": fields["joinMeetingId"],
        },
        "transcript": {
            "id": transcript_id,
            "createdDateTime": format_utc(chosen["createdDateTime"]),
            "endDateTime": format_utc(chosen["endDateTime"]),
            "language": language,
            "speakers": speakers,
            "segments": [
                {"start": s.start, "end": s.end, "speaker": s.speaker, "text": s.text} for s in segments
            ],
            "vtt": vtt_text,
        },
    }
