"""Native commitlint message/check-v1 conformance in isolated workspaces."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import venv
from dataclasses import dataclass
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
class CommitlintRuntime:
    node: Path
    cli: Path
    workspace: Path


@dataclass(frozen=True)
class CommitlintPackage:
    runtime: CommitlintRuntime
    root: Path
    launch: AdapterLaunch
    schema: Draft202012Validator


@pytest.fixture(scope="session")
def commitlint_modules(
    tmp_path_factory: pytest.TempPathFactory, pytestconfig: pytest.Config
) -> Path:
    source = pytestconfig.rootpath / "node_modules"
    if not (source / "@commitlint/cli/package.json").is_file():
        source = pytestconfig.rootpath / ".pgmcp/temp/cy024-native/node_modules"
    metadata = json.loads((source / "@commitlint/cli/package.json").read_text(encoding="utf-8"))
    assert metadata["version"] == "21.2.2", "Install the pinned native prerequisites"
    destination = tmp_path_factory.mktemp("commitlint native") / "node_modules"
    copytree(source, destination)
    return destination


@pytest.fixture
def commitlint_runtime(
    commitlint_modules: Path,
    tmp_path_factory: pytest.TempPathFactory,
    pytestconfig: pytest.Config,
) -> CommitlintRuntime:
    resolved_node = which("node")
    assert resolved_node is not None, "Node is required for the native baseline"
    workspace = commitlint_modules.parent / tmp_path_factory.mktemp("message").name
    workspace.mkdir()
    (workspace / "commitlint.config.cjs").write_bytes(
        (pytestconfig.rootpath / "commitlint.config.cjs").read_bytes()
    )
    return CommitlintRuntime(
        Path(resolved_node), commitlint_modules / "@commitlint/cli/cli.js", workspace
    )


def package_for(runtime: CommitlintRuntime, tmp_path: Path, repo_root: Path) -> CommitlintPackage:
    root = tmp_path / "official packages" / "commitlint"
    copytree(repo_root / "mcp_server/bundled_adapters/commitlint", root)
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
    binding = catalog.get_check("commitlint", "message")
    assert binding.capability.inputs == ("content",)
    assert binding.capability.requires_file is False
    schema_path = repo_root / "mcp_server/execution/contracts/check_v1.schema.json"
    return CommitlintPackage(
        runtime,
        root,
        binding.launch,
        Draft202012Validator(json.loads(schema_path.read_text(encoding="utf-8"))),
    )


def native(
    runtime: CommitlintRuntime, content: str, args: tuple[str, ...] = ()
) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        [str(runtime.node), str(runtime.cli), *args],
        input=content.encode("utf-8"),
        cwd=runtime.workspace,
        capture_output=True,
        timeout=30,
        env={**os.environ, "JITI_FS_CACHE": "0"},
    )


def invoke(
    package: CommitlintPackage,
    content: str,
    args: tuple[str, ...] = (),
    *,
    raw: bytes | None = None,
    env: dict[str, str] | None = None,
    interpreter: Path | None = None,
) -> tuple[int, dict[str, JsonValue]]:
    request = (
        raw
        if raw is not None
        else json.dumps(
            {
                "execution_context": {"scratch_directory": str(package.runtime.workspace.parent)},
                "operation": "message",
                "target_path": str(package.runtime.workspace / "commit.txt"),
                "content": content,
                "args": list(args),
            }
        ).encode("utf-8")
    )
    result = subprocess.run(
        [str(interpreter or package.launch.executable), *package.launch.args],
        input=request,
        cwd=package.runtime.workspace,
        capture_output=True,
        timeout=30,
        env=env,
    )
    payload = TypeAdapter(JsonValue).validate_json(result.stdout)
    assert isinstance(payload, dict)
    package.schema.validate(payload)
    return result.returncode, payload


def evidence(response: dict[str, JsonValue]) -> str:
    item = response.get("evidence")
    if item is None:
        return ""
    assert isinstance(item, dict) and item["format"] == "text"
    value = item["data"]
    assert isinstance(value, str)
    return value


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        (
            "CuStOm(scope)!: Keep Caller Case\n\nMultiple body lines.\nSecond line.\n\n"
            "Refs: #460\nCaller-footer: unchanged\n",
            0,
        ),
        pytest.param(
            "unknown argument\n\n [empty-rules]\n\n"
            "✖   found 1 problems, 0 warnings\ncannot find module\n",
            1,
            id="message-diagnostic-markers",
        ),
        (": missing type\n", 1),
        ("feat: \n", 1),
        ("Merge branch 'native-default-ignore-must-be-disabled'\n", 1),
    ],
)
def test_native_message_baseline(
    commitlint_runtime: CommitlintRuntime,
    tmp_path: Path,
    pytestconfig: pytest.Config,
    content: str,
    expected: int,
) -> None:
    result = native(commitlint_runtime, content, ("--color=false", "--verbose"))
    assert result.returncode == expected, (result.stdout, result.stderr)
    package = package_for(commitlint_runtime, tmp_path, pytestconfig.rootpath)
    code, response = invoke(package, content, ("--color=false", "--verbose"))
    assert code == expected
    for stream in (result.stdout, result.stderr):
        if stream:
            assert stream.decode("utf-8") in evidence(response)
    assert response["external_tools"] == [{"tool_id": "commitlint", "version": "21.2.2"}]


@pytest.fixture
def commitlint_package(
    commitlint_runtime: CommitlintRuntime, tmp_path: Path, pytestconfig: pytest.Config
) -> CommitlintPackage:
    return package_for(commitlint_runtime, tmp_path, pytestconfig.rootpath)


RECORD = "pgmcp:v1 id=example pv=1.2.3 pf=AbCdEfGhIjKlMn_- sf=0123456789abcdef"


@pytest.mark.parametrize(
    ("prefix", "message", "stripped", "expected"),
    [
        ("\ufeff<!-- " + RECORD + " -->\r\n", "Custom!: Subject\n\nBody.\n", True, 0),
        ("# " + RECORD + "\n", "invalid message\n", True, 1),
        (
            "# " + RECORD.replace("pv=1.2.3", "pv=01.2.3") + "\n",
            "feat: valid second line\n",
            False,
            1,
        ),
        ("", "feat: Original subject\n\n# " + RECORD + "\n", False, 0),
    ],
)
def test_only_recognized_first_line_is_removed(
    commitlint_package: CommitlintPackage,
    prefix: str,
    message: str,
    stripped: bool,
    expected: int,
) -> None:
    package = commitlint_package
    content = prefix + message
    view = message if stripped else content
    target = package.runtime.workspace / "commit.txt"
    target.write_text("stale on-disk message", encoding="utf-8")
    before = {
        path: path.read_bytes() for path in package.runtime.workspace.rglob("*") if path.is_file()
    }
    args = ("--color=false", "--verbose")
    result = native(package.runtime, view, args)
    code, response = invoke(package, content, args)
    assert result.returncode == code == expected
    text = evidence(response)
    assert view in text
    assert ("first valid provenance line removed" in text) is stripped
    assert result.stdout.decode("utf-8") in text
    assert before == {
        path: path.read_bytes() for path in package.runtime.workspace.rglob("*") if path.is_file()
    }


@pytest.mark.parametrize(
    ("content", "args", "native_code", "expected_code", "reason"),
    [
        ("invalid message", ("--strict",), 3, 1, None),
        ("invalid message", ("--quiet",), 1, 3, "invalid_result"),
        ("invalid message", ("--nonexistent-option",), 1, 3, "unsupported_input"),
        ("invalid message", ("--config", "missing.cjs"), 1, 3, "invalid_configuration"),
        (" \n", (), 1, 3, "unsupported_input"),
    ],
)
def test_native_negative_outcomes(
    commitlint_package: CommitlintPackage,
    content: str,
    args: tuple[str, ...],
    native_code: int,
    expected_code: int,
    reason: str | None,
) -> None:
    package = commitlint_package
    result = native(package.runtime, content, args)
    assert result.returncode == native_code, (result.stdout, result.stderr)
    code, response = invoke(package, content, args)
    assert code == expected_code
    decision = response["decision"]
    assert isinstance(decision, dict)
    assert decision.get("reason") == reason
    for stream in (result.stdout, result.stderr):
        if stream:
            assert stream.decode("utf-8") in evidence(response)


def test_config_formatter_and_warning_overrides(commitlint_package: CommitlintPackage) -> None:
    package = commitlint_package
    workspace = package.runtime.workspace
    (workspace / "custom.cjs").write_text(
        'module.exports = {rules: {"subject-case": [1, "always", "lower-case"]}};',
        encoding="utf-8",
    )
    formatter = workspace / "formatter.cjs"
    formatter.write_text("module.exports = report => JSON.stringify(report);", encoding="utf-8")
    args = ("-g", "custom.cjs", "-s", "-o", str(formatter))
    result = native(package.runtime, "feat: Uppercase subject", args)
    assert result.returncode == 2, (result.stdout, result.stderr)
    code, response = invoke(package, "feat: Uppercase subject", args)
    assert code == 1
    assert result.stdout.decode("utf-8") in evidence(response)
    assert '"warningCount":1' in evidence(response)


def test_missing_rules_are_configuration_failure_even_under_strict(
    commitlint_package: CommitlintPackage,
) -> None:
    package = commitlint_package
    (package.runtime.workspace / "commitlint.config.cjs").unlink()
    formatter = package.runtime.workspace / "formatter.cjs"
    formatter.write_text("module.exports = report => JSON.stringify(report);", encoding="utf-8")
    for args, native_code in (
        ((), 9),
        (("--strict",), 3),
        (("--strict", "--format", str(formatter)), 3),
    ):
        result = native(package.runtime, "feat: Valid subject", args)
        assert result.returncode == native_code
        assert b"empty-rules" in result.stdout
        code, response = invoke(package, "feat: Valid subject", args)
        assert code == 3
        decision = response["decision"]
        assert isinstance(decision, dict) and decision["reason"] == "invalid_configuration"


def test_source_and_early_return_options_are_refused(
    commitlint_package: CommitlintPackage,
) -> None:
    package = commitlint_package
    poison = package.runtime.workspace / "options.cjs"
    marker = package.runtime.workspace / "options-executed"
    poison.write_text(
        'require("fs").writeFileSync(' + json.dumps(str(marker)) + ', "executed");'
        "module.exports = {last: true};",
        encoding="utf-8",
    )
    for args in (
        ("--edit", "missing.txt"),
        ("-VfHEAD",),
        ("--no-last",),
        ("--fromLastTag",),
        ("--options", str(poison)),
        ("--print-config=json",),
        ("-h",),
    ):
        code, response = invoke(package, "feat: Valid subject", args)
        assert code == 3, args
        decision = response["decision"]
        assert isinstance(decision, dict) and decision["reason"] == "unsupported_input", args
    assert not marker.exists()
    assert not (package.runtime.workspace / "commit.txt").exists()


def test_missing_native_and_reader_dependencies_are_honest(
    commitlint_package: CommitlintPackage,
    tmp_path: Path,
) -> None:
    package = commitlint_package
    code, response = invoke(package, "feat: Subject", env={**os.environ, "PATH": ""})
    assert code == 3
    decision = response["decision"]
    assert isinstance(decision, dict) and decision["reason"] == "dependency_unavailable"
    bare = tmp_path / "bare interpreter"
    venv.EnvBuilder(with_pip=False).create(bare)
    executable = bare / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    code, response = invoke(package, "feat: Subject", interpreter=executable)
    assert code == 3
    decision = response["decision"]
    assert isinstance(decision, dict) and decision["reason"] == "dependency_unavailable"
    isolated = tmp_path / "unprovisioned workspace"
    isolated.mkdir()
    copytree(package.runtime.cli.parent, package.root / "node_modules/@commitlint/cli")
    other = CommitlintPackage(
        CommitlintRuntime(package.runtime.node, package.runtime.cli, isolated),
        package.root,
        package.launch,
        package.schema,
    )
    code, response = invoke(other, "feat: Subject")
    assert code == 3
    assert response["external_tools"] == [{"tool_id": "commitlint", "version": None}]
    decision = response["decision"]
    assert isinstance(decision, dict) and decision["reason"] == "dependency_unavailable"


def test_declared_version_precedes_parser_and_configuration(
    commitlint_package: CommitlintPackage,
) -> None:
    package = commitlint_package
    declaration = package.root / "package.json"
    metadata = json.loads(declaration.read_text(encoding="utf-8"))
    metadata["dependencies"]["@commitlint/cli"] = "0.0.0"
    declaration.write_text(json.dumps(metadata), encoding="utf-8")
    marker = package.runtime.workspace / "config-executed"
    config = package.runtime.workspace / "commitlint.config.cjs"
    config.write_text(
        'require("fs").writeFileSync(' + json.dumps(str(marker)) + ', "executed");'
        "module.exports = {rules: {}};",
        encoding="utf-8",
    )
    code, response = invoke(package, "feat: Valid subject", ("--help",))
    assert code == 3
    result = response["decision"]
    assert isinstance(result, dict) and result["reason"] == "dependency_unavailable"
    assert response["external_tools"] == [{"tool_id": "commitlint", "version": "21.2.2"}]
    message = str(result["message"])
    assert "actual=21.2.2" in message and "expected=0.0.0" in message
    assert not marker.exists()
    assert "evidence" not in response


def test_malformed_wire_is_separate(commitlint_package: CommitlintPackage) -> None:
    raw = json.dumps(
        {
            "execution_context": {
                "scratch_directory": str(commitlint_package.runtime.workspace.parent)
            },
            "operation": "message",
            "target_path": str(commitlint_package.runtime.workspace / "commit.txt"),
            "content": "",
            "args": [],
            "extra": 1,
        }
    ).encode()
    code, response = invoke(commitlint_package, "", raw=raw)
    assert code == 2
    assert response == {
        "reason": "invalid_request",
        "details": [{"location": ["extra"], "code": "unknown_field"}],
    }
