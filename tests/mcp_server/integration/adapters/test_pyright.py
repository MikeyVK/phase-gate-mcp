"""Native Node Pyright/check-v1 conformance in isolated workspaces."""

from __future__ import annotations

import importlib.metadata
import json
import os
import re
import subprocess
import tomllib
from dataclasses import dataclass, replace
from pathlib import Path
from shutil import copytree, which

import pytest
from jsonschema import Draft202012Validator
from pydantic import JsonValue, TypeAdapter

from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.adapter_manifest import AdapterTrustConfig
from mcp_server.core.interfaces.execution import AdapterLaunch
from mcp_server.execution.catalog import AdapterCatalogLoader, FileAdapterPackageReader


@dataclass(frozen=True)
class NativePyright:
    node: Path
    entrypoint: Path
    root: Path


@dataclass(frozen=True)
class PyrightPackage:
    launch: AdapterLaunch
    root: Path
    workspace: Path
    schema: Draft202012Validator


@pytest.fixture(scope="session")
def native_pyright(tmp_path_factory: pytest.TempPathFactory) -> NativePyright:
    executable = which("node")
    assert executable is not None
    provision = tmp_path_factory.mktemp("native_pyright")
    package = provision / "node_modules" / "pyright"
    installed = importlib.metadata.distribution("pyright")
    copytree(Path(str(installed.locate_file("pyright/dist"))), package)
    metadata = json.loads((package / "package.json").read_text(encoding="utf-8"))
    assert metadata["version"] == "1.1.408"
    return NativePyright(Path(executable), package / "index.js", provision)


@pytest.fixture
def pyright_package(
    native_pyright: NativePyright,
    tmp_path: Path,
    pytestconfig: pytest.Config,
) -> PyrightPackage:
    root = tmp_path / "official packages" / "pyright"
    copytree(pytestconfig.rootpath / "mcp_server/bundled_adapters/pyright", root)
    workspace = native_pyright.root / tmp_path.name
    workspace.mkdir()
    loader = ConfigLoader(tmp_path / "config", tmp_path / "templates")
    catalog = AdapterCatalogLoader(
        root.parent,
        tmp_path / "workspace adapters",
        AdapterTrustConfig(trusted_adapter_ids=()),
        read_manifest=loader.load_adapter_manifest,
        files=FileAdapterPackageReader(),
        resolve_program=lambda name: native_pyright.node if name == "node" else None,
        windows=os.name == "nt",
    ).load()
    binding = catalog.get_check("pyright", "types")
    assert binding.capability.inputs == ("selection",)
    assert binding.capability.requires_file is None
    schema = pytestconfig.rootpath / "mcp_server/execution/contracts/check_v1.schema.json"
    return PyrightPackage(
        binding.launch,
        root,
        workspace,
        Draft202012Validator(json.loads(schema.read_text(encoding="utf-8"))),
    )


def native(
    runtime: NativePyright,
    workspace: Path,
    targets: tuple[Path, ...] = (),
    args: tuple[str, ...] = ("--outputjson",),
) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        [str(runtime.node), str(runtime.entrypoint), *args, *(str(path) for path in targets)],
        cwd=workspace,
        capture_output=True,
        timeout=30,
    )


def invoke(
    package: PyrightPackage,
    targets: tuple[Path, ...] = (),
    args: tuple[str, ...] = (),
    *,
    raw: bytes | None = None,
) -> tuple[int, dict[str, JsonValue]]:
    assert package.launch.executable is not None
    request = (
        raw
        if raw is not None
        else json.dumps(
            {
                "operation": "types",
                "targets": [str(path) for path in targets],
                "args": list(args),
            }
        ).encode()
    )
    completed = subprocess.run(
        [str(package.launch.executable), *package.launch.args],
        input=request,
        cwd=package.workspace,
        capture_output=True,
        timeout=40,
    )
    assert not completed.stderr, completed.stderr.decode("utf-8", errors="replace")
    response = TypeAdapter(JsonValue).validate_json(completed.stdout)
    assert isinstance(response, dict)
    package.schema.validate(response)
    return completed.returncode, response


def decision(response: dict[str, JsonValue]) -> dict[str, JsonValue]:
    value = response["decision"]
    assert isinstance(value, dict)
    return value


def evidence_text(response: dict[str, JsonValue]) -> str:
    value = response["evidence"]
    assert isinstance(value, dict) and value["format"] == "text"
    data = value["data"]
    assert isinstance(data, str)
    return data


def native_json(output: bytes) -> dict[str, JsonValue]:
    value = TypeAdapter(JsonValue).validate_json(output)
    assert isinstance(value, dict)
    return value


def assert_json_evidence(
    response: dict[str, JsonValue],
    direct: subprocess.CompletedProcess[bytes],
) -> dict[str, JsonValue]:
    data = evidence_text(response)
    assert data.startswith("stdout:\n")
    stdout = data[len("stdout:\n") :].split("\nstderr:\n", 1)[0]
    actual = native_json(stdout.encode())
    expected = native_json(direct.stdout)
    # Native timing fields vary per invocation; diagnostics are preserved verbatim.
    assert actual["generalDiagnostics"] == expected["generalDiagnostics"]
    assert actual["version"] == expected["version"] == "1.1.408"
    for key in ("filesAnalyzed", "errorCount", "warningCount", "informationCount"):
        actual_summary, expected_summary = actual["summary"], expected["summary"]
        assert isinstance(actual_summary, dict) and isinstance(expected_summary, dict)
        assert actual_summary[key] == expected_summary[key]
    if direct.stderr:
        assert direct.stderr.decode() in data
    assert response["coverage"] is None
    assert response["required_targets"] == []
    assert response["external_tools"] == [{"tool_id": "pyright", "version": "1.1.408"}]
    return actual


@pytest.mark.parametrize(
    ("source", "assignment_severity", "args", "code", "severities"),
    [
        ("value: int = 1\n", "error", (), 0, []),
        ('value: int = "bad"\n', "warning", ("--warnings", "--level", "error"), 1, []),
        (
            'first: int = "bad"\nsecond: str = 1\nreveal_type(first)\n',
            "error",
            (),
            1,
            ["error", "error", "information"],
        ),
        ('value: int = "bad"\nreveal_type(value)\n', "warning", (), 0, ["warning", "information"]),
        (
            'value: int = "bad"\nreveal_type(value)\n',
            "warning",
            ("--warnings",),
            1,
            ["warning", "information"],
        ),
    ],
    ids=[
        "clean",
        "filtered-warning-fails",
        "errors-and-information",
        "warning-passes",
        "warnings-fail",
    ],
)
def test_native_results_and_diagnostic_facts(
    native_pyright: NativePyright,
    pyright_package: PyrightPackage,
    source: str,
    assignment_severity: str,
    args: tuple[str, ...],
    code: int,
    severities: list[str],
) -> None:
    package = pyright_package
    (package.workspace / "pyrightconfig.json").write_text(
        json.dumps(
            {
                "pythonVersion": "3.11",
                "reportAssignmentType": assignment_severity,
            }
        ),
        encoding="utf-8",
    )
    target = package.workspace / "sample with space.py"
    before = source.encode()
    target.write_bytes(before)
    direct = native(native_pyright, package.workspace, (target,), ("--outputjson", *args))
    assert direct.returncode == code
    actual_code, response = invoke(package, (target,), args)
    assert actual_code == code
    assert decision(response)["status"] == ("passed" if code == 0 else "failed")
    actual = assert_json_evidence(response, direct)
    diagnostics = actual["generalDiagnostics"]
    assert isinstance(diagnostics, list)
    assert all(isinstance(item, dict) for item in diagnostics)
    facts = [item for item in diagnostics if isinstance(item, dict)]
    assert [item["severity"] for item in facts] == severities
    for index, item in enumerate(facts):
        assert Path(str(item["file"])) == target
        location = item["range"]
        assert isinstance(location, dict)
        start = location["start"]
        assert isinstance(start, dict) and start["line"] == index
        assert isinstance(item["message"], str) and item["message"]
        if item["severity"] != "information":
            assert item["rule"] == "reportAssignmentType"
    if code == 1:
        expected_message = (
            facts[0]["message"] if facts else "Pyright reported an unsuccessful check."
        )
        assert decision(response)["message"] == expected_message
    assert target.read_bytes() == before
    manifest = json.loads((package.root / "package.json").read_text())
    assert manifest["dependencies"] == {"pyright": "1.1.408"}


@pytest.mark.parametrize("mode", ["--verbose", "--stats", "--dependencies"])
def test_explicit_native_text_modes(
    native_pyright: NativePyright,
    pyright_package: PyrightPackage,
    mode: str,
) -> None:
    package = pyright_package
    target = package.workspace / "sample.py"
    target.write_text('value: int = "bad"\n', encoding="utf-8")
    direct = native(native_pyright, package.workspace, (target,), (mode,))
    assert direct.returncode == 1
    code, response = invoke(package, (target,), (mode,))
    assert code == 1
    text = evidence_text(response)
    assert not text.removeprefix("stdout:\n").lstrip().startswith("{")
    native_lines = (direct.stdout + direct.stderr).decode().splitlines()
    diagnostic = next(line for line in native_lines if " - error: " in line)
    assert diagnostic in text
    assert "assignable" in str(decision(response)["message"])
    assert target.read_text() == 'value: int = "bad"\n'


def test_native_discovery_and_literal_targets(
    native_pyright: NativePyright,
    pyright_package: PyrightPackage,
) -> None:
    package = pyright_package
    included = package.workspace / "mcp_server"
    included.mkdir()
    (included / "clean.py").write_text("value: int = 1\n")
    excluded = package.workspace / "tests"
    excluded.mkdir()
    target = excluded / "negative.py"
    target.write_text('value: int = "bad"\n')
    (package.workspace / "pyrightconfig.json").write_text(
        json.dumps(
            {
                "include": ["mcp_server"],
                "exclude": ["ignored"],
            }
        )
    )
    for targets, expected in (((), 0), ((target,), 1)):
        direct = native(native_pyright, package.workspace, targets)
        assert direct.returncode == expected
        code, response = invoke(package, targets)
        assert code == expected
        assert_json_evidence(response, direct)


@pytest.mark.parametrize(
    ("configuration", "args", "native_code", "reason"),
    [
        ("{", (), 3, "invalid_configuration"),
        ("{}", ("--unknown-option",), 4, "unsupported_input"),
        ("{}", ("--outputjson", "--verbose"), 4, "unsupported_input"),
    ],
    ids=["broken-config", "unknown-option", "explicit-conflicting-output"],
)
def test_native_unavailability(
    native_pyright: NativePyright,
    pyright_package: PyrightPackage,
    configuration: str,
    args: tuple[str, ...],
    native_code: int,
    reason: str,
) -> None:
    package = pyright_package
    (package.workspace / "pyrightconfig.json").write_text(configuration)
    target = package.workspace / "sample.py"
    target.write_text("value: int = 1\n")
    native_args = args if "--outputjson" in args else ("--outputjson", *args)
    direct = native(native_pyright, package.workspace, (target,), native_args)
    assert direct.returncode == native_code
    code, response = invoke(package, (target,), args)
    assert code == 3 and decision(response)["reason"] == reason
    assert str(decision(response)["message"]).strip()
    if direct.stdout.lstrip().startswith(b"{"):
        assert_json_evidence(response, direct)
    else:
        for stream in (direct.stdout, direct.stderr):
            if stream:
                assert stream.decode() in evidence_text(response)


@pytest.mark.parametrize("args", [("--createstub", "sample"), ("-",), ("\x00",)])
def test_refuses_write_and_stdin_routes(
    pyright_package: PyrightPackage,
    args: tuple[str, ...],
) -> None:
    package = pyright_package
    target = package.workspace / "sample.py"
    target.write_text("value: int = 1\n")
    code, response = invoke(package, (target,), args)
    assert code == 3 and decision(response)["reason"] == "unsupported_input"
    assert sorted(path.name for path in package.workspace.iterdir()) == ["sample.py"]
    assert target.read_text() == "value: int = 1\n"


def test_dependency_resolution_uses_workspace_ancestors(
    native_pyright: NativePyright,
    pyright_package: PyrightPackage,
    tmp_path: Path,
) -> None:
    package = pyright_package
    empty = tmp_path / "unprovisioned workspace"
    empty.mkdir()
    # An adapter-adjacent installation must never mask missing workspace provisioning.
    copytree(native_pyright.entrypoint.parent, package.root / "node_modules" / "pyright")
    code, response = invoke(replace(package, workspace=empty))
    assert code == 3 and decision(response)["reason"] == "dependency_unavailable"
    assert response["external_tools"] == [{"tool_id": "pyright", "version": None}]


@pytest.mark.parametrize(
    ("raw", "location", "reason"),
    [
        (b"\xff", [], "invalid_value"),
        (b"[]", [], "wrong_type"),
        (
            b'{"operation":"types","targets":["relative.py"],"args":[]}',
            ["targets", 0],
            "invalid_value",
        ),
    ],
)
def test_invalid_requests(
    pyright_package: PyrightPackage,
    raw: bytes,
    location: list[str | int],
    reason: str,
) -> None:
    code, response = invoke(pyright_package, raw=raw)
    assert code == 2
    assert response == {
        "reason": "invalid_request",
        "details": [{"location": location, "code": reason}],
    }


def test_native_configuration_preservation_and_editor_target(
    native_pyright: NativePyright,
    pyright_package: PyrightPackage,
    pytestconfig: pytest.Config,
) -> None:
    package = pyright_package
    original_toml = (pytestconfig.rootpath / "pyproject.toml").read_bytes()
    toml = original_toml.decode().replace("\r\n", "\n")
    without_duplicate = re.sub(r"(?ms)^\[tool\.pyright\]\n.*?(?=^\[|\Z)", "", toml)
    original_settings = tomllib.loads(toml)
    removed_settings = tomllib.loads(without_duplicate)
    assert original_settings["tool"].pop("pyright") == {"reportFunctionMemberAccess": False}
    assert original_settings == removed_settings
    config = json.loads((pytestconfig.rootpath / "pyrightconfig.json").read_text())
    assert config["pythonVersion"] == "3.11" and config["pythonPlatform"] == "Windows"
    assert config["reportFunctionMemberAccess"] is False
    assert config["reportArgumentType"] is False
    assert config["reportMissingImports"] is True
    assert config["executionEnvironments"] == [
        {"root": "./backend"},
        {"root": "./mcp_server"},
        {"root": "./tests"},
    ]
    for name in ("backend", "mcp_server", "tests"):
        (package.workspace / name).mkdir()
    target = package.workspace / "mcp_server" / "settings_probe.py"
    target.write_text(
        "import sys\n"
        "def accepts_int(value: int) -> int:\n    return value\n"
        'accepted: int = accepts_int("bad")\n'
        "accepts_int.custom = 1\n"
        'if sys.platform != "win32":\n    platform_error: int = "bad"\n'
        'if sys.version_info >= (3, 12):\n    version_error: int = "bad"\n'
        "type Alias = int\n"
        'assignment_error: int = "bad"\n'
        "import missing_dependency_for_pyright_probe\n"
        "reveal_type(accepted)\n",
        encoding="utf-8",
    )
    config_path = package.workspace / "pyrightconfig.json"
    toml_path = package.workspace / "pyproject.toml"
    toml_path.write_text(toml, encoding="utf-8")
    old_config = {**config, "pythonVersion": "3.13"}
    config_path.write_text(json.dumps(old_config))
    legacy = native(
        native_pyright,
        package.workspace,
        args=(
            "--project",
            "pyrightconfig.json",
            "--pythonversion",
            "3.11",
            "--pythonplatform",
            "Windows",
            "--level",
            "warning",
            "--warnings",
            "--outputjson",
        ),
    )
    assert legacy.returncode == 1
    config_path.write_text(json.dumps(config))
    code, before = invoke(package, args=("--level", "warning", "--warnings"))
    assert code == 1
    actual = assert_json_evidence(before, legacy)
    diagnostics = actual["generalDiagnostics"]
    assert isinstance(diagnostics, list)
    facts = [item for item in diagnostics if isinstance(item, dict)]
    messages = [str(item["message"]) for item in facts]
    assert any("3.12" in message for message in messages)
    assert any("missing_dependency_for_pyright_probe" in message for message in messages)
    assert sum(item.get("rule") == "reportAssignmentType" for item in facts) == 1
    assert not any(item.get("rule") == "reportArgumentType" for item in facts)
    assert not any(item.get("rule") == "reportFunctionMemberAccess" for item in facts)
    toml_path.write_text(without_duplicate, encoding="utf-8")
    code, after = invoke(package, args=("--level", "warning", "--warnings"))
    assert code == 1
    assert_json_evidence(after, legacy)
    config_path.write_text(json.dumps(old_config))
    editor = native(native_pyright, package.workspace, args=("--outputjson",))
    editor_facts = native_json(editor.stdout)["generalDiagnostics"]
    assert isinstance(editor_facts, list)
    assert not any("3.12" in str(item) for item in editor_facts)
    assert (pytestconfig.rootpath / "pyproject.toml").read_bytes() == original_toml
