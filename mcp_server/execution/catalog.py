# mcp_server/execution/catalog.py
# template=service version=5d5b489a created=2026-09-13T19:17Z updated=
"""Prepare one immutable adapter catalog through injected readers and launch resolution."""

from __future__ import annotations

import base64
import hashlib
import json
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel

from mcp_server.config.schemas.adapter_manifest import (
    AdapterEntrypoint,
    AdapterManifest,
    AdapterRole,
    AdapterTrustConfig,
    CheckCapability,
    FixCapability,
    PackageFileReference,
    TestCapability,
)
from mcp_server.core.exceptions import ConfigError
from mcp_server.core.interfaces.execution import (
    AdapterBinding,
    AdapterLaunch,
    AdapterPackageIdentity,
    AdapterPackageReader,
)


class FileAdapterPackageReader:
    """Shallow filesystem access and resolved package ownership checks."""

    def discover(self, root: Path) -> tuple[Path, ...]:
        if not root.exists():
            return ()
        if not root.is_dir():
            raise ConfigError("adapter_root_not_directory", str(root))
        packages = []
        for candidate in sorted(root.iterdir()):
            if candidate.is_dir() and (candidate / "manifest.yaml").exists():
                resolved = candidate.resolve()
                if not resolved.is_relative_to(root.resolve()):
                    raise ConfigError("adapter_package_escape", str(candidate))
                packages.append(resolved)
        return tuple(packages)

    def resolve_file(self, root: Path, relative: str) -> Path:
        resolved_root = root.resolve()
        target = (resolved_root / relative).resolve()
        if not target.is_relative_to(resolved_root) or not target.is_file():
            raise ConfigError("adapter_package_file_invalid", str(target))
        return target

    def read_bytes(self, path: Path) -> bytes:
        return path.read_bytes()


CapabilityT = TypeVar("CapabilityT", bound=BaseModel)


def _select(
    bindings: tuple[AdapterBinding[CapabilityT], ...], adapter_id: str, capability: str
) -> AdapterBinding[CapabilityT]:
    for binding in bindings:
        if binding.identity.adapter_id == adapter_id and binding.capability_id == capability:
            return binding
    raise ConfigError(f"adapter_capability_unavailable: {adapter_id}/{capability}")


@dataclass(frozen=True)
class AdapterCatalog:
    """One startup snapshot, exposing separate read-only role selections."""

    checks: tuple[AdapterBinding[CheckCapability], ...]
    tests: tuple[AdapterBinding[TestCapability], ...]
    fixes: tuple[AdapterBinding[FixCapability], ...]

    def get_check(self, adapter_id: str, capability: str) -> AdapterBinding[CheckCapability]:
        return _select(self.checks, adapter_id, capability)

    def get_test(self, adapter_id: str, capability: str) -> AdapterBinding[TestCapability]:
        return _select(self.tests, adapter_id, capability)

    def get_fix(self, adapter_id: str, capability: str) -> AdapterBinding[FixCapability]:
        return _select(self.fixes, adapter_id, capability)


class AdapterCatalogLoader:
    """Admit declared package snapshots; never launch or survey their dependencies."""

    def __init__(
        self,
        official_root: Path,
        workspace_root: Path,
        trust: AdapterTrustConfig,
        *,
        read_manifest: Callable[[Path], AdapterManifest],
        files: AdapterPackageReader,
        resolve_program: Callable[[str], Path | None],
        windows: bool,
    ) -> None:
        if not official_root.is_absolute() or not workspace_root.is_absolute():
            raise ConfigError("absolute_adapter_roots_required")
        self._official_root = official_root
        self._workspace_root = workspace_root
        self._trust = trust
        self._read_manifest = read_manifest
        self._files = files
        self._resolve_program = resolve_program
        self._windows = windows

    def load(self) -> AdapterCatalog:
        """Reject duplicate declarations and invalid cross-package references atomically."""
        identities: set[str] = set()
        checks: list[AdapterBinding[CheckCapability]] = []
        tests: list[AdapterBinding[TestCapability]] = []
        fixes: list[AdapterBinding[FixCapability]] = []
        program_selections: dict[str, Path | None] = {}
        for source, official in ((self._official_root, True), (self._workspace_root, False)):
            for directory in self._files.discover(source):
                manifest_path = self._resolve_file(directory, "manifest.yaml")
                manifest = self._read_manifest(manifest_path)
                if manifest.adapter_id in identities:
                    raise ConfigError(f"duplicate_adapter_id: {manifest.adapter_id}")
                identities.add(manifest.adapter_id)
                if not official and manifest.adapter_id not in self._trust.trusted_adapter_ids:
                    continue
                inventory = self._inventory(directory, manifest, manifest_path)
                identity = _identity(manifest, inventory)
                checks.extend(
                    self._bindings(
                        directory, manifest.roles.check, identity, inventory, program_selections
                    )
                )
                tests.extend(
                    self._bindings(
                        directory, manifest.roles.test, identity, inventory, program_selections
                    )
                )
                fixes.extend(
                    self._bindings(
                        directory, manifest.roles.fix, identity, inventory, program_selections
                    )
                )
        catalog = AdapterCatalog(tuple(checks), tuple(tests), tuple(fixes))
        for binding in catalog.fixes:
            for address in binding.capability.addresses:
                catalog.get_check(address.adapter_id, address.capability)
        return catalog

    def _resolve_file(self, root: Path, relative: str) -> Path:
        path = self._files.resolve_file(root, relative)
        if not path.is_absolute() or not path.is_relative_to(root):
            raise ConfigError("adapter_package_file_escape", str(path))
        return path

    def _inventory(
        self, directory: Path, manifest: AdapterManifest, manifest_path: Path
    ) -> tuple[tuple[str, Path, bytes], ...]:
        selected = {manifest_path}
        result = []
        for name in manifest.files:
            path = self._resolve_file(directory, name)
            if path in selected:
                raise ConfigError("duplicate_adapter_file", name)
            selected.add(path)
            result.append(
                (path.relative_to(directory).as_posix(), path, self._files.read_bytes(path))
            )
        return tuple(sorted(result))

    def _bindings(
        self,
        directory: Path,
        role: AdapterRole[CapabilityT] | None,
        identity: AdapterPackageIdentity,
        inventory: tuple[tuple[str, Path, bytes], ...],
        programs: dict[str, Path | None],
    ) -> tuple[AdapterBinding[CapabilityT], ...]:
        if role is None:
            return ()
        launch = self._launch(directory, role.entrypoint, inventory, programs)
        return tuple(
            AdapterBinding(identity, name, role.contract_version, launch, capability)
            for name, capability in role.capabilities
        )

    def _launch(
        self,
        directory: Path,
        entrypoint: AdapterEntrypoint,
        inventory: tuple[tuple[str, Path, bytes], ...],
        programs: dict[str, Path | None],
    ) -> AdapterLaunch:
        declared = {path for _, path, _ in inventory}

        def package_file(reference: PackageFileReference) -> Path:
            path = self._resolve_file(directory, reference.package_file)
            if path not in declared:
                raise ConfigError(
                    "adapter_entrypoint_file_not_in_inventory", reference.package_file
                )
            return path

        executable: Path | None
        if isinstance(entrypoint.executable, PackageFileReference):
            executable = package_file(entrypoint.executable)
        else:
            name = entrypoint.executable
            if name not in programs:
                programs[name] = self._resolve_program(name)
            executable = programs[name]
        if executable is not None:
            if not executable.is_absolute():
                raise ConfigError("absolute_program_selection_required")
            if self._windows and executable.suffix.lower() in {".bat", ".cmd"}:
                raise ConfigError("direct_windows_batch_forbidden", str(executable))
        args = tuple(
            str(package_file(argument)) if isinstance(argument, PackageFileReference) else argument
            for argument in entrypoint.args
        )
        return AdapterLaunch(executable, args)


def _identity(
    manifest: AdapterManifest, inventory: tuple[tuple[str, Path, bytes], ...]
) -> AdapterPackageIdentity:
    """Hash 8-byte big-endian length-prefixed records, excluding physical locations."""
    canonical = json.dumps(
        manifest.model_dump(mode="json", exclude_unset=True),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    records = [b"pgmcp:adapter-package:v1", canonical]
    for name, _, content in inventory:
        records.extend((name.encode("utf-8"), content))
    digest = hashlib.sha256()
    for record in records:
        digest.update(len(record).to_bytes(8, "big"))
        digest.update(record)
    fingerprint = base64.urlsafe_b64encode(digest.digest()[:12]).decode("ascii").rstrip("=")
    return AdapterPackageIdentity(manifest.adapter_id, manifest.version, fingerprint)
