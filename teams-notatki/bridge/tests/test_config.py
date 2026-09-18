import io
import json
import sys
import unittest
from contextlib import redirect_stderr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

import config  # noqa: E402
import graph  # noqa: E402

# Stały PEM testowy — treść nie jest prawdziwym certyfikatem X.509, tylko dowolnymi bajtami
# zakodowanymi w base64 pod nagłówkami PEM. compute_thumbprint() liczy SHA1 z bajtów po
# base64-dekodowaniu i nie waliduje struktury certyfikatu, więc to wystarcza do sprawdzenia
# strip nagłówków + b64 decode + sha1 upper.
_CERT_PEM = (
    "-----BEGIN CERTIFICATE-----\n"
    "WmVicmFuaSB0ZWFtcy10cmFuc2NyaXB0LWJyaWRnZSB0ZXN0IGNlcnRpZmljYXRl\n"
    "IGNvbnRlbnQgdXNlZCBvbmx5IHRvIGV4ZXJjaXNlIFNIQTEgdGh1bWJwcmludCBj\n"
    "b21wdXRhdGlvbiBpbiB1bml0IHRlc3RzLg==\n"
    "-----END CERTIFICATE-----\n"
)
_EXPECTED_THUMBPRINT = "066E1B8BDCA27DB53572706CF566C9E9D41E23DC"


def _base_env() -> dict[str, str]:
    return {
        "GRAPH_TENANT_ID": "11111111-1111-1111-1111-111111111111",
        "GRAPH_CLIENT_ID": "22222222-2222-2222-2222-222222222222",
        "BRIDGE_ACCOUNTS": json.dumps(
            [
                {
                    "label": "Damian",
                    "upn": "Damian.Dziura@DTCode.pl",
                    "id": "33333333-3333-3333-3333-333333333333",
                }
            ]
        ),
        "BRIDGE_TOKENS": json.dumps({"aaaabbbbccccdddd": "damian"}),
    }


class LoadSettingsTests(unittest.TestCase):
    def test_missing_variable_exits_with_code_1_and_readable_stderr(self):
        env = _base_env()
        del env["GRAPH_TENANT_ID"]
        buffer = io.StringIO()
        with redirect_stderr(buffer):
            with self.assertRaises(SystemExit) as ctx:
                config.load_settings(env)
        self.assertEqual(ctx.exception.code, 1)
        self.assertIn("GRAPH_TENANT_ID", buffer.getvalue())

    def test_missing_tokens_variable_exits_with_code_1(self):
        env = _base_env()
        del env["BRIDGE_TOKENS"]
        with redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as ctx:
                config.load_settings(env)
        self.assertEqual(ctx.exception.code, 1)

    def test_stderr_never_contains_token_values(self):
        env = _base_env()
        env["BRIDGE_TOKENS"] = "{not valid json"
        buffer = io.StringIO()
        with redirect_stderr(buffer):
            with self.assertRaises(SystemExit):
                config.load_settings(env)
        self.assertNotIn("aaaabbbbccccdddd", buffer.getvalue())

    def test_valid_configuration_is_parsed(self):
        env = _base_env()
        settings = config.load_settings(env)
        self.assertEqual(settings.tenant_id, env["GRAPH_TENANT_ID"])
        self.assertEqual(settings.client_id, env["GRAPH_CLIENT_ID"])
        self.assertEqual(len(settings.accounts), 1)
        self.assertEqual(settings.accounts[0].label, "Damian")
        self.assertEqual(settings.accounts[0].upn, "Damian.Dziura@DTCode.pl")
        self.assertEqual(settings.tokens, {"aaaabbbbccccdddd": "damian"})
        self.assertEqual(settings.port, 8080)
        self.assertEqual(settings.timezone_name, "Europe/Warsaw")
        self.assertEqual(settings.cert_path.as_posix(), "/app/secrets/graph-cert.pem")
        self.assertEqual(settings.key_path.as_posix(), "/app/secrets/graph-key.pem")

    def test_invalid_json_in_accounts_exits(self):
        env = _base_env()
        env["BRIDGE_ACCOUNTS"] = "{not json"
        with redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as ctx:
                config.load_settings(env)
        self.assertEqual(ctx.exception.code, 1)

    def test_account_missing_required_field_exits(self):
        env = _base_env()
        env["BRIDGE_ACCOUNTS"] = json.dumps([{"label": "Damian", "upn": "d@x.pl"}])
        with redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                config.load_settings(env)

    def test_custom_port_and_timezone_are_honoured(self):
        env = _base_env()
        env["BRIDGE_PORT"] = "9090"
        env["BRIDGE_TIMEZONE"] = "UTC"
        settings = config.load_settings(env)
        self.assertEqual(settings.port, 9090)
        self.assertEqual(settings.timezone_name, "UTC")

    def test_invalid_timezone_exits(self):
        env = _base_env()
        env["BRIDGE_TIMEZONE"] = "Nie/Istnieje"
        with redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                config.load_settings(env)

    def test_non_numeric_port_exits(self):
        env = _base_env()
        env["BRIDGE_PORT"] = "not-a-number"
        with redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                config.load_settings(env)


class ThumbprintTests(unittest.TestCase):
    def test_thumbprint_matches_manually_computed_sha1(self):
        self.assertEqual(graph.compute_thumbprint(_CERT_PEM), _EXPECTED_THUMBPRINT)

    def test_thumbprint_is_uppercase_hex_of_sha1_length(self):
        result = graph.compute_thumbprint(_CERT_PEM)
        self.assertEqual(len(result), 40)
        self.assertEqual(result, result.upper())
        int(result, 16)  # nie rzuca -> poprawny ciąg szesnastkowy

    def test_thumbprint_ignores_surrounding_whitespace_and_headers(self):
        padded = f"\n\n{_CERT_PEM}\n\n"
        self.assertEqual(graph.compute_thumbprint(padded), _EXPECTED_THUMBPRINT)


if __name__ == "__main__":
    unittest.main()
