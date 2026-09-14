"""Thin public test selection tool with one prepared schema and binding authority."""

from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict, JsonValue
from pydantic.json_schema import JsonSchemaValue

from mcp_server.config.schemas.tests_config import TestsConfig
from mcp_server.core.interfaces.icore_tool import ICoreTool
from mcp_server.core.interfaces.template_catalog import thaw_json
from mcp_server.core.interfaces.tool_input_contract import (
    PreparedToolInputContract,
    prepare_model_input,
)
from mcp_server.core.operation_notes import NoteContext
from mcp_server.core.tool_execution import ToolExecution
from mcp_server.execution.models import RunTestsOutput
from mcp_server.execution.test_service import TestRunManager, TestSelectionRequest


class RunTestsTool(ICoreTool[TestSelectionRequest, RunTestsOutput]):
    """Bind the public test request and delegate its operation meaning."""

    output_model: ClassVar[type[BaseModel]] = RunTestsOutput

    def __init__(self, *, manager: TestRunManager, config: TestsConfig) -> None:
        test_ids = [name for name, _ in config.tests]

        def public_schema(schema: JsonSchemaValue) -> None:
            """Project transport and configured choices onto typed admission."""
            properties = schema["properties"]
            for name in ("targets", "tests", "args", "timeout_seconds"):
                field = properties[name]
                variants = field.pop("anyOf")
                selected = next(value for value in variants if value.get("type") != "null")
                field.pop("default", None)
                field.update(selected)

            tests_field = properties["tests"]
            if test_ids:
                tests_field["items"]["enum"] = test_ids
            else:
                tests_field["items"] = {"not": {}}
            tests_field["uniqueItems"] = True
            properties["args"] = {
                "type": "object",
                "properties": {
                    test_id: {"type": "array", "items": {"type": "string"}} for test_id in test_ids
                },
                "additionalProperties": False,
            }
            schema["allOf"] = [
                {
                    "if": {"properties": {"scope": {"const": "targets"}}, "required": ["scope"]},
                    "then": {"required": ["targets"]},
                    "else": {"not": {"required": ["targets"]}},
                }
            ]

        class AdmittedRunTestsInput(TestSelectionRequest):
            model_config = ConfigDict(
                frozen=True,
                strict=True,
                extra="forbid",
                json_schema_extra=public_schema,
            )

        self._input_model = AdmittedRunTestsInput
        self._input_contract = prepare_model_input(self._input_model)
        self._manager = manager

    @property
    def name(self) -> str:
        return "run_tests"

    @property
    def description(self) -> str:
        return "Run selected tests and report their factual native outcomes."

    @property
    def args_model(self) -> type[TestSelectionRequest] | None:
        return self._input_model

    @property
    def input_contract(self) -> PreparedToolInputContract[TestSelectionRequest]:
        return self._input_contract

    @property
    def input_schema(self) -> dict[str, JsonValue]:
        schema = thaw_json(self._input_contract.schema)
        if not isinstance(schema, dict):
            raise TypeError("tool_input_schema_must_be_object")
        return schema

    async def execute(
        self,
        params: TestSelectionRequest,
        context: NoteContext,
    ) -> ToolExecution[RunTestsOutput]:
        del context
        return ToolExecution(operation=await self._manager.run(params), attachments=())
