# scripts\build_package.py
# template=generic version=f35abd82 created=2026-07-08T05:30Z updated=
"""BuildPackage module.

Build-Time Packaging Automation

@layer: Build
@dependencies: [pathlib, shutil, yaml]
@responsibilities:
    - Compile release assets
    - Trigger build tool
"""

# Standard library
import logging
from pathlib import Path
import shutil
import subprocess
from typing import Any, Dict

# Third-party
import yaml

logger = logging.getLogger(__name__)


def clean_assets(assets_dir: Path) -> None:
    """Cleans the assets directory."""
    if assets_dir.exists():
        for item in assets_dir.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
    else:
        assets_dir.mkdir(parents=True, exist_ok=True)


def read_manifest(manifest_path: Path) -> Dict[str, Any]:
    """Reads the release manifest."""
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest file not found: {manifest_path}")
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError("Manifest content must be a dictionary")
    return data


def copy_assets(project_root: Path, assets_dir: Path, manifest: Dict[str, Any]) -> None:
    """Copies assets from manifest to assets directory."""
    for mapping in manifest.get("assets", []):
        src_rel = mapping.get("source")
        tgt_rel = mapping.get("target")
        if not src_rel or not tgt_rel:
            continue
        src_path = project_root / src_rel
        if not src_path.exists():
            raise FileNotFoundError(f"Source path does not exist: {src_path}")
        tgt_path = assets_dir / tgt_rel
        tgt_path.parent.mkdir(parents=True, exist_ok=True)
        if src_path.is_dir():
            shutil.copytree(src_path, tgt_path)
        else:
            shutil.copy2(src_path, tgt_path)


def build_package() -> None:
    """Orchestrates asset compilation and runs the build tool."""
    project_root = Path(__file__).parent.parent.resolve()
    manifest_path = project_root / ".pgmcp" / "config" / "release_manifest.yaml"
    assets_dir = project_root / "mcp_server" / "assets"

    manifest = read_manifest(manifest_path)
    clean_assets(assets_dir)
    copy_assets(project_root, assets_dir, manifest)

    logger.info("Assets compiled successfully. Running package build...")
    subprocess.run(["python", "-m", "build"], cwd=str(project_root), check=True)


if __name__ == "__main__":
    build_package()
