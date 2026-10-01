# mcp_server/utils/path_resolver.py
# template=generic version=f35abd82 created=2026-02-27T06:08Z updated=
"""Utility for resolving mixed file/directory inputs to concrete .py file paths.

@layer: MCP Server (Utils)
@dependencies: [pathlib, logging]
@responsibilities:
    - Expand directory inputs to concrete .py files
    - Preserve explicit file inputs
    - Deduplicate resolved paths
    - Surface warnings for missing/unresolvable paths
"""

# Standard library
from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from os.path import lexists
from pathlib import Path, PureWindowsPath
from typing import Literal

from mcp_server.core.interfaces.execution import ResolvedScopePath

logger = logging.getLogger(__name__)


def resolve_input_paths(
    paths: list[str],
    workspace_root: Path,
) -> tuple[list[str], list[str]]:
    """Resolve a list of file/directory paths to concrete .py file paths.

    Args:
        paths: Caller-supplied list of relative file or directory paths.
        workspace_root: Absolute workspace root used to resolve relative paths.

    Returns:
        A tuple of (resolved_files, warnings) where resolved_files is a sorted,
        deduplicated list of relative POSIX .py paths, and warnings is a list of
        human-readable strings for paths that could not be resolved.
    """
    resolved: set[str] = set()
    warnings: list[str] = []

    for raw in paths:
        abs_path = workspace_root / raw
        if abs_path.is_dir():
            for py_file in abs_path.rglob("*.py"):
                resolved.add(py_file.relative_to(workspace_root).as_posix())
        elif abs_path.is_file():
            resolved.add(abs_path.relative_to(workspace_root).as_posix())
        else:
            warnings.append(f"Path not found and will be skipped: {raw!r}")
            logger.warning("resolve_input_paths: path not found: %r", raw)

    return sorted(resolved), warnings


@dataclass(frozen=True)
class ResolvedTemporaryPaths:
    """Lexically derived roots for validation and artifact temporary data."""

    temp_root: Path
    validation_root: Path
    artifacts_root: Path


def resolve_temporary_paths(resolved_server_root: Path) -> ResolvedTemporaryPaths:
    """Derive temporary roots without filesystem access or path resolution."""
    if not resolved_server_root.is_absolute():
        raise ValueError("resolved_server_root_must_be_absolute")
    temp_root = resolved_server_root / "temp"
    return ResolvedTemporaryPaths(
        temp_root=temp_root,
        validation_root=temp_root / "validation",
        artifacts_root=temp_root / "artifacts",
    )


def normalize_workspace_relative_path(value: str) -> str:
    """Normalize logical path components without resolving them against the filesystem."""
    if (
        not value.strip()
        or "\x00" in value
        or value.startswith(("/", "\\"))
        or PureWindowsPath(value).drive
    ):
        raise ValueError("workspace_relative_path_required")
    parts: list[str] = []
    for part in value.replace("\\", "/").split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if not parts:
                raise ValueError("workspace_relative_path_required")
            parts.pop()
        else:
            parts.append(part)
    return "/".join(parts) or "."


class ArtifactTargetError(ValueError):
    """A factual location failure with no inference required from diagnostic text."""

    def __init__(
        self,
        reason: Literal["outside_workspace", "force_required", "not_file", "unresolvable"],
        path: str,
        message: str,
    ) -> None:
        super().__init__(message)
        self.reason = reason
        self.path = path


class FileArtifactTargetPaths:
    """Observe contained creation targets while retaining an existing leaf entry."""

    def __init__(self, workspace_root: Path) -> None:
        if not workspace_root.is_absolute():
            raise ValueError("absolute_workspace_required")
        self._workspace_root = workspace_root.resolve(strict=True)
        if not self._workspace_root.is_dir():
            raise ValueError("workspace_directory_required")

    @property
    def workspace_root(self) -> Path:
        return self._workspace_root

    def resolve(self, relative: str) -> ResolvedScopePath:
        normalized = normalize_workspace_relative_path(relative)
        if os.name == "nt" and any(
            PureWindowsPath(part).is_reserved() or ":" in part or part.endswith((".", " "))
            for part in Path(normalized).parts
        ):
            raise ArtifactTargetError("unresolvable", normalized, "artifact_target_name_reserved")
        candidate = self._workspace_root / normalized
        try:
            parent = candidate.parent.resolve()
        except (OSError, RuntimeError) as exc:
            raise ArtifactTargetError("unresolvable", normalized, str(exc)) from exc
        if not parent.is_relative_to(self._workspace_root):
            raise ArtifactTargetError(
                "outside_workspace", normalized, "artifact_target_outside_workspace"
            )
        target = parent / candidate.name
        return ResolvedScopePath(path=target, exists=lexists(target))
