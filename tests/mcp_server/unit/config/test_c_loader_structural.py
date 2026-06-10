# tests/mcp_server/unit/config/test_c_loader_structural.py
"""
Structural regression tests for config-path and legacy exception kwargs.

Guards against re-introduction of raw config-path literals in Path() calls
and legacy hint/blocker/recovery kwargs in production code.

@layer: Tests (Unit)
@dependencies: [ast, pathlib]
@responsibilities:
    - Detect raw .phase-gate/config path literals in Path() calls
    - Detect legacy hints= kwargs in production calls
    - Detect legacy blockers=/recovery= kwargs in production calls
"""

# Standard library
import ast
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[4]
PRODUCTION_ROOT = WORKSPACE_ROOT / "mcp_server"


def _iter_production_python_files() -> list[Path]:
    """Return all production Python files under mcp_server/."""
    return sorted(path for path in PRODUCTION_ROOT.rglob("*.py") if "__pycache__" not in path.parts)


def _parse_python_file(path: Path) -> ast.AST:
    """Parse a Python file into an AST tree."""
    source = path.read_text(encoding="utf-8")
    return ast.parse(source, filename=str(path))


def _relative_path(path: Path) -> str:
    """Return a workspace-relative path string with forward slashes."""
    return path.relative_to(WORKSPACE_ROOT).as_posix()


def _string_constants(tree: ast.AST) -> list[str]:
    """Collect all string constants from an AST tree."""
    constants: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            constants.append(node.value)
    return constants


def _path_constructor_strings(tree: ast.AST) -> list[str]:
    """Collect string args passed to Path() constructors."""
    strings: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name) and node.func.id == "Path":
            for arg in node.args:
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    strings.append(arg.value)
    return strings


def _keyword_matches(tree: ast.AST, *names: str) -> list[str]:
    """Collect matching keyword argument names from call nodes."""
    matches: list[str] = []
    target_names = set(names)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        for keyword in node.keywords:
            if keyword.arg in target_names:
                matches.append(keyword.arg)
    return matches


def test_no_raw_st3_config_paths_in_production() -> None:
    """No production Python module may hardcode .phase-gate/config paths in Path() calls."""
    offenders: list[str] = []

    for path in _iter_production_python_files():
        tree = _parse_python_file(path)
        literals = [v for v in _path_constructor_strings(tree) if ".phase-gate/config/" in v]
        if literals:
            offenders.append(f"{_relative_path(path)}: {literals[0]}")

    assert not offenders, (
        "Raw .phase-gate/config/ path literals in Path() calls remain in production code:\n"
        + "\n".join(offenders)
    )


def test_no_hints_kwarg_on_mcp_error_callsites() -> None:
    """Legacy hints= kwargs must disappear from production call sites."""
    offenders: list[str] = []

    for path in _iter_production_python_files():
        tree = _parse_python_file(path)
        if _keyword_matches(tree, "hints"):
            offenders.append(_relative_path(path))

    assert not offenders, "Legacy hints= kwargs remain in production code:\n" + "\n".join(offenders)


def test_no_blockers_or_recovery_kwargs_on_exception_callsites() -> None:
    """Legacy blockers=/recovery= kwargs must disappear from production calls."""
    offenders: list[str] = []

    for path in _iter_production_python_files():
        tree = _parse_python_file(path)
        if _keyword_matches(tree, "blockers", "recovery"):
            offenders.append(_relative_path(path))

    assert not offenders, (
        "Legacy blockers=/recovery= kwargs remain in production code:\n" + "\n".join(offenders)
    )


def test_no_st3_or_simpletrader_naming_in_tests() -> None:
    """No test Python module may contain the legacy terms 'st3' or 'simpletrader' (case-insensitive)."""
    import re
    # Match st3 or simpletrader as word parts or standalone words (e.g. st3_dir, _ST3_CONFIG, SimpleTraderV3)
    legacy_pattern = re.compile(r"st3|simpletrader", re.IGNORECASE)
    offenders = []

    # Scan all Python files in tests/
    tests_root = WORKSPACE_ROOT / "tests"
    for path in tests_root.rglob("*.py"):
        # Exclude this file itself to avoid false positives on the test definition
        if path.name == "test_c_loader_structural.py":
            continue

        content = path.read_text(encoding="utf-8")
        # Find all occurrences of the pattern
        matches = legacy_pattern.findall(content)
        if matches:
            offenders.append(f"{path.relative_to(WORKSPACE_ROOT).as_posix()} (matches: {set(matches)})")

    assert not offenders, (
        "Legacy terms 'st3' or 'simpletrader' found in test suite files:\n"
        + "\n".join(offenders)
    )
