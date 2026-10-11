# pgmcp:v1 id=python_class pv=1.0.0 pf=u_KOYBekCfsMbBaW sf=5--KpGf2wHUv2qAj
"""Shared lossless scope grammar and configuration vocabulary admission."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mcp_server.config.schemas.workphases import WorkphasesConfig

_TOKEN = re.compile(r"[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*")
_RESERVED = re.compile(r"(?:^|_)SP(?:_|$)|_C[0-9]+(?:_|$)")
_SCOPE = re.compile(
    r"P_(?P<phase>[A-Z][A-Z0-9_]*?)"
    r"(?:_C(?P<cycle>[1-9][0-9]*))?"
    r"(?:_SP_(?P<subphase>[A-Z][A-Z0-9_]*))?"
)


def _admit_names(names: Sequence[str]) -> None:
    """Reject tokens whose normalization or delimiters prevent lossless decoding."""
    tokens: set[str] = set()
    for name in names:
        token = name.upper()
        if _TOKEN.fullmatch(token) is None or _RESERVED.search(token):
            raise ValueError("scope_vocabulary_invalid", name)
        if token in tokens:
            raise ValueError("scope_vocabulary_ambiguous", name)
        tokens.add(token)


def validate_scope_vocabulary(phases: Mapping[str, Sequence[str]]) -> None:
    """Validate configured vocabulary without importing or loading configuration."""
    _admit_names(list(phases))
    for subphases in phases.values():
        _admit_names(subphases)


@dataclass(frozen=True)
class ScopeFields:
    """Configured canonical names and an independently optional cycle."""

    workflow_phase: str
    cycle_number: int | None
    sub_phase: str | None


class ScopeContract:
    """Encode and decode one grammar over admitted injected vocabulary."""

    def __init__(self, workphases_config: WorkphasesConfig) -> None:
        self._phases = {name.upper(): name for name in workphases_config.phases}
        self._subphases = {
            name.upper(): {sub.upper(): sub for sub in definition.subphases}
            for name, definition in workphases_config.phases.items()
        }

    def encode(self, fields: ScopeFields) -> str:
        """Return a canonical scope or reject an invalid semantic value."""
        phase = fields.workflow_phase.upper()
        if phase not in self._phases:
            raise ValueError("scope_phase_unknown", fields.workflow_phase)
        cycle = fields.cycle_number
        if cycle is not None and (type(cycle) is not int or cycle < 1):
            raise ValueError("scope_cycle_invalid", cycle)
        subphase = fields.sub_phase.upper() if fields.sub_phase is not None else None
        if subphase is not None and subphase not in self._subphases[phase]:
            raise ValueError("scope_subphase_unknown", fields.sub_phase)
        scope = f"P_{phase}"
        if cycle is not None:
            scope += f"_C{cycle}"
        if subphase is not None:
            scope += f"_SP_{subphase}"
        return scope

    def decode(self, scope: str) -> ScopeFields | None:
        """Return canonical configured fields or no interpretation for invalid input."""
        match = _SCOPE.fullmatch(scope.upper())
        if match is None:
            return None
        phase_token = match.group("phase")
        phase = self._phases.get(phase_token)
        if phase is None:
            return None
        subphase_token = match.group("subphase")
        subphase = None
        if subphase_token is not None:
            subphase = self._subphases[phase_token].get(subphase_token)
            if subphase is None:
                return None
        cycle_token = match.group("cycle")
        try:
            cycle = int(cycle_token) if cycle_token is not None else None
        except ValueError:
            return None
        return ScopeFields(phase, cycle, subphase)
