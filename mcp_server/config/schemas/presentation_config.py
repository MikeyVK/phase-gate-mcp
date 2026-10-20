# mcp_server/config/schemas/presentation_config.py
# template=schema version=74378193 created=2026-06-12T20:49Z updated=2026-08-21
"""PresentationConfig schema.

@layer: Config
"""

from __future__ import annotations

import string
from typing import Annotated, Literal

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, model_validator

from mcp_server.config.ordering import ConfigId, OrderedConfigEntry, ordered_mapping
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


class ResponseProfileConfig(BaseModel):
    """Shared capabilities and optional per-profile presentation budgets."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    presentation_channel: Literal["text", "structured", "both"]
    data_channel: Literal["text", "structured"]
    data_delivery: Literal["inline", "resource"]
    max_text_response_bytes: int | None = Field(default=None, gt=0)
    max_cache_failure_detail_bytes: int | None = Field(default=None, gt=0)
    cache_read_budget_chars: int | None = Field(default=None, gt=0)


class ResolvedResponseProfile(BaseModel):
    """Immutable process-local capabilities with every budget resolved."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    profile_id: ConfigId
    presentation_channel: Literal["text", "structured", "both"]
    data_channel: Literal["text", "structured"]
    data_delivery: Literal["inline", "resource"]
    max_text_response_bytes: int = Field(gt=0)
    max_cache_failure_detail_bytes: int = Field(gt=0)
    cache_read_budget_chars: int = Field(gt=0)


class GlobalPresentationConfig(BaseModel):
    """Global presentation settings."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    emojis: dict[str, str] = Field(default_factory=dict)
    default_failure_template: str = "Failed: {error_message}"
    next_instruction_texts: dict[str, str] = Field(default_factory=dict)
    formatting: FormattingConfig
    notes: GlobalNotesConfig = Field(default_factory=GlobalNotesConfig)
    failures: dict[str, str] = Field(default_factory=dict)
    default_response_profile: ConfigId
    max_text_response_bytes: int = Field(default=8_000, gt=0)
    max_cache_failure_detail_bytes: int = Field(default=8_000, gt=0)
    cache_read_budget_chars: int = Field(default=6_000, gt=0)

    @model_validator(mode="after")
    def validate_cache_reference_template(self) -> GlobalPresentationConfig:
        """Reject malformed cache references independently of positive budgets."""
        for key in (
            "cache_publication_failed",
            "operation_serialization_failed",
            "diagnostic_excerpt_label",
            "diagnostic_unavailable",
        ):
            if not self.next_instruction_texts.get(key):
                raise ValueError(f"next_instruction_texts.{key} must be nonempty")
        uri_template = "\n".join(
            text
            for key in ("uri_reference", "pagination_reference")
            if (text := self.next_instruction_texts.get(key, ""))
        )
        try:
            uri_template.format(run_id="x" * 32)
        except (KeyError, ValueError) as exc:
            raise ValueError(
                f"next_instruction_texts.uri_reference has invalid placeholder syntax: {exc}"
            ) from exc

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
            allowed = frozenset({"success"}) if key == "response_processing_failed" else frozenset()
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
    response_profiles: dict[ConfigId, ResponseProfileConfig] = Field(min_length=1)
    tools: dict[str, ToolPresentationConfig] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_default_response_profile(self) -> PresentationConfig:
        """Require the configured default to identify a shared profile."""
        if self.global_settings.default_response_profile not in self.response_profiles:
            raise ValueError("default_response_profile must identify a configured response profile")
        return self

    def resolve_response_profile(self, selector: str | None = None) -> ResolvedResponseProfile:
        """Resolve one selection without changing shared definitions or defaults."""
        profile_id = self.global_settings.default_response_profile if selector is None else selector
        if profile_id not in self.response_profiles:
            raise ConfigError(f"Unknown response profile: {profile_id!r}")
        profile = self.response_profiles[profile_id]
        global_settings = self.global_settings
        return ResolvedResponseProfile(
            profile_id=profile_id,
            presentation_channel=profile.presentation_channel,
            data_channel=profile.data_channel,
            data_delivery=profile.data_delivery,
            max_text_response_bytes=(
                global_settings.max_text_response_bytes
                if profile.max_text_response_bytes is None
                else profile.max_text_response_bytes
            ),
            max_cache_failure_detail_bytes=(
                global_settings.max_cache_failure_detail_bytes
                if profile.max_cache_failure_detail_bytes is None
                else profile.max_cache_failure_detail_bytes
            ),
            cache_read_budget_chars=(
                global_settings.cache_read_budget_chars
                if profile.cache_read_budget_chars is None
                else profile.cache_read_budget_chars
            ),
        )
