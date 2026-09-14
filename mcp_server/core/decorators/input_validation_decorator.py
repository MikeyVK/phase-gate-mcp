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
from typing import Any, Generic, TypeVar

# Third-party
import jsonschema
from pydantic import BaseModel, ValidationError

from mcp_server.core.interfaces.icore_tool import ICoreTool
from mcp_server.core.interfaces.itool import ITool
from mcp_server.core.interfaces.template_catalog import FrozenJsonObject, freeze_json, thaw_json
from mcp_server.core.interfaces.tool_input_contract import IToolInputContract, JsonObject
from mcp_server.core.operation_notes import NoteContext
from mcp_server.core.tool_execution import SchemaAttachment, ToolExecution, WholeToolSchemaIdentity
from mcp_server.schemas.error_outputs import ValidationErrorOutput
from mcp_server.utils.schema_utils import resolve_schema_refs

TOutput = TypeVar("TOutput", bound=BaseModel)


class InputValidationDecorator(ITool[TOutput | ValidationErrorOutput], Generic[TOutput]):
    """Bridges the untyped transport layer with the typed core execution layer."""

    def __init__(
        self,
        inner_tool: ICoreTool[BaseModel, TOutput],
        *,
        input_contract: IToolInputContract[BaseModel | None] | None = None,
    ) -> None:
        self._inner_tool = inner_tool
        self._input_contract = input_contract

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
        if self._input_contract is not None:
            return {key: thaw_json(value) for key, value in self._input_contract.schema.items()}
        if self.args_model:
            return resolve_schema_refs(self.args_model.model_json_schema())
        return {
            "type": "object",
            "properties": {},
        }

    async def execute(
        self, params: JsonObject, context: NoteContext
    ) -> ToolExecution[TOutput | ValidationErrorOutput]:
        attachment_schema = (
            self._input_contract.schema
            if self._input_contract is not None
            else freeze_json(self.input_schema)
        )
        if not isinstance(attachment_schema, FrozenJsonObject):
            raise TypeError("Tool input schema must be an object")
        try:
            if self._input_contract is not None:
                validated = self._input_contract.validate(params)
            else:
                # Preserve the public wire contract before Python model construction.
                jsonschema.validate(instance=params, schema=thaw_json(attachment_schema))
                validated = (
                    self.args_model.model_validate(params) if self.args_model is not None else None
                )
        except jsonschema.ValidationError as error:
            return input_validation_failure(
                self.name,
                params,
                attachment_schema,
                [{"field": ".".join(map(str, error.absolute_path)), "error": error.message}],
            )
        except ValidationError as e:
            return input_validation_failure(
                self.name,
                params,
                attachment_schema,
                [
                    {"field": ".".join(map(str, err["loc"])), "error": err["msg"]}
                    for err in e.errors()
                ],
            )

        if validated is None:
            # Preserve the existing no-argument core contract.
            result = await self._inner_tool.execute(None, context)  # type: ignore[arg-type]
        else:
            result = await self._inner_tool.execute(validated, context)
        if isinstance(result, ToolExecution):
            return result
        return ToolExecution(operation=result, attachments=())


def input_validation_failure(
    tool_name: str,
    params: JsonObject,
    schema: FrozenJsonObject,
    errors: list[dict[str, str]],
) -> ToolExecution[ValidationErrorOutput]:
    """Project input rejection through the common whole-tool response carrier."""
    return ToolExecution(
        operation=ValidationErrorOutput(
            error_message=f"Invalid input for {tool_name}",
            validation_errors=errors,
            input_schema={key: thaw_json(value) for key, value in schema.items()},
            params=params,
        ),
        attachments=(
            SchemaAttachment(identity=WholeToolSchemaIdentity(kind="whole_tool"), schema=schema),
        ),
    )
