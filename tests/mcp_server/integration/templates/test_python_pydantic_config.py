"""Delivered configuration package conformance through catalog admission and native Python facts."""

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
class DeliveredConfig:
    catalog: TemplateCatalog
    renderer: TemplateCatalogRenderer
    provenance: FrozenJsonObject


@pytest.fixture
def delivered_config(tmp_path: Path, pytestconfig: pytest.Config) -> DeliveredConfig:
    suite = tmp_path / "explicit suite"
    source = pytestconfig.rootpath / ".pgmcp/template_suite"
    copytree(source / "shared", suite / "shared")
    copytree(source / "python_pydantic_config", suite / "opaque package location")
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
    selected = catalog.get("python_pydantic_config")
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
    return DeliveredConfig(catalog, renderer, provenance)


def parse_config(output: str) -> tuple[ast.Module, ast.ClassDef, dict[str | None, object]]:
    tree = ast.parse(output)
    compile(tree, "<delivered-config>", "exec")
    classes = [item for item in tree.body if isinstance(item, ast.ClassDef)]
    assert len(classes) == 1
    model = classes[0]
    assert [ast.unparse(base) for base in model.bases] == ["BaseModel"]
    config = next(item for item in model.body if isinstance(item, ast.Assign))
    assert [ast.unparse(target) for target in config.targets] == ["model_config"]
    assert isinstance(config.value, ast.Call)
    options = {item.arg: ast.literal_eval(item.value) for item in config.value.keywords}
    assert options["extra"] == "forbid"
    return tree, model, options


def test_empty_configuration_respects_explicit_frozen_choice(
    delivered_config: DeliveredConfig, syntax_package: SyntaxPackage, tmp_path: Path
) -> None:
    context = {"class_name": "exact_settings", "description": "Explicit settings.", "frozen": False}
    output = delivered_config.renderer.render(
        "python_pydantic_config", context, delivered_config.provenance
    )
    tree, model, options = parse_config(output)
    assert model.name == "exact_settings"
    assert ast.get_docstring(tree) == ast.get_docstring(model) == context["description"]
    assert options["frozen"] is False
    assert "json_schema_extra" not in options
    assert not any(isinstance(item, (ast.AnnAssign, ast.FunctionDef)) for item in model.body)
    header = ArtifactHeaderReader().read(output)
    assert header.status is HeaderReadStatus.RECOGNIZED
    assert header.provenance is not None and header.provenance.id == "python_pydantic_config"
    code, response = invoke(syntax_package, tmp_path, request(tmp_path / "settings.py", output))
    assert code == 0 and response["decision"] == {"status": "passed"}
    assert not (tmp_path / "settings.py").exists()
