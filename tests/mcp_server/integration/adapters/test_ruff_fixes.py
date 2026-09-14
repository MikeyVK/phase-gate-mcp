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
    RuffPackage,
    decision,
    evidence_text,
    invoke,
    ruff_package,
)

__all__ = ["ruff_package"]


def fix_package(base: RuffPackage, repo: Path) -> RuffPackage:
    loader = ConfigLoader(base.workspace / "config", base.workspace / "templates")
    catalog = AdapterCatalogLoader(
        base.root.parent,
        base.workspace / "adapters",
        AdapterTrustConfig(trusted_adapter_ids=()),
        read_manifest=loader.load_adapter_manifest,
        files=FileAdapterPackageReader(),
        resolve_program=lambda name: Path(sys.executable) if name == "python" else None,
        windows=os.name == "nt",
    ).load()
    binding = catalog.get_fix("ruff", "format")
    for operation in ("format", "lint"):
        fix = catalog.get_fix("ruff", operation)
        assert [
            (address.adapter_id, address.capability) for address in fix.capability.addresses
        ] == [("ruff", operation)]
        assert fix.identity == catalog.get_check("ruff", operation).identity
    schema = repo / "mcp_server/execution/contracts/fix_v1.schema.json"
    return RuffPackage(
        binding.launch,
        base.root,
        base.workspace,
        Draft202012Validator(json.loads(schema.read_text(encoding="utf-8"))),
    )


def native_fix(
    workspace: Path,
    operation: str,
    target: Path,
    args: tuple[str, ...] = (),
) -> subprocess.CompletedProcess[bytes]:
    controls = ["format"] if operation == "format" else ["check", "--fix"]
    return subprocess.run(
        [sys.executable, "-m", "ruff", *controls, *args, "--", str(target)],
        cwd=workspace,
        capture_output=True,
        timeout=15,
    )


def test_native_format_changes_only_selected_file(
    ruff_package: RuffPackage,
    pytestconfig: pytest.Config,
) -> None:
    base = ruff_package
    target = base.workspace / "selected with spaces.py"
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


@pytest.mark.parametrize(
    ("operation", "before", "args", "native_code", "changed"),
    [
        ("format", b"value = 1\n", (), 0, False),
        ("lint", b"import os\r\n", ("--select", "F401"), 0, True),
        ("lint", b"import os\nunknown_name\n", ("--output-format", "json"), 1, True),
        ("lint", b"unknown_name\n", ("--exit-zero",), 0, False),
    ],
    ids=["format-noop", "lint-fix", "partial-failure", "native-exit-zero"],
)
def test_native_fix_results_and_partial_mutation(
    ruff_package: RuffPackage,
    pytestconfig: pytest.Config,
    operation: str,
    before: bytes,
    args: tuple[str, ...],
    native_code: int,
    changed: bool,
) -> None:
    package = fix_package(ruff_package, pytestconfig.rootpath)
    target = package.workspace / "native.py"
    target.write_bytes(before)
    direct = native_fix(package.workspace, operation, target, args)
    expected = target.read_bytes()
    assert direct.returncode == native_code and (expected != before) == changed
    target.write_bytes(before)
    code, result = invoke(package, operation, (target,), args)
    assert code == native_code and decision(result)["status"] == (
        "failed" if native_code else "passed"
    )
    assert target.read_bytes() == expected
    for stream in (direct.stdout, direct.stderr):
        if stream:
            assert stream.decode("utf-8") in evidence_text(result)
    assert result["external_tools"] == [{"tool_id": "ruff", "version": "0.15.6"}]
    assert "coverage" not in result and "required_targets" not in result


def test_extra_sources_and_conflicting_options_are_refused_before_writes(
    ruff_package: RuffPackage,
    pytestconfig: pytest.Config,
) -> None:
    package = fix_package(ruff_package, pytestconfig.rootpath)
    target = package.workspace / "selected.py"
    other = package.workspace / "outside.py"
    before = b"import os\n"
    target.write_bytes(before)
    other.write_bytes(before)
    direct = native_fix(package.workspace, "lint", target, (str(other),))
    assert direct.returncode == 0 and other.read_bytes() != before
    target.write_bytes(before)
    other.write_bytes(before)
    for args in (
        (str(other),),
        ("--", str(other)),
        ("--select", "F401", str(other)),
        ("@hidden-args",),
        ("--select", "@hidden-args"),
        ("--no-fix",),
        ("--diff",),
        ("--show-files",),
        ("--show-settings",),
        ("--output-file", str(other)),
        ("-o" + str(other),),
        ("--stdin-filename", str(other)),
        ("--help",),
        ("-vh",),
        ("--watch",),
    ):
        code, result = invoke(package, "lint", (target,), args)
        assert code == 3 and decision(result)["reason"] == "unsupported_input"
        assert target.read_bytes() == before and other.read_bytes() == before


def test_complete_target_and_wire_admission_before_native_dependency(
    ruff_package: RuffPackage,
    pytestconfig: pytest.Config,
) -> None:
    package = fix_package(ruff_package, pytestconfig.rootpath)
    target = package.workspace / "valid.py"
    target.write_bytes(b"import os\n")
    for extra in (package.workspace, package.workspace / "missing.py"):
        code, response = invoke(package, "lint", (target, extra))
        assert code == 3 and decision(response)["reason"] == "unsupported_input"
        assert target.read_bytes() == b"import os\n"
    request = {"operation": "lint", "targets": [str(target)], "args": []}
    for malformed in (
        {**request, "targets": []},
        {**request, "targets": None},
        {**request, "targets": ["relative.py"]},
        *(
            {**request, "targets": [path]}
            for path in (
                "/",
                "C:/",
                str(package.workspace) + "/",
                str(package.workspace) + "/.",
                str(package.workspace) + "/..",
            )
        ),
        {**request, "args": [False]},
        {**request, "operation": "other"},
        {**request, "scope": "workspace"},
    ):
        code, response = invoke(package, "lint", raw=json.dumps(malformed).encode())
        assert code == 2 and response["reason"] == "invalid_request"
    without_dependency = subprocess.run(
        [sys.executable, "-S", *package.launch.args],
        input=json.dumps(request).encode(),
        cwd=package.workspace,
        capture_output=True,
        timeout=15,
    )
    result = json.loads(without_dependency.stdout)
    package.schema.validate(result)
    assert without_dependency.returncode == 3
    assert result["decision"]["reason"] == "dependency_unavailable"
    assert target.read_bytes() == b"import os\n"


@pytest.mark.parametrize("case", ["config", "usage"])
def test_native_inability_preserves_diagnostics_without_mutation(
    ruff_package: RuffPackage,
    pytestconfig: pytest.Config,
    case: str,
) -> None:
    package = fix_package(ruff_package, pytestconfig.rootpath)
    target = package.workspace / "selected.py"
    before = b"import os\n"
    target.write_bytes(before)
    if case == "config":
        (package.workspace / "ruff.toml").write_text("invalid [", encoding="utf-8")
        args: tuple[str, ...] = ()
        reason = "invalid_configuration"
    else:
        args = ("--not-a-ruff-option",)
        reason = "unsupported_input"
    direct = native_fix(package.workspace, "lint", target, args)
    assert direct.returncode == 2
    code, response = invoke(package, "lint", (target,), args)
    assert code == 3 and decision(response)["reason"] == reason
    assert direct.stderr.decode("utf-8") in evidence_text(response)
    assert target.read_bytes() == before


def test_inherited_output_destination_cannot_redirect_fix_evidence(
    ruff_package: RuffPackage,
    pytestconfig: pytest.Config,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    package = fix_package(ruff_package, pytestconfig.rootpath)
    target = package.workspace / "selected.py"
    target.write_bytes(b"import os\n")
    output = package.workspace / "external-output.txt"
    monkeypatch.setenv("RUFF_OUTPUT_FILE", str(output))
    code, response = invoke(package, "lint", (target,))
    assert code == 3 and decision(response)["reason"] == "unsupported_input"
    assert target.read_bytes() == b"import os\n" and not output.exists()
