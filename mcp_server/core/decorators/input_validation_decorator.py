# c:\temp\pgmcp\mcp_server\core\decorators\input_validation_decorator.py
# template=generic version=f35abd82 created=2026-06-19T22:04Z updated=
"""InputValidationDecorator module.

Decorator that validates incoming raw parameters dictionary into Pydantic models before execution.

@layer: Backend (Decorators)
@dependencies: [mcp_server.core.interfaces.itool, mcp_server.core.interfaces.icore_tool, pydantic]
@responsibilities:
    - Validate raw dictionaries to Pydantic models
    - Return ValidationErrorOutput DTO on validation failure
    - Bypass validation if no args_model is defined
"""

# Standard library
from typing import Any

# Third-party
from pydantic import BaseModel, ValidationError

from mcp_server.core.interfaces.icore_tool import ICoreTool
from mcp_server.core.interfaces.itool import ITool
from mcp_server.core.operation_notes import NoteContext
from mcp_server.schemas.error_outputs import ValidationErrorOutput
from mcp_server.utils.schema_utils import resolve_schema_refs


class InputValidationDecorator(ITool):
    """Bridges the untyped transport layer with the typed core execution layer."""

    def __init__(self, inner_tool: ICoreTool[BaseModel, BaseModel]) -> None:
        self._inner_tool = inner_tool

    @property
    def name(self) -> str:
        return self._inner_tool.name

    @property
    def description(self) -> str:
        return self._inner_tool.description

    @property
    def args_model(self) -> type[BaseModel] | None:
        return self._inner_tool.args_model

    @property
    def tool_category(self) -> str | None:
        return getattr(self._inner_tool, "tool_category", None)

    @property
    def enforcement_event(self) -> str:
        return getattr(self._inner_tool, "enforcement_event", self.name)

    @property
    def input_schema(self) -> dict[str, Any]:
        if self.args_model:
            return resolve_schema_refs(self.args_model.model_json_schema())
        return {
            "type": "object",
            "properties": {},
        }

    async def execute(self, params: dict[str, Any], context: NoteContext) -> BaseModel:
        if not self.args_model:
            # Bypass validation if no input arguments model is defined
            return await self._inner_tool.execute(None, context)  # type: ignore[arg-type]
        try:
            validated = self.args_model.model_validate(params)
        except ValidationError as e:
            schema = resolve_schema_refs(self.args_model.model_json_schema())
            return ValidationErrorOutput(
                error_message=f"Invalid input for {self.name}",
                validation_errors=[
                    {"field": ".".join(map(str, err["loc"])), "error": err["msg"]}
                    for err in e.errors()
                ],
                input_schema=schema,
                params=params,
            )

        return await self._inner_tool.execute(validated, context)
