# tests/mcp_server/integration/test_prepared_tool_contract.py
# template=integration_test version=c2e61372 created=2026-09-13T17:49Z updated=
"""Prepared input flows through real registration, wrappers and schema presentation."""

from __future__ import annotations

import json
from dataclasses import FrozenInstanceError
from pathlib import Path
from typing import Literal

import pytest
from mcp.types import ListToolsRequest, ListToolsResult
from pydantic import BaseModel, ConfigDict, JsonValue, create_model

from mcp_server.config.settings import ServerSettings, Settings
from mcp_server.core.decorators import InputValidationDecorator, ToolErrorHandlerDecorator
from mcp_server.core.interfaces.template_catalog import FrozenJsonObject, freeze_json, thaw_json
from mcp_server.core.interfaces.tool_input_contract import (
    IToolInputContract,
    PreparedToolInputContract,
    prepare_model_input,
)
from mcp_server.core.operation_notes import NoteContext
from mcp_server.presenters.validation_resource_presenter import ValidationResourcePresenter
from mcp_server.schemas.error_outputs import ValidationErrorOutput
from mcp_server.server import MCPServer


class StaticInput(BaseModel):
    """Existing static envelope, before startup selection projection."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    selected: str
    content: dict[str, JsonValue]


# Startup can project admitted selections while retaining the typed envelope.
AdmittedInput = create_model(
    "AdmittedInput", __base__=StaticInput, selected=(Literal["package-a"], ...)
)


class EchoOutput(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    success: bool
    content: dict[str, JsonValue]


class RecordingCore:
    """Execute the real typed input while observing whether admission reached it."""

    name = "prepared"
    description = "Echo admitted content"
    args_model: type[BaseModel] | None = StaticInput

    def __init__(self) -> None:
        self.inputs: list[BaseModel | None] = []

    async def execute(self, params: BaseModel | None, context: NoteContext) -> BaseModel:
        del context
        self.inputs.append(params)
        if params is None:
            return EchoOutput(success=True, content={})
        assert isinstance(params, StaticInput)
        return EchoOutput(success=True, content=params.content)


def test_prepared_schema_is_a_detached_immutable_snapshot() -> None:
    contract: IToolInputContract[StaticInput] = prepare_model_input(AdmittedInput)
    exposed = thaw_json(contract.schema)
    assert isinstance(exposed, dict)
    exposed.clear()
    assert "properties" in contract.schema
    with pytest.raises(FrozenInstanceError):
        contract.schema = freeze_json({})


@pytest.mark.asyncio
async def test_registered_schema_and_real_admission_share_the_prepared_contract(
    tmp_path: Path,
) -> None:
    contract = prepare_model_input(AdmittedInput)
    core = RecordingCore()
    wrapped = ToolErrorHandlerDecorator(InputValidationDecorator(core, input_contract=contract))
    server = MCPServer(
        settings=Settings(server=ServerSettings(workspace_root=str(tmp_path))),
        tools=[wrapped],
        resources=[],
    )
    listing = await server.server.request_handlers[ListToolsRequest](ListToolsRequest())
    assert isinstance(listing.root, ListToolsResult)
    assert listing.root.tools[0].inputSchema == thaw_json(contract.schema)
    assert wrapped.args_model is StaticInput
    raw: dict[str, JsonValue] = {
        "selected": "package-a",
        "content": {"flag": False, "count": 0, "empty": [], "nested": {"null": None}},
    }
    result = await server.tools[0].execute(raw, NoteContext())
    assert isinstance(result, EchoOutput)
    assert result.content == raw["content"]
    assert isinstance(core.inputs[0], AdmittedInput)
    # Delayed exposure cannot mutate the prepared snapshot through an earlier result.
    listing.root.tools[0].inputSchema.clear()
    repeated = await server.server.request_handlers[ListToolsRequest](ListToolsRequest())
    assert isinstance(repeated.root, ListToolsResult)
    assert repeated.root.tools[0].inputSchema == thaw_json(contract.schema)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "raw",
    [
        {"selected": "stale-package", "content": {}},
        {"selected": "package-a", "content": {}, "unknown": True},
        {"selected": 42, "content": {}},
    ],
    ids=["admitted-selection", "unknown-field", "strict-type"],
)
async def test_rejection_preserves_whole_tool_schema_and_skips_execution(
    raw: dict[str, JsonValue],
) -> None:
    contract = prepare_model_input(AdmittedInput)
    core = RecordingCore()
    wrapped = ToolErrorHandlerDecorator(InputValidationDecorator(core, input_contract=contract))
    result = await wrapped.execute(raw, NoteContext())
    assert isinstance(result, ValidationErrorOutput)
    assert core.inputs == []
    assert result.input_schema == wrapped.input_schema == thaw_json(contract.schema)
    assert result.params == raw
    resources = ValidationResourcePresenter().present_resources(wrapped.name, result)
    assert len(resources) == 1
    assert resources[0].uri == "schema://validation"
    assert resources[0].mime_type == "application/json"
    assert json.loads(resources[0].content) == result.input_schema


@pytest.mark.asyncio
async def test_explicit_no_argument_contract_keeps_none_execution() -> None:
    schema = freeze_json({"type": "object", "properties": {}})
    assert isinstance(schema, FrozenJsonObject)
    contract: PreparedToolInputContract[None] = PreparedToolInputContract(
        schema=schema, admit=lambda _raw: None
    )
    core = RecordingCore()
    core.args_model = None
    wrapped = InputValidationDecorator(core, input_contract=contract)
    result = await wrapped.execute({}, NoteContext())
    assert isinstance(result, EchoOutput)
    assert core.inputs == [None]
    assert wrapped.input_schema == thaw_json(schema)
