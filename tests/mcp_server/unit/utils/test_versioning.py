# tests\mcp_server\unit\utils\test_versioning.py
# template=unit_test version=3d15d309 created=2026-07-17T16:40s updated=
"""
Unit tests for mcp_server.utils.versioning.

Unit tests for mcp_server.utils.versioning

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.utils.versioning, mcp_server.core.exceptions]
@responsibilities:
    - Test SemVer parsing and validation logic
    - Verify compatibility rules (major/minor/patch)
"""

# Standard library
from typing import Any
import logging

# Third-party
import pytest

# Project modules
from mcp_server.core.exceptions import ConfigError
from mcp_server.utils.versioning import SemVer, validate_compatibility


class TestSemVerValidator:
    """Test suite for SemVer parsing and validation logic."""

    @pytest.mark.parametrize(
        "version_str,expected",
        [
            ("1.0.0", SemVer(1, 0, 0)),
            ("0.1.0", SemVer(0, 1, 0)),
            ("10.20.30", SemVer(10, 20, 30)),
        ],
    )
    def test_parse_valid_versions(self, version_str: str, expected: SemVer) -> None:
        """Verify that valid SemVer strings parse correctly."""
        assert SemVer.parse(version_str) == expected

    @pytest.mark.parametrize(
        "version_str",
        [
            "1",
            "1.0",
            "1.0.a",
            "1.0.0.0",
            "v1.0.0",
            "1.0.0-beta",
            "",
            "1.0.0-0.3.7",
            " 1.0.0",
            "1.0.0 ",
        ],
    )
    def test_parse_invalid_versions_raises_config_error(self, version_str: str) -> None:
        """Verify that invalid version strings raise ConfigError."""
        with pytest.raises(ConfigError) as exc_info:
            SemVer.parse(version_str)
        assert "Invalid version format" in str(exc_info.value)

    def test_validate_compatibility_major_mismatch_raises_config_error(self) -> None:
        """Verify that a MAJOR version mismatch raises ConfigError."""
        with pytest.raises(ConfigError) as exc_info:
            validate_compatibility(expected_version="1.0.0", actual_version="2.0.0", context="test_major")
        assert "MAJOR version mismatch" in str(exc_info.value)

    def test_validate_compatibility_minor_newer_warning(self, caplog: pytest.LogCaptureFixture) -> None:
        """Verify that a newer MINOR version logs a Warning but passes."""
        with caplog.at_level(logging.WARNING):
            validate_compatibility(expected_version="1.1.0", actual_version="1.2.0", context="test_minor_newer")
        
        # Verify warning log
        assert len(caplog.records) == 1
        assert caplog.records[0].levelno == logging.WARNING
        assert "MINOR version mismatch" in caplog.text
        assert "test_minor_newer" in caplog.text

    @pytest.mark.parametrize(
        "expected,actual",
        [
            ("1.2.0", "1.1.0"),  # Older minor version is accepted
            ("1.2.0", "1.2.0"),  # Equal minor version
        ],
    )
    def test_validate_compatibility_minor_older_or_equal_passes_silently(
        self, expected: str, actual: str, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Verify that older or equal MINOR version passes silently without warnings."""
        with caplog.at_level(logging.WARNING):
            validate_compatibility(expected_version=expected, actual_version=actual, context="test_minor_ok")
        assert len(caplog.records) == 0

    @pytest.mark.parametrize(
        "expected,actual",
        [
            ("1.1.1", "1.1.2"),  # Newer patch version
            ("1.1.2", "1.1.1"),  # Older patch version
            ("1.1.1", "1.1.1"),  # Equal patch version
        ],
    )
    def test_validate_compatibility_patch_mismatch_passes_silently(
        self, expected: str, actual: str, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Verify that any patch version mismatch passes silently without warnings."""
        with caplog.at_level(logging.WARNING):
            validate_compatibility(expected_version=expected, actual_version=actual, context="test_patch")
        assert len(caplog.records) == 0
