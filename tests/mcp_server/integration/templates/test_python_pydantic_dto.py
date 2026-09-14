"""Delivered DTO package conformance through catalog admission and native Python facts."""

from __future__ import annotations

import ast
from copy import deepcopy
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from shutil import copytree
from types import MappingProxyType

import pytest
from jinja2 import DictLoader, Environment, StrictUndefined
from jsonschema.exceptions import ValidationError as ContextError
from pydantic import JsonValue

from mcp_server.config.loader import ConfigLoader
from mcp_server.config.validator import ConfigValidator
from mcp_server.core.interfaces.artifact_header_reader import HeaderReadStatus
from mcp_server.core.interfaces.template_catalog import FrozenJsonObject, freeze_json
from mcp_server.services.artifact_header_reader import ArtifactHeaderReader
from mcp_server.services.artifact_identity import ArtifactIdentity
from mcp_server.services.template_catalog import (
    TemplateCatalog,
    TemplateCatalogLoader,
    TemplateCatalogRenderer,
    TemplateInputValidator,
)
from mcp_server.services.template_contract_loader import TemplateContractLoader
from mcp_server.services.template_engine import TemplateEngine
from mcp_server.services.template_graph import TemplateGraphResolver
from tests.mcp_server.integration.adapters.test_python_syntax import (
    SyntaxPackage,
    invoke,
    request,
    syntax_package,
)

__all__ = ["syntax_package"]


@dataclass(frozen=True)
class DeliveredDto:
    catalog: TemplateCatalog
    renderer: TemplateCatalogRenderer
    provenance: FrozenJsonObject


@pytest.fixture
def delivered_dto(tmp_path: Path, pytestconfig: pytest.Config) -> DeliveredDto:
    suite = tmp_path / "explicit suite"
    source = pytestconfig.rootpath / ".pgmcp/template_suite"
    copytree(source / "shared", suite / "shared")
    copytree(source / "python_pydantic_dto", suite / "opaque package location")
    contracts = TemplateContractLoader(suite)
    config = ConfigLoader(
        pytestconfig.rootpath / ".pgmcp/config",
        suite,
        context_schema_reader=contracts.load_context_schema,
    )
    validator = ConfigValidator()
    parser = Environment()
    graph = TemplateGraphResolver(suite, parser.parse)
    provenance_schema = freeze_json(ArtifactIdentity.model_json_schema())
    assert isinstance(provenance_schema, FrozenJsonObject)
    inputs = TemplateInputValidator(parser.parse, provenance_schema)
    checks = config.load_checks_config()
    catalog = TemplateCatalogLoader(
        suite,
        read_manifest=config.load_template_manifest,
        read_version=config.load_template_version,
        read_policy=config.load_template_policy,
        read_schema=config.load_template_context_schema,
        validate_policy=partial(
            validator.validate_template_policy,
            profiles=frozenset(name for name, _ in checks.profiles),
        ),
        resolve_graph=graph.resolve,
        validate_inputs=inputs.validate,
    ).load()
    selected = catalog.get("python_pydantic_dto")
    assert selected.policy.persistence == "workspace"
    profile = dict(checks.profiles)[selected.policy.output_profile]
    assert profile.checks == ("python_syntax",)
    engine = TemplateEngine(
        environment=Environment(
            loader=DictLoader(
                MappingProxyType(
                    {item.name: item.content.decode("utf-8") for item in catalog.graph.sources}
                )
            ),
            undefined=StrictUndefined,
            keep_trailing_newline=True,
        )
    )
    renderer = TemplateCatalogRenderer(
        catalog,
        validate_context=validator.validate_template_context,
        render_context=engine.render_context,
    )
    provenance = freeze_json(
        ArtifactIdentity(
            id=selected.manifest.template_id, pv=selected.version, pf="a" * 16, sf="b" * 16
        ).model_dump(mode="json")
    )
    assert isinstance(provenance, FrozenJsonObject)
    return DeliveredDto(catalog, renderer, provenance)


def parse_model(output: str) -> tuple[ast.Module, ast.ClassDef, dict[str | None, object]]:
    tree = ast.parse(output)
    compile(tree, "<delivered-dto>", "exec")
    classes = [item for item in tree.body if isinstance(item, ast.ClassDef)]
    assert len(classes) == 1
    model = classes[0]
    assert [ast.unparse(base) for base in model.bases] == ["BaseModel"]
    config = next(item for item in model.body if isinstance(item, ast.Assign))
    assert [ast.unparse(target) for target in config.targets] == ["model_config"]
    assert isinstance(config.value, ast.Call)
    options = {item.arg: ast.literal_eval(item.value) for item in config.value.keywords}
    assert options["extra"] == "forbid" and options["frozen"] is True
    return tree, model, options


@pytest.mark.parametrize(
    ("extra", "examples"),
    [
        ({}, None),
        ({"fields": [], "examples": []}, None),
        ({"examples": [{"unmatched": False}]}, [{"unmatched": False}]),
    ],
)
def test_empty_dto_is_documented_immutable_and_native_syntax_valid(
    delivered_dto: DeliveredDto,
    syntax_package: SyntaxPackage,
    tmp_path: Path,
    extra: dict[str, JsonValue],
    examples: JsonValue,
) -> None:
    context = {"class_name": "exact_name", "description": "An explicitly empty DTO.", **extra}
    output = delivered_dto.renderer.render("python_pydantic_dto", context, delivered_dto.provenance)
    tree, model, options = parse_model(output)
    assert model.name == "exact_name"
    assert ast.get_docstring(tree) == ast.get_docstring(model) == context["description"]
    assert not any(isinstance(item, ast.AnnAssign) for item in model.body)
    if examples is None:
        assert "json_schema_extra" not in options
    else:
        assert options["json_schema_extra"] == {"examples": examples}
    header = ArtifactHeaderReader().read(output)
    assert header.status is HeaderReadStatus.RECOGNIZED
    assert header.provenance is not None and header.provenance.id == "python_pydantic_dto"
    code, response = invoke(syntax_package, tmp_path, request(tmp_path / "absent.py", output))
    assert code == 0 and response["decision"] == {"status": "passed"}
    assert not (tmp_path / "absent.py").exists()


def test_populated_dto_preserves_explicit_values_constraints_imports_and_examples(
    delivered_dto: DeliveredDto, syntax_package: SyntaxPackage, tmp_path: Path
) -> None:
    fields: list[JsonValue] = [
        {
            "name": "label",
            "type": "str",
            "description": "Required label",
            "min_length": 0,
            "max_length": 20,
            "pattern": "^item",
        },
        {"name": "enabled", "type": "bool", "description": "Feature flag", "default": False},
        {
            "name": "limit",
            "type": "int",
            "description": "Exact zero",
            "default": 0,
            "ge": 0,
            "gt": -1,
            "le": 10,
            "lt": 11,
        },
        {
            "name": "data",
            "type": "object",
            "description": "Nested data",
            "default": [False, 0, None, 'quotes 😀 " and \\', {"key": None}],
        },
        {
            "name": "counter",
            "type": "collections.Counter",
            "description": "Fresh counter",
            "default_factory": "collections.Counter",
        },
    ]
    examples: list[JsonValue] = [{"does_not_match_fields": [False, 0, None]}]
    context: dict[str, JsonValue] = {
        "class_name": "exact_name",
        "description": 'Class "documentation" 😀\nsecond line',
        "module_description": "A separate module description",
        "imports": {
            "stdlib": [{"kind": "import", "module": "collections"}],
            "project": [
                {"kind": "from", "module": "__future__", "names": [{"name": "annotations"}]},
                {"kind": "import", "module": "missing_dependency", "alias": "ExplicitAlias"},
            ],
        },
        "fields": fields,
        "examples": examples,
    }
    before = deepcopy(context)
    output = delivered_dto.renderer.render("python_pydantic_dto", context, delivered_dto.provenance)
    tree, model, options = parse_model(output)
    assert context == before
    assert ast.get_docstring(tree) == context["module_description"]
    assert ast.get_docstring(model) == context["description"]
    assert options["json_schema_extra"] == {"examples": examples}
    imports = [item for item in tree.body if isinstance(item, (ast.Import, ast.ImportFrom))]
    assert isinstance(imports[0], ast.ImportFrom) and imports[0].module == "__future__"
    assert any(
        isinstance(item, ast.Import)
        and [(alias.name, alias.asname) for alias in item.names]
        == [("missing_dependency", "ExplicitAlias")]
        for item in imports
    )
    emitted = [item for item in model.body if isinstance(item, ast.AnnAssign)]
    assert len(emitted) == len(fields)
    for node, expected in zip(emitted, fields, strict=True):
        assert isinstance(expected, dict)
        assert isinstance(node.target, ast.Name) and node.target.id == expected["name"]
        assert ast.unparse(node.annotation) == expected["type"]
        assert isinstance(node.value, ast.Call) and ast.unparse(node.value.func) == "Field"
        values = {
            item.arg: ast.unparse(item.value)
            if item.arg == "default_factory"
            else ast.literal_eval(item.value)
            for item in node.value.keywords
        }
        assert values == {
            key: value for key, value in expected.items() if key not in {"name", "type"}
        }
    assert not any(isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) for item in model.body)
    code, response = invoke(syntax_package, tmp_path, request(tmp_path / "generated.py", output))
    assert code == 0 and response["decision"] == {"status": "passed"}
    assert not (tmp_path / "generated.py").exists()


def test_context_rejects_legacy_and_invalid_concrete_combinations(
    delivered_dto: DeliveredDto,
) -> None:
    base: dict[str, JsonValue] = {"class_name": "Example", "description": "Explicit DTO"}
    field: dict[str, JsonValue] = {"name": "value", "type": "int", "description": "Value"}
    invalid: list[dict[str, JsonValue]] = [
        {"class_name": "Example"},
        {**base, "description": ""},
        {**base, "class_name": "class"},
        {**base, "frozen": False},
        {**base, "layer": "DTOs"},
        {**base, "fields": None},
        {**base, "imports": None},
        {**base, "module_description": None},
        {**base, "fields": [field]},
        {**base, "fields": [field], "examples": []},
        {**base, "examples": [False]},
        {**base, "fields": [{"name": "value", "type": "int"}], "examples": [{}]},
        {**base, "fields": [{**field, "default": 0, "default_factory": "int"}], "examples": [{}]},
        {**base, "fields": [{**field, "extra_args": "strict=True"}], "examples": [{}]},
    ]
    for name in (
        "_private",
        "model_config",
        "Config",
        "Field",
        "model_dump",
        "model_dump_json",
        "model_validate",
        "model_validate_json",
        "model_validate_strings",
    ):
        invalid.append({**base, "fields": [{**field, "name": name}], "examples": [{}]})
    for context in invalid:
        with pytest.raises(ContextError):
            delivered_dto.renderer.render("python_pydantic_dto", context, delivered_dto.provenance)
    # These are native warnings or valid ordinary names, not reserved binding collisions.
    for name in ("model_dump_custom", "ConfigDict", "BaseModel"):
        output = delivered_dto.renderer.render(
            "python_pydantic_dto",
            {**base, "fields": [{**field, "name": name}], "examples": [{}]},
            delivered_dto.provenance,
        )
        parse_model(output)


def test_native_annotation_failure_is_not_claimed_as_valid_output(
    delivered_dto: DeliveredDto, syntax_package: SyntaxPackage, tmp_path: Path
) -> None:
    output = delivered_dto.renderer.render(
        "python_pydantic_dto",
        {
            "class_name": "BrokenAnnotation",
            "description": "Native syntax remains the language checker responsibility",
            "fields": [{"name": "value", "type": "list[", "description": "Incomplete annotation"}],
            "examples": [{}],
        },
        delivered_dto.provenance,
    )
    code, response = invoke(syntax_package, tmp_path, request(tmp_path / "invalid.py", output))
    assert code == 1
    decision = response["decision"]
    assert isinstance(decision, dict) and decision["status"] == "failed"
    assert not (tmp_path / "invalid.py").exists()
