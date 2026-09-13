"""Explicit check selection and preservation of filesystem/Git scope behavior."""

from __future__ import annotations

import json
import os
import subprocess
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

import pytest
from git import Actor, Commit, Repo
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from mcp_server.adapters.git_adapter import GitAdapter
from mcp_server.config.schemas.adapter_manifest import CheckCapability
from mcp_server.config.schemas.checks_config import (
    CheckProfile,
    ChecksConfig,
    ConfiguredCheck,
    RunChecksDefaults,
)
from mcp_server.core.exceptions import ConfigError, ExecutionError
from mcp_server.core.interfaces.execution import (
    AdapterBinding,
    AdapterLaunch,
    AdapterPackageIdentity,
)
from mcp_server.core.interfaces.git import BranchChanges, IBranchChangeReader
from mcp_server.execution.catalog import AdapterCatalog
from mcp_server.execution.check_selection import (
    CheckSelectionError,
    CheckSelectionFailureReason,
    CheckSelectionRequest,
    CheckSelector,
    FileScopePaths,
    ScopeResolver,
)


class EmptyBranch:
    def get_current_branch(self) -> str:
        return "feature/fixture"

    def get_branch_changes(self, parent: str) -> BranchChanges:
        assert parent == "upstream"
        return BranchChanges(current_paths=(), removed_paths=())


class UnreadableBranch:
    def get_current_branch(self) -> str:
        raise AssertionError("Invalid selection must be rejected before scope resolution")

    def get_branch_changes(self, parent: str) -> BranchChanges:
        raise AssertionError(f"Unexpected Git request for {parent}")


@dataclass(frozen=True)
class KnownParent:
    parent: str | None = "upstream"

    def get_parent_branch(self, branch: str) -> str | None:
        assert branch == "feature/fixture"
        return self.parent


def configured_checks(*, default_profile: str | None = "default") -> ChecksConfig:
    return ChecksConfig(
        checks=tuple(
            (
                name,
                ConfiguredCheck(
                    adapter_id="fixture",
                    capability=capability,
                    timeout_seconds=timeout,
                    default_args=args,
                ),
            )
            for name, capability, timeout, args in (
                ("first", "check", 3, ("--default",)),
                ("second", "check", 7, ("--second",)),
                ("content", "content", 3, ()),
            )
        ),
        profiles=(
            ("default", CheckProfile(checks=("first",))),
            ("reverse", CheckProfile(checks=("second", "first"))),
        ),
        profiles_by_extension=(),
        run_checks=(
            RunChecksDefaults()
            if default_profile is None
            else RunChecksDefaults(default_profile=default_profile)
        ),
    )


def selector(
    root: Path,
    *,
    config: ChecksConfig | None = None,
    branch: IBranchChangeReader | None = None,
    parent: str | None = "upstream",
    include_catalog: bool = True,
) -> CheckSelector:
    identity = AdapterPackageIdentity("fixture", "1.0.0", "fixture_snapshot")
    launch = AdapterLaunch(None, ())
    catalog = AdapterCatalog(
        checks=(
            AdapterBinding(identity, "check", 1, launch, CheckCapability(inputs=("selection",))),
            AdapterBinding(
                identity,
                "content",
                1,
                launch,
                CheckCapability(inputs=("content",), requires_file=False),
            ),
        )
        if include_catalog
        else (),
        tests=(),
        fixes=(),
    )
    return CheckSelector(
        config if config is not None else configured_checks(),
        catalog,
        ScopeResolver(
            FileScopePaths(root),
            branch if branch is not None else EmptyBranch(),
            KnownParent(parent),
        ),
    )


def test_configured_empty_targets_still_plan_checks_but_empty_branch_has_no_calls(
    tmp_path: Path,
) -> None:
    planner = selector(tmp_path)
    configured = planner.select(CheckSelectionRequest(scope="configured"))
    assert not configured.empty_selection
    assert configured.selected_check_ids == ("first",)
    assert len(configured.calls) == 1
    assert configured.calls[0].request.targets == ()
    assert configured.calls[0].request.args == ("--default",)

    branch = planner.select(CheckSelectionRequest(scope="branch"))
    assert branch.empty_selection
    assert branch.selected_check_ids == ("first",)
    assert branch.calls == ()
    assert branch.removed_targets == ()


def test_profile_and_caller_order_determine_calls_with_binding_defaults(tmp_path: Path) -> None:
    planner = selector(tmp_path)
    requests = (
        CheckSelectionRequest(scope="configured", profile="reverse"),
        CheckSelectionRequest(scope="configured", checks=("second", "first")),
    )
    for request in requests:
        plan = planner.select(request)
        assert plan.selected_check_ids == ("second", "first")
        assert tuple(call.check_id for call in plan.calls) == ("second", "first")
        assert tuple(call.request.args for call in plan.calls) == (("--second",), ("--default",))
        assert tuple(call.timeout_seconds for call in plan.calls) == (7, 3)
        assert planner.select(request) == plan
    default_changed = selector(tmp_path, config=configured_checks(default_profile="reverse"))
    assert default_changed.select(CheckSelectionRequest(scope="configured")).selected_check_ids == (
        "second",
        "first",
    )


@pytest.mark.parametrize(
    ("overrides", "expected", "source"),
    [
        ({}, ("--default",), "configured"),
        ({"first": []}, (), "caller"),
        ({"first": ["--default"]}, ("--default",), "caller"),
        ({"first": ["", " a b ", "--literal"]}, ("", " a b ", "--literal"), "caller"),
    ],
)
def test_addressed_arguments_replace_without_rewriting_or_broadcast(
    tmp_path: Path,
    overrides: dict[str, list[str]],
    expected: tuple[str, ...],
    source: str,
) -> None:
    request = CheckSelectionRequest.model_validate(
        {
            "scope": "configured",
            "profile": "reverse",
            "args": overrides,
            "timeout_seconds": 11,
        }
    )
    plan = selector(tmp_path).select(request)
    second, first = plan.calls
    assert first.request.args == expected
    assert first.args_source == source
    assert second.request.args == ("--second",)
    assert second.args_source == "configured"
    assert tuple(call.timeout_seconds for call in plan.calls) == (11, 11)


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"scope": "auto"},
        {"scope": "targets"},
        {"scope": "targets", "targets": []},
        {"scope": "workspace", "targets": ["nested"]},
        {"scope": "configured", "profile": "default", "checks": ["first"]},
        {"scope": "configured", "checks": ["first", "first"]},
        {"scope": "configured", "args": None},
        {"scope": "configured", "timeout_seconds": True},
        {"scope": "configured", "fresh": True},
    ],
)
def test_invalid_caller_contract_is_rejected(payload: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        CheckSelectionRequest.model_validate(payload)


@pytest.mark.parametrize(
    ("selection", "reason"),
    [
        ({"checks": ["unknown"]}, CheckSelectionFailureReason.UNKNOWN_CHECK),
        ({"profile": "unknown"}, CheckSelectionFailureReason.UNKNOWN_PROFILE),
        ({"checks": ["content"]}, CheckSelectionFailureReason.SELECTION_UNSUPPORTED),
        ({"args": {"second": []}}, CheckSelectionFailureReason.UNSELECTED_ARGS),
        ({"args": {"unknown": []}}, CheckSelectionFailureReason.UNSELECTED_ARGS),
    ],
)
def test_invalid_selection_is_rejected_before_git_resolution(
    tmp_path: Path,
    selection: dict[str, object],
    reason: CheckSelectionFailureReason,
) -> None:
    planner = selector(tmp_path, branch=UnreadableBranch())
    request = CheckSelectionRequest.model_validate({"scope": "branch", **selection})
    with pytest.raises(CheckSelectionError) as caught:
        planner.select(request)
    assert caught.value.reason == reason


def test_missing_defaults_bindings_and_role_catalog_are_not_empty_success(tmp_path: Path) -> None:
    request = CheckSelectionRequest(scope="branch")
    no_checks = ChecksConfig(
        checks=(), profiles=(), profiles_by_extension=(), run_checks=RunChecksDefaults()
    )
    for config, reason in (
        (no_checks, CheckSelectionFailureReason.NO_CONFIGURED_CHECKS),
        (
            configured_checks(default_profile=None),
            CheckSelectionFailureReason.DEFAULT_PROFILE_MISSING,
        ),
    ):
        with pytest.raises(CheckSelectionError) as caught:
            selector(tmp_path, config=config, branch=UnreadableBranch()).select(request)
        assert caught.value.reason == reason
    with pytest.raises(ConfigError):
        selector(tmp_path, branch=UnreadableBranch(), include_catalog=False).select(request)


def test_explicit_targets_are_canonical_language_agnostic_and_directory_covering(
    tmp_path: Path,
) -> None:
    directory = tmp_path / "nested"
    directory.mkdir()
    (directory / "data.json").write_text("{}", encoding="utf-8")
    loose = tmp_path / "readme.md"
    loose.write_text("content", encoding="utf-8")
    spelling = r"nested\data.json" if os.name == "nt" else "nested/data.json"
    planner = selector(tmp_path)
    plan = planner.select(
        CheckSelectionRequest(
            scope="targets", targets=("readme.md", spelling, "nested", "readme.md")
        )
    )
    assert plan.scope.targets == tuple(sorted((directory, loose), key=str))
    assert plan.calls[0].request.targets == tuple(str(path) for path in plan.scope.targets)
    workspace = planner.select(CheckSelectionRequest(scope="workspace"))
    assert workspace.scope.targets == (tmp_path,)
    assert workspace.calls[0].request.targets == (str(tmp_path),)


def test_missing_escape_and_equivalent_workspace_targets_are_rejected(tmp_path: Path) -> None:
    planner = selector(tmp_path)
    for target in ("missing.md", ".", "./"):
        with pytest.raises(CheckSelectionError) as caught:
            planner.select(CheckSelectionRequest(scope="targets", targets=(target,)))
        assert caught.value.reason == CheckSelectionFailureReason.INVALID_TARGETS
    for target in ("../outside", "/absolute", r"C:\outside", r"nested\..\outside"):
        with pytest.raises(ValidationError):
            CheckSelectionRequest(scope="targets", targets=(target,))


def test_real_directory_link_cannot_escape_workspace(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    outside = tmp_path / "outside"
    workspace.mkdir()
    outside.mkdir()
    (outside / "file.md").write_text("outside", encoding="utf-8")
    link = workspace / "linked"
    if os.name == "nt":
        subprocess.run(
            ["cmd", "/d", "/c", "mklink", "/J", str(link), str(outside)],
            check=True,
            capture_output=True,
        )
    else:
        link.symlink_to(outside, target_is_directory=True)
    try:
        with pytest.raises(CheckSelectionError) as caught:
            selector(workspace).select(
                CheckSelectionRequest(scope="targets", targets=("linked/file.md",))
            )
        assert caught.value.reason == CheckSelectionFailureReason.INVALID_TARGETS
    finally:
        if os.name == "nt":
            link.rmdir()
        else:
            link.unlink()


ACTOR = Actor("Scope Fixture", "scope@example.invalid")


def commit(repo: Repo, message: str) -> Commit:
    return repo.index.commit(message, author=ACTOR, committer=ACTOR)


@pytest.fixture
def branch_repo(tmp_path: Path) -> Iterator[Repo]:
    repo = Repo.init(tmp_path, initial_branch="upstream")
    for name in (
        "keep.md",
        "rename.md",
        "deleted.ts",
        "staged.txt",
        "unstaged.json",
        "ignored-tracked",
    ):
        (tmp_path / name).write_text(f"baseline {name}\n", encoding="utf-8")
    repo.index.add(
        ["keep.md", "rename.md", "deleted.ts", "staged.txt", "unstaged.json", "ignored-tracked"]
    )
    (tmp_path / ".gitignore").write_text("ignored*\n", encoding="utf-8")
    repo.index.add([".gitignore"])
    commit(repo, "baseline")
    repo.create_head("feature/fixture").checkout()
    try:
        yield repo
    finally:
        repo.close()


def test_branch_uses_merge_base_and_current_mixed_language_working_state(
    tmp_path: Path,
    branch_repo: Repo,
) -> None:
    repo = branch_repo
    (tmp_path / "rename.md").rename(tmp_path / "renamed.md")
    (tmp_path / "deleted.ts").unlink()
    (tmp_path / "committed.yaml").write_text("committed: yes", encoding="utf-8")
    repo.index.remove(["rename.md", "deleted.ts"])
    repo.index.add(["renamed.md", "committed.yaml"])
    commit(repo, "branch changes")
    repo.heads["upstream"].checkout()
    (tmp_path / "upstream-only.md").write_text("parent divergence", encoding="utf-8")
    repo.index.add(["upstream-only.md"])
    commit(repo, "parent changes")
    repo.heads["feature/fixture"].checkout()
    (tmp_path / "staged.txt").write_text("staged", encoding="utf-8")
    repo.index.add(["staged.txt"])
    (tmp_path / "unstaged.json").write_text("staged JSON content", encoding="utf-8")
    repo.index.add(["unstaged.json"])
    for name in ("unstaged.json", "untracked.data", "ignored-tracked", "ignored-new"):
        (tmp_path / name).write_text("working", encoding="utf-8")

    adapter = GitAdapter(str(tmp_path))
    try:
        planner = selector(tmp_path, branch=adapter)
        plan = planner.select(CheckSelectionRequest(scope="branch"))
        expected = (
            "committed.yaml",
            "ignored-tracked",
            "renamed.md",
            "staged.txt",
            "unstaged.json",
            "untracked.data",
        )
        assert plan.scope.targets == tuple(tmp_path / name for name in expected)
        assert plan.removed_targets == ("deleted.ts", "rename.md")
        assert not plan.empty_selection
        assert (tmp_path / "staged.txt").read_text(encoding="utf-8") == "staged"
        assert (tmp_path / "unstaged.json").read_text(encoding="utf-8") == "working"
        assert planner.select(CheckSelectionRequest(scope="branch")) == plan
    finally:
        adapter.repo.close()


def test_deleted_only_branch_has_evidence_without_runnable_calls(
    tmp_path: Path,
    branch_repo: Repo,
) -> None:
    (tmp_path / "deleted.ts").unlink()
    branch_repo.index.remove(["deleted.ts"])
    commit(branch_repo, "delete only")
    adapter = GitAdapter(str(tmp_path))
    try:
        plan = selector(tmp_path, branch=adapter).select(CheckSelectionRequest(scope="branch"))
        assert plan.empty_selection
        assert plan.calls == ()
        assert plan.removed_targets == ("deleted.ts",)
    finally:
        adapter.repo.close()


def test_missing_parent_invalid_revision_and_unrelated_history_are_errors(
    tmp_path: Path,
    branch_repo: Repo,
) -> None:
    adapter = GitAdapter(str(tmp_path))
    try:
        request = CheckSelectionRequest(scope="branch")
        for parent in (None, "missing-parent"):
            with pytest.raises(ExecutionError):
                selector(tmp_path, branch=adapter, parent=parent).select(request)
        unrelated = Commit.create_from_tree(
            branch_repo,
            branch_repo.head.commit.tree,
            "unrelated",
            parent_commits=[],
            author=ACTOR,
            committer=ACTOR,
        )
        branch_repo.create_head("unrelated", unrelated)
        with pytest.raises(ExecutionError, match="merge-base"):
            selector(tmp_path, branch=adapter, parent="unrelated").select(request)
    finally:
        adapter.repo.close()


def test_native_selection_request_matches_published_wire_contract(
    tmp_path: Path,
    pytestconfig: pytest.Config,
) -> None:
    schema_path = pytestconfig.rootpath / "mcp_server/execution/contracts/check_v1.schema.json"
    validator = Draft202012Validator(json.loads(schema_path.read_text(encoding="utf-8")))
    planner = selector(tmp_path)
    for scope in ("configured", "workspace"):
        plan = planner.select(CheckSelectionRequest.model_validate({"scope": scope}))
        payload = plan.calls[0].request.model_dump(mode="json")
        assert set(payload) == {"operation", "targets", "args"}
        assert validator.is_valid(payload), list(validator.iter_errors(payload))


def test_deleted_file_replaced_by_directory_does_not_expand_branch_targets(
    tmp_path: Path,
    branch_repo: Repo,
) -> None:
    (tmp_path / "deleted.ts").unlink()
    (tmp_path / "deleted.ts").mkdir()
    selected = tmp_path / "deleted.ts" / "new.md"
    selected.write_text("new", encoding="utf-8")
    (tmp_path / "deleted.ts" / "ignored-secret").write_text("ignored", encoding="utf-8")
    adapter = GitAdapter(str(tmp_path))
    try:
        plan = selector(tmp_path, branch=adapter).select(CheckSelectionRequest(scope="branch"))
        assert plan.scope.targets == (selected,)
        assert plan.removed_targets == ("deleted.ts",)
        assert plan.calls[0].request.targets == (str(selected),)
    finally:
        adapter.repo.close()


def test_missing_current_path_is_not_reported_as_git_deletion(tmp_path: Path) -> None:
    class DisappearedCurrentPath(EmptyBranch):
        def get_branch_changes(self, parent: str) -> BranchChanges:
            assert parent == "upstream"
            return BranchChanges(current_paths=("disappeared.md",), removed_paths=())

    with pytest.raises(CheckSelectionError) as caught:
        selector(tmp_path, branch=DisappearedCurrentPath()).select(
            CheckSelectionRequest(scope="branch")
        )
    assert caught.value.reason == CheckSelectionFailureReason.INVALID_TARGETS
    assert caught.value.selection_id == "disappeared.md"
