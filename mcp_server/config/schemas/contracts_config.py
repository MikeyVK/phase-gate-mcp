# mcp_server/config/schemas/contracts_config.py
"""Typed workflow contracts with canonical mapping identities and explicit order."""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, model_validator

from mcp_server.config.ordering import ConfigId, OrderedConfigEntry, ordered_mapping


class BranchLocalArtifact(OrderedConfigEntry):
    """One identified artifact excluded by merge policy."""

    path: str
    reason: str


class MergePolicy(BaseModel):
    """Merge policy resolved from configuration."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    pr_allowed_phase: str
    branch_local_artifacts: Annotated[
        dict[ConfigId, BranchLocalArtifact], AfterValidator(ordered_mapping)
    ] = Field(default_factory=dict)


class CheckPayload(BaseModel):
    """Shared requirement fields for config and planning/runtime checks."""

    model_config = ConfigDict(extra="forbid")

    type: str
    required: bool = True
    file: str | None = None
    heading: str | None = None
    text: str | None = None
    dir: str | None = None
    pattern: str | None = None
    path: str | None = None


class CheckSpec(CheckPayload):
    """Public planning/runtime check retaining its explicit domain identifier."""

    id: str


class ConfigCheckRequirement(CheckPayload, OrderedConfigEntry):
    """Ordered config payload whose identifier is its containing mapping key."""

    model_config = ConfigDict(extra="forbid", frozen=True)


OrderedRequirements = Annotated[
    dict[ConfigId, ConfigCheckRequirement], AfterValidator(ordered_mapping)
]


class PhaseInstructionsSpec(BaseModel):
    """Role-specific instructions for one workflow phase."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    sub_role: str
    phase_instructions: str
    handover_template: str | None = None


class PhaseContractPhase(BaseModel):
    """Phase behavior and identified requirements."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    subphases: list[str] = Field(default_factory=list)
    commit_type_map: dict[str, str] = Field(default_factory=dict)
    cycle_based: bool = False
    exit_requires: OrderedRequirements = Field(default_factory=dict)
    cycle_exit_requires: dict[int, OrderedRequirements] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_cycle_based_commit_map(self) -> PhaseContractPhase:
        if self.cycle_based and not self.commit_type_map:
            raise ValueError("cycle_based phases require a non-empty commit_type_map")
        return self


class WorkflowPhaseEntry(PhaseContractPhase, OrderedConfigEntry):
    """One ranked phase; the containing key is the phase identifier."""

    instructions: PhaseInstructionsSpec


class WorkflowEntry(BaseModel):
    """A workflow with explicit phase ordering and one possible cycle owner."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    phases: Annotated[dict[ConfigId, WorkflowPhaseEntry], AfterValidator(ordered_mapping)] = Field(
        ..., min_length=1
    )

    @model_validator(mode="after")
    def validate_cycle_owner(self) -> WorkflowEntry:
        cycle_phases = [key for key, phase in self.phases.items() if phase.cycle_based]
        if len(cycle_phases) > 1:
            raise ValueError(f"workflow_cycle_based_conflict: {', '.join(cycle_phases)}")
        return self

    def get_phase_ids(self) -> list[str]:
        """Return canonical phase identifiers in configured rank order."""
        return list(self.phases)

    def get_phase(self, phase_id: str) -> WorkflowPhaseEntry:
        """Look up one phase by its canonical key."""
        try:
            return self.phases[phase_id]
        except KeyError:
            raise ValueError(f"Phase '{phase_id}' not in workflow") from None


class ContractsConfig(BaseModel):
    """Resolved workflow membership, ordering and transition contracts."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    version: Literal["1.0.0"] = Field("1.0.0", description="Config schema version")
    merge_policy: MergePolicy
    workflows: dict[ConfigId, WorkflowEntry] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_terminal_phase(self) -> ContractsConfig:
        terminal = self.merge_policy.pr_allowed_phase
        for name, workflow in self.workflows.items():
            last = workflow.get_phase_ids()[-1]
            if last != terminal:
                raise ValueError(
                    f"Workflow '{name}': last phase must be '{terminal}' "
                    f"(merge_policy.pr_allowed_phase), got '{last}'"
                )
        return self

    def get_pr_allowed_phase(self) -> str:
        return self.merge_policy.pr_allowed_phase

    def get_first_phase(self, workflow_name: str) -> str:
        """Return the first ranked phase identifier."""
        return self._get_workflow(workflow_name).get_phase_ids()[0]

    def get_phases(self, workflow_name: str) -> list[str]:
        """Return phase identifiers in explicit configured order."""
        return self._get_workflow(workflow_name).get_phase_ids()

    def validate_transition(
        self,
        workflow_name: str,
        current_phase: str,
        target_phase: str,
    ) -> bool:
        """Validate sequential phase transition."""
        workflow = self._get_workflow(workflow_name)
        names = workflow.get_phase_ids()
        if current_phase not in names:
            raise ValueError(
                f"Current phase '{current_phase}' not in workflow '{workflow_name}'\n"
                f"Valid phases: {names}"
            )
        if target_phase not in names:
            raise ValueError(
                f"Target phase '{target_phase}' not in workflow '{workflow_name}'\n"
                f"Valid phases: {names}"
            )
        current_idx = names.index(current_phase)
        target_idx = names.index(target_phase)
        if target_idx != current_idx + 1:
            next_phase = names[current_idx + 1] if current_idx + 1 < len(names) else None
            raise ValueError(
                f"Invalid transition: {current_phase} → {target_phase}\n"
                f"Expected next phase: {next_phase}\n"
                f"Workflow: {names}\n"
                "Hint: Use force_phase_transition tool for non-sequential transitions"
            )
        return True

    def _get_workflow(self, workflow_name: str) -> WorkflowEntry:
        if workflow_name not in self.workflows:
            available = ", ".join(sorted(self.workflows))
            raise ValueError(
                f"Unknown workflow: '{workflow_name}'\nAvailable workflows: {available}"
            )
        return self.workflows[workflow_name]
