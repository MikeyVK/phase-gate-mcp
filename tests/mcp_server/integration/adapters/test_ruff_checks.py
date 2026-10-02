"""Native Ruff/check-v1 conformance using isolated packages and workspaces."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import venv
from dataclasses import dataclass
from pathlib import Path
from shutil import copytree, rmtree

import pytest
from jsonschema import Draft202012Validator
from pydantic import JsonValue, TypeAdapter

from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.adapter_manifest import AdapterTrustConfig
from mcp_server.core.interfaces.execution import AdapterLaunch
from mcp_server.execution.catalog import AdapterCatalogLoader, FileAdapterPackageReader

NATIVE_CONFIG = (
    '[tool.ruff]\nline-length = 100\ntarget-version = "py311"\n[tool.ruff.lint]\nselect = ["F"]\n'
)


@dataclass(frozen=True)
class RuffPackage:
    launch: AdapterLaunch
    root: Path
    workspace: Path
    schema: Draft202012Validator


@pytest.fixture
def ruff_package(tmp_path: Path, pytestconfig: pytest.Config) -> RuffPackage:
    root = tmp_path / "official packages" / "ruff"
    copytree(pytestconfig.rootpath / "mcp_server/bundled_adapters/ruff", root)
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    (workspace / "pyproject.toml").write_text(NATIVE_CONFIG, encoding="utf-8")
    loader = ConfigLoader(tmp_path / "config", tmp_path / "templates")
    catalog = AdapterCatalogLoader(
        root.parent,
        tmp_path / "workspace adapters",
        AdapterTrustConfig(trusted_adapter_ids=()),
        read_manifest=loader.load_adapter_manifest,
        files=FileAdapterPackageReader(),
        resolve_program=lambda name: Path(sys.executable) if name == "python" else None,
        windows=os.name == "nt",
    ).load()
    for operation in ("lint", "format"):
        binding = catalog.get_check("ruff", operation)
        assert binding.capability.inputs == ("selection",)
        assert binding.capability.requires_file is None
    schema_path = pytestconfig.rootpath / "mcp_server/execution/contracts/check_v1.schema.json"
    return RuffPackage(
        catalog.get_check("ruff", "lint").launch,
        root,
        workspace,
        Draft202012Validator(json.loads(schema_path.read_text(encoding="utf-8"))),
    )


def native(
    workspace: Path,
    operation: str,
    targets: tuple[Path, ...],
    args: tuple[str, ...] = (),
) -> subprocess.CompletedProcess[bytes]:
    controls = (
        ["format", "--check", "--diff"]
        if operation == "format"
        else ["check", "--no-fix", "--no-fix-only"]
    )
    return subprocess.run(
        [sys.executable, "-m", "ruff", *controls, *args, *(str(path) for path in targets)],
        cwd=workspace,
        capture_output=True,
        timeout=15,
    )


def invoke(
    package: RuffPackage,
    operation: str,
    targets: tuple[Path, ...] = (),
    args: tuple[str, ...] = (),
    *,
    interpreter: Path | None = None,
    raw: bytes | None = None,
) -> tuple[int, dict[str, JsonValue]]:
    executable = interpreter if interpreter is not None else package.launch.executable
    assert executable is not None
    request = (
        raw
        if raw is not None
        else json.dumps(
            {
                "execution_context": {"scratch_directory": str(package.workspace.parent)},
                "operation": operation,
                "targets": [str(path) for path in targets],
                "args": list(args),
            }
        ).encode("utf-8")
    )
    completed = subprocess.run(
        [str(executable), *package.launch.args],
        input=request,
        cwd=package.workspace,
        capture_output=True,
        timeout=20,
    )
    assert not completed.stderr, completed.stderr.decode("utf-8", errors="replace")
    response: JsonValue = TypeAdapter(JsonValue).validate_json(completed.stdout)
    assert isinstance(response, dict)
    package.schema.validate(response)
    return completed.returncode, response


def evidence_text(response: dict[str, JsonValue]) -> str:
    evidence = response.get("evidence")
    if evidence is None:
        return ""
    assert isinstance(evidence, dict) and evidence["format"] == "text"
    data = evidence["data"]
    assert isinstance(data, str)
    return data


def decision(response: dict[str, JsonValue]) -> dict[str, JsonValue]:
    value = response["decision"]
    assert isinstance(value, dict)
    return value


def assert_native_evidence(
    response: dict[str, JsonValue],
    result: subprocess.CompletedProcess[bytes],
) -> None:
    evidence = evidence_text(response)
    for stream in (result.stdout, result.stderr):
        if stream:
            assert stream.decode("utf-8", errors="replace") in evidence
    assert response["coverage"] is None
    assert response["required_targets"] == []
    assert response["external_tools"] == [{"tool_id": "ruff", "version": "0.15.6"}]


def test_native_ruff_version_and_read_only_controls_override_fix_configuration(
    ruff_package: RuffPackage,
) -> None:
    package = ruff_package
    version = subprocess.run(
        [sys.executable, "-m", "ruff", "--version"],
        cwd=package.workspace,
        capture_output=True,
        check=True,
        timeout=15,
    )
    assert version.stdout.decode("utf-8").strip() == "ruff 0.15.6"
    assert (package.root / "requirements.txt").read_text(encoding="utf-8").strip() == "ruff==0.15.6"
    target = package.workspace / "unused.py"
    before = b"import os\n"
    target.write_bytes(before)
    (package.workspace / "pyproject.toml").write_text(
        '[tool.ruff]\nfix = true\nfix-only = true\n[tool.ruff.lint]\nselect = ["F"]\n',
        encoding="utf-8",
    )
    result = native(package.workspace, "lint", (target,))
    assert result.returncode == 1
    assert target.read_bytes() == before
    code, response = invoke(package, "lint", (target,))
    assert code == 1
    assert decision(response)["status"] == "failed"
    assert_native_evidence(response, result)
    assert target.read_bytes() == before


def test_lint_preserves_complete_native_json_diagnostics_and_source_bytes(
    ruff_package: RuffPackage,
) -> None:
    package = ruff_package
    target = package.workspace / "multiple findings.py"
    before = b"import os\nmissing_name\n"
    target.write_bytes(before)
    args = ("--output-format=json",)
    result = native(package.workspace, "lint", (target,), args)
    assert result.returncode == 1
    diagnostics = json.loads(result.stdout)
    assert {item["code"] for item in diagnostics} == {"F401", "F821"}
    assert any(item["fix"] is not None for item in diagnostics)
    assert any(item["fix"] is None for item in diagnostics)
    code, response = invoke(package, "lint", (target,), args)
    assert code == 1
    assert decision(response)["status"] == "failed"
    assert diagnostics[0]["code"] in str(decision(response)["message"])
    assert diagnostics[0]["message"] in str(decision(response)["message"])
    assert_native_evidence(response, result)
    assert target.read_bytes() == before


@pytest.mark.parametrize("source", [b"x = 1\n", b"x=1\n"])
def test_format_preserves_native_result_diff_and_notes_without_writing(
    ruff_package: RuffPackage,
    source: bytes,
) -> None:
    package = ruff_package
    target = package.workspace / "format me.py"
    target.write_bytes(source)
    (package.workspace / "pyproject.toml").write_text(
        '[tool.ruff]\nline-length = 100\ntarget-version = "py311"\n'
        '[tool.ruff.lint]\nselect = ["W191"]\n',
        encoding="utf-8",
    )
    result = native(package.workspace, "format", (target,))
    assert result.returncode == (0 if source == b"x = 1\n" else 1)
    assert b"file" in result.stderr
    code, response = invoke(package, "format", (target,))
    assert code == result.returncode
    assert decision(response)["status"] == ("passed" if code == 0 else "failed")
    if code == 1:
        assert "format" in str(decision(response)["message"]).casefold()
        assert not str(decision(response)["message"]).startswith("---")
    assert_native_evidence(response, result)
    legacy = native(package.workspace, "format", (target,), ("--isolated", "--line-length=100"))
    assert legacy.returncode == result.returncode
    assert legacy.stdout == result.stdout
    assert target.read_bytes() == source


def test_literal_targets_configured_discovery_and_explicit_broader_args(
    ruff_package: RuffPackage,
) -> None:
    package = ruff_package
    clean = package.workspace / "clean.py"
    bad = package.workspace / "bad.py"
    clean.write_text("value = 1\n", encoding="utf-8")
    bad.write_text("missing_name\n", encoding="utf-8")
    assert invoke(package, "lint", (clean,))[0] == 0
    assert invoke(package, "lint")[0] == 1
    assert invoke(package, "lint", (clean,), (str(bad),))[0] == 1
    (package.workspace / "pyproject.toml").write_text(
        NATIVE_CONFIG + 'ignore = ["F821"]\n', encoding="utf-8"
    )
    native_result = native(package.workspace, "lint", (bad,))
    code, response = invoke(package, "lint", (bad,))
    assert native_result.returncode == code == 0
    assert_native_evidence(response, native_result)


def test_native_exit_zero_preserves_findings_without_reclassifying_success(
    ruff_package: RuffPackage,
) -> None:
    package = ruff_package
    target = package.workspace / "negative.py"
    target.write_text("missing_name\n", encoding="utf-8")
    args = ("--exit-zero", "--output-format=json")
    result = native(package.workspace, "lint", (target,), args)
    assert result.returncode == 0 and b"F821" in result.stdout
    code, response = invoke(package, "lint", (target,), args)
    assert code == 0 and decision(response)["status"] == "passed"
    assert_native_evidence(response, result)


def test_quiet_native_failure_does_not_fabricate_negative_evidence(
    ruff_package: RuffPackage,
) -> None:
    package = ruff_package
    target = package.workspace / "negative.py"
    target.write_text("missing_name\n", encoding="utf-8")
    args = ("--silent",)
    result = native(package.workspace, "lint", (target,), args)
    assert result.returncode == 1
    assert not result.stdout and not result.stderr
    code, response = invoke(package, "lint", (target,), args)
    assert code == 3
    assert decision(response)["reason"] == "invalid_result"


@pytest.mark.parametrize(
    ("bad_config", "args", "reason"),
    [
        (True, (), "invalid_configuration"),
        (False, ("--unknown-fixture-option",), "unsupported_input"),
    ],
)
@pytest.mark.parametrize("operation", ["lint", "format"])
def test_native_inability_keeps_diagnostics_and_is_not_protocol_rejection(
    ruff_package: RuffPackage,
    operation: str,
    bad_config: bool,
    args: tuple[str, ...],
    reason: str,
) -> None:
    package = ruff_package
    target = package.workspace / "clean.py"
    target.write_text("value = 1\n", encoding="utf-8")
    if bad_config:
        directory = package.workspace / "unknown option unexpected argument no such option"
        directory.mkdir()
        config = directory / "invalid value unrecognized option (os error 2)"
        config.write_text('line-length = "not an integer"\n', encoding="utf-8")
        args = ("--config", str(config))
    result = native(package.workspace, operation, (target,), args)
    assert result.returncode == 2 and result.stderr
    code, response = invoke(package, operation, (target,), args)
    assert code == 3
    assert decision(response)["status"] == "unavailable"
    assert decision(response)["reason"] == reason, result.stderr.decode("utf-8")
    assert_native_evidence(response, result)


@pytest.mark.parametrize(
    "args",
    [
        ("--fix",),
        ("-",),
        ("-o", "forbidden-report.json"),
        ("--add-noqa",),
        ("-voforbidden-report.json",),
        ("\x00",),
    ],
)
def test_check_refuses_fix_stdin_and_output_file_routes(
    ruff_package: RuffPackage,
    args: tuple[str, ...],
) -> None:
    package = ruff_package
    target = package.workspace / "negative.py"
    before = b"import os\n"
    target.write_bytes(before)
    if args[0] == "--add-noqa":
        native(package.workspace, "lint", (target,), args)
        assert target.read_bytes() != before
        target.write_bytes(before)
    elif args[0] == "-voforbidden-report.json":
        native(package.workspace, "lint", (target,), args)
        report = package.workspace / "forbidden-report.json"
        assert report.exists()
        report.unlink()
    code, response = invoke(package, "lint", (target,), args)
    assert code == 3
    assert decision(response)["reason"] == "unsupported_input"
    assert target.read_bytes() == before
    assert not (package.workspace / "forbidden-report.json").exists()


def test_missing_dependency_is_observed_in_the_selected_interpreter(
    ruff_package: RuffPackage,
) -> None:
    package = ruff_package
    environment = package.root.parent / "without ruff"
    venv.EnvBuilder(with_pip=False).create(environment)
    interpreter = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    code, response = invoke(package, "lint", interpreter=interpreter)
    assert code == 3
    assert decision(response)["reason"] == "dependency_unavailable"
    assert response["external_tools"] == [{"tool_id": "ruff", "version": None}]


def test_approved_native_settings_remove_only_the_declared_exemptions(
    ruff_package: RuffPackage,
    pytestconfig: pytest.Config,
) -> None:
    package = ruff_package
    (package.workspace / "pyproject.toml").write_bytes(
        (pytestconfig.rootpath / "pyproject.toml").read_bytes()
    )
    production = package.workspace / "sample.py"
    production.write_text(
        "from typing import Any\n\nclass Sample:\n"
        "    def run(self, unused: int, value: Any) -> None:\n        return None\n",
        encoding="utf-8",
    )
    tests = package.workspace / "tests"
    tests.mkdir()
    test_source = tests / "sample.py"
    test_source.write_text(
        "def sample(unused):\n    UPPER = 1\n"
        '    with open("a") as first:\n        with open("b") as second:\n            pass\n'
        "    try:\n        int('bad')\n    except ValueError:\n        pass\n",
        encoding="utf-8",
    )
    args = ("--output-format=json",)
    result = native(package.workspace, "lint", (production, test_source), args)
    assert result.returncode == 1
    reports = json.loads(result.stdout)
    production_codes = {item["code"] for item in reports if item["filename"] == str(production)}
    test_codes = {item["code"] for item in reports if item["filename"] == str(test_source)}
    assert {"ANN401", "ARG002"} <= production_codes
    assert {"N806", "SIM117", "SIM105"} <= test_codes
    assert not any(code.startswith(("ANN", "ARG")) for code in test_codes)
    code, response = invoke(package, "lint", (production, test_source), args)
    assert code == 1
    assert_native_evidence(response, result)


def test_native_fixture_exclusion_distinguishes_discovery_from_explicit_targets(
    ruff_package: RuffPackage,
    pytestconfig: pytest.Config,
) -> None:
    package = ruff_package
    (package.workspace / "pyproject.toml").write_bytes(
        (pytestconfig.rootpath / "pyproject.toml").read_bytes()
    )
    fixture = package.workspace / "tests/mcp_server/validation_fixtures/negative.py"
    fixture.parent.mkdir(parents=True)
    fixture.write_text("missing_name\n", encoding="utf-8")
    assert invoke(package, "lint")[0] == 0
    result = native(package.workspace, "lint", (fixture,))
    code, response = invoke(package, "lint", (fixture,))
    assert result.returncode == code == 1
    assert b"F821" in result.stdout
    assert_native_evidence(response, result)


def test_request_rejections_preserve_root_and_index_details(ruff_package: RuffPackage) -> None:
    for payload, location, reason in (
        (b"{", [], "invalid_value"),
        (b"[]", [], "wrong_type"),
        (
            json.dumps(
                {
                    "execution_context": {"scratch_directory": str(ruff_package.workspace.parent)},
                    "operation": [],
                    "targets": [],
                    "args": [],
                }
            ).encode(),
            ["operation"],
            "wrong_type",
        ),
        (
            json.dumps(
                {
                    "execution_context": {"scratch_directory": str(ruff_package.workspace.parent)},
                    "operation": "lint",
                    "targets": [42],
                    "args": [],
                }
            ).encode(),
            ["targets", 0],
            "wrong_type",
        ),
    ):
        code, response = invoke(ruff_package, "lint", raw=payload)
        assert code == 2
        assert response == {
            "reason": "invalid_request",
            "details": [{"location": location, "code": reason}],
        }


def test_inherited_output_file_is_refused_before_native_writes(
    ruff_package: RuffPackage,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    package = ruff_package
    target = package.workspace / "negative.py"
    before = b"import os\n"
    target.write_bytes(before)
    report = package.workspace / "inherited-report.json"
    monkeypatch.setenv("RUFF_OUTPUT_FILE", str(report))
    native(package.workspace, "lint", (target,))
    assert report.exists()
    report.unlink()
    code, response = invoke(package, "lint", (target,))
    assert code == 3 and decision(response)["reason"] == "unsupported_input"
    assert not report.exists()
    assert target.read_bytes() == before


@pytest.mark.parametrize("output_format", ["junit", "sarif"])
def test_alternative_native_output_keeps_evidence_and_meaningful_failure_message(
    ruff_package: RuffPackage,
    output_format: str,
) -> None:
    package = ruff_package
    target = package.workspace / "negative.py"
    target.write_text("missing_name\n", encoding="utf-8")
    args = (f"--output-format={output_format}",)
    result = native(package.workspace, "lint", (target,), args)
    assert result.returncode == 1 and result.stdout
    code, response = invoke(package, "lint", (target,), args)
    assert code == 1
    assert "violations" in str(decision(response)["message"]).casefold()
    assert_native_evidence(response, result)


def test_response_file_tokens_do_not_hide_writes_in_pinned_native(
    ruff_package: RuffPackage,
) -> None:
    package = ruff_package
    target = package.workspace / "negative.py"
    before = b"import os\n"
    target.write_bytes(before)
    options = package.workspace / "options.txt"
    options.write_text("--add-noqa\nnegative.py\n", encoding="utf-8")
    args = ("@" + str(options),)
    result = native(package.workspace, "lint", (), args)
    assert result.returncode == 0 and b"noqa" in result.stderr
    assert target.read_bytes() != before
    target.write_bytes(before)
    code, response = invoke(package, "lint", args=args)
    assert code == 3 and decision(response)["reason"] == "unsupported_input"
    assert target.read_bytes() == before


@pytest.mark.parametrize(
    ("operation", "args"),
    [
        ("lint", ("--help",)),
        ("lint", ("-h",)),
        ("lint", ("-vh",)),
        ("lint", ("--show-files",)),
        ("lint", ("--show-settings",)),
        ("lint", ("--diff",)),
        ("format", ("--help",)),
        ("format", ("-h",)),
    ],
)
def test_metadata_and_alternate_modes_cannot_be_passed_analysis(
    ruff_package: RuffPackage,
    operation: str,
    args: tuple[str, ...],
) -> None:
    package = ruff_package
    target = package.workspace / "negative.py"
    before = b"unknown_name\n"
    target.write_bytes(before)
    direct = native(package.workspace, operation, (target,), args)
    assert direct.returncode == 0
    code, response = invoke(package, operation, (target,), args)
    assert code == 3 and decision(response)["reason"] == "unsupported_input"
    assert target.read_bytes() == before


@pytest.mark.parametrize("verbose", [False, True])
def test_native_access_failure_preserves_cause_under_verbosity(
    ruff_package: RuffPackage,
    verbose: bool,
) -> None:
    package = ruff_package
    target = package.workspace / "[DEBUG]missing.py"
    args = ("--verbose",) if verbose else ()
    direct = native(package.workspace, "format", (target,), args)
    assert direct.returncode == 2 and b"os error" in direct.stderr
    code, response = invoke(package, "format", (target,), args)
    assert code == 3 and decision(response)["reason"] == "execution_error"
    native_error = next(line for line in direct.stderr.decode().splitlines() if "os error" in line)
    assert decision(response)["message"] == native_error, direct.stderr.decode("utf-8")
    assert native_error in evidence_text(response)
    if verbose:
        assert "[DEBUG] Using configuration file" in evidence_text(response)


@pytest.mark.parametrize("declaration", ["ruff==0.0.0", "ruff>=0.15.6"])
def test_unsupported_or_malformed_declared_version_is_not_assumed_supported(
    ruff_package: RuffPackage,
    declaration: str,
) -> None:
    package = ruff_package
    target = package.workspace / "clean.py"
    target.write_text("value = 1\n", encoding="utf-8")
    (package.root / "requirements.txt").write_text(declaration + "\n", encoding="utf-8")
    code, response = invoke(package, "lint", (target,))
    assert code == 3 and decision(response)["reason"] == "dependency_unavailable"
    assert response["external_tools"] == [{"tool_id": "ruff", "version": "0.15.6"}]
    assert declaration in str(decision(response)["message"])


@pytest.mark.parametrize("token", ["", " ", "#literal", " literal "])
def test_pinned_argument_file_token_grammar(
    ruff_package: RuffPackage,
    token: str,
) -> None:
    package = ruff_package
    target = package.workspace / "negative Ω with spaces.py"
    target.write_text("unknown_name\n", encoding="utf-8")
    args = ("--exclude", token)
    direct = native(package.workspace, "lint", (target,), args)
    arguments = package.workspace.parent / "grammar-arguments.txt"
    arguments.write_text(
        "\n".join(["--no-fix", "--no-fix-only", *args, str(target)]) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    encoded = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "@" + str(arguments)],
        cwd=package.workspace,
        capture_output=True,
        timeout=15,
    )
    assert encoded.returncode == direct.returncode
    assert encoded.stdout == direct.stdout
    assert encoded.stderr == direct.stderr


@pytest.mark.parametrize("operation", ["format", "lint"])
def test_argument_file_preserves_oversized_selection_and_late_diagnostic(
    ruff_package: RuffPackage,
    operation: str,
) -> None:
    package = ruff_package
    targets = tuple(package.workspace / f"selection_member_{index:03d}.py" for index in range(350))
    for target in targets:
        target.write_text("value = 1\n", encoding="utf-8")
    late = targets[-1]
    late.write_text(
        "value=1\n" if operation == "format" else "late_unknown_name\n", encoding="utf-8"
    )
    decoy = package.workspace / "unselected.py"
    decoy.write_text("unselected_unknown_name\n", encoding="utf-8")
    command = subprocess.list2cmdline([str(path) for path in targets])
    assert len(command.encode("utf-16-le")) // 2 > 32767
    small_code, small = invoke(package, operation, (late,))
    assert small_code == 1 and decision(small)["status"] == "failed"
    code, response = invoke(package, operation, targets)
    assert code == 1 and decision(response)["status"] == "failed"
    assert late.name in evidence_text(response)
    assert "unselected_unknown_name" not in evidence_text(response)
    assert late.read_text(encoding="utf-8") == (
        "value=1\n" if operation == "format" else "late_unknown_name\n"
    )


@pytest.mark.parametrize("token", ["line\nbreak", "line\rbreak", "\ud800"])
def test_unrepresentable_argument_file_tokens_are_explicitly_refused(
    ruff_package: RuffPackage,
    token: str,
) -> None:
    package = ruff_package
    target = package.workspace / "clean.py"
    target.write_text("value = 1\n", encoding="utf-8")
    code, response = invoke(package, "lint", (target,), ("--exclude", token))
    assert code == 3 and decision(response)["reason"] == "unsupported_input"


@pytest.mark.parametrize(
    ("operation", "setting"),
    [("lint", "cli"), ("format", "config"), ("lint", "environment")],
)
def test_operator_cache_preserves_native_check_diagnostics_and_sources(
    ruff_package: RuffPackage,
    monkeypatch: pytest.MonkeyPatch,
    operation: str,
    setting: str,
) -> None:
    package = ruff_package
    target = package.workspace / "selected.py"
    before = b"import os\nvalue=1\n"
    target.write_bytes(before)
    destination = package.workspace.parent / "operator cache"
    args: tuple[str, ...] = ()
    if setting == "cli":
        args = ("--cache-dir", str(destination))
    elif setting == "config":
        config = package.workspace / "pyproject.toml"
        config.write_text(
            config.read_text(encoding="utf-8").replace(
                "[tool.ruff]\n", "[tool.ruff]\ncache-dir = " + json.dumps(str(destination)) + "\n"
            ),
            encoding="utf-8",
        )
    else:
        monkeypatch.setenv("RUFF_CACHE_DIR", str(destination))
    direct = native(package.workspace, operation, (target,), args)
    assert direct.returncode == 1 and destination.is_dir()
    rmtree(destination)
    code, response = invoke(package, operation, (target,), args)
    assert code == 1 and decision(response)["status"] == "failed"
    assert_native_evidence(response, direct)
    assert any(path.is_file() for path in destination.rglob("*"))
    assert not (package.workspace / ".ruff_cache").exists()
    assert target.read_bytes() == before


@pytest.mark.parametrize(
    "key",
    [
        "ordinary-key",
        "os error",
        "permission denied",
        "access denied",
        "is a directory",
        "(os error 2)",
        "[DEBUG]",
        "Failed to load configuration",
        "TOML parse error",
    ],
)
def test_quoted_configuration_key_is_native_usage_error(
    ruff_package: RuffPackage,
    key: str,
) -> None:
    package = ruff_package
    target = package.workspace / "selected.py"
    before = b"import os\n"
    target.write_bytes(before)
    args = ("--config", json.dumps(key) + " = true")
    direct = native(package.workspace, "lint", (target,), args)
    assert direct.returncode == 2 and b"invalid value" in direct.stderr
    code, response = invoke(package, "lint", (target,), args)
    assert code == 3 and decision(response)["reason"] == "unsupported_input"
    assert_native_evidence(response, direct)
    assert target.read_bytes() == before
