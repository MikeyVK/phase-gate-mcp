# pgmcp:v1 id=python_class pv=1.0.0 pf=u_KOYBekCfsMbBaW sf=5--KpGf2wHUv2qAj

"""Tool-independent configured-target matching without filesystem or native discovery."""

from __future__ import annotations

import re
from pathlib import Path

from mcp_server.config.schemas.checks_config import ConfiguredTargets

CompiledPattern = tuple[re.Pattern[str] | None, ...]


def _compile(pattern: str) -> CompiledPattern:
    return tuple(
        None
        if part == "**"
        else re.compile(re.escape(part).replace(r"\*", "[^/]*").replace(r"\?", "[^/]"))
        for part in pattern.split("/")
    )


def _matches(parts: tuple[str, ...], pattern: CompiledPattern) -> bool:
    positions = {0}
    for component in pattern:
        if component is None:
            positions = {
                position for start in positions for position in range(start, len(parts) + 1)
            }
        else:
            positions = {
                position + 1
                for position in positions
                if position < len(parts) and component.fullmatch(parts[position]) is not None
            }
        if not positions:
            return False
    return len(parts) in positions


class ConfiguredTargetMatcher:
    """Match admitted policies against candidates relative to the shared canonical root."""

    def __init__(self, workspace_root: Path) -> None:
        if not workspace_root.is_absolute():
            raise ValueError("absolute_workspace_required")
        self._workspace_root = workspace_root

    def select(self, targets: tuple[Path, ...], *, policy: ConfiguredTargets) -> tuple[Path, ...]:
        include = tuple(_compile(pattern) for pattern in policy.include)
        exclude = tuple(_compile(pattern) for pattern in policy.exclude)
        selected: list[Path] = []
        for target in targets:
            parts = tuple(target.relative_to(self._workspace_root).as_posix().split("/"))
            if any(_matches(parts, pattern) for pattern in include) and not any(
                _matches(parts, pattern) for pattern in exclude
            ):
                selected.append(target)
        return tuple(selected)
