"""Serwer HTTP (stdlib) serwisu teams-transcript-bridge: routing, auth, JSON, logowanie."""

from __future__ import annotations

import hmac
import json
import sys
import time
import urllib.parse
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from config import Settings, load_settings
from graph import GraphClient, GraphError, build_token_provider, graph_error_response, urllib_transport
from meetings import (
    InvalidLinkError,
    MeetingNotFoundError,
    TranscriptNotFoundError,
    UnknownAccountError,
    fetch_adhoc_transcript,
    fetch_transcript,
    parse_link,
    resolve_by_date_title,
    resolve_by_link,
)

_HEALTH_BODY = b'{"status":"ok","service":"teams-transcript-bridge"}'
_MAX_BODY_BYTES = 64 * 1024


class ApiError(Exception):
    """Błąd, który ma trafić do klienta jako {"error": {"code", "message"}}."""

    def __init__(self, status: int, code: str, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message


def _log_request(method: str, path: str, caller: str, status: int, elapsed_ms: int, mode: str, accounts_tried: object) -> None:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(
        f"{timestamp} INFO {method} {path} caller={caller} status={status} "
        f"ms={elapsed_ms} mode={mode} accounts_tried={accounts_tried}",
        flush=True,
    )


def build_handler(settings: Settings, client: GraphClient) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        server_version = "teams-transcript-bridge/1.0"

        def log_message(self, format: str, *args: object) -> None:  # noqa: A002
            return  # własne logowanie w _log_request, jedna linia na żądanie

        def _send_json(self, status: int, payload: dict) -> None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _send_error_json(self, status: int, code: str, message: str) -> None:
            self._send_json(status, {"error": {"code": code, "message": message}})

        def _send_raw(self, status: int, body: bytes, content_type: str) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _authenticate(self) -> str:
            header = self.headers.get("Authorization", "")
            if not header.startswith("Bearer "):
                raise ApiError(401, "unauthorized", "Brak lub niepoprawny nagłówek Authorization")
            token = header[len("Bearer ") :].strip()
            for known_token, caller in settings.tokens.items():
                if hmac.compare_digest(known_token, token):
                    return caller
            raise ApiError(401, "unauthorized", "Nieznany token")

        def _read_json_body(self) -> dict:
            length_header = self.headers.get("Content-Length")
            if length_header is None:
                raise ApiError(400, "bad_request", "Brak nagłówka Content-Length")
            try:
                length = int(length_header)
            except ValueError:
                raise ApiError(400, "bad_request", "Niepoprawny nagłówek Content-Length")
            if length > _MAX_BODY_BYTES:
                raise ApiError(413, "payload_too_large", "Ciało żądania przekracza limit 64 KiB")
            raw = self.rfile.read(length) if length else b""
            if not raw:
                return {}
            try:
                data = json.loads(raw.decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                raise ApiError(400, "bad_request", "Ciało żądania nie jest poprawnym JSON-em") from exc
            if not isinstance(data, dict):
                raise ApiError(400, "bad_request", "Ciało żądania musi być obiektem JSON")
            return data

        def do_GET(self) -> None:
            self._dispatch("GET")

        def do_POST(self) -> None:
            self._dispatch("POST")

        def do_PUT(self) -> None:
            self._dispatch("PUT")

        def do_DELETE(self) -> None:
            self._dispatch("DELETE")

        def do_PATCH(self) -> None:
            self._dispatch("PATCH")

        def do_HEAD(self) -> None:
            self._dispatch("HEAD")

        def do_OPTIONS(self) -> None:
            self._dispatch("OPTIONS")

        def _dispatch(self, method: str) -> None:
            start = time.monotonic()
            path, _, query_string = self.path.partition("?")
            segments = [s for s in path.split("/") if s]
            caller = "-"
            status = 500
            mode = "-"
            accounts_tried: object = "-"
            try:
                if path == "/health":
                    if method != "GET":
                        raise ApiError(405, "method_not_allowed", "Metoda niedozwolona")
                    self._send_raw(200, _HEALTH_BODY, "application/json")
                    status = 200
                    return

                caller = self._authenticate()

                if segments == ["meetings", "resolve"]:
                    if method != "POST":
                        raise ApiError(405, "method_not_allowed", "Metoda niedozwolona")
                    status, mode, accounts_tried = self._handle_resolve()
                    return

                if len(segments) == 4 and segments[0] == "meetings" and segments[3] == "transcript":
                    if method != "GET":
                        raise ApiError(405, "method_not_allowed", "Metoda niedozwolona")
                    status = self._handle_transcript(segments[1], segments[2], query_string)
                    return

                if len(segments) == 4 and segments[0] == "calls" and segments[3] == "transcript":
                    if method != "GET":
                        raise ApiError(405, "method_not_allowed", "Metoda niedozwolona")
                    status = self._handle_call_transcript(segments[1], segments[2], query_string)
                    return

                raise ApiError(404, "not_found", "Nieznana ścieżka")
            except ApiError as exc:
                status = exc.status
                self._send_error_json(exc.status, exc.code, exc.message)
            except Exception as exc:  # pragma: no cover - siatka bezpieczeństwa
                status = 500
                self._send_error_json(500, "internal_error", "Nieoczekiwany błąd serwera")
                print(f"UNHANDLED {exc!r}", file=sys.stderr)
            finally:
                elapsed_ms = int((time.monotonic() - start) * 1000)
                _log_request(method, path, caller, status, elapsed_ms, mode, accounts_tried)

        def _handle_resolve(self) -> tuple[int, str, object]:
            body = self._read_json_body()
            link = body.get("link")
            date_value = body.get("date")
            title = body.get("title")
            time_value = body.get("time")
            window_days = body.get("window_days", 0)

            if link is not None:
                if not isinstance(link, str) or not link.strip():
                    raise ApiError(400, "bad_request", "Pole link musi być niepustym tekstem")
                try:
                    link_query = parse_link(link)
                except InvalidLinkError:
                    raise ApiError(400, "invalid_link", "Nierozpoznany format linku/identyfikatora spotkania")
                try:
                    candidate, accounts_tried = resolve_by_link(client, settings, link_query)
                except MeetingNotFoundError as exc:
                    raise ApiError(404, "meeting_not_found", str(exc)) from exc
                except GraphError as exc:
                    status_code, code, message = graph_error_response(exc)
                    raise ApiError(status_code, code, message) from exc
                self._send_json(200, {"candidates": [candidate], "skipped_without_teams_link": 0})
                return 200, "link", accounts_tried

            if date_value is not None or title is not None:
                if date_value is not None and not isinstance(date_value, str):
                    raise ApiError(400, "bad_request", "Pole date musi być tekstem w formacie YYYY-MM-DD")
                if title is not None and not isinstance(title, str):
                    raise ApiError(400, "bad_request", "Pole title musi być tekstem")
                if time_value is not None and not isinstance(time_value, str):
                    raise ApiError(400, "bad_request", "Pole time musi być tekstem w formacie HH:MM")
                if not isinstance(window_days, int) or isinstance(window_days, bool):
                    raise ApiError(400, "bad_request", "Pole window_days musi być liczbą całkowitą")
                try:
                    candidates, skipped = resolve_by_date_title(
                        client, settings, date_value, time_value, title, window_days
                    )
                except GraphError as exc:
                    status_code, code, message = graph_error_response(exc)
                    raise ApiError(status_code, code, message) from exc
                self._send_json(200, {"candidates": candidates, "skipped_without_teams_link": skipped})
                return 200, "date_title", len(settings.accounts)

            raise ApiError(400, "bad_request", "Podaj pole link albo date/title")

        def _handle_transcript(self, account_id: str, meeting_id: str, query_string: str) -> int:
            return self._fetch_and_send_transcript(account_id, meeting_id, query_string, fetch_transcript)

        def _handle_call_transcript(self, account_id: str, call_id: str, query_string: str) -> int:
            return self._fetch_and_send_transcript(account_id, call_id, query_string, fetch_adhoc_transcript)

        def _fetch_and_send_transcript(self, account_id: str, object_id: str, query_string: str, fetch_fn) -> int:
            params = urllib.parse.parse_qs(query_string, keep_blank_values=True)
            transcript_id = params.get("transcriptId", [None])[0]
            fmt = params.get("format", [None])[0]

            try:
                result = fetch_fn(client, settings, account_id, object_id, transcript_id)
            except UnknownAccountError as exc:
                raise ApiError(400, "unknown_account", str(exc)) from exc
            except TranscriptNotFoundError as exc:
                raise ApiError(404, "transcript_not_found", str(exc)) from exc
            except MeetingNotFoundError as exc:
                raise ApiError(404, "meeting_not_found", str(exc)) from exc
            except GraphError as exc:
                not_found = ("meeting_not_found", "Nie znaleziono spotkania o podanym identyfikatorze")
                status_code, code, message = graph_error_response(exc, not_found=not_found)
                raise ApiError(status_code, code, message) from exc

            if fmt == "vtt":
                vtt_bytes = result["transcript"]["vtt"].encode("utf-8")
                self._send_raw(200, vtt_bytes, "text/vtt; charset=utf-8")
                return 200

            self._send_json(200, result)
            return 200

    return Handler


def main() -> None:
    settings = load_settings()
    token_provider = build_token_provider(settings)
    client = GraphClient(transport=urllib_transport, token_provider=token_provider)
    handler_cls = build_handler(settings, client)
    server = ThreadingHTTPServer(("0.0.0.0", settings.port), handler_cls)
    try:
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
