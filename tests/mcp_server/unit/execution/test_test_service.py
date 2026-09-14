"""Public service behavior for test bindings, typed facts and bounded stops."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from mcp_server.config.schemas.adapter_manifest import TestCapability as Capability
from mcp_server.config.schemas.tests_config import TestsConfig as Config
from mcp_server.core.interfaces.execution import (
    AdapterBinding,
    AdapterLaunch,
    AdapterPackageIdentity,
)
from mcp_server.execution.check_selection import FileScopePaths
from mcp_server.execution.test_service import (
    TestRunManager as RunManager,
    TestSelectionRequest as Selection,
)
from tests.mcp_server.fixtures.test_role_double import RecordingTestRuntime


class Catalog:
    @property
    def tests(self) -> tuple[AdapterBinding[Capability], ...]:
        return tuple(self.get_test(name, "suite") for name in ("alpha", "beta"))

    def get_test(self, adapter_id: str, capability: str) -> AdapterBinding[Capability]:
        return AdapterBinding(
            AdapterPackageIdentity(adapter_id, "1.0.0", "a" * 64),
            capability,
            1,
            AdapterLaunch(Path("C:/adapter/python.exe"), (adapter_id,)),
            Capability(),
        )


def configuration() -> Config:
    return Config.model_validate(
        {"tests": {
            name: {
                "adapter_id": adapter,
                "capability": "suite",
                "timeout_seconds": budget,
                "default_args": ["--label", "two words", ""],
                "active": active,
            }
            for name, adapter, budget, active in (
                ("first", "alpha", 10, True),
                ("second", "beta", 20, True),
                ("manual", "alpha", 30, False),
            )
        }}
    )


def passed() -> tuple[bytes, int]:
    return json.dumps({
        "decision": {"status": "passed", "message": "Native collection succeeded."},
        "external_tools": [],
    }).encode(), 0


@pytest.mark.asyncio
async def test_configured_selection_keeps_order_args_and_native_empty_scope(tmp_path: Path) -> None:
    runtime = RecordingTestRuntime((passed(), passed()))
    manager = RunManager(configuration(), Catalog(), runtime, FileScopePaths(tmp_path))
    output = await manager.run(Selection(scope="configured", args={"second": []}))
    assert output.success and output.error_code is None
    assert output.selected_tests == ("first", "second")
    assert [call.request.model_dump() for call in runtime.calls] == [
        {"operation": "suite", "targets": (), "args": ("--label", "two words", "")},
        {"operation": "suite", "targets": (), "args": ()},
    ]
    assert [call.timeout_seconds for call in runtime.calls] == [10, 20]
    assert [(row.args_source, row.effective_args) for row in output.results] == [
        ("configured", ("--label", "two words", "")), ("caller", ()),
    ]
    assert output.results[0].message == "Native collection succeeded."
    assert output.results[0].evidence is None
    assert output.results[0].external_tools == ()
    assert "evidence" in output.model_dump()["results"][0]
