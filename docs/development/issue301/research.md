# Research — Issue #301: Use MCP `structuredContent` for Tool JSON Payloads

**Status:** Research complete — QA approved (Round 4)  
**Branch:** `feature/301-use-mcp-structured-content-for-tool-json-payloads`  
**Phase:** research  
**Date:** 2026-05-04

---

## 1. Problem Statement

Two tools — `RunTestsTool` and `RunQualityGatesTool` — currently return a `ToolResult` with two
content items:

- `content[0]`: `{"type": "text", "text": "<human-readable summary>"}` — one-liner for display
- `content[1]`: `{"type": "json", "json": <dict>}` — structured machine-readable payload

`server.py:_convert_tool_result_to_content()` converts the `type=json` item to a **second
`TextContent`** via `json.dumps(..., indent=2)`. `CallToolResult` is sent to the MCP client
with **two text blocks** and `structuredContent=None`.

Result: the AI model receives the same data twice — the concise summary *and* a full JSON dump
repeating all fields verbatim. The `structuredContent` field of `CallToolResult` is never
populated, even though it exists specifically for this purpose.

---

## 2. SDK and Dependency Verification

### 2.1 `structuredContent` availability

| Location | Value | Status |
|---|---|---|
| `pyproject.toml` `dependencies` | `mcp>=1.0.0` | ✅ SSOT — correct location |
| `requirements.txt` | **not present** | ✅ correct — runtime dep in pyproject.toml |
| `requirements-dev.txt` | **not present** | ✅ correct — not a dev-only dep |
| Installed in venv | `mcp==1.27.0` | ✅ confirmed |
| `CallToolResult.structuredContent` | `dict[str, Any] \| None = None` | ✅ present in 1.27.0 |

`mcp` is a runtime dependency, correctly declared only in `pyproject.toml`. No change to
requirements files needed.

### 2.2 `CallToolResult` shape (SDK 1.27.0)

```python
class CallToolResult(Result):
    content: list[ContentBlock]
    structuredContent: dict[str, Any] | None = None
    isError: bool = False
```

The field accepts a **single dict** — not a list. Both affected tools return exactly one JSON
dict per invocation, which maps cleanly.

---

## 3. Current Wire Format

### 3.1 `RunTestsTool` — current

`_to_tool_result()` in `mcp_server/tools/test_tools.py`:

```python
ToolResult(content=[
    {"type": "text",  "text": "2 failed, 10 passed in 1.23s\nFAILED test_foo — …"},
    {"type": "json",  "json": {
        "exit_code": 1,
        "summary": {"passed": 10, "failed": 2, "skipped": 0, "errors": 0},
        "summary_line": "2 failed, 10 passed in 1.23s",
        "failures": [{"test_id": "test_foo", "short_reason": "…", …}],
        "coverage_pct": 87.4,
        "lf_cache_was_empty": False,
        "stderr": ""
    }}
])
```

After `_convert_tool_result_to_content()` → `CallToolResult` sent to client:

```json
{
  "content": [
    {"type": "text", "text": "2 failed, 10 passed in 1.23s\nFAILED test_foo — …"},
    {"type": "text", "text": "{\n  \"exit_code\": 1,\n  \"summary\": {…}\n}"}
  ],
  "structuredContent": null,
  "isError": false
}
```

### 3.2 `RunQualityGatesTool` — current

`execute()` in `mcp_server/tools/quality_tools.py`:

```python
ToolResult(content=[
    {"type": "text", "text": "✅ Quality gates passed (3/3) in 1234ms"},
    {"type": "json", "json": {
        "overall_pass": True,
        "duration_ms": 1234,
        "gates": [{"id": 1, "name": "Gate 0: Ruff Format", "passed": True, …}]
    }}
])
```

Same conversion applies — second text block is a JSON dump.

### 3.3 Background: `ToolResult.json_data()` design intent

`ToolResult.json_data()` is a classmethod on `mcp_server/tools/tool_result.py` designed as the
canonical factory for tools returning structured data. Three independent sources confirm this was
the intended architectural pattern:

1. **`docs/architecture/VSCODE_AGENT_ORCHESTRATION.md` (line 1474):** Documents `json_data()`
   as the standard return method for tools returning structured data.
2. **`docs/development/archive/issue103/planning.md` (line 66):** `execute()` was planned to
   return `ToolResult.json_data(parsed)` — the canonical pattern for quality tools from the start.
3. **`docs/development/archive/issue251/research.md` Investigation 3 (lines 149–174):**
   Identified the double-output bug as caused by `_convert_tool_result_to_content` converting
   any `{"type": "json"}` item into a text block regardless of content order; prescribed the
   `run_tests` json-first content pattern as the fix for `run_quality_gates` — the same
   ordering that `json_data()` produces.

**The gap:** Both `test_tools.py` (lines 109, 123) and `quality_tools.py` (line 120) bypass
`json_data()` by manually constructing `{"type": "json"}` items. This is the root cause of the
inconsistency — `json_data()` creates `content[0]=json, content[1]=text` (json-first order),
but both tools use text-first order (`content[0]=text, content[1]=json`). `json_data()` was
never adopted as the canonical path in practice.

---

## 4. Full Blast Radius

### 4.1 Production code — files requiring change

| File | Change needed |
|---|---|
| `mcp_server/server.py` | `_convert_tool_result_to_content()` — remove `type==json` branch; `_convert_tool_result_to_mcp_result()` — extract json items and pass as `structuredContent` |
| `mcp_server/tools/test_tools.py` | `_to_tool_result()` — **no change required** if ToolResult internal format `{"type":"json"}` is preserved as the server-level boundary; OR remove json item if ToolResult contract changes |
| `mcp_server/tools/quality_tools.py` | Same as test_tools.py |
| `mcp_server/tools/tool_result.py` | `json_data()` classmethod — currently adds both json+text items; if internal contract changes this needs updating |
| `mcp_server/managers/qa_manager.py` | Docstring only — `content[1].json` reference in method docstring (line 591) |

**Note on design boundary:** Whether the `{"type": "json"}` item lives in `ToolResult.content`
(tool layer) and gets extracted at the server layer, or is removed from `ToolResult.content`
entirely and stored in a new field, is a **design decision** — see Open Questions §7.

### 4.2 Test suite — files requiring change

All files below have assertions that depend on `content[1]` being `type="json"` or directly
access `content[1]["json"]`. These will break with any change to the two-item ToolResult
contract.

| File | Lines | Description |
|---|---|---|
| `tests/mcp_server/unit/tools/test_test_tools.py` | 97, 122–124, 283, 293, 307, 495 | 8 assertions on `content[1]["json"].*` |
| `tests/mcp_server/unit/tools/test_quality_tools.py` | 36–37, 276–277 | 4 assertions: `content[1]["type"]=="json"`, `content[1]["json"]` |
| `tests/mcp_server/unit/tools/test_tool_result_contract.py` | 60, 92, 101–102, 124, 149, 155, 167 | Contract tests: exactly 2 items, content[1] type=json, compact schema shape |
| `tests/mcp_server/unit/tools/test_dev_tools.py` | 45 | `content[1]["json"]["summary"]["passed"]` |
| `tests/mcp_server/unit/integration/test_all_tools.py` | 407–408 | `content[1]["json"]` |
| `tests/mcp_server/integration/test_qa.py` | 53, 57, 61 | `content[1]["type"]=="json"`, `content[1]["json"]` |
| `tests/mcp_server/unit/managers/test_qa_manager.py` | 1433–1444 | `test_json_data_returns_dual_content` — tests `ToolResult.json_data()` directly (not QAManager behavior); will need to move or be deleted depending on the §7.1 design decision |

**Not affected** (use `content[1]["text"]` for appended notes, or `content[1]["resource"]`):

- `tests/mcp_server/integration/test_blocker_recovery_note_dispatch.py` — notes are text
- `tests/mcp_server/unit/core/test_note_context_unit.py` — notes are text
- `tests/mcp_server/integration/test_scaffold_validation_e2e.py` — uses `type="resource"` for schema

**Total: 7 test files, ~25 assertions need updating.**

No backward-compat shims, no legacy conditional paths. All affected assertions must be
rewritten to reflect the new contract; no old test variant is kept.

### 4.3 Test suite — new files to create

The existing test suite has **zero coverage** of `_convert_tool_result_to_mcp_result()` at the
server layer. §8.5 requires a test that verifies `structuredContent` is populated after the
change. This cannot be satisfied by updating existing tests — it requires a new test file.

| File (to create) | Purpose |
|---|---|
| `tests/mcp_server/unit/server/test_tool_result_conversion.py` (or equivalent) | Assert that `_convert_tool_result_to_mcp_result()` populates `structuredContent` for tools with `{"type":"json"}` items; assert `structuredContent=None` for text-only tools |

---

## 5. MCP Specification Findings

### 5.1 `structuredContent` (§5.2.6 — spec 2025-11-25, confirmed identical in 2025-06-18)

> "Structured content is returned as a JSON object in the `structuredContent` field of a result.  
> For backwards compatibility, a tool that returns structured content **SHOULD** also return the
> serialized JSON in a TextContent block."

**Critical implication:** The spec SHOULD exists to preserve backward compatibility for clients
that don't yet support `structuredContent`. Per VS Code MCP team's stated design goal (§6.1,
via connor4312 on issue #290063): `content[].text` is the intended model-input channel;
`structuredContent` serves the MCP client UI/programmatic layer — not the LLM. Since VS Code is
the sole client and routes `structuredContent` via a dedicated code path (separate from model
context), a JSON-text duplicate in `content[]` provides no practical benefit for this deployment.

### 5.2 `outputSchema` (§5.2.7)

Tools may declare `outputSchema` on their tool definition (alongside `inputSchema`). If present:
- Server **MUST** ensure `structuredContent` conforms to the schema.
- Clients **SHOULD** validate `structuredContent` against the schema.

`outputSchema` is the machine-readable contract that completes the `structuredContent` story.
Without it, `structuredContent` is still valid but unvalidated. See §7.2 (confirmed in scope for #301).
---

## 6. Model / Client Compatibility Assessment

`structuredContent` is a **server-to-client** protocol field. It is the MCP *client* that
decides whether and how to expose the structured data to the underlying language model.

### 6.1 VS Code GitHub Copilot (primary client for this codebase)

- Uses the MCP proxy transport (`mcp_server/core/proxy.py` — stdio bridge).
- **Support confirmed:** VS Code added `structuredContent` support in July 2025
  ([issue #254329](https://github.com/microsoft/vscode/issues/254329), closed 14 July 2025).
- **Verified client behavior** (source: `mcpLanguageModelToolContribution.ts`, documented in
  open bug [#290063](https://github.com/microsoft/vscode/issues/290063)):
  - When `structuredContent` is **absent**: `content[].text` is sent to the model.
  - When `structuredContent` is **present**: `content[].text` is **skipped**;
    `JSON.stringify(structuredContent)` is sent to the model instead.
- **VS Code MCP team intent** (connor4312, 29 Jan 2026, comment on #290063): `structuredContent`
  **should not be presented to the model**; its intended use is programmatic tool calls (PTC)
  and MCP Apps UI rendering. Ongoing spec clarification:
  [modelcontextprotocol/modelcontextprotocol#1624](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1624).
- **Implication:** `content[].text` is the **primary model input** per spec intent.
  `structuredContent` is consumed by the MCP client layer (UI/programmatic), not the LLM.
  Both fields serve independent purposes; populating both is the correct approach.

### 6.2 Claude Desktop

- Anthropic's own MCP client; has first-party support for MCP spec features.
- Likely to support `structuredContent` in newer versions, but whether it is presented to the
  Claude model in context (vs. used internally by the client) is unconfirmed.

### 6.3 GPT / OpenAI

- No native MCP client. OpenAI API uses its own function-calling / tool-use protocol.
- Any GPT+MCP integration uses a third-party bridge (e.g., OpenAI Agents SDK MCP adapter).
- Such bridges typically forward `content` text blocks; `structuredContent` support depends
  entirely on the bridge implementation.
- **Assessment: not relevant for this codebase** — this server is consumed only by VS Code
  Copilot.

### 6.4 Gemini (Google)

- No native MCP client. Google's Vertex AI / Gemini uses its own tool protocol.
- Same situation as GPT: any Gemini+MCP integration is third-party.
- **Assessment: not relevant for this codebase.**

### 6.5 Summary

Only VS Code GitHub Copilot matters for this server. Per the VS Code MCP team's stated design
intent (§6.1, via connor4312, issue #290063): `content[].text` is the intended model-input
channel; `structuredContent` serves the MCP client UI/programmatic layer. Both fields are
independent and both should be populated — the text summary in `content[0]` for the model,
`structuredContent` for non-model consumers.

---

## 7. Open Design Questions

These questions must be resolved in the design phase. No implementation detail is given here.

### 7.1 Where is the boundary between ToolResult and structuredContent?

`ToolResult` is the *internal* result type (tool layer → server layer). `CallToolResult` is the
*protocol* type (server layer → MCP client). Two design options exist:

**Option A — Extract at server layer:** Keep `{"type": "json"}` items in `ToolResult.content`;
server extracts them and promotes to `structuredContent`. Tools are unaware of the wire format
change.

**Option B — New ToolResult field:** Add a `structured_content` field (or similar) to
`ToolResult` itself; tools populate it directly; server maps it 1:1 to `CallToolResult.structuredContent`.
The `{"type": "json"}` internal type disappears entirely.

Which option better satisfies SOLID/SRP and the architecture principles?

### 7.2 `outputSchema` — shape and placement

`outputSchema` on tool definition enables schema validation of `structuredContent` by clients
(§5.2.7). **Confirmed in scope for #301.** Design must cover:

1. Where `outputSchema` is declared (on the tool definition, via SDK `Tool.outputSchema`).
2. JSON Schema shape for `RunTestsTool` and `RunQualityGatesTool` payloads.
3. Server-side pass-through in the `tools/list` response.

### 7.3 `test_tool_result_contract.py` — delete or rewrite?

This file tests the current `content[0]=text, content[1]=json` contract explicitly. After the
change, the contract it tests no longer exists. Options:
- Delete and replace with a new contract test for the new server-level behavior.
- Rewrite in place.

The answer flows from the design decision in §7.1.

---

## 8. Expected Results

The following outcomes define "done" for this issue. They are stated as observable behavior,
not implementation details.

### 8.1 Wire format after change

A `run_tests` call with 2 failures must produce a `CallToolResult` where:

```json
{
  "content": [
    {
      "type": "text",
      "text": "2 failed, 10 passed in 1.23s\nFAILED test_foo — assert 1 == 2"
    }
  ],
  "structuredContent": {
    "exit_code": 1,
    "summary": {"passed": 10, "failed": 2, "skipped": 0, "errors": 0},
    "summary_line": "2 failed, 10 passed in 1.23s",
    "failures": [{"test_id": "test_foo", "short_reason": "assert 1 == 2"}],
    "coverage_pct": 87.4,
    "lf_cache_was_empty": false,
    "stderr": ""
  },
  "isError": false
}
```

### 8.2 Wire format — RunQualityGatesTool

```json
{
  "content": [
    {"type": "text", "text": "✅ Quality gates passed (3/3) in 1234ms"}
  ],
  "structuredContent": {
    "overall_pass": true,
    "duration_ms": 1234,
    "gates": [{"id": 1, "name": "Gate 0: Ruff Format", "passed": true, …}]
  },
  "isError": false
}
```

### 8.3 All tests pass

- 0 regressions in existing test suite.
- All 7 affected test files updated to assert the new contract.
- No `content[1]["type"] == "json"` assertions remain in the codebase.
- No legacy conditional paths, no `# compat` comments, no `# TODO: remove after X` lines.

### 8.4 Architecture principles compliance

Every changed or new file must comply with all clauses of `ARCHITECTURE_PRINCIPLES.md`:

- **§1.1 SRP**: Each class/method has one responsibility. Server-layer conversion, tool-layer
  result building, and protocol-layer dispatch remain separated.
- **§1.5 DIP**: No direct instantiation in `execute()`. Constructor injection is the default.
- **§5 CQS**: Conversion method returns value; does not mutate. ToolResult remains frozen
  after construction.
- **§14 Public API in tests**: No `result._internal` access. All test assertions via the public
  `ToolResult` API or via the server conversion method's return value.
- **YAGNI (§9)**: No migration shims, no feature flags, no `if legacy:` conditionals. One
  correct implementation only.

### 8.5 No `structuredContent=None` for affected tools

After the change, calling `run_tests` or `run_quality_gates` MUST produce a `CallToolResult`
where `structuredContent` is not `None`. A test must verify this at the server layer.

### 8.6 Unaffected tools unchanged

All tools that currently return only `TextContent` (no `type=json` items) must continue to
produce `structuredContent=None`. No unintended scope creep.

---

## 9. Files Examined

| File | Purpose |
|---|---|
| `mcp_server/server.py` lines 498–530 | `_convert_tool_result_to_content()` and `_convert_tool_result_to_mcp_result()` |
| `mcp_server/tools/test_tools.py` lines 85–130 | `_to_tool_result()` |
| `mcp_server/tools/quality_tools.py` lines 80–130 | `execute()` |
| `mcp_server/tools/tool_result.py` | `ToolResult`, `json_data()` |
| `mcp_server/managers/qa_manager.py` lines 491, 591 | Docstring references |
| `pyproject.toml` | Dependency declaration |
| `requirements.txt` / `requirements-dev.txt` | Confirmed mcp absent (correct) |
| MCP spec 2025-11-25 §5.2.6, §5.2.7 | `structuredContent` and `outputSchema` normative text |
| MCP SDK source (venv) | `CallToolResult` class definition |
| GitHub microsoft/vscode [#254329](https://github.com/microsoft/vscode/issues/254329) | `structuredContent` support added (closed 14 July 2025) |
| GitHub microsoft/vscode [#290063](https://github.com/microsoft/vscode/issues/290063) | `structuredContent` overrides `content[].text` — open bug; confirmed current VS Code behavior |
| VS Code source `mcpLanguageModelToolContribution.ts` lines 307–378 | Verified: text skipped when `structuredContent` present; `JSON.stringify(structuredContent)` sent to model |
| `docs/architecture/VSCODE_AGENT_ORCHESTRATION.md` line 1474 | `json_data()` documented as standard return method |
| `docs/development/archive/issue103/planning.md` line 66 | `json_data()` was the planned canonical pattern from the start |
| `docs/development/archive/issue251/research.md` Investigation 3 (lines 149–174) | Double-output bug attributed to server mishandling json-first content; prescribed the run_tests json-first pattern as the fix — identical ordering to what `json_data()` produces |
