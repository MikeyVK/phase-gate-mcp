# c:\temp\pgmcp\tests\mcp_server\unit\assembly\test_bootstrap.py
# template=unit_test version=3d15d309 created=2026-06-25T19:31Z updated=
"""
Unit tests for mcp_server.bootstrap.

Tests for the bootstrap module assembly and circular import prevention.

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.bootstrap, unittest.mock]
@responsibilities:
    - Test TestBootstrapper functionality
    - Verify None
    - None
"""

# Standard library
from unittest.mock import Mock, MagicMock, AsyncMock, patch
from typing import Any

# Third-party
import pytest
from pathlib import Path

# Project modules
from mcp_server.bootstrap import ServerBootstrapper


class TestBootstrapper:
    """Test suite for bootstrap."""

    def test_main_not_in_server(self) -> None:
        """Verify that the process entrypoint main() has been removed from server.py."""
        import mcp_server.server
        assert not hasattr(mcp_server.server, "main")
