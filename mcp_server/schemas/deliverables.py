# mcp_server/schemas/deliverables.py
# template=schema version=74378193 created=2026-06-11T09:44:27Z updated=2026-06-11T09:44:27Z
"""Deliverables validation schemas.

Defines Pydantic value objects for strict, frozen validation of planning
deliverables at the server boundary (CQS-compliant, frozen=True).
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ValidatesModel(BaseModel):
    """Pydantic model representing a validation rule spec."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    type: Literal["file_exists", "file_glob", "contains_text", "absent_text", "key_path"]
    file: str | None = Field(default=None, description="Target file path")
    text: str | None = Field(default=None, description="Expected text content")
    path: str | None = Field(default=None, description="Expected JSON key path")

    @model_validator(mode="after")
    def validate_required_fields(self) -> "ValidatesModel":
        required_fields = {
            "file_exists": ["file"],
            "file_glob": ["file"],
            "contains_text": ["file", "text"],
            "absent_text": ["file", "text"],
            "key_path": ["file", "path"],
        }
        fields = required_fields.get(self.type, [])
        for field in fields:
            if getattr(self, field) is None:
                raise ValueError(f"validates type '{self.type}' requires field '{field}'")
        return self


class DeliverableModel(BaseModel):
    """Pydantic model representing a single deliverable."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str = Field(..., description="Unique deliverable ID, e.g., 'D1.1'")
    description: str = Field(..., description="Human-readable description of the deliverable")
    validates: ValidatesModel | None = Field(default=None, description="Optional validation spec")


class CycleModel(BaseModel):
    """Pydantic model representing a single cycle."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    cycle_number: int = Field(..., description="1-based cycle index")
    name: str | None = Field(default=None, description="Optional cycle name")
    deliverables: list[DeliverableModel] = Field(..., min_length=1, description="Deliverables list")
    exit_criteria: str = Field(..., description="Non-empty exit criteria description")

    @model_validator(mode="after")
    def validate_exit_criteria(self) -> "CycleModel":
        if not self.exit_criteria.strip():
            raise ValueError("exit_criteria must be a non-empty string")
        return self


class PhaseCyclesModel(BaseModel):
    """Pydantic model representing cycle list wrapper."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    total: int = Field(..., gt=0, description="Total number of cycles")
    cycles: list[CycleModel] = Field(..., description="List of cycles")

    @model_validator(mode="after")
    def validate_cycles_total_and_sequential(self) -> "PhaseCyclesModel":
        if self.total != len(self.cycles):
            raise ValueError(f"total ({self.total}) must equal len(cycles) ({len(self.cycles)})")
        for idx, cycle in enumerate(self.cycles):
            expected = idx + 1
            if cycle.cycle_number != expected:
                raise ValueError(
                    f"Cycle at index {idx} has cycle_number {cycle.cycle_number}, "
                    f"expected {expected} (must be sequential 1-based)"
                )
        return self


class PhaseDeliverablesModel(BaseModel):
    """Pydantic model representing list of deliverables for a phase (design, etc.)."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    deliverables: list[DeliverableModel] = Field(..., description="List of deliverables")


class CyclePlanningModel(BaseModel):
    """Main model for save_planning_deliverables validation."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    cycles: PhaseCyclesModel | None = Field(default=None, description="TDD cycles plan")
    design: PhaseDeliverablesModel | None = Field(default=None, description="Design deliverables")
    validation: PhaseDeliverablesModel | None = Field(
        default=None, description="Validation deliverables"
    )
    documentation: PhaseDeliverablesModel | None = Field(
        default=None, description="Documentation deliverables"
    )


class UpdateCycleModel(BaseModel):
    """Pydantic model representing a cycle update payload."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    cycle_number: int = Field(..., description="1-based cycle index")
    name: str | None = Field(default=None, description="Optional cycle name")
    deliverables: list[DeliverableModel] | None = Field(
        default=None, description="Optional deliverables list to update"
    )
    exit_criteria: str | None = Field(
        default=None, description="Optional exit criteria description to update"
    )

    @model_validator(mode="after")
    def validate_update_cycle_fields(self) -> "UpdateCycleModel":
        if self.exit_criteria is not None and not self.exit_criteria.strip():
            raise ValueError("exit_criteria must be a non-empty string")
        return self


class UpdateCyclesModel(BaseModel):
    """Cycles wrapper model for update_planning_deliverables validation."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    total: int | None = Field(default=None, gt=0, description="Total number of cycles")
    cycles: list[UpdateCycleModel] | None = Field(default=None, description="List of cycles")


class UpdatePlanningModel(BaseModel):
    """Permissive partial update model for update_planning_deliverables."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    cycles: UpdateCyclesModel | None = Field(default=None, description="TDD cycles plan update")
    design: PhaseDeliverablesModel | None = Field(
        default=None, description="Design deliverables update"
    )
    validation: PhaseDeliverablesModel | None = Field(
        default=None, description="Validation deliverables update"
    )
    documentation: PhaseDeliverablesModel | None = Field(
        default=None, description="Documentation deliverables update"
    )
