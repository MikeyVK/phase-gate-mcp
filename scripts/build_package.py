# scripts/build_package.py
"""Compile manifest-declared release assets, then invoke the package build."""

from __future__ import annotations

import logging
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


def _asset_mappings(manifest: object) -> tuple[tuple[str, str], ...]:
    """Admit the current manifest shape without transforming its metadata."""
    if not isinstance(manifest, dict):
        raise ValueError("Manifest content must be a dictionary")
    assets = manifest.get("assets")
    if not isinstance(assets, list) or not assets:
        raise ValueError("Manifest assets must be a nonempty list")
    mappings: list[tuple[str, str]] = []
    for index, mapping in enumerate(assets):
        if not isinstance(mapping, dict):
            raise ValueError(f"Manifest assets[{index}] must be a mapping")
        source, target = mapping.get("source"), mapping.get("target")
        if not isinstance(source, str) or not source.strip():
            raise ValueError(f"Manifest assets[{index}].source must be a nonblank string")
        if not isinstance(target, str) or not target.strip():
            raise ValueError(f"Manifest assets[{index}].target must be a nonblank string")
        mappings.append((source, target))
    return tuple(mappings)


def _node_info(path: Path) -> os.stat_result | None:
    """Inspect an endpoint without following a link or Windows reparse point."""
    try:
        info = path.lstat()
    except FileNotFoundError:
        return None
    if stat.S_ISLNK(info.st_mode) or (
        os.name == "nt" and info.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT
    ):
        raise ValueError(f"Linked asset path is not allowed: {path}")
    return info


def _inspect_tree(root: Path, *, output: bool = False) -> None:
    """Refuse indirect paths before traversing the explicit source/output tree."""
    for component in (root, *root.parents):
        _node_info(component)
    pending = [root]
    while pending:
        path = pending.pop()
        info = _node_info(path)
        if info is None:
            continue
        if stat.S_ISDIR(info.st_mode):
            pending.extend(path.iterdir())
        elif not stat.S_ISREG(info.st_mode):
            raise ValueError(f"Unsupported asset filesystem node: {path}")
        elif output and info.st_nlink > 1:
            raise ValueError(f"Hardlinked asset output is not allowed: {path}")


def _relative_path(value: str, *, index: int, field: str) -> Path:
    path = Path(value)
    if path.anchor or ".." in path.parts or (field == "target" and path == Path(".")):
        raise ValueError(f"Manifest assets[{index}].{field} must stay within its root: {value}")
    return path


def _prepare_assets(
    project_root: Path, assets_dir: Path, manifest: dict[str, Any]
) -> tuple[tuple[Path, Path], ...]:
    """Admit every mapping and filesystem boundary before any output mutation."""
    mappings = _asset_mappings(manifest)
    source_root = project_root.absolute()
    output_root = assets_dir.absolute()
    try:
        _inspect_tree(output_root, output=True)
    except OSError as exc:
        exc.add_note(f"prepare asset output: {output_root}")
        raise
    prepared: list[tuple[Path, Path]] = []
    for index, (source, target) in enumerate(mappings):
        source_path = source_root / _relative_path(source, index=index, field="source")
        target_path = output_root / _relative_path(target, index=index, field="target")
        try:
            resolved_source = source_path.resolve()
            resolved_target = target_path.resolve()
            resolved_output = output_root.resolve()
            if not resolved_source.is_relative_to(source_root.resolve()):
                raise ValueError(f"Source escapes project root: {source_path}")
            if resolved_target == resolved_output or not resolved_target.is_relative_to(
                resolved_output
            ):
                raise ValueError(f"Target escapes asset root: {target_path}")
            if resolved_source.is_relative_to(resolved_output) or resolved_output.is_relative_to(
                resolved_source
            ):
                raise ValueError(f"Source and asset output overlap: {source_path}, {output_root}")
            _inspect_tree(source_path)
            source_path.stat()  # Required sources must exist, unlike new output endpoints.
        except OSError as exc:
            exc.add_note(f"prepare assets[{index}]: source={source_path}; target={target_path}")
            raise
        prepared.append((resolved_source, resolved_target))
    return tuple(prepared)


def clean_assets(assets_dir: Path) -> None:
    """Clear only caller-designated disposable output, refusing indirect paths."""
    affected = assets_dir
    try:
        _inspect_tree(assets_dir.absolute(), output=True)
        assets_dir.mkdir(parents=True, exist_ok=True)
        for item in assets_dir.iterdir():
            affected = item
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
    except (OSError, shutil.Error) as exc:
        exc.add_note(f"cleanup asset path: {affected}")
        raise


def read_manifest(manifest_path: Path) -> dict[str, Any]:
    """Read and admit the existing release manifest, preserving native failures."""
    try:
        with manifest_path.open(encoding="utf-8") as file_handle:
            data = yaml.safe_load(file_handle)
        _asset_mappings(data)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        exc.add_note(f"read release manifest: {manifest_path}")
        raise
    return data


def _copy_prepared(prepared: tuple[tuple[Path, Path], ...]) -> None:
    for source, target in prepared:
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, target, dirs_exist_ok=True)
            else:
                shutil.copy2(source, target)
        except (OSError, shutil.Error) as exc:
            exc.add_note(f"copy asset: source={source}; target={target}")
            raise


def copy_assets(project_root: Path, assets_dir: Path, manifest: dict[str, Any]) -> None:
    """Copy all admitted mappings, including hidden members, to an explicit root."""
    _copy_prepared(_prepare_assets(project_root, assets_dir, manifest))


def build_package() -> None:
    """Validate and assemble disposable assets; build only after successful assembly."""
    project_root = Path(__file__).parent.parent.resolve()
    manifest_path = project_root / ".pgmcp" / "config" / "release_manifest.yaml"
    assets_dir = project_root / "mcp_server" / "assets"

    manifest = read_manifest(manifest_path)
    prepared = _prepare_assets(project_root, assets_dir, manifest)
    clean_assets(assets_dir)
    _copy_prepared(prepared)

    logger.info("Assets compiled successfully. Running package build...")
    subprocess.run([sys.executable, "-m", "build"], cwd=str(project_root), check=True)


if __name__ == "__main__":
    build_package()
