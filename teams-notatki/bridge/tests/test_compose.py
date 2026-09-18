import re
import unittest
from pathlib import Path

BRIDGE_DIR = Path(__file__).parents[1]
COMPOSE_PATH = BRIDGE_DIR / "docker-compose.yml"
DOCKERFILE_PATH = BRIDGE_DIR / "Dockerfile"


class ComposeDefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.compose = COMPOSE_PATH.read_text(encoding="utf-8")

    def _service_names(self) -> list[str]:
        names = []
        in_services = False
        for line in self.compose.splitlines():
            if line == "services:":
                in_services = True
                continue
            if in_services and line and not line.startswith(" "):
                break
            if (
                in_services
                and line.startswith("  ")
                and not line.startswith("   ")
                and line.rstrip().endswith(":")
            ):
                names.append(line.strip()[:-1])
        return names

    def test_compose_defines_exactly_one_service(self):
        self.assertEqual(self._service_names(), ["teams-transcript-bridge"])

    def test_compose_has_required_directives(self):
        self.assertIn("restart: unless-stopped", self.compose)
        self.assertIn("env_file: .env", self.compose)
        self.assertIn("build: .", self.compose)

    def test_compose_maps_only_the_expected_port(self):
        ports = re.search(
            r"(?ms)^\s{4}ports:\s*\n(?P<entries>(?:^\s{6}-[^\n]*\n?)+)",
            self.compose,
        )
        self.assertIsNotNone(ports)
        mappings = re.findall(r"(?m)^\s{6}-\s*[\"']([^\"']+)[\"']\s*$", ports.group("entries"))
        self.assertEqual(mappings, ["40002:8080"])

    def test_compose_mounts_the_secrets_volume_read_only(self):
        volumes = re.search(
            r"(?ms)^\s{4}volumes:\s*\n(?P<entries>(?:^\s{6}-[^\n]*\n?)+)",
            self.compose,
        )
        self.assertIsNotNone(volumes)
        mounts = re.findall(r"(?m)^\s{6}-\s*([^\n]+?)\s*$", volumes.group("entries"))
        self.assertEqual(mounts, ["./secrets:/app/secrets:ro"])

    def test_compose_forbids_unexpected_sections(self):
        for forbidden in ("deploy", "depends_on", "environment", "secrets"):
            pattern = re.compile(rf"(?m)^\s*{forbidden}:\s*$")
            self.assertIsNone(
                pattern.search(self.compose),
                f"nieoczekiwana sekcja top-level '{forbidden}:' w compose",
            )

    def test_compose_does_not_mention_graph_directly(self):
        self.assertNotIn("Graph", self.compose)

    def test_dockerfile_runs_the_standard_library_app_on_port_8080_as_non_root(self):
        dockerfile = DOCKERFILE_PATH.read_text(encoding="utf-8")
        self.assertIn("FROM python:3.12-slim", dockerfile)
        self.assertIn("EXPOSE 8080", dockerfile)
        self.assertIn('CMD ["python", "app.py"]', dockerfile)
        self.assertIn("useradd -r bridge", dockerfile)
        self.assertIn("USER bridge", dockerfile)


if __name__ == "__main__":
    unittest.main()
