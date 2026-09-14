"""Public scaffold operation tool with prepared template admission."""

from __future__ import annotations

import re
from typing import Annotated, ClassVar, Self

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    JsonValue,
    create_model,
    model_validator,
)

from mcp_server.config.schemas.template_suite import TemplateId
from mcp_server.core.interfaces.icore_tool import ICoreTool
from mcp_server.core.interfaces.template_catalog import thaw_json
from mcp_server.core.interfaces.tool_input_contract import (
    JsonObject,
    PreparedToolInputContract,
    prepare_model_input,
)
from mcp_server.core.operation_notes import NoteContext
from mcp_server.core.tool_execution import (
    SchemaAttachment,
    TemplateContextSchemaIdentity,
    ToolExecution,
)
from mcp_server.schemas.mutation_outputs import ScaffoldOperationOutput
from mcp_server.services.scaffold_operation import ScaffoldOperation, ValidationPolicy
from mcp_server.services.template_catalog import TemplateCatalog
from mcp_server.utils.path_resolver import normalize_workspace_relative_path


class ScaffoldArtifactInput(BaseModel):
    """Strict public input envelope for the scaffold operation."""

    model_config = ConfigDict(
        frozen=True,
        strict=True,
        extra="forbid",
        json_schema_extra={
            "allOf": [
                {
                    "if": {
                        "required": ["force_target"],
                        "properties": {"force_target": {"const": True}},
                    },
                    "then": {
                        "required": ["target_path"],
                        "properties": {"target_path": {"type": "string"}},
                    },
                }
            ],
        },
    )

    artifact_type: TemplateId = Field(
        description="Admitted template-package identity.",
    )
    file_name: str = Field(
        min_length=1,
        pattern=re.compile(r"^(?!\.{1,2}$(?![\s\S]))(?![\s\S]:)[^/\\\x00]+$(?![\s\S])"),
        description="Exact output basename, including extension.",
    )
    context: JsonObject = Field(description="Caller-provided template context.")
    target_path: (
        Annotated[
            str,
            Field(pattern=re.compile(r"^(?![\\/])(?![\s\S]:)(?=[\s\S]*\S)[^\x00]+$(?![\s\S])")),
            AfterValidator(normalize_workspace_relative_path),
        ]
        | None
    ) = Field(
        default=None,
        description="Optional target directory inside the workspace.",
    )
    force_target: bool = Field(
        default=False,
        description="Allow a target outside configured locations, within the workspace.",
    )
    validation: ValidationPolicy = Field(
        default="enforce",
        description="Validation policy for the generated content.",
    )

    @model_validator(mode="after")
    def validate_target_override(self) -> Self:
        """Require an explicit directory when opting out of configured locations."""
        if self.force_target and self.target_path is None:
            raise ValueError("force_target_requires_target_path")
        return self


class ScaffoldArtifactTool(ICoreTool[ScaffoldArtifactInput, ScaffoldOperationOutput]):
    """Execute the prepared scaffold operation and transport approved schema facts."""

    output_model: ClassVar[type[BaseModel]] = ScaffoldOperationOutput

    def __init__(
        self,
        *,
        catalog: TemplateCatalog,
        operation: ScaffoldOperation,
    ) -> None:
        package_ids = tuple(package.manifest.template_id for package in catalog.packages)
        self._catalog = catalog
        self._input_model = create_model(
            "AdmittedScaffoldArtifactInput",
            __base__=ScaffoldArtifactInput,
            artifact_type=(
                TemplateId,
                Field(
                    description="Admitted template-package identity.",
                    json_schema_extra={"enum": list(package_ids)},
                ),
            ),
        )
        self._input_contract: PreparedToolInputContract[ScaffoldArtifactInput] = (
            prepare_model_input(self._input_model)
        )
        self._operation = operation

    @property
    def name(self) -> str:
        return "scaffold_artifact"

    @property
    def description(self) -> str:
        return "Generate and persist one selected template artifact."

    @property
    def args_model(self) -> type[ScaffoldArtifactInput] | None:
        return self._input_model

    @property
    def input_contract(self) -> PreparedToolInputContract[ScaffoldArtifactInput]:
        return self._input_contract

    @property
    def input_schema(self) -> dict[str, JsonValue]:
        schema = thaw_json(self._input_contract.schema)
        if not isinstance(schema, dict):
            raise TypeError("tool_input_schema_must_be_object")
        return schema

    async def execute(
        self,
        params: ScaffoldArtifactInput,
        context: NoteContext,
    ) -> ToolExecution[ScaffoldOperationOutput]:
        """Delegate execution while attaching the selected context schema on rejection."""
        del context
        result = await self._operation.execute(
            artifact_type=params.artifact_type,
            file_name=params.file_name,
            context=params.context,
            target_path=params.target_path,
            force_target=params.force_target,
            validation=params.validation,
        )
        attachments: tuple[SchemaAttachment, ...] = ()
        if result.error_code == "context_invalid":
            package = self._catalog.get(result.template_id)
            attachments = (
                SchemaAttachment(
                    identity=TemplateContextSchemaIdentity(
                        kind="template_context",
                        template_id=package.manifest.template_id,
                    ),
                    schema=package.schema,
                ),
            )
        return ToolExecution(operation=result, attachments=attachments)
