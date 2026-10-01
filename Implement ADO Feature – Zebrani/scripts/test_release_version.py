"""Testy skryptu release_version.py — SemVer per repo aplikacji (FE/BE).

Uruchomienie (bez tworzenia __pycache__ w repo):
    PYTHONDONTWRITEBYTECODE=1 python3 test_release_version.py

Testy operuja wylacznie na TemporaryDirectory — nie dotykaja prawdziwych
repozyatoriow ZebraniFE / ZebraniBE.
"""

import codecs
import json
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "release_version.py")


def run_cli(*args):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    return subprocess.run(
        [sys.executable, SCRIPT, *args],
        capture_output=True,
        text=True,
        env=env,
    )


def make_fe_repo(root, version="1.2.3"):
    with open(os.path.join(root, "package.json"), "w", encoding="utf-8") as f:
        json.dump({"name": "zebrani", "version": version}, f, indent=2)
        f.write("\n")
    lock = {
        "name": "zebrani",
        "version": version,
        "lockfileVersion": 3,
        "requires": True,
        "packages": {"": {"name": "zebrani", "version": version}},
    }
    with open(os.path.join(root, "package-lock.json"), "w", encoding="utf-8") as f:
        json.dump(lock, f, indent=2)
        f.write("\n")


def make_version_json(root, version="1.2.3", work_item=2280, base="1.2.3", bump="none",
                     initialized=False):
    payload = {
        "version": version,
        "lastRelease": {"workItem": work_item, "baseVersion": base, "bump": bump},
    }
    if initialized:
        payload["initialized"] = True
    with open(os.path.join(root, "version.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")


def read_version_json(root):
    with open(os.path.join(root, "version.json"), encoding="utf-8") as f:
        return json.load(f)


BE_CSPROJ_TEMPLATE = """<Project Sdk="Microsoft.NET.Sdk.Web">

  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <Nullable>enable</Nullable>
{version_line}  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Dapper" Version="2.1.79" />
  </ItemGroup>

</Project>
"""


def make_be_repo(root, version_line=None):
    proj_dir = os.path.join(root, "ZebraniBE")
    os.makedirs(proj_dir, exist_ok=True)
    body = BE_CSPROJ_TEMPLATE.format(
        version_line=("    <Version>%s</Version>\n" % version_line) if version_line else ""
    )
    with open(os.path.join(proj_dir, "ZebraniBE.csproj"), "w", encoding="utf-8", newline="\n") as f:
        f.write(body)


class ReleaseVersionCliTest(unittest.TestCase):
    def test_preview_does_not_write(self):
        with tempfile.TemporaryDirectory() as repo:
            make_fe_repo(repo, "1.2.3")
            make_version_json(repo, "1.2.3", 2280, "1.2.3", "none")
            proc = run_cli("--repo", repo, "--work-item", "2290", "--bump", "patch")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            out = json.loads(proc.stdout)
            self.assertEqual(out["newVersion"], "1.2.4")
            self.assertFalse(out["write"])
            # Zadnych zmian na dysku.
            self.assertEqual(read_version_json(repo)["version"], "1.2.3")
            with open(os.path.join(repo, "package.json"), encoding="utf-8") as f:
                self.assertEqual(json.load(f)["version"], "1.2.3")

    def test_init_missing_source(self):
        with tempfile.TemporaryDirectory() as repo:
            make_fe_repo(repo, "0.0.0")
            proc = run_cli(
                "--repo", repo, "--work-item", "2290", "--bump", "none",
                "--initial", "0.1.0", "--write",
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            out = json.loads(proc.stdout)
            self.assertEqual(out["newVersion"], "0.1.0")
            self.assertTrue(out["initialized"])
            state = read_version_json(repo)
            self.assertEqual(state["version"], "0.1.0")
            self.assertEqual(state["lastRelease"]["baseVersion"], "0.1.0")
            self.assertEqual(state["lastRelease"]["bump"], "none")
            self.assertEqual(state["lastRelease"]["workItem"], 2290)
            with open(os.path.join(repo, "package.json"), encoding="utf-8") as f:
                self.assertEqual(json.load(f)["version"], "0.1.0")

    def test_missing_source_requires_initial(self):
        with tempfile.TemporaryDirectory() as repo:
            make_fe_repo(repo, "0.0.0")
            proc = run_cli("--repo", repo, "--work-item", "2290", "--bump", "minor", "--write")
            self.assertNotEqual(proc.returncode, 0)
            self.assertFalse(os.path.exists(os.path.join(repo, "version.json")))

    def test_init_rejects_non_none_bump(self):
        with tempfile.TemporaryDirectory() as repo:
            make_fe_repo(repo, "0.0.0")
            proc = run_cli(
                "--repo", repo, "--work-item", "2290", "--bump", "minor",
                "--initial", "0.1.0", "--write",
            )
            self.assertNotEqual(proc.returncode, 0)
            self.assertFalse(os.path.exists(os.path.join(repo, "version.json")))

    def test_major_resets_minor_and_patch(self):
        with tempfile.TemporaryDirectory() as repo:
            make_fe_repo(repo, "1.2.3")
            make_version_json(repo, "1.2.3", 2280, "1.2.3", "none")
            proc = run_cli("--repo", repo, "--work-item", "2290", "--bump", "major", "--write")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(json.loads(proc.stdout)["newVersion"], "2.0.0")
            self.assertEqual(read_version_json(repo)["version"], "2.0.0")

    def test_minor_resets_patch(self):
        with tempfile.TemporaryDirectory() as repo:
            make_fe_repo(repo, "1.2.3")
            make_version_json(repo, "1.2.3", 2280, "1.2.3", "none")
            proc = run_cli("--repo", repo, "--work-item", "2290", "--bump", "minor", "--write")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(read_version_json(repo)["version"], "1.3.0")

    def test_patch(self):
        with tempfile.TemporaryDirectory() as repo:
            make_fe_repo(repo, "1.2.3")
            make_version_json(repo, "1.2.3", 2280, "1.2.3", "none")
            proc = run_cli("--repo", repo, "--work-item", "2290", "--bump", "patch", "--write")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(read_version_json(repo)["version"], "1.2.4")

    def test_repeat_same_pbi_is_idempotent(self):
        with tempfile.TemporaryDirectory() as repo:
            make_fe_repo(repo, "0.1.0")
            make_version_json(repo, "0.1.0", 2290, "0.1.0", "none")
            args = ["--repo", repo, "--work-item", "2290", "--bump", "patch", "--write"]
            first = run_cli(*args)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(read_version_json(repo)["version"], "0.1.1")
            second = run_cli(*args)
            self.assertEqual(second.returncode, 0, second.stderr)
            # Ponowienie tego samego PBI nic nie podbija (1.1.1 -> bez 1.1.2).
            self.assertEqual(read_version_json(repo)["version"], "0.1.1")

    def test_upgrade_bump_recomputed_from_base(self):
        with tempfile.TemporaryDirectory() as repo:
            make_fe_repo(repo, "0.1.0")
            make_version_json(repo, "0.1.0", 2290, "0.1.0", "none")
            proc = run_cli("--repo", repo, "--work-item", "2290", "--bump", "patch", "--write")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            proc = run_cli("--repo", repo, "--work-item", "2290", "--bump", "minor", "--write")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            out = json.loads(proc.stdout)
            # Przeliczone od baseVersion (0.1.0), nie od 0.1.1.
            self.assertEqual(out["newVersion"], "0.2.0")
            self.assertEqual(out["baseVersion"], "0.1.0")

    def test_no_downgrade_on_rerun(self):
        with tempfile.TemporaryDirectory() as repo:
            make_fe_repo(repo, "0.2.0")
            make_version_json(repo, "0.2.0", 2290, "0.1.0", "minor")
            proc = run_cli("--repo", repo, "--work-item", "2290", "--bump", "patch", "--write")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            out = json.loads(proc.stdout)
            self.assertEqual(out["newVersion"], "0.2.0")
            self.assertEqual(out["bumpEffective"], "minor")

    def test_next_work_item_starts_from_current(self):
        with tempfile.TemporaryDirectory() as repo:
            make_fe_repo(repo, "0.2.0")
            make_version_json(repo, "0.2.0", 2290, "0.1.0", "minor")
            proc = run_cli("--repo", repo, "--work-item", "2291", "--bump", "patch", "--write")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            out = json.loads(proc.stdout)
            self.assertEqual(out["baseVersion"], "0.2.0")
            self.assertEqual(out["newVersion"], "0.2.1")

    def test_none_changes_nothing(self):
        with tempfile.TemporaryDirectory() as repo:
            make_fe_repo(repo, "1.2.3")
            make_version_json(repo, "1.2.3", 2280, "1.2.3", "none")
            with open(os.path.join(repo, "package.json"), encoding="utf-8") as f:
                before_pkg = f.read()
            proc = run_cli("--repo", repo, "--work-item", "2291", "--bump", "none", "--write")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            out = json.loads(proc.stdout)
            self.assertEqual(out["newVersion"], "1.2.3")
            self.assertEqual(out["files"], [])
            self.assertEqual(read_version_json(repo)["lastRelease"]["workItem"], 2280)
            with open(os.path.join(repo, "package.json"), encoding="utf-8") as f:
                after_pkg = f.read()
            self.assertEqual(before_pkg, after_pkg)

    def test_invalid_version_rejected_without_write(self):
        with tempfile.TemporaryDirectory() as repo:
            make_fe_repo(repo, "1.2.3")
            make_version_json(repo, "01.2.3", 2280, "01.2.3", "none")
            proc = run_cli("--repo", repo, "--work-item", "2290", "--bump", "patch", "--write")
            self.assertNotEqual(proc.returncode, 0)
            with open(os.path.join(repo, "package.json"), encoding="utf-8") as f:
                self.assertEqual(json.load(f)["version"], "1.2.3")

    def test_inconsistent_state_rejected_without_write(self):
        with tempfile.TemporaryDirectory() as repo:
            make_fe_repo(repo, "1.2.3")
            # version 1.2.4 nie wynika z base 1.2.3 + bump none.
            make_version_json(repo, "1.2.4", 2280, "1.2.3", "none")
            proc = run_cli("--repo", repo, "--work-item", "2291", "--bump", "patch", "--write")
            self.assertNotEqual(proc.returncode, 0)
            self.assertEqual(read_version_json(repo)["version"], "1.2.4")
            with open(os.path.join(repo, "package.json"), encoding="utf-8") as f:
                self.assertEqual(json.load(f)["version"], "1.2.3")

    def test_fe_lock_sync(self):
        with tempfile.TemporaryDirectory() as repo:
            make_fe_repo(repo, "1.2.3")
            make_version_json(repo, "1.2.3", 2280, "1.2.3", "none")
            proc = run_cli("--repo", repo, "--work-item", "2290", "--bump", "patch", "--write")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            with open(os.path.join(repo, "package.json"), encoding="utf-8") as f:
                self.assertEqual(json.load(f)["version"], "1.2.4")
            with open(os.path.join(repo, "package-lock.json"), encoding="utf-8") as f:
                lock = json.load(f)
            self.assertEqual(lock["version"], "1.2.4")
            self.assertEqual(lock["packages"][""]["version"], "1.2.4")

    def test_fe_broken_lock_structure_is_error(self):
        with tempfile.TemporaryDirectory() as repo:
            make_fe_repo(repo, "1.2.3")
            make_version_json(repo, "1.2.3", 2280, "1.2.3", "none")
            with open(os.path.join(repo, "package-lock.json"), "w", encoding="utf-8") as f:
                json.dump({"name": "zebrani", "version": "1.2.3", "packages": []}, f)
            proc = run_cli("--repo", repo, "--work-item", "2290", "--bump", "patch", "--write")
            self.assertNotEqual(proc.returncode, 0)
            self.assertEqual(read_version_json(repo)["version"], "1.2.3")

    def test_be_version_without_touching_dependencies(self):
        with tempfile.TemporaryDirectory() as repo:
            make_be_repo(repo, version_line=None)
            make_version_json(repo, "1.2.3", 2280, "1.2.3", "none")
            proc = run_cli("--repo", repo, "--work-item", "2290", "--bump", "minor", "--write")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            csproj = os.path.join(repo, "ZebraniBE", "ZebraniBE.csproj")
            with open(csproj, encoding="utf-8") as f:
                content = f.read()
            self.assertIn("<Version>1.3.0</Version>", content)
            self.assertIn('PackageReference Include="Dapper" Version="2.1.79"', content)
            self.assertEqual(read_version_json(repo)["version"], "1.3.0")

    def test_be_version_update_keeps_rest(self):
        with tempfile.TemporaryDirectory() as repo:
            make_be_repo(repo, version_line="1.2.3")
            make_version_json(repo, "1.2.3", 2280, "1.2.3", "none")
            proc = run_cli("--repo", repo, "--work-item", "2290", "--bump", "patch", "--write")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            csproj = os.path.join(repo, "ZebraniBE", "ZebraniBE.csproj")
            with open(csproj, encoding="utf-8") as f:
                content = f.read()
            self.assertIn("<Version>1.2.4</Version>", content)
            self.assertNotIn("<Version>1.2.3</Version>", content)
            self.assertIn('PackageReference Include="Dapper" Version="2.1.79"', content)

    def test_ambiguous_repo_is_error(self):
        with tempfile.TemporaryDirectory() as repo:
            make_fe_repo(repo, "1.2.3")
            make_be_repo(repo, version_line="1.2.3")
            make_version_json(repo, "1.2.3", 2280, "1.2.3", "none")
            proc = run_cli("--repo", repo, "--work-item", "2290", "--bump", "patch", "--write")
            self.assertNotEqual(proc.returncode, 0)
            self.assertEqual(read_version_json(repo)["version"], "1.2.3")

    def test_unknown_repo_is_error(self):
        with tempfile.TemporaryDirectory() as repo:
            make_version_json(repo, "1.2.3", 2280, "1.2.3", "none")
            proc = run_cli("--repo", repo, "--work-item", "2290", "--bump", "patch", "--write")
            self.assertNotEqual(proc.returncode, 0)

    def test_leading_zeros_rejected(self):
        with tempfile.TemporaryDirectory() as repo:
            make_fe_repo(repo, "1.2.3")
            proc = run_cli(
                "--repo", repo, "--work-item", "2290", "--bump", "none",
                "--initial", "01.2.3", "--write",
            )
            self.assertNotEqual(proc.returncode, 0)
            self.assertFalse(os.path.exists(os.path.join(repo, "version.json")))

    def test_init_is_first_release_retry_stays_then_new_pbi_bumps(self):
        with tempfile.TemporaryDirectory() as repo:
            make_fe_repo(repo, "0.0.0")
            proc = run_cli(
                "--repo", repo, "--work-item", "2290", "--bump", "none",
                "--initial", "1.0.0", "--write",
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(json.loads(proc.stdout)["newVersion"], "1.0.0")
            # Powtorzenie inicjalizujacego PBI z minor zostaje przy 1.0.0.
            proc = run_cli("--repo", repo, "--work-item", "2290", "--bump", "minor", "--write")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            out = json.loads(proc.stdout)
            self.assertEqual(out["newVersion"], "1.0.0")
            state = read_version_json(repo)
            self.assertEqual(state["version"], "1.0.0")
            self.assertTrue(state.get("initialized"))
            with open(os.path.join(repo, "package.json"), encoding="utf-8") as f:
                self.assertEqual(json.load(f)["version"], "1.0.0")
            # Nowe PBI gubi initialized i bumpuje normalnie od biezacej wersji.
            proc = run_cli("--repo", repo, "--work-item", "2291", "--bump", "minor", "--write")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            out = json.loads(proc.stdout)
            self.assertEqual(out["newVersion"], "1.1.0")
            state = read_version_json(repo)
            self.assertEqual(state["version"], "1.1.0")
            self.assertNotIn("initialized", state)
            self.assertEqual(state["lastRelease"]["workItem"], 2291)

    def test_initialized_marker_requires_none_base(self):
        with tempfile.TemporaryDirectory() as repo:
            make_fe_repo(repo, "0.2.0")
            make_version_json(repo, "0.2.0", 2290, "0.1.0", "minor", initialized=True)
            proc = run_cli("--repo", repo, "--work-item", "2291", "--bump", "patch", "--write")
            self.assertNotEqual(proc.returncode, 0)
            self.assertEqual(read_version_json(repo)["version"], "0.2.0")

    def test_semver_trailing_newline_rejected(self):
        with tempfile.TemporaryDirectory() as repo:
            make_fe_repo(repo, "0.0.0")
            proc = run_cli(
                "--repo", repo, "--work-item", "2290", "--bump", "none",
                "--initial", "1.2.3\n", "--write",
            )
            self.assertNotEqual(proc.returncode, 0)
            self.assertFalse(os.path.exists(os.path.join(repo, "version.json")))

    def test_semver_trailing_newline_in_state_rejected(self):
        with tempfile.TemporaryDirectory() as repo:
            make_fe_repo(repo, "1.2.3")
            make_version_json(repo, "1.2.3\n", 2280, "1.2.3\n", "none")
            proc = run_cli("--repo", repo, "--work-item", "2290", "--bump", "patch", "--write")
            self.assertNotEqual(proc.returncode, 0)
            with open(os.path.join(repo, "package.json"), encoding="utf-8") as f:
                self.assertEqual(json.load(f)["version"], "1.2.3")

    def test_bom_json_files_update_works_and_preview_preserves_bytes(self):
        with tempfile.TemporaryDirectory() as repo:
            pkg_doc = {"name": "zebrani", "version": "1.2.3"}
            lock_doc = {
                "name": "zebrani",
                "version": "1.2.3",
                "lockfileVersion": 3,
                "packages": {"": {"name": "zebrani", "version": "1.2.3"}},
            }
            state_doc = {
                "version": "1.2.3",
                "lastRelease": {"workItem": 2280, "baseVersion": "1.2.3", "bump": "none"},
            }
            paths = {
                "package.json": pkg_doc,
                "package-lock.json": lock_doc,
                "version.json": state_doc,
            }
            for name, doc in paths.items():
                with open(os.path.join(repo, name), "wb") as f:
                    f.write(codecs.BOM_UTF8 + json.dumps(doc, indent=2).encode("utf-8"))
            before = {name: read_raw(os.path.join(repo, name)) for name in paths}
            # Podglad: poprawny wynik i zero zmian bajtow (BOM nietkniety).
            proc = run_cli("--repo", repo, "--work-item", "2290", "--bump", "patch")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(json.loads(proc.stdout)["newVersion"], "1.2.4")
            for name in paths:
                self.assertEqual(read_raw(os.path.join(repo, name)), before[name])
            # Zapis: wersje podbite mimo BOM na wejsciu.
            proc = run_cli("--repo", repo, "--work-item", "2290", "--bump", "patch", "--write")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(read_version_json(repo)["version"], "1.2.4")
            with open(os.path.join(repo, "package.json"), encoding="utf-8-sig") as f:
                self.assertEqual(json.load(f)["version"], "1.2.4")
            with open(os.path.join(repo, "package-lock.json"), encoding="utf-8-sig") as f:
                lock = json.load(f)
            self.assertEqual(lock["version"], "1.2.4")
            self.assertEqual(lock["packages"][""]["version"], "1.2.4")

    def test_be_version_with_label_attribute_updates_and_verifies(self):
        body = (
            '<Project Sdk="Microsoft.NET.Sdk.Web">\n'
            '  <PropertyGroup>\n'
            '    <TargetFramework>net10.0</TargetFramework>\n'
            '    <Version Label="release">1.2.3</Version>\n'
            '  </PropertyGroup>\n'
            '  <ItemGroup>\n'
            '    <PackageReference Include="Dapper" Version="2.1.79" />\n'
            '  </ItemGroup>\n'
            '</Project>\n'
        )
        with tempfile.TemporaryDirectory() as repo:
            csproj = write_csproj(repo, body)
            make_version_json(repo, "1.2.3", 2280, "1.2.3", "none")
            proc = run_cli("--repo", repo, "--work-item", "2290", "--bump", "patch", "--write")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            with open(csproj, encoding="utf-8") as f:
                content = f.read()
            # Atrybut zachowany, tekst podbity, zaleznosci nietkniete.
            self.assertIn('<Version Label="release">1.2.4</Version>', content)
            self.assertNotIn("<Version>1.2.3</Version>", content)
            self.assertIn('PackageReference Include="Dapper" Version="2.1.79"', content)
            self.assertEqual(read_version_json(repo)["version"], "1.2.4")


def write_csproj(root, content):
    proj_dir = os.path.join(root, "ZebraniBE")
    os.makedirs(proj_dir, exist_ok=True)
    path = os.path.join(proj_dir, "ZebraniBE.csproj")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    return path


def read_raw(path):
    with open(path, "rb") as f:
        return f.read()


class ReleaseVersionCsprojGuardTest(unittest.TestCase):
    def test_conditional_version_is_error_before_any_write(self):
        body = (
            '<Project Sdk="Microsoft.NET.Sdk.Web">\n'
            '  <PropertyGroup>\n'
            '    <TargetFramework>net10.0</TargetFramework>\n'
            '    <Version Condition="\'$(Configuration)\'==\'Release\'">1.2.3</Version>\n'
            '  </PropertyGroup>\n'
            '</Project>\n'
        )
        with tempfile.TemporaryDirectory() as repo:
            csproj = write_csproj(repo, body)
            make_version_json(repo, "1.2.3", 2280, "1.2.3", "none")
            before_csproj = read_raw(csproj)
            proc = run_cli("--repo", repo, "--work-item", "2290", "--bump", "patch", "--write")
            self.assertNotEqual(proc.returncode, 0)
            self.assertEqual(read_raw(csproj), before_csproj)
            self.assertEqual(read_version_json(repo)["version"], "1.2.3")

    def test_conditional_first_property_group_is_error(self):
        body = (
            '<Project Sdk="Microsoft.NET.Sdk.Web">\n'
            '  <PropertyGroup Condition="\'$(Configuration)\'==\'Release\'">\n'
            '    <Version>1.2.3</Version>\n'
            '  </PropertyGroup>\n'
            '</Project>\n'
        )
        with tempfile.TemporaryDirectory() as repo:
            csproj = write_csproj(repo, body)
            make_version_json(repo, "1.2.3", 2280, "1.2.3", "none")
            before_csproj = read_raw(csproj)
            proc = run_cli("--repo", repo, "--work-item", "2290", "--bump", "patch", "--write")
            self.assertNotEqual(proc.returncode, 0)
            self.assertEqual(read_raw(csproj), before_csproj)
            self.assertEqual(read_version_json(repo)["version"], "1.2.3")

    def test_multiple_versions_in_first_group_is_error(self):
        body = (
            '<Project Sdk="Microsoft.NET.Sdk.Web">\n'
            '  <PropertyGroup>\n'
            '    <Version>1.2.3</Version>\n'
            '    <Version>1.2.3</Version>\n'
            '  </PropertyGroup>\n'
            '</Project>\n'
        )
        with tempfile.TemporaryDirectory() as repo:
            csproj = write_csproj(repo, body)
            make_version_json(repo, "1.2.3", 2280, "1.2.3", "none")
            before_csproj = read_raw(csproj)
            proc = run_cli("--repo", repo, "--work-item", "2290", "--bump", "patch", "--write")
            self.assertNotEqual(proc.returncode, 0)
            self.assertEqual(read_raw(csproj), before_csproj)
            self.assertEqual(read_version_json(repo)["version"], "1.2.3")

    def test_version_outside_first_group_is_error(self):
        body = (
            '<Project Sdk="Microsoft.NET.Sdk.Web">\n'
            '  <PropertyGroup>\n'
            '    <TargetFramework>net10.0</TargetFramework>\n'
            '  </PropertyGroup>\n'
            '  <PropertyGroup>\n'
            '    <Version>1.2.3</Version>\n'
            '  </PropertyGroup>\n'
            '</Project>\n'
        )
        with tempfile.TemporaryDirectory() as repo:
            csproj = write_csproj(repo, body)
            make_version_json(repo, "1.2.3", 2280, "1.2.3", "none")
            before_csproj = read_raw(csproj)
            proc = run_cli("--repo", repo, "--work-item", "2290", "--bump", "patch", "--write")
            self.assertNotEqual(proc.returncode, 0)
            self.assertEqual(read_raw(csproj), before_csproj)
            self.assertEqual(read_version_json(repo)["version"], "1.2.3")

    def test_malformed_xml_is_error_before_any_write(self):
        body = (
            '<Project Sdk="Microsoft.NET.Sdk.Web">\n'
            '  <PropertyGroup>\n'
            '    <Version>1.2.3</Version>\n'
            '  <!-- niezamkniety komentarz\n'
            '</Project>\n'
        )
        with tempfile.TemporaryDirectory() as repo:
            csproj = write_csproj(repo, body)
            make_version_json(repo, "1.2.3", 2280, "1.2.3", "none")
            before_csproj = read_raw(csproj)
            proc = run_cli("--repo", repo, "--work-item", "2290", "--bump", "patch", "--write")
            self.assertNotEqual(proc.returncode, 0)
            self.assertEqual(read_raw(csproj), before_csproj)
            self.assertEqual(read_version_json(repo)["version"], "1.2.3")


if __name__ == "__main__":
    unittest.main(verbosity=2)
