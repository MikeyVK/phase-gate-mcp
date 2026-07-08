# tests/mcp_server/unit/schemas/test_tracking_artifact_schema.py
# SCAFFOLD: test:manual | 2026-02-18T00:00:00Z
"""Schema and pipeline tests for tracking artifact types.

Covers: commit, pr, issue (all ephemeral — write to .pgmcp/temp/)

2 tests per artifact type:
  1. context_validates_minimal  - schema instantiates with required fields
  2. rejects_invalid_context    - empty context raises ValidationError

@layer: Tests (Unit)
@dependencies: pytest, pydantic, tracking artifact schemas, mcp_server scaffolding pipeline
"""

import asyncio  # noqa: I001
import os
from pathlib import Path

import pytest

from mcp_server.core.exceptions import ValidationError
from mcp_server.managers.artifact_manager import ArtifactManager
from tests.mcp_server.test_support import make_artifact_manager


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _make_manager(tmp_path: Path) -> ArtifactManager:
    return make_artifact_manager(tmp_path)


def _run_v2_tracking(manager: ArtifactManager, artifact_type: str, context: dict) -> str:
    """Run V2 pipeline for tracking (ephemeral) artifacts, return rendered content.

    Unlike _run_v2 (which mocks fs_adapter.write_file), tracking artifacts bypass
    fs_adapter and write to .pgmcp/temp/ via Path.write_text. We patch _validate_and_write
    to capture content before the ephemeral write occurs.
    """
    output_captured: list[str] = []
    original_vaw = manager._validate_and_write  # type: ignore[reportPrivateUsage]

    async def mock_vaw(
        art_type: str,  # noqa: ARG001
        path: str,  # noqa: ARG001
        content: str,
        **kwargs: object,  # noqa: ARG001
    ) -> str:
        output_captured.append(content)
        return "mocked_path"

    manager._validate_and_write = mock_vaw  # type: ignore[method-assign]
    os.environ["PYDANTIC_SCAFFOLDING_ENABLED"] = "true"
    try:
        asyncio.run(manager.scaffold_artifact(artifact_type, **context))
    finally:
        os.environ.pop("PYDANTIC_SCAFFOLDING_ENABLED", None)
        manager._validate_and_write = original_vaw  # type: ignore[method-assign]

    assert len(output_captured) == 1, f"V2 pipeline produced no output for {artifact_type}"
    return output_captured[0]


def _spy_v2_routed(manager: ArtifactManager) -> list[bool]:
    """Spy whether _enrich_schema_context is called (V2 pipeline active, not V1 fallback)."""
    v2_calls: list[bool] = []
    original = manager._enrich_schema_context  # type: ignore[reportPrivateUsage]

    def spy(*args, **kwargs):  # noqa: ANN002, ANN003, ANN202
        v2_calls.append(True)
        return original(*args, **kwargs)

    manager._enrich_schema_context = spy  # type: ignore[method-assign]
    return v2_calls


# ---------------------------------------------------------------------------
# Commit (3 tests)
# ---------------------------------------------------------------------------


class TestCommitV2Parity:
    """V2 parity tests for commit tracking artifact."""

    @pytest.fixture
    def manager(self, tmp_path: Path) -> ArtifactManager:
        return _make_manager(tmp_path)

    _MINIMAL = {
        "type": "feat",
        "message": "add V2 schemas for tracking artifacts",
    }

    def test_commit_context_validates_minimal(self) -> None:
        """CommitContext schema accepts minimal required fields."""
        from mcp_server.schemas import CommitContext  # noqa: PLC0415

        ctx = CommitContext(**self._MINIMAL)
        assert ctx.type == self._MINIMAL["type"]
        assert ctx.message == self._MINIMAL["message"]

    def test_commit_v2_routing_confirmed(self, manager: ArtifactManager) -> None:
        """Commit V2 pipeline routes via _enrich_schema_context (not V1 fallback)."""
        calls = _spy_v2_routed(manager)
        _run_v2_tracking(manager, "commit", self._MINIMAL)
        assert len(calls) == 1, "V2 routing not active for commit — not in _v2_context_registry"

    def test_commit_v2_rejects_invalid_context(self, manager: ArtifactManager) -> None:
        """Commit V2 pipeline rejects empty context with ValidationError."""
        with pytest.raises(ValidationError):
            _run_v2_tracking(manager, "commit", {})


# ---------------------------------------------------------------------------
# PR (3 tests)
# ---------------------------------------------------------------------------


class TestPRV2Parity:
    """V2 parity tests for pr tracking artifact."""

    @pytest.fixture
    def manager(self, tmp_path: Path) -> ArtifactManager:
        return _make_manager(tmp_path)

    _MINIMAL = {
        "title": "Cycle 7: Add V2 schemas for tracking artifacts",
        "changes": "Added CommitContext, PRContext, IssueContext schemas",
    }

    def test_pr_context_validates_minimal(self) -> None:
        """PRContext schema accepts minimal required fields."""
        from mcp_server.schemas import PRContext  # noqa: PLC0415

        ctx = PRContext(**self._MINIMAL)
        assert ctx.title == self._MINIMAL["title"]
        assert ctx.changes == self._MINIMAL["changes"]

    def test_pr_v2_routing_confirmed(self, manager: ArtifactManager) -> None:
        """PR V2 pipeline routes via _enrich_schema_context (not V1 fallback)."""
        calls = _spy_v2_routed(manager)
        _run_v2_tracking(manager, "pr", self._MINIMAL)
        assert len(calls) == 1, "V2 routing not active for pr — not in _v2_context_registry"

    def test_pr_v2_rejects_invalid_context(self, manager: ArtifactManager) -> None:
        """PR V2 pipeline rejects empty context with ValidationError."""
        with pytest.raises(ValidationError):
            _run_v2_tracking(manager, "pr", {})

    def test_pr_context_deferred_work_and_tracking_state_optional(self) -> None:
        """PRContext accepts deferred_work and tracking_state as optional fields."""
        from mcp_server.schemas import PRContext  # noqa: PLC0415

        ctx = PRContext(
            **self._MINIMAL,
            deferred_work="Issue #400: deferred multi-remote support",
            tracking_state="Tracked via #400",
        )
        assert ctx.deferred_work == "Issue #400: deferred multi-remote support"
        assert ctx.tracking_state == "Tracked via #400"


# ---------------------------------------------------------------------------
# Issue (3 tests)
# ---------------------------------------------------------------------------


class TestIssueV2Parity:
    """V2 parity tests for issue tracking artifact."""

    @pytest.fixture
    def manager(self, tmp_path: Path) -> ArtifactManager:
        return _make_manager(tmp_path)

    _MINIMAL = {
        "title": "Add V2 schemas for tracking artifacts",
        "problem": "Tracking artifact types commit/pr/issue lack Pydantic V2 schemas",
    }

    def test_issue_context_validates_minimal(self) -> None:
        """IssueContext schema accepts minimal required fields."""
        from mcp_server.schemas import IssueContext  # noqa: PLC0415

        ctx = IssueContext(**self._MINIMAL)
        assert ctx.title == self._MINIMAL["title"]
        assert ctx.problem == self._MINIMAL["problem"]

    def test_issue_v2_routing_confirmed(self, manager: ArtifactManager) -> None:
        """Issue V2 pipeline routes via _enrich_schema_context (not V1 fallback)."""
        calls = _spy_v2_routed(manager)
        _run_v2_tracking(manager, "issue", self._MINIMAL)
        assert len(calls) == 1, "V2 routing not active for issue — not in _v2_context_registry"

    def test_issue_v2_rejects_invalid_context(self, manager: ArtifactManager) -> None:
        """Issue V2 pipeline rejects empty context with ValidationError."""
        with pytest.raises(ValidationError):
            _run_v2_tracking(manager, "issue", {})
