# tests/mcp_server/unit/test_build_package.py
"""Behavior contracts for bounded, fail-closed release asset assembly."""

from __future__ import annotations

import logging
import os
import subprocess
from pathlib import Path
from unittest.mock import Mock

import pytest
import yaml

from scripts import build_package as builder


@pytest.fixture
def assembly_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Prepare only scratch inputs, generated output and a recovery sentinel."""
    root = tmp_path / "project"
    inputs = root / "input"
    inputs.mkdir(parents=True)
    (inputs / "data.txt").write_text("required", encoding="utf-8")
    (inputs / ".version").write_text("1.0.0\n", encoding="utf-8")
    config = root / ".pgmcp/config"
    config.mkdir(parents=True)
    (root / ".pgmcp/state.json").write_text("preserve", encoding="utf-8")
    (config / "release_manifest.yaml").write_text(
        yaml.safe_dump({"assets": [{"source": "input", "target": "bundle"}]}),
        encoding="utf-8",
    )
    assets = root / "mcp_server/assets"
    assets.mkdir(parents=True)
    (assets / "stale.txt").write_text("old", encoding="utf-8")
    monkeypatch.setattr(builder, "__file__", str(root / "scripts/build_package.py"))
    return root


def directory_link(link: Path, target: Path) -> None:
    """Create a real scratch directory link, using a Windows junction if needed."""
    try:
        link.symlink_to(target, target_is_directory=True)
    except OSError:
        if os.name != "nt":
            raise
        subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link), str(target)],
            check=True,
            capture_output=True,
        )


def test_clean_assets_clears_directory(tmp_path: Path) -> None:
    assets = tmp_path / "assets"
    (assets / "nested").mkdir(parents=True)
    (assets / "nested/file.txt").write_text("old", encoding="utf-8")
    (assets / "loose.txt").write_text("old", encoding="utf-8")

    builder.clean_assets(assets)

    assert assets.is_dir()
    assert list(assets.iterdir()) == []


def test_read_manifest_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        builder.read_manifest(tmp_path / "missing.yaml")


def test_read_manifest_preserves_valid_metadata(tmp_path: Path) -> None:
    manifest = {"version": "1.0.0", "assets": [{"source": "input", "target": "bundle"}]}
    path = tmp_path / "release_manifest.yaml"
    path.write_text(yaml.safe_dump(manifest), encoding="utf-8")

    assert builder.read_manifest(path) == manifest


@pytest.mark.parametrize(
    "manifest",
    [
        None,
        {},
        {"assets": []},
        {"assets": {}},
        {"assets": ["not a mapping"]},
        {"assets": [{"source": "input"}]},
        {"assets": [{"source": 7, "target": "bundle"}]},
        {"assets": [{"source": "input", "target": "  "}]},
    ],
    ids=[
        "top-level",
        "absent",
        "empty",
        "collection-type",
        "record-type",
        "required",
        "field-type",
        "blank",
    ],
)
def test_invalid_manifest_preserves_output_and_blocks_build(
    assembly_root: Path, monkeypatch: pytest.MonkeyPatch, manifest: object
) -> None:
    path = assembly_root / ".pgmcp/config/release_manifest.yaml"
    path.write_text(yaml.safe_dump(manifest), encoding="utf-8")
    build = Mock()
    monkeypatch.setattr(builder.subprocess, "run", build)

    with pytest.raises(ValueError):
        builder.build_package()

    assert (assembly_root / "mcp_server/assets/stale.txt").read_text() == "old"
    assert (assembly_root / ".pgmcp/state.json").read_text() == "preserve"
    build.assert_not_called()


def test_direct_copy_admits_all_records_before_writing(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "input.txt").write_text("required", encoding="utf-8")
    output = tmp_path / "staging/assets"
    manifest = {
        "assets": [{"source": "input.txt", "target": "copied.txt"}, {"source": "input.txt"}]
    }

    with pytest.raises(ValueError, match="target"):
        builder.copy_assets(source, output, manifest)

    assert not output.exists()


def test_missing_source_blocks_cleanup_and_build(
    assembly_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = {
        "assets": [
            {"source": "input", "target": "bundle"},
            {"source": "missing", "target": "other"},
        ]
    }
    (assembly_root / ".pgmcp/config/release_manifest.yaml").write_text(
        yaml.safe_dump(manifest), encoding="utf-8"
    )
    build = Mock()
    monkeypatch.setattr(builder.subprocess, "run", build)

    with pytest.raises(FileNotFoundError, match="missing"):
        builder.build_package()

    assert (assembly_root / "mcp_server/assets/stale.txt").read_text() == "old"
    build.assert_not_called()


@pytest.mark.parametrize("side", ["source", "target"])
@pytest.mark.parametrize("kind", ["parent", "absolute"])
def test_copy_refuses_paths_outside_roots(tmp_path: Path, side: str, kind: str) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "input.txt").write_text("replacement", encoding="utf-8")
    outside = tmp_path / "outside.txt"
    outside.write_text("preserve", encoding="utf-8")
    output = tmp_path / "assets"
    mapping = {"source": "input.txt", "target": "copied.txt"}
    mapping[side] = "../outside.txt" if kind == "parent" else str(outside)

    with pytest.raises(ValueError):
        builder.copy_assets(source, output, {"assets": [mapping]})

    assert outside.read_text() == "preserve"
    assert not output.exists()


@pytest.mark.parametrize("inside_output", [False, True], ids=["source-contains", "source-inside"])
def test_copy_refuses_source_output_overlap(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, inside_output: bool
) -> None:
    root = tmp_path / "project"
    output = root / "assets"
    output.mkdir(parents=True)
    (output / "preserve.txt").write_text("preserve", encoding="utf-8")
    source = "assets/preserve.txt" if inside_output else "."
    # Admission must refuse overlap before a directory copy can recurse into itself.
    copy = Mock()
    monkeypatch.setattr(builder.shutil, "copytree", copy)

    with pytest.raises(ValueError):
        builder.copy_assets(root, output, {"assets": [{"source": source, "target": "copy"}]})

    assert (output / "preserve.txt").read_text() == "preserve"


@pytest.mark.parametrize("linked_side", ["source", "output", "output-child"])
def test_links_cannot_redirect_reads_or_cleanup(tmp_path: Path, linked_side: str) -> None:
    outside = tmp_path / "outside"
    outside.mkdir()
    sentinel = outside / "sentinel.txt"
    sentinel.write_text("preserve", encoding="utf-8")
    root = tmp_path / "project"
    root.mkdir()
    output = tmp_path / "assets"
    link = root / "linked" if linked_side == "source" else output
    if linked_side == "output-child":
        output.mkdir()
        (output / "stale.txt").write_text("old", encoding="utf-8")
        link = output / "linked"
    directory_link(link, outside)
    try:
        with pytest.raises(ValueError):
            if linked_side == "source":
                builder.copy_assets(
                    root, output, {"assets": [{"source": "linked", "target": "copy"}]}
                )
            else:
                builder.clean_assets(output)
        assert sentinel.read_text() == "preserve"
        if linked_side == "output-child":
            assert (output / "stale.txt").read_text() == "old"
    finally:
        if link.is_symlink():
            link.unlink()
        else:
            link.rmdir()


def test_copy_refuses_hardlinked_output(tmp_path: Path) -> None:
    root = tmp_path / "project"
    root.mkdir()
    (root / "input.txt").write_text("replacement", encoding="utf-8")
    outside = tmp_path / "outside.txt"
    outside.write_text("preserve", encoding="utf-8")
    output = tmp_path / "assets"
    output.mkdir()
    (output / "copy.txt").hardlink_to(outside)

    with pytest.raises(ValueError):
        builder.copy_assets(
            root, output, {"assets": [{"source": "input.txt", "target": "copy.txt"}]}
        )

    assert outside.read_text() == "preserve"


@pytest.mark.parametrize("directory", [False, True], ids=["unlink", "rmtree"])
def test_cleanup_failure_keeps_original_diagnosis(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, directory: bool
) -> None:
    output = tmp_path / "assets"
    output.mkdir()
    item = output / "old"
    if directory:
        item.mkdir()
        (item / "child.txt").write_text("old", encoding="utf-8")
    else:
        item.write_text("old", encoding="utf-8")
    failure = PermissionError("injected required cleanup denial")
    if directory:
        monkeypatch.setattr(builder.shutil.os, "unlink", Mock(side_effect=failure))
    else:
        monkeypatch.setattr(Path, "unlink", Mock(side_effect=failure))

    with pytest.raises(PermissionError) as caught:
        builder.clean_assets(output)

    assert caught.value is failure
    assert any("clean" in note and str(item) in note for note in failure.__notes__)
    assert item.exists()


@pytest.mark.parametrize("operation", ["cleanup", "copy"])
def test_io_failure_blocks_success_and_build(
    assembly_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
    operation: str,
) -> None:
    failure = PermissionError("injected assembly denial")
    if operation == "cleanup":
        monkeypatch.setattr(Path, "unlink", Mock(side_effect=failure))
    else:
        monkeypatch.setattr(builder.shutil, "copytree", Mock(side_effect=failure))
    build = Mock()
    monkeypatch.setattr(builder.subprocess, "run", build)

    with caplog.at_level(logging.INFO), pytest.raises(PermissionError) as caught:
        builder.build_package()

    assert caught.value is failure
    assert any(operation in note for note in failure.__notes__)
    assert (assembly_root / ".pgmcp/state.json").read_text() == "preserve"
    assert "Assets compiled successfully" not in caplog.text
    build.assert_not_called()


def test_valid_external_staging_preserves_nested_dotfiles(tmp_path: Path) -> None:
    root = tmp_path / "project"
    inputs = root / "input/nested"
    inputs.mkdir(parents=True)
    (inputs / ".version").write_text("1.0.0\n", encoding="utf-8")
    output = tmp_path / "separate_stage/mcp_server/assets"

    builder.copy_assets(root, output, {"assets": [{"source": "input", "target": "bundle"}]})

    assert (output / "bundle/nested/.version").read_text() == "1.0.0\n"


def test_valid_assembly_copies_before_build(
    assembly_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    output = assembly_root / "mcp_server/assets"

    def observe_build(command: list[str], *, cwd: str, check: bool) -> None:
        assert command == [builder.sys.executable, "-m", "build"]
        assert cwd == str(assembly_root)
        assert check is True
        assert not (output / "stale.txt").exists()
        assert (output / "bundle/data.txt").read_text() == "required"
        assert (output / "bundle/.version").read_text() == "1.0.0\n"

    build = Mock(side_effect=observe_build)
    monkeypatch.setattr(builder.subprocess, "run", build)

    builder.build_package()

    build.assert_called_once()
    assert (assembly_root / ".pgmcp/state.json").read_text() == "preserve"
