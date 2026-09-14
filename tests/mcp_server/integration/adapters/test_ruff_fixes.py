"""Native Ruff fix/v1 conformance with independently observed file effects."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.adapter_manifest import AdapterTrustConfig
from mcp_server.execution.catalog import AdapterCatalogLoader, FileAdapterPackageReader
from tests.mcp_server.integration.adapters.test_ruff_checks import (
    RuffPackage, decision, evidence_text, invoke, ruff_package as ruff_package,
)


def fix_package(base: RuffPackage, repo: Path) -> RuffPackage:
    loader = ConfigLoader(base.workspace / "config", base.workspace / "templates")
    catalog = AdapterCatalogLoader(
        base.root.parent, base.workspace / "adapters", AdapterTrustConfig(trusted_adapter_ids=()),
        read_manifest=loader.load_adapter_manifest, files=FileAdapterPackageReader(),
        resolve_program=lambda name: Path(sys.executable) if name == "python" else None,
        windows=os.name == "nt",
    ).load()
    binding = catalog.get_fix("ruff", "format")
    for operation in ("format", "lint"):
        fix = catalog.get_fix("ruff", operation)
        assert [(address.adapter_id, address.capability) for address in fix.capability.addresses] == [
            ("ruff", operation)
        ]
        assert fix.identity == catalog.get_check("ruff", operation).identity
    schema = repo / "mcp_server/execution/contracts/fix_v1.schema.json"
    return RuffPackage(
        binding.launch, base.root, base.workspace,
        Draft202012Validator(json.loads(schema.read_text(encoding="utf-8"))),
    )


def native_fix(
    workspace: Path, operation: str, target: Path, args: tuple[str, ...] = (),
) -> subprocess.CompletedProcess[bytes]:
    controls = ["format"] if operation == "format" else ["check", "--fix"]
    return subprocess.run(
        [sys.executable, "-m", "ruff", *controls, *args, "--", str(target)],
        cwd=workspace, capture_output=True, timeout=15,
    )


def test_native_format_changes_only_selected_file(
    ruff_package: RuffPackage, pytestconfig: pytest.Config,
) -> None:
    base = ruff_package
    target = base.workspace / "selected.py"
    decoy = base.workspace / "decoy.py"
    before = b"value=1\n"
    target.write_bytes(before)
    decoy.write_bytes(before)
    direct = native_fix(base.workspace, "format", target)
    assert direct.returncode == 0
    expected = target.read_bytes()
    assert expected != before
    target.write_bytes(before)
    package = fix_package(base, pytestconfig.rootpath)
    code, result = invoke(package, "format", (target,))
    assert code == 0 and decision(result) == {"status": "passed"}
    assert target.read_bytes() == expected and decoy.read_bytes() == before
    assert direct.stdout.decode() in evidence_text(result)
