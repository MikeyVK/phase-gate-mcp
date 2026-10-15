"""Tests for filesystem and status components.

@layer: Tests (Integration)
@dependencies: pytest, pathlib, unittest.mock, mcp_server.adapters.filesystem,
    mcp_server.resources.status
"""

import json
from pathlib import Path
from unittest.mock import Mock

import pytest

from mcp_server.adapters.filesystem import FilesystemAdapter
from mcp_server.core.exceptions import ValidationError
from mcp_server.managers.state_repository import (
    BranchState,
    BranchValidatedStateReader,
    FileStateRepository,
    StateBranchMismatchError,
    StateNotFoundError,
)
from mcp_server.resources.status import StatusResource


def test_fs_adapter_read_write(tmp_path: Path) -> None:
    """Test filesystem adapter can write and read files correctly."""
    adapter = FilesystemAdapter(root_path=str(tmp_path))

    adapter.write_file("test.txt", "content")
    assert (tmp_path / "test.txt").exists()
    assert adapter.read_file("test.txt") == "content"


def test_fs_adapter_security(tmp_path: Path) -> None:
    """Test filesystem adapter prevents path traversal attacks."""
    adapter = FilesystemAdapter(root_path=str(tmp_path))

    with pytest.raises(ValidationError):
        adapter.read_file("../outside.txt")


@pytest.mark.asyncio
@pytest.mark.parametrize("state_branch", ["feature/test", "docs/other", None])
async def test_status_resource(tmp_path: Path, state_branch: str | None) -> None:
    """Report persisted phases and preserve missing/mismatched state failures."""
    mock_git = Mock()
    mock_git.get_status.return_value = {"branch": "feature/test", "is_clean": True}
    repository = FileStateRepository(state_file=tmp_path / "state.json")
    if state_branch is not None:
        repository.save(
            BranchState(
                branch=state_branch,
                workflow_name="custom",
                current_phase="review",
                parent_branch="main",
            )
        )
    state_reader = BranchValidatedStateReader(inner=repository)
    resource = StatusResource(git_context_reader=mock_git, state_reader=state_reader)

    if state_branch != "feature/test":
        expected_error = StateNotFoundError if state_branch is None else StateBranchMismatchError
        with pytest.raises(expected_error):
            await resource.read("pgmcp://status/phase")
        return

    data = json.loads(await resource.read("pgmcp://status/phase"))
    assert data["current_phase"] == "review"
    assert data["active_branch"] == "feature/test"
    assert data["is_clean"] is True
