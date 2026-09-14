"""Integration evidence for complete candidate staging and proposal admission."""

from __future__ import annotations

import json
import os
import subprocess
from collections.abc import Iterable
from pathlib import Path
from typing import Literal

import pytest
from jinja2 import Environment

from mcp_server.config.loader import ConfigLoader
from mcp_server.config.validator import ConfigValidator
from mcp_server.core.exceptions import MCPError
from mcp_server.core.interfaces.template_catalog import FrozenJsonObject, freeze_json
from mcp_server.execution.catalog import AdapterCatalogLoader, FileAdapterPackageReader
from mcp_server.services.artifact_identity import ArtifactIdentity
from mcp_server.services.template_catalog import TemplateCatalogLoader, TemplateInputValidator
from mcp_server.services.template_components import ComponentSelection, select_components
from mcp_server.services.template_contract_loader import DRAFT_2020_12, TemplateContractLoader
from mcp_server.services.template_graph import TemplateGraphResolver
from mcp_server.services.template_proposal import (
    SuiteSnapshot,
    TemplateProposalService,
    admit_template_suite,
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


def _write_config(
    root: Path,
    profiles: Iterable[str],
    *,
    adapter_id: str = "python_syntax",
) -> None:
    configured = ", ".join(f"{profile}: {{checks: [syntax]}}" for profile in profiles)
    write_package_tree(
        root,
        {
            "adapters.yaml": b"trusted_adapter_ids: []\n",
            "checks.yaml": (
                "checks:\n"
                "  syntax:\n"
                f"    adapter_id: {adapter_id}\n"
                "    capability: syntax\n"
                "    timeout_seconds: 30\n"
                "    default_args: []\n"
                f"profiles: {{{configured}}}\n"
                "profiles_by_extension: {}\n"
                "run_checks: {}\n"
            ).encode(),
        },
    )

    write_package_tree(
        root.parent / "official-adapters" / "syntax",
        {
            "manifest.yaml": (
                b"adapter_id: python_syntax\nversion: 1.0.0\nfiles: [check.py]\n"
                b"roles:\n  check:\n    contract_version: 1\n"
                b"    entrypoint: {executable: unavailable_native, args: []}\n"
                b"    capabilities:\n"
                b"      syntax: {inputs: [content, selection], requires_file: false}\n"
            ),
            "check.py": b"raise RuntimeError('admission must not execute native tools')\n",
        },
    )


def _admit_suite(root: Path, config_root: Path) -> SuiteSnapshot:
    validator = ConfigValidator()
    environment = Environment()
    provenance = freeze_json(ArtifactIdentity.model_json_schema())
    assert isinstance(provenance, FrozenJsonObject)

    def create_config(config_path: Path, suite_path: Path) -> ConfigLoader:
        contracts = TemplateContractLoader(suite_path)
        return ConfigLoader(
            config_path, suite_path, context_schema_reader=contracts.load_context_schema
        )

    def create_catalog(
        suite_path: Path, config: ConfigLoader, profiles: frozenset[str]
    ) -> TemplateCatalogLoader:
        return TemplateCatalogLoader(
            suite_path,
            read_manifest=config.load_template_manifest,
            read_version=config.load_template_version,
            read_policy=config.load_template_policy,
            read_schema=config.load_template_context_schema,
            validate_policy=lambda policy: validator.validate_template_policy(policy, profiles),
            resolve_graph=TemplateGraphResolver(suite_path, environment.parse).resolve,
            validate_inputs=TemplateInputValidator(environment.parse, provenance).validate,
        )

    def create_adapters(config: ConfigLoader) -> AdapterCatalogLoader:
        return AdapterCatalogLoader(
            config_root.parent / "official-adapters",
            config_root.parent / "workspace-adapters",
            config.load_adapter_trust(),
            read_manifest=config.load_adapter_manifest,
            files=FileAdapterPackageReader(),
            resolve_program=lambda _: None,
            windows=os.name == "nt",
        )

    return admit_template_suite(
        root,
        config_root,
        create_config=create_config,
        create_catalog=create_catalog,
        create_adapters=create_adapters,
        validator=validator,
    )


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
        admit=_admit_suite,
    )


def _selections(
    actual: SuiteSnapshot,
    candidate: SuiteSnapshot,
    *,
    adopted_shared_source: Literal["actual", "candidate"] = "candidate",
) -> tuple[ComponentSelection, ...]:
    actual_map = {state.key: state for state in (actual.evidence.shared, *actual.evidence.packages)}
    candidate_map = {
        state.key: state for state in (candidate.evidence.shared, *candidate.evidence.packages)
    }
    adopted = {key: candidate_map[key] for key in actual_map.keys() & candidate_map.keys()}
    if adopted_shared_source == "actual":
        adopted[("shared", "shared")] = actual_map[("shared", "shared")]
    return select_components(adopted, actual_map, candidate_map)


def test_flat_supersession_and_mixed_proposal_use_complete_admitted_snapshots(
    tmp_path: Path,
) -> None:
    actual = tmp_path / "active" / "templates"
    supplied = tmp_path / "release" / "templates"
    staged = tmp_path / "workspace" / ".pgmcp" / "upgrade"
    proposal = tmp_path / "workspace" / ".pgmcp" / "proposal"
    config = tmp_path / "owner-config"
    write_package_tree(actual, _package_files("actual-dir", "demo", body=b"local"))
    write_package_tree(
        supplied,
        {
            **_package_files("candidate-dir", "demo", body=b"upstream"),
            **_package_files("new-dir", "new", body=b"new"),
        },
    )
    _write_config(config, ("text",))
    write_package_tree(staged, {"stale.txt": b"old"})
    actual_before = {
        path.relative_to(actual): path.read_bytes() for path in actual.rglob("*") if path.is_file()
    }
    config_before = (config / "checks.yaml").read_bytes()
    service = _service(actual, staged, proposal, config)
    actual_snapshot = service.admit(actual)
    supplied_snapshot = _admit_suite(supplied, config)

    assert service.stage_candidate(supplied) is None
    candidate_snapshot = service.admit(staged)
    assert service.materialize_proposal(_selections(actual_snapshot, supplied_snapshot)) is None
    proposal_snapshot = service.admit(proposal)

    assert not (staged / "stale.txt").exists()
    assert (staged / "candidate-dir" / "manifest.yaml").is_file()
    assert not (staged / "templates").exists()
    assert (proposal / "actual-dir" / "template.jinja2").read_bytes() == b"local"
    assert (proposal / "new-dir" / "template.jinja2").read_bytes() == b"new"
    assert candidate_snapshot.sources
    assert [item.component_id for item in proposal_snapshot.evidence.packages] == [
        "demo",
        "new",
    ]
    assert actual_before == {
        path.relative_to(actual): path.read_bytes() for path in actual.rglob("*") if path.is_file()
    }
    assert (config / "checks.yaml").read_bytes() == config_before


def test_candidate_invalid_is_distinct_and_preserves_existing_stage(tmp_path: Path) -> None:
    actual = tmp_path / "actual"
    supplied = tmp_path / "supplied"
    staged = tmp_path / "upgrade"
    proposal = tmp_path / "proposal"
    config = tmp_path / "external-config"
    write_package_tree(actual, _package_files("pkg", "demo"))
    write_package_tree(supplied, _package_files("pkg", "demo", profile="missing"))
    write_package_tree(staged, {"retained.txt": b"keep"})
    _write_config(config, ("text",))
    service = _service(actual, staged, proposal, config)

    with pytest.raises(MCPError, match="template_candidate_invalid") as raised:
        service.stage_candidate(supplied)

    assert raised.value.params["config_root"] == str(config.resolve())
    assert raised.value.params["cause"] == "template_output_profile_unknown"
    assert raised.value.params["template_id"] == "demo"
    assert raised.value.params["output_profile"] == "missing"
    assert raised.value.params["policy_source"] == "pkg/policy.yaml"
    assert raised.value.params["config_source"] == "checks.yaml"
    assert (staged / "retained.txt").read_bytes() == b"keep"
    assert not proposal.exists()

    _write_config(config, ("text", "missing"))
    assert service.stage_candidate(supplied) is None
    assert (staged / "pkg" / "manifest.yaml").is_file()


def test_candidate_unknown_adapter_is_invalid_and_preserves_stage(tmp_path: Path) -> None:
    actual = tmp_path / "actual"
    supplied = tmp_path / "supplied"
    staged = tmp_path / "upgrade"
    proposal = tmp_path / "proposal"
    config = tmp_path / "external-config"
    write_package_tree(actual, _package_files("pkg", "demo"))
    write_package_tree(supplied, _package_files("pkg", "demo"))
    write_package_tree(staged, {"retained.txt": b"keep"})
    _write_config(config, ("text",), adapter_id="missing_adapter")

    with pytest.raises(MCPError, match="template_candidate_invalid"):
        _service(actual, staged, proposal, config).stage_candidate(supplied)

    assert (staged / "retained.txt").read_bytes() == b"keep"
    assert not proposal.exists()


def test_proposal_invalid_is_distinct_and_retains_valid_candidate(tmp_path: Path) -> None:
    actual = tmp_path / "actual"
    supplied = tmp_path / "supplied"
    staged = tmp_path / "upgrade"
    proposal = tmp_path / "proposal"
    config = tmp_path / "effective-config"
    old_reference = b"{% include 'shared/templates/old.jinja2' %}{{ content.value }}"
    write_package_tree(
        actual,
        {
            **_package_files("local", "demo", body=old_reference),
            "shared/templates/old.jinja2": b"old",
        },
    )
    write_package_tree(
        supplied,
        _package_files("upstream", "demo", body=b"{{ content.value }}"),
    )
    _write_config(config, ("text",))
    actual_snapshot = _admit_suite(actual, config)
    candidate_snapshot = _admit_suite(supplied, config)
    service = _service(actual, staged, proposal, config)
    service.stage_candidate(supplied)

    selections = _selections(
        actual_snapshot,
        candidate_snapshot,
        adopted_shared_source="actual",
    )
    shared_selection = next(selection for selection in selections if selection.kind == "shared")
    assert shared_selection.selected_source == "candidate"
    package_selection = next(selection for selection in selections if selection.kind == "package")
    assert package_selection.selected_source == "actual"

    with pytest.raises(MCPError, match="template_proposal_invalid") as raised:
        service.materialize_proposal(selections)

    assert raised.value.params["cause"] == "template_source_unavailable"
    assert (staged / "upstream" / "manifest.yaml").is_file()
    assert not proposal.exists()


@pytest.mark.parametrize(
    ("actual_relative", "candidate_relative", "proposal_relative"),
    [
        ("workspace/.upgrade.incoming", "workspace/upgrade", "workspace/proposal"),
        ("workspace/active", "workspace/upgrade", "workspace/upgrade/proposal"),
    ],
)
def test_owned_write_path_overlap_preserves_existing_trees(
    tmp_path: Path,
    actual_relative: str,
    candidate_relative: str,
    proposal_relative: str,
) -> None:
    actual = tmp_path / actual_relative
    supplied = tmp_path / "release" / "templates"
    candidate = tmp_path / candidate_relative
    proposal = tmp_path / proposal_relative
    config = tmp_path / "owner-config"
    write_package_tree(actual, _package_files("pkg", "demo"))
    write_package_tree(supplied, _package_files("pkg", "demo", body=b"candidate"))
    write_package_tree(candidate, {"retained.txt": b"keep"})
    _write_config(config, ("text",))
    actual_before = {
        path.relative_to(actual): path.read_bytes() for path in actual.rglob("*") if path.is_file()
    }
    candidate_before = {
        path.relative_to(candidate): path.read_bytes()
        for path in candidate.rglob("*")
        if path.is_file()
    }

    with pytest.raises(MCPError, match="template_proposal_roots_overlap"):
        _service(actual, candidate, proposal, config)

    assert actual_before == {
        path.relative_to(actual): path.read_bytes() for path in actual.rglob("*") if path.is_file()
    }
    assert candidate_before == {
        path.relative_to(candidate): path.read_bytes()
        for path in candidate.rglob("*")
        if path.is_file()
    }


def test_candidate_link_is_rejected_before_supersession(tmp_path: Path) -> None:
    actual = tmp_path / "actual"
    supplied = tmp_path / "supplied"
    staged = tmp_path / "upgrade"
    proposal = tmp_path / "proposal"
    config = tmp_path / "config"
    outside = tmp_path / "outside"
    write_package_tree(actual, _package_files("pkg", "demo"))
    write_package_tree(supplied, _package_files("pkg", "demo"))
    write_package_tree(staged, {"retained.txt": b"keep"})
    _write_config(config, ("text",))
    write_package_tree(outside, {"outside.txt": b"outside"})
    link = supplied / "pkg" / "escape"
    _directory_link(link, outside)

    with pytest.raises(MCPError, match="template_candidate_invalid") as raised:
        _service(actual, staged, proposal, config).stage_candidate(supplied)

    assert raised.value.params["cause"] == "template_suite_symlink_escape"
    assert (staged / "retained.txt").read_bytes() == b"keep"


def _directory_link(link: Path, target: Path) -> None:
    if os.name == "nt":
        subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link), str(target)],
            check=True,
            capture_output=True,
        )
    else:
        link.symlink_to(target, target_is_directory=True)


def test_writable_endpoint_alias_preserves_target(tmp_path: Path) -> None:
    actual = tmp_path / "actual"
    staged = tmp_path / "upgrade"
    proposal = tmp_path / "proposal"
    config = tmp_path / "config"
    outside = tmp_path / "owner-data"
    write_package_tree(outside, {"retained.txt": b"keep"})
    _directory_link(staged, outside)

    with pytest.raises(MCPError, match="template_writable_endpoint_alias"):
        _service(actual, staged, proposal, config)

    assert (outside / "retained.txt").read_bytes() == b"keep"
    assert staged.is_dir()
