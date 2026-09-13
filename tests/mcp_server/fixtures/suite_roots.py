# tests/mcp_server/fixtures/suite_roots.py
# template=generic version=f35abd82 created=2026-09-13T14:34Z updated=
"""Explicit filesystem support; synthetic trees and delivered suites stay separate.

@layer: Tests (Support)
@dependencies: pathlib, pytest, mcp_server.config.settings
"""

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path, PureWindowsPath
from shutil import copytree

import pytest

from mcp_server.config.settings import ServerSettings


@dataclass(frozen=True)
class SuiteRoots:
    """Named isolated paths, with no configuration or loader state."""

    workspace: Path
    server: Path
    config: Path
    templates: Path
    bundled_adapters: Path
    workspace_adapters: Path
    temp: Path


def create_suite_roots(parent: Path, server_root_name: str) -> SuiteRoots:
    """Create empty roots beneath an explicitly selected absolute parent."""
    if not parent.is_absolute():
        raise ValueError("An absolute parent is required")
    name = Path(server_root_name)
    if (
        not server_root_name
        or name.name != server_root_name
        or server_root_name in {".", ".."}
        or PureWindowsPath(server_root_name).drive
    ):
        raise ValueError("The server root must be one relative directory name")
    workspace = parent.resolve()
    server = workspace / server_root_name
    roots = SuiteRoots(
        workspace=workspace,
        server=server,
        config=server / "config",
        templates=server / "templates",
        bundled_adapters=server / "adapters",
        workspace_adapters=workspace / "adapters",
        temp=workspace / "temp",
    )
    directories = (
        roots.config,
        roots.templates,
        roots.bundled_adapters,
        roots.workspace_adapters,
        roots.temp,
    )
    if any(not path.resolve().is_relative_to(workspace) for path in directories):
        raise ValueError("Suite directories must remain inside the selected workspace")
    for path in directories:
        path.mkdir(parents=True, exist_ok=True)
    return roots


def write_package_tree(root: Path, files: Mapping[str, bytes]) -> Path:
    """Write explicitly authored bytes after checking every path for containment."""
    if not root.is_absolute():
        raise ValueError("An absolute package root is required")
    resolved_root = root.resolve()
    targets: dict[Path, bytes] = {}
    for relative_name, content in files.items():
        relative = Path(relative_name)
        portable = PureWindowsPath(relative_name)
        target = (resolved_root / relative).resolve()
        if (
            not relative_name
            or relative.is_absolute()
            or portable.is_absolute()
            or portable.drive
            or ".." in relative.parts
            or ".." in portable.parts
            or target == resolved_root
            or not target.is_relative_to(resolved_root)
            or target in targets
        ):
            raise ValueError(f"Package path is not a unique contained file: {relative_name!r}")
        targets[target] = content
    for target, content in targets.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    return resolved_root


@pytest.fixture
def suite_roots(tmp_path: Path) -> SuiteRoots:
    """Provide empty roots using the current legacy server directory convention."""
    return create_suite_roots(tmp_path, ServerSettings().server_root_dir)


@pytest.fixture
def legacy_suite_roots(suite_roots: SuiteRoots, pytestconfig: pytest.Config) -> SuiteRoots:
    """Copy actual legacy sources for retained consumers, without changing the process."""
    source = pytestconfig.rootpath / suite_roots.server.name
    copytree(source / "config", suite_roots.config, dirs_exist_ok=True)
    copytree(source / "templates", suite_roots.templates, dirs_exist_ok=True)
    return suite_roots


@pytest.fixture
def legacy_suite_workspace(legacy_suite_roots: SuiteRoots) -> Path:
    """Expose the isolated workspace to existing workspace-based test constructors."""
    return legacy_suite_roots.workspace
