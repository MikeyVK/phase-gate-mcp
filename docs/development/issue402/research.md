<!-- c:\temp\pgmcp\docs\development\issue402\research.md -->
<!-- template=research version=8b7bb3ab created=2026-06-12T05:54:00Z updated=2026-06-14T17:19:00Z -->
# Research — Issue #402: Expose JSON data in MCP tools

**Status:** APPROVED  
**Version:** 2.0  
**Last Updated:** 2026-06-14

---

## Purpose

Investigate the migration of MCP tools to structured outputs, establish a stable research nucleus for exposing JSON data via the resource cache, and resolve architectural cohesion for tool dispatch.

## Scope

**In Scope:**
- All registered MCP tools in the `mcp_server/tools/` directory.
- Standardisation of JSON output payloads for tools.
- Presentation of options for defining JSON schemas.
- Refactoring of server tool orchestration, caching, and presentation pipelines.

**Out of Scope:**
- External libraries, protocols outside MCP, or changes to client implementations.

---

## Problem Statement

Expose structured JSON data alongside human-readable text fallbacks in the responses of MCP tools (in accordance with the design contract established in #301), while maintaining strict separation of concerns between tools, caching, and presentation.

---

## Background

Initial research under Issue #301 laid the groundwork, and Issue #390 introduced `StructuredTool` and `mcp_converters.py`. Cycle 1 successfully implemented the `TextPresenter`, and Cycle 8 piloted the `AutoFixTool` with Resource Caching.

---

## Findings

### 1. Existing Behavior and Patterns
Our MCP server uses a two-tiered tool response model:
- **`BaseTool` / `BaseTool.execute`:** Returns `ToolResult.text(...)`, which produces a single content block of type `"text"`.
- **`StructuredTool` / `StructuredTool.execute_structured`:** Returns a tuple `(data_dict, summary_text)`, creating two content blocks: `"json"` and `"text"`. The server's `convert_tool_result_to_mcp_result` extracts the JSON block to `CallToolResult.structuredContent`.

### 2. Architectural Cohesion Analysis (Post Cycle 1 & 8)
After piloting the `TextPresenter` and `AutoFixTool` Resource Cache, an architectural analysis of the `MCPServer` identified severe cohesion problems:
- **God Method**: `MCPServer.handle_call_tool()` combines tool lookup, argument validation, execution, inline presenter formatting, and protocol conversion into a single method.
- **OCP Violations**: The server contains hardcoded exceptions like `skip_json=(name == "auto_fix")` to prevent caching conflicts.
- **DRY Violations**: The `MCPConverter` injects JSON as markdown via a `QUICKFIX` block, duplicating payload data.
- **Protocol Leakage**: Tools build MCP-specific `ToolResult` objects instead of pure Domain objects (DTOs).

### 3. Proposed Architectural Patterns
To solve the cohesion issues and standardize the successful Auto-Fix flow across all tools, the following architectural patterns were identified:
1. **ITool Interface (Input/Output Contracts)**: All tools must implement a strict `ITool` interface that accepts a `BaseModel` (the existing `args_model`) and returns a pure `BaseModel` DTO. No `ToolResult` or MCP-specifics leak into the domain tools.
2. **Resource Publishing Decorator (Caching)**: Caching is an application state concern. A decorator wraps the base tool, executing the cache insertion and generating a `run_id` without polluting the core tool's logic.
3. **ToolFactory (Composition Root)**: A factory centralizes the creation and decoration of tools, returning fully assembled `ITool` instances to the server via Dependency Injection.
4. **Envelope Pattern**: To prevent mutating immutable (`frozen=True`) domain DTOs with a `run_id`, the decorator returns a `ToolExecutionEnvelope(run_id, data)` containing the pure DTO and the infrastructure metadata.
5. **Server Orchestration (MVP Pattern)**: The `MCPServer` acts as the Controller: it executes the Tool (Model), passes the Envelope to the `TextPresenter` (Presenter), and returns the formatted Markdown (View). 

### 4. The structuredContent Resolution
The initial plan to expose JSON via MCP's `structuredContent` caused the `skip_json` and `QUICKFIX` hacks. 
**Finding**: By entirely dropping `structuredContent` (JSON) from the MCP response, the MCP response becomes ultra-lightweight pure Text. The LLM relies on the `pgmcp://cache/runs/{{run_id}}` URI in the text to fetch the deep JSON data via `read_resource`.

---

## Open Questions

None. The architectural patterns resolve the cohesion issues completely.

---

## Approved Strategy

### Boundary / consumer scope
All MCP tools in `mcp_server/tools/` without exception. The MCP Protocol Response Boundary.

### Selected strategy
1. **JSON DTO Migration**: Define Pydantic DTOs for all tool outputs.
2. **ITool Interface & MVP Orchestration**: Implement `ITool`, `ToolFactory`, and `ResourcePublishingDecorator`. Transform `MCPServer.handle_call_tool()` into a clean MVP Controller pipeline.
3. **Drop MCP structuredContent**: Completely remove JSON from the MCP `CallToolResult`. Return pure `TextContent` formatted by the Presenter. 
4. **Envelope Pattern**: Use `ToolExecutionEnvelope` to cleanly pass the `run_id` and Domain DTO to the server/presenter without mutating frozen domain models.

### Rationale
This strategy completely eliminates hardcoded OCP hacks (`skip_json`), removes duplicated JSON payloads (`QUICKFIX`), and guarantees pure, immutable domain DTOs. It cleanly separates concerns (Tool=Logic, Decorator=Cache, Presenter=View, Server=Protocol Orchestrator) while fulfilling the goal of exposing JSON data via the robust MCP Resource side-channel.