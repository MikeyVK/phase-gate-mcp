"""Tests for WorkflowStatusResolver (C3: C_RESOLVER_CORE RED phase)."""
from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import MagicMock

import pytest

from mcp_server.config.schemas.workphases import PhaseDefinition, WorkphasesConfig

if TYPE_CHECKING:
    pass

_TEST_WORKPHASES = WorkphasesConfig(
    phases={
        "research": PhaseDefinition(commit_type_hint="docs"),
        "planning": PhaseDefinition(commit_type_hint="docs"),
        "design": PhaseDefinition(commit_type_hint="docs"),
        "implementation": PhaseDefinition(
            commit_type_hint=None, subphases=["red", "green", "refactor"]
        ),
        "validation": PhaseDefinition(commit_type_hint="test"),
        "documentation": PhaseDefinition(commit_type_hint="docs"),
        "ready": PhaseDefinition(commit_type_hint="chore", terminal=True),
    }
)


class TestWorkflowStatusDTO:
    """WorkflowStatusDTO shape and immutability."""

    def test_dto_has_required_fields(self) -> None:
        from mcp_server.state.workflow_status import WorkflowStatusDTO

        dto = WorkflowStatusDTO(
            current_phase="implementation",
            phase_source="commit-scope",
            phase_confidence="high",
        )
        assert dto.current_phase == "implementation"
        assert dto.sub_phase is None
        assert dto.current_cycle is None
        assert dto.phase_source == "commit-scope"
        assert dto.phase_confidence == "high"
        assert dto.phase_detection_error is None

    def test_dto_is_frozen(self) -> None:
        from mcp_server.state.workflow_status import WorkflowStatusDTO

        dto = WorkflowStatusDTO(
            current_phase="research",
            phase_source="state.json",
            phase_confidence="medium",
        )
        with pytest.raises(Exception):  # noqa: PT011
            dto.current_phase = "other"  # type: ignore[misc]

    def test_dto_rejects_extra_fields(self) -> None:
        from mcp_server.state.workflow_status import WorkflowStatusDTO
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            WorkflowStatusDTO(  # type: ignore[call-arg]
                current_phase="research",
                phase_source="state.json",
                phase_confidence="high",
                unexpected_field="boom",
            )

    def test_dto_with_all_optional_fields(self) -> None:
        from mcp_server.state.workflow_status import WorkflowStatusDTO

        dto = WorkflowStatusDTO(
            current_phase="implementation",
            sub_phase="red",
            current_cycle=2,
            phase_source="commit-scope",
            phase_confidence="high",
            phase_detection_error=None,
        )
        assert dto.sub_phase == "red"
        assert dto.current_cycle == 2


class TestIGitContextReader:
    """IGitContextReader protocol surface exists."""

    def test_protocol_has_get_current_branch(self) -> None:
        from mcp_server.core.interfaces import IGitContextReader

        assert hasattr(IGitContextReader, "get_current_branch")

    def test_protocol_has_get_recent_commits(self) -> None:
        from mcp_server.core.interfaces import IGitContextReader

        assert hasattr(IGitContextReader, "get_recent_commits")

    def test_concrete_class_satisfies_protocol(self) -> None:
        from mcp_server.core.interfaces import IGitContextReader

        class _Stub:
            def get_current_branch(self) -> str:
                return "feature/99-test"

            def get_recent_commits(self, limit: int = 5) -> list[str]:
                return []

        assert isinstance(_Stub(), IGitContextReader)


class TestCommitPhaseDetector:
    """CommitPhaseDetector wraps ScopeDecoder with fallback_to_state=False."""

    def test_detector_exists_and_detects_from_commit(self, tmp_path: pytest.TempPathFactory) -> None:
        from mcp_server.core.commit_phase_detector import CommitPhaseDetector

        detector = CommitPhaseDetector(workspace_root=tmp_path, workphases_config=_TEST_WORKPHASES)
        result = detector.detect_from_commit("feat(P_IMPLEMENTATION_SP_C3_GREEN): add dto")
        assert result["workflow_phase"] == "implementation"
        assert result["source"] == "commit-scope"

    def test_detector_never_reads_state_json(self, tmp_path: pytest.TempPathFactory) -> None:
        """Even with a valid state.json present, detector uses commit-scope only."""
        from mcp_server.core.commit_phase_detector import CommitPhaseDetector

        state_dir = tmp_path / ".st3"
        state_dir.mkdir()
        (state_dir / "state.json").write_text(
            '{"branch": "main", "current_phase": "research", "workflow_name": "feature"}'
        )
        detector = CommitPhaseDetector(workspace_root=tmp_path, workphases_config=_TEST_WORKPHASES)
        result = detector.detect_from_commit("feat(P_IMPLEMENTATION_SP_C3_RED): add tests")
        # Must read commit-scope, NOT state.json
        assert result["source"] == "commit-scope"
        assert result["workflow_phase"] == "implementation"

    def test_detector_returns_unknown_for_missing_scope(
        self, tmp_path: pytest.TempPathFactory
    ) -> None:
        from mcp_server.core.commit_phase_detector import CommitPhaseDetector

        detector = CommitPhaseDetector(workspace_root=tmp_path, workphases_config=_TEST_WORKPHASES)
        result = detector.detect_from_commit("chore: bump version")
        assert result["workflow_phase"] == "unknown"
        assert result["source"] == "unknown"

    def test_detector_returns_unknown_for_none_commit(
        self, tmp_path: pytest.TempPathFactory
    ) -> None:
        from mcp_server.core.commit_phase_detector import CommitPhaseDetector

        detector = CommitPhaseDetector(workspace_root=tmp_path, workphases_config=_TEST_WORKPHASES)
        result = detector.detect_from_commit(None)
        assert result["workflow_phase"] == "unknown"


class TestWorkflowStatusResolver:
    """WorkflowStatusResolver resolves current branch status."""

    def _make_resolver(
        self,
        branch: str = "feature/50-test",
        commits: list[str] | None = None,
        state_phase: str = "implementation",
        state_cycle: int | None = 3,
        *,
        tmp_path: object,
    ) -> object:
        from mcp_server.managers.workflow_status_resolver import WorkflowStatusResolver
        from mcp_server.managers.state_repository import BranchState, InMemoryStateRepository
        from mcp_server.core.commit_phase_detector import CommitPhaseDetector

        git_reader = MagicMock()
        git_reader.get_current_branch.return_value = branch
        git_reader.get_recent_commits.return_value = commits or []

        state_repo = InMemoryStateRepository()
        state_repo.save(
            BranchState(
                branch=branch,
                current_phase=state_phase,
                current_cycle=state_cycle,
                workflow_name="feature",
                issue_number=50,
                parent_branch="main",
            )
        )

        detector = CommitPhaseDetector(workspace_root=tmp_path, workphases_config=_TEST_WORKPHASES)  # type: ignore[arg-type]
        return WorkflowStatusResolver(
            git_context_reader=git_reader,
            state_reader=state_repo,
            commit_phase_detector=detector,
        )

    def test_resolve_current_returns_dto(self, tmp_path: pytest.TempPathFactory) -> None:
        from mcp_server.state.workflow_status import WorkflowStatusDTO

        resolver = self._make_resolver(
            commits=["feat(P_IMPLEMENTATION_SP_C3_GREEN): add resolver"],
            tmp_path=tmp_path,
        )
        result = resolver.resolve_current()
        assert isinstance(result, WorkflowStatusDTO)

    def test_resolve_uses_commit_scope_when_high_confidence(
        self, tmp_path: pytest.TempPathFactory
    ) -> None:
        resolver = self._make_resolver(
            commits=["feat(P_IMPLEMENTATION_SP_C3_GREEN): add resolver"],
            tmp_path=tmp_path,
        )
        result = resolver.resolve_current()
        assert result.phase_source == "commit-scope"
        assert result.phase_confidence == "high"
        assert result.current_phase == "implementation"

    def test_resolve_falls_back_to_state_when_no_commit_scope(
        self, tmp_path: pytest.TempPathFactory
    ) -> None:
        resolver = self._make_resolver(
            commits=["chore: bump version"],
            state_phase="research",
            state_cycle=None,
            tmp_path=tmp_path,
        )
        result = resolver.resolve_current()
        assert result.phase_source == "state.json"
        assert result.current_phase == "research"

    def test_resolve_current_cycle_from_state(self, tmp_path: pytest.TempPathFactory) -> None:
        resolver = self._make_resolver(
            commits=["feat(P_IMPLEMENTATION_SP_C3_GREEN): add resolver"],
            state_cycle=3,
            tmp_path=tmp_path,
        )
        result = resolver.resolve_current()
        assert result.current_cycle == 3

    def test_resolve_handles_branch_mismatch_gracefully(
        self, tmp_path: pytest.TempPathFactory
    ) -> None:
        """When state.json has a different branch, resolver falls back to unknown."""
        from mcp_server.managers.workflow_status_resolver import WorkflowStatusResolver
        from mcp_server.managers.state_repository import BranchState, InMemoryStateRepository
        from mcp_server.core.commit_phase_detector import CommitPhaseDetector

        git_reader = MagicMock()
        git_reader.get_current_branch.return_value = "feature/99-other"
        git_reader.get_recent_commits.return_value = []

        state_repo = InMemoryStateRepository()
        state_repo.save(
            BranchState(
                branch="feature/50-test",  # mismatch
                current_phase="research",
                workflow_name="feature",
                issue_number=50,
                parent_branch="main",
            )
        )

        detector = CommitPhaseDetector(workspace_root=tmp_path, workphases_config=_TEST_WORKPHASES)  # type: ignore[arg-type]
        resolver = WorkflowStatusResolver(
            git_context_reader=git_reader,
            state_reader=state_repo,
            commit_phase_detector=detector,
        )
        result = resolver.resolve_current()
        assert result.phase_source in ("unknown", "state.json")
        # Must not raise; graceful degradation
