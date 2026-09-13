"""Native Node Pyright/check-v1 conformance in isolated workspaces."""

from __future__ import annotations

import importlib.metadata
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from shutil import copytree, which

import pytest


@dataclass(frozen=True)
class NativePyright:
    node: Path
    entrypoint: Path
    root: Path


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


def test_native_pyright_error_baseline(native_pyright: NativePyright, tmp_path: Path) -> None:
    source = tmp_path / "sample.py"
    source.write_text('value: int = "bad"\n', encoding="utf-8")
    result = subprocess.run(
        [str(native_pyright.node), str(native_pyright.entrypoint), "--outputjson", str(source)],
        cwd=tmp_path, capture_output=True, timeout=30,
    )
    assert result.returncode == 1
    response = json.loads(result.stdout)
    assert response["version"] == "1.1.408"
    assert response["generalDiagnostics"][0]["severity"] == "error"


def test_adapter_preserves_native_negative_diagnostic(
    native_pyright: NativePyright, tmp_path: Path, pytestconfig: pytest.Config,
) -> None:
    package = tmp_path / "official packages" / "pyright"
    copytree(pytestconfig.rootpath / "mcp_server/bundled_adapters/pyright", package)
    workspace = native_pyright.root / tmp_path.name
    workspace.mkdir()
    source = workspace / "sample.py"
    before = b'value: int = "bad"\n'
    source.write_bytes(before)
    result = subprocess.run(
        [str(native_pyright.node), str(package / "check.cjs")],
        input=json.dumps({"operation": "types", "targets": [str(source)], "args": []}).encode(),
        cwd=workspace, capture_output=True, timeout=30,
    )
    assert result.returncode == 1
    response = json.loads(result.stdout)
    assert response["decision"]["status"] == "failed"
    assert "assigned" in response["decision"]["message"]
    assert source.read_bytes() == before
