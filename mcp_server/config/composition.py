# pgmcp:v1 id=python_pydantic_config pv=1.0.0 pf=TDVmp2pacKoBW_qk sf=KoFPQ3-cAAWFeesb

"""Compose explicit configuration layers through native Pydantic Settings sources."""

from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy

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
    return _ConfigurationSources(
        defaults=deepcopy(dict(defaults)),
        override=deepcopy(dict(override)) if override is not None else {},
    ).model_dump()
