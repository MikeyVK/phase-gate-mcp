# mcp_server\utils\mcp_converters.py
# template=generic version=f35abd82 created=2026-06-11T06:55Z updated=2026-06-11T06:57Z
"""McpConverters module.

MCP response converter utilities

@layer: MCP Server
@dependencies: [None]
@responsibilities:
    - Convert ToolResult to MCP content or result
"""

from __future__ import annotations

import json
from typing import Any, cast

from mcp.types import (
    CallToolResult,
    EmbeddedResource,
    ImageContent,
    TextContent,
)

from mcp_server.tools.tool_result import ToolResult


def convert_tool_result_to_content(
    content_list: list[dict[str, Any]],
) -> list[TextContent | ImageContent | EmbeddedResource]:
    """Convert list of content dicts to MCP content list."""
    response_content: list[TextContent | ImageContent | EmbeddedResource] = []

    for content in content_list:
        if content.get("type") == "text":
            text = content["text"]
            response_content.append(TextContent(type="text", text=text))
        elif content.get("type") == "json":
            # Fallback for text conversion
            response_content.append(
                TextContent(
                    type="text",
                    text=json.dumps(content["json"], indent=2, default=str),
                )
            )
        elif content.get("type") == "image":
            response_content.append(
                ImageContent(type="image", data=content["data"], mimeType=content["mimeType"])
            )
        elif content.get("type") == "resource":
            response_content.append(EmbeddedResource(type="resource", resource=content["resource"]))

    return response_content


def convert_tool_result_to_mcp_result(result: ToolResult) -> CallToolResult:
    """Convert ToolResult to CallToolResult while extracting JSON data to structuredContent."""
    json_blocks = [c for c in result.content if c.get("type") == "json"]
    if len(json_blocks) > 1:
        raise ValueError("Multiple JSON content blocks found in ToolResult")

    structured_content = None
    if json_blocks:
        structured_content = json_blocks[0]["json"]

    # Keep JSON blocks in content list for clients that do not support structuredContent
    filtered_content = [c for c in result.content if c.get("type") != "json"]
    mcp_content = convert_tool_result_to_content(filtered_content)

    # QUICKFIX: If structured JSON is present, embed it as a markdown JSON code block
    # in the text content block so the model can read it!
    if structured_content is not None:
        json_dump_str = json.dumps(structured_content, indent=2, default=str)
        markdown_json = f"\n\n```json\n{json_dump_str}\n```"

        # Find the first TextContent block and append to it
        text_content_blocks = [c for c in mcp_content if isinstance(c, TextContent)]
        if text_content_blocks:
            text_content_blocks[0].text += markdown_json
        else:
            mcp_content.append(TextContent(type="text", text=markdown_json))

    return CallToolResult(
        content=cast(list[Any], mcp_content),
        isError=result.is_error,
        structuredContent=structured_content,
    )
