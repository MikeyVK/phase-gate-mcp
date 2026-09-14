"""Pure component renewal analysis over immutable comparison facts."""

from __future__ import annotations

from collections.abc import Mapping

from pydantic import BaseModel, ConfigDict

from mcp_server.services.template_components import (
    ComponentKey,
    ComponentSelection,
    ComponentState,
    select_components,
)


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
