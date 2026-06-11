# mcp_server/schemas/deliverables.py
# template=schema version=74378193 created=2026-06-11T09:44:27Z updated=2026-06-11T09:44:27Z
"""Deliverables validation schemas.

Defines Pydantic value objects for strict, frozen validation of planning
deliverables at the server boundary (CQS-compliant, frozen=True).
"""

from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field


class ValidatesModel(BaseModel):
    """Pydantic model representing a validation rule spec."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    type: Literal["file_exists", "file_glob", "contains_text", "absent_text", "key_path"]
    file: str | None = Field(default=None, description="Target file path")
    text: str | None = Field(default=None, description="Expected text content")
    path: str | None = Field(default=None, description="Expected JSON key path")


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
    deliverables: list[DeliverableModel] = Field(..., description="Deliverables list")
    exit_criteria: str = Field(..., description="Non-empty exit criteria description")


class PhaseCyclesModel(BaseModel):
    """Pydantic model representing cycle list wrapper."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    total: int = Field(..., description="Total number of cycles")
    cycles: list[CycleModel] = Field(..., description="List of cycles")


class PhaseDeliverablesModel(BaseModel):
    """Pydantic model representing list of deliverables for a phase (design, etc.)."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    deliverables: list[DeliverableModel] = Field(..., description="List of deliverables")


class CyclePlanningModel(BaseModel):
    """Main model for save_planning_deliverables validation."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    cycles: PhaseCyclesModel | None = Field(default=None, description="TDD cycles plan")
    design: PhaseDeliverablesModel | None = Field(default=None, description="Design deliverables")
    validation: PhaseDeliverablesModel | None = Field(default=None, description="Validation deliverables")
    documentation: PhaseDeliverablesModel | None = Field(default=None, description="Documentation deliverables")


class UpdateCyclesModel(BaseModel):
    """Cycles wrapper model for update_planning_deliverables validation."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    total: int | None = Field(default=None, description="Total number of cycles")
    cycles: list[CycleModel] | None = Field(default=None, description="List of cycles")


class UpdatePlanningModel(BaseModel):
    """Permissive partial update model for update_planning_deliverables."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    cycles: UpdateCyclesModel | None = Field(default=None, description="TDD cycles plan update")
    design: PhaseDeliverablesModel | None = Field(default=None, description="Design deliverables update")
    validation: PhaseDeliverablesModel | None = Field(default=None, description="Validation deliverables update")
    documentation: PhaseDeliverablesModel | None = Field(default=None, description="Documentation deliverables update")

