"""Native commitlint message/check-v1 conformance in isolated workspaces."""

from __future__ import annotations

import json
import os
import subprocess
import sys
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

MINIMAL_CONFIG = """
module.exports = {
  parserPreset: "conventional-changelog-conventionalcommits",
  defaultIgnores: false,
  rules: {"type-empty": [2, "never"], "subject-empty": [2, "never"]},
};
"""


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
    commitlint_modules: Path, tmp_path_factory: pytest.TempPathFactory
) -> CommitlintRuntime:
    resolved_node = which("node")
    assert resolved_node is not None, "Node is required for the native baseline"
    workspace = commitlint_modules.parent / tmp_path_factory.mktemp("message").name
    workspace.mkdir()
    (workspace / "commitlint.config.cjs").write_text(MINIMAL_CONFIG, encoding="utf-8")
    return CommitlintRuntime(
        Path(resolved_node), commitlint_modules / "@commitlint/cli/cli.js", workspace
    )


def package_for(
    runtime: CommitlintRuntime, tmp_path: Path, repo_root: Path
) -> CommitlintPackage:
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
        runtime, root, binding.launch,
        Draft202012Validator(json.loads(schema_path.read_text(encoding="utf-8"))),
    )


def native(
    runtime: CommitlintRuntime, content: str, args: tuple[str, ...] = ()
) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        [str(runtime.node), str(runtime.cli), *args],
        input=content.encode("utf-8"), cwd=runtime.workspace,
        capture_output=True, timeout=30,
        env={**os.environ, "JITI_FS_CACHE": "0"},
    )


def invoke(
    package: CommitlintPackage, content: str, args: tuple[str, ...] = (), *,
    raw: bytes | None = None, env: dict[str, str] | None = None,
    interpreter: Path | None = None,
) -> tuple[int, dict[str, JsonValue]]:
    request = raw if raw is not None else json.dumps({
        "operation": "message",
        "target_path": str(package.runtime.workspace / "commit.txt"),
        "content": content,
        "args": list(args),
    }).encode("utf-8")
    result = subprocess.run(
        [str(interpreter or package.launch.executable), *package.launch.args],
        input=request, cwd=package.runtime.workspace,
        capture_output=True, timeout=30, env=env,
    )
    assert not result.stderr, result.stderr.decode("utf-8", errors="replace")
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
        ("CuStOm(scope)!: Keep Caller Case\n\nMultiple body lines.\nSecond line.\n\n"
         "Refs: #460\nCaller-footer: unchanged\n", 0),
        ("not a conventional message\n", 1),
    ],
)
def test_native_message_baseline(
    commitlint_runtime: CommitlintRuntime, tmp_path: Path,
    pytestconfig: pytest.Config, content: str, expected: int,
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
