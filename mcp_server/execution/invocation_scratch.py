# pgmcp:v1 id=python_class pv=1.0.0 pf=hy3SAizDAZ8yUHLN sf=9PfER5JkyAoFQLRi
"""Filesystem commands for PGMCP-owned invocation directories."""

from __future__ import annotations

import shutil
from pathlib import Path
from uuid import UUID

from mcp_server.core.interfaces.execution import InvocationDirectory


class FileInvocationScratch:
    """Describe locations and exclusively create invocation directories."""

    def __init__(self, validation_root: Path) -> None:
        if not validation_root.is_absolute():
            raise ValueError("validation_root_must_be_absolute")
        self._validation_root = validation_root

    def describe(self, invocation_id: UUID) -> InvocationDirectory:
        """Calculate a stable location without touching the filesystem."""
        return InvocationDirectory(self._validation_root / f"invocation-{invocation_id}")

    def create(self, directory: InvocationDirectory) -> None:
        """Create exclusively; failure never adopts an existing allocation."""
        self._validate(directory)
        self._validation_root.mkdir(parents=True, exist_ok=True)
        directory.directory.mkdir(exist_ok=False)

    def remove(self, directory: InvocationDirectory) -> None:
        """Remove a successfully owned child after confirmed process completion."""
        self._validate(directory)
        if directory.directory.is_symlink():
            raise ValueError("invocation_directory_is_symlink")
        shutil.rmtree(directory.directory)

    def _validate(self, directory: InvocationDirectory) -> None:
        if (
            directory.directory.parent != self._validation_root
            or directory.directory == self._validation_root
            or not directory.directory.name.startswith("invocation-")
        ):
            raise ValueError("invocation_directory_not_owned")
