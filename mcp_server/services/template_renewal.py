"""Immutable component renewal facts and prepared renewal orchestration."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from contextlib import AbstractContextManager
from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from mcp_server.config.schemas.installation import InstallationState, TemplateCheckpoint
from mcp_server.core.exceptions import MCPError
from mcp_server.services.template_components import (
    ComponentKey,
    ComponentSelection,
    ComponentState,
    select_components,
)

if TYPE_CHECKING:
    from mcp_server.services.template_activation import ActivationResult
    from mcp_server.services.template_proposal import SuiteSnapshot

RenewalOutcome = Literal[
    "fresh_installed",
    "unchanged",
    "baseline_established",
    "candidate_equal",
    "activated",
    "activated_with_conflicts",
    "checkpoint_required",
    "reconciliation_completed",
    "upgrade_busy",
    "rolled_back",
    "forced_candidate_installed",
    "candidate_unavailable",
    "candidate_invalid",
    "proposal_invalid",
    "activation_failed",
    "recovery_failed",
]
CheckpointEffect = Literal["unchanged", "created", "advanced"]
CandidateDisposition = Literal["absent", "removed", "retained", "staged"]
RenewalActionKind = Literal[
    "accept_template_baseline",
    "resolve_template",
    "force_template_upgrade",
]


class RenewalAction(BaseModel):
    """One owner action derived from a completed renewal attempt."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    kind: RenewalActionKind
    component_ids: tuple[str, ...] = ()


class RenewalResult(BaseModel):
    """Immutable factual result consumed directly by the CLI presenter."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    outcome: RenewalOutcome
    actual_changed: bool = False
    checkpoint_effect: CheckpointEffect = "unchanged"
    candidate_disposition: CandidateDisposition = "absent"
    candidate_path: Path | None = None
    backup_path: Path | None = None
    components: tuple[ComponentSelection, ...] = ()
    validation_stage: str | None = None
    failure_code: str | None = None
    failure_params: Mapping[str, str] = Field(default_factory=dict)
    available_actions: tuple[RenewalAction, ...] = ()

    @field_validator("failure_params", mode="after")
    @classmethod
    def freeze_failure_params(cls, value: Mapping[str, str]) -> Mapping[str, str]:
        return MappingProxyType(dict(value))

    @property
    def exit_code(self) -> int:
        """Map factual outcome to the public CLI exit code."""

        if self.outcome in {
            "candidate_unavailable",
            "candidate_invalid",
            "proposal_invalid",
            "activation_failed",
            "recovery_failed",
        }:
            return 1
        if self.outcome in {
            "checkpoint_required",
            "activated_with_conflicts",
            "upgrade_busy",
            "rolled_back",
        }:
            return 2
        if self.outcome == "reconciliation_completed" and self.available_actions:
            return 2
        return 0


class RenewalAnalysis(BaseModel):
    """Deterministic component decisions; all summaries derive from them."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    decisions: tuple[ComponentSelection, ...]

    @property
    def conflicts(self) -> tuple[ComponentKey, ...]:
        return tuple(decision.key for decision in self.decisions if decision.relation == "conflict")

    @property
    def additions(self) -> tuple[ComponentKey, ...]:
        return tuple(
            decision.key for decision in self.decisions if decision.change_kind == "addition"
        )

    @property
    def removals(self) -> tuple[ComponentKey, ...]:
        return tuple(
            decision.key for decision in self.decisions if decision.change_kind == "removal"
        )

    @property
    def checkpoint_advances(self) -> tuple[ComponentKey, ...]:
        return tuple(
            decision.key
            for decision in self.decisions
            if decision.checkpoint_action == "advance_to_candidate"
        )


def analyze_components(
    adopted: Mapping[ComponentKey, ComponentState],
    actual: Mapping[ComponentKey, ComponentState],
    candidate: Mapping[ComponentKey, ComponentState],
) -> RenewalAnalysis:
    """Build immutable renewal facts without mutating supplied state."""

    return RenewalAnalysis(decisions=select_components(adopted, actual, candidate))


class TemplateRenewalService:
    """Coordinate renewal commands; expose their frozen facts separately."""

    def __init__(
        self,
        *,
        actual_root: Path,
        candidate_root: Path,
        proposal_root: Path,
        supplied_candidate_root: Path,
        pgmcp_version: str,
        managed: bool,
        read_installation: Callable[[], InstallationState | None],
        publish_installation: Callable[[InstallationState], None],
        admit: Callable[[Path], SuiteSnapshot],
        stage_candidate: Callable[[Path], None],
        materialize_proposal: Callable[[tuple[ComponentSelection, ...]], None],
        activate: Callable[[Path, str, bool, bool], None],
        recover: Callable[[], None],
        read_activation_result: Callable[[], ActivationResult | None],
        discard_candidate: Callable[[Path], None],
        hold_lock: Callable[[], AbstractContextManager[None]],
        recovery_pending: Callable[[], bool],
    ) -> None:
        roots = (actual_root, candidate_root, proposal_root, supplied_candidate_root)
        if any(not root.is_absolute() for root in roots):
            raise MCPError("absolute_template_renewal_roots_required", code="ERR_CONFIG")
        self._actual_root = actual_root
        self._candidate_root = candidate_root
        self._proposal_root = proposal_root
        self._supplied_candidate_root = supplied_candidate_root
        self._pgmcp_version = pgmcp_version
        self._managed = managed
        self._read_installation = read_installation
        self._publish_installation = publish_installation
        self._admit = admit
        self._stage_candidate = stage_candidate
        self._materialize_proposal = materialize_proposal
        self._activate_proposal = activate
        self._recover = recover
        self._read_activation_result = read_activation_result
        self._discard_candidate = discard_candidate
        self._hold_lock = hold_lock
        self._recovery_pending = recovery_pending
        self._last_result: RenewalResult | None = None
        self._pending: tuple[SuiteSnapshot | None, SuiteSnapshot, RenewalAnalysis | None] | None = (
            None
        )

    @property
    def last_result(self) -> RenewalResult | None:
        """Read immutable facts from the most recent command."""
        return self._last_result

    def execute(
        self,
        *,
        accept_baseline: bool = False,
        force: bool = False,
        resolve_components: tuple[str, ...] = (),
    ) -> None:
        """Recover first, prepare under exclusion, then activate a verified proposal."""
        self._last_result = None
        self._pending = None
        if int(accept_baseline) + int(force) + int(bool(resolve_components)) > 1:
            self._reject("modes_mutually_exclusive")
            return
        try:
            self._recover()
            if self._read_activation_result() is not None:
                self._recovered()
                return
        except (MCPError, OSError, ValueError, TypeError) as error:
            self._fail("recovery_failed", "recovery", error)
            return
        try:
            with self._hold_lock():
                # Another process may have started an activation after recovery released
                # its lock. Never stage or publish over its durable recovery record.
                if self._recovery_pending():
                    self._reject("template_recovery_required", outcome="recovery_failed")
                    return
                self._prepare(accept_baseline, force, resolve_components)
        except (MCPError, OSError, ValueError, TypeError) as error:
            self._fail("activation_failed", "checkpoint preparation", error)
            return
        if self._pending is not None:
            self._activate(force=force)

    def _prepare(
        self, accept_baseline: bool, force: bool, resolve_components: tuple[str, ...]
    ) -> None:
        if not (accept_baseline or force or resolve_components):
            try:
                if not self._supplied_candidate_root.exists():
                    self._reject("candidate_missing", outcome="candidate_unavailable")
                    return
                if self._supplied_candidate_root != self._candidate_root:
                    self._stage_candidate(self._supplied_candidate_root)
            except (MCPError, OSError, ValueError, TypeError) as error:
                self._fail("candidate_invalid", "candidate", error)
                return
        if not self._candidate_root.exists():
            self._reject("candidate_missing", outcome="candidate_unavailable")
            return
        try:
            candidate = self._admit(self._candidate_root)
        except (MCPError, OSError, ValueError, TypeError) as error:
            self._fail("candidate_invalid", "candidate", error)
            return
        installation = self._read_installation()
        checkpoint = None if installation is None else installation.template_checkpoint
        try:
            actual = self._admit(self._actual_root) if self._actual_root.exists() else None
        except (MCPError, OSError, ValueError, TypeError) as error:
            self._fail("candidate_invalid", "actual", error)
            return

        if accept_baseline:
            if checkpoint is not None or actual is None:
                self._reject(
                    "checkpoint_available" if checkpoint is not None else "actual_suite_required"
                )
                return
            self._publish(candidate.evidence.to_checkpoint())
            self._discard_candidate(self._candidate_root)
            self._last_result = RenewalResult(
                outcome="baseline_established",
                checkpoint_effect="created",
                candidate_disposition="removed",
            )
            return
        if resolve_components:
            self._resolve(checkpoint, actual, candidate, resolve_components)
            return
        if force:
            if not self._managed or actual is None:
                self._reject(
                    "external_root_force_forbidden"
                    if not self._managed
                    else "force_requires_managed_actual",
                    outcome="activation_failed",
                )
                return
            self._pending = (actual, candidate, None)
            return
        if checkpoint is None:
            self._bootstrap(actual, candidate)
            return
        if not self._managed or actual is None:
            self._reject(
                "external_root_activation_forbidden"
                if not self._managed
                else "actual_suite_missing",
                outcome="activation_failed",
            )
            return
        analysis = self._analyze(checkpoint, actual, candidate)
        try:
            self._materialize_proposal(analysis.decisions)
        except (MCPError, OSError, ValueError, TypeError) as error:
            self._fail("proposal_invalid", "complete proposal", error)
            return
        self._pending = (actual, candidate, analysis)

    def _bootstrap(self, actual: SuiteSnapshot | None, candidate: SuiteSnapshot) -> None:
        if self._managed and actual is None:
            self._pending = (None, candidate, None)
            return
        if (
            self._managed
            and actual is not None
            and (actual.evidence.to_checkpoint() == candidate.evidence.to_checkpoint())
        ):
            self._publish(candidate.evidence.to_checkpoint())
            self._discard_candidate(self._candidate_root)
            self._last_result = RenewalResult(
                outcome="candidate_equal",
                checkpoint_effect="created",
                candidate_disposition="removed",
            )
            return
        actions: tuple[RenewalAction, ...] = (
            (RenewalAction(kind="accept_template_baseline"),) if actual is not None else ()
        )
        if self._managed and actual is not None:
            actions += (RenewalAction(kind="force_template_upgrade"),)
        self._last_result = RenewalResult(
            outcome="checkpoint_required",
            candidate_disposition="staged",
            candidate_path=self._candidate_root,
            available_actions=actions,
        )

    def _activate(self, *, force: bool) -> None:
        pending = self._pending
        assert pending is not None
        actual, candidate, analysis = pending
        try:
            before = self._read_installation()
            self._activate_proposal(
                self._proposal_root if analysis is not None else self._candidate_root,
                self._pgmcp_version,
                actual is None,
                force,
            )
        except (MCPError, OSError, ValueError, TypeError) as error:
            self._fail("activation_failed", "activation", error)
            return
        result = self._read_activation_result()
        if result is None:
            self._reject("activation_result_missing", outcome="activation_failed")
            return
        if result.outcome != "activated":
            self._recovered()
            return
        after = self._read_installation()
        effect: CheckpointEffect = "unchanged"
        if before != after:
            effect = (
                "created" if before is None or before.template_checkpoint is None else "advanced"
            )
        changed = actual is None or (
            actual.sources != candidate.sources
            if analysis is None
            else any(item.selected != item.actual for item in analysis.decisions)
        )
        outcome: RenewalOutcome = (
            "fresh_installed"
            if actual is None
            else "forced_candidate_installed"
            if force
            else "activated_with_conflicts"
            if result.candidate_retained
            else "activated"
        )
        self._last_result = RenewalResult(
            outcome=outcome,
            actual_changed=changed,
            checkpoint_effect=effect,
            candidate_disposition="retained" if result.candidate_retained else "removed",
            candidate_path=self._candidate_root if result.candidate_retained else None,
            backup_path=result.backup_path,
            components=analysis.decisions if analysis is not None else (),
            available_actions=self._resolve_actions(analysis) if analysis is not None else (),
        )

    def _recovered(self) -> None:
        result = self._read_activation_result()
        assert result is not None
        analysis: RenewalAnalysis | None = None
        if result.outcome == "completed" and result.candidate_retained:
            with self._hold_lock():
                installation = self._read_installation()
                if installation is not None and installation.template_checkpoint is not None:
                    analysis = self._analyze(
                        installation.template_checkpoint,
                        self._admit(self._actual_root),
                        self._admit(self._candidate_root),
                    )
        self._last_result = RenewalResult(
            outcome="rolled_back"
            if result.outcome == "rolled_back"
            else ("activated_with_conflicts" if result.candidate_retained else "activated"),
            actual_changed=result.actual_changed,
            checkpoint_effect=result.checkpoint_effect,
            candidate_disposition="retained" if result.candidate_retained else "removed",
            candidate_path=self._candidate_root if result.candidate_retained else None,
            backup_path=result.backup_path,
            components=analysis.decisions if analysis is not None else (),
            available_actions=self._resolve_actions(analysis) if analysis is not None else (),
        )

    def _resolve(
        self,
        checkpoint: TemplateCheckpoint | None,
        actual: SuiteSnapshot | None,
        candidate: SuiteSnapshot,
        component_ids: tuple[str, ...],
    ) -> None:
        if checkpoint is None or actual is None:
            self._reject("checkpoint_required")
            return
        if len(set(component_ids)) != len(component_ids):
            self._reject("duplicate_component")
            return
        analysis = self._analyze(checkpoint, actual, candidate)
        selected: list[ComponentSelection] = []
        for name in component_ids:
            matches = tuple(item for item in analysis.decisions if item.component_id == name)
            if len(matches) != 1:
                self._reject("ambiguous_component" if matches else "unknown_component")
                return
            if matches[0].relation != "conflict":
                self._reject("component_not_conflicted")
                return
            selected.append(matches[0])
        packages = dict(checkpoint.packages)
        shared = checkpoint.shared
        for decision in selected:
            fingerprint = decision.candidate.fingerprint
            if decision.kind == "shared":
                assert fingerprint is not None
                shared = fingerprint
            elif fingerprint is not None:
                packages[decision.component_id] = fingerprint
            else:
                packages.pop(decision.component_id, None)
        updated = TemplateCheckpoint(shared=shared, packages=packages)
        accepted_keys = {item.key for item in selected}
        remaining = self._analyze(updated, actual, candidate)
        self._publish(updated)
        if not remaining.conflicts:
            self._discard_candidate(self._candidate_root)
        self._last_result = RenewalResult(
            outcome="reconciliation_completed",
            checkpoint_effect="advanced",
            candidate_disposition="retained" if remaining.conflicts else "removed",
            candidate_path=self._candidate_root if remaining.conflicts else None,
            components=tuple(
                item.model_copy(
                    update={
                        "checkpoint_action": "advance_to_candidate",
                        "proposed_checkpoint": item.candidate,
                    }
                )
                if item.key in accepted_keys
                else item
                for item in remaining.decisions
            ),
            available_actions=self._resolve_actions(remaining),
        )

    def _publish(self, checkpoint: TemplateCheckpoint) -> None:
        self._publish_installation(
            InstallationState(pgmcp_version=self._pgmcp_version, template_checkpoint=checkpoint)
        )

    @classmethod
    def _analyze(
        cls, checkpoint: TemplateCheckpoint, actual: SuiteSnapshot, candidate: SuiteSnapshot
    ) -> RenewalAnalysis:
        return analyze_components(
            cls._states(checkpoint),
            cls._states(actual.evidence.to_checkpoint()),
            cls._states(candidate.evidence.to_checkpoint()),
        )

    @staticmethod
    def _resolve_actions(analysis: RenewalAnalysis) -> tuple[RenewalAction, ...]:
        if not analysis.conflicts:
            return ()
        return (
            RenewalAction(
                kind="resolve_template", component_ids=tuple(key[1] for key in analysis.conflicts)
            ),
        )

    @staticmethod
    def _states(checkpoint: TemplateCheckpoint) -> dict[ComponentKey, ComponentState]:
        return {
            ("shared", "shared"): ComponentState(
                kind="shared", component_id="shared", present=True, fingerprint=checkpoint.shared
            ),
            **{
                ("package", name): ComponentState(
                    kind="package", component_id=name, present=True, fingerprint=value
                )
                for name, value in checkpoint.packages.items()
            },
        }

    def _reject(self, code: str, *, outcome: RenewalOutcome = "candidate_invalid") -> None:
        retained = self._candidate_root.exists()
        self._last_result = RenewalResult(
            outcome=outcome,
            failure_code=code,
            candidate_disposition="retained" if retained else "absent",
            candidate_path=self._candidate_root if retained else None,
        )

    def _fail(self, outcome: RenewalOutcome, stage: str, error: BaseException) -> None:
        code = error.message if isinstance(error, MCPError) else type(error).__name__
        params = (
            {key: str(value) for key, value in error.params.items()}
            if isinstance(error, MCPError)
            else {"cause": str(error)}
        )
        if code == "template_upgrade_locked":
            outcome = "upgrade_busy"
        retained = self._candidate_root.exists()
        self._last_result = RenewalResult(
            outcome=outcome,
            candidate_disposition="retained" if retained else "absent",
            candidate_path=self._candidate_root if retained else None,
            validation_stage=stage,
            failure_code=code,
            failure_params=params,
        )


__all__ = [
    "CandidateDisposition",
    "CheckpointEffect",
    "RenewalAction",
    "RenewalAnalysis",
    "RenewalOutcome",
    "RenewalResult",
    "TemplateRenewalService",
    "analyze_components",
]
