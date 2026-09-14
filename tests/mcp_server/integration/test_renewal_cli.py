"""Public renewal CLI behavior on isolated roots."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

import pytest

from mcp_server.cli_renewal import RenewalCli
from mcp_server.config.schemas.installation import InstallationState
from mcp_server.presenters.renewal_presenter import RenewalPresenter
from mcp_server.services.installation_state import ValidatedSuiteEvidence
from mcp_server.services.template_components import (
    ComponentSelection,
    ComponentState,
)
from mcp_server.services.template_renewal import RenewalResult, TemplateRenewalService


def _selection(
    component_id: str,
    *,
    relation: str = "upstream_only",
) -> ComponentSelection:
    adopted = ComponentState(
        kind="package",
        component_id=component_id,
        present=True,
        fingerprint="aaaaaaaaaaaaaaaa",
    )
    actual = adopted
    candidate = ComponentState(
        kind="package",
        component_id=component_id,
        present=True,
        fingerprint="bbbbbbbbbbbbbbbb",
    )
    return ComponentSelection(
        kind="package",
        component_id=component_id,
        adopted=adopted,
        actual=actual,
        candidate=candidate,
        relation=relation,
        selected=candidate if relation == "upstream_only" else actual,
        selected_source="candidate" if relation == "upstream_only" else "actual",
        checkpoint_action=(
            "advance_to_candidate" if relation == "upstream_only" else "retain_adopted"
        ),
        proposed_checkpoint=candidate if relation == "upstream_only" else adopted,
        change_kind="change",
    )


class RecordingOperation:
    """Small public operation double that records CLI intent and returns facts."""

    def __init__(self, result: RenewalResult) -> None:
        self.result = result
        self.calls: list[dict[str, object]] = []

    def execute(self, **kwargs: object) -> RenewalResult:
        self.calls.append(kwargs)
        return self.result


def test_modifiers_are_mutually_exclusive(capsys: pytest.CaptureFixture[str]) -> None:
    operation = RecordingOperation(RenewalResult(outcome="unchanged"))

    code = RenewalCli(operation=operation, presenter=RenewalPresenter()).run(
        ["--upgrade", "--accept-template-baseline", "--force-template-upgrade"]
    )

    assert code == 2
    assert operation.calls == []
    assert "not allowed" in capsys.readouterr().err


def test_checkpoint_acceptance_creates_only_checkpoint_on_isolated_root(
    tmp_path: Path,
) -> None:
    actual = tmp_path / "template_suite"
    actual.mkdir()
    marker = actual / "marker.txt"
    marker.write_bytes(b"owner content")
    result = RenewalResult(
        outcome="baseline_established",
        checkpoint_effect="created",
        candidate_disposition="removed",
        actual_changed=False,
    )
    operation = RecordingOperation(result)

    code = RenewalCli(operation=operation, presenter=RenewalPresenter()).run(
        ["--upgrade", "--accept-template-baseline"]
    )

    assert code == 0
    assert marker.read_bytes() == b"owner content"
    assert operation.calls == [{"accept_baseline": True, "force": False, "resolve_components": ()}]


def test_force_replacement_reports_verified_backup(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    backup = tmp_path / ".pgmcp_template_backup_20260914T120000000000Z"
    result = RenewalResult(
        outcome="forced_candidate_installed",
        actual_changed=True,
        checkpoint_effect="created",
        candidate_disposition="removed",
        backup_path=backup,
    )
    operation = RecordingOperation(result)

    code = RenewalCli(operation=operation, presenter=RenewalPresenter()).run(
        ["--upgrade", "--force-template-upgrade"]
    )

    assert code == 0
    assert operation.calls == [{"accept_baseline": False, "force": True, "resolve_components": ()}]
    output = capsys.readouterr().out
    assert str(backup) in output
    assert "Restart any running pgmcp server" in output


def test_checkpoint_required_reports_every_actionable_component(
    capsys: pytest.CaptureFixture[str],
) -> None:
    result = RenewalResult(
        outcome="checkpoint_required",
        candidate_disposition="staged",
        candidate_path=Path(".pgmcp/upgrade"),
        components=(_selection("design"), _selection("research")),
        available_actions=(),
    )
    operation = RecordingOperation(result)

    code = RenewalCli(operation=operation, presenter=RenewalPresenter()).run(["--upgrade"])

    assert code == 2
    output = capsys.readouterr().out
    assert "checkpoint" in output.lower()
    assert "design" in output
    assert "research" in output
    assert "--accept-template-baseline" in output


def test_actual_changed_only_controls_restart_hint(
    capsys: pytest.CaptureFixture[str],
) -> None:
    unchanged = RecordingOperation(RenewalResult(outcome="unchanged", actual_changed=False))
    changed = RecordingOperation(RenewalResult(outcome="activated", actual_changed=True))

    unchanged_code = RenewalCli(operation=unchanged, presenter=RenewalPresenter()).run(
        ["--upgrade"]
    )
    unchanged_output = capsys.readouterr().out
    changed_code = RenewalCli(operation=changed, presenter=RenewalPresenter()).run(["--upgrade"])
    changed_output = capsys.readouterr().out

    assert unchanged_code == changed_code == 0
    assert "Restart any running pgmcp server" not in unchanged_output
    assert "Restart any running pgmcp server" in changed_output


@dataclass(frozen=True)
class _Snapshot:
    evidence: ValidatedSuiteEvidence
    sources: tuple[str, ...]


class _ActivationDouble:
    last_result = None

    def activate(
        self,
        proposal_root: Path,
        *,
        pgmcp_version: str,
        fresh: bool = False,
        force: bool = False,
    ) -> None:
        del proposal_root, pgmcp_version, fresh, force

    def recover(self) -> None:
        return None


def _evidence(shared: str, package: str) -> ValidatedSuiteEvidence:
    return ValidatedSuiteEvidence(
        shared=ComponentState(
            kind="shared",
            component_id="shared",
            present=True,
            fingerprint=shared,
        ),
        packages=(
            ComponentState(
                kind="package",
                component_id="demo",
                present=True,
                fingerprint=package,
            ),
        ),
    )


def test_real_renewal_baseline_publishes_checkpoint_without_copying_candidate(
    tmp_path: Path,
) -> None:
    actual_root = tmp_path / "template_suite"
    candidate_root = tmp_path / "upgrade"
    proposal_root = tmp_path / "proposal"
    actual_root.mkdir()
    candidate_root.mkdir()
    (actual_root / "owner.txt").write_bytes(b"owner")
    (candidate_root / "candidate.txt").write_bytes(b"candidate")
    actual_snapshot = _Snapshot(_evidence("aaaaaaaaaaaaaaaa", "bbbbbbbbbbbbbbbb"), ("owner",))
    candidate_snapshot = _Snapshot(
        _evidence("cccccccccccccccc", "dddddddddddddddd"), ("candidate",)
    )
    snapshots = {actual_root: actual_snapshot, candidate_root: candidate_snapshot}
    published: list[InstallationState] = []

    def admit(root: Path) -> _Snapshot:
        return snapshots[root]

    operation = TemplateRenewalService(
        actual_root=actual_root,
        candidate_root=candidate_root,
        proposal_root=proposal_root,
        pgmcp_version="3.0.0",
        managed=True,
        read_installation=lambda: None,
        publish_installation=published.append,
        admit=admit,
        materialize_proposal=lambda _selections: None,
        activation=_ActivationDouble(),
        discard_candidate=lambda root: shutil.rmtree(root),
    )

    result = operation.execute(accept_baseline=True)

    assert result.outcome == "baseline_established"
    assert result.actual_changed is False
    assert published[0].template_checkpoint == candidate_snapshot.evidence.to_checkpoint()
    assert (actual_root / "owner.txt").read_bytes() == b"owner"
    assert not candidate_root.exists()
