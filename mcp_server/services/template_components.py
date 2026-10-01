"""Pure operational component fingerprints and immutable three-way selection."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Literal, TypeAlias

from pydantic import BaseModel, ConfigDict, model_validator

from mcp_server.config.schemas.template_suite import TemplateId
from mcp_server.core.exceptions import MCPError
from mcp_server.schemas.template_identity import CompactFingerprint
from mcp_server.services.artifact_identity import (
    FingerprintRecord,
    GenerationPackage,
    GenerationSource,
    fingerprint_records,
    normalize_source_bytes,
)

SHARED_COMPONENT_ID = "shared"
ComponentKind = Literal["shared", "package"]
ComponentKey: TypeAlias = tuple[ComponentKind, str]
ComponentRelation = Literal[
    "unchanged",
    "upstream_only",
    "local_only",
    "converged",
    "conflict",
]
CheckpointAction = Literal["retain_adopted", "advance_to_candidate"]
ChangeKind = Literal["none", "addition", "removal", "change"]


class ComponentState(BaseModel):
    """One immutable namespaced component state, including explicit absence."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    kind: ComponentKind
    component_id: TemplateId
    present: bool
    fingerprint: CompactFingerprint | None = None

    @model_validator(mode="after")
    def validate_presence(self) -> ComponentState:
        if self.present != (self.fingerprint is not None):
            raise ValueError("component_presence_fingerprint_mismatch")
        if self.kind == "shared" and self.component_id != SHARED_COMPONENT_ID:
            raise ValueError("shared_component_id_invalid")
        return self

    @property
    def key(self) -> ComponentKey:
        """Return the stable namespace and manifest-ID key."""

        return (self.kind, self.component_id)


class ComponentSelection(BaseModel):
    """Pure selection facts for one adopted/actual/candidate component."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    kind: ComponentKind
    component_id: TemplateId
    adopted: ComponentState
    actual: ComponentState
    candidate: ComponentState
    relation: ComponentRelation
    selected: ComponentState
    selected_source: Literal["actual", "candidate"]
    checkpoint_action: CheckpointAction
    proposed_checkpoint: ComponentState
    change_kind: ChangeKind

    @model_validator(mode="after")
    def validate_ids(self) -> ComponentSelection:
        states = (self.adopted, self.actual, self.candidate, self.selected)
        if any(state.key != self.key for state in states):
            raise ValueError("component_selection_key_mismatch")
        if self.proposed_checkpoint.key != self.key:
            raise ValueError("component_checkpoint_key_mismatch")
        return self

    @property
    def key(self) -> ComponentKey:
        return (self.kind, self.component_id)


def component_fingerprints(
    packages: tuple[GenerationPackage, ...],
    sources: tuple[GenerationSource, ...],
) -> tuple[ComponentState, ...]:
    """Compute complete operational states from one admitted source snapshot."""

    package_dirs = {package.directory: package for package in packages}
    package_ids = [package.manifest.template_id for package in packages]
    if len(package_dirs) != len(packages) or len(set(package_ids)) != len(package_ids):
        raise MCPError("template_component_inventory_invalid", code="ERR_CONFIG")

    files: dict[str, bytes] = {}
    for source in sources:
        if source.path in files:
            raise MCPError("template_component_source_duplicate", code="ERR_CONFIG")
        files[source.path] = source.content

    grouped: dict[ComponentKey, list[FingerprintRecord]] = {
        ("shared", SHARED_COMPONENT_ID): [],
        **{("package", package.manifest.template_id): [] for package in packages},
    }
    for path, content in files.items():
        owner, separator, relative = path.partition("/")
        if not separator:
            raise MCPError(
                "template_component_source_invalid",
                code="ERR_CONFIG",
                params={"source": path},
            )
        if owner == SHARED_COMPONENT_ID:
            grouped[("shared", SHARED_COMPONENT_ID)].append(
                FingerprintRecord("file", relative, normalize_source_bytes(content))
            )
            continue
        package = package_dirs.get(owner)
        if package is None:
            raise MCPError(
                "template_component_source_unknown",
                code="ERR_CONFIG",
                params={"source": path},
            )
        grouped[("package", package.manifest.template_id)].append(
            FingerprintRecord("file", relative, normalize_source_bytes(content))
        )

    states: list[ComponentState] = []
    for kind, component_id in _ordered_component_keys(grouped):
        records = grouped[(kind, component_id)]
        fingerprint = fingerprint_records(_domain(kind), records)
        states.append(
            ComponentState(
                kind=kind,
                component_id=component_id,
                present=kind == "shared" or bool(records),
                fingerprint=fingerprint if kind == "shared" or records else None,
            )
        )
    return tuple(states)


def select_components(
    adopted: Mapping[ComponentKey, ComponentState],
    actual: Mapping[ComponentKey, ComponentState],
    candidate: Mapping[ComponentKey, ComponentState],
) -> tuple[ComponentSelection, ...]:
    """Select complete components without changing any input mapping."""

    maps = tuple(_validated_map(states) for states in (adopted, actual, candidate))
    keys = set().union(*(mapping.keys() for mapping in maps))
    result: list[ComponentSelection] = []
    for kind, component_id in _ordered_component_keys(dict.fromkeys(keys)):
        key = (kind, component_id)
        adopted_state = _state_for(key, maps[0])
        actual_state = _state_for(key, maps[1])
        candidate_state = _state_for(key, maps[2])
        relation, selected, source, action = _classify(
            adopted_state,
            actual_state,
            candidate_state,
        )
        result.append(
            ComponentSelection(
                kind=kind,
                component_id=component_id,
                adopted=adopted_state,
                actual=actual_state,
                candidate=candidate_state,
                relation=relation,
                selected=selected,
                selected_source=source,
                checkpoint_action=action,
                proposed_checkpoint=(
                    candidate_state if action == "advance_to_candidate" else adopted_state
                ),
                change_kind=_change_kind(adopted_state, candidate_state),
            )
        )
    return tuple(result)


def _validated_map(
    states: Mapping[ComponentKey, ComponentState],
) -> dict[ComponentKey, ComponentState]:
    if not isinstance(states, Mapping):
        raise TypeError("component_states_must_be_mapping")
    result = dict(states)
    if any(
        not isinstance(component_key, tuple)
        or len(component_key) != 2
        or not isinstance(component_key[0], str)
        or not isinstance(component_key[1], str)
        or not isinstance(state, ComponentState)
        or state.key != component_key
        for component_key, state in result.items()
    ):
        raise ValueError("component_state_map_invalid")
    return result


def _state_for(
    key: ComponentKey,
    states: Mapping[ComponentKey, ComponentState],
) -> ComponentState:
    kind, component_id = key
    return states.get(
        key,
        ComponentState(kind=kind, component_id=component_id, present=False),
    )


def _ordered_component_keys(
    states: Mapping[ComponentKey, object],
) -> tuple[ComponentKey, ...]:
    return tuple(
        sorted(
            states,
            key=lambda key: (
                key[0] != "shared",
                key[1],
            ),
        )
    )


def _domain(kind: ComponentKind) -> str:
    return (
        "pgmcp:template-component:shared:v1"
        if kind == "shared"
        else "pgmcp:template-component:package:v1"
    )


def _equal(left: ComponentState, right: ComponentState) -> bool:
    return left.present == right.present and left.fingerprint == right.fingerprint


def _classify(
    adopted: ComponentState,
    actual: ComponentState,
    candidate: ComponentState,
) -> tuple[
    ComponentRelation,
    ComponentState,
    Literal["actual", "candidate"],
    CheckpointAction,
]:
    actual_adopted = _equal(actual, adopted)
    candidate_adopted = _equal(candidate, adopted)
    actual_candidate = _equal(actual, candidate)
    if actual_adopted and candidate_adopted:
        return "unchanged", actual, "actual", "retain_adopted"
    if actual_adopted:
        return "upstream_only", candidate, "candidate", "advance_to_candidate"
    if candidate_adopted:
        return "local_only", actual, "actual", "retain_adopted"
    if actual_candidate:
        return "converged", actual, "actual", "advance_to_candidate"
    return "conflict", actual, "actual", "retain_adopted"


def _change_kind(
    adopted: ComponentState,
    candidate: ComponentState,
) -> ChangeKind:
    if adopted.present == candidate.present:
        if not adopted.present or adopted.fingerprint == candidate.fingerprint:
            return "none"
        return "change"
    return "addition" if candidate.present else "removal"
