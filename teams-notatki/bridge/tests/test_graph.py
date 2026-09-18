import socket
import sys
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1]))

import graph  # noqa: E402
from graph import GraphTransportError, _FastFailoverHTTPSConnection  # noqa: E402

_ADDRESSES = [
    (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("20.20.32.96", 443)),
    (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("20.20.32.97", 443)),
]


class _FakeSocket:
    """Atrapa gniazda: `connect()` rzuca TimeoutError natychmiast (bez realnego czekania)
    dla adresów oznaczonych jako martwe, przechodzi bez błędu dla żywych."""

    def __init__(self, should_fail: bool) -> None:
        self.should_fail = should_fail
        self.closed = False
        self.timeouts: list[float] = []

    def settimeout(self, value: float) -> None:
        self.timeouts.append(value)

    def connect(self, address) -> None:
        if self.should_fail:
            raise TimeoutError("timed out")

    def close(self) -> None:
        self.closed = True


def _connection_with_stub_tls(host: str = "graph.microsoft.com", port: int = 443) -> _FastFailoverHTTPSConnection:
    connection = _FastFailoverHTTPSConnection(host, port)
    # TLS nie jest tu przedmiotem testu (brief: "TLS w teście omiń") — zastępujemy _context
    # atrapą, żeby wrap_socket() był no-opem zwracającym to samo (fałszywe) gniazdo.
    connection._context = SimpleNamespace(wrap_socket=lambda sock, server_hostname: sock)
    return connection


class FastFailoverConnectTests(unittest.TestCase):
    def test_falls_over_to_second_address_without_waiting_30_seconds(self):
        fake_sockets = [_FakeSocket(should_fail=True), _FakeSocket(should_fail=False)]
        connection = _connection_with_stub_tls()

        with (
            patch("graph.socket.getaddrinfo", return_value=_ADDRESSES),
            patch("graph.socket.socket", side_effect=fake_sockets),
        ):
            started = time.monotonic()
            connection.connect()
            elapsed = time.monotonic() - started

        self.assertLess(elapsed, 1.0, "connect() nie powinien czekać na martwy adres")
        self.assertTrue(fake_sockets[0].closed, "gniazdo dla martwego adresu musi być zamknięte")
        self.assertIs(connection.sock, fake_sockets[1])
        self.assertIn(graph._CONNECT_TIMEOUT_SECONDS, fake_sockets[0].timeouts)
        self.assertIn(graph._TIMEOUT_SECONDS, fake_sockets[1].timeouts)

    def test_raises_os_error_when_every_address_fails(self):
        fake_sockets = [_FakeSocket(should_fail=True), _FakeSocket(should_fail=True)]
        connection = _connection_with_stub_tls()

        with (
            patch("graph.socket.getaddrinfo", return_value=_ADDRESSES),
            patch("graph.socket.socket", side_effect=fake_sockets),
        ):
            started = time.monotonic()
            with self.assertRaises(OSError):
                connection.connect()
            elapsed = time.monotonic() - started

        self.assertLess(elapsed, 1.0)
        self.assertTrue(all(sock.closed for sock in fake_sockets))


class UrllibTransportFailoverTests(unittest.TestCase):
    def test_exhausted_addresses_surface_as_graph_transport_error(self):
        fake_socket = _FakeSocket(should_fail=True)

        with (
            patch("graph.socket.getaddrinfo", return_value=[_ADDRESSES[0]]),
            patch("graph.socket.socket", return_value=fake_socket),
        ):
            started = time.monotonic()
            with self.assertRaises(GraphTransportError):
                graph.urllib_transport(
                    "https://graph.microsoft.com/v1.0/users/x/onlineMeetings",
                    {"Authorization": "Bearer test-token"},
                )
            elapsed = time.monotonic() - started

        self.assertLess(elapsed, 1.0)

    def test_invalid_url_without_host_raises_graph_transport_error(self):
        with self.assertRaises(GraphTransportError):
            graph.urllib_transport("not-a-url", {})


if __name__ == "__main__":
    unittest.main()
