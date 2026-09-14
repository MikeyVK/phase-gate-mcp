"""Direct native Pytest and test/v1 adapter conformance in isolated workspaces."""

from __future__ import annotations

import asyncio
import ctypes
import json
import os
import subprocess
import sys
import tomllib
from ctypes import wintypes
from dataclasses import dataclass
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.adapter_manifest import AdapterTrustConfig, TestCapability
from mcp_server.core.interfaces.execution import AdapterBinding
from mcp_server.execution.catalog import AdapterCatalogLoader, FileAdapterPackageReader
from mcp_server.execution.check_selection import SelectionCheckRequest
from mcp_server.execution.models import InvocationCancelled, TextEvidence
from mcp_server.execution.process_runtime import AdapterProcessRuntime, AsyncioProcessBackend
from tests.mcp_server.fixtures.test_role_double import (
    NativeTestResponse,
    NativeTestResult,
    role_response_contract,
)


@dataclass(frozen=True)
class NativeCase:
    workspace: Path
    source: Path
    repo_root: Path


@pytest.fixture
def native_case(tmp_path: Path, pytestconfig: pytest.Config) -> NativeCase:
    workspace = tmp_path / "native workspace"
    workspace.mkdir()
    (workspace / "pytest.ini").write_text(
        "[pytest]\naddopts = -q\ntestpaths = selected\n", encoding="utf-8"
    )
    selected = workspace / "selected"
    selected.mkdir()
    source = selected / "test_native.py"
    source.write_text("def test_pass():\n    assert True\n", encoding="utf-8")
    (workspace / "outside").mkdir()
    (workspace / "outside/test_decoy.py").write_text(
        "def test_decoy():\n    assert False, 'OUTSIDE_DECOY'\n", encoding="utf-8"
    )
    return NativeCase(workspace, source, pytestconfig.rootpath)


def binding_for(case: NativeCase) -> AdapterBinding[TestCapability]:
    loader = ConfigLoader(case.repo_root / ".pgmcp/config", case.repo_root / ".pgmcp/templates")
    catalog = AdapterCatalogLoader(
        case.repo_root / "mcp_server/bundled_adapters",
        case.workspace / "no workspace adapters",
        AdapterTrustConfig(trusted_adapter_ids=()),
        read_manifest=loader.load_adapter_manifest,
        files=FileAdapterPackageReader(),
        resolve_program=lambda name: Path(sys.executable) if name == "python" else None,
        windows=os.name == "nt",
    ).load()
    return catalog.get_test("pytest", "tests")


def native(
    case: NativeCase, targets: list[str], args: list[str]
) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        [sys.executable, "-m", "pytest", *targets, *args],
        cwd=case.workspace,
        capture_output=True,
        timeout=45,
    )


def invoke(
    case: NativeCase, request: dict[str, object], *, isolated: bool = False
) -> tuple[int, NativeTestResponse]:
    binding = binding_for(case)
    command = [str(binding.launch.executable), *(["-S"] if isolated else []), *binding.launch.args]
    result = subprocess.run(
        command,
        input=json.dumps(request).encode(),
        cwd=case.workspace,
        capture_output=True,
        timeout=55,
    )
    schema = json.loads(
        (case.repo_root / "mcp_server/execution/contracts/test_v1.schema.json").read_text()
    )
    Draft202012Validator(schema).validate(json.loads(result.stdout))
    response = NativeTestResponse.model_validate_json(result.stdout)
    return result.returncode, response


@pytest.mark.parametrize(
    ("case_name", "native_code", "wire_code", "status", "token"),
    [
        ("pass", 0, 0, "passed", "1 passed"),
        ("fail", 1, 1, "failed", "FAILURE_DETAIL"),
        ("skip", 0, 0, "passed", "1 skipped"),
        ("collect", 0, 0, "passed", "test_pass"),
        ("empty", 5, 0, "passed", "no tests"),
        ("collection-error", 2, 3, "unavailable", "SyntaxError"),
        ("usage", 4, 3, "unavailable", "unrecognized arguments"),
        ("bad-config", 4, 3, "unavailable", "invalid.toml"),
        ("xdist", 0, 0, "passed", "1 passed"),
        ("literal-rejected", 4, 3, "unavailable", "path cannot contain"),
    ],
    ids=[
        "pass",
        "fail",
        "skip",
        "collect",
        "empty",
        "collection-error",
        "usage",
        "bad-config",
        "xdist",
        "literal-rejected",
    ],
)
def test_native_outcomes_and_options(
    native_case: NativeCase, case_name, native_code, wire_code, status, token
) -> None:
    case = native_case
    args: list[str] = []
    if case_name == "fail":
        case.source.write_bytes(b"def test_fail():\r\n    assert False, 'FAILURE_DETAIL'\r\n")
    elif case_name == "skip":
        case.source.write_text(
            "import pytest\n\ndef test_skip():\n    pytest.skip('native skip')\n", encoding="utf-8"
        )
    elif case_name == "empty":
        case.source.write_text("# no tests\n", encoding="utf-8")
    elif case_name == "collection-error":
        case.source.write_text("def broken(:\n", encoding="utf-8")
    elif case_name == "collect":
        args = ["--collect-only"]
    elif case_name == "usage":
        args = ["--not-a-pytest-option"]
    elif case_name == "bad-config":
        invalid = case.workspace / "invalid.toml"
        invalid.write_text("[invalid\n", encoding="utf-8")
        args = ["-c", str(invalid)]
    elif case_name == "xdist":
        args = ["-n", "2"]
    elif case_name == "literal-rejected":
        renamed = case.source.with_name("test_[literal].py")
        case.source.rename(renamed)
        case = NativeCase(case.workspace, renamed, case.repo_root)
    targets = [str(case.source)]
    direct = native(case, targets, args)
    assert direct.returncode == native_code, (direct.stdout, direct.stderr)
    assert token.lower() in (direct.stdout + direct.stderr).decode().lower()
    code, response = invoke(case, {"operation": "tests", "targets": targets, "args": args})
    assert code == wire_code
    result = response.root
    assert isinstance(result, NativeTestResult)
    assert result.decision.status == status
    assert result.external_tools[0].version == "9.0.2"
    assert isinstance(result.evidence, TextEvidence)
    assert token.lower() in result.evidence.data.lower()
    assert "OUTSIDE_DECOY" not in result.evidence.data
    if case_name == "empty":
        assert "no tests" in result.decision.message.lower()
    if case_name == "bad-config":
        assert result.decision.reason == "invalid_configuration"
        assert not direct.stdout
        assert result.evidence.data == direct.stderr.decode("utf-8", errors="replace")


def test_configured_discovery_and_deliberate_native_expansion(native_case: NativeCase) -> None:
    case = native_case
    for targets, args, code, token in [
        ([], [], 0, "1 passed"),
        ([str(case.source)], [str(case.workspace / "outside")], 1, "OUTSIDE_DECOY"),
    ]:
        direct = native(case, targets, args)
        assert direct.returncode == code
        actual, response = invoke(case, {"operation": "tests", "targets": targets, "args": args})
        assert actual == code
        assert isinstance(response.root, NativeTestResult)
        assert isinstance(response.root.evidence, TextEvidence)
        assert token in response.root.evidence.data


def test_last_failed_and_verbose_traceback_remain_native(native_case: NativeCase) -> None:
    case = native_case
    case.source.write_text(
        "def test_pass():\n    assert True\n\ndef test_bad():\n    assert "
        + repr("x" * 400)
        + " == 'different'\n",
        encoding="utf-8",
    )
    targets = [str(case.source)]
    assert native(case, targets, []).returncode == 1
    args = ["--lf", "-vv", "--tb=long"]
    direct = native(case, targets, args)
    assert direct.returncode == 1 and b"1 deselected" in direct.stdout
    code, response = invoke(case, {"operation": "tests", "targets": targets, "args": args})
    assert code == 1 and isinstance(response.root, NativeTestResult)
    assert isinstance(response.root.evidence, TextEvidence)
    assert "1 deselected" in response.root.evidence.data
    assert "x" * 400 in response.root.evidence.data


def test_native_coverage_is_opt_in_and_owns_threshold_rejection(native_case: NativeCase) -> None:
    case = native_case
    package = case.workspace / "mcp_server"
    package.mkdir()
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "sample.py").write_text(
        "def choose(value):\n    if value:\n        return 1\n    return 2\n", encoding="utf-8"
    )
    case.source.write_text(
        "from mcp_server.sample import choose\n\n"
        "def test_choose():\n    assert choose(True) == 1\n",
        encoding="utf-8",
    )
    configured = tomllib.loads((case.repo_root / "pyproject.toml").read_text(encoding="utf-8"))[
        "tool"
    ]["coverage"]
    assert configured["run"] == {"source": ["mcp_server"], "branch": True}
    assert configured["report"]["fail_under"] == 90
    (case.workspace / "pyproject.toml").write_text(
        '[tool.coverage.run]\nsource = ["mcp_server"]\nbranch = true\n'
        "[tool.coverage.report]\nfail_under = 90\n",
        encoding="utf-8",
    )
    targets = [str(case.source)]
    assert native(case, targets, []).returncode == 0
    assert not (case.workspace / ".coverage").exists()
    code, _ = invoke(case, {"operation": "tests", "targets": targets, "args": []})
    assert code == 0 and not (case.workspace / ".coverage").exists()
    direct = native(case, targets, ["--cov"])
    assert direct.returncode == 1 and b"90" in direct.stdout
    code, response = invoke(case, {"operation": "tests", "targets": targets, "args": ["--cov"]})
    assert code == 1 and isinstance(response.root, NativeTestResult)
    assert isinstance(response.root.evidence, TextEvidence)
    assert "90" in response.root.evidence.data and "sample.py" in response.root.evidence.data


def test_wire_rejection_dependency_and_metadata_only_requests(
    native_case: NativeCase, monkeypatch: pytest.MonkeyPatch
) -> None:
    case = native_case
    request = {"operation": "tests", "targets": [], "args": []}
    for invalid in (
        {**request, "operation": "other"},
        {**request, "scope": "workspace"},
        {**request, "targets": ["relative.py"]},
        {**request, "args": [True]},
    ):
        code, response = invoke(case, invalid)
        assert code == 2 and response.root.reason == "invalid_request"
    code, response = invoke(case, request, isolated=True)
    assert code == 3 and isinstance(response.root, NativeTestResult)
    assert response.root.decision.reason == "dependency_unavailable"
    for args in (["--version"], ["--help"], ["-VV"], ["-qh"]):
        code, response = invoke(case, {**request, "args": args})
        assert code == 3 and isinstance(response.root, NativeTestResult)
        assert response.root.decision.reason == "unsupported_input"
    monkeypatch.setenv("PYTEST_ADDOPTS", "--help")
    assert native(case, [], []).returncode == 0
    code, response = invoke(case, request)
    assert code == 3 and isinstance(response.root, NativeTestResult)
    assert response.root.decision.reason == "unsupported_input"


def is_running(pid: int) -> bool:
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel.OpenProcess.restype = wintypes.HANDLE
    kernel.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    handle = kernel.OpenProcess(0x00100000, False, pid)
    if not handle:
        if ctypes.get_last_error() == 87:
            return False
        raise ctypes.WinError()
    try:
        return kernel.WaitForSingleObject(handle, 0) == 258
    finally:
        kernel.CloseHandle(handle)


@pytest.mark.asyncio
@pytest.mark.skipif(os.name != "nt", reason="Windows process-tree evidence")
async def test_cancellation_stops_native_pytest_descendant(native_case: NativeCase) -> None:
    case = native_case
    child = case.workspace / "child.py"
    child.write_text(
        "import os, pathlib, time\n"
        "pathlib.Path('child.pid').write_text(str(os.getpid()))\ntime.sleep(60)\n",
        encoding="utf-8",
    )
    case.source.write_text(
        "import subprocess, sys, time\n\ndef test_spawn():\n"
        "    subprocess.Popen([sys.executable, 'child.py'], "
        "stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)\n"
        "    time.sleep(60)\n",
        encoding="utf-8",
    )
    task = asyncio.create_task(
        AdapterProcessRuntime(AsyncioProcessBackend()).invoke(
            launch=binding_for(case).launch,
            workspace_root=case.workspace,
            request=SelectionCheckRequest(operation="tests", targets=(str(case.source),), args=()),
            response_contract=role_response_contract(),
            timeout_seconds=20,
        )
    )
    try:
        async with asyncio.timeout(12):
            while not (case.workspace / "child.pid").exists():
                await asyncio.sleep(0.02)
        pid = int((case.workspace / "child.pid").read_text())
        assert is_running(pid)
        task.cancel()
        outcome = await task
        assert isinstance(outcome, InvocationCancelled)
        assert outcome.termination_problem is None
        assert not is_running(pid)
    finally:
        if not task.done():
            task.cancel()
            await task
