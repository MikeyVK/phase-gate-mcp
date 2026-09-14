"""Native Lychee/check-v1 content and literal selection conformance."""

from __future__ import annotations

import json
import os
import re
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

DEFAULT_ARGS = ("--offline", "--cache=false", "--include-fragments")


@dataclass(frozen=True)
class LycheeRuntime:
    executable: Path
    workspace: Path


@dataclass(frozen=True)
class LycheePackage:
    runtime: LycheeRuntime
    launch: AdapterLaunch
    schema: Draft202012Validator


@pytest.fixture
def lychee_runtime(tmp_path: Path, pytestconfig: pytest.Config) -> LycheeRuntime:
    program = which("lychee")
    executable = Path(program) if program else (
        pytestconfig.rootpath
        / "temp/link-probe-20260906/bin/lychee-x86_64-pc-windows-msvc/lychee.exe"
    )
    assert executable.is_file(), "Install the declared Lychee native prerequisite"
    version = subprocess.run(
        [str(executable), "--version"], capture_output=True, check=True, timeout=10
    )
    assert version.stdout.decode().strip() == "lychee 0.24.2"
    workspace = tmp_path / "workspace with spaces"
    workspace.mkdir()
    return LycheeRuntime(executable, workspace)


def package_for(
    runtime: LycheeRuntime, tmp_path: Path, repo_root: Path
) -> LycheePackage:
    root = tmp_path / "official packages" / "lychee"
    copytree(repo_root / "mcp_server/bundled_adapters/lychee", root)
    loader = ConfigLoader(tmp_path / "config", tmp_path / "templates")
    catalog = AdapterCatalogLoader(
        root.parent, tmp_path / "workspace adapters",
        AdapterTrustConfig(trusted_adapter_ids=()),
        read_manifest=loader.load_adapter_manifest, files=FileAdapterPackageReader(),
        resolve_program=lambda name: Path(sys.executable) if name == "python" else None,
        windows=os.name == "nt",
    ).load()
    binding = catalog.get_check("lychee", "links")
    assert set(binding.capability.inputs) == {"content", "selection"}
    assert binding.capability.requires_file is True
    schema_path = repo_root / "mcp_server/execution/contracts/check_v1.schema.json"
    return LycheePackage(
        runtime, binding.launch,
        Draft202012Validator(json.loads(schema_path.read_text(encoding="utf-8"))),
    )


def invoke(
    package: LycheePackage, request: dict[str, object]
) -> tuple[int, dict[str, JsonValue]]:
    environment = {
        **os.environ,
        "PATH": str(package.runtime.executable.parent) + os.pathsep + os.environ.get("PATH", ""),
    }
    result = subprocess.run(
        [str(package.launch.executable), *package.launch.args],
        input=json.dumps(request).encode("utf-8"), cwd=package.runtime.workspace,
        capture_output=True, timeout=30, env=environment,
    )
    payload = TypeAdapter(JsonValue).validate_json(result.stdout)
    assert isinstance(payload, dict)
    package.schema.validate(payload)
    return result.returncode, payload


@pytest.mark.parametrize("broken", [False, True])
def test_native_self_toc_and_neighbor_snapshot(
    lychee_runtime: LycheeRuntime, tmp_path: Path, pytestconfig: pytest.Config, broken: bool,
) -> None:
    runtime = lychee_runtime
    target = runtime.workspace / "docs" / "guide.md"
    target.parent.mkdir()
    neighbor = target.with_name("neighbor.md")
    neighbor.write_text("# Neighbor\n\n## Existing\n", encoding="utf-8")
    scratch = tmp_path / "validation" / "fresh invocation" / target.name
    scratch.parent.mkdir(parents=True)
    content = "# Guide\n\n## Existing\n\n[TOC](#existing)\n"
    content += "[Self](guide.md#existing)\n[Neighbor](neighbor.md#existing)\n"
    if broken:
        content += "[Bad TOC](#absent)\n[Bad self](guide.md#absent)\n"
        content += "[Bad neighbor](neighbor.md#absent)\n[Missing](missing.md)\n"
    scratch.write_text(content, encoding="utf-8")
    logical_url = target.as_uri()
    remap = "^" + re.escape(logical_url) + "(#.*)?$ " + scratch.as_uri() + "$1"
    args = (*DEFAULT_ARGS, "--format", "json")
    native_result = subprocess.run(
        [str(runtime.executable), *args, "--base-url", logical_url, "--remap", remap,
         str(scratch)],
        cwd=runtime.workspace, capture_output=True, timeout=30,
    )
    assert native_result.returncode == (2 if broken else 0), (
        native_result.stdout, native_result.stderr
    )
    assert not target.exists()
    package = package_for(runtime, tmp_path, pytestconfig.rootpath)
    code, response = invoke(package, {
        "operation": "links", "target_path": str(target), "input_path": str(scratch),
        "args": list(args),
    })
    assert code == (1 if broken else 0)
    decision = response["decision"]
    assert isinstance(decision, dict) and decision["status"] == ("failed" if broken else "passed")
    assert response["external_tools"] == [{"tool_id": "lychee", "version": "0.24.2"}]
    assert not target.exists()
    assert scratch.read_text(encoding="utf-8") == content
    assert neighbor.read_text(encoding="utf-8") == "# Neighbor\n\n## Existing\n"
