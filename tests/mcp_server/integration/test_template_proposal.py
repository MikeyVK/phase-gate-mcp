"""Integration evidence for complete candidate staging and proposal admission."""

from __future__ import annotations

import json
import os
from collections.abc import Iterable
from functools import partial
from pathlib import Path

import pytest
from jinja2 import Environment

from mcp_server.config.loader import ConfigLoader
from mcp_server.config.validator import ConfigValidator
from mcp_server.core.exceptions import MCPError
from mcp_server.core.interfaces.template_catalog import FrozenJsonObject, freeze_json
from mcp_server.services.artifact_identity import GenerationPackage, GenerationSource
from mcp_server.services.installation_state import ValidatedSuiteEvidence
from mcp_server.services.template_catalog import TemplateCatalogLoader, TemplateInputValidator
from mcp_server.services.template_components import (
    ComponentSelection,
    component_fingerprints,
    select_components,
)
from mcp_server.services.template_contract_loader import DRAFT_2020_12, TemplateContractLoader
from mcp_server.services.template_graph import TemplateGraphResolver
from mcp_server.services.template_proposal import (
    ComponentLocation,
    SuiteSnapshot,
    TemplateProposalService,
)
from tests.mcp_server.fixtures.suite_roots import write_package_tree


def _package_files(
    directory: str,
    template_id: str,
    *,
    profile: str = "text",
    body: bytes = b"{{ content.value }}",
) -> dict[str, bytes]:
    schema = {
        "$schema": DRAFT_2020_12,
        "type": "object",
        "additionalProperties": False,
        "properties": {"value": {"type": "integer"}},
        "required": ["value"],
    }
    return {
        f"{directory}/manifest.yaml": (
            f"template_id: {template_id}\npurpose: Test artifact\n".encode()
        ),
        f"{directory}/.version": b"1.2.3\n",
        f"{directory}/policy.yaml": (
            f"output_profile: {profile}\npersistence: workspace\n".encode()
        ),
        f"{directory}/context.schema.json": json.dumps(schema).encode(),
        f"{directory}/template.jinja2": body,
        "shared/templates/base.jinja2": b"shared",
    }


def _write_config(root: Path, profiles: Iterable[str]) -> None:
    checks = ", ".join(f"{profile}: {{checks: [syntax]}}" for profile in profiles)
    write_package_tree(
        root,
        {
            "checks.yaml": (
                "checks:\n"
                "  syntax:\n"
                "    adapter_id: python_syntax\n"
                "    capability: syntax\n"
                "    timeout_seconds: 30\n"
                "    default_args: []\n"
                f"profiles: {{{checks}}}\n"
                "profiles_by_extension: {}\n"
                "run_checks: {}\n"
            ).encode()
        },
    )


def _sources(root: Path) -> tuple[GenerationSource, ...]:
    return tuple(
        GenerationSource(path=path.relative_to(root).as_posix(), content=path.read_bytes())
        for path in sorted(root.rglob("*"))
        if path.is_file()
    )


def _admit(root: Path, config_root: Path) -> SuiteSnapshot:
    reader = TemplateContractLoader(root)
    config = ConfigLoader(config_root, root, context_schema_reader=reader.load_context_schema)
    configured_profiles = frozenset(name for name, _ in config.load_checks_config().profiles)
    validator = ConfigValidator()
    environment = Environment()
    graph = TemplateGraphResolver(root, environment.parse)
    provenance = freeze_json(
        {"type": "object", "properties": {"id": {"type": "string"}}, "additionalProperties": False}
    )
    assert isinstance(provenance, FrozenJsonObject)
    catalog = TemplateCatalogLoader(
        root,
        read_manifest=config.load_template_manifest,
        read_version=config.load_template_version,
        read_policy=config.load_template_policy,
        read_schema=config.load_template_context_schema,
        validate_policy=partial(
            validator.validate_template_policy, profiles=configured_profiles
        ),
        resolve_graph=graph.resolve,
        validate_inputs=TemplateInputValidator(environment.parse, provenance).validate,
    ).load()
    packages = tuple(
        GenerationPackage(
            manifest=package.manifest,
            version=package.version,
            directory=package.renderer.partition("/")[0],
        )
        for package in catalog.packages
    )
    states = component_fingerprints(packages, _sources(root))
    evidence = ValidatedSuiteEvidence(
        shared=next(state for state in states if state.kind == "shared"),
        packages=tuple(state for state in states if state.kind == "package"),
    )
    locations = (
        ComponentLocation(kind="shared", component_id="shared", directory="shared"),
        *(
            ComponentLocation(
                kind="package",
                component_id=package.manifest.template_id,
                directory=package.directory,
            )
            for package in packages
        ),
    )
    return SuiteSnapshot(root=root, evidence=evidence, locations=locations)


def _service(
    actual: Path,
    staged: Path,
    proposal: Path,
    config: Path,
) -> TemplateProposalService:
    return TemplateProposalService(
        actual_root=actual,
        candidate_root=staged,
        proposal_root=proposal,
        effective_config_root=config,
        admit=_admit,
    )


def _selections(actual: SuiteSnapshot, candidate: SuiteSnapshot) -> tuple[ComponentSelection, ...]:
    actual_map = {
        state.key: state for state in (actual.evidence.shared, *actual.evidence.packages)
    }
    candidate_map = {
        state.key: state for state in (candidate.evidence.shared, *candidate.evidence.packages)
    }
    return select_components(actual_map, actual_map, candidate_map)


def test_stages_flat_candidate_supersedes_stale_and_admits_mixed_proposal(
    tmp_path: Path,
) -> None:
    actual = tmp_path / "active" / "templates"
    supplied = tmp_path / "release" / "templates"
    staged = tmp_path / "workspace" / ".pgmcp" / "upgrade"
    proposal = tmp_path / "workspace" / ".pgmcp" / "proposal"
    external_config = tmp_path / "owner-config"
    write_package_tree(actual, _package_files("actual-dir", "demo", body=b"local"))
    write_package_tree(
        supplied,
        {
            **_package_files("candidate-dir", "demo", body=b"upstream"),
            **_package_files("new-dir", "new", body=b"new"),
        },
    )
    _write_config(external_config, ("text",))
    write_package_tree(staged, {"stale.txt": b"old"})
    actual_before = {path.relative_to(actual): path.read_bytes() for path in actual.rglob("*") if path.is_file()}
    config_before = (external_config / "checks.yaml").read_bytes()

    actual_snapshot = _admit(actual, external_config)
    candidate_snapshot = _admit(supplied, external_config)
    result = _service(actual, staged, proposal, external_config).prepare(
        supplied_candidate_root=supplied,
        selections=_selections(actual_snapshot, candidate_snapshot),
    )

    assert not (staged / "stale.txt").exists()
    assert (staged / "candidate-dir" / "manifest.yaml").is_file()
    assert not (staged / "templates").exists()
    assert (proposal / "actual-dir" / "template.jinja2").read_bytes() == b"local"
    assert (proposal / "new-dir" / "template.jinja2").read_bytes() == b"new"
    assert result.candidate.root == staged.resolve()
    assert result.proposal.root == proposal.resolve()
    assert [item.component_id for item in result.proposal.evidence.packages] == ["demo", "new"]
    assert actual_before == {
        path.relative_to(actual): path.read_bytes() for path in actual.rglob("*") if path.is_file()
    }
    assert (external_config / "checks.yaml").read_bytes() == config_before


def test_invalid_candidate_preserves_existing_stage_and_reports_effective_config(
    tmp_path: Path,
) -> None:
    actual = tmp_path / "actual"
    supplied = tmp_path / "supplied"
    staged = tmp_path / "upgrade"
    proposal = tmp_path / "proposal"
    config = tmp_path / "external-config"
    write_package_tree(actual, _package_files("pkg", "demo"))
    write_package_tree(supplied, _package_files("pkg", "demo", profile="missing"))
    write_package_tree(staged, {"retained.txt": b"keep"})
    _write_config(config, ("text",))

    with pytest.raises(MCPError, match="template_candidate_invalid") as raised:
        _service(actual, staged, proposal, config).prepare(
            supplied_candidate_root=supplied,
            selections=(),
        )

    assert raised.value.params["config_root"] == str(config.resolve())
    assert raised.value.params["cause"] == "template_output_profile_unknown"
    assert (staged / "retained.txt").read_bytes() == b"keep"
    assert not proposal.exists()


def test_invalid_mixed_proposal_is_distinct_and_retains_valid_candidate(
    tmp_path: Path,
) -> None:
    actual = tmp_path / "actual"
    supplied = tmp_path / "supplied"
    staged = tmp_path / "upgrade"
    proposal = tmp_path / "proposal"
    broad_config = tmp_path / "broad-config"
    effective_config = tmp_path / "effective-config"
    write_package_tree(actual, _package_files("local", "demo", profile="local"))
    write_package_tree(
        supplied,
        {
            **_package_files("upstream", "demo"),
            **_package_files("added", "new"),
        },
    )
    _write_config(broad_config, ("text", "local"))
    _write_config(effective_config, ("text",))
    actual_snapshot = _admit(actual, broad_config)
    candidate_snapshot = _admit(supplied, effective_config)

    with pytest.raises(MCPError, match="template_proposal_invalid") as raised:
        _service(actual, staged, proposal, effective_config).prepare(
            supplied_candidate_root=supplied,
            selections=_selections(actual_snapshot, candidate_snapshot),
        )

    assert raised.value.params["config_root"] == str(effective_config.resolve())
    assert raised.value.params["cause"] == "template_output_profile_unknown"
    assert (staged / "upstream" / "manifest.yaml").is_file()
    assert not proposal.exists()


def test_candidate_symlink_escape_is_rejected_before_supersession(tmp_path: Path) -> None:
    actual = tmp_path / "actual"
    supplied = tmp_path / "supplied"
    staged = tmp_path / "upgrade"
    proposal = tmp_path / "proposal"
    config = tmp_path / "config"
    outside = tmp_path / "outside.txt"
    write_package_tree(actual, _package_files("pkg", "demo"))
    write_package_tree(supplied, _package_files("pkg", "demo"))
    write_package_tree(staged, {"retained.txt": b"keep"})
    _write_config(config, ("text",))
    outside.write_bytes(b"outside")
    link = supplied / "pkg" / "escape.txt"
    try:
        os.symlink(outside, link)
    except OSError:
        pytest.skip("symlink creation is unavailable on this host")

    with pytest.raises(MCPError, match="template_candidate_invalid") as raised:
        _service(actual, staged, proposal, config).prepare(
            supplied_candidate_root=supplied,
            selections=(),
        )

    assert raised.value.params["cause"] == "template_suite_symlink_escape"
    assert (staged / "retained.txt").read_bytes() == b"keep"
