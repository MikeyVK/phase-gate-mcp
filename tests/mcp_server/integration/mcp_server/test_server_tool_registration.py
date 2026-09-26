"""Integration tests for MCP server tool registration.

Tests verify that the correct tools are registered in the server
and that legacy tools have been properly removed.

@layer: Tests (Integration)
@dependencies: pytest, mcp_server.server
"""

from mcp_server.server import MCPServer


def test_scaffold_artifact_tool_registered(server: MCPServer) -> None:
    """Verify ScaffoldArtifactTool is registered in server tools list."""
    tool_names = [type(getattr(t, "_tool", t)).__name__ for t in server.tools]
    assert "ScaffoldArtifactTool" in tool_names, f"ScaffoldArtifactTool not found in {tool_names}"


def test_legacy_scaffold_tools_not_registered(server: MCPServer) -> None:
    """Verify legacy scaffold tools are NOT registered."""
    tool_names = [type(getattr(t, "_tool", t)).__name__ for t in server.tools]
    assert "ScaffoldComponentTool" not in tool_names, (
        "Legacy ScaffoldComponentTool should not be registered"
    )
    assert "ScaffoldDesignDocTool" not in tool_names, (
        "Legacy ScaffoldDesignDocTool should not be registered"
    )


def test_scaffold_artifact_tool_has_correct_name(server: MCPServer) -> None:
    """Verify tool name matches expected MCP tool name."""
    scaffold_tools = [
        t for t in server.tools if type(getattr(t, "_tool", t)).__name__ == "ScaffoldArtifactTool"
    ]
    assert len(scaffold_tools) == 1, "Expected exactly one ScaffoldArtifactTool"
    tool = scaffold_tools[0]
    assert tool.name == "scaffold_artifact", f"Expected name 'scaffold_artifact', got '{tool.name}'"


def test_transition_cycle_tool_registered(server: MCPServer) -> None:
    """Verify TransitionCycleTool is registered in server tools list (Issue #146)."""
    tool_names = [type(getattr(t, "_tool", t)).__name__ for t in server.tools]
    assert "TransitionCycleTool" in tool_names, (
        f"TransitionCycleTool not found in registered tools. Registered: {tool_names}"
    )


def test_force_cycle_transition_tool_registered(server: MCPServer) -> None:
    """Verify ForceCycleTransitionTool is registered in server tools list (Issue #146)."""
    tool_names = [type(getattr(t, "_tool", t)).__name__ for t in server.tools]
    assert "ForceCycleTransitionTool" in tool_names, (
        f"ForceCycleTransitionTool not found in registered tools. Registered: {tool_names}"
    )


def test_transition_cycle_tool_has_correct_name(server: MCPServer) -> None:
    """Verify TransitionCycleTool MCP name matches expected value (Issue #146)."""
    tools = [
        t for t in server.tools if type(getattr(t, "_tool", t)).__name__ == "TransitionCycleTool"
    ]
    assert len(tools) == 1, "Expected exactly one TransitionCycleTool"
    assert tools[0].name == "transition_cycle", (
        f"Expected name 'transition_cycle', got '{tools[0].name}'"
    )


def test_force_cycle_transition_tool_has_correct_name(server: MCPServer) -> None:
    """Verify ForceCycleTransitionTool MCP name matches expected value (Issue #146)."""
    tools = [
        t
        for t in server.tools
        if type(getattr(t, "_tool", t)).__name__ == "ForceCycleTransitionTool"
    ]
    assert len(tools) == 1, "Expected exactly one ForceCycleTransitionTool"
    assert tools[0].name == "force_cycle_transition", (
        f"Expected name 'force_cycle_transition', got '{tools[0].name}'"
    )


def test_search_documentation_removed_and_get_work_context_preserved(server: MCPServer) -> None:
    """The clean-break inventory omits search while retaining workflow context."""

    tool_names = [tool.name for tool in server.tools]

    assert "search_documentation" not in tool_names
    assert "get_work_context" in tool_names
