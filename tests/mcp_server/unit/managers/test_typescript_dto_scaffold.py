# tests\mcp_server\unit\managers\test_typescript_dto_scaffold.py
# template=unit_test version=3d15d309 created=2026-07-15T21:39Z updated=
"""
Unit tests for mcp_server.managers.artifact_manager.

Test scaffolding of TypeScript DTO artifact.

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.managers.artifact_manager]
@responsibilities:
    - Test TestTypeScriptDTOScaffold functionality
    - Verify None
    - None
"""

# Standard library
from typing import Any

# Third-party
import pytest
from pathlib import Path
from pydantic import ValidationError

# Project modules
from mcp_server.managers.artifact_manager import ArtifactManager


class TestTypeScriptDTOScaffold:
    """Test suite for artifact_manager."""

    @pytest.mark.asyncio
    async def test_scaffold_typescript_dto(self, tmp_path: Path) -> None:
        """Test scaffolding of a TypeScript DTO using the tiered template structure."""
        # Arrange
        workspace_root = tmp_path / "workspace"
        config_root = workspace_root / ".pgmcp" / "config"
        templates_dir = workspace_root / ".pgmcp" / "templates"
        concrete_dir = templates_dir / "concrete"

        # Create directories
        config_root.mkdir(parents=True)
        concrete_dir.mkdir(parents=True)

        # Write index configuration file
        (config_root / "artifacts.yaml").write_text("version: '1.0.0'\nartifact_types: []\n", encoding="utf-8")
        (config_root / "git.yaml").write_text("branch_types: []\n", encoding="utf-8")
        (config_root / "project_structure.yaml").write_text("version: '1.0.0'\nbase_path: '.'\n", encoding="utf-8")

        # Create artifacts/ directory with typescript_dto.yaml
        artifacts_dir = config_root / "artifacts"
        artifacts_dir.mkdir(parents=True)
        
        dto_yaml = (
            "type: code\n"
            "type_id: typescript_dto\n"
            "name: TypeScript DTO\n"
            "description: TypeScript DTO class\n"
            "output_type: file\n"
            "scaffolder_class: GenericScaffolder\n"
            "scaffolder_module: mcp_server.scaffolders.generic_scaffolder\n"
            "template_path: concrete/typescript_dto.ts.jinja2\n"
            "fallback_template: null\n"
            "name_suffix: null\n"
            "file_extension: .ts\n"
            "generate_test: false\n"
            "base_path: src/dtos/\n"
            "context_schema:\n"
            "  fields:\n"
            "    type: array\n"
            "    title: Fields\n"
            "    description: List of DTO properties\n"
            "    required: true\n"
            "    items:\n"
            "      type: object\n"
            "      properties:\n"
            "        name:\n"
            "          type: string\n"
            "        type:\n"
            "          type: string\n"
            "        readonly:\n"
            "          type: boolean\n"
            "  implements:\n"
            "    type: string\n"
            "    title: Implements interface\n"
            "    description: Optional interface to implement\n"
            "    required: false\n"
            "state_machine:\n"
            "  states: [CREATED]\n"
            "  initial_state: CREATED\n"
            "  valid_transitions: []\n"
        )
        (artifacts_dir / "typescript_dto.yaml").write_text(dto_yaml, encoding="utf-8")

        # Write tiered templates
        tier0_content = (
            "{% if format == 'typescript' %}\n"
            "// template={{ artifact_type }} version={{ version_hash }}\n"
            "{% endif %}\n"
            "{% block content %}{% endblock %}\n"
        )
        (templates_dir / "tier0_base_artifact.jinja2").write_text(tier0_content, encoding="utf-8")

        tier1_content = (
            "{% extends 'tier0_base_artifact.jinja2' %}\n"
            "{% block content %}\n"
            "{% block module_docstring %}{% endblock %}\n"
            "{% block imports_section %}{% endblock %}\n"
            "{% block class_structure %}{% endblock %}\n"
            "{% endblock %}\n"
        )
        (templates_dir / "tier1_base_code.jinja2").write_text(tier1_content, encoding="utf-8")

        tier2_content = (
            "{% extends 'tier1_base_code.jinja2' %}\n"
            "{% set format = 'typescript' %}\n"
            "{% block module_docstring %}\n"
            "/**\n"
            " * {{ test_description | default('TypeScript DTO') }}\n"
            " */\n"
            "{% endblock %}\n"
            "{% block class_structure %}\n"
            "export class {{ name }} {%%\n"
            "  {% block class_body %}{% endblock %}\n"
            "}\n"
            "{% endblock %}\n"
        )
        # Note: replace {%% with {% to avoid jinja escaping issues during template writing
        tier2_content = tier2_content.replace("{%%", "{%")
        (templates_dir / "tier2_base_typescript.jinja2").write_text(tier2_content, encoding="utf-8")

        tier3_content = (
            "{% extends 'tier2_base_typescript.jinja2' %}\n"
            "{% block class_body %}\n"
            "{% for field in fields %}\n"
            "  public {% if field.readonly %}readonly {% endif %}{{ field.name }}: {{ field.type }};\n"
            "{% endfor %}\n"
            "{% endblock %}\n"
        )
        (templates_dir / "tier3_pattern_typescript_dto.jinja2").write_text(tier3_content, encoding="utf-8")

        concrete_content = (
            "{% extends 'tier3_pattern_typescript_dto.jinja2' %}\n"
        )
        (concrete_dir / "typescript_dto.ts.jinja2").write_text(concrete_content, encoding="utf-8")

        # Initialize manager
        manager = make_artifact_manager(workspace_root)

        # Act
        result = await manager.scaffold_artifact(
            artifact_type="typescript_dto",
            output_path="src/dtos/user.ts",
            name="UserDTO",
            fields=[
                {"name": "id", "type": "string", "readonly": True},
                {"name": "name", "type": "string", "readonly": False}
            ]
        )

        # Assert
        assert result.file_name == "user.ts"
        content = result.content
        assert "template=typescript_dto" in content
        assert "export class UserDTO" in content
        assert "public readonly id: string;" in content
        assert "public name: string;" in content
