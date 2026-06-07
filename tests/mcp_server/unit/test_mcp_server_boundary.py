# tests/mcp_server/unit/test_mcp_server_boundary.py
"""
Permanent architectural boundary tests for phase-gate-mcp.

Verifies that the mcp_server package maintains its boundary:
- no imports from backend.*
- pyproject.toml covers only mcp_server*

Zone 1: source inspection and pyproject.toml parsing; no network, no YAML.

@layer: Tests (Unit)
@dependencies: [tomllib, pathlib]
"""

import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).parents[3]


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


def test_pyproject_includes_only_mcp_server() -> None:
    """pyproject.toml packages.find.include must contain only mcp_server*, not backend*."""
    pyproject = REPO_ROOT / "pyproject.toml"
    with open(pyproject, "rb") as f:
        data = tomllib.load(f)
    include = data["tool"]["setuptools"]["packages"]["find"]["include"]
    backend_entries = [e for e in include if e.startswith("backend")]
    assert backend_entries == [], f"pyproject.toml still includes backend*: {backend_entries}"
