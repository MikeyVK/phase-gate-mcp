"""Compose real delivered package snapshots for family-level conformance tests."""

from __future__ import annotations

from dataclasses import dataclass
from functools import partial
from pathlib import Path
from shutil import copytree
from types import MappingProxyType

from jinja2 import DictLoader, Environment, StrictUndefined

from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.checks_config import ChecksConfig
from mcp_server.config.validator import ConfigValidator
from mcp_server.core.interfaces.template_catalog import FrozenJsonObject, freeze_json
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


@dataclass(frozen=True)
class DeliveredTemplate:
    catalog: TemplateCatalog
    renderer: TemplateCatalogRenderer
    provenance: FrozenJsonObject
    checks: ChecksConfig


def load_delivered_template(
    *,
    source_suite: Path,
    source_package: Path,
    config_root: Path,
    destination: Path,
    template_id: str,
) -> DeliveredTemplate:
    copytree(source_suite / "shared", destination / "shared")
    copytree(source_package, destination / "opaque package location")
    contracts = TemplateContractLoader(destination)
    config = ConfigLoader(
        config_root, destination, context_schema_reader=contracts.load_context_schema
    )
    validator = ConfigValidator()
    parser = Environment()
    graph = TemplateGraphResolver(destination, parser.parse)
    provenance_schema = freeze_json(ArtifactIdentity.model_json_schema())
    assert isinstance(provenance_schema, FrozenJsonObject)
    inputs = TemplateInputValidator(parser.parse, provenance_schema)
    checks = config.load_checks_config()
    catalog = TemplateCatalogLoader(
        destination,
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
    selected = catalog.get(template_id)
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
    return DeliveredTemplate(catalog, renderer, provenance, checks)
