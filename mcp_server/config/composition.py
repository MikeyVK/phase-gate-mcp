# pgmcp:v1 id=python_pydantic_config pv=1.0.0 pf=TDVmp2pacKoBW_qk sf=KoFPQ3-cAAWFeesb

"""Compose explicit configuration layers through native Pydantic Settings sources."""

from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from typing import Any

from pydantic_settings import (
    BaseSettings,
    InitSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)


class _ConfigurationSources(BaseSettings):
    """Supply only caller-owned layers to the native source merge."""

    model_config = SettingsConfigDict(frozen=True, extra="allow")

    def __init__(self, *, defaults: dict[str, object], override: dict[str, object]) -> None:
        super().__init__(defaults=defaults, override=override)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        del env_settings, dotenv_settings, file_secret_settings
        layers = init_settings()
        return (
            InitSettingsSource(settings_cls, init_kwargs=layers["override"]),
            InitSettingsSource(settings_cls, init_kwargs=layers["defaults"]),
        )


def compose_configuration(
    defaults: Mapping[str, object],
    override: Mapping[str, object] | None,
) -> dict[str, object]:
    """Merge explicit layers without IO, ambient settings or shared input containers."""
    validate_complete_configuration(defaults)
    basis = deepcopy(dict(defaults))
    changes = deepcopy(dict(override)) if override is not None else {}
    _prepare_deletions(basis, changes, ())
    return _ConfigurationSources(defaults=basis, override=changes).model_dump()


def validate_complete_configuration(value: object, path: tuple[str, ...] = ()) -> None:
    """Reject reserved commands in complete sources and literal value lists."""
    if isinstance(value, dict):
        if "$delete" in value:
            raise ValueError(f"configuration_delete_command_not_allowed: {'.'.join(path)}")
        for key, child in value.items():
            validate_complete_configuration(child, (*path, str(key)))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            validate_complete_configuration(child, (*path, str(index)))


def _prepare_deletions(
    basis: dict[str, Any], changes: dict[str, Any], path: tuple[str, ...]
) -> None:
    """Remove tombstones on detached trees; leave all ordinary merging to Settings."""
    if "$delete" in changes:
        raise ValueError(f"configuration_delete_invalid_command: {'.'.join(path)}")
    for key, value in tuple(changes.items()):
        target = (*path, str(key))
        if not isinstance(value, dict):
            validate_complete_configuration(value, target)
            continue
        if "$delete" in value:
            if len(value) != 1 or value["$delete"] is not True:
                raise ValueError(f"configuration_delete_invalid_command: {'.'.join(target)}")
            if key not in basis:
                raise ValueError(f"configuration_delete_unknown_target: {'.'.join(target)}")
            del basis[key]
            del changes[key]
        else:
            inherited = basis.get(key)
            _prepare_deletions(inherited if isinstance(inherited, dict) else {}, value, target)
