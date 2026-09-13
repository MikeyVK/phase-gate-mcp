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
