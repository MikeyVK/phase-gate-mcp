# mcp_server/config/schemas/adapter_manifest.py
# template=schema version=74378193 created=2026-09-13T19:17Z updated=
"""Strict immutable adapter declarations; no filesystem or execution knowledge."""

from __future__ import annotations

import re
from pathlib import PurePosixPath, PureWindowsPath
from typing import Annotated, Generic, Literal, Self, TypeVar

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    StringConstraints,
    field_serializer,
    field_validator,
    model_validator,
)

AdapterId = Annotated[
    str, StringConstraints(strict=True, pattern=re.compile(r"^[a-z][a-z0-9_]{0,63}$(?![\s\S])"))
]
CapabilityId = AdapterId
AdapterVersion = Annotated[
    str,
    StringConstraints(
        strict=True,
        pattern=re.compile(
            r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
            r"(?:-(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)"
            r"(?:\.(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*))*)?"
            r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$(?![\s\S])"
        ),
    ),
]


def _text(value: object) -> object:
    if isinstance(value, str) and "\x00" in value:
        raise ValueError("nul_in_process_text")
    return value


def _program(value: object) -> object:
    _text(value)
    if isinstance(value, str) and (
        not value.strip() or value in {".", ".."} or any(char in value for char in "/\\:")
    ):
        raise ValueError("program_name_required")
    return value


def _relative_file(value: object) -> object:
    _text(value)
    if isinstance(value, str) and (
        not value.strip()
        or PurePosixPath(value).is_absolute()
        or PureWindowsPath(value).root
        or PureWindowsPath(value).drive
    ):
        raise ValueError("package_relative_file_required")
    return value


def _array(value: object) -> object:
    return tuple(value) if isinstance(value, list) else value


ProgramName = Annotated[str, BeforeValidator(_program), StringConstraints(strict=True)]
PackageRelativeFilePath = Annotated[
    str, BeforeValidator(_relative_file), StringConstraints(strict=True)
]
ProcessArgument = Annotated[str, BeforeValidator(_text), StringConstraints(strict=True)]


class _Declaration(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")


class PackageFileReference(_Declaration):
    """One shared file reference for executable and argument positions."""

    package_file: PackageRelativeFilePath


AdapterExecutable = ProgramName | PackageFileReference
AdapterArgument = ProcessArgument | PackageFileReference


class AdapterEntrypoint(_Declaration):
    """Authored launch data, without resolved paths or an implicit shell."""

    executable: AdapterExecutable
    args: Annotated[tuple[AdapterArgument, ...], BeforeValidator(_array)]


class CheckCapability(_Declaration):
    """Supported input routes and their explicitly declared file requirement."""

    inputs: Annotated[
        tuple[Literal["content", "selection"], ...], BeforeValidator(_array), Field(min_length=1)
    ]
    requires_file: bool | None = None

    @model_validator(mode="after")
    def validate_inputs(self) -> Self:
        if len(set(self.inputs)) != len(self.inputs):
            raise ValueError("duplicate_check_input")
        if "content" in self.inputs:
            if self.requires_file is None:
                raise ValueError("content_requires_file_declaration")
        elif "requires_file" in self.model_fields_set:
            raise ValueError("selection_forbids_requires_file")
        return self


class TestCapability(_Declaration):
    """Native test arguments have no per-capability options schema."""


class CheckAddress(_Declaration):
    """An exact check capability addressed by a fix."""

    adapter_id: AdapterId
    capability: CapabilityId


class FixCapability(_Declaration):
    """Discovery relation only; no automatic verification execution."""

    addresses: Annotated[tuple[CheckAddress, ...], BeforeValidator(_array), Field(min_length=1)]


CapabilityT = TypeVar("CapabilityT", bound=BaseModel)


class AdapterRole(_Declaration, Generic[CapabilityT]):
    """One role protocol and immutable named capability declarations."""

    contract_version: Annotated[int, Field(strict=True, ge=1, le=1)]
    entrypoint: AdapterEntrypoint
    capabilities: Annotated[tuple[tuple[CapabilityId, CapabilityT], ...], Field(min_length=1)]

    @field_validator("capabilities", mode="before")
    @classmethod
    def freeze_capabilities(cls, value: object) -> object:
        return tuple(value.items()) if isinstance(value, dict) else value

    @field_validator("capabilities")
    @classmethod
    def unique_capabilities(
        cls, value: tuple[tuple[str, CapabilityT], ...]
    ) -> tuple[tuple[str, CapabilityT], ...]:
        if len({name for name, _ in value}) != len(value):
            raise ValueError("duplicate_capability")
        return value

    @field_serializer("capabilities")
    def wire_capabilities(
        self, value: tuple[tuple[str, CapabilityT], ...]
    ) -> dict[str, CapabilityT]:
        return dict(value)


class AdapterRoles(_Declaration):
    """An absent role is not offered; explicit null is never a declaration."""

    check: AdapterRole[CheckCapability] | None = None
    test: AdapterRole[TestCapability] | None = None
    fix: AdapterRole[FixCapability] | None = None

    @field_validator("check", "test", "fix", mode="before")
    @classmethod
    def reject_null_role(cls, value: object) -> object:
        if value is None:
            raise ValueError("null_adapter_role")
        return value

    @model_validator(mode="after")
    def nonempty(self) -> Self:
        if not self.model_fields_set:
            raise ValueError("adapter_role_required")
        return self


class AdapterManifest(_Declaration):
    """Manifest identity, exact file inventory and independently versioned roles."""

    adapter_id: AdapterId
    version: AdapterVersion
    files: Annotated[
        tuple[PackageRelativeFilePath, ...], BeforeValidator(_array), Field(min_length=1)
    ]
    roles: AdapterRoles

    @field_validator("files")
    @classmethod
    def unique_files(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(set(value)) != len(value) or "manifest.yaml" in value:
            raise ValueError("invalid_adapter_inventory")
        return value


class AdapterTrustConfig(_Declaration):
    """The sole owner-authored workspace adapter trust policy."""

    trusted_adapter_ids: Annotated[tuple[AdapterId, ...], BeforeValidator(_array)]

    @field_validator("trusted_adapter_ids")
    @classmethod
    def unique_ids(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(set(value)) != len(value):
            raise ValueError("duplicate_trusted_adapter")
        return value
