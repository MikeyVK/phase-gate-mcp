# pgmcp:v1 id=pytest_unit_test pv=1.0.0 pf=PbcHYV4rwlUcaINu sf=KoFPQ3-cAAWFeesb

"""Native configuration layers inherit fields without external sources or input mutation."""

# Standard library
from copy import deepcopy

# Third party
import pytest
from pydantic_settings import (
    DotEnvSettingsSource,
    EnvSettingsSource,
    PydanticBaseSettingsSource,
    SecretsSettingsSource,
)

# Project
from mcp_server.config.composition import compose_configuration


def test_updates_nested_fields_and_adds_objects_without_losing_inheritance() -> None:
    "Only supplied fields change; existing siblings and other sections inherit."
    defaults = {
        "checks": {
            "lint": {"adapter_id": "ruff", "timeout": 60},
            "format": {"adapter_id": "ruff", "timeout": 30},
        },
        "enabled": True,
    }
    override = {
        "checks": {
            "lint": {"timeout": 90},
            "types": {"adapter_id": "mypy", "timeout": 120},
        },
    }
    assert compose_configuration(defaults, override) == {
        "checks": {
            "lint": {"adapter_id": "ruff", "timeout": 90},
            "format": {"adapter_id": "ruff", "timeout": 30},
            "types": {"adapter_id": "mypy", "timeout": 120},
        },
        "enabled": True,
    }


@pytest.mark.parametrize("value", [["second", "first", "second"], [], None])
def test_replaces_leaf_values_literally(value: list[str] | None) -> None:
    "Lists replace as a whole, retain order/duplicates, and null remains null."
    defaults = {"options": {"value": ["inherited"], "enabled": True}}
    override = {"options": {"value": value}}
    assert compose_configuration(defaults, override) == {
        "options": {"value": value, "enabled": True}
    }


@pytest.mark.parametrize("override", [None, {}])
def test_absent_or_empty_override_inherits_defaults(override: dict[str, object] | None) -> None:
    "No supplied changes preserve the complete basis."
    defaults = {"options": {"values": ["first", "second"]}}
    assert compose_configuration(defaults, override) == defaults


def test_composition_detaches_inherited_and_overridden_values() -> None:
    "Composition and later result mutation leave both input trees intact."
    defaults = {"inherited": ["original"], "options": {"keep": True}}
    override = {"options": {"added": ["workspace"]}}
    before = deepcopy((defaults, override))
    result = compose_configuration(defaults, override)
    assert (defaults, override) == before

    inherited = result["inherited"]
    options = result["options"]
    assert isinstance(inherited, list)
    assert isinstance(options, dict)
    added = options["added"]
    assert isinstance(added, list)
    inherited.append("changed")
    added.append("changed")
    assert (defaults, override) == before


def test_external_settings_sources_are_not_executed(monkeypatch: pytest.MonkeyPatch) -> None:
    "Environment, dotenv and secret sources cannot participate in composition."

    def reject_source(_source: PydanticBaseSettingsSource) -> dict[str, object]:
        raise AssertionError("An external settings source was executed")

    for source_type in (EnvSettingsSource, DotEnvSettingsSource, SecretsSettingsSource):
        monkeypatch.setattr(source_type, "__call__", reject_source)

    assert compose_configuration({"setting": "basis"}, {"setting": "workspace"}) == {
        "setting": "workspace"
    }
