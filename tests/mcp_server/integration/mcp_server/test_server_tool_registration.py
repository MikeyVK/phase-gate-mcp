"""Verify supported MCP operations through the public registered tool contract."""

import pytest

from mcp_server.server import MCPServer


@pytest.mark.parametrize(
    "name",
    ["scaffold_artifact", "transition_cycle", "force_cycle_transition", "get_work_context"],
)
def test_supported_tool_is_registered_with_public_input_contract(
    server: MCPServer, name: str
) -> None:
    tools = [tool for tool in server.tools if tool.name == name]
    assert len(tools) == 1
    assert tools[0].input_schema["type"] == "object"
    assert isinstance(tools[0].input_schema["properties"], dict)
