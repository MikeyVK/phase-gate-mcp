"""Immutable component renewal facts and prepared renewal orchestration."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING, Literal, Protocol

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
            "reconciliation_completed",
            "upgrade_busy",
            "rolled_back",
        }:
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


class RenewalActivation(Protocol):
    """Narrow activation boundary used by renewal orchestration."""

    @property
    def last_result(self) -> object | None:
        """Return the factual result of the most recent activation attempt."""

    def activate(
        self,
        proposal_root: Path,
        *,
        pgmcp_version: str,
        fresh: bool = False,
        force: bool = False,
    ) -> None:
        """Activate one complete proposal root."""

    def recover(self) -> None:
        """Recover one interrupted activation."""


class TemplateRenewalService:
    """Coordinate bootstrap, selection, proposal, and activation through injected seams."""

    def __init__(
        self,
        *,
        actual_root: Path,
        candidate_root: Path,
        proposal_root: Path,
        pgmcp_version: str,
        managed: bool,
        read_installation: Callable[[], InstallationState | None],
        publish_installation: Callable[[InstallationState], None],
        admit: Callable[[Path], SuiteSnapshot],
        materialize_proposal: Callable[[tuple[ComponentSelection, ...]], None],
        activation: RenewalActivation,
        discard_candidate: Callable[[Path], None],
    ) -> None:
        roots = (actual_root, candidate_root, proposal_root)
        if any(not root.is_absolute() for root in roots):
            raise MCPError("absolute_template_renewal_roots_required", code="ERR_CONFIG")
        self._actual_root = actual_root.resolve()
        self._candidate_root = candidate_root.resolve()
        self._proposal_root = proposal_root.resolve()
        if len({self._actual_root, self._candidate_root, self._proposal_root}) != 3:
            raise MCPError("template_renewal_roots_overlap", code="ERR_CONFIG")
        self._pgmcp_version = pgmcp_version
        self._managed = managed
        self._read_installation = read_installation
        self._publish_installation = publish_installation
        self._admit = admit
        self._materialize_proposal = materialize_proposal
        self._activation = activation
        self._discard_candidate = discard_candidate

    def execute(
        self,
        *,
        accept_baseline: bool = False,
        force: bool = False,
        resolve_components: tuple[str, ...] = (),
    ) -> RenewalResult:
        """Execute one explicit renewal attempt and return immutable facts."""

        modes = int(accept_baseline) + int(force) + int(bool(resolve_components))
        if modes > 1:
            return RenewalResult(
                outcome="candidate_invalid", failure_code="modes_mutually_exclusive"
            )
        installation = self._read_installation()
        checkpoint = None if installation is None else installation.template_checkpoint

        if not self._candidate_root.exists():
            return RenewalResult(
                outcome="candidate_unavailable",
                candidate_disposition="absent",
                failure_code="candidate_missing",
            )
        try:
            candidate = self._admit(self._candidate_root)
        except (MCPError, OSError, ValueError, TypeError) as error:
            return self._failure("candidate_invalid", "candidate", error, retained=True)

        actual: SuiteSnapshot | None
        if self._actual_root.exists():
            try:
                actual = self._admit(self._actual_root)
            except (MCPError, OSError, ValueError, TypeError) as error:
                return self._failure("candidate_invalid", "actual", error, retained=True)
        else:
            actual = None

        if accept_baseline:
            return self._accept_baseline(installation, actual, candidate)

        if checkpoint is not None and not self._managed:
            return RenewalResult(
                outcome="activation_failed",
                candidate_disposition="retained",
                candidate_path=self._candidate_root,
                failure_code="external_root_activation_forbidden",
            )

        if force:
            if not self._managed:
                return RenewalResult(
                    outcome="activation_failed",
                    candidate_disposition="retained",
                    candidate_path=self._candidate_root,
                    failure_code="external_root_force_forbidden",
                )
            if checkpoint is None or actual is None:
                return RenewalResult(
                    outcome="activation_failed",
                    candidate_disposition="retained",
                    candidate_path=self._candidate_root,
                    failure_code="force_requires_managed_actual",
                )
            return self._force(candidate, actual)

        if resolve_components:
            return self._resolve(installation, checkpoint, actual, candidate, resolve_components)

        if checkpoint is None:
            return self._bootstrap(actual, candidate)

        if actual is None:
            return RenewalResult(
                outcome="activation_failed",
                candidate_disposition="retained",
                candidate_path=self._candidate_root,
                failure_code="actual_suite_missing",
            )
        analysis = analyze_components(
            self._states(checkpoint),
            self._states(actual.evidence.to_checkpoint()),
            self._states(candidate.evidence.to_checkpoint()),
        )
        try:
            self._materialize_proposal(analysis.decisions)
            self._activation.activate(self._proposal_root, pgmcp_version=self._pgmcp_version)
        except MCPError as error:
            return self._failure("proposal_invalid", "complete proposal", error, retained=True)
        except (OSError, ValueError, TypeError) as error:
            return self._failure("activation_failed", "activation", error, retained=True)

        activation_result = self._activation.last_result
        if getattr(activation_result, "outcome", None) == "rolled_back":
            return RenewalResult(
                outcome="rolled_back",
                candidate_disposition="retained",
                candidate_path=self._candidate_root,
                actual_changed=False,
                checkpoint_effect="unchanged",
                components=analysis.decisions,
            )
        return RenewalResult(
            outcome="activated_with_conflicts" if analysis.conflicts else "activated",
            actual_changed=any(
                decision.selected.present != decision.actual.present
                or decision.selected.fingerprint != decision.actual.fingerprint
                for decision in analysis.decisions
            ),
            checkpoint_effect="advanced",
            candidate_disposition=("retained" if analysis.conflicts else "removed"),
            candidate_path=self._candidate_root if analysis.conflicts else None,
            components=analysis.decisions,
            available_actions=(
                (
                    RenewalAction(
                        kind="resolve_template",
                        component_ids=tuple(key[1] for key in analysis.conflicts),
                    ),
                )
                if analysis.conflicts
                else ()
            ),
        )

    def _accept_baseline(
        self,
        installation: InstallationState | None,
        actual: SuiteSnapshot | None,
        candidate: SuiteSnapshot,
    ) -> RenewalResult:
        if installation is not None and installation.template_checkpoint is not None:
            return RenewalResult(
                outcome="candidate_invalid",
                candidate_disposition="retained",
                candidate_path=self._candidate_root,
                failure_code="checkpoint_available",
            )
        if actual is None:
            return RenewalResult(
                outcome="candidate_invalid",
                candidate_disposition="retained",
                candidate_path=self._candidate_root,
                failure_code="actual_suite_required",
            )
        checkpoint = candidate.evidence.to_checkpoint()
        self._publish_installation(
            InstallationState(pgmcp_version=self._pgmcp_version, template_checkpoint=checkpoint)
        )
        self._discard_candidate(self._candidate_root)
        return RenewalResult(
            outcome="baseline_established",
            checkpoint_effect="created",
            candidate_disposition="removed",
            actual_changed=False,
        )

    def _bootstrap(
        self,
        actual: SuiteSnapshot | None,
        candidate: SuiteSnapshot,
    ) -> RenewalResult:
        if actual is None:
            if not self._managed:
                return RenewalResult(
                    outcome="checkpoint_required",
                    candidate_disposition="staged",
                    candidate_path=self._candidate_root,
                    available_actions=(
                        RenewalAction(kind="accept_template_baseline"),
                        RenewalAction(kind="force_template_upgrade"),
                    ),
                )
            try:
                self._activation.activate(
                    self._candidate_root,
                    pgmcp_version=self._pgmcp_version,
                    fresh=True,
                )
            except MCPError as error:
                return self._failure("activation_failed", "activation", error, retained=True)
            except (OSError, ValueError, TypeError) as error:
                return self._failure("activation_failed", "activation", error, retained=True)
            activation_result = self._activation.last_result
            if getattr(activation_result, "outcome", None) == "rolled_back":
                return RenewalResult(
                    outcome="rolled_back",
                    candidate_disposition="retained",
                    candidate_path=self._candidate_root,
                )
            return RenewalResult(
                outcome="fresh_installed",
                actual_changed=True,
                checkpoint_effect="created",
                candidate_disposition="removed",
            )
        if actual.evidence.to_checkpoint() == candidate.evidence.to_checkpoint():
            self._publish_installation(
                InstallationState(
                    pgmcp_version=self._pgmcp_version,
                    template_checkpoint=candidate.evidence.to_checkpoint(),
                )
            )
            self._discard_candidate(self._candidate_root)
            return RenewalResult(
                outcome="candidate_equal",
                checkpoint_effect="created",
                candidate_disposition="removed",
            )
        return RenewalResult(
            outcome="checkpoint_required",
            candidate_disposition="staged",
            candidate_path=self._candidate_root,
            available_actions=(
                RenewalAction(kind="accept_template_baseline"),
                RenewalAction(kind="force_template_upgrade"),
            ),
        )

    def _force(self, candidate: SuiteSnapshot, actual: SuiteSnapshot) -> RenewalResult:
        try:
            self._activation.activate(
                self._candidate_root,
                pgmcp_version=self._pgmcp_version,
                force=True,
            )
        except MCPError as error:
            return self._failure("activation_failed", "force activation", error, retained=True)
        except (OSError, ValueError, TypeError) as error:
            return self._failure("activation_failed", "force activation", error, retained=True)
        activation_result = self._activation.last_result
        outcome = getattr(activation_result, "outcome", None)
        if outcome == "rolled_back":
            return RenewalResult(
                outcome="rolled_back",
                candidate_disposition="retained",
                candidate_path=self._candidate_root,
                backup_path=getattr(activation_result, "backup_path", None),
            )
        return RenewalResult(
            outcome="forced_candidate_installed",
            actual_changed=actual.sources != candidate.sources,
            checkpoint_effect="advanced",
            candidate_disposition="removed",
            backup_path=getattr(activation_result, "backup_path", None),
        )

    def _resolve(
        self,
        installation: InstallationState | None,
        checkpoint: TemplateCheckpoint | None,
        actual: SuiteSnapshot | None,
        candidate: SuiteSnapshot,
        component_ids: tuple[str, ...],
    ) -> RenewalResult:
        if installation is None or checkpoint is None or actual is None:
            return RenewalResult(
                outcome="activation_failed",
                candidate_disposition="retained",
                candidate_path=self._candidate_root,
                failure_code="checkpoint_required",
            )
        if len(set(component_ids)) != len(component_ids):
            return RenewalResult(
                outcome="candidate_invalid",
                candidate_disposition="retained",
                candidate_path=self._candidate_root,
                failure_code="duplicate_component",
            )
        analysis = analyze_components(
            self._states(checkpoint),
            self._states(actual.evidence.to_checkpoint()),
            self._states(candidate.evidence.to_checkpoint()),
        )
        by_id = {decision.component_id: decision for decision in analysis.decisions}
        if any(component_id not in by_id for component_id in component_ids):
            return RenewalResult(
                outcome="candidate_invalid",
                candidate_disposition="retained",
                candidate_path=self._candidate_root,
                failure_code="unknown_component",
                components=analysis.decisions,
            )
        if any(by_id[component_id].relation != "conflict" for component_id in component_ids):
            return RenewalResult(
                outcome="candidate_invalid",
                candidate_disposition="retained",
                candidate_path=self._candidate_root,
                failure_code="component_not_conflicted",
                components=analysis.decisions,
            )
        accepted = set(component_ids)
        next_packages = dict(checkpoint.packages)
        for decision in analysis.decisions:
            if decision.component_id not in accepted:
                continue
            if decision.kind == "package":
                if decision.candidate.present and decision.candidate.fingerprint is not None:
                    next_packages[decision.component_id] = decision.candidate.fingerprint
                else:
                    next_packages.pop(decision.component_id, None)
            else:
                shared = decision.candidate.fingerprint
                if shared is None:
                    return RenewalResult(
                        outcome="candidate_invalid",
                        candidate_disposition="retained",
                        candidate_path=self._candidate_root,
                        failure_code="shared_checkpoint_missing",
                    )
                checkpoint = TemplateCheckpoint(shared=shared, packages=next_packages)
        self._publish_installation(
            InstallationState(pgmcp_version=self._pgmcp_version, template_checkpoint=checkpoint)
        )
        remaining = tuple(
            decision
            for decision in analysis.decisions
            if decision.relation == "conflict" and decision.component_id not in accepted
        )
        if not remaining:
            self._discard_candidate(self._candidate_root)
        return RenewalResult(
            outcome="reconciliation_completed",
            checkpoint_effect="advanced",
            candidate_disposition="retained" if remaining else "removed",
            candidate_path=self._candidate_root if remaining else None,
            components=analysis.decisions,
            available_actions=(
                (
                    RenewalAction(
                        kind="resolve_template",
                        component_ids=tuple(item.component_id for item in remaining),
                    ),
                )
                if remaining
                else ()
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

    @staticmethod
    def _failure(
        outcome: Literal["candidate_invalid", "proposal_invalid", "activation_failed"],
        stage: str,
        error: BaseException,
        *,
        retained: bool,
    ) -> RenewalResult:
        if isinstance(error, MCPError):
            code = error.message
            params = {key: str(value) for key, value in error.params.items()}
        else:
            code = type(error).__name__
            params = {"cause": str(error)}
        return RenewalResult(
            outcome=outcome,
            candidate_disposition="retained" if retained else "absent",
            validation_stage=stage,
            failure_code=code,
            failure_params=params,
        )


RenewalOperation = TemplateRenewalService


__all__ = [
    "CandidateDisposition",
    "CheckpointEffect",
    "RenewalAction",
    "RenewalAnalysis",
    "RenewalOperation",
    "RenewalOutcome",
    "RenewalResult",
    "TemplateRenewalService",
    "analyze_components",
]
