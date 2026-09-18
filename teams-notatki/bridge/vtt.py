"""Parser WebVTT (transkrypcje Teams) → lista segmentów."""

from __future__ import annotations

import html
import re
from dataclasses import dataclass

_TIMING_RE = re.compile(
    r"^(?P<start>(?:\d{2}:)?\d{2}:\d{2}\.\d{3})\s*-->\s*(?P<end>(?:\d{2}:)?\d{2}:\d{2}\.\d{3})(?:\s+.*)?$"
)
_VOICE_RE = re.compile(r"<v([^>]*)>(.*?)(?:</v>|$)", re.IGNORECASE | re.DOTALL)
_TAG_RE = re.compile(r"</?[a-zA-Z][^>]*>")


@dataclass(frozen=True)
class Segment:
    start: str
    end: str
    speaker: str | None
    text: str


def parse_vtt(text: str) -> list[Segment]:
    """Parsuje treść WebVTT (nagłówek, cue z opcjonalnym id, wieloliniowy tekst, <v>)."""

    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = normalized.split("\n")

    index = 0
    if index < len(lines) and lines[index].strip().startswith("WEBVTT"):
        index += 1
        while index < len(lines) and lines[index].strip() != "":
            index += 1  # metadane nagłówka aż do pierwszej pustej linii

    segments: list[Segment] = []
    block: list[str] = []
    for line in lines[index:]:
        if line.strip() == "":
            if block:
                segment = _parse_block(block)
                if segment is not None:
                    segments.append(segment)
                block = []
            continue
        block.append(line)
    if block:
        segment = _parse_block(block)
        if segment is not None:
            segments.append(segment)

    return segments


def _parse_block(block_lines: list[str]) -> Segment | None:
    timing_index = None
    match = None
    for i, line in enumerate(block_lines):
        candidate = _TIMING_RE.match(line.strip())
        if candidate is not None:
            timing_index, match = i, candidate
            break
    if match is None or timing_index is None:
        return None  # blok bez linii timingu (np. tylko identyfikator) — pomijamy

    start = _normalize_timestamp(match.group("start"))
    end = _normalize_timestamp(match.group("end"))

    text_lines = block_lines[timing_index + 1 :]
    raw_text = " ".join(t.strip() for t in text_lines if t.strip() != "")
    if raw_text == "":
        return None

    speaker, content = _extract_voice(raw_text)
    content = _TAG_RE.sub("", content)
    content = html.unescape(content).strip()
    if content == "":
        return None

    return Segment(start=start, end=end, speaker=speaker, text=content)


def _extract_voice(raw_text: str) -> tuple[str | None, str]:
    match = _VOICE_RE.search(raw_text)
    if match is None:
        return None, raw_text
    speaker = match.group(1).strip() or None
    return speaker, match.group(2)


def _normalize_timestamp(value: str) -> str:
    parts = value.split(":")
    if len(parts) == 2:
        return f"00:{value}"
    return value
