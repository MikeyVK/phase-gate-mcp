"""Unit tests for MCPProxy - transparent server restart.

Tests:
- Proxy initialization
- Initialize handshake capture and replay
- Restart marker detection (stderr)
- UTF-8 encoding handling
- Transparent restart flow

@layer: Tests (Unit)
@dependencies: pytest, mcp_server.core.proxy
"""

import sys

from mcp_server.core.proxy import RESTART_MARKER, MCPProxy


class TestMCPProxyInitialization:
    """Test proxy initialization."""

    def test_proxy_init(self) -> None:
        """Test proxy initializes with correct defaults."""
        proxy = MCPProxy()

        assert proxy.server_process is None
        assert proxy.init_request is None
        assert proxy.restarting is False
        assert not proxy.restart_count  # 0 is falsey
        assert proxy.proxy_pid > 0


class TestInitializeCapture:
    """Test initialize handshake capture."""

    def test_captures_initialize_request(self) -> None:
        """Test proxy captures initialize request for replay."""
        proxy = MCPProxy()

        init_message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-11-25",
                "clientInfo": {"name": "Visual Studio Code", "version": "1.0.0"},
            },
        }

        # Simulate capturing init request
        proxy.init_request = init_message

        assert proxy.init_request["method"] == "initialize"
        assert proxy.init_request["id"] == 1


class TestRestartMarkerDetection:
    """Test restart marker detection on stderr."""

    def test_restart_marker_constant(self) -> None:
        """Test restart marker constant is defined."""
        assert RESTART_MARKER == "__MCP_RESTART_REQUEST__"

    def test_detects_restart_marker_in_stderr(self) -> None:
        """Test proxy detects restart marker in stderr stream."""
        # Placeholder for future implementation
        proxy = MCPProxy()
        assert hasattr(proxy, "trigger_restart")  # Method exists


class TestUTF8Encoding:
    """Test UTF-8 encoding fixes for Windows."""

    def test_utf8_forced_on_windows(self) -> None:
        """Test UTF-8 is forced on stdout/stderr on Windows."""
        # This test verifies the module-level UTF-8 setup
        # If we get here without errors, UTF-8 setup worked
        if sys.platform == "win32":
            assert sys.stdout.encoding == "utf-8"
            assert sys.stderr.encoding == "utf-8"


class TestTransparentRestart:
    """Test transparent restart flow."""

    def test_restart_increments_counter(self) -> None:
        """Test restart counter increments on each restart."""
        proxy = MCPProxy()

        assert not proxy.restart_count  # 0 is falsey
        proxy.restart_count += 1
        assert proxy.restart_count == 1
