"""Exercise location routing and admission without creating artifacts."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import pytest
from pydantic import ValidationError

from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.artifact_locations import ArtifactLocationsConfig
from mcp_server.config.validator import ConfigValidator
from mcp_server.core.exceptions import ConfigError
from mcp_server.services.artifact_target_resolver import ArtifactTargetResolver
from mcp_server.utils.path_resolver import FileArtifactTargetPaths, resolve_temporary_paths


@pytest.fixture
def locations() -> ArtifactLocationsConfig:
    return ArtifactLocationsConfig.model_validate(
        {
            "version": "2.0.0",
            "artifacts": {
                "design": {"default_root": "docs", "additional_roots": ["notes\\drafts"]}
            },
        }
    )


@pytest.fixture
def resolver(tmp_path: Path, locations: ArtifactLocationsConfig) -> ArtifactTargetResolver:
    return ArtifactTargetResolver(
        paths=FileArtifactTargetPaths(tmp_path),
        temporary_artifacts_root=resolve_temporary_paths(tmp_path / "custom-server").artifacts_root,
        locations=locations,
    )


def test_default_explicit_and_temporary_routes(
    resolver: ArtifactTargetResolver, tmp_path: Path
) -> None:
    cases: tuple[tuple[str, Literal["workspace", "temporary"], str | None, bool, str], ...] = (
        ("design", "workspace", None, False, "docs"),
        ("design", "temporary", None, False, "custom-server/temp/artifacts"),
        ("unmapped", "workspace", None, False, "custom-server/temp/artifacts"),
        ("design", "workspace", "docs", False, "docs"),
        ("design", "workspace", "notes\\drafts/./nested", False, "notes/drafts/nested"),
        ("design", "workspace", "docs/scratch/../final", False, "docs/final"),
        ("design", "workspace", "other", True, "other"),
        ("unmapped", "workspace", "other", True, "other"),
        ("design", "temporary", "docs", False, "docs"),
        ("unmapped", "temporary", ".", True, "."),
    )
    filename = "MiXeD release.v2.md"
    for template_id, persistence, target_path, force_target, directory in cases:
        target = resolver.resolve(
            template_id=template_id,
            persistence=persistence,
            file_name=filename,
            target_path=target_path,
            force_target=force_target,
        )
        expected = Path(directory) / filename
        assert target.output_path == expected.as_posix()
        assert target.path == tmp_path / expected
        assert target.path.name == filename
        assert not target.path.exists()
    assert list(tmp_path.iterdir()) == []


def test_force_changes_only_location_permission(resolver: ArtifactTargetResolver) -> None:
    for template_id, target_path in (
        ("design", "docs-other"),
        ("design", "elsewhere"),
        ("unmapped", "docs"),
    ):
        with pytest.raises(ValueError, match="force_target_required"):
            resolver.resolve(
                template_id=template_id, persistence="workspace",
                file_name="result.md", target_path=target_path,
            )
    with pytest.raises(ValueError, match="force_target_requires_target_path"):
        resolver.resolve(
            template_id="unmapped", persistence="workspace",
            file_name="result.md", force_target=True,
        )
    for target_path in ("../outside", "docs/../../outside", "/absolute", "C:\\absolute", ""):
        with pytest.raises(ValueError, match="workspace_relative_path_required"):
            resolver.resolve(
                template_id="design", persistence="workspace", file_name="result.md",
                target_path=target_path, force_target=True,
            )


def test_filename_is_a_basename_and_collision_never_overwrites(
    resolver: ArtifactTargetResolver, tmp_path: Path
) -> None:
    for filename in ("", ".", "..", "nested/file.md", "nested\\file.md", "C:file.md"):
        with pytest.raises(ValueError, match="basename_required"):
            resolver.resolve(template_id="design", persistence="workspace", file_name=filename)
    existing = tmp_path / "docs" / "result.md"
    existing.parent.mkdir()
    original = b"already authored\r\n"
    existing.write_bytes(original)
    with pytest.raises(FileExistsError):
        resolver.resolve(
            template_id="design", persistence="workspace", file_name=existing.name,
            target_path="docs", force_target=True,
        )
    assert existing.read_bytes() == original


def test_loader_and_one_way_catalog_references(tmp_path: Path) -> None:
    (tmp_path / "artifacts.yaml").write_text(
        'version: "2.0.0"\nartifacts:\n  design:\n'
        '    default_root: docs/./design\n    additional_roots: [notes/drafts]\n',
        encoding="utf-8",
    )
    config = ConfigLoader(tmp_path, template_root=tmp_path).load_artifact_locations_config()
    assert config.artifacts[0][1].default_root == "docs/design"
    assert config.artifacts[0][1].additional_roots == ("notes/drafts",)
    validator = ConfigValidator()
    validator.validate_artifact_locations(config, frozenset({"design", "unmapped"}))
    with pytest.raises(ConfigError):
        validator.validate_artifact_locations(config, frozenset({"other"}))
    (tmp_path / "artifacts.yaml").write_text(
        'version: "2.0.0"\nartifacts:\n  design: {default_root: docs}\n'
        '  design: {default_root: other}\n',
        encoding="utf-8",
    )
    with pytest.raises(ConfigError):
        ConfigLoader(tmp_path, template_root=tmp_path).load_artifact_locations_config()


def test_location_config_rejects_invalid_or_duplicate_roots(
    locations: ArtifactLocationsConfig,
) -> None:
    invalid_entries: tuple[dict[str, object], ...] = (
        {"default_root": "../outside"},
        {"default_root": "C:\\outside"},
        {"default_root": "docs", "additional_roots": ["docs/./"]},
        {"default_root": "docs", "additional_roots": ["notes", "notes/"]},
        {"default_root": "docs", "temporary_root": "temp"},
    )
    for entry in invalid_entries:
        with pytest.raises(ValidationError):
            ArtifactLocationsConfig.model_validate(
                {"version": "2.0.0", "artifacts": {"design": entry}}
            )
    with pytest.raises(ValidationError):
        locations.artifacts[0][1].default_root = "changed"
    assert locations.artifacts[0][1].default_root == "docs"


def test_dangling_output_entry_is_a_collision(
    resolver: ArtifactTargetResolver, tmp_path: Path
) -> None:
    directory = tmp_path / "docs"
    directory.mkdir()
    target = directory / "requested.md"
    referent = directory / "missing.md"
    target.symlink_to(referent)
    with pytest.raises(FileExistsError):
        resolver.resolve(
            template_id="design", persistence="workspace", file_name=target.name,
            target_path="docs", force_target=True,
        )
    assert target.is_symlink()
    assert target.readlink() == referent
    assert not referent.exists()
