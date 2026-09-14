"""User-facing projection of immutable template renewal facts."""

from __future__ import annotations

from collections.abc import Iterable

from mcp_server.services.template_components import ComponentSelection
from mcp_server.services.template_renewal import RenewalAction, RenewalResult


class RenewalPresenter:
    """Render renewal facts as concise actionable CLI text."""

    def present(self, result: RenewalResult) -> str:
        """Return the complete projection for one completed renewal attempt."""

        lines = [self._heading(result), ""]
        lines.extend(
            (
                f"Actual suite: {self._actual_effect(result)}",
                f"Checkpoint: {self._checkpoint_effect(result)}",
            )
        )
        if result.candidate_disposition == "staged" or result.candidate_disposition == "retained":
            if result.candidate_path is not None:
                lines.append(f"Candidate: {result.candidate_path}")
            else:
                lines.append("Candidate: retained")
        elif result.candidate_disposition == "removed":
            lines.append("Candidate: removed")
        else:
            lines.append("Candidate: absent")

        groups = self._component_groups(result.components)
        for label, values in groups:
            if values:
                lines.append(f"{label}: {', '.join(values)}")

        if result.validation_stage is not None:
            lines.append(f"Validation stage: {result.validation_stage}")
        if result.failure_code is not None:
            lines.append(f"Failure: {result.failure_code}")
        if result.backup_path is not None:
            lines.append(f"Backup: {result.backup_path}")

        action_lines = self._actions(result)
        if action_lines:
            lines.append("")
            lines.extend(action_lines)

        if result.actual_changed:
            lines.extend(
                (
                    "",
                    "Restart any running pgmcp server to load the new template suite.",
                )
            )
        return "\n".join(lines) + "\n"

    def _heading(self, result: RenewalResult) -> str:
        return {
            "fresh_installed": "Template installation completed.",
            "unchanged": "Template upgrade completed.",
            "baseline_established": "Template baseline accepted.",
            "candidate_equal": "Template upgrade completed.",
            "activated": "Template upgrade completed.",
            "activated_with_conflicts": "Template upgrade completed with conflicts.",
            "checkpoint_required": "Template upgrade requires a baseline.",
            "reconciliation_completed": "Template conflict resolved.",
            "upgrade_busy": "Template upgrade is already in progress.",
            "rolled_back": "Template upgrade rolled back safely.",
            "forced_candidate_installed": "Template candidate installed.",
            "candidate_unavailable": "Template upgrade failed: candidate unavailable.",
            "candidate_invalid": "Template upgrade failed: candidate invalid.",
            "proposal_invalid": "Template upgrade failed: proposed suite invalid.",
            "activation_failed": "Template upgrade failed: activation failed.",
            "recovery_failed": "Template upgrade failed: recovery failed.",
        }[result.outcome]

    @staticmethod
    def _actual_effect(result: RenewalResult) -> str:
        return "updated" if result.actual_changed else "unchanged"

    @staticmethod
    def _checkpoint_effect(result: RenewalResult) -> str:
        return {
            "unchanged": "unchanged",
            "created": "created",
            "advanced": "advanced",
        }[result.checkpoint_effect]

    @staticmethod
    def _component_groups(
        components: Iterable[ComponentSelection],
    ) -> tuple[tuple[str, tuple[str, ...]], ...]:
        grouped: dict[str, list[str]] = {
            "Updated from candidate": [],
            "Preserved locally": [],
            "Conflicts": [],
            "Resolved": [],
        }
        for component in components:
            if component.relation == "conflict":
                grouped["Conflicts"].append(component.component_id)
            elif component.relation == "upstream_only":
                grouped["Updated from candidate"].append(component.component_id)
            elif component.relation in {"local_only", "unchanged"}:
                grouped["Preserved locally"].append(component.component_id)
            elif component.relation == "converged":
                grouped["Resolved"].append(component.component_id)
        return tuple((label, tuple(values)) for label, values in grouped.items())

    def _actions(self, result: RenewalResult) -> tuple[str, ...]:
        actions = result.available_actions
        if not actions:
            if result.outcome == "checkpoint_required":
                return (
                    "Next:",
                    "- migrate local templates and run:",
                    "  pgmcp --upgrade --accept-template-baseline",
                    "- or replace the managed suite using:",
                    "  pgmcp --upgrade --force-template-upgrade",
                )
            if result.outcome == "activated_with_conflicts":
                conflicts = tuple(
                    item.component_id for item in result.components if item.relation == "conflict"
                )
                actions = (RenewalAction(kind="resolve_template", component_ids=conflicts),)
            else:
                return ()

        rendered: list[str] = ["Next:"]
        for action in actions:
            if action.kind == "accept_template_baseline":
                rendered.append("  pgmcp --upgrade --accept-template-baseline")
            elif action.kind == "force_template_upgrade":
                rendered.append("  pgmcp --upgrade --force-template-upgrade")
            else:
                ids = " ".join(action.component_ids)
                rendered.extend(
                    (
                        f'Reconcile package "{ids}", then run:',
                        f"  pgmcp --upgrade --resolve-template {ids}",
                    )
                )
        return tuple(rendered)


__all__ = ["RenewalPresenter"]
