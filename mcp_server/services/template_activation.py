"""Recoverable complete-suite activation under one cross-process lock."""

from __future__ import annotations

import hashlib
import os
import shutil
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, BinaryIO, Literal

from pydantic import BaseModel, ConfigDict, field_serializer, model_validator

from mcp_server.config.schemas.installation import InstallationState, TemplateCheckpoint
from mcp_server.core.exceptions import MCPError
from mcp_server.services.artifact_identity import GenerationSource
from mcp_server.services.installation_state import JsonWriter
from mcp_server.services.template_components import ComponentKey, ComponentState
from mcp_server.services.template_proposal import SuiteSnapshot
from mcp_server.services.template_renewal import analyze_components

if os.name == "nt":
    import msvcrt

    _fcntl_module: Any = None
else:
    import fcntl

    _fcntl_module = fcntl


def _posix_lock(fd: int, *operation_names: str) -> None:
    module = _fcntl_module
    if module is None:
        raise RuntimeError("posix_lock_unavailable")
    operation = 0
    for name in operation_names:
        operation |= getattr(module, name)
    flock_name = "flock"
    getattr(module, flock_name)(fd, operation)


@dataclass(frozen=True)
class ActivationPaths:
    """Fixed filesystem ownership below an explicitly resolved server root."""

    root: Path

    def __post_init__(self) -> None:
        if not self.root.is_absolute():
            raise ValueError("absolute_activation_root_required")
        object.__setattr__(self, "root", self.root.resolve())

    @property
    def actual(self) -> Path:
        return self.root / "template_suite"

    @property
    def candidate(self) -> Path:
        return self.root / "upgrade"

    @property
    def next(self) -> Path:
        return self.root / "template_suite.next"

    @property
    def previous(self) -> Path:
        return self.root / "template_suite.previous"

    @property
    def installation(self) -> Path:
        return self.root / "installation.json"

    @property
    def record(self) -> Path:
        return self.root / "template_upgrade.json"

    @property
    def lock(self) -> Path:
        return self.root / "template_upgrade.lock"

    @property
    def owned(self) -> tuple[Path, ...]:
        return (
            self.actual,
            self.candidate,
            self.next,
            self.previous,
            self.installation,
            self.record,
            self.lock,
        )


class SuiteIdentity(BaseModel):
    """Presence and complete operational identity, independent of adopted state."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    present: bool
    components: TemplateCheckpoint | None

    @model_validator(mode="after")
    def validate_presence(self) -> SuiteIdentity:
        if self.present != (self.components is not None):
            raise ValueError("activation_suite_presence_mismatch")
        return self


class LegacyBackupFile(BaseModel):
    """Exact legacy file identity needed to verify an interrupted migration backup."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    path: str
    sha256: str

    @model_validator(mode="after")
    def validate_file_fact(self) -> LegacyBackupFile:
        relative = Path(self.path)
        if relative.is_absolute() or ".." in relative.parts or len(self.sha256) != 64:
            raise ValueError("activation_legacy_backup_fact_invalid")
        try:
            int(self.sha256, 16)
        except ValueError as error:
            raise ValueError("activation_legacy_backup_fact_invalid") from error
        return self


class ActivationRecord(BaseModel):
    """Immutable facts published before the first authoritative directory move."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    prior_suite: SuiteIdentity
    target_suite: SuiteIdentity
    prior_installation: InstallationState | None
    target_installation: InstallationState
    retain_candidate: bool
    backup_path: Path | None
    legacy_backup_files: tuple[LegacyBackupFile, ...] = ()
    legacy_backup_directories: tuple[str, ...] = ()
    force: bool = False
    fresh: bool = False

    @model_validator(mode="after")
    def validate_target(self) -> ActivationRecord:
        if not self.target_suite.present or self.target_installation.template_checkpoint is None:
            raise ValueError("activation_target_incomplete")
        directories = self.legacy_backup_directories
        if (
            len(set(directories)) != len(directories)
            or tuple(sorted(directories)) != directories
            or any(
                Path(directory).is_absolute() or ".." in Path(directory).parts or "\\" in directory
                for directory in directories
            )
        ):
            raise ValueError("activation_legacy_backup_directories_invalid")
        return self

    @field_serializer("prior_installation", "target_installation")
    def serialize_installation(self, value: InstallationState | None) -> dict[str, object] | None:
        return None if value is None else value.model_dump(mode="json", exclude_none=True)


@dataclass(frozen=True)
class ActivationResult:
    """Observed command outcome; read separately from filesystem mutations."""

    outcome: Literal["activated", "rolled_back", "completed"]
    candidate_retained: bool
    backup_path: Path | None
    actual_changed: bool = False
    checkpoint_effect: Literal["unchanged", "created", "advanced"] = "unchanged"
    force_applied: bool = False
    fresh_applied: bool = False


def _completed_result(
    record: ActivationRecord, outcome: Literal["activated", "completed"]
) -> ActivationResult:
    """Project durable prior/target facts without inspecting cleaned-up paths."""
    prior = record.prior_installation
    previous_checkpoint = None if prior is None else prior.template_checkpoint
    target_checkpoint = record.target_installation.template_checkpoint
    effect: Literal["unchanged", "created", "advanced"] = "unchanged"
    if previous_checkpoint != target_checkpoint:
        effect = "created" if previous_checkpoint is None else "advanced"
    return ActivationResult(
        outcome,
        record.retain_candidate,
        record.backup_path,
        actual_changed=record.prior_suite != record.target_suite,
        checkpoint_effect=effect,
        force_applied=record.force,
        fresh_applied=record.fresh,
    )


def _require_owned_endpoint(path: Path) -> None:
    if path.is_symlink() or _is_junction(path) or path.resolve() != path:
        raise MCPError("template_activation_endpoint_alias", code="ERR_CONFIG")


def _is_junction(path: Path) -> bool:
    checker = getattr(path, "is_junction", None)
    return bool(checker and checker())


def _path_entry_present(path: Path) -> bool:
    return path.exists() or path.is_symlink() or _is_junction(path)


class UpgradeLock:
    """Own one OS lock until release or process termination; never remove its inode."""

    def __init__(self, path: Path) -> None:
        if not path.is_absolute():
            raise ValueError("absolute_upgrade_lock_required")
        self.path = path.parent.resolve() / path.name
        self._file: BinaryIO | None = None

    def acquire(self) -> None:
        if self._file is not None:
            raise MCPError("template_upgrade_locked", code="ERR_CONFIG")
        _require_owned_endpoint(self.path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        stream = self.path.open("a+b")
        try:
            if os.fstat(stream.fileno()).st_size == 0:
                stream.write(b"\0")
                stream.flush()
            stream.seek(0)
            if os.name == "nt":
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                _posix_lock(stream.fileno(), "LOCK_EX", "LOCK_NB")
        except OSError as error:
            stream.close()
            raise MCPError("template_upgrade_locked", code="ERR_CONFIG") from error
        self._file = stream

    def release(self) -> None:
        stream, self._file = self._file, None
        if stream is None:
            return
        try:
            stream.seek(0)
            if os.name == "nt":
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                _posix_lock(stream.fileno(), "LOCK_UN")
        finally:
            stream.close()

    @contextmanager
    def hold(self) -> Iterator[None]:
        self.acquire()
        try:
            yield
        finally:
            self.release()


class ActivationFiles:
    """Read and explicitly mutate the bounded activation filesystem."""

    def __init__(
        self,
        server_root: Path,
        *,
        json_writer: JsonWriter,
        move: Callable[[Path, Path], None],
        read_installation: Callable[[], InstallationState | None],
        legacy_root: Path | None = None,
        legacy_version_path: Path | None = None,
    ) -> None:
        self.paths = ActivationPaths(server_root)
        self._legacy_root = legacy_root
        self._legacy_version_path = legacy_version_path
        if any(
            path is not None and not path.is_relative_to(self.paths.root)
            for path in (legacy_root, legacy_version_path)
        ):
            raise ValueError("activation_legacy_source_outside_root")
        self._json_writer = json_writer
        self._move = move
        self._read_installation = read_installation

    def validate_endpoints(self) -> None:
        for path in self.paths.owned:
            _require_owned_endpoint(path)

    def installation(self) -> InstallationState | None:
        return self._read_installation()

    def record(self) -> ActivationRecord | None:
        if not self.paths.record.exists():
            return None
        try:
            return ActivationRecord.model_validate_json(
                self.paths.record.read_text(encoding="utf-8")
            )
        except (OSError, ValueError) as error:
            raise MCPError("template_recovery_record_invalid", code="ERR_CONFIG") from error

    def publish_record(self, record: ActivationRecord) -> None:
        self._json_writer(self.paths.record, record.model_dump(mode="json"))

    def publish_installation(self, state: InstallationState | None) -> None:
        if state is None:
            self.paths.installation.unlink(missing_ok=True)
        else:
            self._json_writer(
                self.paths.installation, state.model_dump(mode="json", exclude_none=True)
            )

    def move(self, source: Path, destination: Path) -> None:
        _require_owned_endpoint(source)
        _require_owned_endpoint(destination)
        self._move(source, destination)

    def discard(self, path: Path) -> None:
        _require_owned_endpoint(path)
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink(missing_ok=True)

    def write_sources(self, target: Path, sources: tuple[GenerationSource, ...]) -> None:
        _require_owned_endpoint(target)
        target.mkdir(parents=True, exist_ok=False)
        try:
            for source in sources:
                destination = target / source.path
                if not destination.resolve().is_relative_to(target):
                    raise MCPError("template_activation_source_escape", code="ERR_CONFIG")
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(source.content)
        except (OSError, ValueError, MCPError):
            self.discard(target)
            raise

    def _legacy_sources(self) -> tuple[tuple[str, bytes], ...]:
        sources: list[tuple[str, bytes]] = []
        root = self._legacy_root
        if root is not None and _path_entry_present(root):
            if root.is_symlink() or _is_junction(root) or not root.is_dir():
                raise MCPError("template_legacy_backup_source_invalid", code="ERR_CONFIG")
            resolved_root = root.resolve()
            for source in sorted(root.rglob("*")):
                if (
                    source.is_symlink()
                    or _is_junction(source)
                    or not source.resolve().is_relative_to(resolved_root)
                ):
                    raise MCPError("template_legacy_backup_source_invalid", code="ERR_CONFIG")
                if source.is_dir():
                    continue
                if not source.is_file():
                    raise MCPError("template_legacy_backup_source_invalid", code="ERR_CONFIG")
                relative = source.relative_to(root).as_posix()
                sources.append((f"templates/{relative}", source.read_bytes()))
        version_path = self._legacy_version_path
        if version_path is not None and _path_entry_present(version_path):
            if (
                version_path.is_symlink()
                or _is_junction(version_path)
                or not version_path.is_file()
                or not version_path.resolve().is_relative_to(self.paths.root)
            ):
                raise MCPError("template_legacy_backup_source_invalid", code="ERR_CONFIG")
            sources.append((".version", version_path.read_bytes()))
        return tuple(sorted(sources))

    def _legacy_directories(self) -> tuple[str, ...]:
        root = self._legacy_root
        if root is None or not _path_entry_present(root):
            return ()
        if root.is_symlink() or _is_junction(root) or not root.is_dir():
            raise MCPError("template_legacy_backup_source_invalid", code="ERR_CONFIG")
        resolved_root = root.resolve()
        directories = ["templates"]
        for source in sorted(root.rglob("*")):
            if (
                source.is_symlink()
                or _is_junction(source)
                or not source.resolve().is_relative_to(resolved_root)
            ):
                raise MCPError("template_legacy_backup_source_invalid", code="ERR_CONFIG")
            if source.is_dir():
                directories.append(f"templates/{source.relative_to(root).as_posix()}")
        return tuple(sorted(directories))

    @staticmethod
    def _legacy_backup_facts(
        sources: tuple[tuple[str, bytes], ...],
    ) -> tuple[LegacyBackupFile, ...]:
        return tuple(
            LegacyBackupFile(path=relative, sha256=hashlib.sha256(content).hexdigest())
            for relative, content in sources
        )

    def legacy_backup_matches(
        self,
        path: Path,
        expected_files: tuple[LegacyBackupFile, ...],
        expected_directories: tuple[str, ...],
    ) -> bool:
        legacy = path / "legacy"
        if not expected_files and not expected_directories:
            return not _path_entry_present(legacy)
        if legacy.is_symlink() or _is_junction(legacy) or not legacy.is_dir():
            return False
        resolved_legacy = legacy.resolve()
        actual_files: list[LegacyBackupFile] = []
        actual_directories: list[str] = []
        for source in sorted(legacy.rglob("*")):
            if (
                source.is_symlink()
                or _is_junction(source)
                or not source.resolve().is_relative_to(resolved_legacy)
            ):
                return False
            relative = source.relative_to(legacy).as_posix()
            if source.is_dir():
                actual_directories.append(relative)
                continue
            if not source.is_file():
                return False
            actual_files.append(
                LegacyBackupFile(
                    path=relative,
                    sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                )
            )
        return (
            tuple(actual_files) == expected_files
            and tuple(actual_directories) == expected_directories
        )

    def create_backup(
        self,
        path: Path,
        prior: SuiteSnapshot | None,
        installation: InstallationState | None,
    ) -> tuple[tuple[LegacyBackupFile, ...], tuple[str, ...]]:
        _require_owned_endpoint(path)
        sources = self._legacy_sources() if prior is None else ()
        directories = self._legacy_directories() if prior is None else ()
        path.mkdir(parents=False, exist_ok=False)
        try:
            if prior is not None:
                self.write_sources(path / "template_suite", prior.sources)
            if installation is not None:
                self._json_writer(
                    path / "installation.json",
                    installation.model_dump(mode="json", exclude_none=True),
                )
            legacy_root = path / "legacy"
            for relative in directories:
                destination = legacy_root / relative
                if not destination.resolve().is_relative_to(legacy_root):
                    raise MCPError("template_legacy_backup_path_invalid", code="ERR_CONFIG")
                destination.mkdir(parents=True, exist_ok=True)
            for relative, content in sources:
                destination = legacy_root / relative
                if not destination.resolve().is_relative_to(legacy_root):
                    raise MCPError("template_legacy_backup_path_invalid", code="ERR_CONFIG")
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(content)
            facts = self._legacy_backup_facts(sources)
            if (
                not self.legacy_backup_matches(path, facts, directories)
                or self._legacy_sources() != sources
                or self._legacy_directories() != directories
            ):
                raise MCPError("template_activation_backup_invalid", code="ERR_CONFIG")
            return facts, directories
        except (OSError, ValueError, MCPError):
            self.discard(path)
            raise

    def backup_installation(self, path: Path) -> InstallationState | None:
        target = path / "installation.json"
        if not target.exists():
            return None
        return InstallationState.model_validate_json(target.read_text(encoding="utf-8"))


def _identity(snapshot: SuiteSnapshot | None) -> SuiteIdentity:
    return SuiteIdentity(
        present=snapshot is not None,
        components=None if snapshot is None else snapshot.evidence.to_checkpoint(),
    )


def _states(checkpoint: TemplateCheckpoint) -> dict[ComponentKey, ComponentState]:
    values = [
        ComponentState(
            kind="shared", component_id="shared", present=True, fingerprint=checkpoint.shared
        ),
        *(
            ComponentState(kind="package", component_id=name, present=True, fingerprint=value)
            for name, value in checkpoint.packages.items()
        ),
    ]
    return {state.key: state for state in values}


def _checkpoint(states: tuple[ComponentState, ...]) -> TemplateCheckpoint:
    present = {state.key: state for state in states if state.present}
    shared = present.get(("shared", "shared"))
    if shared is None or shared.fingerprint is None:
        raise MCPError("template_activation_shared_missing", code="ERR_CONFIG")
    packages: dict[str, str] = {}
    for state in present.values():
        if state.kind == "package" and state.fingerprint is not None:
            packages[state.component_id] = state.fingerprint
    return TemplateCheckpoint(shared=shared.fingerprint, packages=packages)


class TemplateActivationService:
    """Coordinate the recoverable publication of one complete tree and installation pair."""

    def __init__(
        self,
        files: ActivationFiles,
        lock: UpgradeLock,
        *,
        admit: Callable[[Path], SuiteSnapshot],
        clock: Callable[[], datetime],
    ) -> None:
        if files.paths.lock != lock.path:
            raise ValueError("activation_lock_root_mismatch")
        self._files = files
        self._lock = lock
        self._admit = admit
        self._clock = clock
        self._last_result: ActivationResult | None = None

    @property
    def last_result(self) -> ActivationResult | None:
        return self._last_result

    def activate(
        self,
        proposal_root: Path,
        *,
        pgmcp_version: str,
        fresh: bool = False,
        force: bool = False,
    ) -> None:
        self._last_result = None
        if fresh and force:
            raise MCPError("template_activation_mode_invalid", code="ERR_CONFIG")
        self._files.validate_endpoints()
        with self._lock.hold():
            self._files.validate_endpoints()
            if self._files.record() is not None:
                self._recover_locked()
                return
            self._activate_locked(proposal_root, pgmcp_version, fresh=fresh, force=force)

    def recover(self) -> None:
        self._last_result = None
        self._files.validate_endpoints()
        with self._lock.hold():
            self._files.validate_endpoints()
            self._recover_locked()

    def _snapshot(self, path: Path) -> SuiteSnapshot | None:
        if not path.exists():
            return None
        snapshot = self._admit(path)
        if snapshot.root != path.resolve():
            raise MCPError("template_activation_admission_root_mismatch", code="ERR_CONFIG")
        return snapshot

    def _transition(
        self,
        prior: SuiteSnapshot | None,
        candidate: SuiteSnapshot,
        proposal: SuiteSnapshot,
        installation: InstallationState | None,
        *,
        fresh: bool,
        force: bool,
    ) -> tuple[TemplateCheckpoint, bool]:
        candidate_map = candidate.evidence.to_checkpoint()
        proposal_map = proposal.evidence.to_checkpoint()
        if fresh or force:
            if fresh and (
                prior is not None
                or (installation is not None and installation.template_checkpoint is not None)
            ):
                raise MCPError("template_fresh_activation_precondition", code="ERR_CONFIG")
            if proposal_map != candidate_map or proposal.sources != candidate.sources:
                raise MCPError("template_replacement_requires_candidate", code="ERR_CONFIG")
            return candidate_map, False
        if prior is None or installation is None or installation.template_checkpoint is None:
            raise MCPError("template_activation_checkpoint_required", code="ERR_CONFIG")
        analysis = analyze_components(
            _states(installation.template_checkpoint),
            _states(prior.evidence.to_checkpoint()),
            _states(candidate_map),
        )
        if proposal_map != _checkpoint(tuple(decision.selected for decision in analysis.decisions)):
            raise MCPError("template_activation_proposal_changed", code="ERR_CONFIG")
        return (
            _checkpoint(tuple(decision.proposed_checkpoint for decision in analysis.decisions)),
            bool(analysis.conflicts),
        )

    def _activate_locked(
        self, proposal_root: Path, pgmcp_version: str, *, fresh: bool, force: bool
    ) -> None:
        paths = self._files.paths
        if paths.next.exists() or paths.previous.exists():
            raise MCPError("template_activation_unrecorded_material", code="ERR_CONFIG")
        prior = self._snapshot(paths.actual)
        candidate = self._snapshot(paths.candidate)
        proposal = self._snapshot(proposal_root)
        if candidate is None or proposal is None:
            raise MCPError("template_activation_input_missing", code="ERR_CONFIG")
        previous_installation = self._files.installation()
        checkpoint, retain = self._transition(
            prior, candidate, proposal, previous_installation, fresh=fresh, force=force
        )
        target_installation = InstallationState(
            pgmcp_version=pgmcp_version, template_checkpoint=checkpoint
        )
        self._files.write_sources(paths.next, proposal.sources)
        backup: Path | None = None
        backup_created = False
        try:
            prepared = self._snapshot(paths.next)
            if prepared is None or prepared.sources != proposal.sources:
                raise MCPError("template_activation_preparation_changed", code="ERR_CONFIG")
            legacy_backup_files: tuple[LegacyBackupFile, ...] = ()
            legacy_backup_directories: tuple[str, ...] = ()
            if force:
                instant = self._clock()
                if instant.tzinfo is None:
                    raise ValueError("activation_clock_timezone_required")
                stamp = instant.astimezone(UTC).strftime("%Y%m%dT%H%M%S%fZ")
                backup = paths.root.parent / f".pgmcp_template_backup_{stamp}"
                legacy_backup_files, legacy_backup_directories = self._files.create_backup(
                    backup, prior, previous_installation
                )
                backup_created = True
                backup_snapshot = self._snapshot(backup / "template_suite")
                if (
                    _identity(backup_snapshot) != _identity(prior)
                    or (
                        backup_snapshot is not None
                        and prior is not None
                        and backup_snapshot.sources != prior.sources
                    )
                    or self._files.backup_installation(backup) != previous_installation
                    or not self._files.legacy_backup_matches(
                        backup, legacy_backup_files, legacy_backup_directories
                    )
                ):
                    raise MCPError("template_activation_backup_invalid", code="ERR_CONFIG")
            record = ActivationRecord(
                prior_suite=_identity(prior),
                target_suite=_identity(prepared),
                prior_installation=previous_installation,
                target_installation=target_installation,
                retain_candidate=retain,
                backup_path=backup,
                legacy_backup_files=legacy_backup_files,
                legacy_backup_directories=legacy_backup_directories,
                force=force,
                fresh=fresh,
            )
            self._files.publish_record(record)
        except (OSError, ValueError, MCPError):
            if not paths.record.exists():
                self._files.discard(paths.next)
                if backup_created and backup is not None:
                    self._files.discard(backup)
            raise
        if prior is not None:
            self._files.move(paths.actual, paths.previous)
        self._files.move(paths.next, paths.actual)
        self._files.publish_installation(target_installation)
        if (
            _identity(self._snapshot(paths.actual)) != record.target_suite
            or self._files.installation() != target_installation
        ):
            raise MCPError("template_activation_publication_changed", code="ERR_CONFIG")
        self._complete_target(record)
        self._last_result = _completed_result(record, "activated")

    def _recover_locked(self) -> None:
        record = self._files.record()
        if record is None:
            return
        paths = self._files.paths
        try:
            actual = _identity(self._snapshot(paths.actual))
            previous = _identity(self._snapshot(paths.previous))
            next_tree = _identity(self._snapshot(paths.next))
            installation = self._files.installation()
            if any(
                tree.present and tree != record.prior_suite and tree != record.target_suite
                for tree in (actual, previous, next_tree)
            ) or installation not in (record.prior_installation, record.target_installation):
                raise ValueError("unrecognized_activation_facts")
            if record.backup_path is not None:
                backup = record.backup_path
                if backup.parent != paths.root.parent or not backup.name.startswith(
                    ".pgmcp_template_backup_"
                ):
                    raise ValueError("unowned_activation_backup")
                _require_owned_endpoint(backup)
                if (
                    not backup.is_dir()
                    or _identity(self._snapshot(backup / "template_suite")) != record.prior_suite
                    or self._files.backup_installation(backup) != record.prior_installation
                    or not self._files.legacy_backup_matches(
                        backup,
                        record.legacy_backup_files,
                        record.legacy_backup_directories,
                    )
                ):
                    raise ValueError("unrecognized_activation_backup")
        except (MCPError, OSError, ValueError) as error:
            raise MCPError("template_recovery_unknown", code="ERR_CONFIG") from error

        if actual == record.target_suite and installation == record.target_installation:
            if previous.present and previous != record.prior_suite:
                raise MCPError("template_recovery_unknown", code="ERR_CONFIG")
            if next_tree.present and next_tree != record.target_suite:
                raise MCPError("template_recovery_unknown", code="ERR_CONFIG")
            self._complete_target(record)
            self._last_result = _completed_result(record, "completed")
            return

        prior_authoritative = (
            actual == record.prior_suite and installation == record.prior_installation
        )
        missing_prior = (
            not actual.present and record.prior_suite.present and previous == record.prior_suite
        )
        uncommitted_target = (
            actual == record.target_suite
            and installation == record.prior_installation
            and previous == record.prior_suite
        )
        if (
            (prior_authoritative and not previous.present)
            or missing_prior
            or (uncommitted_target and not next_tree.present)
        ):
            if next_tree.present and next_tree != record.target_suite:
                raise MCPError("template_recovery_unknown", code="ERR_CONFIG")
            if uncommitted_target:
                self._files.move(paths.actual, paths.next)
            # Publish prior installation before restoring a missing actual path, so a
            # second interruption still matches the missing-actual recovery row.
            self._files.publish_installation(record.prior_installation)
            if record.prior_suite.present and (missing_prior or uncommitted_target):
                self._files.move(paths.previous, paths.actual)
            self._files.discard(paths.next)
            self._files.discard(paths.record)
            self._last_result = ActivationResult(
                "rolled_back", paths.candidate.exists(), record.backup_path
            )
            return
        raise MCPError("template_recovery_unknown", code="ERR_CONFIG")

    def _complete_target(self, record: ActivationRecord) -> None:
        paths = self._files.paths
        if not record.retain_candidate:
            self._files.discard(paths.candidate)
        self._files.discard(paths.previous)
        self._files.discard(paths.next)
        self._files.discard(paths.record)
