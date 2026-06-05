<!-- docs\development\issue348\research.md -->
<!-- template=research version=8b7bb3ab created=2026-06-05T18:31Z updated=2026-06-05 -->
# Issue #348 Research

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-06-05

---

## Purpose

Establish whether `safe_edit_file` can safely stop returning unified diffs in its default MCP response without degrading the useful status and validation feedback that agents rely on.

## Problem Statement

`safe_edit_file` currently returns the full unified diff in default tool responses. This adds token overhead and visual noise to agent sessions, even though the status and validation information that agents actually need is much smaller and already separable from the diff payload.

## Research Goals

- Determine whether status feedback is mechanically and semantically separable from diff feedback.
- Map the smallest safe blast radius for removing diff from the default response contract.
- Identify tests and documentation surfaces that currently encode the diff-heavy response behavior.
- Establish an approved strategy for the agent-facing `safe_edit_file` contract.

## Scope In

- The agent-facing MCP input and output contract of `safe_edit_file`
- Response composition in `mcp_server/tools/safe_edit_tool.py`
- Result formatting via `ToolResult.text(...)`
- Unit and integration test expectations tied to diff presence
- Documentation examples that describe or demonstrate current response behavior

## Scope Out

- Redesign of the validation engine itself
- New response channels, streaming protocols, or telemetry formats
- Broader MCP-wide response contract changes outside `safe_edit_file`
- External caller compatibility analysis beyond LLM agents
- Implementation details for future local-LLM or non-agent execution paths

## Prerequisites

- Read the issue definition for #348
- Read `ARCHITECTURE_PRINCIPLES.md`
- Read `DOCUMENTATION_STANDARD.md`
- Inspect current `safe_edit_file` response builders and related tests

## Background

Issue #348 targets a narrow but high-frequency UX problem in the MCP server: `safe_edit_file` responses are verbose by default because they embed the full unified diff in the text returned to the agent. The issue motivation is agent-side efficiency and clarity, not a functional defect in file mutation itself.

The current branch context indicates this is a research-phase feature issue, so the goal here is to bound the problem, identify the affected surfaces, and capture a strategy decision for later phases without drifting into design or implementation commitments.

## Findings

### 1. Status feedback is already built separately from diff feedback

The current implementation composes useful status text first and only prepends diff output afterward.

| Surface | Evidence | Conclusion |
|---|---|---|
| `verify_only` response | `mcp_server/tools/safe_edit_tool.py` builds `text = f"{status}{response.issues}"` in `_build_verify_response()` before checking `response.diff` | Validation result text is independent of diff payload |
| strict rejection response | `_build_rejection_response()` constructs the rejection message and guidance first, then conditionally prepends diff | Error reporting is independent of diff payload |
| success / interactive response | `_write_and_respond()` builds `✅ File saved successfully.` plus warnings or non-blocking issues before diff prepend | Success and warning feedback are independent of diff payload |

Observed pattern in all three response builders:
- build compact status / validation text
- if `response.diff` exists, prepend `**Diff Preview:**` block
- return the final text through `ToolResult.text(...)`

Research conclusion: stripping diff at the response-builder layer does not require altering the status or validation message logic.

### 2. The diff is presentation payload, not functional status data

`ToolResult` does not model diff and status as separate typed channels. The current separation is still clear because the diff is merely concatenated into the text blob after status creation.

| Surface | Evidence | Conclusion |
|---|---|---|
| `ToolResult.text(...)` | `mcp_server/tools/tool_result.py` returns a single `{"type": "text", "text": text}` item | No deeper coupling exists in the result model |
| `show_diff` / `response.diff` usage | Diff is only consumed in the conditional prepend paths in `safe_edit_tool.py` | Diff removal can be localized to the tool response-build layer |

Research conclusion: the diff is not carrying hidden machine-readable semantics inside the MCP result model.

### 3. The current blast radius is small and local

The affected surfaces are narrow and visible.

| Area | Evidence | Impact |
|---|---|---|
| production response builders | `mcp_server/tools/safe_edit_tool.py` response-building methods | Primary contract change surface |
| input model | `show_diff: bool = True` on `SafeEditInput` | Public parameter surface if the strategy removes exposure |
| tests | `tests/mcp_server/unit/tools/test_safe_edit_tool.py` asserts `"**Diff Preview:**"` presence | Tests will need contract-aligned updates |
| docs | response examples in tooling docs and historical safe-edit planning docs | Documentation must be updated to match compact output |

Research conclusion: no broad runtime blast radius has been found beyond `safe_edit_file` itself, its tests, and response-format documentation.

### 4. There is no evidence of non-agent external callers that require diff-in-response behavior

The issue statement and current session guidance both frame the consumers as LLM agents. No repo evidence found a distinct external consumer boundary that must preserve the exposed diff toggle as part of a public compatibility contract.

Research conclusion: this supports a clean-break strategy on the agent-facing tool contract.

### 5. Existing tests encode the current verbose contract and must not be mistaken for a deeper architectural dependency

Current tests assert diff presence and duplication behavior, for example in `tests/mcp_server/unit/tools/test_safe_edit_tool.py`.

What these tests prove:
- current response contract includes diff output
- duplicate diff regressions were previously important enough to test

What they do not prove:
- that agents need diff output to function
- that status text depends on diff text
- that diff must remain part of the exposed API long term

Research conclusion: tests are part of the blast radius, but not evidence against compact-response separation.

## Architectural Constraints

- Keep responsibilities narrow: response compaction should remain a local concern of `safe_edit_file` response composition, not spill into unrelated tool infrastructure.
- Preserve explicit, actionable status feedback for success, warnings, and validation failures.
- Do not replace the current problem with heuristic complexity such as file-size-dependent diff rules or multiple hidden output modes.
- Avoid introducing a new public toggle if the goal is to prevent accidental verbose output from agent callers.
- Do not let documentation or tests become the de facto source of truth over the intended tool contract.

## Existing Patterns / Prior Art

- Other MCP tools in this repository typically return compact `ToolResult.text(...)` messages rather than large textual payloads.
- `safe_edit_file` already follows the same compact pattern internally for status construction; the diff prepend is the outlier.
- The existing `show_diff` field demonstrates that diff generation was already considered optional behavior, even though it is exposed with a verbose default.

## Blast Radius

### Production surfaces
- `mcp_server/tools/safe_edit_tool.py`
- potentially the `SafeEditInput` schema in the same module if the exposed parameter is removed

### Test surfaces
- `tests/mcp_server/unit/tools/test_safe_edit_tool.py`
- any integration tests that assert diff preview presence or exact response phrasing

### Documentation surfaces
- tool reference docs describing `safe_edit_file`
- response examples that currently show `**Diff Preview:**` blocks
- historical safe-edit notes where current response behavior is explicitly illustrated

## Risks And Assumptions

| Type | Item |
|---|---|
| Assumption | LLM agents are the only meaningful callers that matter for compatibility on this boundary |
| Assumption | Internal diff generation may still be useful later for other execution contexts, such as local non-agent workflows |
| Risk | Removing the exposed diff toggle without updating tests and docs will create misleading failures and stale contract examples |
| Risk | If hidden consumers exist outside current repo evidence, they could rely on the existing `show_diff` field or diff-heavy text |
| Risk | If status compaction accidentally removes `response.issues`, useful validation feedback would regress even if diff removal itself is safe |

## Implementation Notes For Later Phases

- Internal diff-generation capability may remain private unless implementation reveals it is truly unused and removable without widening blast radius.
- Active documentation examples for `safe_edit_file` must be updated to the compact-response contract; historical notes may remain historical when they are not active product documentation.
- Implementation should still audit response-text assertions outside the known safe-edit test file, but this is an execution check rather than an unresolved research question.

## Expected Results

Implementation should be able to operate from the following bounded outcome frame without a separate substantive design phase:
- `safe_edit_file` returns compact, actionable status output by default
- the agent-facing contract no longer exposes a diff toggle that can accidentally reintroduce verbose responses
- useful validation and status messaging remains intact
- the production blast radius stays local to the safe-edit tool contract, tests, and documentation examples

## Approved Strategy

### Boundary / consumer scope
Agent-facing MCP input and output contract of `safe_edit_file`.

### Selected strategy
Clean break.

### Rationale
There is no evidence of external callers beyond LLM agents. For these consumers, compact and predictable status feedback is more valuable than a public diff toggle that can accidentally reintroduce large responses. Status and diff are already separated strongly enough in the current implementation to support this change with a small blast radius.

### Constraints for later phases
- Remove `show_diff` from the public agent-facing input contract.
- Remove diff preview from the default `safe_edit_file` response contract.
- Preserve the current useful status and validation feedback semantics.
- Internal diff functionality may remain as a private capability for future non-agent contexts.
- Tests and documentation must be updated to reflect the compact-response contract.

## Related Documentation
- `docs/coding_standards/ARCHITECTURE_PRINCIPLES.md`
- `docs/coding_standards/DOCUMENTATION_STANDARD.md`
- `docs/development/issue-38-enhanced-safe-edit-planning.md`
- `docs/reference/mcp/tools/editing.md`

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-05 | Agent | Initial draft |
