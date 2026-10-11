# pgmcp:v1 id=pytest_integration_test pv=1.0.0 pf=4obIYmqMTT5tMpqf sf=2JPaeqdf6mSOUgvn

"""Delivered data packages retain values and keep native and consumer admission distinct."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from shutil import copytree

import pytest
import yaml
from jsonschema.exceptions import ValidationError as ContextError
from pydantic import JsonValue

from mcp_server.config.validator import ConfigValidator
from mcp_server.core.interfaces.artifact_header_reader import HeaderReadStatus
from mcp_server.core.interfaces.template_catalog import thaw_json
from mcp_server.services.artifact_header_reader import ArtifactHeaderReader
from mcp_server.services.template_contract_loader import TemplateContractLoader
from tests.mcp_server.fixtures.delivered_templates import DeliveredTemplate, load_delivered_template

DIALECT = "https://json-schema.org/draft/2020-12/schema"


def delivered(tmp_path: Path, repo: Path, template_id: str) -> DeliveredTemplate:
    suite = repo / ".pgmcp/template_suite"
    return load_delivered_template(
        source_suite=suite,
        source_package=suite / template_id,
        config_root=repo / ".pgmcp/config",
        destination=tmp_path / "delivered",
        template_id=template_id,
    )


def native_check(repo: Path, target: Path, *, mode: str) -> None:
    args = (
        ["--check-metaschema"]
        if mode == "metaschema"
        else [
            "--schemafile",
            str(repo / ".pgmcp/config/check_schemas" / f"{mode}.schema.json"),
        ]
    )
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "check_jsonschema",
            *args,
            "--force-filetype",
            "yaml" if mode == "yaml_configuration" else "json",
            "--output-format",
            "JSON",
            str(target),
        ],
        capture_output=True,
        timeout=30,
    )
    assert result.returncode == 0, (result.stdout, result.stderr)
    assert json.loads(result.stdout)["status"] == "ok"


@pytest.mark.parametrize("populated", [False, True], ids=["minimal", "populated"])
def test_yaml_roundtrip_native_and_comments(
    tmp_path: Path, pytestconfig: pytest.Config, populated: bool
) -> None:
    package = delivered(tmp_path, pytestconfig.rootpath, "yaml_configuration")
    data: dict[str, JsonValue] = {}
    context: dict[str, JsonValue] = {"data": data}
    if populated:
        data.update(
            {
                "enabled": False,
                "count": 0,
                "nothing": None,
                "empty_list": [],
                "empty_map": {},
                "nested": {"values": [True, 1.25, "null", "false", "01", "2026-10-11"]},
                "locale.key": "yes",
                "雪": "café",
                "line\nkey": "key remains text",
                "multiline": "first\nsecond\n",
                "carriage": "first\r\nsecond\r",
                "control": "\x01\t",
                "literal": "# comment: [text]",
            }
        )
        context["header_comment"] = "Authored note\nsecond line"
    rendered = package.renderer.render("yaml_configuration", context, package.provenance)
    parsed = yaml.safe_load(rendered)
    assert parsed == data
    if populated:
        assert type(parsed["enabled"]) is bool
        assert type(parsed["count"]) is int
        assert type(parsed["nested"]["values"][1]) is float
        assert all(isinstance(value, str) for value in parsed["nested"]["values"][2:])
    assert rendered.endswith("\n") and not rendered.endswith("\n\n")
    if populated:
        assert "# Authored note\n# second line" in rendered
    else:
        assert rendered.count("#") == 1
    identity = ArtifactHeaderReader().read(rendered)
    assert identity.status is HeaderReadStatus.RECOGNIZED
    assert identity.provenance is not None and identity.provenance.id == "yaml_configuration"
    target = tmp_path / "ordinary.yaml"
    target.write_text(rendered, encoding="utf-8")
    native_check(pytestconfig.rootpath, target, mode="yaml_configuration")
    empty = package.renderer.render(
        "yaml_configuration", {"data": {}, "header_comment": ""}, package.provenance
    )
    assert "\n#\n" in empty and yaml.safe_load(empty) == {}


@pytest.mark.parametrize("populated", [False, True], ids=["minimal", "populated"])
def test_schema_roundtrip_native_and_identity(
    tmp_path: Path, pytestconfig: pytest.Config, populated: bool
) -> None:
    package = delivered(tmp_path, pytestconfig.rootpath, "json_schema")
    source: dict[str, JsonValue] = {"$schema": DIALECT}
    if populated:
        source.update(
            {
                "$id": "https://example.invalid/node.schema.json",
                "$anchor": "node",
                "description": "Authored description\nwith café",
                "type": "object",
                "properties": {
                    "label": {"type": "string", "$comment": "Authored nested annotation"},
                    "child": {"$ref": "#"},
                    "disabled": False,
                },
                "$defs": {"enabled": True},
            }
        )
    rendered = package.renderer.render("json_schema", {"schema": source}, package.provenance)
    parsed = json.loads(rendered)
    assert next(iter(parsed)) == "$comment"
    identity = ArtifactHeaderReader().read(rendered)
    assert identity.status is HeaderReadStatus.RECOGNIZED
    assert identity.provenance is not None and identity.provenance.id == "json_schema"
    assert parsed.pop("$comment").startswith("pgmcp:v1 id=json_schema ")
    assert parsed == source
    assert rendered.endswith("\n") and not rendered.endswith("\n\n")
    target = tmp_path / "node.schema.json"
    target.write_text(rendered, encoding="utf-8")
    native_check(pytestconfig.rootpath, target, mode="json_schema_source")
    native_check(pytestconfig.rootpath, target, mode="metaschema")


@pytest.mark.parametrize(
    ("template_id", "context"),
    [
        ("yaml_configuration", {"data": [], "header_comment": "note"}),
        ("yaml_configuration", {"data": {}, "name": "unadmitted"}),
        ("json_schema", {"schema": {"type": "object"}}),
        ("json_schema", {"schema": {"$schema": DIALECT, "$comment": "caller"}}),
        ("json_schema", {"schema": {"$schema": DIALECT}, "title": "unadmitted"}),
    ],
    ids=["yaml-root", "yaml-extra", "schema-dialect", "schema-reserved", "schema-extra"],
)
def test_data_context_rejects_unadmitted_envelopes(
    tmp_path: Path, pytestconfig: pytest.Config, template_id: str, context: dict[str, JsonValue]
) -> None:
    package = delivered(tmp_path, pytestconfig.rootpath, template_id)
    with pytest.raises(ContextError):
        package.renderer.render(template_id, context, package.provenance)


def test_generated_schema_is_consumed_and_validates_instances(
    tmp_path: Path, pytestconfig: pytest.Config
) -> None:
    package = delivered(tmp_path, pytestconfig.rootpath, "json_schema")
    source: dict[str, JsonValue] = {
        "$schema": DIALECT,
        "type": "object",
        "additionalProperties": False,
        "required": ["enabled"],
        "properties": {"enabled": {"type": "boolean"}},
    }
    consumer_suite = tmp_path / "consumer suite"
    schema_path = consumer_suite / "consumer/context.schema.json"
    schema_path.parent.mkdir(parents=True)
    schema_path.write_text(
        package.renderer.render("json_schema", {"schema": source}, package.provenance),
        encoding="utf-8",
    )
    prepared = TemplateContractLoader(consumer_suite).load_context_schema(schema_path)
    validator = ConfigValidator()
    assert thaw_json(validator.validate_template_context(prepared, {"enabled": False})) == {
        "enabled": False
    }
    for invalid in ({"enabled": "false"}, {}, {"enabled": True, "extra": 1}):
        with pytest.raises(ContextError):
            validator.validate_template_context(prepared, invalid)
    source["$id"] = "https://example.invalid/source.schema.json"
    schema_path.write_text(
        package.renderer.render("json_schema", {"schema": source}, package.provenance),
        encoding="utf-8",
    )
    native_check(pytestconfig.rootpath, schema_path, mode="metaschema")
    with pytest.raises(ValueError, match="unsupported_schema_keyword"):
        TemplateContractLoader(consumer_suite).load_context_schema(schema_path)


def test_suite_only_yaml_extension_uses_delivered_generic_capability(
    tmp_path: Path, pytestconfig: pytest.Config
) -> None:
    repo = pytestconfig.rootpath
    suite = repo / ".pgmcp/template_suite"
    source_package = tmp_path / "authored package"
    copytree(suite / "yaml_configuration", source_package)
    manifest_path = source_package / "manifest.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["template_id"] = "custom.locale"
    manifest_path.write_text(yaml.safe_dump(manifest), encoding="utf-8")
    package = load_delivered_template(
        source_suite=suite,
        source_package=source_package,
        config_root=repo / ".pgmcp/config",
        destination=tmp_path / "delivered",
        template_id="custom.locale",
    )
    values: dict[str, JsonValue] = {"ordinary.key": "Localized text", "answer": "yes"}
    output = package.renderer.render("custom.locale", {"data": values}, package.provenance)
    assert yaml.safe_load(output) == values
    identity = ArtifactHeaderReader().read(output)
    assert identity.provenance is not None and identity.provenance.id == "custom.locale"
    target = tmp_path / "locale.yaml"
    target.write_text(output, encoding="utf-8")
    native_check(repo, target, mode="yaml_configuration")
