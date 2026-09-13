# tests/mcp_server/unit/services/test_template_catalog.py
# template=unit_test version=8825c0bb created=2026-09-13T16:00Z updated=
"""Admit real package files and exercise shared catalog/schema/renderer selections."""

from __future__ import annotations

import json
from dataclasses import FrozenInstanceError
from functools import partial
from types import MappingProxyType

import pytest
from jinja2 import DictLoader, Environment, StrictUndefined, UndefinedError
from jsonschema.exceptions import ValidationError as ContextError
from pydantic import ValidationError

from mcp_server.config.loader import ConfigLoader
from mcp_server.config.validator import ConfigValidator
from mcp_server.core.exceptions import MCPError
from mcp_server.core.interfaces.template_catalog import FrozenJsonObject, freeze_json, thaw_json
from mcp_server.services.template_catalog import (
    TemplateCatalog,
    TemplateCatalogLoader,
    TemplateCatalogRenderer,
    TemplateInputValidator,
)
from mcp_server.services.template_contract_loader import DRAFT_2020_12, TemplateContractLoader
from mcp_server.services.template_engine import TemplateEngine
from mcp_server.services.template_graph import TemplateGraphResolver
from tests.mcp_server.fixtures.suite_roots import SuiteRoots, write_package_tree


def package_files(directory: str, template_id: str) -> dict[str, bytes]:
    """Return explicitly authored test contracts, without fixture-level config fallback."""
    schema = {
        "$schema": DRAFT_2020_12,
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "value": {"type": "integer"},
            "flag": {"type": "boolean"},
            "empty": {"type": ["string", "null"]},
        },
        "required": ["value", "flag"],
    }
    return {
        f"{directory}/manifest.yaml": (
            f"template_id: {template_id}\npurpose: Test artifact\n".encode()
        ),
        f"{directory}/.version": b"1.2.3\n",
        f"{directory}/policy.yaml": b"output_profile: text\npersistence: workspace\n",
        f"{directory}/context.schema.json": json.dumps(schema).encode(),
        f"{directory}/template.jinja2": b'{% extends "shared/templates/base.jinja2" %}'
        b"{% block body %}{{ content.value }}|{{ content.flag }}|"
        b"{% if content.empty is not defined %}absent{% elif content.empty is none %}null"
        b"{% else %}present:{{ content.empty }}{% endif %}{% endblock %}",
        "shared/templates/base.jinja2": b"BEGIN[{% block body %}{% endblock %}]END",
    }


def catalog_loader(roots: SuiteRoots) -> TemplateCatalogLoader:
    reader = TemplateContractLoader(roots.templates)
    config = ConfigLoader(
        roots.config, roots.templates, context_schema_reader=reader.load_context_schema
    )
    validator = ConfigValidator()
    environment = Environment()
    graph = TemplateGraphResolver(roots.templates, environment.parse)
    provenance = freeze_json(
        {"type": "object", "properties": {"id": {"type": "string"}}, "additionalProperties": False}
    )
    assert isinstance(provenance, FrozenJsonObject)
    inputs = TemplateInputValidator(environment.parse, provenance)
    return TemplateCatalogLoader(
        roots.templates,
        read_manifest=config.load_template_manifest,
        read_version=config.load_template_version,
        read_policy=config.load_template_policy,
        read_schema=config.load_template_context_schema,
        validate_policy=partial(validator.validate_template_policy, profiles=frozenset({"text"})),
        resolve_graph=graph.resolve,
        validate_inputs=inputs.validate,
    )


def catalog_renderer(catalog: TemplateCatalog) -> TemplateCatalogRenderer:
    sources = MappingProxyType(
        {source.name: source.content.decode("utf-8-sig") for source in catalog.graph.sources}
    )
    engine = TemplateEngine(
        environment=Environment(
            loader=DictLoader(sources),
            undefined=StrictUndefined,
        )
    )
    return TemplateCatalogRenderer(
        catalog,
        validate_context=ConfigValidator().validate_template_context,
        render_context=engine.render_context,
    )


class TestTemplateCatalog:
    @pytest.mark.parametrize(
        ("extra", "suffix"),
        [({}, "absent"), ({"empty": ""}, "present:"), ({"empty": None}, "null")],
    )
    def test_one_snapshot_drives_selection_schema_and_rendering(
        self,
        suite_roots: SuiteRoots,
        extra: dict[str, str | None],
        suffix: str,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        write_package_tree(
            suite_roots.templates, package_files("opaque-location", "custom.artifact")
        )
        loader = catalog_loader(suite_roots)
        monkeypatch.chdir(suite_roots.temp)
        catalog = loader.load()
        selected = catalog.get("custom.artifact")
        assert selected.renderer == "opaque-location/template.jinja2"
        assert selected.manifest.purpose == "Test artifact"
        assert selected.version == "1.2.3"
        assert selected.policy.output_profile == "text"
        assert isinstance(thaw_json(selected.schema), dict)
        renderer = catalog_renderer(catalog)
        context = {"value": 0, "flag": False, **extra}
        before = dict(context)
        assert (
            renderer.render("custom.artifact", context, FrozenJsonObject(()))
            == f"BEGIN[0|False|{suffix}]END"
        )
        assert context == before
        with pytest.raises(ContextError):
            renderer.render(
                "custom.artifact", {**context, "file_name": "hidden"}, FrozenJsonObject(())
            )
        with pytest.raises(MCPError, match="template_selection_unknown"):
            catalog.get("opaque-location")
        with pytest.raises(FrozenInstanceError):
            catalog.packages = ()
        write_package_tree(suite_roots.templates, {"opaque-location/template.jinja2": b"Updated"})
        assert (
            renderer.render("custom.artifact", context, FrozenJsonObject(()))
            == f"BEGIN[0|False|{suffix}]END"
        )
        assert (
            catalog_renderer(loader.load()).render("custom.artifact", context, FrozenJsonObject(()))
            == "Updated"
        )

    @pytest.mark.parametrize(
        "missing",
        ["manifest.yaml", ".version", "policy.yaml", "context.schema.json", "template.jinja2"],
    )
    def test_missing_package_members_prevent_publication(
        self, suite_roots: SuiteRoots, missing: str
    ) -> None:
        files = package_files("pkg", "custom")
        del files[f"pkg/{missing}"]
        write_package_tree(suite_roots.templates, files)
        with pytest.raises(MCPError, match="template_package_member_invalid"):
            catalog_loader(suite_roots).load()

    @pytest.mark.parametrize(
        ("member", "payload"),
        [
            ("manifest.yaml", b"template_id: custom\npurpose: Artifact\ntype_id: legacy"),
            ("policy.yaml", b"output_profile: text\npersistence: inline"),
            (".version", b"01.2.3"),
            (".version", b" 1.2.3\n"),
            ("context.schema.json", b"{}"),
        ],
    )
    def test_invalid_authored_contracts_fail(
        self, suite_roots: SuiteRoots, member: str, payload: bytes
    ) -> None:
        files = package_files("pkg", "custom")
        files[f"pkg/{member}"] = payload
        write_package_tree(suite_roots.templates, files)
        with pytest.raises((ValueError, ValidationError)):
            catalog_loader(suite_roots).load()

    def test_duplicate_identity_and_unknown_profile_fail(self, suite_roots: SuiteRoots) -> None:
        write_package_tree(
            suite_roots.templates,
            {
                **package_files("one", "same-id"),
                **package_files("two", "same-id"),
            },
        )
        with pytest.raises(MCPError, match="template_identity_duplicate"):
            catalog_loader(suite_roots).load()
        write_package_tree(
            suite_roots.templates,
            {
                "two/manifest.yaml": b"template_id: second-id\npurpose: Artifact",
                "two/policy.yaml": b"output_profile: missing\npersistence: workspace",
            },
        )
        with pytest.raises(MCPError, match="template_output_profile_unknown"):
            catalog_loader(suite_roots).load()

    def test_undeclared_direct_directory_and_parallel_inventory_fail(
        self, suite_roots: SuiteRoots
    ) -> None:
        write_package_tree(suite_roots.templates, package_files("pkg", "custom"))
        (suite_roots.templates / "unregistered").mkdir()
        with pytest.raises(MCPError, match="template_package_member_invalid"):
            catalog_loader(suite_roots).load()
        write_package_tree(suite_roots.templates, {"templates.yaml": b"templates: []"})
        with pytest.raises(MCPError, match="duplicate_template_inventory"):
            catalog_loader(suite_roots).load()

    def test_direct_files_cannot_be_silently_omitted_from_inventory(
        self, suite_roots: SuiteRoots
    ) -> None:
        """Every non-shared direct child must be a complete concrete package."""
        write_package_tree(
            suite_roots.templates,
            {
                **package_files("pkg", "custom"),
                "incomplete-package.txt": b"not a package",
            },
        )
        with pytest.raises(MCPError, match="template_package_directory_required"):
            catalog_loader(suite_roots).load()

    @pytest.mark.parametrize(
        "source",
        [
            b"{{ content.undeclared }}",
            b"{{ content['undeclared'] }}",
            b"{{ file_name }}",
            b"{{ provenance.undeclared }}",
            b"{{ content.get('undeclared') }}",
            b"{% set alias = content %}{{ alias.undeclared }}",
        ],
    )
    def test_undeclared_renderer_inputs_prevent_publication(
        self, suite_roots: SuiteRoots, source: bytes
    ) -> None:
        files = package_files("pkg", "custom")
        files["shared/templates/base.jinja2"] = source
        write_package_tree(suite_roots.templates, files)
        with pytest.raises(MCPError, match="template_input_undeclared"):
            catalog_loader(suite_roots).load()

    @pytest.mark.parametrize("composition", ["allOf", "anyOf", "oneOf"])
    def test_composed_schema_nested_reads_and_local_scopes_remain_valid(
        self, suite_roots: SuiteRoots, composition: str
    ) -> None:
        """Schema declarations coexist with Jinja methods, aliases, loops and macros."""
        files = package_files("pkg", "custom")
        schema = json.loads(files["pkg/context.schema.json"])
        schema[composition] = [{"properties": schema.pop("properties")}]
        schema.pop("additionalProperties")
        schema["unevaluatedProperties"] = False
        schema[composition][0]["properties"]["rows"] = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"label": {"type": "string"}},
                "additionalProperties": False,
            },
        }
        files["pkg/context.schema.json"] = json.dumps(schema).encode()
        files["pkg/template.jinja2"] = (
            b'{% import "shared/templates/macros.jinja2" as helpers %}'
            b"{% set alias = content %}{{ alias.get('value') }}|"
            b"{% for row in content.rows %}{{ row.label }}{% endfor %}|"
            b"{% with content = {'local': 'scoped'} %}{{ content.local }}{% endwith %}|"
            b"{{ helpers.label({'local': 'macro'}) }}|{{ provenance.id }}"
        )
        files["shared/templates/macros.jinja2"] = (
            b"{% macro label(content) %}{{ content.local }}{% endmacro %}"
        )
        write_package_tree(suite_roots.templates, files)
        catalog = catalog_loader(suite_roots).load()
        provenance = freeze_json({"id": "custom"})
        assert isinstance(provenance, FrozenJsonObject)
        assert (
            catalog_renderer(catalog).render(
                "custom", {"value": 0, "flag": False, "rows": [{"label": "row"}]}, provenance
            )
            == "0|row|scoped|macro|custom"
        )
        files["pkg/template.jinja2"] = b"{% for row in content.rows %}{{ row.missing }}{% endfor %}"
        write_package_tree(
            suite_roots.templates, {"pkg/template.jinja2": files["pkg/template.jinja2"]}
        )
        with pytest.raises(MCPError, match="template_input_undeclared"):
            catalog_loader(suite_roots).load()

    def test_shared_inputs_are_checked_for_each_selectable_package(
        self, suite_roots: SuiteRoots
    ) -> None:
        files = {**package_files("one", "one"), **package_files("two", "two")}
        schema = json.loads(files["two/context.schema.json"])
        schema["properties"].pop("empty")
        files["two/context.schema.json"] = json.dumps(schema).encode()
        write_package_tree(suite_roots.templates, files)
        with pytest.raises(MCPError, match="template_input_undeclared"):
            catalog_loader(suite_roots).load()

    def test_loop_local_cannot_hide_an_undefined_external_input(
        self, suite_roots: SuiteRoots
    ) -> None:
        files = package_files("pkg", "custom")
        files["pkg/template.jinja2"] = (
            b"{% for file_name in ['local'] %}{{ file_name }}{% endfor %}{{ file_name }}"
        )
        write_package_tree(suite_roots.templates, files)
        with pytest.raises(MCPError, match="template_input_undeclared"):
            catalog_loader(suite_roots).load()

    def test_include_receives_only_its_visible_local_bindings(
        self, suite_roots: SuiteRoots
    ) -> None:
        files = package_files("pkg", "custom")
        files["pkg/template.jinja2"] = (
            b"{% for label in ['local'] %}"
            b'{% include "shared/templates/label.jinja2" %}{% endfor %}'
        )
        files["shared/templates/label.jinja2"] = b"{{ label }}"
        write_package_tree(suite_roots.templates, files)
        catalog = catalog_loader(suite_roots).load()
        assert (
            catalog_renderer(catalog).render(
                "custom", {"value": 0, "flag": False}, FrozenJsonObject(())
            )
            == "local"
        )

        write_package_tree(
            suite_roots.templates,
            {
                "pkg/template.jinja2": b"{% set label = 'local' %}"
                b'{% include "shared/templates/label.jinja2" without context %}',
            },
        )
        with pytest.raises(MCPError, match="template_input_undeclared"):
            catalog_loader(suite_roots).load()

    def test_inherited_macro_is_an_internal_binding(self, suite_roots: SuiteRoots) -> None:
        files = package_files("pkg", "custom")
        files["pkg/template.jinja2"] = (
            b'{% extends "shared/templates/base.jinja2" %}'
            b"{% block body %}{{ label(content.value) }}{% endblock %}"
        )
        files["shared/templates/base.jinja2"] = (
            b"{% macro label(value) %}prefix{{ value }}{% endmacro %}{% block body %}{% endblock %}"
        )
        native = Environment(
            loader=DictLoader(
                {name: value.decode() for name, value in files.items() if name.endswith(".jinja2")}
            ),
            undefined=StrictUndefined,
        )
        context = {"value": 0, "flag": False}
        assert native.get_template("pkg/template.jinja2").render(content=context) == "prefix0"
        write_package_tree(suite_roots.templates, files)
        catalog = catalog_loader(suite_roots).load()
        assert (
            catalog_renderer(catalog).render("custom", context, FrozenJsonObject(())) == "prefix0"
        )

    @pytest.mark.parametrize(
        ("source", "base", "expected"),
        [
            (
                b'{% extends "shared/templates/base.jinja2" %}{% set title = content.value %}',
                b"{{ title }}",
                "0",
            ),
            (
                b"{% macro label(content, value=content.local) %}{{ value }}{% endmacro %}"
                b"{{ label({'local':'ok'}) }}",
                b"",
                "ok",
            ),
            (
                b'{% extends "shared/templates/base.jinja2" %}{% set title = content.value %}'
                b"{% block body %}{{ title }}{% endblock %}",
                b"{% block body %}{% endblock %}",
                "0",
            ),
            (
                b"{% macro wrap() %}{{ caller({'local':'ok'}) }}{% endmacro %}"
                b"{% call(content) wrap() %}{{ content.local }}{% endcall %}",
                b"",
                "ok",
            ),
        ],
    )
    def test_native_scope_order_is_preserved(
        self, suite_roots: SuiteRoots, source: bytes, base: bytes, expected: str
    ) -> None:
        files = package_files("pkg", "custom")
        files["pkg/template.jinja2"] = source
        files["shared/templates/base.jinja2"] = base
        native = Environment(
            loader=DictLoader(
                {name: value.decode() for name, value in files.items() if name.endswith(".jinja2")}
            ),
            undefined=StrictUndefined,
        )
        context = {"value": 0, "flag": False}
        assert native.get_template("pkg/template.jinja2").render(content=context) == expected
        write_package_tree(suite_roots.templates, files)
        catalog = catalog_loader(suite_roots).load()
        assert catalog_renderer(catalog).render("custom", context, FrozenJsonObject(())) == expected

    def test_later_assignment_cannot_hide_an_earlier_external_read(
        self, suite_roots: SuiteRoots
    ) -> None:
        source = "{{ file_name }}{% set file_name = 'local' %}"
        with pytest.raises(UndefinedError):
            Environment(undefined=StrictUndefined).from_string(source).render()
        files = package_files("pkg", "custom")
        files["pkg/template.jinja2"] = source.encode()
        write_package_tree(suite_roots.templates, files)
        with pytest.raises(MCPError, match="template_input_undeclared"):
            catalog_loader(suite_roots).load()

    def test_parent_binding_cannot_supply_an_earlier_child_root_read(
        self, suite_roots: SuiteRoots
    ) -> None:
        sources = {
            "pkg/template.jinja2": '{{ file_name }}{% extends "shared/templates/base.jinja2" %}',
            "shared/templates/base.jinja2": "{% set file_name = 'local' %}body",
        }
        with pytest.raises(UndefinedError):
            Environment(loader=DictLoader(sources), undefined=StrictUndefined).get_template(
                "pkg/template.jinja2"
            ).render()
        files = package_files("pkg", "custom")
        files.update({name: source.encode() for name, source in sources.items()})
        write_package_tree(suite_roots.templates, files)
        with pytest.raises(MCPError, match="template_input_undeclared"):
            catalog_loader(suite_roots).load()

    @pytest.mark.parametrize("scoped", [True, False], ids=["scoped", "unscoped"])
    def test_block_visibility_matches_native_scope(
        self, suite_roots: SuiteRoots, scoped: bool
    ) -> None:
        modifier = " scoped" if scoped else ""
        source = (
            "{% for label in ['ok'] %}{% block body"
            + modifier
            + " %}{{ label }}{% endblock %}{% endfor %}"
        )
        native = Environment(undefined=StrictUndefined).from_string(source)
        files = package_files("pkg", "custom")
        files["pkg/template.jinja2"] = source.encode()
        write_package_tree(suite_roots.templates, files)
        if scoped:
            assert native.render() == "ok"
            catalog = catalog_loader(suite_roots).load()
            assert (
                catalog_renderer(catalog).render(
                    "custom", {"value": 0, "flag": False}, FrozenJsonObject(())
                )
                == "ok"
            )
        else:
            with pytest.raises(UndefinedError):
                native.render()
            with pytest.raises(MCPError, match="template_input_undeclared"):
                catalog_loader(suite_roots).load()

    @pytest.mark.parametrize(
        "source",
        [
            "{% filter upper %}{% set file_name = 'local' %}{% endfilter %}{{ file_name }}",
            "{% set captured %}{% set file_name = 'local' %}{% endset %}{{ file_name }}",
        ],
        ids=["filter", "capture"],
    )
    def test_local_output_scope_cannot_export_an_input_binding(
        self, suite_roots: SuiteRoots, source: str
    ) -> None:
        with pytest.raises(UndefinedError):
            Environment(undefined=StrictUndefined).from_string(source).render()
        files = package_files("pkg", "custom")
        files["pkg/template.jinja2"] = source.encode()
        write_package_tree(suite_roots.templates, files)
        with pytest.raises(MCPError, match="template_input_undeclared"):
            catalog_loader(suite_roots).load()
