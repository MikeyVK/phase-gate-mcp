# mcp_server/config/schemas/presentation_config.py
# template=schema version=74378193 created=2026-06-12T20:49Z updated=2026-08-21
"""PresentationConfig schema.

@layer: Config
"""

from __future__ import annotations

import string
from typing import Annotated, Literal

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    TypeAdapter,
    ValidationError,
    model_validator,
)

from mcp_server.config.ordering import ConfigId, OrderedConfigEntry, ordered_mapping
from mcp_server.config.settings import ResponseMode
from mcp_server.core.exceptions import ConfigError


def _validate_placeholders(
    template: str,
    *,
    allowed: frozenset[str],
    field_name: str,
) -> None:
    """Reject invalid or unsupported placeholders in a presentation template."""
    try:
        placeholders = {
            placeholder.split(".")[0].split("[")[0]
            for _, placeholder, _, _ in string.Formatter().parse(template)
            if placeholder is not None
        }
    except ValueError as exc:
        raise ValueError(f"{field_name} has invalid placeholder syntax: {exc}") from exc

    unsupported = placeholders - allowed
    if unsupported:
        rendered = ", ".join(sorted(unsupported))
        raise ValueError(f"{field_name} contains unsupported placeholder(s): {rendered}")


class FormattingConfig(BaseModel):
    """Formatting settings for text presentation."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    none_value: str = "-"
    inline_sequence_separator: str = ", "
    inline_sequence_omission_template: str
    collection_omission_template: str
    truncation_notice: str
    cache_unavailable_truncation_notice: str

    @model_validator(mode="after")
    def validate_templates(self) -> FormattingConfig:
        """Validate the deliberately small generic formatting vocabulary."""
        _validate_placeholders(
            self.inline_sequence_omission_template,
            allowed=frozenset({"omitted_count"}),
            field_name="inline_sequence_omission_template",
        )
        _validate_placeholders(
            self.collection_omission_template,
            allowed=frozenset({"omitted_count", "field"}),
            field_name="collection_omission_template",
        )
        _validate_placeholders(
            self.truncation_notice,
            allowed=frozenset(),
            field_name="truncation_notice",
        )
        _validate_placeholders(
            self.cache_unavailable_truncation_notice,
            allowed=frozenset(),
            field_name="cache_unavailable_truncation_notice",
        )
        return self


class NoteGroupConfig(BaseModel):
    """Configuration for a note group."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    emoji: str
    header: str


class GlobalNotesConfig(BaseModel):
    """Global notes settings."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    groups: dict[str, NoteGroupConfig] = Field(default_factory=dict)
    templates: dict[str, dict[str, str]] = Field(default_factory=dict)


class CollectionPresentationConfig(OrderedConfigEntry):
    """Declarative rendering policy for one direct ordered-sequence field."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    field: str = Field(min_length=1)
    heading: str | None = None
    item_template: str
    children: Annotated[
        dict[ConfigId, CollectionPresentationConfig], AfterValidator(ordered_mapping)
    ] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_children(self) -> CollectionPresentationConfig:
        """Require unique direct child declarations."""
        child_fields = [child.field for child in self.children.values()]
        if len(child_fields) != len(set(child_fields)):
            raise ValueError(f"Collection '{self.field}' has duplicate child field declarations")
        return self


class EnumCasePresentationConfig(OrderedConfigEntry):
    """Declarative text blocks selected by a serialized enum value."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    field: str = Field(min_length=1)
    cases: dict[str, str] = Field(min_length=1)


class GlobalPresentationConfig(BaseModel):
    """Global presentation settings."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    emojis: dict[str, str] = Field(default_factory=dict)
    default_failure_template: str = "Failed: {error_message}"
    next_instruction_texts: dict[str, str] = Field(default_factory=dict)
    formatting: FormattingConfig
    notes: GlobalNotesConfig = Field(default_factory=GlobalNotesConfig)
    failures: dict[str, str] = Field(default_factory=dict)
    response_mode: ResponseMode
    max_text_response_bytes: int = Field(default=8_000, gt=0)
    max_cache_failure_detail_bytes: int = Field(default=8_000, gt=0)
    cache_read_budget_chars: int = Field(default=6_000, gt=0)

    @model_validator(mode="after")
    def validate_delivery_templates(self) -> GlobalPresentationConfig:
        """Validate delivery wording and its conservative fixed notice reserve."""
        required = (
            "uri_reference",
            "structured_reference",
            "attachment_reference",
            "delivery_failure_outcome",
            "cache_publication_failed",
            "operation_serialization_failed",
            "diagnostic_excerpt_label",
            "diagnostic_unavailable",
            "response_processing_failed",
            "recovery_cache_unavailable",
            "processing_diagnostic_truncated",
        )
        rendered: list[str] = []
        for key in (*required, "pagination_reference"):
            text = self.next_instruction_texts.get(key, "")
            if key in required and not text.strip():
                raise ValueError(f"next_instruction_texts.{key} must be nonempty")
            allowed = (
                frozenset({"run_id"})
                if key == "uri_reference"
                else frozenset({"success"})
                if key in {"response_processing_failed", "delivery_failure_outcome"}
                else frozenset[str]()
            )
            _validate_placeholders(text, allowed=allowed, field_name=key)
            for _, placeholder, format_spec, conversion in string.Formatter().parse(text):
                if placeholder is not None and (
                    placeholder not in allowed or format_spec or conversion
                ):
                    raise ValueError(f"{key} contains an unsupported scalar placeholder")
            rendered.append(text.format(run_id="x" * 32, success=False))
        rendered.extend(
            (
                self.formatting.truncation_notice,
                self.formatting.cache_unavailable_truncation_notice,
            )
        )
        reserve = sum(len(text.encode("utf-8")) for text in rendered)
        reserve += 2 * (len(rendered) + 1) + len("\n```")
        if self.max_text_response_bytes < reserve:
            raise ValueError(
                f"max_text_response_bytes cannot contain configured notices (minimum {reserve})"
            )
        return self

    @model_validator(mode="after")
    def validate_recovery_templates(self) -> GlobalPresentationConfig:
        """Keep recovery wording independent of ordinary rendering inputs."""
        for key in (
            "response_processing_failed",
            "recovery_cache_unavailable",
            "processing_diagnostic_truncated",
        ):
            text = self.next_instruction_texts.get(key, "")
            if not text.strip():
                raise ValueError(f"next_instruction_texts.{key} must be nonempty")
            allowed = (
                frozenset({"success"}) if key == "response_processing_failed" else frozenset[str]()
            )
            _validate_placeholders(text, allowed=allowed, field_name=key)
            for _, placeholder, format_spec, conversion in string.Formatter().parse(text):
                if placeholder is not None and (
                    placeholder not in allowed or format_spec or conversion
                ):
                    raise ValueError(f"{key} contains an unsupported scalar placeholder")
        return self


class ToolPresentationConfig(BaseModel):
    """Presentation settings for a specific tool."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    category: str | None = None
    template_success: str | None = None
    template_failure: str | None = None
    next_instructions: list[str] = Field(default_factory=list)
    exclusions: dict[str, str] = Field(default_factory=dict)
    suggestions: dict[str, str] = Field(default_factory=dict)
    recoveries: dict[str, str] = Field(default_factory=dict)
    info: dict[str, str] = Field(default_factory=dict)
    max_items: int | None = Field(default=None, gt=0)
    collections: Annotated[
        dict[ConfigId, CollectionPresentationConfig], AfterValidator(ordered_mapping)
    ] = Field(default_factory=dict)
    enum_cases: Annotated[
        dict[ConfigId, EnumCasePresentationConfig], AfterValidator(ordered_mapping)
    ] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_declaration_identity(self) -> ToolPresentationConfig:
        """Reject ambiguous sibling declarations before runtime assembly."""
        collection_fields = [collection.field for collection in self.collections.values()]
        if len(collection_fields) != len(set(collection_fields)):
            raise ValueError("Tool has duplicate collection field declarations")

        enum_fields = [enum_case.field for enum_case in self.enum_cases.values()]
        if len(enum_fields) != len(set(enum_fields)):
            raise ValueError("Tool has duplicate enum-case field declarations")
        return self


class PresentationConfig(BaseModel):
    """Unified configuration for declarative text presentation."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    version: Literal["2.0.0"] = Field("2.0.0", description="Config schema version")
    global_settings: GlobalPresentationConfig = Field(alias="global")
    tools: dict[str, ToolPresentationConfig] = Field(default_factory=dict)

    def resolve_response_mode(self, selector: ResponseMode | None = None) -> ResponseMode:
        """Resolve one local choice without changing shared configuration."""
        if selector is None:
            return self.global_settings.response_mode
        try:
            return TypeAdapter(ResponseMode).validate_python(selector)
        except ValidationError as exc:
            raise ConfigError(f"Invalid response mode: {selector}") from exc
