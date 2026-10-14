# tests/mcp_server/unit/core/test_tool_factory.py
# template=unit_test version=3d15d309 created=2026-06-19T22:38Z updated=
"""Behavior tests for ToolFactory's public execution pipeline."""

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, call

import pytest
from pydantic import BaseModel, ConfigDict

from mcp_server.core.exceptions import ConfigError, MCPError
from mcp_server.core.interfaces.icore_tool import ICoreTool
from mcp_server.core.operation_notes import NoteContext
from mcp_server.core.tool_factory import ToolFactory
from mcp_server.managers.enforcement_runner import EnforcementRunner
from mcp_server.schemas.error_outputs import (
    ConfigErrorOutput,
    ExecutionErrorOutput,
    ValidationErrorOutput,
)


class FactoryInput(BaseModel):
    """A typed input whose validation is observable at the factory boundary."""

    model_config = ConfigDict(frozen=True)
    value: int


class FactoryOutput(BaseModel):
    """The value returned by the core test double."""

    model_config = ConfigDict(frozen=True)
    value: int


class TestToolFactory:
    """Public execution proves validation, enforcement and error handling."""

    @pytest.mark.parametrize(
        "failure",
        [
            ValueError("execution failed"),
            ConfigError("invalid config", file_path="settings.yaml"),
            MCPError("domain rejection", code="domain_rejected", params={"value": "domain fact"}),
        ],
    )
    @pytest.mark.asyncio
    async def test_create_tool_executes_public_pipeline(self, failure: Exception) -> None:
        """Validate before policies, run policies around the core, and convert failures."""
        runner = MagicMock(spec=EnforcementRunner)
        root = Path("mock/workspace/root")
        core = MagicMock(spec=ICoreTool)
        core.name = "mock_tool"
        core.description = "mock description"
        core.args_model = FactoryInput
        core.enforcement_event = "mock_tool"
        core.tool_category = None
        output = FactoryOutput(value=3)
        core.execute = AsyncMock(return_value=output)
        pipeline = MagicMock()
        pipeline.attach_mock(runner.run, "policy")
        pipeline.attach_mock(core.execute, "execute")
        decorated = ToolFactory(runner, root).create_tool(core)
        context = NoteContext()

        rejected = await decorated.execute({"value": "invalid"}, context)
        assert isinstance(rejected.operation, ValidationErrorOutput)
        runner.run.assert_not_called()
        core.execute.assert_not_awaited()

        accepted = await decorated.execute({"value": 3}, context)
        assert accepted.operation == output
        assert [entry[0] for entry in pipeline.mock_calls] == ["policy", "execute", "policy"]
        core.execute.assert_awaited_once_with(FactoryInput(value=3), context)
        assert runner.run.call_count == 2
        for policy_call, timing in zip(runner.run.call_args_list, ("pre", "post"), strict=True):
            assert policy_call.kwargs["event"] == "mock_tool"
            assert policy_call.kwargs["timing"] == timing
            enforcement_context = policy_call.kwargs["enforcement_ctx"]
            assert enforcement_context.workspace_root == root
            assert enforcement_context.params == FactoryInput(value=3)

        core.execute.side_effect = failure
        failed = await decorated.execute({"value": 3}, context)
        diagnostic = failed.operation
        assert isinstance(diagnostic, (ExecutionErrorOutput, ConfigErrorOutput))
        assert diagnostic.params == {"value": 3}
        assert diagnostic.traceback is not None
        assert type(failure).__name__ in diagnostic.traceback
        if isinstance(failure, MCPError):
            assert diagnostic.error_code == failure.code
            assert diagnostic.error_params == failure.params
        if isinstance(failure, ConfigError):
            assert isinstance(diagnostic, ConfigErrorOutput)
            assert diagnostic.file_path == "settings.yaml"
        assert pipeline.mock_calls[-1] == call.execute(FactoryInput(value=3), context)
