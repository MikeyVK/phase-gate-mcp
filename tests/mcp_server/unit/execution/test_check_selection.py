"""Explicit check/argument selection and truthful filesystem/Git scope resolution."""

from __future__ import annotations

from pathlib import Path

from mcp_server.config.schemas.adapter_manifest import CheckCapability
from mcp_server.config.schemas.checks_config import (
    CheckProfile,
    ChecksConfig,
    ConfiguredCheck,
    RunChecksDefaults,
)
from mcp_server.execution.check_selection import (
    CheckSelectionRequest,
    CheckSelector,
    FileScopePaths,
    ScopeResolver,
)
from mcp_server.core.interfaces.execution import AdapterBinding, AdapterLaunch, AdapterPackageIdentity
from mcp_server.core.interfaces.git import BranchChanges
from mcp_server.execution.catalog import AdapterCatalog


class EmptyBranch:
    def get_current_branch(self) -> str:
        return "feature/fixture"

    def get_branch_changes(self, parent: str) -> BranchChanges:
        assert parent == "upstream"
        return BranchChanges(current_paths=(), removed_paths=())


class KnownParent:
    def get_parent_branch(self, branch: str) -> str | None:
        assert branch == "feature/fixture"
        return "upstream"


def selector(tmp_path: Path) -> CheckSelector:
    config = ChecksConfig(
        checks=(("first", ConfiguredCheck(
            adapter_id="fixture", capability="check", timeout_seconds=3, default_args=("--default",)
        )),),
        profiles=(("default", CheckProfile(checks=("first",))),),
        profiles_by_extension=(),
        run_checks=RunChecksDefaults(default_profile="default"),
    )
    catalog = AdapterCatalog(
        checks=(AdapterBinding(
            AdapterPackageIdentity("fixture", "1.0.0", "fixture_snapshot"),
            "check", 1, AdapterLaunch(None, ()),
            CheckCapability(inputs=("selection",)),
        ),),
        tests=(),
        fixes=(),
    )
    return CheckSelector(
        config, catalog, ScopeResolver(FileScopePaths(tmp_path), EmptyBranch(), KnownParent())
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
