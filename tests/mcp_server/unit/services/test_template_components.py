"""Operational component fingerprint and selection evidence."""

from __future__ import annotations

import base64
import hashlib

from mcp_server.config.schemas.template_suite import TemplateManifest
from mcp_server.services.artifact_identity import GenerationPackage, GenerationSource
from mcp_server.services.template_components import (
    ComponentKey,
    ComponentKind,
    ComponentState,
    component_fingerprints,
)
from mcp_server.services.template_renewal import analyze_components


def _package(
    directory: str = "pkg",
    template_id: str = "alpha",
    purpose: str = "A",
) -> GenerationPackage:
    return GenerationPackage(
        manifest=TemplateManifest(template_id=template_id, purpose=purpose),
        version="1.0.0",
        directory=directory,
    )


def _sources(
    directory: str = "pkg",
    template_id: str = "alpha",
    purpose: str = "A",
) -> tuple[GenerationSource, ...]:
    files = {
        f"{directory}/manifest.yaml": (
            f"template_id: {template_id}\npurpose: {purpose}\n".encode()
        ),
        f"{directory}/context.schema.json": b'{"type":"object"}\n',
        f"{directory}/template.jinja2": b"hello\n",
        f"{directory}/.version": b"1.0.0\n",
        f"{directory}/policy.yaml": b"output_profile: text\npersistence: workspace\n",
    }
    return tuple(GenerationSource(path=path, content=value) for path, value in files.items())


def _state(
    component_id: str,
    fingerprint: str | None,
    kind: ComponentKind = "package",
) -> ComponentState:
    return ComponentState(
        kind=kind,
        component_id=component_id,
        present=fingerprint is not None,
        fingerprint=fingerprint,
    )


def _map(*states: ComponentState) -> dict[ComponentKey, ComponentState]:
    return {state.key: state for state in states}


def _absent(name: str) -> ComponentState:
    return ComponentState(kind="package", component_id=name, present=False)


def _empty_shared_fingerprint() -> str:
    vector = b"pgmcp:template-component:shared:v1\x00"
    return base64.urlsafe_b64encode(hashlib.sha256(vector).digest()[:12]).decode()


def test_operational_vectors_include_complete_sources_and_shared_presence() -> None:
    states = component_fingerprints((_package(),), _sources())
    (shared, state) = states
    vector = (
        b"pgmcp:template-component:package:v1\x00"
        b"file\x00.version\x006\x001.0.0\n"
        b'file\x00context.schema.json\x0018\x00{"type":"object"}\n'
        b"file\x00manifest.yaml\x0030\x00template_id: alpha\npurpose: A\n"
        b"file\x00policy.yaml\x0044\x00"
        b"output_profile: text\npersistence: workspace\n"
        b"file\x00template.jinja2\x006\x00hello\n"
    )
    expected = base64.urlsafe_b64encode(hashlib.sha256(vector).digest()[:12]).decode()
    assert shared.present is True
    assert shared.fingerprint == _empty_shared_fingerprint()
    assert state.fingerprint == expected

    concrete_shared = component_fingerprints(
        (_package(),),
        _sources() + (GenerationSource(path="shared/base.txt", content=b"shared\r\n"),),
    )[0]
    shared_vector = b"pgmcp:template-component:shared:v1\x00file\x00base.txt\x007\x00shared\n"
    assert (
        concrete_shared.fingerprint
        == base64.urlsafe_b64encode(hashlib.sha256(shared_vector).digest()[:12]).decode()
    )

    renamed = component_fingerprints((_package("moved"),), _sources("moved"))
    assert renamed[0] == shared
    assert renamed[1] == state

    version_changed = list(_sources())
    version_changed[3] = GenerationSource(
        path="pkg/.version",
        content=b"2.0.0\n",
    )
    policy_changed = list(_sources())
    policy_changed[4] = GenerationSource(
        path="pkg/policy.yaml",
        content=b"output_profile: json\npersistence: workspace\n",
    )
    assert component_fingerprints((_package(),), tuple(version_changed))[1] != state
    assert component_fingerprints((_package(),), tuple(policy_changed))[1] != state

    packages = (_package(), _package("other", "beta", "B"))
    source_files = _sources() + _sources("other", "beta", "B")
    changed_beta = list(source_files)
    changed_beta[-3] = GenerationSource(path="other/template.jinja2", content=b"changed\n")
    before = component_fingerprints(packages, source_files)
    after = component_fingerprints(packages, tuple(changed_beta))
    assert before[1] == after[1]
    assert before[2] != after[2]


def test_selection_orders_shared_first_and_carries_all_facts() -> None:
    adopted = _map(
        _state("shared", "AAAAAAAAAAAAAAAA", "shared"),
        _state("alpha", "AAAAAAAAAAAAAAAA"),
        _state("beta", "AAAAAAAAAAAAAAAA"),
        _state("delta", "AAAAAAAAAAAAAAAA"),
        _state("echo", "AAAAAAAAAAAAAAAA"),
    )
    actual = _map(
        _state("shared", "AAAAAAAAAAAAAAAA", "shared"),
        _state("alpha", "AAAAAAAAAAAAAAAA"),
        _state("beta", "BBBBBBBBBBBBBBBB"),
        _state("delta", "BBBBBBBBBBBBBBBB"),
        _state("echo", "BBBBBBBBBBBBBBBB"),
    )
    candidate = _map(
        _state("shared", "AAAAAAAAAAAAAAAA", "shared"),
        _state("alpha", "BBBBBBBBBBBBBBBB"),
        _state("beta", "AAAAAAAAAAAAAAAA"),
        _state("delta", "BBBBBBBBBBBBBBBB"),
        _state("echo", "CCCCCCCCCCCCCCCC"),
    )

    analysis = analyze_components(adopted, actual, candidate)
    assert [item.key for item in analysis.decisions] == [
        ("shared", "shared"),
        ("package", "alpha"),
        ("package", "beta"),
        ("package", "delta"),
        ("package", "echo"),
    ]
    expected = [
        ("unchanged", "actual", "AAAAAAAAAAAAAAAA", "retain_adopted"),
        ("upstream_only", "candidate", "BBBBBBBBBBBBBBBB", "advance_to_candidate"),
        ("local_only", "actual", "BBBBBBBBBBBBBBBB", "retain_adopted"),
        ("converged", "actual", "BBBBBBBBBBBBBBBB", "advance_to_candidate"),
        ("conflict", "actual", "BBBBBBBBBBBBBBBB", "retain_adopted"),
    ]
    for decision, (relation, source, selected, action) in zip(
        analysis.decisions, expected, strict=True
    ):
        assert decision.relation == relation
        assert decision.selected_source == source
        assert decision.selected.fingerprint == selected
        assert decision.proposed_checkpoint.fingerprint == (
            selected if action == "advance_to_candidate" else decision.adopted.fingerprint
        )
        assert decision.checkpoint_action == action
    assert analysis.conflicts == (("package", "echo"),)
    assert analysis.checkpoint_advances == (
        ("package", "alpha"),
        ("package", "delta"),
    )


def test_absence_lifecycle_and_conflicts_are_explicit() -> None:
    adopted = _map(
        _absent("upstream_add"),
        _state("upstream_remove", "AAAAAAAAAAAAAAAA"),
        _absent("local_add"),
        _state("local_remove", "AAAAAAAAAAAAAAAA"),
        _absent("dual_add"),
        _state("change_remove", "AAAAAAAAAAAAAAAA"),
        _state("removed_change", "AAAAAAAAAAAAAAAA"),
    )
    actual = _map(
        _absent("upstream_add"),
        _state("upstream_remove", "AAAAAAAAAAAAAAAA"),
        _state("local_add", "BBBBBBBBBBBBBBBB"),
        _absent("local_remove"),
        _state("dual_add", "AAAAAAAAAAAAAAAA"),
        _state("change_remove", "BBBBBBBBBBBBBBBB"),
        _absent("removed_change"),
    )
    candidate = _map(
        _state("upstream_add", "BBBBBBBBBBBBBBBB"),
        _absent("upstream_remove"),
        _absent("local_add"),
        _state("local_remove", "AAAAAAAAAAAAAAAA"),
        _state("dual_add", "CCCCCCCCCCCCCCCC"),
        _absent("change_remove"),
        _state("removed_change", "BBBBBBBBBBBBBBBB"),
    )
    analysis = analyze_components(adopted, actual, candidate)
    assert analysis.additions == (
        ("package", "dual_add"),
        ("package", "upstream_add"),
    )
    assert analysis.removals == (
        ("package", "change_remove"),
        ("package", "upstream_remove"),
    )
    by_id = {item.component_id: item for item in analysis.decisions}
    assert by_id["upstream_add"].selected_source == "candidate"
    assert by_id["upstream_remove"].selected.present is False
    for name in ("dual_add", "change_remove", "removed_change"):
        decision = by_id[name]
        assert decision.relation == "conflict"
        assert decision.selected == decision.actual
        assert decision.proposed_checkpoint == decision.adopted
    assert by_id["local_add"].relation == "local_only"
    assert by_id["local_remove"].relation == "local_only"
    assert by_id["upstream_add"].change_kind == "addition"
