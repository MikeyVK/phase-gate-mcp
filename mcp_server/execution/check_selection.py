"""Resolve explicit check obligations, native arguments, and filesystem/Git scopes."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path, PureWindowsPath
from typing import Annotated, Literal

from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    StrictInt,
    StrictStr,
    StringConstraints,
    model_validator,
)

from mcp_server.config.schemas.adapter_manifest import CapabilityId, CheckCapability
from mcp_server.config.schemas.checks_config import CheckId, ChecksConfig, ProfileId
from mcp_server.core.interfaces.execution import (
    AdapterBinding,
    CheckCatalogReader,
    ConfiguredTargetFilter,
    ResolvedScopePath,
    ScopePaths,
)
from mcp_server.core.interfaces.git import (
    BranchBasisUnavailableError,
    IBranchChangeReader,
    IBranchParentReader,
)

CheckScope = Literal["configured", "workspace", "targets", "branch"]
ArgsSource = Literal["configured", "caller"]


def _relative_path(value: str) -> str:
    if (
        not value.strip()
        or "\x00" in value
        or re.search(r"^(?:[\\/]|[A-Za-z]:)", value)
        or re.search(r"(?:^|[\\/])\.\.(?:[\\/]|$)", value)
    ):
        raise ValueError("workspace_relative_path_required")
    return value


def _absolute_path(value: str) -> str:
    if (
        "\x00" in value
        or re.search(r"^(?:/|[A-Za-z]:[\\/]|\\\\[^\\/]+[\\/][^\\/]+)[\s\S]*$(?![\s\S])", value)
        is None
    ):
        raise ValueError("absolute_path_required")
    return value


def _tuple(value: object) -> object:
    return tuple(value) if isinstance(value, list) else value


def _args_map(value: object) -> object:
    return tuple(value.items()) if isinstance(value, dict) else value


WorkspaceRelativePath = Annotated[
    str, StringConstraints(strict=True, min_length=1), AfterValidator(_relative_path)
]
AbsolutePath = Annotated[
    str, StringConstraints(strict=True, min_length=1), AfterValidator(_absolute_path)
]
NativeArguments = Annotated[tuple[StrictStr, ...], BeforeValidator(_tuple)]
AddressedArguments = Annotated[
    tuple[tuple[CheckId, NativeArguments], ...], BeforeValidator(_args_map)
]


class CheckSelectionRequest(BaseModel):
    """Internal immutable caller selection; public tool activation is separate."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    scope: CheckScope
    targets: (
        Annotated[tuple[WorkspaceRelativePath, ...], BeforeValidator(_tuple), Field(min_length=1)]
        | None
    ) = None
    profile: ProfileId | None = None
    checks: Annotated[tuple[CheckId, ...], BeforeValidator(_tuple), Field(min_length=1)] | None = (
        None
    )
    args: AddressedArguments | None = None
    timeout_seconds: Annotated[StrictInt, Field(gt=0)] | None = None

    @model_validator(mode="after")
    def validate_selection(self) -> CheckSelectionRequest:
        for name in ("targets", "profile", "checks", "args", "timeout_seconds"):
            if name in self.model_fields_set and getattr(self, name) is None:
                raise ValueError(f"{name}_must_be_omitted")
        if (self.scope == "targets") != (self.targets is not None):
            raise ValueError("targets_required_only_for_targets_scope")
        if self.profile is not None and self.checks is not None:
            raise ValueError("profile_and_checks_are_exclusive")
        if self.checks is not None and len(set(self.checks)) != len(self.checks):
            raise ValueError("duplicate_check_selection")
        if self.args is not None and len({key for key, _ in self.args}) != len(self.args):
            raise ValueError("duplicate_argument_recipient")
        return self


class SelectionCheckRequest(BaseModel):
    """Complete native selection input; configured scope deliberately sends []."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    operation: CapabilityId
    targets: tuple[AbsolutePath, ...]
    args: tuple[StrictStr, ...]


class CheckSelectionFailureReason(StrEnum):
    NO_CONFIGURED_CHECKS = "no_configured_checks"
    DEFAULT_PROFILE_MISSING = "default_profile_missing"
    UNKNOWN_PROFILE = "unknown_profile"
    UNKNOWN_CHECK = "unknown_check"
    UNSELECTED_ARGS = "unselected_args"
    SELECTION_UNSUPPORTED = "selection_unsupported"
    INVALID_TARGETS = "invalid_targets"


class CheckSelectionError(ValueError):
    """Typed selection failure facts, without presenter wording or native execution."""

    def __init__(
        self, reason: CheckSelectionFailureReason, selection_id: str | None = None
    ) -> None:
        super().__init__(reason.value)
        self.reason = reason
        self.selection_id = selection_id


class CheckScopeError(CheckSelectionError):
    """Typed scope failure facts while retaining the selection error contract."""

    def __init__(
        self,
        target: str,
        scope_reason: Literal["missing", "outside_workspace", "unresolvable"],
        message: str,
    ) -> None:
        super().__init__(CheckSelectionFailureReason.INVALID_TARGETS, target)
        self.target = target
        self.scope_reason = scope_reason
        self.message = message


@dataclass(frozen=True)
class ResolvedCheckScope:
    scope: CheckScope
    targets: tuple[Path, ...]
    removed_targets: tuple[str, ...]
    empty_selection: bool


@dataclass(frozen=True)
class SelectedCheckCall:
    check_id: str
    binding: AdapterBinding[CheckCapability]
    request: SelectionCheckRequest
    timeout_seconds: int
    args_source: ArgsSource


@dataclass(frozen=True)
class NotApplicableCheck:
    """A preselected obligation without any request or native invocation."""

    check_id: str
    binding: AdapterBinding[CheckCapability]
    effective_args: tuple[str, ...]
    args_source: ArgsSource
    timeout_seconds: int


@dataclass(frozen=True)
class CheckSelectionPlan:
    scope: ResolvedCheckScope
    selected_check_ids: tuple[str, ...]
    checks: tuple[SelectedCheckCall | NotApplicableCheck, ...]
    selected_profile: ProfileId | None = None

    @property
    def empty_selection(self) -> bool:
        return self.scope.empty_selection

    @property
    def removed_targets(self) -> tuple[str, ...]:
        return self.scope.removed_targets


class FileScopePaths:
    """Resolve existing or removed paths without scanning directories or native globs."""

    def __init__(self, workspace_root: Path) -> None:
        if not workspace_root.is_absolute():
            raise ValueError("absolute_workspace_required")
        root = workspace_root.resolve(strict=True)
        if not root.is_dir():
            raise ValueError("workspace_directory_required")
        self._workspace_root = root

    @property
    def workspace_root(self) -> Path:
        return self._workspace_root

    def resolve(self, relative: str) -> ResolvedScopePath:
        try:
            _relative_path(relative)
        except ValueError as exc:
            raise CheckScopeError(
                relative,
                "unresolvable",
                "Target is not a valid workspace-relative path.",
            ) from exc
        if PureWindowsPath(relative).drive:
            raise CheckScopeError(
                relative,
                "outside_workspace",
                "Target is outside the workspace.",
            )
        try:
            candidate = (self._workspace_root / relative).resolve()
            if candidate == self._workspace_root:
                raise CheckScopeError(
                    relative,
                    "unresolvable",
                    "Target must identify a non-root workspace path.",
                )
            if not candidate.is_relative_to(self._workspace_root):
                raise CheckScopeError(
                    relative,
                    "outside_workspace",
                    "Target is outside the workspace.",
                )
            exists = candidate.exists()
        except CheckScopeError:
            raise
        except (OSError, RuntimeError) as exc:
            raise CheckScopeError(
                relative,
                "unresolvable",
                "Target could not be resolved.",
            ) from exc
        return ResolvedScopePath(path=candidate, exists=exists)


class ScopeResolver:
    """Resolve caller intent using separately injected filesystem and Git readers."""

    def __init__(
        self, paths: ScopePaths, git: IBranchChangeReader, parents: IBranchParentReader
    ) -> None:
        self._paths = paths
        self._git = git
        self._parents = parents

    def resolve(self, request: CheckSelectionRequest) -> ResolvedCheckScope:
        if request.scope == "configured":
            return ResolvedCheckScope(request.scope, (), (), False)
        if request.scope == "workspace":
            return ResolvedCheckScope(request.scope, (self._paths.workspace_root,), (), False)

        if request.scope == "targets":
            paths: list[Path] = []
            for relative in request.targets or ():
                resolved = self._paths.resolve(relative)
                if not resolved.exists:
                    raise CheckScopeError(
                        relative,
                        "missing",
                        "Requested target does not exist.",
                    )
                paths.append(resolved.path)
            return ResolvedCheckScope(request.scope, tuple(sorted(set(paths), key=str)), (), False)

        branch = self._git.get_current_branch()
        parent = self._parents.get_parent_branch(branch)
        if not parent:
            raise BranchBasisUnavailableError("parent_unavailable", "branch_parent_missing")
        changes = self._git.get_branch_changes(parent)
        current: list[Path] = []
        removed = set(changes.removed_paths)
        for relative in changes.current_paths:
            resolved = self._paths.resolve(relative)
            if resolved.exists:
                current.append(resolved.path)
                removed.discard(relative)
            elif relative not in removed:
                raise CheckScopeError(
                    relative,
                    "missing",
                    "Requested branch path does not exist.",
                )
        targets = tuple(sorted(set(current), key=str))
        removed_targets = tuple(
            sorted(PureWindowsPath(_relative_path(relative)).as_posix() for relative in removed)
        )
        return ResolvedCheckScope(request.scope, targets, removed_targets, not targets)


class CheckSelector:
    """Resolve complete configured obligations before creating any runnable calls."""

    def __init__(
        self,
        config: ChecksConfig,
        catalog: CheckCatalogReader,
        scopes: ScopeResolver,
        configured_targets: ConfiguredTargetFilter,
    ) -> None:
        self._config = config
        self._catalog = catalog
        self._scopes = scopes
        self._configured_targets = configured_targets

    def select(self, request: CheckSelectionRequest) -> CheckSelectionPlan:
        configured = dict(self._config.checks)
        if not configured:
            raise CheckSelectionError(CheckSelectionFailureReason.NO_CONFIGURED_CHECKS)
        profiles = dict(self._config.profiles)
        selected_profile: ProfileId | None = None
        if request.checks is not None:
            selected = request.checks
        else:
            profile = request.profile or self._config.run_checks.default_profile
            if profile is None:
                raise CheckSelectionError(CheckSelectionFailureReason.DEFAULT_PROFILE_MISSING)
            if profile not in profiles:
                raise CheckSelectionError(CheckSelectionFailureReason.UNKNOWN_PROFILE, profile)
            selected_profile = profile
            selected = profiles[profile].checks

        bindings: dict[str, AdapterBinding[CheckCapability]] = {}
        for check_id in selected:
            if check_id not in configured:
                raise CheckSelectionError(CheckSelectionFailureReason.UNKNOWN_CHECK, check_id)
            declaration = configured[check_id]
            binding = self._catalog.get_check(declaration.adapter_id, declaration.capability)
            if "selection" not in binding.capability.inputs:
                raise CheckSelectionError(
                    CheckSelectionFailureReason.SELECTION_UNSUPPORTED, check_id
                )
            bindings[check_id] = binding
        overrides = dict(request.args or ())
        for recipient in overrides:
            if recipient not in selected:
                raise CheckSelectionError(CheckSelectionFailureReason.UNSELECTED_ARGS, recipient)

        scope = self._scopes.resolve(request)
        planned: list[SelectedCheckCall | NotApplicableCheck] = []
        policies = dict(self._config.configured_targets)
        if not scope.empty_selection:
            for check_id in selected:
                declaration = configured[check_id]
                binding = bindings[check_id]
                args = overrides.get(check_id, declaration.default_args)
                args_source: ArgsSource = "caller" if check_id in overrides else "configured"
                timeout = (
                    request.timeout_seconds
                    if request.timeout_seconds is not None
                    else declaration.timeout_seconds
                )
                targets = scope.targets
                if scope.scope == "branch":
                    reference = binding.capability.configured_targets
                    assert reference is not None
                    targets = self._configured_targets.select(targets, policy=policies[reference])
                    if not targets:
                        planned.append(
                            NotApplicableCheck(check_id, binding, args, args_source, timeout)
                        )
                        continue
                planned.append(
                    SelectedCheckCall(
                        check_id=check_id,
                        binding=binding,
                        request=SelectionCheckRequest(
                            operation=binding.capability_id,
                            targets=tuple(str(path) for path in targets),
                            args=args,
                        ),
                        timeout_seconds=timeout,
                        args_source=args_source,
                    )
                )
        return CheckSelectionPlan(
            scope=scope,
            selected_check_ids=selected,
            checks=tuple(planned),
            selected_profile=selected_profile,
        )
