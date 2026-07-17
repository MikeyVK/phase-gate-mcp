# tests\mcp_server\unit\utils\test_template_parser.py
# template=unit_test version=3d15d309 created=2026-07-17T16:47Z updated=
"""
Unit tests for mcp_server.utils.template_parser.

Unit tests for template_parser version extraction

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.utils.template_parser, mcp_server.core.exceptions]
@responsibilities:
    - Test TestTemplateParser functionality
    - Verify template version extraction from Jinja2 templates
"""

# Standard library
from pathlib import Path

# Third-party
import pytest

# Project modules
from mcp_server.core.exceptions import ConfigError
from mcp_server.utils.template_parser import extract_template_version


class TestTemplateParser:
    """Test suite for template_parser."""

    @pytest.mark.parametrize(
        "content,expected_version",
        [
            ("{#- Version: 1.0.0 -#}\nprint('hello')", "1.0.0"),
            ("{#-Version:2.3.4-#}\nsome code", "2.3.4"),
            ("{#-   Version:   10.20.30   -#}\n", "10.20.30"),
            ("\n\n{#- Version: 0.1.0 -#}\n", "0.1.0"),
        ],
    )
    def test_extract_template_version_valid(
        self, tmp_path: Path, content: str, expected_version: str
    ) -> None:
        """Verify that valid version headers are successfully extracted."""
        temp_file = tmp_path / "template.py.jinja2"
        temp_file.write_text(content, encoding="utf-8")

        assert extract_template_version(temp_file) == expected_version

    def test_extract_template_version_missing_raises_config_error(
        self, tmp_path: Path
    ) -> None:
        """Verify that missing version header raises ConfigError."""
        temp_file = tmp_path / "template.py.jinja2"
        temp_file.write_text("print('no version')", encoding="utf-8")

        with pytest.raises(ConfigError) as exc_info:
            extract_template_version(temp_file)
        assert "Version header missing" in str(exc_info.value)

    @pytest.mark.parametrize(
        "content",
        [
            "{#- Version: 1.0 -#}",
            "{#- Version: v1.0.0 -#}",
            "{#- Version: 1.0.0-beta -#}",
            "{# Version: 1.0.0 #}",
        ],
    )
    def test_extract_template_version_invalid_raises_config_error(
        self, tmp_path: Path, content: str
    ) -> None:
        """Verify that invalid version headers raise ConfigError."""
        temp_file = tmp_path / "template.py.jinja2"
        temp_file.write_text(content, encoding="utf-8")

        with pytest.raises(ConfigError) as exc_info:
            extract_template_version(temp_file)
        assert "Version header missing" in str(exc_info.value) or "Invalid version format" in str(exc_info.value)
