# tests/mcp_server/unit/fixtures/test_suite_roots.py
# template=unit_test version=8825c0bb created=2026-09-13T14:43Z updated=
"""Verify root isolation through real configuration reads and actual file bytes.

@layer: Tests (Unit)
@dependencies: pytest, mcp_server.config.loader, tests.mcp_server.fixtures.suite_roots
"""

import os
import subprocess
from pathlib import Path

import pytest

from mcp_server.config.loader import ConfigLoader
from mcp_server.core.exceptions import ConfigError
from tests.mcp_server.fixtures.suite_roots import (
    SuiteRoots,
    create_suite_roots,
    write_package_tree,
)


def test_config_loaders_remain_isolated_from_cwd_and_environment(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Distinct authored configuration remains local under hostile ambient roots."""
    original_cwd = Path.cwd()
    original_environment = dict(os.environ)
    first = create_suite_roots(tmp_path / "first", "owned")
    second = create_suite_roots(tmp_path / "second", "owned")
    first_bytes = (
        b"version: '1.0.0'\nworkflows:\n  alpha:\n"
        b"    name: alpha\n    default_execution_mode: interactive\n"
        b"    description: First root\n"
    )
    second_bytes = (
        b"version: '1.0.0'\nworkflows:\n  beta:\n"
        b"    name: beta\n    default_execution_mode: autonomous\n"
        b"    description: Second root\n"
    )
    write_package_tree(first.config, {"workflows.yaml": first_bytes})
    write_package_tree(second.config, {"workflows.yaml": second_bytes})
    first_loader = ConfigLoader(first.config, first.templates)
    second_loader = ConfigLoader(second.config, second.templates)
    with monkeypatch.context() as ambient:
        ambient.chdir(second.workspace)
        ambient.setenv("PGMCP_CONFIG_ROOT", str(second.config))
        ambient.setenv("PGMCP_TEMPLATE_ROOT", str(second.templates))
        left = first_loader.load_workflow_config()
        right = second_loader.load_workflow_config()
        assert set(left.workflows) == {"alpha"}
        assert left.get_workflow("alpha").description == "First root"
        assert set(right.workflows) == {"beta"}
        assert right.get_workflow("beta").default_execution_mode == "autonomous"
        (first.config / "workflows.yaml").unlink()
        with pytest.raises(ConfigError):
            first_loader.load_workflow_config()
        assert second_loader.load_workflow_config() == right
        assert (second.config / "workflows.yaml").read_bytes() == second_bytes
        assert Path.cwd() == second.workspace
    assert Path.cwd() == original_cwd
    assert dict(os.environ) == original_environment


def test_roots_are_empty_and_do_not_mutate_process_state(tmp_path: Path) -> None:
    """Creating support introduces neither package defaults nor process-wide state."""
    original_cwd = Path.cwd()
    original_environment = dict(os.environ)
    roots = create_suite_roots(tmp_path, "selected-server")
    paths = (
        roots.config,
        roots.templates,
        roots.bundled_adapters,
        roots.workspace_adapters,
        roots.temp,
    )
    assert roots.workspace == tmp_path
    assert roots.server == tmp_path / "selected-server"
    assert len(set(paths)) == len(paths)
    assert all(path.is_dir() and not list(path.iterdir()) for path in paths)
    assert Path.cwd() == original_cwd
    assert dict(os.environ) == original_environment


@pytest.mark.parametrize("invalid_name", ["", ".", "../escape", "nested/../../escape", "C:/escape"])
def test_package_tree_rejects_escape_before_writing(tmp_path: Path, invalid_name: str) -> None:
    """A bad package entry cannot partially populate the otherwise valid tree."""
    root = tmp_path / "package"
    with pytest.raises(ValueError, match="contained file"):
        write_package_tree(root, {"valid/schema.json": b"{}", invalid_name: b"untrusted"})
    assert not root.exists()
    assert not (tmp_path / "escape").exists()


def test_package_tree_preserves_authored_bytes_and_has_no_defaults(tmp_path: Path) -> None:
    """Synthetic package support copies explicit bytes without adding schema or IDs."""
    root = tmp_path / "package"
    files = {"nested/schema.json": b'{"required": ["authored"]}', "template.jinja2": b"\x00\r\n"}
    assert write_package_tree(root, files) == root
    assert {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    } == files


def test_support_rejects_ambient_or_escaping_roots(tmp_path: Path) -> None:
    """Caller omissions cannot silently acquire CWD or a sibling server directory."""
    with pytest.raises(ValueError, match="absolute parent"):
        create_suite_roots(Path("relative"), "server")
    with pytest.raises(ValueError, match="absolute package"):
        write_package_tree(Path("relative"), {})
    with pytest.raises(ValueError, match="relative directory"):
        create_suite_roots(tmp_path, "../escape")
    assert not (tmp_path.parent / "escape").exists()


def test_delivered_suite_preserves_workflow_plugin_contract(
    legacy_suite_roots: SuiteRoots, feature_phases: list[str], pytestconfig: pytest.Config
) -> None:
    """The real isolated loader retains existing workflow fixture semantics."""
    source = pytestconfig.rootpath / legacy_suite_roots.server.name
    loader = ConfigLoader(legacy_suite_roots.config, legacy_suite_roots.templates)
    assert loader.load_contracts_config().get_phases("feature") == feature_phases
    assert legacy_suite_roots.config != source / "config"
    assert legacy_suite_roots.templates != source / "templates"
    assert (legacy_suite_roots.config / "contracts.yaml").read_bytes() == (
        source / "config" / "contracts.yaml"
    ).read_bytes()


def test_existing_directory_link_cannot_escape_before_any_creation(tmp_path: Path) -> None:
    """A real junction or symlink cannot redirect suite creation into another workspace."""
    workspace = tmp_path / "workspace"
    outside = tmp_path / "outside"
    workspace.mkdir()
    outside.mkdir()
    link = workspace / "server"
    if os.name == "nt":
        subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link), str(outside)],
            check=True,
            capture_output=True,
        )
    else:
        link.symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError, match="inside the selected workspace"):
        create_suite_roots(workspace, "server")
    assert not list(outside.iterdir())
    assert list(workspace.iterdir()) == [link]
