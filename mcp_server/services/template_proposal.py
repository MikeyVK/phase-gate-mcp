"""Stage complete template candidates and materialize independently admitted proposals."""

from __future__ import annotations

import inspect
import os
import shutil
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from jinja2 import Environment

from mcp_server.config.loader import ConfigLoader
from mcp_server.config.validator import ConfigValidator
from mcp_server.core.exceptions import MCPError
from mcp_server.core.interfaces.template_catalog import FrozenJsonObject, freeze_json
from mcp_server.services.artifact_identity import (
    ArtifactIdentity,
    GenerationPackage,
    GenerationSource,
)
from mcp_server.services.installation_state import ValidatedSuiteEvidence
from mcp_server.services.template_catalog import (
    TemplateCatalog,
    TemplateCatalogLoader,
    TemplateInputValidator,
)
from mcp_server.services.template_components import (
    ComponentKey,
    ComponentSelection,
    component_fingerprints,
)
from mcp_server.services.template_contract_loader import TemplateContractLoader
from mcp_server.services.template_graph import TemplateGraphResolver

Admission = Callable[[Path, Path], "SuiteSnapshot"]


@dataclass(frozen=True)
class ComponentLocation:
    """Physical location of one admitted component within its suite snapshot."""

    kind: Literal["shared", "package"]
    component_id: str
    directory: str

    @property
    def key(self) -> ComponentKey:
        return (self.kind, self.component_id)


@dataclass(frozen=True)
class SuiteSnapshot:
    """Complete immutable catalog, source and component evidence from one suite."""

    root: Path
    catalog: TemplateCatalog
    packages: tuple[GenerationPackage, ...]
    sources: tuple[GenerationSource, ...]
    evidence: ValidatedSuiteEvidence
    locations: tuple[ComponentLocation, ...]

    def __post_init__(self) -> None:
        if not self.root.is_absolute():
            raise ValueError("absolute_suite_snapshot_root_required")
        expected = {state.key for state in (self.evidence.shared, *self.evidence.packages)}
        actual = {location.key for location in self.locations}
        if len(actual) != len(self.locations) or actual != expected:
            raise ValueError("suite_snapshot_location_mismatch")


def admit_template_suite(root: Path, effective_config_root: Path) -> SuiteSnapshot:
    """Load and validate one complete suite through the existing admission chain."""

    if _is_link(root):
        raise MCPError(
            "template_suite_symlink_escape",
            code="ERR_CONFIG",
            params={"source": str(root)},
        )
    suite_root = _absolute_directory(root, "template_suite_root_invalid")
    config_root = _absolute_directory(effective_config_root, "effective_config_root_invalid")
    inventory = _inventory(suite_root)
    contract_reader = TemplateContractLoader(suite_root)
    config = ConfigLoader(
        config_root,
        suite_root,
        context_schema_reader=contract_reader.load_context_schema,
    )
    checks = config.load_checks_config()
    profiles = frozenset(name for name, _ in checks.profiles)
    validator = ConfigValidator()
    environment = Environment()
    graph = TemplateGraphResolver(suite_root, environment.parse)
    provenance = freeze_json(ArtifactIdentity.model_json_schema())
    if not isinstance(provenance, FrozenJsonObject):
        raise MCPError("template_provenance_schema_invalid", code="ERR_CONFIG")
    catalog = TemplateCatalogLoader(
        suite_root,
        read_manifest=config.load_template_manifest,
        read_version=config.load_template_version,
        read_policy=config.load_template_policy,
        read_schema=config.load_template_context_schema,
        validate_policy=lambda policy: validator.validate_template_policy(policy, profiles),
        resolve_graph=graph.resolve,
        validate_inputs=TemplateInputValidator(environment.parse, provenance).validate,
    ).load()
    if _inventory(suite_root) != inventory:
        raise MCPError("template_suite_snapshot_changed", code="ERR_CONFIG")
    packages = tuple(
        GenerationPackage(
            manifest=package.manifest,
            version=package.version,
            directory=package.renderer.partition("/")[0],
        )
        for package in catalog.packages
    )
    states = component_fingerprints(packages, inventory)
    evidence = ValidatedSuiteEvidence(
        shared=next(state for state in states if state.kind == "shared"),
        packages=tuple(state for state in states if state.kind == "package"),
    )
    locations = (
        ComponentLocation(kind="shared", component_id="shared", directory="shared"),
        *(
            ComponentLocation(
                kind="package",
                component_id=package.manifest.template_id,
                directory=package.directory,
            )
            for package in packages
        ),
    )
    return SuiteSnapshot(
        root=suite_root,
        catalog=catalog,
        packages=packages,
        sources=inventory,
        evidence=evidence,
        locations=locations,
    )


class TemplateProposalService:
    """Stage and materialize template suites while leaving admission pure."""

    def __init__(
        self,
        *,
        actual_root: Path,
        candidate_root: Path,
        proposal_root: Path,
        effective_config_root: Path,
        admit: Admission | None = None,
    ) -> None:
        roots = (actual_root, candidate_root, proposal_root, effective_config_root)
        if any(not root.is_absolute() for root in roots):
            raise MCPError("absolute_template_proposal_roots_required", code="ERR_CONFIG")
        self._actual_root = actual_root.resolve()
        self._candidate_root = candidate_root.resolve()
        self._proposal_root = proposal_root.resolve()
        self._config_root = effective_config_root.resolve()
        self._admit = admit or admit_template_suite
        self._validate_owned_roots()

    def admit(self, root: Path) -> SuiteSnapshot:
        """Read and validate a complete suite snapshot without changing filesystem state."""

        return self._admit_snapshot(root, "template_suite_invalid")

    def stage_candidate(self, supplied_candidate_root: Path) -> None:
        """Validate and atomically supersede the flat candidate staging root."""

        try:
            sources = _inventory(supplied_candidate_root)
            snapshot = self._admit_snapshot(supplied_candidate_root, "template_candidate_invalid")
            _assert_snapshot_bytes(snapshot, sources)
            self._materialize_sources(self._candidate_root, sources)
        except MCPError as exc:
            raise self._wrap("template_candidate_invalid", exc) from exc
        except (OSError, ValueError, TypeError) as exc:
            raise self._wrap("template_candidate_invalid", exc) from exc

    def materialize_proposal(
        self,
        selections: Iterable[ComponentSelection],
    ) -> None:
        """Materialize selected complete component bytes and validate the result off-root."""

        incoming = self._temporary_root(self._proposal_root)
        self._remove_tree(incoming)
        try:
            actual = self._admit_snapshot(self._actual_root, "template_proposal_invalid")
            candidate = self._admit_snapshot(self._candidate_root, "template_proposal_invalid")
            sources = _selected_sources(actual, candidate, tuple(selections))
            self._materialize_sources(incoming, sources)
            admitted = self._admit_snapshot(incoming, "template_proposal_invalid")
            _assert_snapshot_bytes(admitted, sources)
            self._replace_tree(incoming, self._proposal_root)
        except MCPError as exc:
            self._remove_tree(incoming)
            raise self._wrap("template_proposal_invalid", exc) from exc
        except (OSError, ValueError, TypeError) as exc:
            self._remove_tree(incoming)
            raise self._wrap("template_proposal_invalid", exc) from exc

    def _admit_snapshot(self, root: Path, failure: str) -> SuiteSnapshot:
        try:
            candidate = _absolute_directory(root, "template_suite_root_invalid")
            snapshot = _invoke_admission(self._admit, candidate, self._config_root)
            if snapshot.root.resolve() != candidate.resolve():
                raise MCPError("template_admission_root_mismatch", code="ERR_CONFIG")
            return snapshot
        except MCPError:
            raise
        except (OSError, ValueError, TypeError) as exc:
            raise self._wrap(failure, exc) from exc

    def _materialize_sources(
        self,
        target: Path,
        sources: tuple[GenerationSource, ...],
    ) -> None:
        incoming = self._temporary_root(target)
        self._remove_tree(incoming)
        try:
            incoming.mkdir(parents=True, exist_ok=False)
            owner = incoming.resolve(strict=True)
            for source in sources:
                relative = Path(source.path)
                destination = incoming / relative
                lexical = Path(os.path.abspath(destination))
                if not lexical.is_relative_to(Path(os.path.abspath(incoming))):
                    raise MCPError("template_source_path_invalid", code="ERR_CONFIG")
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(source.content)
                resolved = destination.resolve(strict=True)
                if not resolved.is_relative_to(owner):
                    raise MCPError("template_source_path_escape", code="ERR_CONFIG")
            self._replace_tree(incoming, target)
        except BaseException:
            self._remove_tree(incoming)
            raise

    def _wrap(self, message: str, error: BaseException) -> MCPError:
        if isinstance(error, MCPError):
            params = dict(error.params)
            cause = error.message
            code = error.code
        else:
            params = {}
            cause = str(error)
            code = "ERR_CONFIG"
        params.update({"cause": cause, "config_root": str(self._config_root)})
        if code != "ERR_CONFIG":
            params["admission_code"] = code
        return MCPError(message, code="ERR_CONFIG", params=params)

    def _validate_owned_roots(self) -> None:
        mutable = (self._candidate_root, self._proposal_root)
        if self._candidate_root == self._proposal_root:
            raise MCPError("template_proposal_roots_overlap", code="ERR_CONFIG")
        for root in mutable:
            if (
                root == self._actual_root
                or root.is_relative_to(self._actual_root)
                or self._actual_root.is_relative_to(root)
                or root == self._config_root
                or root.is_relative_to(self._config_root)
                or self._config_root.is_relative_to(root)
            ):
                raise MCPError("template_proposal_roots_overlap", code="ERR_CONFIG")

    @staticmethod
    def _temporary_root(target: Path) -> Path:
        return target.parent / f".{target.name}.incoming"

    @classmethod
    def _replace_tree(cls, prepared: Path, target: Path) -> None:
        prior = target.parent / f".{target.name}.previous"
        cls._remove_tree(prior)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() or target.is_symlink():
            target.replace(prior)
        try:
            prepared.replace(target)
        except OSError:
            if prior.exists() and not target.exists():
                prior.replace(target)
            raise
        cls._remove_tree(prior)

    @staticmethod
    def _remove_tree(path: Path) -> None:
        if path.is_symlink() or _is_junction(path):
            path.unlink()
        elif path.exists():
            shutil.rmtree(path)


def _invoke_admission(
    admit: Admission,
    root: Path,
    config_root: Path,
) -> SuiteSnapshot:
    try:
        parameters = inspect.signature(admit).parameters
    except (TypeError, ValueError):
        parameters = {}
    if len(parameters) == 1:
        return admit(root)  # type: ignore[call-arg]
    return admit(root, config_root)


def _absolute_directory(path: Path, message: str) -> Path:
    if not path.is_absolute():
        raise MCPError(message, code="ERR_CONFIG")
    candidate = path.resolve(strict=True)
    if not candidate.is_dir():
        raise MCPError(message, code="ERR_CONFIG")
    return candidate


def _inventory(root: Path) -> tuple[GenerationSource, ...]:
    if _is_link(root):
        raise MCPError(
            "template_suite_symlink_escape",
            code="ERR_CONFIG",
            params={"source": str(root)},
        )
    suite = _absolute_directory(root, "template_suite_root_invalid")
    if _is_link(suite):
        raise MCPError(
            "template_suite_symlink_escape",
            code="ERR_CONFIG",
            params={"source": str(suite)},
        )
    resolved_suite = suite.resolve(strict=True)
    records: list[GenerationSource] = []
    for current, directories, files in os.walk(suite, followlinks=False):
        current_path = Path(current)
        for name in (*directories, *files):
            member = current_path / name
            if _is_link(member):
                raise MCPError(
                    "template_suite_symlink_escape",
                    code="ERR_CONFIG",
                    params={"source": str(member)},
                )
            lexical = Path(os.path.abspath(member))
            if not lexical.is_relative_to(Path(os.path.abspath(suite))):
                raise MCPError("template_suite_path_escape", code="ERR_CONFIG")
            resolved = member.resolve(strict=True)
            if not resolved.is_relative_to(resolved_suite):
                raise MCPError(
                    "template_suite_path_escape",
                    code="ERR_CONFIG",
                    params={"source": str(member)},
                )
            logical = member.relative_to(suite).as_posix()
            resolved_logical = resolved.relative_to(resolved_suite).as_posix()
            if logical.split("/", 1)[0] != resolved_logical.split("/", 1)[0]:
                raise MCPError(
                    "template_suite_component_escape",
                    code="ERR_CONFIG",
                    params={"source": logical},
                )
            if member.is_file():
                records.append(GenerationSource(path=logical, content=member.read_bytes()))
    return tuple(sorted(records, key=lambda item: item.path))


def _assert_snapshot_bytes(
    snapshot: SuiteSnapshot,
    expected: tuple[GenerationSource, ...],
) -> None:
    if snapshot.sources != expected:
        raise MCPError("template_suite_snapshot_incomplete", code="ERR_CONFIG")


def _selected_sources(
    actual: SuiteSnapshot,
    candidate: SuiteSnapshot,
    selections: tuple[ComponentSelection, ...],
) -> tuple[GenerationSource, ...]:
    actual_locations = {location.key: location for location in actual.locations}
    candidate_locations = {location.key: location for location in candidate.locations}
    selected = {selection.key: selection for selection in selections}
    if len(selected) != len(selections):
        raise MCPError("template_component_selection_duplicate", code="ERR_CONFIG")
    expected = set(actual_locations) | set(candidate_locations)
    if set(selected) != expected:
        raise MCPError("template_component_selection_incomplete", code="ERR_CONFIG")
    result: list[GenerationSource] = []
    for key, selection in selected.items():
        if not selection.selected.present:
            continue
        snapshot = actual if selection.selected_source == "actual" else candidate
        location = {item.key: item for item in snapshot.locations}.get(key)
        if location is None:
            raise MCPError("template_selected_component_missing", code="ERR_CONFIG")
        prefix = f"{location.directory}/"
        result.extend(source for source in snapshot.sources if source.path == location.directory or source.path.startswith(prefix))
    if not result:
        raise MCPError("template_proposal_empty", code="ERR_CONFIG")
    return tuple(sorted(result, key=lambda item: item.path))


def _is_link(path: Path) -> bool:
    return path.is_symlink() or _is_junction(path)


def _is_junction(path: Path) -> bool:
    checker = getattr(path, "is_junction", None)
    return bool(checker and checker())


__all__ = [
    "ComponentLocation",
    "SuiteSnapshot",
    "TemplateProposalService",
    "admit_template_suite",
]
