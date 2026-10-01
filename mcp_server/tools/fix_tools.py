"""Thin public fix selection tool with one prepared schema and binding authority."""

from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict, JsonValue
from pydantic.json_schema import JsonSchemaValue

from mcp_server.config.schemas.fixes_config import FixesConfig
from mcp_server.core.interfaces.icore_tool import ICoreTool
from mcp_server.core.interfaces.template_catalog import thaw_json
from mcp_server.core.interfaces.tool_input_contract import (
    PreparedToolInputContract,
    prepare_model_input,
)
from mcp_server.core.operation_notes import NoteContext
from mcp_server.core.tool_execution import ToolExecution
from mcp_server.execution.fix_service import FixManager, FixSelectionRequest
from mcp_server.execution.models import ApplyFixesOutput


class ApplyFixesTool(ICoreTool[FixSelectionRequest, ApplyFixesOutput]):
    """Bind the public fix request and delegate its operation meaning."""

    output_model: ClassVar[type[BaseModel]] = ApplyFixesOutput

    def __init__(self, *, manager: FixManager, config: FixesConfig) -> None:
        fix_ids = [name for name, _ in config.fixes]

        def public_schema(schema: JsonSchemaValue) -> None:
            """Project transport and configured choices onto typed admission."""
            properties = schema["properties"]
            for name in ("args", "timeout_seconds"):
                field = properties[name]
                variants = field.pop("anyOf")
                selected = next(value for value in variants if value.get("type") != "null")
                field.pop("default", None)
                field.update(selected)

            fixes_field = properties["fixes"]
            if fix_ids:
                fixes_field["items"]["enum"] = fix_ids
            else:
                fixes_field["items"] = {"not": {}}
            fixes_field["uniqueItems"] = True
            properties["args"] = {
                "type": "object",
                "properties": {
                    fix_id: {"type": "array", "items": {"type": "string"}} for fix_id in fix_ids
                },
                "additionalProperties": False,
            }

        class AdmittedApplyFixesInput(FixSelectionRequest):
            model_config = ConfigDict(
                frozen=True,
                strict=True,
                extra="forbid",
                json_schema_extra=public_schema,
            )

        self._input_model = AdmittedApplyFixesInput
        self._input_contract = prepare_model_input(self._input_model)
        self._manager = manager

    @property
    def name(self) -> str:
        return "apply_fixes"

    @property
    def description(self) -> str:
        return "Apply selected fixes and report their factual native outcomes."

    @property
    def args_model(self) -> type[FixSelectionRequest] | None:
        return self._input_model

    @property
    def input_contract(self) -> PreparedToolInputContract[FixSelectionRequest]:
        return self._input_contract

    @property
    def input_schema(self) -> dict[str, JsonValue]:
        schema = thaw_json(self._input_contract.schema)
        if not isinstance(schema, dict):
            raise TypeError("tool_input_schema_must_be_object")
        return schema

    async def execute(
        self,
        params: FixSelectionRequest,
        context: NoteContext,
    ) -> ToolExecution[ApplyFixesOutput]:
        del context
        return ToolExecution(operation=await self._manager.run(params), attachments=())
