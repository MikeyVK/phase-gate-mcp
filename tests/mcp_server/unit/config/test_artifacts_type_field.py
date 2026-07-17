"""Unit tests for artifacts.yaml type field.

Validates:
- ALL artifacts in .pgmcp/config/artifacts.yaml have type field (code|doc|config)
- Code artifacts (dto, worker, adapter, tool, resource, etc.) have type: code
- Document artifacts (research, planning, design, etc.) have type: doc

@layer: Tests (Unit)
@dependencies: pytest, mcp_server.config.schemas.artifact_registry_config
"""

from pathlib import Path

import pytest

from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas import ArtifactRegistryConfig, ArtifactType


@pytest.fixture
def artifacts_config() -> ArtifactRegistryConfig:
    """Load config from actual .pgmcp/config/artifacts.yaml."""
    from mcp_server.config.settings import Settings  # noqa: PLC0415

    settings = Settings.from_env()
    config_root = Path(settings.server.resolved_config_root)
    template_root = Path(settings.server.resolved_template_root)
    artifacts_yaml = template_root / "config" / "artifacts.yaml"
    loader = ConfigLoader(config_root, template_root=template_root)
    return loader.load_artifact_registry_config(config_path=artifacts_yaml)


class TestArtifactsTypeField:
    """Test type field validation for all artifacts (Issue #72, Cycle 1)."""

    def test_all_artifacts_have_type_field(self, artifacts_config: ArtifactRegistryConfig) -> None:
        """All artifacts must have type field (code|doc|config)."""
        # RED: Every artifact must have a type field
        for artifact in artifacts_config.artifact_types:
            assert hasattr(artifact, "type"), f"Artifact {artifact.type_id} missing 'type' field"
            assert artifact.type in [
                ArtifactType.CODE,
                ArtifactType.DOC,
                ArtifactType.TRACKING,
            ], (
                f"Artifact {artifact.type_id} has invalid type: "
                f"{artifact.type} (expected CODE|DOC|TRACKING)"
            )

    def test_code_artifacts_have_correct_type(
        self, artifacts_config: ArtifactRegistryConfig
    ) -> None:
        """Code artifacts must have type: code."""
        # RED: Assert all known code artifacts have type=CODE
        code_type_ids = [
            "dto",
            "worker",
            "adapter",
            "tool",
            "resource",
            "interface",
            "schema",
            "service",
        ]
        for type_id in code_type_ids:
            artifact = artifacts_config.get_artifact(type_id)
            if artifact:  # Skip if artifact doesn't exist yet
                assert artifact.type == ArtifactType.CODE, (
                    f"Code artifact '{type_id}' MUST have type=CODE, got {artifact.type}"
                )

    def test_document_artifacts_have_correct_type(
        self, artifacts_config: ArtifactRegistryConfig
    ) -> None:
        """Document artifacts must have type: doc."""
        # RED: Assert all known document artifacts have type=DOC
        doc_type_ids = [
            "research",
            "planning",
            "design",
            "architecture",
            # "tracking",  # DISABLED (issue #325 - stale template)
            "reference",
        ]
        for type_id in doc_type_ids:
            artifact = artifacts_config.get_artifact(type_id)
            if artifact:  # Skip if artifact doesn't exist yet
                assert artifact.type == ArtifactType.DOC, (
                    f"Document artifact '{type_id}' MUST have type=DOC, got {artifact.type}"
                )
