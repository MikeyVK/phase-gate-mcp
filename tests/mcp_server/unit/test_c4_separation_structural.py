# tests/mcp_server/unit/test_c4_separation_structural.py
"""
Structural invariant tests for C4: ST3 backend removal from phase-gate-mcp.

Verifies that after separation, the phase-gate-mcp repo no longer tracks
ST3 backend content (backend/, tests/backend/, locales/, docs/temp/, etc.)
and that pyproject.toml covers only mcp_server*.

Zone 1: git ls-files and pyproject.toml inspection; no imports, no network.

@layer: Tests (Unit)
@dependencies: [subprocess, pathlib, tomllib]
"""
import subprocess
import sys
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).parents[3]

ST3_PATHS_MUST_BE_ABSENT = [
    "backend/",
    "tests/backend/",
    "locales/",
    "docs/temp/",
    "docs/architecture/",
    "docs/coding_standards/",
    "docs/system/",
    "docs/implementation/",
]


def _git_tracked_files() -> set[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        check=True,
    )
    return set(result.stdout.splitlines())


def test_backend_dir_not_tracked() -> None:
    """backend/ must not be tracked in phase-gate-mcp after C4."""
    tracked = _git_tracked_files()
    backend_files = [f for f in tracked if f.startswith("backend/")]
    assert backend_files == [], f"backend/ still tracked: {backend_files[:5]}"


def test_tests_backend_not_tracked() -> None:
    """tests/backend/ must not be tracked in phase-gate-mcp after C4."""
    tracked = _git_tracked_files()
    found = [f for f in tracked if f.startswith("tests/backend/")]
    assert found == [], f"tests/backend/ still tracked: {found[:5]}"


def test_locales_not_tracked() -> None:
    """locales/ must not be tracked in phase-gate-mcp after C4."""
    tracked = _git_tracked_files()
    found = [f for f in tracked if f.startswith("locales/")]
    assert found == [], f"locales/ still tracked: {found[:5]}"


def test_docs_temp_not_tracked() -> None:
    """docs/temp/ must not be tracked in phase-gate-mcp after C4."""
    tracked = _git_tracked_files()
    found = [f for f in tracked if f.startswith("docs/temp/")]
    assert found == [], f"docs/temp/ still tracked: {found[:5]}"


def test_docs_architecture_not_tracked() -> None:
    """docs/architecture/ must not be tracked in phase-gate-mcp after C4."""
    tracked = _git_tracked_files()
    found = [f for f in tracked if f.startswith("docs/architecture/")]
    assert found == [], f"docs/architecture/ still tracked: {found[:5]}"


def test_docs_system_not_tracked() -> None:
    """docs/system/ must not be tracked in phase-gate-mcp after C4."""
    tracked = _git_tracked_files()
    found = [f for f in tracked if f.startswith("docs/system/")]
    assert found == [], f"docs/system/ still tracked: {found[:5]}"


def test_docs_implementation_not_tracked() -> None:
    """docs/implementation/ must not be tracked in phase-gate-mcp after C4."""
    tracked = _git_tracked_files()
    found = [f for f in tracked if f.startswith("docs/implementation/")]
    assert found == [], f"docs/implementation/ still tracked: {found[:5]}"


def test_pyproject_includes_only_mcp_server() -> None:
    """pyproject.toml packages.find.include must contain only mcp_server*, not backend*."""
    pyproject = REPO_ROOT / "pyproject.toml"
    with open(pyproject, "rb") as f:
        data = tomllib.load(f)
    include = data["tool"]["setuptools"]["packages"]["find"]["include"]
    backend_entries = [e for e in include if e.startswith("backend")]
    assert backend_entries == [], f"pyproject.toml still includes backend*: {backend_entries}"


def test_no_backend_imports_in_mcp_server() -> None:
    """No mcp_server source file may import from backend.*"""
    mcp_src = REPO_ROOT / "mcp_server"
    violations = []
    for py_file in mcp_src.rglob("*.py"):
        text = py_file.read_text(encoding="utf-8")
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith(("import backend", "from backend")):
                violations.append(f"{py_file.relative_to(REPO_ROOT)}: {stripped}")
    assert violations == [], "backend imports found in mcp_server:\n" + "\n".join(violations)
