import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from vtt import Segment, parse_vtt  # noqa: E402


class ParseVttTests(unittest.TestCase):
    def test_context_example_from_brief(self):
        text = (
            "WEBVTT\n"
            "\n"
            "00:00:07.153 --> 00:00:08.593\n"
            "<v Damian Dziura>To jest testowe spotkanie.</v>\n"
            "\n"
            "00:00:12.713 --> 00:00:20.033\n"
            "<v Damian Dziura>Chcę, żebyś utworzył notatki z tego spotkania.</v>\n"
        )
        segments = parse_vtt(text)
        self.assertEqual(
            segments,
            [
                Segment("00:00:07.153", "00:00:08.593", "Damian Dziura", "To jest testowe spotkanie."),
                Segment(
                    "00:00:12.713",
                    "00:00:20.033",
                    "Damian Dziura",
                    "Chcę, żebyś utworzył notatki z tego spotkania.",
                ),
            ],
        )

    def test_header_with_metadata_block_is_skipped(self):
        text = "WEBVTT\nKind: captions\nLanguage: pl\n\n00:00:01.000 --> 00:00:02.000\nHello\n"
        segments = parse_vtt(text)
        self.assertEqual(len(segments), 1)
        self.assertEqual(segments[0].text, "Hello")

    def test_cue_identifier_line_above_timing_is_ignored(self):
        text = "WEBVTT\n\n1\n00:00:01.000 --> 00:00:02.000\nHello world\n"
        segments = parse_vtt(text)
        self.assertEqual(len(segments), 1)
        self.assertEqual(segments[0].start, "00:00:01.000")
        self.assertEqual(segments[0].text, "Hello world")

    def test_mm_ss_timing_is_normalized_to_hh_mm_ss(self):
        text = "WEBVTT\n\n01:02.500 --> 01:05.000\nShort form\n"
        segments = parse_vtt(text)
        self.assertEqual(segments[0].start, "00:01:02.500")
        self.assertEqual(segments[0].end, "00:01:05.000")

    def test_timing_with_trailing_cue_settings_is_accepted(self):
        text = "WEBVTT\n\n00:00:01.000 --> 00:00:02.000 align:start position:0%\nHello\n"
        segments = parse_vtt(text)
        self.assertEqual(len(segments), 1)
        self.assertEqual(segments[0].text, "Hello")

    def test_multiline_cue_text_is_joined_with_space(self):
        text = "WEBVTT\n\n00:00:01.000 --> 00:00:02.000\nLine one\nLine two\n"
        segments = parse_vtt(text)
        self.assertEqual(segments[0].text, "Line one Line two")

    def test_cue_without_voice_tag_has_no_speaker(self):
        text = "WEBVTT\n\n00:00:01.000 --> 00:00:02.000\nNo speaker here\n"
        segments = parse_vtt(text)
        self.assertIsNone(segments[0].speaker)
        self.assertEqual(segments[0].text, "No speaker here")

    def test_voice_tag_missing_closing_tag_is_tolerated(self):
        text = "WEBVTT\n\n00:00:01.000 --> 00:00:02.000\n<v Jan Kowalski>tekst bez zamknięcia\n"
        segments = parse_vtt(text)
        self.assertEqual(segments[0].speaker, "Jan Kowalski")
        self.assertEqual(segments[0].text, "tekst bez zamknięcia")

    def test_other_tags_are_stripped(self):
        text = "WEBVTT\n\n00:00:01.000 --> 00:00:02.000\n<v Jan><c.colorCyan>Hello</c> world</v>\n"
        segments = parse_vtt(text)
        self.assertEqual(segments[0].speaker, "Jan")
        self.assertEqual(segments[0].text, "Hello world")

    def test_html_entities_are_unescaped(self):
        text = "WEBVTT\n\n00:00:01.000 --> 00:00:02.000\nTom &amp; Jerry\n"
        segments = parse_vtt(text)
        self.assertEqual(segments[0].text, "Tom & Jerry")

    def test_crlf_line_endings_are_handled(self):
        text = "WEBVTT\r\n\r\n00:00:01.000 --> 00:00:02.000\r\nHello\r\n"
        segments = parse_vtt(text)
        self.assertEqual(len(segments), 1)
        self.assertEqual(segments[0].text, "Hello")

    def test_empty_cue_is_skipped(self):
        text = "WEBVTT\n\n00:00:01.000 --> 00:00:02.000\n\n\n00:00:03.000 --> 00:00:04.000\nReal text\n"
        segments = parse_vtt(text)
        self.assertEqual(len(segments), 1)
        self.assertEqual(segments[0].text, "Real text")

    def test_speakers_are_unique_in_order_of_first_appearance(self):
        text = (
            "WEBVTT\n\n"
            "00:00:01.000 --> 00:00:02.000\n<v Anna>Cześć</v>\n\n"
            "00:00:03.000 --> 00:00:04.000\n<v Jan>Hej</v>\n\n"
            "00:00:05.000 --> 00:00:06.000\n<v Anna>Jeszcze raz</v>\n"
        )
        segments = parse_vtt(text)
        speakers = []
        for segment in segments:
            if segment.speaker and segment.speaker not in speakers:
                speakers.append(segment.speaker)
        self.assertEqual(speakers, ["Anna", "Jan"])


if __name__ == "__main__":
    unittest.main()
