"""Inspect complete wheel assets and exercise public installed consumers outside checkout."""

from __future__ import annotations

import json
from email.parser import BytesParser
from pathlib import Path
from zipfile import ZipFile

import pytest
import yaml
from packaging.requirements import Requirement

from tests.mcp_server.fixtures.installed_distribution import (
    CATALOG_PROBE,
    ENTRYPOINT_PROBE,
    build_installed_distribution,
)
from tests.mcp_server.integration.adapters.test_commitlint import (
    CommitlintRuntime,
    commitlint_modules,
    commitlint_runtime,
    native,
)

__all__ = ["commitlint_modules", "commitlint_runtime"]


def test_complete_wheel_and_installed_catalogs_and_entrypoints(
    tmp_path: Path,
    pytestconfig: pytest.Config,
    commitlint_runtime: CommitlintRuntime,
) -> None:
    source = pytestconfig.rootpath
    distribution = build_installed_distribution(source, tmp_path / "distribution")
    inventories = (
        (source / ".pgmcp/template_suite", "mcp_server/assets/template_suite"),
        (source / ".pgmcp/config", "mcp_server/assets/config"),
        (source / "mcp_server/bundled_adapters", "mcp_server/bundled_adapters"),
        (source / "mcp_server/execution/contracts", "mcp_server/execution/contracts"),
    )
    with ZipFile(distribution.wheel) as wheel:
        names = set(wheel.namelist())
        assert not any(name.startswith("mcp_server/assets/bundled_adapters/") for name in names)
        assert not any("/workspace_adapters/" in name for name in names)
        for root, installed in inventories:
            files = [
                path
                for path in root.rglob("*")
                if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
            ]
            assert files
            for path in files:
                member = installed + "/" + path.relative_to(root).as_posix()
                assert member in names, member
                assert wheel.read(member) == path.read_bytes(), member
                assert (distribution.root / member).read_bytes() == path.read_bytes(), member
        metadata_path = next(name for name in names if name.endswith(".dist-info/METADATA"))
        metadata = BytesParser().parsebytes(wheel.read(metadata_path))
        requirements = {
            Requirement(value).name.lower()
            for value in metadata.get_all("Requires-Dist", [])
            if Requirement(value).marker is None
        }
        assert "jsonschema" in requirements
        entrypoints = next(name for name in names if name.endswith(".dist-info/entry_points.txt"))
        assert "pgmcp = mcp_server.cli:main" in wheel.read(entrypoints).decode()
    header = "# pgmcp:v1 id=example pv=1.2.3 pf=AbCdEfGhIjKlMn_- sf=0123456789abcdef\n"
    probed = distribution.python(CATALOG_PROBE, arguments=(header,))
    assert probed.returncode == 0, probed.stdout + probed.stderr
    observed = json.loads(probed.stdout)
    expected_templates = {
        yaml.safe_load(path.read_text(encoding="utf-8"))["template_id"]
        for path in (source / ".pgmcp/template_suite").glob("*/manifest.yaml")
    }
    expected_adapters = {
        yaml.safe_load(path.read_text(encoding="utf-8"))["adapter_id"]
        for path in (source / "mcp_server/bundled_adapters").glob("*/manifest.yaml")
    }
    assert set(observed["templates"]) == expected_templates
    assert set(observed["adapters"]) == expected_adapters
    assert observed["header"]["status"] == "recognized"
    assert observed["header"]["provenance"]["id"] == "example"
    assert observed["origins"]
    assert all(
        Path(path).is_relative_to(distribution.root) for path in observed["origins"].values()
    )
    assert not Path(observed["package"]).is_relative_to(source)

    message = "Custom!: Installed consumer\n\nBody.\n"
    native_result = native(commitlint_runtime, message)
    assert native_result.returncode == 0, native_result.stdout + native_result.stderr
    report = distribution.workspace / "entrypoint-origins.json"
    scratch_directory = tmp_path / "installed adapter invocation"
    scratch_directory.mkdir()
    request = {
        "operation": "message",
        "target_path": str(commitlint_runtime.workspace / "commit.txt"),
        "content": header + message,
        "args": [],
        "execution_context": {"scratch_directory": str(scratch_directory)},
    }
    invoked = distribution.python(
        ENTRYPOINT_PROBE,
        arguments=("mcp_server/bundled_adapters/commitlint/check.py", str(report)),
        input_text=json.dumps(request),
        cwd=commitlint_runtime.workspace,
    )
    assert invoked.returncode == 0, invoked.stdout + invoked.stderr
    result = json.loads(invoked.stdout)
    assert result["decision"]["status"] == "passed"
    assert result["external_tools"][0]["tool_id"] == "commitlint"
    assert "first valid provenance line removed" in result["evidence"]["data"]
    assert message in result["evidence"]["data"]
    origins = json.loads(report.read_text(encoding="utf-8"))
    reader = Path(origins["mcp_server.services.artifact_header_reader"])
    assert reader.is_relative_to(distribution.root)
    assert all(Path(path).is_relative_to(distribution.root) for path in origins.values())
