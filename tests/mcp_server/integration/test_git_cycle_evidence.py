# pgmcp:v1 id=pytest_integration_test pv=1.0.0 pf=70EjvGU6LK1YPSz3 sf=5--KpGf2wHUv2qAj

"Local captured-HEAD evidence and title attribution at the real Git boundary."

# Standard library
from pathlib import Path
from unittest.mock import MagicMock

# Third party
import pytest
from git import Actor, Repo

# Project
from mcp_server.adapters.git_adapter import GitAdapter
from mcp_server.core.interfaces.git import (
    CommitHistorySnapshot,
    CommitHistoryUnavailableError,
    CommitRecord,
)
from mcp_server.core.operation_notes import NoteContext
from tests.mcp_server.test_support import make_git_manager


@pytest.fixture
def history(tmp_path: Path) -> tuple[Repo, GitAdapter]:
    "A deep branch with execution evidence on both merge parents."
    repo = Repo.init(tmp_path)
    actor = Actor("Evidence Test", "evidence@example.com")
    root = repo.index.commit("chore: root", author=actor, committer=actor)
    branch = repo.create_head("refactor/491-evidence", root)
    branch.checkout()
    repo.index.commit("feat(P_IMPLEMENTATION_C1): old work (#491)", author=actor, committer=actor)
    left = repo.head.commit
    side = repo.create_head("side", root)
    side.checkout()
    right = repo.index.commit(
        "feat(P_IMPLEMENTATION_C3_SP_GREEN): side work (#491)", author=actor, committer=actor
    )
    branch.checkout()
    repo.index.commit("chore: merge", parent_commits=(left, right), author=actor, committer=actor)
    for message in [
        "docs(P_DESIGN_C8): another phase (#491)",
        "feat(P_IMPLEMENTATION_C7): another issue (#492)",
        "feat(P_IMPLEMENTATION_C9): body only\n\n(#491)",
        "feat(P_IMPLEMENTATION_C6): nonterminal (#491) follows",
        *(f"chore: newer {index}" for index in range(6)),
    ]:
        repo.index.commit(message, author=actor, committer=actor)
    return repo, GitAdapter(str(tmp_path))


def test_complete_ancestry_and_exact_subject_attribution(history: tuple[Repo, GitAdapter]) -> None:
    "Old and merged execution commits qualify while other phases/issues and body markers do not."
    repo, adapter = history
    result = make_git_manager(adapter=adapter).read_cycle_evidence(491, "implementation")
    assert result.status == "complete"
    assert result.protected_cycle_numbers == (1, 3)
    assert result.head_sha == repo.head.commit.hexsha
    assert result.branch == repo.active_branch.name


def test_unknown_scope_retains_known_positive_cycles(history: tuple[Repo, GitAdapter]) -> None:
    "An undecodable attributed subject retains positives and makes absence uncertain."
    repo, adapter = history
    actor = Actor("Evidence Test", "evidence@example.com")
    unknown = repo.index.commit("chore: undecodable (#491)", author=actor, committer=actor)
    result = make_git_manager(adapter=adapter).read_cycle_evidence(491, "implementation")
    assert result.status == "unavailable"
    assert result.reason_code == "commit_scope_unavailable"
    assert result.diagnostic_commit_sha == unknown.hexsha
    assert result.protected_cycle_numbers == (1, 3)


def test_shallow_and_failed_reads_are_explicit() -> None:
    "Incomplete snapshots retain positives; traversal failures remain unavailable."
    adapter = MagicMock(spec=GitAdapter)
    adapter.read_issue_history.return_value = CommitHistorySnapshot(
        "refactor/491-evidence",
        "captured",
        True,
        (CommitRecord("positive", "feat(P_IMPLEMENTATION_C2): work (#491)"),),
    )
    manager = make_git_manager(adapter=adapter)
    shallow = manager.read_cycle_evidence(491, "implementation")
    assert shallow.status == "unavailable"
    assert shallow.reason_code == "git_history_shallow"
    assert shallow.protected_cycle_numbers == (2,)
    adapter.read_issue_history.side_effect = CommitHistoryUnavailableError(
        "git_history_unavailable", "refactor/491-evidence", "captured"
    )
    failed = manager.read_cycle_evidence(491, "implementation")
    assert failed.status == "unavailable"
    assert failed.reason_code == "git_history_unavailable"
    assert failed.head_sha == "captured"
    assert adapter.read_issue_history.call_count == 2


def test_title_normalization_preserves_other_references_and_body() -> None:
    "Own issue markers are collapsed into one terminal title marker and the body is preserved."
    adapter = MagicMock(spec=GitAdapter)
    adapter.commit.return_value = "new"
    manager = make_git_manager(adapter=adapter)
    body = "\n\nDetails about #491 stay here."
    manager.commit_with_scope(
        workflow_phase="implementation",
        cycle_number=1,
        message="fix #491 (#491) mentions #49 and #4910" + body,
        issue_number=491,
        commit_type="fix",
        note_context=NoteContext(),
    )
    assert adapter.commit.call_args.args[0] == (
        "fix(P_IMPLEMENTATION_C1): fix mentions #49 and #4910 (#491)" + body
    )


def test_detached_head_and_missing_execution_cycle_are_unavailable(
    history: tuple[Repo, GitAdapter],
) -> None:
    "A detached branch or missing execution-cycle value cannot justify absence of cycle work."
    repo, adapter = history
    actor = Actor("Evidence Test", "evidence@example.com")
    repo.index.commit("feat(P_IMPLEMENTATION): missing cycle (#491)", author=actor, committer=actor)
    missing = make_git_manager(adapter=adapter).read_cycle_evidence(491, "implementation")
    assert missing.reason_code == "execution_cycle_missing"
    assert missing.protected_cycle_numbers == (1, 3)
    repo.git.checkout("--detach", repo.head.commit.hexsha)
    detached = make_git_manager(adapter=adapter).read_cycle_evidence(491, "implementation")
    assert detached.reason_code == "git_head_detached"
    assert detached.status == "unavailable"
