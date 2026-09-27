"""Prepared public template-context schema discovery."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated, ClassVar, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    GetPydanticSchema,
    JsonValue,
    WithJsonSchema,
    create_model,
    field_serializer,
)
from pydantic_core import core_schema

from mcp_server.config.schemas.template_suite import (
    PackageText,
    TemplateId,
    TemplatePackageVersion,
)
from mcp_server.core.interfaces.icore_tool import ICoreTool
from mcp_server.core.interfaces.template_catalog import (
    FrozenJsonObject,
    thaw_json,
)
from mcp_server.core.interfaces.tool_input_contract import (
    PreparedToolInputContract,
    prepare_model_input,
)
from mcp_server.core.operation_notes import NoteContext
from mcp_server.core.tool_execution import (
    SchemaAttachment,
    TemplateContextSchemaIdentity,
    ToolExecution,
)
from mcp_server.schemas.template_identity import ArtifactIdentity, CompactFingerprint
from mcp_server.services.template_catalog import TemplateCatalog

SchemaData = Annotated[
    FrozenJsonObject,
    GetPydanticSchema(lambda _source, _handler: core_schema.is_instance_schema(FrozenJsonObject)),
    WithJsonSchema({"type": "object"}, mode="validation"),
]


class ScaffoldSchemaInput(BaseModel):
    """Typed envelope for selecting one admitted template package."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    artifact_type: TemplateId = Field(
        description="Public template-package identity from the resolved catalog.",
    )


class ScaffoldSchemaOutput(BaseModel):
    """Immutable operation facts for one successful schema discovery query."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    success: Literal[True]
    template_id: TemplateId
    purpose: PackageText
    package_version: TemplatePackageVersion
    package_fingerprint: CompactFingerprint
    schema_data: SchemaData

    @field_serializer("schema_data", when_used="json")
    def serialize_schema(self, value: FrozenJsonObject) -> Mapping[str, JsonValue]:
        """Serialize the immutable catalog view without changing its stored identity."""
        serialized = thaw_json(value)
        if not isinstance(serialized, dict):
            raise TypeError("schema_data_object_required")
        return serialized


class ScaffoldSchemaTool(ICoreTool[ScaffoldSchemaInput, ScaffoldSchemaOutput]):
    """Expose one resolved template context schema through prepared admission."""

    output_model: ClassVar[type[BaseModel]] = ScaffoldSchemaOutput

    def __init__(
        self,
        *,
        catalog: TemplateCatalog,
        identities: tuple[ArtifactIdentity, ...],
    ) -> None:
        packages = tuple(catalog.packages)
        package_ids = tuple(package.manifest.template_id for package in packages)
        identity_map = {identity.id: identity for identity in identities}
        if len(identity_map) != len(identities):
            raise ValueError("duplicate_artifact_identity")
        if set(identity_map) != set(package_ids):
            raise ValueError("artifact_identity_catalog_mismatch")
        for package in packages:
            identity = identity_map[package.manifest.template_id]
            if identity.pv != package.version:
                raise ValueError("artifact_identity_version_mismatch")

        self._catalog = catalog
        self._identities = identity_map
        self._input_model = create_model(
            "AdmittedScaffoldSchemaInput",
            __base__=ScaffoldSchemaInput,
            artifact_type=(
                TemplateId,
                Field(json_schema_extra={"enum": list(package_ids)}),
            ),
        )
        self._input_contract: PreparedToolInputContract[ScaffoldSchemaInput] = prepare_model_input(
            self._input_model
        )

    @property
    def name(self) -> str:
        return "scaffold_schema"

    @property
    def description(self) -> str:
        return "Return the complete resolved context schema for one template package."

    @property
    def args_model(self) -> type[ScaffoldSchemaInput] | None:
        return self._input_model

    @property
    def input_contract(self) -> PreparedToolInputContract[ScaffoldSchemaInput]:
        return self._input_contract

    @property
    def input_schema(self) -> dict[str, JsonValue]:
        schema = thaw_json(self._input_contract.schema)
        if not isinstance(schema, dict):
            raise TypeError("tool_input_schema_must_be_object")
        return schema

    async def execute(
        self,
        params: ScaffoldSchemaInput,
        context: NoteContext,
    ) -> ToolExecution[ScaffoldSchemaOutput]:
        """Return the selected catalog schema and its context-schema attachment."""
        del context
        package = self._catalog.get(params.artifact_type)
        identity = self._identities[params.artifact_type]
        operation = ScaffoldSchemaOutput(
            success=True,
            template_id=identity.id,
            purpose=package.manifest.purpose,
            package_version=identity.pv,
            package_fingerprint=identity.pf,
            schema_data=package.schema,
        )
        attachment = SchemaAttachment(
            identity=TemplateContextSchemaIdentity(
                kind="template_context",
                template_id=package.manifest.template_id,
            ),
            schema=package.schema,
        )
        return ToolExecution(operation=operation, attachments=(attachment,))
