"""Odczyt i walidacja konfiguracji serwisu ze zmiennych środowiskowych."""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import NoReturn
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


@dataclass(frozen=True)
class Account:
    """Konto Microsoft 365, w którego kontekście szukamy spotkań."""

    label: str
    upn: str
    id: str


@dataclass(frozen=True)
class Settings:
    """Zwalidowana konfiguracja serwisu."""

    tenant_id: str
    client_id: str
    cert_path: Path
    key_path: Path
    accounts: tuple[Account, ...]
    tokens: dict[str, str]
    port: int
    timezone: ZoneInfo
    timezone_name: str


def _fail(message: str) -> NoReturn:
    print(f"Błąd konfiguracji: {message}", file=sys.stderr)
    raise SystemExit(1)


def _require_env(source: dict[str, str], name: str) -> str:
    value = (source.get(name) or "").strip()
    if not value:
        _fail(f"brak wymaganej zmiennej środowiskowej {name}")
    return value


def _parse_accounts(raw: str) -> tuple[Account, ...]:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        _fail(f"BRIDGE_ACCOUNTS nie jest poprawnym JSON-em: {exc}")
    if not isinstance(data, list) or not data:
        _fail("BRIDGE_ACCOUNTS musi być niepustą listą obiektów {label, upn, id}")
    accounts: list[Account] = []
    for entry in data:
        if not isinstance(entry, dict) or not all(
            isinstance(entry.get(key), str) and entry.get(key) for key in ("label", "upn", "id")
        ):
            _fail("każdy wpis BRIDGE_ACCOUNTS musi zawierać niepuste pola label, upn, id")
        accounts.append(Account(label=entry["label"], upn=entry["upn"], id=entry["id"]))
    return tuple(accounts)


def _parse_tokens(raw: str) -> dict[str, str]:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        _fail(f"BRIDGE_TOKENS nie jest poprawnym JSON-em: {exc}")
    if not isinstance(data, dict) or not data:
        _fail("BRIDGE_TOKENS musi być niepustym obiektem token -> etykieta wołającego")
    tokens: dict[str, str] = {}
    for key, value in data.items():
        if not isinstance(key, str) or not key or not isinstance(value, str) or not value:
            _fail("BRIDGE_TOKENS musi mapować niepusty token na niepustą etykietę")
        tokens[key] = value
    return tokens


def _parse_port(raw: str) -> int:
    try:
        port = int(raw)
    except ValueError:
        _fail("BRIDGE_PORT musi być liczbą całkowitą")
    if port <= 0 or port > 65535:
        _fail("BRIDGE_PORT musi być z zakresu 1-65535")
    return port


def _parse_timezone(name: str) -> ZoneInfo:
    try:
        return ZoneInfo(name)
    except (ZoneInfoNotFoundError, ValueError) as exc:
        _fail(f"BRIDGE_TIMEZONE niepoprawna strefa czasowa ({name}): {exc}")


def load_settings(env: dict[str, str] | None = None) -> Settings:
    """Wczytuje i waliduje konfigurację. Przy błędzie kończy proces kodem 1."""

    source = env if env is not None else dict(os.environ)

    tenant_id = _require_env(source, "GRAPH_TENANT_ID")
    client_id = _require_env(source, "GRAPH_CLIENT_ID")
    cert_path = Path(source.get("GRAPH_CERT_PATH") or "/app/secrets/graph-cert.pem")
    key_path = Path(source.get("GRAPH_KEY_PATH") or "/app/secrets/graph-key.pem")

    accounts = _parse_accounts(_require_env(source, "BRIDGE_ACCOUNTS"))
    tokens = _parse_tokens(_require_env(source, "BRIDGE_TOKENS"))
    port = _parse_port(source.get("BRIDGE_PORT") or "8080")
    timezone_name = source.get("BRIDGE_TIMEZONE") or "Europe/Warsaw"
    timezone = _parse_timezone(timezone_name)

    return Settings(
        tenant_id=tenant_id,
        client_id=client_id,
        cert_path=cert_path,
        key_path=key_path,
        accounts=accounts,
        tokens=tokens,
        port=port,
        timezone=timezone,
        timezone_name=timezone_name,
    )
