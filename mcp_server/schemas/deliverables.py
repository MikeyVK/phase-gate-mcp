# mcp_server/schemas/deliverables.py
"""Pure, frozen authoring values, explicit operations and stored planning references."""

from __future__ import annotations

from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

PlanningText = Annotated[str, StringConstraints(strict=True, min_length=1, pattern=r"\S")]
CycleRef = Annotated[str, Field(strict=True, pattern=r"^C_[1-9][0-9]*$")]


class PlanningMutationError(ValueError):
    """Structured planning command failure for the presentation boundary."""

    def __init__(self, error_code: str) -> None:
        super().__init__(error_code)
        self.error_code = error_code


class PlanningValue(BaseModel):
    """Shared admission constraints without configuration or IO."""

    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)


class ValidatesModel(PlanningValue):
    """Type-specific validation rule consumed by the existing checker."""

    type: Literal["file_exists", "file_glob", "contains_text", "absent_text", "key_path"]
    file: str | None = None
    text: str | None = None
    path: str | None = None
    dir: PlanningText | None = None
    pattern: PlanningText | None = None

    @model_validator(mode="after")
    def validate_rule_fields(self) -> Self:
        required = {
            "file_exists": {"file"},
            "file_glob": {"dir", "pattern"},
            "contains_text": {"file", "text"},
            "absent_text": {"file", "text"},
            "key_path": {"file", "path"},
        }[self.type]
        supplied = {
            name for name in ("file", "text", "path", "dir", "pattern")
            if getattr(self, name) is not None
        }
        if supplied != required:
            raise ValueError("planning_validation_fields_invalid")
        return self


class DeliverableInput(PlanningValue):
    """One complete deliverable, without caller-generated references."""

    deliverable_name: PlanningText
    description: PlanningText
    validates: ValidatesModel | None = None


class CycleInput(PlanningValue):
    """One complete authoring cycle; its position determines its reference."""

    cycle_name: PlanningText
    deliverables: list[DeliverableInput] = Field(min_length=1)
    exit_criteria: PlanningText


class PhaseBlockInput(PlanningValue):
    """The complete deliverables of one configured non-cycle phase."""

    deliverables: list[DeliverableInput] = Field(min_length=1)


class CyclesInput(PlanningValue):
    """An ordered, nonempty initial cycle collection."""

    cycles: list[CycleInput] = Field(min_length=1)


class SavePlanningModel(PlanningValue):
    """Complete initial plan. Omission, rather than null, means no cycles."""

    cycles: CyclesInput | None = None
    phases: dict[str, PhaseBlockInput] = Field(default_factory=dict)

    @model_validator(mode="before")
    @classmethod
    def reject_explicit_null_cycles(cls, value: object) -> object:
        if isinstance(value, dict) and "cycles" in value and value["cycles"] is None:
            raise ValueError("planning_cycles_null")
        return value

    @model_validator(mode="after")
    def validate_nonempty(self) -> Self:
        if self.cycles is None and not self.phases:
            raise ValueError("planning_result_empty")
        return self


class AppendCycle(PlanningValue):
    """Append one complete cycle after the original surviving cycles."""

    op: Literal["append_cycle"]
    cycle: CycleInput


class ReplaceCycle(PlanningValue):
    """Replace an existing original-snapshot cycle as one complete block."""

    op: Literal["replace_cycle"]
    cycle_id: CycleRef
    cycle: CycleInput


class RemoveCycle(PlanningValue):
    """Explicitly remove an existing original-snapshot cycle."""

    op: Literal["remove_cycle"]
    cycle_id: CycleRef


class SetPhase(PlanningValue):
    """Create or replace the complete block for a configured phase."""

    op: Literal["set_phase"]
    phase: PlanningText
    block: PhaseBlockInput


class RemovePhase(PlanningValue):
    """Explicitly remove an existing phase block."""

    op: Literal["remove_phase"]
    phase: PlanningText


PlanningOperation = Annotated[
    AppendCycle | ReplaceCycle | RemoveCycle | SetPhase | RemovePhase,
    Field(discriminator="op"),
]


class StoredDeliverable(DeliverableInput):
    """Authoring content with a server-derived reference within its block."""

    deliverable_id: PlanningText


class StoredCycle(PlanningValue):
    """One current cycle with coherent numeric and readable references."""

    cycle_id: CycleRef
    cycle_number: int = Field(gt=0)
    cycle_name: PlanningText
    deliverables: list[StoredDeliverable] = Field(min_length=1)
    exit_criteria: PlanningText

    @model_validator(mode="after")
    def validate_references(self) -> Self:
        if self.cycle_id != f"C_{self.cycle_number}":
            raise ValueError("planning_cycle_reference_invalid")
        for index, deliverable in enumerate(self.deliverables, 1):
            if deliverable.deliverable_id != f"D_{self.cycle_number}.{index}":
                raise ValueError("planning_deliverable_reference_invalid")
        return self


class StoredCycles(PlanningValue):
    """Contiguous current cycles and their derived total."""

    total: int = Field(gt=0)
    cycles: list[StoredCycle] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_sequence(self) -> Self:
        if self.total != len(self.cycles):
            raise ValueError("planning_cycle_total_invalid")
        if any(cycle.cycle_number != index for index, cycle in enumerate(self.cycles, 1)):
            raise ValueError("planning_cycle_sequence_invalid")
        return self


class StoredPhaseBlock(PlanningValue):
    """A phase block with local, ordered deliverable references."""

    deliverables: list[StoredDeliverable] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_references(self) -> Self:
        for index, deliverable in enumerate(self.deliverables, 1):
            if deliverable.deliverable_id != f"D_{index}":
                raise ValueError("planning_deliverable_reference_invalid")
        return self


class StoredPlanningModel(PlanningValue):
    """The sole persisted and queried nested planning representation."""

    cycles: StoredCycles | None = None
    phases: dict[str, StoredPhaseBlock] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_nonempty(self) -> Self:
        if self.cycles is None and not self.phases:
            raise ValueError("planning_result_empty")
        return self
