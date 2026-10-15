# pgmcp:v1 id=pytest_unit_test pv=1.0.0 pf=PbcHYV4rwlUcaINu sf=KoFPQ3-cAAWFeesb

"""Native configuration layers inherit fields without external sources or input mutation."""

# Standard library
from copy import deepcopy

# Third party
import pytest
from pydantic import ValidationError
from pydantic_settings import (
    DotEnvSettingsSource,
    EnvSettingsSource,
    PydanticBaseSettingsSource,
    SecretsSettingsSource,
)

# Project
from mcp_server.config.composition import compose_configuration
from mcp_server.config.schemas.checks_config import ConfiguredCheck


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


def test_deletes_only_the_requested_inherited_member() -> None:
    defaults = {"checks": {"lint": {"timeout": 60}, "format": {"timeout": 30}}}
    override = {"checks": {"format": {"$delete": True}, "lint": {"timeout": 90}}}
    before = deepcopy((defaults, override))
    assert compose_configuration(defaults, override) == {"checks": {"lint": {"timeout": 90}}}
    assert (defaults, override) == before


@pytest.mark.parametrize(
    "defaults, override",
    [
        ({}, {"missing": {"$delete": True}}),
        ({"item": {}}, {"item": {"$delete": False}}),
        ({"item": {}}, {"item": {"$delete": True, "value": 1}}),
        ({"item": 1}, {"item": {"nested": {"$delete": True}}}),
        ({}, {"items": [{"$delete": True}]}),
        ({"item": {"$delete": True}}, {}),
    ],
)
def test_rejects_invalid_deletion_without_mutating_inputs(
    defaults: dict[str, object], override: dict[str, object]
) -> None:
    before = deepcopy((defaults, override))
    with pytest.raises(ValueError, match="configuration_delete"):
        compose_configuration(defaults, override)
    assert (defaults, override) == before


def test_deleted_fields_follow_existing_model_required_and_default_rules() -> None:
    defaults = {
        "adapter_id": "ruff",
        "capability": "lint",
        "timeout_seconds": 60,
        "default_args": [],
        "configuration_choice": "native_discovery",
    }
    optional = compose_configuration(defaults, {"configuration_choice": {"$delete": True}})
    assert ConfiguredCheck.model_validate(optional).configuration_choice is None
    required = compose_configuration(defaults, {"timeout_seconds": {"$delete": True}})
    with pytest.raises(ValidationError, match="timeout_seconds"):
        ConfiguredCheck.model_validate(required)
