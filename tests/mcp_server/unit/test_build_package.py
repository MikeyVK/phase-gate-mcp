# tests\mcp_server\unit\test_build_package.py
# template=unit_test version=3d15d309 created=2026-07-08T05:30Z updated=
"""Unit tests for scripts.build_package.

@layer: Tests (Unit)
@dependencies: [pytest, scripts.build_package]
@responsibilities:
    - Test TestBuildPackage functionality
    - Verify build-time packaging automation behavior
"""

# Standard library
from pathlib import Path

# Third-party
import pytest

# Project modules
from scripts.build_package import (
    clean_assets,
    copy_assets,
    read_manifest,
)


class TestBuildPackage:
    """Test suite for build_package."""

    def test_clean_assets_clears_directory(self, tmp_path: Path) -> None:
        """clean_assets must delete all contents in the directory but keep the directory itself."""
        assets_dir = tmp_path / "assets"
        assets_dir.mkdir()
        file_to_delete = assets_dir / "old_asset.txt"
        file_to_delete.write_text("dummy", encoding="utf-8")
        subdir = assets_dir / "subdir"
        subdir.mkdir()
        subfile = subdir / "subfile.txt"
        subfile.write_text("dummy", encoding="utf-8")

        clean_assets(assets_dir)

        assert assets_dir.exists()
        assert not file_to_delete.exists()
        assert not subdir.exists()
        assert not subfile.exists()

    def test_read_manifest_raises_file_not_found(self, tmp_path: Path) -> None:
        """read_manifest must raise FileNotFoundError if release_manifest.yaml does not exist."""
        non_existent = tmp_path / "missing_manifest.yaml"
        with pytest.raises(FileNotFoundError):
            read_manifest(non_existent)

    def test_read_manifest_returns_dict(self, tmp_path: Path) -> None:
        """read_manifest must parse release_manifest.yaml and return a dictionary."""
        manifest_file = tmp_path / "release_manifest.yaml"
        manifest_file.write_text(
            'version: "1.0.0"\nassets:\n  - source: "src_dir"\n    target: "tgt_dir"\n',
            encoding="utf-8",
        )
        data = read_manifest(manifest_file)
        assert data["version"] == "1.0.0"
        assert len(data["assets"]) == 1
        assert data["assets"][0]["source"] == "src_dir"

    def test_copy_assets_raises_file_not_found_on_missing_source(self, tmp_path: Path) -> None:
        """copy_assets must fail fast with FileNotFoundError if a source path does not exist."""
        project_root = tmp_path / "project"
        project_root.mkdir()
        assets_dir = tmp_path / "assets"
        assets_dir.mkdir()

        manifest = {
            "version": "1.0.0",
            "assets": [{"source": "non_existent_source", "target": "target_dir"}],
        }

        with pytest.raises(FileNotFoundError) as exc_info:
            copy_assets(project_root, assets_dir, manifest)
        assert "non_existent_source" in str(exc_info.value)
