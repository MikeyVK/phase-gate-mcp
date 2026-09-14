"""Public renewal CLI behavior on isolated roots."""

from __future__ import annotations

from pathlib import Path

import pytest

from mcp_server.cli_renewal import RenewalCli
from mcp_server.presenters.renewal_presenter import RenewalPresenter
from mcp_server.services.template_components import (
    ComponentSelection,
    ComponentState,
)
from mcp_server.services.template_renewal import RenewalResult


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
    assert "mutually exclusive" in capsys.readouterr().err


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

    unchanged_code = RenewalCli(
        operation=unchanged, presenter=RenewalPresenter()
    ).run(["--upgrade"])
    changed_code = RenewalCli(operation=changed, presenter=RenewalPresenter()).run(["--upgrade"])

    assert unchanged_code == changed_code == 0
    first_output = capsys.readouterr().out
    assert "Restart any running pgmcp server" not in first_output

    RenewalCli(operation=changed, presenter=RenewalPresenter()).run(["--upgrade"])
    second_output = capsys.readouterr().out
    assert "Restart any running pgmcp server" in second_output
