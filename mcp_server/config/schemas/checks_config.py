"""Strict immutable check bindings and output-profile configuration."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    StrictInt,
    StrictStr,
    StringConstraints,
    field_serializer,
    model_validator,
)

from mcp_server.config.schemas.adapter_manifest import AdapterId, CapabilityId

CheckId = AdapterId
ProfileId = AdapterId


def _sequence(value: object) -> object:
    if isinstance(value, list):
        return tuple(value)
    return value


def _mapping_items(value: object) -> object:
    if isinstance(value, Mapping):
        return tuple(value.items())
    if isinstance(value, tuple):
        items = value
        for item in items:
            if not isinstance(item, (tuple, list)) or len(item) != 2:
                raise ValueError("mapping_items_required")
        return tuple((item[0], item[1]) for item in items)
    raise ValueError("mapping_required")


def _extension(value: object) -> object:
    if not isinstance(value, str):
        return value
    if (
        "\x00" in value
        or len(value) < 2
        or not value.startswith(".")
        or "/" in value
        or "\\" in value
        or any(char in value for char in "*?[]")
    ):
        raise ValueError("invalid_extension")
    return value


ExtensionKey = Annotated[str, BeforeValidator(_extension), StringConstraints(strict=True)]
StrictStringTuple = Annotated[tuple[StrictStr, ...], BeforeValidator(_sequence)]


class _ChecksBase(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")


class ConfiguredCheck(_ChecksBase):
    adapter_id: AdapterId
    capability: CapabilityId
    timeout_seconds: Annotated[StrictInt, Field(gt=0)]
    default_args: StrictStringTuple


class CheckProfile(_ChecksBase):
    checks: Annotated[tuple[CheckId, ...], BeforeValidator(_sequence), Field(min_length=1)]

    @model_validator(mode="after")
    def validate_unique_checks(self) -> CheckProfile:
        if len(set(self.checks)) != len(self.checks):
            raise ValueError("duplicate_profile_check")
        return self


class RunChecksDefaults(_ChecksBase):
    default_profile: ProfileId | None = None

    @model_validator(mode="after")
    def reject_explicit_null(self) -> RunChecksDefaults:
        if "default_profile" in self.model_fields_set and self.default_profile is None:
            raise ValueError("default_profile_must_be_omitted")
        return self


class ChecksConfig(_ChecksBase):
    checks: Annotated[tuple[tuple[CheckId, ConfiguredCheck], ...], BeforeValidator(_mapping_items)]
    profiles: Annotated[tuple[tuple[ProfileId, CheckProfile], ...], BeforeValidator(_mapping_items)]
    profiles_by_extension: Annotated[
        tuple[tuple[ExtensionKey, ProfileId], ...], BeforeValidator(_mapping_items)
    ]
    run_checks: RunChecksDefaults

    @field_serializer("checks")
    def serialize_checks(
        self, value: tuple[tuple[CheckId, ConfiguredCheck], ...]
    ) -> dict[str, ConfiguredCheck]:
        return dict(value)

    @field_serializer("profiles")
    def serialize_profiles(
        self, value: tuple[tuple[ProfileId, CheckProfile], ...]
    ) -> dict[str, CheckProfile]:
        return dict(value)

    @field_serializer("profiles_by_extension")
    def serialize_extension_profiles(
        self, value: tuple[tuple[ExtensionKey, ProfileId], ...]
    ) -> dict[str, str]:
        return dict(value)

    @model_validator(mode="after")
    def validate_references(self) -> ChecksConfig:
        checks = dict(self.checks)
        profiles = dict(self.profiles)
        extension_profiles = dict(self.profiles_by_extension)

        if len(checks) != len(self.checks):
            raise ValueError("duplicate_check_id")
        if len(profiles) != len(self.profiles):
            raise ValueError("duplicate_profile_id")
        if len(extension_profiles) != len(self.profiles_by_extension):
            raise ValueError("duplicate_extension")
        if len({extension.casefold() for extension in extension_profiles}) != len(
            extension_profiles
        ):
            raise ValueError("duplicate_extension_casefold")

        unknown_checks = {
            check_id
            for profile in profiles.values()
            for check_id in profile.checks
            if check_id not in checks
        }
        if unknown_checks:
            raise ValueError("profile_check_reference_unknown")

        if any(profile_id not in profiles for profile_id in extension_profiles.values()):
            raise ValueError("extension_profile_reference_unknown")

        if (
            self.run_checks.default_profile is not None
            and self.run_checks.default_profile not in profiles
        ):
            raise ValueError("default_profile_reference_unknown")
        return self

    def match_for_filename(self, filename: str) -> tuple[str, str] | None:
        if not isinstance(filename, str) or not filename or "/" in filename or "\\" in filename:
            raise ValueError("basename_required")
        if "\x00" in filename:
            raise ValueError("nul_in_filename")

        folded_filename = filename.casefold()
        matches = [
            (extension.casefold(), extension, profile_id)
            for extension, profile_id in self.profiles_by_extension
            if len(folded_filename) > len(extension.casefold())
            and folded_filename.endswith(extension.casefold())
        ]
        if not matches:
            return None
        _, extension, profile_id = max(matches, key=lambda item: len(item[0]))
        return extension, profile_id

    def profile_for_filename(self, filename: str) -> str | None:
        match = self.match_for_filename(filename)
        return None if match is None else match[1]
