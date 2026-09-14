"""Ordered fixes preserve native mutation and stop before later work."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import TypeVar

import pytest
from pydantic import BaseModel

from mcp_server.config.schemas.adapter_manifest import FixCapability
from mcp_server.core.interfaces.execution import AdapterBinding, AdapterLaunch, AdapterPackageIdentity
from mcp_server.execution.check_selection import FileScopePaths
from mcp_server.execution.models import InvocationCompleted, ProcessCapture, StreamCapture
from mcp_server.execution.process_runtime import AdapterProcessRuntime
from mcp_server.execution.protocol import AdapterResponseContract

TResponse = TypeVar("TResponse", bound=BaseModel)


class Catalog:
    @property
    def fixes(self) -> tuple[AdapterBinding[FixCapability], ...]:
        return tuple(self.get_fix(name, "repair") for name in ("alpha", "beta"))

    def get_fix(self, adapter_id: str, capability: str) -> AdapterBinding[FixCapability]:
        return AdapterBinding(
            AdapterPackageIdentity(adapter_id, "1.0.0", "a" * 16), capability, 1,
            AdapterLaunch(Path("C:/adapter/python.exe"), (adapter_id,)),
            FixCapability.model_validate({"addresses": []}),
        )


@dataclass(frozen=True)
class Call:
    launch: AdapterLaunch
    workspace_root: Path
    request: BaseModel
    timeout_seconds: float


class RecordingRuntime(AdapterProcessRuntime):
    def __init__(self, answers: tuple[tuple[bytes, int], ...]) -> None:
        self.answers = iter(answers)
        self.calls: list[Call] = []

    async def invoke(
        self, *, launch: AdapterLaunch, workspace_root: Path, request: BaseModel,
        response_contract: AdapterResponseContract[TResponse], timeout_seconds: float,
    ) -> InvocationCompleted[TResponse]:
        self.calls.append(Call(launch, workspace_root, request, timeout_seconds))
        raw, code = next(self.answers)
        empty = StreamCapture(observed_bytes=0, head="", tail="", truncated=False)
        capture = ProcessCapture(
            exit_code=code,
            stdout=StreamCapture(observed_bytes=len(raw), head=None, tail=None, truncated=False),
            stderr=empty,
        )
        return response_contract.complete(response_contract.decode(raw, code), capture)


def passed() -> tuple[bytes, int]:
    return json.dumps({"decision": {"status": "passed"}, "external_tools": []}).encode(), 0


@pytest.mark.asyncio
async def test_explicit_order_args_and_noop_continue(tmp_path: Path) -> None:
    from mcp_server.config.schemas.fixes_config import FixesConfig
    from mcp_server.execution.fix_service import FixManager, FixSelectionRequest

    config = FixesConfig.model_validate({
        "fixes": {
            name: {"adapter_id": adapter, "capability": "repair",
                   "timeout_seconds": budget, "default_args": ["two words", ""]}
            for name, adapter, budget in (("first", "alpha", 10), ("second", "beta", 20))
        }
    })
    source = tmp_path / "input with spaces.py"
    source.write_bytes(b"# native no-op\n")
    runtime = RecordingRuntime((passed(), passed()))
    output = await FixManager(config, Catalog(), runtime, FileScopePaths(tmp_path)).run(
        FixSelectionRequest(scope="targets", targets=[source.name, "./" + source.name],
                            fixes=["second", "first"], args={"second": []})
    )
    assert output.success and output.error_code is None
    assert output.selected_fixes == ("second", "first")
    assert [call.request.model_dump() for call in runtime.calls] == [
        {"operation": "repair", "targets": (str(source),), "args": ()},
        {"operation": "repair", "targets": (str(source),), "args": ("two words", "")},
    ]
    assert [call.timeout_seconds for call in runtime.calls] == [20, 10]
    assert [row.args_source for row in output.results] == ["caller", "configured"]
    assert all(row.status == "passed" and row.message is None for row in output.results)
    assert output.results[0].evidence is None and output.results[0].external_tools == ()
    assert source.read_bytes() == b"# native no-op\n"
