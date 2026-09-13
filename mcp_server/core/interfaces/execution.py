# mcp_server/core/interfaces/execution.py
# template=interface version=3fb28c28 created=2026-09-13T19:17Z updated=
"""Immutable launch selections and narrow role catalog readers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Generic, Protocol, TypeVar

from mcp_server.config.schemas.adapter_manifest import (
    CheckCapability,
    FixCapability,
    TestCapability,
)


@dataclass(frozen=True)
class AdapterPackageIdentity:
    """Identity of the admitted bytes, independent of physical package location."""

    adapter_id: str
    version: str
    fingerprint: str


@dataclass(frozen=True)
class AdapterLaunch:
    """Startup-selected executable; None retains a missing external dependency."""

    executable: Path | None
    args: tuple[str, ...]


CapabilityT_co = TypeVar("CapabilityT_co", covariant=True)


@dataclass(frozen=True)
class AdapterBinding(Generic[CapabilityT_co]):
    """One qualified capability from an admitted package snapshot."""

    identity: AdapterPackageIdentity
    capability_id: str
    contract_version: int
    launch: AdapterLaunch
    capability: CapabilityT_co


class AdapterPackageReader(Protocol):
    """Read-only package discovery, file resolution and exact byte access."""

    def discover(self, root: Path) -> tuple[Path, ...]: ...
    def resolve_file(self, root: Path, relative: str) -> Path: ...
    def read_bytes(self, path: Path) -> bytes: ...


class CheckCatalogReader(Protocol):
    @property
    def checks(self) -> tuple[AdapterBinding[CheckCapability], ...]: ...
    def get_check(self, adapter_id: str, capability: str) -> AdapterBinding[CheckCapability]: ...


class TestCatalogReader(Protocol):
    @property
    def tests(self) -> tuple[AdapterBinding[TestCapability], ...]: ...
    def get_test(self, adapter_id: str, capability: str) -> AdapterBinding[TestCapability]: ...


class FixCatalogReader(Protocol):
    @property
    def fixes(self) -> tuple[AdapterBinding[FixCapability], ...]: ...
    def get_fix(self, adapter_id: str, capability: str) -> AdapterBinding[FixCapability]: ...


class AdapterProcess(Protocol):
    """One process with separately drained byte streams and explicit stdin EOF."""

    async def write_input(self, payload: bytes) -> None: ...
    async def read_stdout(self, maximum: int) -> bytes: ...
    async def read_stderr(self, maximum: int) -> bytes: ...
    @property
    def returncode(self) -> int | None:
        """Observed adapter exit only; not a certificate for associated work."""
        ...

    async def wait(self) -> int:
        """Wait for the adapter exit, independently of descendant completion."""
        ...

    async def wait_finished(self) -> None:
        """Confirm completion of the adapter and its associated managed work."""
        ...

    def kill(self) -> None:
        """Request termination of all managed work; confirmation is separate."""
        ...

    def close(self) -> None:
        """Release owned resources; closing is not termination confirmation."""
        ...


class AdapterProcessBackend(Protocol):
    """Launch one startup-selected command in an explicit workspace."""

    async def start(self, launch: AdapterLaunch, workspace_root: Path) -> AdapterProcess: ...


class AdapterProcessSetupError(RuntimeError):
    """A process exists, but setup failed; the caller retains cleanup ownership."""

    def __init__(self, process: AdapterProcess, cause: OSError) -> None:
        super().__init__(str(cause))
        self.process = process


@dataclass(frozen=True)
class OwnedScratchFile:
    """One validation file and the directory owned by its invocation."""

    directory: Path
    input_path: Path


class ContentScratchFiles(Protocol):
    """Narrow provider for per-invocation validation scratch files."""

    def create(self, basename: str, content: bytes) -> OwnedScratchFile: ...

    def remove(self, allocation: OwnedScratchFile) -> None: ...
