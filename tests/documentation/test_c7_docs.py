# tests\documentation\test_c7_docs.py
# template=unit_test version=3d15d309 created=2026-07-08T05:42Z updated=
"""Unit tests for verifying developer isolation documentation.

@layer: Tests (Unit)
@dependencies: [pytest]
@responsibilities:
    - Verify developer isolation documentation exists and contains required sections
"""

# Standard library
from pathlib import Path

# Third-party
import pytest


class TestC7Docs:
    """Test suite for verifying Developer Isolation Documentation."""

    def test_dev_isolation_docs_exist_and_valid(self) -> None:
        """The developer isolation document must exist and contain key required sections."""
        project_root = Path(__file__).resolve().parents[2]
        docs_file = project_root / "docs" / "setup" / "dev-isolation.md"

        # Check existence
        assert docs_file.exists(), "docs/setup/dev-isolation.md does not exist"

        # Check content structure
        content = docs_file.read_text(encoding="utf-8")
        assert "# Developer Isolation" in content, "Missing title header"
        assert "## Introduction" in content or "## Purpose" in content, "Missing Introduction/Purpose section"
        assert "## Architecture" in content, "Missing Architecture section"
        assert "mermaid" in content, "Missing Mermaid architecture diagram"
        assert "## Step-by-Step" in content or "## Setup" in content, "Missing Setup section"
        assert "## Environment Variables" in content, "Missing Environment Variables section"
        assert "## Development Workflow" in content, "Missing Development Workflow section"
