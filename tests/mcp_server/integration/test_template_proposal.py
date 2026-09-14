"""Integration evidence for complete candidate staging and proposal admission."""

from __future__ import annotations

import json
import os
from collections.abc import Iterable
from pathlib import Path

import pytest

from mcp_server.core.exceptions import MCPError
from mcp_server.services.template_components import ComponentSelection, select_components
from mcp_server.services.template_contract_loader import DRAFT_2020_12
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


def _write_config(root: Path, profiles: Iterable[str]) -> None:
    configured = ", ".join(f"{profile}: {{checks: [syntax]}}" for profile in profiles)
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
                f"profiles: {{{configured}}}\n"
                "profiles_by_extension: {}\n"
                "run_checks: {}\n"
            ).encode()
        },
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
    )


def _selections(
    actual: SuiteSnapshot,
    candidate: SuiteSnapshot,
) -> tuple[ComponentSelection, ...]:
    actual_map = {state.key: state for state in (actual.evidence.shared, *actual.evidence.packages)}
    candidate_map = {
        state.key: state for state in (candidate.evidence.shared, *candidate.evidence.packages)
    }
    adopted = {key: candidate_map[key] for key in actual_map.keys() & candidate_map.keys()}
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
    supplied_snapshot = admit_template_suite(supplied, config)

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

    with pytest.raises(MCPError, match="template_candidate_invalid") as raised:
        _service(actual, staged, proposal, config).stage_candidate(supplied)

    assert raised.value.params["config_root"] == str(config.resolve())
    assert raised.value.params["cause"] == "template_output_profile_unknown"
    assert (staged / "retained.txt").read_bytes() == b"keep"
    assert not proposal.exists()


def test_proposal_invalid_is_distinct_and_retains_valid_candidate(tmp_path: Path) -> None:
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
    actual_snapshot = admit_template_suite(actual, broad_config)
    candidate_snapshot = admit_template_suite(supplied, effective_config)
    service = _service(actual, staged, proposal, effective_config)
    service.stage_candidate(supplied)

    with pytest.raises(MCPError, match="template_proposal_invalid") as raised:
        service.materialize_proposal(_selections(actual_snapshot, candidate_snapshot))

    assert raised.value.params["config_root"] == str(effective_config.resolve())
    assert raised.value.params["cause"] == "template_output_profile_unknown"
    assert (staged / "upstream" / "manifest.yaml").is_file()
    assert not proposal.exists()


def test_candidate_link_is_rejected_before_supersession(tmp_path: Path) -> None:
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
        pytest.skip("link creation is unavailable on this host")

    with pytest.raises(MCPError, match="template_candidate_invalid") as raised:
        _service(actual, staged, proposal, config).stage_candidate(supplied)

    assert raised.value.params["cause"] == "template_suite_symlink_escape"
    assert (staged / "retained.txt").read_bytes() == b"keep"
