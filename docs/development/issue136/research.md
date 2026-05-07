<!-- docs\development\issue136\research.md -->
<!-- template=research version=8b7bb3ab created=2026-05-07T15:54Z updated=2026-05-07T18:20Z -->
# Error Taxonomy & Strict Input Validation — Research

**Status:** COMPLETE  
**Version:** 3.0  
**Last Updated:** 2026-05-07  
**Issues:** #136 (predictable error handling via NoteContext taxonomy) + #147 (strict tool input models, bundled deliverable)  
**Epic:** #320 phase 0

---

## Problem Statement

Predictable failures in MCP tools currently fall into two overlapping gaps:

1. Runtime/domain failures often return generic error text and generic internal `error_code` values.
2. Tool argument validation happens before `NoteContext` exists, so once `extra="forbid"` is applied to all tool input models, agent-supplied extra fields will fail before any tool or manager can produce an actionable note.

The central research question is therefore not “which new error codes should exist?” but:

**How does the existing NoteContext architecture require failures to be surfaced, and how does tool input schema validation fit that architecture when source files are not available to the agent?**

---

## Research Goals

1. Recover the design rationale for `NoteContext` from current docs and git history.
2. Identify the hard architecture constraints that are already settled.
3. Trace what happens today when Pydantic tool input validation fails.
4. Determine the impact of applying `extra="forbid"` to all tool input models.
5. Identify whether input schemas can currently be surfaced through the existing note architecture.
6. Document implementation touch-points without making design decisions reserved for planning/design.

---

## 1. NoteContext Rationale From Docs And Git History

### 1.1 Current documentation: exactly three communication paths

Issue #300 research states the current MCP server has exactly three communication paths from tool internals to the caller:

1. `ToolResult` — primary response object returned by `execute()`
2. `NoteContext` — typed secondary notes attached during execution and rendered after primary content
3. Exceptions — infrastructure path caught by `@tool_error_handler` and converted to `ToolResult.error(...)`

The same document states: **no new communication paths should be created**.

Issue #300 also clarifies the division of responsibility:

- `ToolResult` is the primary diagnostic transport.
- `NoteContext` is the secondary/actionable signal transport.
- Exceptions are an infrastructure transport for expected failure conversion, not the place to preserve rich diagnostics.

### 1.2 Historical issue #283 planning: typed notes replaced hints/blockers/recovery

Git history shows the NoteContext protocol was introduced and then wired in cycles:

| Commit | Evidence |
|--------|----------|
| `7d5314ad` | `feat(P_IMPLEMENTATION_SP_C1_GREEN): implement NoteContext note-protocol contract (operation_notes.py)` |
| `c7644435` | `refactor(P_IMPLEMENTATION_SP_C1_REFACTOR): ... structural-failure documentation` |
| `49ff69b2` | RED tests for NoteContext wiring in `EnforcementRunner`, `GitCommitTool`, and full dispatch integration |
| `e326f1c6` | GREEN wiring through `EnforcementRunner`, `BaseTool`, `GitCommitTool`, and `server` |
| `a9b90b2d` | Adds `del context` to tools where the newly required `NoteContext` parameter was still unused |

Historical issue #283 planning establishes these hard contracts:

- `MCPServer.handle_call_tool()` creates one `NoteContext` per call.
- Enforcement and tool execution receive the same context.
- `render_to_response()` is called unconditionally after execution.
- Typed notes replace legacy untyped channels (`hints`, `blockers=`, `recovery=`).
- Notes must be written before raising, because `tool_error_handler` remains context-agnostic.
- `tool_error_handler` must not import `operation_notes` and must not become the note producer.

### 1.3 Current tests confirm the contract

`tests/mcp_server/integration/test_blocker_recovery_note_dispatch.py` proves:

- Notes produced before `PreflightError`, `ExecutionError`, or `ValidationError` survive the exception.
- `NoteContext.render_to_response()` appends notes to error results.
- Rendering works on success results too.
- Multiple note types render in insertion order.

This is not optional behavior; it is the tested protocol replacing the old hint/blocker/recovery channels.

### 1.4 Consequence for this issue

For predictable failures, the target architecture is already settled:

- Core diagnostic content belongs in `ToolResult`.
- Actionable context belongs in typed `NoteEntry` values produced through `NoteContext`.
- Exceptions may still carry coarse machine/test metadata, but `ToolResult.error_code` is not sufficient for agent-facing context.

---

## 2. What The Agent Actually Sees Today

### 2.1 `ToolResult.error_code` is not agent-visible

`ToolResult` has `error_code` and `file_path`, but `_convert_tool_result_to_mcp_result()` converts only `content` and `isError` into `CallToolResult`.

The MCP client receives:

- `isError`
- `content[]`

It does not receive `ToolResult.error_code` as a structured field. Therefore, adding more internal error codes alone cannot solve agent-facing feedback. Error codes may still be useful for tests, logs, routing, or future structured adapters, but not as the primary mechanism for the LLM agent.

### 2.2 Notes are visible because they become content

`NoteContext.render_to_response()` appends all `Renderable` notes as a text content block.

Current renderable note types:

| Note type | Current rendered form |
|-----------|-----------------------|
| `ExclusionNote` | `Excluded from commit index: {file_path}` |
| `SuggestionNote` | `Suggestion: {message}` |
| `BlockerNote` | `Blocker: {message}` |
| `RecoveryNote` | `Recovery: {message}` |
| `InfoNote` | `{message}` |

`CommitNote` intentionally does not render.

---

## 3. Tool Argument Validation Path Today

### 3.1 Validation happens before NoteContext creation

`MCPServer.handle_call_tool()` currently runs in this order:

```text
_validate_tool_arguments(tool, arguments, call_id, name)
if validation failed: return list[TextContent]

note_context = NoteContext()
_run_tool_enforcement(..., note_context)
raw_result = await tool.execute(validated, note_context)
result = note_context.render_to_response(raw_result)
```

This means Pydantic argument validation failures happen before any `NoteContext` exists.

### 3.2 Validation failure currently bypasses ToolResult

On Pydantic validation failure, `_validate_tool_arguments()` returns:

```python
[TextContent(type="text", text=f"Invalid input for {name}: {error_details}")]
```

This bypasses:

- `ToolResult.error(...)`
- `ToolResult.is_error`
- `ToolResult.error_code`
- `NoteContext`
- `render_to_response()`
- Embedded schema resources

The failure does come back as content, but not through the normal error/note pipeline.

### 3.3 Current `extra="forbid"` coverage

Only `GitCommitInput` currently has `model_config = ConfigDict(extra="forbid")`.

All other 50 tool input models are permissive by default. Pydantic’s default behavior for extra fields is to ignore them. Therefore, many agent typos are currently accepted and silently discarded.

---

## 4. Impact Of Applying `extra="forbid"` To All Tool Inputs

### 4.1 The blast radius is central, not 50 independent execution paths

If `extra="forbid"` is applied to all 50 input models, every extra-field failure will fail in the same central server method: `_validate_tool_arguments()`.

The affected tools will not reach:

- `tool.execute()`
- enforcement pre-checks
- domain managers
- `@tool_error_handler`
- existing NoteContext note production

Therefore, the strict-input change requires a central response-path fix. Adding notes inside individual tools cannot cover extra-field failures because those tools never execute.

### 4.2 Agent experience after `extra="forbid"` without additional work

Expected current behavior after adding strict models:

```text
Invalid input for <tool>: 1 validation error for <InputModel>
<extra_field>
  Extra inputs are not permitted ...
```

Missing from that response:

- a normal `ToolResult.error` shape
- explicit `isError=True` from the server conversion path
- a typed note explaining what to do
- the valid input schema
- a schema resource usable when source files are not exposed

This is the main issue #147 integration gap.

### 4.3 Source access cannot be assumed

The tool input schema already exists at runtime through each tool’s `input_schema` property / `args_model.model_json_schema()`.

That runtime schema is the correct source for agent-facing input guidance when the MCP server is packaged as an executable and source files are not available. Any solution that expects the agent to inspect Python source files is incompatible with executable-only MCP distribution.

---

## 5. Existing Schema-In-Response Precedent

### 5.1 Scaffold validation already has a schema resource path

Issue #120 introduced structured schema resources for scaffold validation errors. The current `tool_error_handler` still has special handling:

```python
if isinstance(exc, ValidationError) and hasattr(exc, "schema") and exc.schema:
    content = [
        {"type": "text", "text": message},
        {
            "type": "resource",
            "resource": {
                "uri": "schema://validation",
                "mimeType": "application/json",
                "text": json.dumps(exc.schema.to_dict(), indent=2),
            },
        },
    ]
```

`tests/mcp_server/integration/test_scaffold_validation_e2e.py` asserts that missing required fields return:

- text error content
- a `schema://validation` JSON resource

### 5.2 Historical rationale for resource content

Issue #120 handover documents why schema resources were used:

- MCP supports multiple content items in a tool result.
- Agents can parse JSON schema separately from human-readable error text.
- This enables AI-driven schema comprehension.

This is directly relevant to strict input validation. The same problem appears one layer earlier: tool argument validation fails before execution, and the agent needs the valid schema in the response.

---

## 6. Can An Input Schema Be A Note Today?

### 6.1 Current NoteEntry variants are text-rendered only

Current `Renderable` notes expose only:

```python
def to_message(self) -> str: ...
```

`NoteContext.render_to_response()` joins all renderable notes into a single text block:

```python
notes_text = "\n".join(n.to_message() for n in renderable)
augmented = list(base.content) + [{"type": "text", "text": notes_text}]
```

There is currently no note variant that renders as an MCP resource, JSON content item, or embedded schema.

### 6.2 Input schemas do not fit the current note renderer without loss

A JSON schema can be serialized into a `SuggestionNote` message, but that would:

- collapse structured JSON into a plain text note
- mix human guidance and machine-readable schema in one text block
- lose the existing `schema://validation` resource precedent
- make long schemas noisy and harder for agents to parse

Therefore, the current note architecture can express “remove unknown field X” or “valid fields are A, B, C” as text, but it cannot express “here is the full valid input schema” as a structured note.

### 6.3 Architecture gap identified

The architecture currently has:

- `ToolResult` resource content for schemas (proven by scaffold validation)
- `NoteContext` text-rendered secondary notes
- no structured/resource-producing note subtype
- no `NoteContext` during argument validation

This means strict tool input validation creates two gaps:

1. **Lifecycle gap:** `NoteContext` is created too late for argument validation errors.
2. **Representation gap:** current notes cannot carry structured input schema resources.

Planning/design must decide how to close those gaps without adding a fourth communication path.

---

## 7. Scaffold Artifact Chain Gap

The scaffold chain has a separate but related gap.

`ScaffoldArtifactTool.execute()` currently does:

```python
async def execute(self, params: ScaffoldArtifactInput, context: NoteContext) -> ToolResult:
    del context
    ...
    artifact_path = await self.manager.scaffold_artifact(params.artifact_type, **kwargs)
```

This was introduced in the historical C4 cleanup commit that added `del context` to tools with unused parameters. It should be understood as “currently unused”, not as an architectural decision that scaffold errors should avoid notes.

Current scaffold raise-sites produce no notes:

| Layer | Raise-sites | Notes today |
|-------|-------------|-------------|
| `ArtifactRegistryConfig.get_artifact()` | unknown artifact type | none |
| `ArtifactManager.scaffold_artifact()` | missing output path, missing template config, V2 context validation, render context lookup, generated-content validation | none |
| `TemplateScaffolder.validate()` | no template configured, missing fields, loader not configured, generic template missing | partial schema resource only for missing fields; no note |
| `JinjaRenderer.get_template()` | template not found | none |
| `FilesystemAdapter` | path outside workspace, write/read system failures | none |

Because `ToolResult.error_code` is not visible to the agent, adding granular scaffold error codes alone would not address this gap. The agent-facing part must flow through `ToolResult.content` and/or `NoteContext`.

---

## 8. Input Models Without `extra="forbid"`

Only `GitCommitInput` is strict today. The following 50 input models are not strict.

| File | Models missing `extra="forbid"` |
|------|----------------------------------|
| `admin_tools.py` | `RestartServerInput` |
| `cycle_tools.py` | `TransitionCycleInput`, `ForceCycleTransitionInput` |
| `discovery_tools.py` | `SearchDocumentationInput`, `GetWorkContextInput` |
| `git_analysis_tools.py` | `GitListBranchesInput`, `GitDiffInput` |
| `git_fetch_tool.py` | `GitFetchInput` |
| `git_pull_tool.py` | `GitPullInput` |
| `git_tools.py` | `CreateBranchInput`, `GitStatusInput`, `GitRestoreInput`, `GitCheckoutInput`, `GitPushInput`, `GitMergeInput`, `GitDeleteBranchInput`, `GitStashInput`, `GetParentBranchInput` |
| `health_tools.py` | `HealthCheckInput` |
| `issue_tools.py` | `CreateIssueInput`, `GetIssueInput`, `ListIssuesInput`, `UpdateIssueInput`, `CloseIssueInput` |
| `label_tools.py` | `ListLabelsInput`, `CreateLabelInput`, `DeleteLabelInput`, `RemoveLabelsInput`, `AddLabelsInput`, `DetectLabelDriftInput` |
| `milestone_tools.py` | `ListMilestonesInput`, `CreateMilestoneInput`, `CloseMilestoneInput` |
| `phase_tools.py` | `TransitionPhaseInput`, `ForcePhaseTransitionInput` |
| `pr_tools.py` | `ListPRsInput`, `MergePRInput`, `SubmitPRInput` |
| `project_tools.py` | `InitializeProjectInput`, `GetProjectPlanInput`, `SavePlanningDeliverablesInput`, `UpdatePlanningDeliverablesInput` |
| `quality_tools.py` | `RunQualityGatesInput` |
| `safe_edit_tool.py` | `SafeEditInput` |
| `scaffold_artifact.py` | `ScaffoldArtifactInput` |
| `template_validation_tool.py` | `TemplateValidationInput` |
| `test_tools.py` | `RunTestsInput` |
| `validation_tools.py` | `ValidationInput`, `ValidateDTOInput` |
| `code_tools.py` | `CreateFileInput` |

`SafeEditInput` also has nested Pydantic models (`LineEdit`, `InsertLine`). Their strictness is a planning/design scope question because nested validation failures surface through the same central argument-validation path.

---

## 9. Research Findings

1. `NoteContext` is not optional guidance. It is the established replacement for legacy hints/blockers/recovery and is the required channel for actionable secondary context.
2. `ToolResult` remains the primary diagnostic transport. Notes should not replace primary diagnostics.
3. `ToolResult.error_code` is currently not visible to the LLM agent. Error-code granularity alone cannot solve the user-facing problem.
4. Applying `extra="forbid"` to 50 models will route all extra-field failures through `_validate_tool_arguments()` before `NoteContext` exists.
5. Current argument-validation failure bypasses `ToolResult.error`, `render_to_response`, and schema resources.
6. Runtime input schemas are available via `args_model.model_json_schema()` and do not require source-file access.
7. The project already has a precedent for returning schema resources (`schema://validation`) on validation errors.
8. Current `NoteEntry` rendering can only emit text. A full input schema cannot be carried as a structured note without extending the note rendering model or placing schema resources directly in `ToolResult.content`.
9. The scaffold chain still discards `NoteContext` (`del context`) and produces zero notes for predictable errors.
10. The line through the remaining tools is central argument-validation architecture, not per-tool bespoke error handling.

---

## 10. Planning Inputs (Not Design Decisions)

These are facts and constraints for the next phase, not chosen solutions:

- Strict input validation needs a central failure response path in `server.py`.
- That response must include both a diagnostic and actionable note-style guidance.
- The valid input schema must be returned from runtime schema data, because source visibility is not guaranteed.
- Closing the lifecycle gap may require creating `NoteContext` before argument validation.
- Closing the representation gap may require extending `NoteContext`/`NoteEntry` to support structured resource content, or using `ToolResult.content` for schema resources while notes remain textual guidance.
- `tool_error_handler` should remain context-agnostic unless planning explicitly revisits the issue #283 contract.
- Scaffold predictable errors should use the existing NoteContext pattern rather than relying on new error codes alone.

---

## Related Documentation And Evidence

- `docs/development/issue300/research.md` — three communication paths; ToolResult primary, NoteContext secondary, exceptions infrastructure
- `docs/development/issue300/design.md` — no new communication paths constraint
- Historical `docs/development/issue283/planning.md` from commit `c7644435` — C3/C4 NoteContext wiring and flag-day migration rationale
- `docs/development/archive/issue120/SESSIE_OVERDRACHT_IMP_20260122.md` — schema resource rationale for validation errors
- `tests/mcp_server/integration/test_blocker_recovery_note_dispatch.py` — notes survive exceptions and render on error/success
- `tests/mcp_server/integration/test_scaffold_validation_e2e.py` — schema resource returned on scaffold validation error
- `mcp_server/server.py` — argument validation order and response conversion
- `mcp_server/core/operation_notes.py` — current note model and renderer
- `mcp_server/core/error_handling.py` — schema-resource special case and context-agnostic error conversion
- `mcp_server/tools/scaffold_artifact.py` — current `del context` gap
- `mcp_server/tools/base.py` — execute contract includes `context: NoteContext`

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-07 | imp-agent | Initial research; mixed research with premature error-code design |
| 2.0 | 2026-05-07 | imp-agent | Rewritten around NoteContext end-to-end path, but still framed some settled behavior as open questions |
| 3.0 | 2026-05-07 | imp-agent | Added docs/history rationale, strict-input central failure analysis, schema-resource precedent, and NoteContext representation/lifecycle gaps |
