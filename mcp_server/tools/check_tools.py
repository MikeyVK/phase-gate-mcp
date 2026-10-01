"""Thin public selection checks with one prepared schema and binding authority."""

from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict, JsonValue
from pydantic.json_schema import JsonSchemaValue

from mcp_server.config.schemas.checks_config import ChecksConfig
from mcp_server.core.interfaces.icore_tool import ICoreTool
from mcp_server.core.interfaces.template_catalog import thaw_json
from mcp_server.core.interfaces.tool_input_contract import (
    PreparedToolInputContract,
    prepare_model_input,
)
from mcp_server.core.operation_notes import NoteContext
from mcp_server.core.tool_execution import ToolExecution
from mcp_server.execution.check_selection import CheckSelectionRequest
from mcp_server.schemas.execution_outputs import RunChecksOutput
from mcp_server.services.check_operation import CheckOperation


class RunChecksTool(ICoreTool[CheckSelectionRequest, RunChecksOutput]):
    """Bind the public check request and delegate its operation meaning."""

    output_model: ClassVar[type[BaseModel]] = RunChecksOutput

    def __init__(self, *, operation: CheckOperation, config: ChecksConfig) -> None:
        check_ids = [name for name, _ in config.checks]
        profile_ids = [name for name, _ in config.profiles]

        def public_schema(schema: JsonSchemaValue) -> None:
            """Project JSON transport and configured choices onto existing typed admission."""
            properties = schema["properties"]
            for name in ("targets", "profile", "checks", "args", "timeout_seconds"):
                field = properties[name]
                variants = field.pop("anyOf")
                selected = next(value for value in variants if value.get("type") != "null")
                field.pop("default", None)
                field.update(selected)
            properties["profile"]["enum"] = profile_ids
            properties["checks"]["items"]["enum"] = check_ids
            properties["checks"]["uniqueItems"] = True
            properties["args"] = {
                "type": "object",
                "properties": {
                    name: {"type": "array", "items": {"type": "string"}} for name in check_ids
                },
                "additionalProperties": False,
            }
            schema["allOf"] = [
                {
                    "if": {"properties": {"scope": {"const": "targets"}}, "required": ["scope"]},
                    "then": {"required": ["targets"]},
                    "else": {"not": {"required": ["targets"]}},
                },
                {"not": {"required": ["profile", "checks"]}},
            ]

        class AdmittedRunChecksInput(CheckSelectionRequest):
            model_config = ConfigDict(
                frozen=True,
                strict=True,
                extra="forbid",
                json_schema_extra=public_schema,
            )

        self._input_model = AdmittedRunChecksInput
        self._input_contract = prepare_model_input(self._input_model)
        self._operation = operation

    @property
    def name(self) -> str:
        return "run_checks"

    @property
    def description(self) -> str:
        return "Run selected checks and report their factual native outcomes."

    @property
    def args_model(self) -> type[CheckSelectionRequest] | None:
        return self._input_model

    @property
    def input_contract(self) -> PreparedToolInputContract[CheckSelectionRequest]:
        return self._input_contract

    @property
    def input_schema(self) -> dict[str, JsonValue]:
        schema = thaw_json(self._input_contract.schema)
        if not isinstance(schema, dict):
            raise TypeError("tool_input_schema_must_be_object")
        return schema

    async def execute(
        self,
        params: CheckSelectionRequest,
        context: NoteContext,
    ) -> ToolExecution[RunChecksOutput]:
        del context
        return ToolExecution(operation=await self._operation.execute(params), attachments=())
