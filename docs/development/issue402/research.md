<!-- c:\temp\pgmcp\docs\development\issue402\research.md -->
<!-- template=research version=8b7bb3ab created=2026-06-12T05:54:00Z updated=2026-06-13T08:30:00Z -->
# Research — Issue #402: Expose JSON data in MCP tools

**Status:** APPROVED  
**Version:** 2.0  
**Last Updated:** 2026-06-13

---

## Purpose

Investigate the migration of MCP tools to StructuredTool, address the client-side stripping of structuredContent, and research the addition of a tool-agnostic code auto-fixing capability.

## Scope

**In Scope:**
- All registered MCP tools in the `mcp_server/tools/` directory.
- Standardisation of JSON output payloads for tools.
- Resolution of the client-side `structuredContent` limitation (where the Antigravity LLM runner stript/discards `type: "json"` payloads from the chat context).
- Designing a tool-agnostic `auto_fix` tool that integrates with the existing quality gates configuration.
- Reusing the `QAManager`'s file resolution, gate filtering, and venv command execution.
- Defining explicit `fix_command` structures in `quality.yaml` to avoid implicit string manipulation.

**Out of Scope:**
- Modifications to client-side runner implementations or the core Antigravity platform.

---

## Problem Statement

Expose structured JSON data in a format that the LLM model can actually read (remedying the fact that the client runner discards `type: "json"` payloads), and introduce a safe, configuration-controlled, tool-agnostic `auto_fix` tool to automatically fix linting/formatting violations.

## Research Goals

- Identify how existing tools produce JSON data and standardise them.
- Compare options for exposing JSON data to the LLM (embedded markdown vs MCP Resources).
- Formulate the design of the `auto_fix` tool and trace how it can reuse the scope-resolution, file-filtering, and command-resolution logic of `QAManager`.
- Define how `quality.yaml` can be extended with explicit `fix_command` arrays.

---

## Background

Initial research under Issue #301 laid the groundwork, and Issue #390 introduced `StructuredTool` and `mcp_converters.py`. During the implementation phase of #402, it was discovered that the Antigravity client runner discards `type: "json"` blocks from tool responses before presenting them to the model, rendering the dual-payload model ineffective.

---

## Findings

### 1. Existing Behavior and Patterns
Our MCP server uses a two-tiered tool response model:
- **`BaseTool` / `BaseTool.execute`:** Returns `ToolResult.text(...)`, which produces a single content block of type `"text"`. Standard MCP clients receive `structuredContent = None`.
- **`StructuredTool` / `StructuredTool.execute_structured`:** Returns a tuple `(data_dict, summary_text)`. The base class maps this to `ToolResult.json_data(data_dict, text=summary_text)`, creating two content blocks: `content[0]` of type `"json"`, and `content[1]` of type `"text"`. The server's `convert_tool_result_to_mcp_result` extracts the JSON block to `CallToolResult.structuredContent` and leaves the text fallback block in `CallToolResult.content`.

### 2. The Structured Content Limitation & Alternatives
Since the client runner discards `structuredContent` (the `"json"` content item), we researched two options to make the JSON data available to the model:

#### Option A: Single-Payload Markdown Injection (Quickfix)
- **Mechanism:** Modify `ToolResult.json_data()` to return a single `"text"` content block containing the geformatteerde text summary, followed by a markdown code block containing the JSON dump (` ```json ... ``` `).
- **Pros:** Fast to implement, 100% visible to the model, resolves the interaction breakdown immediately.
- **Cons:** Slightly clutters the text output with raw JSON, but perfectly readable for both humans and models.

#### Option B: MCP Resources (Future State)
- **Mechanism:** Return only the text summary in the tool response, accompanied by a resource URI (e.g. `issue://402/json`). The model can then explicitly read this details payload using the native `read_resource` tool.
- **Pros:** Perfect architectural separation between action/presentation and details. Highly clean.
- **Cons:** Requires implementing a dynamic resource registry and state cache on the server.

### 3. Agnostic Code Auto-Fixing
We researched how to implement an automatic code-fixing tool without violating CQS (Command/Query Separation) and SRP (Single Responsibility Principle):
- **Agnostic Naming:** The tool should be named `auto_fix` (or `lint_fix`), decoupling it from Ruff or any other specific command-line tool.
- **Config-First & Explicit over Implicit:** Rather than letting the server magically strip `--check` or `--diff` flags from the validation commands, we will add an explicit `fix_command` string array to `ExecutionConfig` in `quality.yaml` for each gate supporting autofix.
- **Internal Code Reuse:** The `AutoFixTool` will delegate to `QAManager.run_auto_fix()`, which will reuse:
  - `_resolve_scope(scope, files)` for scope-to-path resolution.
  - `_files_for_gate(gate, files)` to filter paths by glob patterns and file types.
  - `_resolve_command(base_command, files)` to execute scripts in the correct `.venv`.

---

## Open Questions

1. Should the `auto_fix` tool return a detailed diff of changes, or just a list of gates and files fixed?
2. How do we cache dynamic tool outputs to serve them as MCP Resources under Option B?

---

## Approved Strategy

### Boundary / consumer scope
All MCP tools in `mcp_server/tools/` without exception. The new `auto_fix` tool will be added to `mcp_server/tools/quality_tools.py`.

### Selected strategy
1. **JSON Exposure:** Implement Option A (Markdown JSON injection in a single text payload) as the immediate quickfix. Design Option B (MCP Resources) for the long-term solution.
2. **Auto-Fix Tool:** Create a separate, tool-agnostic `auto_fix` tool utilizing the explicit `fix_command` from `quality.yaml` and reusing the internal file-filtering and command-resolution logic of `QAManager`.

### Rationale
Ensures that JSON data is immediately visible to the LLM without platform workarounds. The separate `auto_fix` tool respects CQS and SRP, while the explicit `fix_command` respects the "Explicit over Implicit" principle and prevents configuration drift.

### Constraints for later phases
- `ExecutionConfig` schema must be updated to support optional `fix_command`.
- `quality.yaml` must explicitly define `fix_command` for all gates where `supports_autofix` is True.
- Test helpers must parse the JSON block out of the text content to run assertions.
