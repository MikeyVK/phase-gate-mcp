<!-- docs\development\issue136\research.md -->
<!-- template=research version=8b7bb3ab created=2026-05-07T15:54Z updated=2026-05-07T19:05Z -->
# Error Taxonomy & Strict Input Validation - Research

**Status:** COMPLETE  
**Version:** 5.0  
**Last Updated:** 2026-05-07  
**Issues:** #136 (predictable error handling via NoteContext taxonomy) + #147 (strict tool input models, bundled deliverable)  
**Epic:** #320 phase 0

---

## Problem Statement

Predictable MCP failures currently have two separate but connected gaps:

1. Many runtime/domain failures return generic diagnostics and rely on internal `ToolResult.error_code` values that are not visible to the LLM client.
2. Tool argument validation happens before `NoteContext` exists. Once `extra="forbid"` is applied to all tool input models, agent-supplied extra fields will fail before any tool or manager can produce an actionable note.

The practical consequence is severe: strict input validation will correctly reject typo fields, but the agent will not automatically receive the valid input schema unless the central argument-validation response path is changed.

This research investigates how strict input schema failures fit the already-established NoteContext architecture. It does not choose implementation details for planning/design, but it does identify the non-negotiable architecture constraints and the current gaps.

---

## Research Goals

1. Recover the design rationale for `NoteContext` from reference docs and git history.
2. Identify the hard architecture constraints that are already settled.
3. Trace the current argument-validation failure path.
4. Determine what happens when `extra="forbid"` is applied to all tool inputs.
5. Investigate whether input schemas can be carried as notes in the current architecture.
6. Identify existing schema-response precedents and MCP-client constraints.
7. Document touch-points for planning without choosing a design.

---

## 1. NoteContext Rationale From Docs And Git History

### 1.1 Current documented communication model

Issue #300 research states that the MCP server has exactly three communication paths from tool internals to the caller:

1. `ToolResult` - primary response object returned by `execute()`
2. `NoteContext` - typed secondary notes attached during execution and rendered after primary content
3. Exceptions - infrastructure path caught by `@tool_error_handler` and converted to `ToolResult.error(...)`

The same document states that no new communication paths should be created.

Issue #300 also defines the responsibility split:

- `ToolResult` carries primary diagnostic data.
- `NoteContext` carries secondary/actionable signals.
- Exceptions are infrastructure for conversion, not a place to preserve rich user-facing context.

### 1.2 Git history confirms NoteContext was a deliberate protocol replacement

Relevant git-history evidence:

| Commit | Evidence |
|--------|----------|
| `7d5314ad` | `feat(P_IMPLEMENTATION_SP_C1_GREEN): implement NoteContext note-protocol contract (operation_notes.py)` |
| `c7644435` | `refactor(P_IMPLEMENTATION_SP_C1_REFACTOR): ... structural-failure documentation` |
| `49ff69b2` | RED tests for NoteContext wiring in `EnforcementRunner`, `GitCommitTool`, and full dispatch integration |
| `e326f1c6` | GREEN wiring through `EnforcementRunner`, `BaseTool`, `GitCommitTool`, and `server` |
| `a9b90b2d` | Adds `del context` to tools where the newly required `NoteContext` parameter was unused |

Historical issue #283 planning establishes these contracts:

- `MCPServer.handle_call_tool()` creates one `NoteContext` per call.
- Enforcement and tool execution receive the same context.
- `render_to_response()` is called unconditionally after execution.
- Typed notes replace legacy untyped channels: `hints`, `blockers=`, and `recovery=`.
- Notes are written before raising; `tool_error_handler` remains context-agnostic.
- `tool_error_handler` must not import `operation_notes`.

### 1.3 Current tests make the protocol executable

`tests/mcp_server/integration/test_blocker_recovery_note_dispatch.py` proves:

- Notes produced before `PreflightError`, `ExecutionError`, or `ValidationError` survive the exception.
- `NoteContext.render_to_response()` appends notes to error results.
- Rendering works on success results too.
- Multiple note types render in insertion order.

This behavior is not optional guidance. It is the tested replacement for the old hint/blocker/recovery channels.

### 1.4 Canonical existing note patterns

Existing docs and code show the intended mapping:

| Failure kind | Existing pattern |
|--------------|------------------|
| Preflight blocker before mutation | `BlockerNote` + `PreflightError` |
| Advisory validation guidance | `SuggestionNote` + `ValidationError` or explicit error result |
| Post-mutation recovery | `RecoveryNote` + `ToolResult.error()` or `ExecutionError` |
| General secondary context | `InfoNote` |

Issue #295 research states this pattern directly for submit PR:

- Preflights with no mutation use `BlockerNote + PreflightError`.
- Post-mutation recovery uses `RecoveryNote + ToolResult.error()`.

Issue #298 applies the same rule to `GetWorkContextTool`: tool-layer state errors produce `RecoveryNote` and return `ToolResult.error(...)`.

---

## 2. What The Agent Actually Sees Today

### 2.1 `ToolResult.error_code` is not agent-visible

`ToolResult` has `error_code` and `file_path`, but `_convert_tool_result_to_mcp_result()` converts only `content` and `isError` into `CallToolResult`.

The MCP client receives:

- `isError`
- `content[]`

It does not receive `ToolResult.error_code` as a structured field. Therefore, adding more internal error codes alone cannot solve agent-facing feedback. Error codes may still be useful for tests, logs, and future internal routing, but they are not sufficient for the LLM agent.

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

`CommitNote` intentionally does not render because the commit hash is already primary output.

---

## 3. Current Tool Argument Validation Path

### 3.1 Validation happens before `NoteContext` creation

`MCPServer.handle_call_tool()` currently runs in this order:

```text
validated = _validate_tool_arguments(tool, arguments, call_id, name)
if validation failed: return list[TextContent]

note_context = NoteContext()
pre_result = _run_tool_enforcement(..., note_context)
raw_result = await tool.execute(validated, note_context)
result = note_context.render_to_response(raw_result)
```

Pydantic argument validation failures therefore occur before any `NoteContext` exists.

### 3.2 Validation failure bypasses the normal response pipeline

On Pydantic validation failure, `_validate_tool_arguments()` returns:

```python
[TextContent(type="text", text=f"Invalid input for {name}: {error_details}")]
```

This bypasses:

- `ToolResult.error(...)`
- normal `isError=True` conversion through `ToolResult`
- `ToolResult.error_code`
- `NoteContext`
- `render_to_response()`
- embedded schema resources
- `@tool_error_handler`

The response contains text, but it is not a normal tool error response and it has no note.

### 3.3 `extra="forbid"` will make this path common

Only `GitCommitInput` currently has `model_config = ConfigDict(extra="forbid")`.

All other 50 tool input models currently accept and ignore extra fields. Once they become strict, every extra-field typo will fail in `_validate_tool_arguments()` before the tool executes.

This makes argument validation a first-class error path that must participate in the same agent-facing response architecture as other predictable failures.

---

## 4. Impact Of Applying `extra="forbid"` To All 50 Tool Inputs

### 4.1 The blast radius is central

The strict-input change will not create 50 independent runtime failure paths. It will route failures from all 50 input models into one central method: `_validate_tool_arguments()`.

Affected calls will not reach:

- `tool.execute()`
- enforcement pre-checks
- domain managers
- `@tool_error_handler`
- existing note-producing code

Therefore, the response fix belongs primarily in the server argument-validation path, not inside each individual tool.

### 4.2 Current post-strict agent experience would be incomplete

Without a central response change, an agent passing an extra field would see text similar to:

```text
Invalid input for <tool>: 1 validation error for <InputModel>
<extra_field>
  Extra inputs are not permitted ...
```

Missing from the response:

- a normal `ToolResult.error` shape
- a typed note explaining the fix
- the valid input schema
- an embedded schema resource
- a source-independent way to learn what inputs are valid

### 4.3 Runtime schema is available even without source files

Each tool already exposes input schema through `input_schema`, usually backed by `args_model.model_json_schema()`.

This runtime schema is the only reliable source for agent-facing input guidance when the MCP server is packaged as an executable and Python source files are not exposed.

A solution that expects the agent to inspect Python source files is incompatible with executable-only MCP distribution.

---

## 5. Schema Exposure Constraints From Existing Docs

### 5.1 MCP clients cache tool input schemas

Issue #55 documents that MCP tool JSON schemas are generated at the MCP initialize handshake and cached by the VS Code MCP client for the connection lifetime.

Important implications:

- Tool schemas are available at startup, but may be stale until client reconnect/reload.
- A failed tool call cannot assume the agent will actively rediscover or reread source.
- A response-time schema resource is useful even though schemas also exist in `list_tools`, because it gives the agent the relevant schema at the failure point.

### 5.2 Descriptions are the most compatible guidance carrier

Issue #236 research concluded that maximum agent compatibility requires guidance in JSON Schema `description` fields, because every agent reads those natively. `x-*` JSON Schema extensions are unreliable across MCP clients.

For strict input validation responses, this means the returned schema should preserve field descriptions. The descriptions are not cosmetic; they are the agent-readable contract.

### 5.3 Nested schemas can be hard for clients

Issue #99 documents that some clients struggle with nested/indirect JSON Schema structures, especially `$defs` and `$ref` generated by Pydantic for nested models.

`SafeEditInput` uses nested models (`LineEdit`, `InsertLine`), so its schema is a known high-complexity case. Any response-time schema strategy must account for this existing client-compatibility issue.

This does not decide whether to normalize schemas in this issue, but it identifies a real compatibility risk for returning raw `model_json_schema()` output.

---

## 6. Existing Schema-In-Response Precedent

### 6.1 Scaffold validation already returns schema resources

Issue #120 introduced structured schema resources for scaffold validation errors. The current `tool_error_handler` still contains special handling for `ValidationError` with `schema`:

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

`tests/mcp_server/integration/test_scaffold_validation_e2e.py` asserts that missing required scaffold fields return:

- text error content
- a `schema://validation` JSON resource

### 6.2 Historical rationale for resource content

Issue #120 handover documents why schema resources were used:

- MCP supports multiple content items in a tool result.
- Agents can parse JSON schema separately from human-readable error text.
- This enables AI-driven schema comprehension.

Strict tool-input validation has the same need one layer earlier: argument validation fails before execution, and the agent needs the valid tool input schema in the failure response.

---

## 7. Can An Input Schema Be A Note Today?

### 7.1 Current note rendering is text-only

Current `Renderable` notes expose only:

```python
def to_message(self) -> str: ...
```

`NoteContext.render_to_response()` joins renderable notes into a single text block:

```python
notes_text = "\n".join(n.to_message() for n in renderable)
augmented = list(base.content) + [{"type": "text", "text": notes_text}]
```

There is no note variant that renders a `resource` content item or JSON schema content item.

### 7.2 A full schema does not fit safely into `SuggestionNote`

A JSON schema could be serialized into a `SuggestionNote.message`, but that would:

- collapse structured JSON into plain text
- mix human guidance and machine-readable schema in one block
- lose the existing `schema://validation` resource precedent
- make long schemas noisy and harder for agents to parse
- worsen `$defs`/`$ref` readability for complex inputs such as `SafeEditInput`

A text note can say “remove unknown field X” or “valid top-level fields are A, B, C”. It cannot currently carry a full structured input schema as a note.

### 7.3 Current architecture has two specific gaps

Strict input validation exposes two separate gaps:

1. **Lifecycle gap:** `NoteContext` is created too late for argument validation errors.
2. **Representation gap:** current `NoteEntry` rendering cannot emit structured schema resources.

If the requirement is literally “input schema as note”, the current NoteContext architecture must be extended. If the requirement is “input schema appears in the response with a note explaining it”, then existing `ToolResult.content` resource precedent plus textual notes may be sufficient. Which shape to choose belongs to planning/design, but the current limitation is factual.

---

## 8. Scaffold Artifact Chain Gap

`ScaffoldArtifactTool.execute()` currently does:

```python
async def execute(self, params: ScaffoldArtifactInput, context: NoteContext) -> ToolResult:
    del context
    ...
    artifact_path = await self.manager.scaffold_artifact(params.artifact_type, **kwargs)
```

This `del context` came from a cleanup commit that marked unused parameters after the base execute signature changed. It should be treated as current non-use, not as an architectural decision that scaffold errors should avoid notes.

Current scaffold raise-sites produce no notes:

| Layer | Predictable condition examples | Notes today |
|-------|--------------------------------|-------------|
| `ArtifactRegistryConfig.get_artifact()` | unknown artifact type | none |
| `ArtifactManager.scaffold_artifact()` | missing output path, missing template config, V2 context validation, render context lookup, generated-content validation | none |
| `TemplateScaffolder.validate()` | no template configured, missing fields, loader not configured, generic template missing | partial schema resource for missing fields; no note |
| `JinjaRenderer.get_template()` | template not found | none |
| `FilesystemAdapter` | path outside workspace, write/read system failures | none |

Because `ToolResult.error_code` is not visible to the agent, adding granular scaffold error codes alone would not address this gap. Agent-facing improvement must flow through `ToolResult.content` and `NoteContext`.

---

## 9. Input Models Without `extra="forbid"`

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

`SafeEditInput` also contains nested models (`LineEdit`, `InsertLine`). Strictness for nested models matters because extra fields inside nested objects will surface through the same central argument-validation path.

---

## 10. Line Through The Remaining Tools

The cross-tool line is not “create bespoke error codes for every tool”. The existing architecture points to failure-channel categories:

| Category | Current/expected transport |
|----------|----------------------------|
| Argument schema failure before execution | central server validation response; must include `ToolResult`-style error content, note guidance, and valid input schema |
| Domain validation with corrective advice | `SuggestionNote` plus diagnostic primary result or exception |
| Preflight blocker | `BlockerNote` plus `PreflightError` |
| Execution/recovery failure | `RecoveryNote` plus primary diagnostic result or `ExecutionError` |
| Configuration/resource failure | primary diagnostic content plus note guidance where actionable |

This line applies across the other tools even though many still use generic internal codes today. The agent-facing requirement is not primarily more codes; it is that predictable failures return primary diagnostics and actionable notes through the established response channels.

---

## 11. Research Findings

1. `NoteContext` is a non-negotiable architecture mechanism, not an open design question.
2. Typed notes replaced legacy `hints`, `blockers=`, and `recovery=` channels.
3. `ToolResult` is primary diagnostic transport; `NoteContext` is secondary actionable context transport.
4. `ToolResult.error_code` is not visible to the LLM client and cannot solve agent-facing context by itself.
5. Applying `extra="forbid"` to 50 models routes extra-field failures through `_validate_tool_arguments()` before `NoteContext` exists.
6. The current argument-validation failure path bypasses `ToolResult.error`, `render_to_response`, `@tool_error_handler`, and schema resources.
7. Runtime input schemas are available from `tool.input_schema` / `args_model.model_json_schema()` and are required in executable-only distribution where source files are not exposed.
8. Response-time schema resources have precedent in scaffold validation (`schema://validation`) and were introduced specifically so agents can parse schema separately from error text.
9. MCP clients cache tool schemas at initialization, so response-time schema context remains useful at the moment of failure.
10. Current `NoteEntry` rendering is text-only. A full input schema cannot be represented as a structured note without extending NoteContext rendering or returning schema as `ToolResult.content` alongside text notes.
11. `SafeEditInput` is a known complex schema case because nested models generate `$defs`/`$ref`, which prior research identified as problematic for some clients.
12. Scaffold predictable errors still discard `NoteContext` (`del context`) and produce no notes for 14 predictable raise-sites.

---

## 12. Planning Inputs (Facts And Constraints, Not Decisions)

The next phase should treat these as constraints:

- Strict input validation requires a central server-side error response path.
- That path must not move `NoteContext` creation earlier. `_validate_tool_arguments` must return `ToolResult` (with `is_error=True` and a `schema://validation` EmbeddedResource) instead of a bare `list[TextContent]`. `NoteContext` remains created after argument validation, as today.
- The response must include a primary diagnostic text and the valid runtime input schema as an embedded resource.
- The schema must be generated from runtime tool schema data, not source inspection.
- The schema response must preserve field descriptions because descriptions are the most compatible agent guidance channel.
- `NoteContext`/`NoteEntry` must not be extended with structured resource rendering. Notes remain textual (`to_message() -> str`). Schema always goes via `ToolResult.content` resource, consistent with the `schema://validation` precedent.
- `tool_error_handler` must remain context-agnostic (issue #283 contract unchanged).
- Scaffold predictable errors are in scope: `del context` must be removed from `ScaffoldArtifactTool`, and `NoteContext` must be propagated through `ArtifactManager` and the full scaffold chain (TemplateScaffolder, JinjaRenderer, FilesystemAdapter), following the `GitManager` reference pattern.
- Granular error codes for scaffold raise-sites are not in scope. Existing codes (`ERR_CONFIG`, `ERR_VALIDATION`, etc.) remain. Agent-facing improvement flows through typed notes and `ToolResult.content` text.
- `$defs`/`$ref` in tool input schemas is a confirmed defect, not a hypothetical risk. VS Code / Copilot Chat cannot construct tool calls when `input_schema` contains `$ref` (confirmed in issue #99 C9, commit `5592979e`; fix applied only to `CreateIssueTool` via `_resolve_schema_refs()`). The `_resolve_schema_refs()` utility in `issue_tools.py` must be moved to a shared location and applied to all tools via `BaseTool.input_schema`. This is a pre-condition for safe `extra="forbid"` application to `SafeEditInput`.

---

## 13. Constraint Decisions From Design Preparation (2026-05-07)

These five constraint decisions were established through architectural review against `ARCHITECTURE_PRINCIPLES.md` after research v4. They belong in research because they close design options, not open them.

### C1 — Lifecycle gap: `_validate_tool_arguments` returns `ToolResult`

**Decision:** Optie B. `_validate_tool_arguments` is changed to return `ToolResult` on failure (with `is_error=True`, error text, and `schema://validation` EmbeddedResource from `tool.input_schema`). `NoteContext` is not created earlier.

**Rationale:** Moving `NoteContext` creation earlier would give `_validate_tool_arguments` a second responsibility (SRP §1.1) and introduce NoteContext as a dependency in the server dispatch layer where it does not belong (Law of Demeter §7, Cohesion §10). The schema resource in `ToolResult.content` is sufficient actionable guidance for argument validation failures (YAGNI §9). The `schema://validation` resource precedent from issue #120 applies directly.

### C2 — Representation gap: NoteContext not extended

**Decision:** `NoteContext`/`NoteEntry` are not extended with structured resource rendering. `to_message() -> str` remains the only rendering interface for notes.

**Rationale:** Adding resource-type notes would give NoteContext two responsibilities — textual actionable guidance and structured machine-readable data (SRP §1.1). Schema belongs in `ToolResult.content` as a resource, which is the existing SSOT for structured response content (DRY §2). No concrete case in this issue requires schema-as-note (YAGNI §9).

### C3 — Scaffold chain: in scope

**Decision:** `del context` removed from `ScaffoldArtifactTool`. `NoteContext` propagated through `ArtifactManager` and the full scaffold chain (TemplateScaffolder, JinjaRenderer, FilesystemAdapter). Reference pattern: `GitManager`.

**Rationale:** The error taxonomy established by this issue applies to the scaffold chain's 14 raise-sites. Leaving them outside scope makes the taxonomy a paper contract inconsistent with the codebase (DRY §2, Explicit §8). The `del context` comment documents a temporary non-use state, not an architectural decision.

### C4 — Error codes: not in scope

**Decision:** No new granular error codes for the scaffold chain or other tools. Existing codes remain.

**Rationale:** `ToolResult.error_code` is not visible to the LLM client (research §2.1). Granular codes would serve only tests and logs, with no agent-facing benefit. No current consumer routes on specific codes (YAGNI §9).

### C5 — SafeEditInput / schema normalization: in scope as DRY refactor

**Decision:** `_resolve_schema_refs()` moved from `issue_tools.py` to a shared location and applied to all tools via `BaseTool.input_schema`. `SafeEditInput` receives `extra="forbid"` after this pre-condition is met.

**Rationale:** The `$defs`/`$ref` defect is confirmed, not hypothetical: VS Code cannot construct tool calls with `$ref` in input schemas (issue #99 C9, commit `5592979e`, test `test_create_issue_schema.py`). `SafeEditInput` (`LineEdit`, `InsertLine`) still has this defect. The fix utility already exists; applying it broadly is a DRY refactor (§2), not new infrastructure (YAGNI §9 does not apply to fixing a confirmed defect).

---

## Related Documentation And Evidence

- `docs/development/issue300/research.md` - three communication paths; ToolResult primary, NoteContext secondary, exceptions infrastructure
- `docs/development/issue300/design.md` - no new communication paths constraint
- Historical issue #283 planning from commit `c7644435` - C3/C4 NoteContext wiring and flag-day migration rationale
- `docs/development/issue295/research.md` - canonical preflight/recovery NoteContext patterns
- `docs/development/issue298/research-state-json-authoritative-and-subphase-persistence.md` - tool-layer error handling with `RecoveryNote + ToolResult.error`
- `docs/development/archive/issue120/SESSIE_OVERDRACHT_IMP_20260122.md` - schema resource rationale for validation errors
- `docs/development/archive/issue55/mcp_schema_caching_limitation.md` - MCP client schema caching limitation
- `docs/development/archive/issue236/research.md` - schema `description` as maximum compatibility guidance carrier
- `docs/development/archive/issue99/research.md` - `$defs`/`$ref` compatibility issues for nested tool schemas
- `tests/mcp_server/integration/test_blocker_recovery_note_dispatch.py` - notes survive exceptions and render on error/success
- `tests/mcp_server/integration/test_scaffold_validation_e2e.py` - schema resource returned on scaffold validation error
- `mcp_server/server.py` - argument validation order and response conversion
- `mcp_server/core/operation_notes.py` - current text-only note model and renderer
- `mcp_server/core/error_handling.py` - schema-resource special case and context-agnostic error conversion
- `mcp_server/tools/scaffold_artifact.py` - current `del context` scaffold gap
- `mcp_server/tools/safe_edit_tool.py` - nested input schema case (`LineEdit`, `InsertLine`)
- `mcp_server/tools/base.py` - execute contract includes `context: NoteContext`
- `mcp_server/tools/issue_tools.py` - `_resolve_schema_refs()` utility: inlines `$defs`/`$ref` in JSON Schema; currently module-local
- `tests/mcp_server/unit/tools/test_create_issue_schema.py` - C9 contract: `input_schema` must not contain `$ref`/`$defs`; confirms the defect is real

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-07 | imp-agent | Initial research; mixed research with premature error-code design |
| 2.0 | 2026-05-07 | imp-agent | Rewritten around NoteContext end-to-end path, but still framed some settled behavior as open questions |
| 3.0 | 2026-05-07 | imp-agent | Added docs/history rationale, strict-input central failure analysis, schema-resource precedent, and NoteContext representation/lifecycle gaps |
| 4.0 | 2026-05-07 | imp-agent | Deepened reference/history evidence, strict-input agent experience, schema-as-note gap, MCP schema caching, description guidance, and nested schema compatibility |
| 5.0 | 2026-05-07 | imp-agent | Added §12 updated planning inputs (5 closed constraints) and §13 constraint decisions C1–C5 from architectural review against ARCHITECTURE_PRINCIPLES.md |
