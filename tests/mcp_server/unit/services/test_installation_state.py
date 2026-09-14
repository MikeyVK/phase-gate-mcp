"""Installation state contract and bootstrap evidence."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from mcp_server.services.artifact_identity import CompactFingerprint
from mcp_server.services.installation_state import (
    BootstrapResolver,
    InstallationStateRepository,
    ValidatedSuiteEvidence,
)
from mcp_server.config.schemas.installation import InstallationState, TemplateCheckpoint
from mcp_server.services.template_components import ComponentState


FP_A = "AAAAAAAAAAAAAAAA"
FP_B = "BBBBBBBBBBBBBBBB"


def _evidence(package_id: str = "alpha", package_fp: str = FP_A) -> ValidatedSuiteEvidence:
    return ValidatedSuiteEvidence(
        shared=ComponentState(
            kind="shared",
            component_id="shared",
            present=True,
            fingerprint=FP_A,
        ),
        packages=(
            ComponentState(
                kind="package",
                component_id=package_id,
                present=True,
                fingerprint=package_fp,
            ),
        ),
    )


def _state(checkpoint: TemplateCheckpoint | None = None) -> InstallationState:
    return InstallationState(pgmcp_version="3.0.0", template_checkpoint=checkpoint)


class FakeWriter:
    def __init__(self) -> None:
        self.calls: list[tuple[Path, dict[str, object]]] = []

    def write_json(self, path: Path, payload: dict[str, object]) -> None:
        self.calls.append((path, payload))


class FakeAdmission:
    def __init__(self, evidence: dict[str, ValidatedSuiteEvidence]) -> None:
        self.evidence = evidence
        self.calls: list[str] = []

    def admit(self, source: str) -> ValidatedSuiteEvidence:
        self.calls.append(source)
        return self.evidence[source]


def test_checkpoint_is_closed_and_empty_packages_are_valid() -> None:
    checkpoint = TemplateCheckpoint(shared=FP_A, packages={})
    assert checkpoint.model_dump() == {"shared": FP_A, "packages": {}}
    with pytest.raises(ValidationError):
        TemplateCheckpoint(shared=FP_A, packages={"alpha": None})
    with pytest.raises(ValidationError):
        TemplateCheckpoint.model_validate(
            {"shared": FP_A, "packages": {}, "metadata": "forbidden"},
            strict=True,
        )


def test_repository_reads_fail_fast_and_publishes_atomically(tmp_path: Path) -> None:
    path = tmp_path / "installation.json"
    writer = FakeWriter()
    repository = InstallationStateRepository(path, writer=writer)
    assert repository.read() is None

    state = _state(TemplateCheckpoint(shared=FP_A, packages={"alpha": FP_B}))
    repository.publish(state)
    assert writer.calls == [
        (path, {"pgmcp_version": "3.0.0", "template_checkpoint": {
            "shared": FP_A,
            "packages": {"alpha": FP_B},
        }})
    ]

    path.write_text(json.dumps({"pgmcp_version": "3.0.0", "extra": 1}), encoding="utf-8")
    with pytest.raises(Exception):
        repository.read()
    assert writer.calls[0][1]["template_checkpoint"] is not None


def test_evidence_requires_present_shared_and_unique_present_packages() -> None:
    with pytest.raises(ValidationError):
        ValidatedSuiteEvidence(
            shared=ComponentState(
                kind="shared",
                component_id="shared",
                present=False,
            ),
            packages=(),
        )
    with pytest.raises(ValidationError):
        ValidatedSuiteEvidence(
            shared=_evidence().shared,
            packages=(
                _evidence().packages[0],
                _evidence().packages[0],
            ),
        )
    slash_id = _evidence("retail/eu")
    assert slash_id.packages[0].component_id == "retail/eu"


def test_bootstrap_routes_managed_equality_prior_and_external_baseline() -> None:
    actual = _evidence()
    candidate = _evidence()
    changed = _evidence(package_fp=FP_B)
    admission = FakeAdmission(
        {"actual": actual, "candidate": candidate, "changed": changed, "prior": actual}
    )
    resolver = BootstrapResolver(admission=admission)

    equal = resolver.resolve(
        actual_source="actual",
        candidate_source="candidate",
        managed=True,
    )
    assert equal.disposition == "candidate_equal"
    assert equal.checkpoint == candidate.to_checkpoint()
    assert equal.actual_unchanged is True

    prior = resolver.resolve(
        actual_source="changed",
        candidate_source="candidate",
        trusted_prior_source="prior",
        managed=True,
    )
    assert prior.disposition == "trusted_prior"
    assert prior.adopted == actual

    required = resolver.resolve(
        actual_source="changed",
        candidate_source="candidate",
        managed=True,
    )
    assert required.disposition == "checkpoint_required"
    assert required.checkpoint is None

    external = resolver.resolve(
        actual_source="actual",
        candidate_source="candidate",
        managed=False,
    )
    assert external.disposition == "checkpoint_required"

    accepted = resolver.resolve(
        actual_source="actual",
        candidate_source="candidate",
        managed=False,
        accept_baseline=True,
    )
    assert accepted.disposition == "baseline_accepted"
    assert accepted.actual_unchanged is True
    assert accepted.checkpoint == candidate.to_checkpoint()


def test_fresh_requires_admitted_candidate_and_legacy_read_is_explicit(tmp_path: Path) -> None:
    candidate = _evidence()
    admission = FakeAdmission({"candidate": candidate})
    resolver = BootstrapResolver(admission=admission)
    fresh = resolver.resolve(candidate_source="candidate", managed=True)
    assert fresh.disposition == "fresh"
    assert fresh.adopted == candidate

    legacy = tmp_path / ".version"
    legacy.write_text("2.0.0\n", encoding="utf-8")
    repository = InstallationStateRepository(tmp_path / "installation.json", writer=FakeWriter())
    assert repository.read_legacy_compatibility(legacy) == "2.0.0"
