"""Construct proposed edit text and select its original-file validation profile."""

from __future__ import annotations

import re
from collections.abc import Callable, Mapping
from difflib import get_close_matches
from functools import singledispatch
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr, model_validator

from mcp_server.config.schemas.checks_config import ExtensionKey, ProfileId
from mcp_server.config.schemas.template_suite import TemplateId
from mcp_server.core.interfaces.artifact_header_reader import (
    HeaderReadStatus,
    IArtifactHeaderReader,
)
from mcp_server.execution.models import NonBlankText


class _EditModel(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")


class ReplaceOperation(_EditModel):
    op: Literal["replace"] = "replace"
    target_content: StrictStr
    replacement: StrictStr
    search_window: tuple[StrictInt, StrictInt] | None = None


class AppendOperation(_EditModel):
    op: Literal["append"] = "append"
    content: StrictStr
    anchor: StrictStr | None = None
    position: Literal["after", "before"] = "after"


class RewriteOperation(_EditModel):
    op: Literal["rewrite"] = "rewrite"
    content: StrictStr


class PatternReplaceOperation(_EditModel):
    op: Literal["pattern_replace"] = "pattern_replace"
    pattern: StrictStr
    replacement: StrictStr
    regex: StrictBool = True


EditOperation = Annotated[
    ReplaceOperation | AppendOperation | RewriteOperation | PatternReplaceOperation,
    Field(discriminator="op"),
]
EditFailureReason = Literal[
    "missing_match", "missing_anchor", "invalid_pattern", "invalid_replacement"
]
MetadataFallbackReason = Literal["absent", "invalid", "unknown_template"]


class SourceLine(_EditModel):
    line_number: Annotated[StrictInt, Field(gt=0)]
    text: StrictStr


class EditDetails(_EditModel):
    reason: EditFailureReason
    message: NonBlankText
    suggestions: Annotated[tuple[NonBlankText, ...], Field(max_length=3)]
    context: Annotated[tuple[SourceLine, ...], Field(max_length=10)]


class EditConstructionError(ValueError):
    """Carry construction failure facts without a validation verdict."""

    def __init__(self, details: EditDetails) -> None:
        super().__init__(details.message)
        self.details = details


def _missing(original: str, target: str, reason: EditFailureReason) -> EditConstructionError:
    lines = original.splitlines()
    target_lines = target.splitlines()
    suggestions = get_close_matches(
        target_lines[0] if target_lines else target, lines, n=3, cutoff=0.6
    )
    return EditConstructionError(
        EditDetails(
            reason=reason,
            message=reason,
            suggestions=tuple(line for line in suggestions if line.strip()),
            context=tuple(
                SourceLine(line_number=index, text=line) for index, line in enumerate(lines[:10], 1)
            ),
        )
    )


@singledispatch
def _construct(_operation: object, _original: str) -> str:
    raise TypeError("unsupported_edit_operation")


@_construct.register
def _replace(operation: ReplaceOperation, original: str) -> str:
    if operation.search_window is None:
        if operation.target_content not in original:
            raise _missing(original, operation.target_content, "missing_match")
        return original.replace(operation.target_content, operation.replacement, 1)
    start, end = operation.search_window
    lines = original.splitlines(keepends=True)
    chunk = "".join(lines[start - 1 : end])
    if operation.target_content not in chunk:
        raise _missing(original, operation.target_content, "missing_match")
    lines[start - 1 : end] = [chunk.replace(operation.target_content, operation.replacement, 1)]
    return "".join(lines)


@_construct.register
def _append(operation: AppendOperation, original: str) -> str:
    text = operation.content
    if not text.endswith("\n"):
        text += "\n"
    if operation.anchor is None:
        prefix = "" if original.endswith("\n") or not original else "\n"
        return original + prefix + text
    if operation.anchor not in original:
        raise _missing(original, operation.anchor, "missing_anchor")
    if operation.position == "before":
        return original.replace(operation.anchor, text + operation.anchor, 1)
    return original.replace(operation.anchor, operation.anchor + "\n" + text.rstrip("\n"), 1)


@_construct.register
def _rewrite(operation: RewriteOperation, _original: str) -> str:
    return operation.content


@_construct.register
def _pattern_replace(operation: PatternReplaceOperation, original: str) -> str:
    if not operation.regex:
        return original.replace(operation.pattern, operation.replacement)
    try:
        compiled = re.compile(operation.pattern)
    except re.error as exc:
        raise EditConstructionError(
            EditDetails(
                reason="invalid_pattern",
                message=str(exc),
                suggestions=(),
                context=(),
            )
        ) from exc
    try:
        return compiled.sub(operation.replacement, original)
    except (re.error, IndexError) as exc:
        raise EditConstructionError(
            EditDetails(
                reason="invalid_replacement",
                message=str(exc),
                suggestions=(),
                context=(),
            )
        ) from exc


def construct_edit(original: str, operation: EditOperation) -> str:
    """Return one proposed text value without checking, reading or writing files."""
    return _construct(operation, original)


class EditProfileSelection(_EditModel):
    selected_source: Literal["input", "metadata", "extension", "none"]
    profile_id: ProfileId | None
    template_id: TemplateId | None
    extension: ExtensionKey | None
    selection_reason: MetadataFallbackReason | None

    @model_validator(mode="after")
    def validate_selection(self) -> Self:
        if self.selected_source in ("input", "metadata"):
            if (
                self.profile_id is None
                or self.template_id is None
                or self.extension is not None
                or self.selection_reason is not None
            ):
                raise ValueError("template_selection_facts_invalid")
        elif self.selected_source == "extension":
            if (
                self.profile_id is None
                or self.extension is None
                or self.template_id is not None
                or self.selection_reason is None
            ):
                raise ValueError("extension_selection_facts_invalid")
        elif (
            self.profile_id is not None
            or self.template_id is not None
            or self.extension is not None
            or self.selection_reason is None
        ):
            raise ValueError("no_profile_selection_facts_invalid")
        return self


def select_profile(
    original: str,
    filename: str,
    *,
    explicit_template_id: str | None,
    header_reader: IArtifactHeaderReader,
    template_profiles: Mapping[str, str],
    extension_profile_for_filename: Callable[[str], tuple[str, str] | None],
) -> EditProfileSelection:
    """Select from admitted current profiles without inspecting proposed content."""
    if explicit_template_id is not None:
        if explicit_template_id not in template_profiles:
            raise ValueError("unknown_template")
        return EditProfileSelection(
            selected_source="input",
            profile_id=template_profiles[explicit_template_id],
            template_id=explicit_template_id,
            extension=None,
            selection_reason=None,
        )
    header = header_reader.read(original)
    reason: MetadataFallbackReason
    if header.status is HeaderReadStatus.RECOGNIZED:
        provenance = header.provenance
        if provenance is None:
            raise ValueError("recognized_header_requires_provenance")
        if provenance.id in template_profiles:
            return EditProfileSelection(
                selected_source="metadata",
                profile_id=template_profiles[provenance.id],
                template_id=provenance.id,
                extension=None,
                selection_reason=None,
            )
        reason = "unknown_template"
    else:
        reason = "invalid" if header.status is HeaderReadStatus.INVALID else "absent"
    match = extension_profile_for_filename(filename)
    return EditProfileSelection(
        selected_source="extension" if match is not None else "none",
        profile_id=match[1] if match is not None else None,
        template_id=None,
        extension=match[0] if match is not None else None,
        selection_reason=reason,
    )
