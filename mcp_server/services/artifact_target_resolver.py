"""Resolve artifact location policy without rendering, enforcement, or mutation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Literal

from mcp_server.config.schemas.artifact_locations import ArtifactLocationsConfig
from mcp_server.core.interfaces.execution import ScopePaths
from mcp_server.utils.path_resolver import ArtifactTargetError, normalize_workspace_relative_path


@dataclass(frozen=True)
class ArtifactTarget:
    """An exact logical output name and its contained native creation path."""

    path: Path
    output_path: str


class ArtifactTargetResolver:
    """Choose a target using package storage intent and injected location observations."""

    def __init__(
        self,
        *,
        paths: ScopePaths,
        temporary_artifacts_root: Path,
        locations: ArtifactLocationsConfig,
    ) -> None:
        if not temporary_artifacts_root.is_absolute():
            raise ValueError("absolute_temporary_artifacts_root_required")
        self._temporary_root = normalize_workspace_relative_path(
            temporary_artifacts_root.relative_to(paths.workspace_root).as_posix()
        )
        self._paths = paths
        self._locations = dict(locations.artifacts)

    def resolve(
        self,
        *,
        template_id: str,
        persistence: Literal["workspace", "temporary"],
        file_name: str,
        target_path: str | None = None,
        force_target: bool = False,
    ) -> ArtifactTarget:
        """Return a new-file target; force only relaxes configured directory admission."""
        if (
            not file_name
            or file_name in (".", "..")
            or any(char in file_name for char in ("/", "\\", "\x00"))
            or PureWindowsPath(file_name).drive
        ):
            raise ValueError("basename_required")
        if force_target and target_path is None:
            raise ValueError("force_target_requires_target_path")

        location = self._locations.get(template_id)
        if target_path is None:
            directory = (
                location.default_root
                if persistence == "workspace" and location is not None
                else self._temporary_root
            )
        else:
            directory = normalize_workspace_relative_path(target_path)
            allowed_roots = (
                (location.default_root, *location.additional_roots) if location is not None else ()
            )
            allowed = any(PurePosixPath(directory).is_relative_to(root) for root in allowed_roots)
            if not allowed and not force_target:
                raise ArtifactTargetError("force_required", directory, "force_target_required")

        output_path = (PurePosixPath(directory) / file_name).as_posix()
        observed = self._paths.resolve(output_path)
        if observed.exists:
            raise FileExistsError(output_path)
        return ArtifactTarget(path=observed.path, output_path=output_path)
