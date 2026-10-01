"""Public service behavior for test bindings, typed facts and bounded stops."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TypeVar

import pytest
from pydantic import BaseModel, ValidationError

from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.adapter_manifest import AdapterTrustConfig
from mcp_server.config.schemas.adapter_manifest import TestCapability as Capability
from mcp_server.config.schemas.tests_config import TestsConfig as Config
from mcp_server.config.validator import ConfigValidator
from mcp_server.core.exceptions import ConfigError
from mcp_server.core.interfaces.execution import (
    AdapterBinding,
    AdapterLaunch,
    AdapterPackageIdentity,
)
from mcp_server.execution.catalog import AdapterCatalogLoader, FileAdapterPackageReader
from mcp_server.execution.check_selection import FileScopePaths
from mcp_server.execution.models import (
    AdapterCallFailure,
    AdapterCallFailureReason,
    InvocationCancelled,
    InvocationCompleted,
    InvocationFailed,
    ProcessCapture,
    PublicTestResult,
    RejectedTestRequestDetails,
    RunTestsOutput,
    ScopeDetails,
    StreamCapture,
    TerminationProblem,
    TextEvidence,
)
from mcp_server.execution.models import (
    TestRoleResponse as RoleResponse,
)
from mcp_server.execution.models import (
    TestTerminationDetails as TerminationDetails,
)
from mcp_server.execution.process_runtime import AdapterProcessRuntime
from mcp_server.execution.protocol import AdapterResponseContract
from mcp_server.execution.test_service import (
    TestRunManager as RunManager,
)
from mcp_server.execution.test_service import (
    TestSelectionRequest as Selection,
)
from tests.mcp_server.fixtures.test_role_double import RecordingTestRuntime


class Catalog:
    @property
    def tests(self) -> tuple[AdapterBinding[Capability], ...]:
        return tuple(self.get_test(name, "suite") for name in ("alpha", "beta"))

    def get_test(self, adapter_id: str, capability: str) -> AdapterBinding[Capability]:
        return AdapterBinding(
            AdapterPackageIdentity(adapter_id, "1.0.0", "a" * 16),
            capability,
            1,
            AdapterLaunch(Path("C:/adapter/python.exe"), (adapter_id,)),
            Capability(),
        )


def configuration() -> Config:
    return Config.model_validate(
        {
            "tests": {
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
            }
        }
    )


def passed() -> tuple[bytes, int]:
    return json.dumps(
        {
            "decision": {"status": "passed", "message": "Native collection succeeded."},
            "external_tools": [],
        }
    ).encode(), 0


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
        ("configured", ("--label", "two words", "")),
        ("caller", ()),
    ]
    assert output.results[0].message == "Native collection succeeded."
    assert output.results[0].evidence is None
    assert output.results[0].external_tools == ()
    assert "evidence" in output.model_dump()["results"][0]


@pytest.mark.asyncio
@pytest.mark.parametrize("scope", ["workspace", "targets"])
async def test_explicit_inactive_selection_scope_and_budget(tmp_path: Path, scope: str) -> None:
    source = tmp_path / "input with spaces.py"
    source.write_text("# input", encoding="utf-8")
    request = Selection.model_validate(
        {
            "scope": scope,
            "tests": ["manual", "first"],
            "args": {"manual": ["a b", ""]},
            "timeout_seconds": 7,
            **({"targets": [source.name]} if scope == "targets" else {}),
        }
    )
    runtime = RecordingTestRuntime((passed(), passed()))
    output = await RunManager(configuration(), Catalog(), runtime, FileScopePaths(tmp_path)).run(
        request
    )
    expected = str(source) if scope == "targets" else str(tmp_path)
    assert output.selected_tests == ("manual", "first")
    assert output.requested_targets == ((source.name,) if scope == "targets" else ())
    assert [call.request.model_dump()["targets"] for call in runtime.calls] == [
        (expected,),
        (expected,),
    ]
    assert [call.timeout_seconds for call in runtime.calls] == [7, 7]
    assert output.results[0].effective_args == ("a b", "")
    assert output.results[1].effective_args == ("--label", "two words", "")


@pytest.mark.asyncio
async def test_selection_failures_are_explicit_and_launch_nothing(tmp_path: Path) -> None:
    empty = Config.model_validate({"tests": {}})
    inactive = Config(tests=(("manual", dict(configuration().tests)["manual"]),))
    for config, request, expected in (
        (empty, Selection(scope="configured"), "no_configured_tests"),
        (inactive, Selection(scope="configured"), "no_active_tests"),
        (configuration(), Selection(scope="workspace", tests=["unknown"]), "selection_invalid"),
        (configuration(), Selection(scope="configured", args={"unknown": []}), "selection_invalid"),
        (configuration(), Selection(scope="configured", args={"manual": []}), "selection_invalid"),
    ):
        runtime = RecordingTestRuntime(())
        output = await RunManager(config, Catalog(), runtime, FileScopePaths(tmp_path)).run(request)
        assert output.success and output.error_code == expected
        assert output.results == () and not runtime.calls
        assert RunTestsOutput.model_validate_json(output.model_dump_json()) == output


def test_public_selection_rejects_legacy_fields_nulls_and_root_aliases() -> None:
    for fields in (
        {"scope": "branch"},
        {"scope": "targets"},
        {"scope": "targets", "targets": []},
        {"scope": "workspace", "targets": ["input.py"]},
        *({"scope": "targets", "targets": [root]} for root in (".", "./", ".//.")),
        *(
            {"scope": "configured", key: None}
            for key in ("targets", "tests", "args", "timeout_seconds")
        ),
        {"scope": "configured", "tests": ["first", "first"]},
        {"scope": "configured", "timeout_seconds": True},
        {"scope": "configured", "args": {"first": [True]}},
        {"scope": "configured", "coverage": True},
    ):
        with pytest.raises(ValidationError):
            Selection.model_validate(fields)


@pytest.mark.asyncio
async def test_all_paths_resolve_before_any_native_launch(tmp_path: Path) -> None:
    existing = tmp_path / "valid.py"
    existing.write_text("# valid", encoding="utf-8")
    runtime = RecordingTestRuntime(())
    request = Selection(scope="targets", targets=[existing.name, "missing.py"])
    output = await RunManager(configuration(), Catalog(), runtime, FileScopePaths(tmp_path)).run(
        request
    )
    assert output.success and output.error_code == "scope_resolution_failed"
    assert isinstance(output.error_details, ScopeDetails)
    assert output.error_details.issues[0].target == "missing.py"
    assert output.error_details.issues[0].reason == "missing"
    assert not runtime.calls
    assert [row.reason for row in output.results] == ["not_started", "not_started"]
    assert all(row.adapter is None and row.capture is None for row in output.results)


@pytest.mark.asyncio
async def test_native_results_keep_meaning_without_aggregate_verdict(tmp_path: Path) -> None:
    negative = {
        "decision": {"status": "failed", "message": "Native threshold rejected."},
        "external_tools": [{"tool_id": "engine", "version": "2.0"}],
        "evidence": {"format": "json", "data": {"native": [0, False, "detail"]}},
    }
    unavailable = {
        "decision": {
            "status": "unavailable",
            "reason": "unsupported_input",
            "message": "Native usage error.",
        },
        "external_tools": [],
        "evidence": {"format": "text", "data": "line one\r\nline two"},
    }
    runtime = RecordingTestRuntime(
        (
            passed(),
            (json.dumps(negative).encode(), 1),
            (json.dumps(unavailable).encode(), 3),
        )
    )
    output = await RunManager(configuration(), Catalog(), runtime, FileScopePaths(tmp_path)).run(
        Selection(scope="configured", tests=["first", "second", "manual"])
    )
    assert output.success and output.error_code is None and len(runtime.calls) == 3
    assert [row.status for row in output.results] == ["passed", "failed", "unavailable"]
    assert output.results[1].evidence is not None
    assert output.results[1].evidence.model_dump(mode="json") == negative["evidence"]
    assert output.results[2].evidence == TextEvidence(format="text", data="line one\r\nline two")
    assert output.results[0].evidence is None and output.results[0].external_tools == ()
    restored = RunTestsOutput.model_validate_json(output.model_dump_json())
    assert restored == output
    for field in ("evidence", "reason", "termination_problem", "request_rejection"):
        assert field in output.model_dump()["results"][0]
    assert "run_status" not in output.model_dump()
    for change in (
        {"evidence": None},
        {"evidence": {"format": "text", "data": "   "}},
        {"external_tools": None},
        {"reason": "not_started"},
        {"capture": None},
    ):
        with pytest.raises(ValidationError):
            PublicTestResult.model_validate({**output.results[1].model_dump(), **change})
    with pytest.raises(ValidationError):
        RunTestsOutput.model_validate({**output.model_dump(), "error_code": "selection_invalid"})
    for change in ({"evidence": None}, {"decision": {"status": "collected", "message": "x"}}):
        with pytest.raises(ValidationError):
            RoleResponse.model_validate_json(json.dumps({**negative, **change}))


TResponse = TypeVar("TResponse", bound=BaseModel)


class InterruptedRuntime(AdapterProcessRuntime):
    """Inject an existing runtime fact between two accepted native results."""

    def __init__(self, fault: InvocationFailed | InvocationCancelled) -> None:
        self.fault = fault
        self.native = RecordingTestRuntime((passed(), passed()))
        self.calls = 0

    async def invoke(
        self,
        *,
        launch: AdapterLaunch,
        workspace_root: Path,
        request: BaseModel,
        response_contract: AdapterResponseContract[TResponse],
        timeout_seconds: float,
    ) -> InvocationCompleted[TResponse] | InvocationFailed | InvocationCancelled:
        self.calls += 1
        if self.calls == 2:
            return self.fault
        return await self.native.invoke(
            launch=launch,
            workspace_root=workspace_root,
            request=request,
            response_contract=response_contract,
            timeout_seconds=timeout_seconds,
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("kind", "unconfirmed", "expected"),
    [
        ("failed", False, None),
        ("failed", True, "termination_unconfirmed"),
        ("cancelled", False, "operation_interrupted"),
        ("cancelled", True, "termination_unconfirmed"),
    ],
)
async def test_shared_failure_and_cancellation_preserve_partial_results(
    tmp_path: Path,
    kind: str,
    unconfirmed: bool,
    expected: str | None,
) -> None:
    stream = StreamCapture(observed_bytes=4, head="head", tail="", truncated=False)
    capture = ProcessCapture(exit_code=None, stdout=stream, stderr=stream)
    termination = TerminationProblem.UNCONFIRMED if unconfirmed else None
    fault = (
        InvocationFailed(
            outcome="failed",
            capture=capture,
            termination_problem=termination,
            failure=AdapterCallFailure(
                reason=AdapterCallFailureReason.TIMEOUT, message="Budget expired."
            ),
        )
        if kind == "failed"
        else InvocationCancelled(
            outcome="cancelled", capture=capture, termination_problem=termination
        )
    )
    runtime = InterruptedRuntime(fault)
    output = await RunManager(configuration(), Catalog(), runtime, FileScopePaths(tmp_path)).run(
        Selection(scope="configured", tests=["first", "second", "manual"])
    )
    assert output.success and output.error_code == expected
    assert output.results[0].status == "passed"
    assert output.results[1].capture == capture and output.results[1].adapter is not None
    assert output.results[1].external_tools is None and output.results[1].evidence is None
    assert output.results[1].reason == ("timeout" if kind == "failed" else "interrupted")
    assert output.results[1].termination_problem == (termination if kind == "failed" else None)
    assert runtime.calls == (2 if expected else 3)
    assert output.results[2].reason == ("not_started" if expected else None)
    if unconfirmed:
        assert isinstance(output.error_details, TerminationDetails)
        assert output.error_details.test_ids == ("second",)
        assert output.error_details.interrupted == (kind == "cancelled")
        for changed_details in (
            {"test_ids": ("first",), "interrupted": kind == "cancelled"},
            {"test_ids": ("second",), "interrupted": kind != "cancelled"},
        ):
            with pytest.raises(ValidationError):
                RunTestsOutput.model_validate(
                    {
                        **output.model_dump(),
                        "error_details": changed_details,
                    }
                )
    if expected:
        with pytest.raises(ValidationError):
            RunTestsOutput.model_validate(
                {
                    **output.model_dump(),
                    "error_code": None,
                    "error_details": None,
                }
            )
    assert RunTestsOutput.model_validate_json(output.model_dump_json()) == output


@pytest.mark.asyncio
async def test_internal_rejection_stops_and_is_operational_failure(tmp_path: Path) -> None:
    rejected = {
        "reason": "invalid_request",
        "details": [{"location": ["args"], "code": "wrong_type"}],
    }
    runtime = RecordingTestRuntime((passed(), (json.dumps(rejected).encode(), 2)))
    output = await RunManager(configuration(), Catalog(), runtime, FileScopePaths(tmp_path)).run(
        Selection(scope="configured", tests=["first", "second", "manual"])
    )
    assert not output.success and output.error_code == "adapter_request_rejected"
    assert isinstance(output.error_details, RejectedTestRequestDetails)
    assert output.error_details.test_id == "second"
    assert [row.status for row in output.results] == ["passed", "not_executed", "not_executed"]
    assert output.results[1].reason == "invalid_request"
    assert output.results[1].request_rejection is not None
    assert output.results[1].request_rejection[0].location == ("args",)
    assert output.results[1].capture is not None
    assert output.results[1].capture.exit_code == 2
    assert output.results[2].reason == "not_started" and output.results[2].adapter is None
    assert len(runtime.calls) == 2
    with pytest.raises(ValidationError):
        RunTestsOutput.model_validate(
            {
                **output.model_dump(),
                "success": True,
                "error_code": None,
                "error_details": None,
            }
        )


def test_required_config_loads_strictly_and_validates_catalog_without_launch(
    tmp_path: Path,
    pytestconfig: pytest.Config,
) -> None:
    root = pytestconfig.rootpath
    loader = ConfigLoader(tmp_path, root / ".pgmcp/templates")
    authored = (root / ".pgmcp/config/tests.yaml").read_text(encoding="utf-8")
    config_file = tmp_path / "tests.yaml"
    with pytest.raises(ConfigError):
        loader.load_tests_config()
    config_file.write_text(authored, encoding="utf-8")
    config = loader.load_tests_config()
    binding = dict(config.tests)["python_tests"]
    assert (binding.adapter_id, binding.capability, binding.default_args, binding.active) == (
        "pytest",
        "tests",
        (),
        True,
    )
    catalog = AdapterCatalogLoader(
        root / "mcp_server/bundled_adapters",
        tmp_path / "adapters",
        AdapterTrustConfig(trusted_adapter_ids=()),
        read_manifest=loader.load_adapter_manifest,
        files=FileAdapterPackageReader(),
        resolve_program=lambda _name: None,
        windows=True,
    ).load()
    ConfigValidator().validate_tests_config(config, catalog)
    assert catalog.get_test("pytest", "tests").launch.executable is None
    for replacement in (
        authored.replace("active: true", "active: 1"),
        authored.replace("timeout_seconds: 300", "timeout_seconds: true"),
        authored.replace("default_args: []", "default_args: [true]"),
        authored.replace("    active: true", "    active: true\n    active: false"),
        authored.replace("    active: true", "    active: true\n    parser: legacy"),
    ):
        config_file.write_text(replacement, encoding="utf-8")
        with pytest.raises(ConfigError):
            loader.load_tests_config()
    for adapter, capability in (("unknown", "tests"), ("python", "syntax"), ("pytest", "unknown")):
        changed = config.model_dump()
        changed["tests"]["python_tests"].update(adapter_id=adapter, capability=capability)
        with pytest.raises(ConfigError):
            ConfigValidator().validate_tests_config(Config.model_validate(changed), catalog)
