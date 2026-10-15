# mcp_server/managers/state_repository.py
# template=generic version=f35abd82 created=2026-03-12T15:02Z updated=
"""State repository abstractions for one current branch workflow registration."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from mcp_server.core.exceptions import StateNotFoundError
from mcp_server.core.interfaces import IStateReader
from mcp_server.managers.state_version_validator import StateVersionValidator
from mcp_server.utils.atomic_json_writer import AtomicJsonWriter


class StateBranchMismatchError(Exception):
    """Raised when loaded branch state does not match the requested branch."""


class StateAlreadyExistsError(Exception):
    """Raised when initialization would overwrite the same branch registration."""


class BranchState(BaseModel):
    """Validated immutable branch state with explicit registration identity."""

    model_config = ConfigDict(frozen=True, extra="forbid", populate_by_name=True)
    SCHEMA_VERSION: ClassVar[str] = "2.0.0"

    schema_version: str = SCHEMA_VERSION
    branch: str
    parent_branch: str
    issue_number: int | None = None
    workflow_name: str
    current_phase: str
    current_cycle: int | None = None
    last_cycle: int | None = None
    cycle_history: list[dict[str, Any]] = Field(default_factory=list)
    required_phases: list[str] = Field(default_factory=list)
    execution_mode: str = "normal"
    skip_reason: str | None = None
    issue_title: str | None = None
    created_at: str | None = None
    transitions: list[dict[str, Any]] = Field(default_factory=list)
    reconstructed: bool = False
    current_sub_phase: str | None = None

    @field_validator("schema_version")
    @classmethod
    def validate_schema_version(cls, value: str) -> str:
        """Require the current envelope without accepting an older data contract."""
        if value != cls.SCHEMA_VERSION:
            raise ValueError(f"Expected branch-state schema version '{cls.SCHEMA_VERSION}'")
        return value

    @field_validator("branch", "parent_branch")
    @classmethod
    def validate_reference(cls, value: str) -> str:
        """Reject empty or whitespace-containing references without normalizing them."""
        if not value or any(character.isspace() for character in value):
            raise ValueError("Branch references must be nonblank and contain no whitespace")
        return value

    @model_validator(mode="after")
    def validate_parent_identity(self) -> BranchState:
        """A registration must name distinct head and parent references."""
        if self.branch == self.parent_branch:
            raise ValueError("Parent branch must differ from the registered branch")
        return self

    def with_updates(self, **updates: object) -> BranchState:
        """Reconstruct and validate the complete updated state."""
        return type(self).model_validate({**self.model_dump(), **updates})


class FileStateRepository:
    """Filesystem-backed storage of one current branch registration."""

    def __init__(
        self,
        state_file: Path,
        writer: AtomicJsonWriter | None = None,
        state_version_validator: StateVersionValidator | None = None,
    ) -> None:
        self._state_file = state_file
        self._writer = writer or AtomicJsonWriter()
        self._validator = state_version_validator or StateVersionValidator()

    def load(self, branch: str) -> BranchState:
        """Read current registration without moving invalid source or checking branch identity."""
        del branch
        self._validator.validate_file(
            self._state_file, expected_version=BranchState.SCHEMA_VERSION, is_planning=False
        )
        data = json.loads(self._state_file.read_text(encoding="utf-8"))
        return BranchState.model_validate(data)

    def save(self, state: BranchState) -> None:
        """Validate complete field data and atomically replace current registration."""
        validated = BranchState.model_validate(state.model_dump())
        self._writer.write_json(
            self._state_file, validated.model_dump(mode="json"), temp_name=".state.tmp"
        )


class InMemoryStateRepository:
    """Single-current-registration storage with the filesystem repository's semantics."""

    def __init__(self) -> None:
        self._state: BranchState | None = None

    def load(self, branch: str) -> BranchState:
        """Return current valid registration regardless of the requested branch."""
        del branch
        if self._state is None:
            raise StateNotFoundError("No branch state is stored")
        return BranchState.model_validate(self._state.model_dump())

    def save(self, state: BranchState) -> None:
        """Validate and replace the current registration."""
        self._state = BranchState.model_validate(state.model_dump())


class BranchValidatedStateReader:
    """Read-only adapter that enforces exact branch identity on every load."""

    def __init__(self, inner: IStateReader) -> None:
        self._inner = inner

    def load(self, branch: str) -> BranchState:
        """Load state and reject a different stored branch."""
        state: BranchState = self._inner.load(branch)
        if state.branch != branch:
            raise StateBranchMismatchError(
                f"Loaded state branch '{state.branch}' does not match requested branch '{branch}'"
            )
        return state
