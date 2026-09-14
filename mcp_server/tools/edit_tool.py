"""Public safe-edit operation with prepared strict input admission."""

from __future__ import annotations

import re
from typing import Annotated, ClassVar

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    JsonValue,
    StrictInt,
    create_model,
)

from mcp_server.config.schemas.template_suite import TemplateId
from mcp_server.core.interfaces.icore_tool import ICoreTool
from mcp_server.core.interfaces.template_catalog import thaw_json
from mcp_server.core.interfaces.tool_input_contract import (
    PreparedToolInputContract,
    prepare_model_input,
)
from mcp_server.core.operation_notes import NoteContext
from mcp_server.core.tool_execution import ToolExecution
from mcp_server.schemas.mutation_outputs import EditOperationOutput
from mcp_server.services.edit_construction import (
    AppendOperation,
    PatternReplaceOperation,
    ReplaceOperation,
    RewriteOperation,
)
from mcp_server.services.edit_operation import EditOperation
from mcp_server.services.scaffold_operation import ValidationPolicy
from mcp_server.services.template_catalog import TemplateCatalog
from mcp_server.utils.path_resolver import normalize_workspace_relative_path


class PublicReplaceOperation(ReplaceOperation):
    """Accept JSON array transport for the existing strict window value."""

    search_window: Annotated[tuple[StrictInt, StrictInt], Field(strict=False)] | None = None


PublicEditOperation = Annotated[
    PublicReplaceOperation | AppendOperation | RewriteOperation | PatternReplaceOperation,
    Field(discriminator="op"),
]


class SafeEditInput(BaseModel):
    """Strict public input envelope for one safe-edit operation."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    path: Annotated[
        str,
        Field(pattern=re.compile(r"^(?![\\/])(?![\s\S]:)(?=[\s\S]*\S)[^\x00]+$(?![\s\S])")),
        AfterValidator(normalize_workspace_relative_path),
    ]
    operation: PublicEditOperation
    template_id: TemplateId | None = Field(
        default=None,
        description="Optional selected template identity.",
    )
    validation: ValidationPolicy = Field(
        default="enforce",
        description="Validation policy for the proposed edit.",
    )


class SafeEditTool(ICoreTool[SafeEditInput, EditOperationOutput]):
    """Execute the injected edit operation and return its complete operation facts."""

    output_model: ClassVar[type[BaseModel]] = EditOperationOutput

    def __init__(
        self,
        *,
        catalog: TemplateCatalog,
        operation: EditOperation,
    ) -> None:
        template_ids = tuple(package.manifest.template_id for package in catalog.packages)
        self._input_model = create_model(
            "AdmittedSafeEditInput",
            __base__=SafeEditInput,
            template_id=(
                TemplateId | None,
                Field(
                    default=None,
                    description="Optional selected template identity.",
                    json_schema_extra={"enum": [*template_ids, None]},
                ),
            ),
        )
        self._input_contract: PreparedToolInputContract[SafeEditInput] = prepare_model_input(
            self._input_model
        )
        self._operation = operation

    @property
    def name(self) -> str:
        return "safe_edit_file"

    @property
    def description(self) -> str:
        return "Apply one validated edit to an existing workspace file."

    @property
    def args_model(self) -> type[SafeEditInput] | None:
        return self._input_model

    @property
    def input_contract(self) -> PreparedToolInputContract[SafeEditInput]:
        return self._input_contract

    @property
    def input_schema(self) -> dict[str, JsonValue]:
        schema = thaw_json(self._input_contract.schema)
        if not isinstance(schema, dict):
            raise TypeError("tool_input_schema_must_be_object")
        return schema

    async def execute(
        self,
        params: SafeEditInput,
        context: NoteContext,
    ) -> ToolExecution[EditOperationOutput]:
        """Delegate to the operation without adding transport attachments."""
        del context
        result = await self._operation.execute(
            path=params.path,
            operation=params.operation,
            template_id=params.template_id,
            validation=params.validation,
        )
        return ToolExecution(operation=result, attachments=())
