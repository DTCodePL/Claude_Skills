"""Klient Microsoft Graph: token (msal + certyfikat), GET z obsługą błędów."""

from __future__ import annotations

import base64
import hashlib
import http.client
import json
import socket
import urllib.parse
from typing import Callable

from config import Settings

GRAPH_BASE = "https://graph.microsoft.com/v1.0"
_CONNECT_TIMEOUT_SECONDS = 5
_TIMEOUT_SECONDS = 30

Transport = Callable[[str, dict[str, str]], tuple[int, bytes, dict[str, str]]]
TokenProvider = Callable[[], str]


class GraphError(Exception):
    """Błąd zwrócony przez Microsoft Graph (albo błąd transportu bez odpowiedzi HTTP)."""

    def __init__(
        self,
        status: int,
        code: str | None,
        message: str,
        inner_code: str | None = None,
        request_id: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message
        self.inner_code = inner_code
        self.request_id = request_id


class GraphTransportError(GraphError):
    """Błąd sieci / timeout — brak odpowiedzi HTTP od Graph."""

    def __init__(self, message: str) -> None:
        super().__init__(status=0, code=None, message=message)


def compute_thumbprint(cert_pem: str) -> str:
    """SHA1 (hex, wielkie litery) z DER-a wyciągniętego z PEM-owego certyfikatu."""

    lines = [line.strip() for line in cert_pem.strip().splitlines()]
    body = "".join(line for line in lines if line and not line.startswith("-----"))
    der = base64.b64decode(body)
    return hashlib.sha1(der).hexdigest().upper()


def _header(headers: dict[str, str], name: str) -> str | None:
    lowered = name.lower()
    for key, value in headers.items():
        if key.lower() == lowered:
            return value
    return None


def _parse_error(status: int, body: bytes) -> GraphError:
    text = body.decode("utf-8", errors="replace") if body else ""
    code = None
    message = text
    inner_code = None
    request_id = None
    try:
        data = json.loads(text) if text else {}
        error = data.get("error", {}) if isinstance(data, dict) else {}
        code = error.get("code")
        message = error.get("message") or text
        inner = error.get("innerError") or {}
        inner_code = inner.get("code")
        request_id = inner.get("request-id") or inner.get("client-request-id")
    except (json.JSONDecodeError, AttributeError):
        pass
    return GraphError(status=status, code=code, message=message, inner_code=inner_code, request_id=request_id)


class GraphClient:
    """Cienki klient Graph — testowalny przez wstrzyknięty transport i dostawcę tokenu."""

    def __init__(self, transport: Transport, token_provider: TokenProvider) -> None:
        self._transport = transport
        self._token_provider = token_provider

    def get(self, path: str, *, raw: bool = False) -> tuple[dict | str, dict[str, str]]:
        """GET na Graph. `path` może być pełnym URL-em (np. @odata.nextLink) albo ścieżką od GRAPH_BASE."""

        url = path if path.startswith("http://") or path.startswith("https://") else f"{GRAPH_BASE}{path}"
        token = self._token_provider()
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        try:
            status, body, response_headers = self._transport(url, headers)
        except GraphError:
            raise
        except Exception as exc:  # sieć/timeout z transportu
            raise GraphTransportError(str(exc)) from exc
        if status >= 400:
            raise _parse_error(status, body)
        if raw:
            return body.decode("utf-8", errors="replace"), response_headers
        if not body:
            return {}, response_headers
        return json.loads(body.decode("utf-8")), response_headers


def graph_error_response(err: GraphError, not_found: tuple[str, str] | None = None) -> tuple[int, str, str]:
    """Mapuje GraphError na (status HTTP, kod błędu API, komunikat po polsku)."""

    if err.status == 404 and not_found is not None:
        code, message = not_found
        return 404, code, message
    if err.status == 403 and err.inner_code == "GraphAccessToTranscriptsDisabled":
        return (
            502,
            "transcript_access_disabled",
            "Administrator wyłączył dostęp API do transkrypcji w Teams Admin Center",
        )
    if err.status in (401, 403):
        return 502, "graph_forbidden", f"Graph odrzucił żądanie ({err.code}): {err.message}"
    return 502, "graph_error", f"Błąd Graph ({err.code or 'network'}): {err.message}"


class _FastFailoverHTTPSConnection(http.client.HTTPSConnection):
    """HTTPSConnection z krótkim timeoutem *per adres IP* na `connect()`.

    Niektóre adresy z anycastowej puli `graph.microsoft.com` bywają z danego serwera
    nieosiągalne — `socket.create_connection()` (użyte przez `urllib.request.urlopen`)
    próbuje je po kolei, ale z timeoutem żądania (30 s) na KAŻDĄ próbę, więc jeden martwy
    adres blokuje cały request na 30 s zanim padnie failover na następny. Tu timeout na
    sam `connect()` jest krótki (5 s), a długi timeout (30 s) włącza się dopiero na odczyt,
    po udanym połączeniu.
    """

    def connect(self) -> None:
        last_error: Exception | None = None
        addresses = socket.getaddrinfo(self.host, self.port, socket.AF_INET, socket.SOCK_STREAM)
        for family, socktype, proto, _canonname, sockaddr in addresses:
            sock = socket.socket(family, socktype, proto)
            sock.settimeout(_CONNECT_TIMEOUT_SECONDS)
            try:
                sock.connect(sockaddr)
            except OSError as exc:
                last_error = exc
                sock.close()
                continue
            sock.settimeout(_TIMEOUT_SECONDS)
            self.sock = self._context.wrap_socket(sock, server_hostname=self.host)
            return
        raise OSError(f"brak osiągalnego adresu IP dla {self.host}:{self.port} ({last_error})")


def urllib_transport(url: str, headers: dict[str, str]) -> tuple[int, bytes, dict[str, str]]:
    """Produkcyjny transport: własne HTTPSConnection (patrz `_FastFailoverHTTPSConnection`),
    timeout na odczyt 30 s. `url` może być ścieżką od GRAPH_BASE albo pełnym URL-em Graph
    (np. `@odata.nextLink`) — host/ścieżka są zawsze brane z `url`, nigdy ze stałej
    `GRAPH_BASE`. Wstrzykiwany w app.main()."""

    parsed = urllib.parse.urlsplit(url)
    if parsed.hostname is None:
        raise GraphTransportError(f"niepoprawny URL Graph: {url!r}")
    path = parsed.path or "/"
    if parsed.query:
        path = f"{path}?{parsed.query}"

    connection = _FastFailoverHTTPSConnection(parsed.hostname, parsed.port or 443, timeout=_TIMEOUT_SECONDS)
    try:
        connection.request("GET", path, headers=headers)
        response = connection.getresponse()
        body = response.read()
        response_headers = dict(response.getheaders())
        return response.status, body, response_headers
    except (OSError, http.client.HTTPException) as exc:
        raise GraphTransportError(str(exc)) from exc
    finally:
        connection.close()


def build_token_provider(settings: Settings) -> TokenProvider:
    """Leniwie importuje `msal` przy pierwszym wywołaniu — nie jest wymagany do importu modułu."""

    state: dict[str, object] = {}

    def _get_app():
        if "app" not in state:
            import msal  # import leniwy — msal nie musi być zainstalowany lokalnie / w testach

            cert_pem = settings.cert_path.read_text(encoding="utf-8")
            key_pem = settings.key_path.read_text(encoding="utf-8")
            thumbprint = compute_thumbprint(cert_pem)
            state["app"] = msal.ConfidentialClientApplication(
                client_id=settings.client_id,
                authority=f"https://login.microsoftonline.com/{settings.tenant_id}",
                client_credential={
                    "private_key": key_pem,
                    "thumbprint": thumbprint,
                    "public_certificate": cert_pem,
                },
            )
        return state["app"]

    def provider() -> str:
        app = _get_app()
        result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
        if not result or "access_token" not in result:
            description = (result or {}).get("error_description") or (result or {}).get("error")
            raise RuntimeError(f"nie udało się uzyskać tokenu Graph: {description}")
        return result["access_token"]

    return provider
