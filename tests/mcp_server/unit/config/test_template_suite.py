# tests/mcp_server/unit/config/test_template_suite.py
# template=unit_test version=8825c0bb created=2026-09-13T15:00Z updated=
"""Public package-value admission and lossless immutable JSON transfer.

@layer: Tests (Unit)
@dependencies: pytest, pydantic, template package contracts
"""

from decimal import Decimal

import pytest
from pydantic import JsonValue, TypeAdapter, ValidationError

from mcp_server.config.schemas.template_suite import (
    TemplateId,
    TemplateManifest,
    TemplatePackageVersion,
    TemplatePolicy,
)
from mcp_server.core.interfaces.template_catalog import (
    FrozenJsonObject,
    FrozenJsonValue,
    freeze_json,
    thaw_json,
)


def test_manifest_contains_only_generation_identity_and_purpose() -> None:
    """An arbitrary valid selector needs no registry or physical directory name."""
    manifest = TemplateManifest(template_id="consumer-defined", purpose="  A caller capability  ")
    assert manifest.model_dump() == {
        "template_id": "consumer-defined",
        "purpose": "A caller capability",
    }
    schema = TemplateManifest.model_json_schema()
    assert set(schema["properties"]) == {"template_id", "purpose"}
    assert set(schema["required"]) == {"template_id", "purpose"}
    assert schema["additionalProperties"] is False
    with pytest.raises(ValidationError, match="frozen"):
        manifest.purpose = "Changed"


@pytest.mark.parametrize(
    "removed", ["type_id", "template_version", "context_schema", "state_machine"]
)
def test_manifest_rejects_removed_parallel_authorities(removed: str) -> None:
    with pytest.raises(ValidationError):
        TemplateManifest.model_validate(
            {"template_id": "arbitrary", "purpose": "A capability", removed: "legacy"}
        )


@pytest.mark.parametrize(
    "invalid",
    [
        "",
        "a" * 25,
        "two words",
        "line\nbreak",
        "trailing\n",
        "x=y",
        "a-->b",
        "a/*b",
        "a#b",
        "\x85",
        42,
    ],
)
def test_template_id_rejects_invalid_header_tokens(invalid: object) -> None:
    with pytest.raises(ValidationError):
        TypeAdapter(TemplateId).validate_python(invalid)


@pytest.mark.parametrize("valid", ["external-v7", "x" * 24, "Type_2", "démo"])
def test_template_id_accepts_non_registry_identifiers(valid: str) -> None:
    assert TypeAdapter(TemplateId).validate_python(valid) == valid


@pytest.mark.parametrize("valid", ["0.0.0", "12.34.56", "1.0.0-rc.1", "1.0.0+build", "1.2.3-0"])
def test_package_version_preserves_valid_bounded_semver(valid: str) -> None:
    assert TypeAdapter(TemplatePackageVersion).validate_python(valid) == valid


@pytest.mark.parametrize(
    "invalid",
    ["1.0", "01.0.0", "1.0.0-01", "1.0.0-", "1.0.0+", "1.0.0-a..b", "1.0.0-alpha.1", "1.0.0\n", 1],
)
def test_package_version_rejects_invalid_syntax_and_representation(invalid: object) -> None:
    with pytest.raises(ValidationError):
        TypeAdapter(TemplatePackageVersion).validate_python(invalid)


@pytest.mark.parametrize("persistence", ["workspace", "temporary"])
def test_policy_is_separate_required_closed_and_frozen(persistence: str) -> None:
    policy = TemplatePolicy.model_validate(
        {"output_profile": "selected-profile", "persistence": persistence}
    )
    assert policy.model_dump() == {
        "output_profile": "selected-profile",
        "persistence": persistence,
    }
    with pytest.raises(ValidationError, match="frozen"):
        policy.output_profile = "other"
    with pytest.raises(ValidationError):
        TemplatePolicy.model_validate({"output_profile": "selected-profile"})


@pytest.mark.parametrize(
    "payload",
    [
        {"output_profile": "", "persistence": "workspace"},
        {"output_profile": "profile", "persistence": "ephemeral"},
        {"output_profile": "profile", "persistence": "workspace", "strict_validation": True},
    ],
)
def test_policy_rejects_legacy_and_unknown_fields(payload: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        TemplatePolicy.model_validate(payload)


def test_json_transfer_preserves_presence_types_and_empty_values() -> None:
    nested: list[JsonValue] = [None, {"empty": ""}]
    source: dict[str, JsonValue] = {
        "false": False,
        "zero": 0,
        "number": 0.5,
        "null": None,
        "text": "",
        "array": [],
        "object": {},
        "nested": nested,
    }
    frozen = freeze_json(source)
    assert isinstance(frozen, FrozenJsonObject)
    assert "absent" not in frozen
    with pytest.raises(KeyError):
        _ = frozen["absent"]
    assert frozen["false"] is False
    assert type(frozen["zero"]) is int
    assert frozen["null"] is None
    assert frozen["array"] == ()
    expected = thaw_json(frozen)
    assert expected == source
    nested.append("later")
    source["injected"] = "later"
    assert thaw_json(frozen) == expected
    copy = thaw_json(frozen)
    assert isinstance(copy, dict)
    copy["injected"] = "detached output"
    assert "injected" not in frozen
    assert len(frozen) == 8
    assert isinstance(frozen["object"], FrozenJsonObject)


@pytest.mark.parametrize(
    "invalid",
    [
        float("nan"),
        float("inf"),
        -float("inf"),
        Decimal("1"),
        b"text",
        (1, 2),
        {1: "key"},
        object(),
    ],
)
def test_json_transfer_rejects_non_json_and_non_finite_values(invalid: object) -> None:
    with pytest.raises(ValidationError):
        freeze_json({"nested": [invalid]})


def test_json_transfer_rejects_cyclic_containers() -> None:
    cyclic: list[object] = []
    cyclic.append(cyclic)
    with pytest.raises(ValidationError):
        freeze_json(cyclic)


@pytest.mark.parametrize(
    "entries",
    [
        (("same", 1), ("same", 2)),
        (("value", float("inf")),),
        (("array", (float("nan"),)),),
    ],
)
def test_frozen_object_constructor_enforces_value_invariants(
    entries: tuple[tuple[str, FrozenJsonValue], ...],
) -> None:
    """Direct domain construction cannot introduce duplicate keys or non-finite values."""
    with pytest.raises(ValueError):
        FrozenJsonObject(entries)
