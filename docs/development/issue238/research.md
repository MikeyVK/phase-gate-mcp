<!-- docs\development\issue238\research.md -->
<!-- template=research version=8b7bb3ab created=2026-06-06T10:18Z updated= -->
# Refactor create_issue: split scaffolding from submission (mirror submit_pr pattern)

**Status:** PRELIMINARY  
**Version:** 1.0  
**Last Updated:** 2026-06-06

---

## Purpose

Provide evidence-backed input for design and planning of the create_issue refactor.

## Scope

**In Scope:**
mcp_server/tools/issue_tools.py (CreateIssueTool, IssueBody, CreateIssueInput), mcp_server/scaffolding/templates/concrete/issue.md.jinja2, affected tests, tool reference docs, slash-prompt for co-agent issue creation workflow

**Out of Scope:**
issues.yaml body_fields extension (original three-unity scope, superseded), IssueTypeEntry schema changes, dynamic input_schema description-append, model_validator soft hints

## Prerequisites

Read these first:
1. docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
2. submit_pr tool pattern (pr_tools.py:SubmitPRTool)
---

## Problem Statement

CreateIssueTool violates SRP by combining four concerns: semantic validation, Jinja2 body rendering, label assembly, and GitHub API submission. The three-unity architecture originally proposed in issue #238 (issues.yaml + IssueBody Pydantic model + issue.md.jinja2) is superseded by a cleaner split modelled on the existing submit_pr pattern: scaffold_artifact(artifact_type='issue') generates the body; create_issue accepts a pre-rendered string and handles label assembly + API submission only.

## Research Goals

- Identify current create_issue responsibilities and which belong where after the split
- Map blast radius across production code, tests, and documentation
- Confirm the issue artifact type is already registered and usable
- Identify architectural constraints and forbidden approaches
- Determine whether the H1 duplicate bug in issue.md.jinja2 is in scope
- Establish an Approved Strategy for the affected boundary (API consumers that currently pass IssueBody)

---

## Background

Issue #238 was originally scoped as a 'three-unity architecture': structured body_fields per issue type in issues.yaml, IssueBody Pydantic model as a per-type validation contract, and issue.md.jinja2 as the presentation layer. Research revealed this approach requires complex schema injection and per-type guidance in static MCP schema fields — architecturally inferior to the existing submit_pr split pattern, which the codebase already uses successfully. The submit_pr pattern lets scaffold_artifact generate the rendered body, and the submission tool receives a pre-rendered string. The issue artifact type already exists in the scaffolding registry.

---

## Findings

### Current CreateIssueTool Responsibilities

`CreateIssueTool` (mcp_server/tools/issue_tools.py) currently combines four distinct concerns:

| Responsibility | Method | Belongs where after split |
|---|---|---|
| Semantic validation | `validate_issue_params()` (GitHubManager) | Stays in `create_issue` — pure input guard |
| Body rendering | `_render_body(body: IssueBody, title)` | Moves to `scaffold_artifact(artifact_type='issue')` |
| Label assembly | `_assemble_labels(params)` | Stays in `create_issue` — policy concern |
| GitHub API submission | `manager.create_issue(...)` | Stays in `create_issue` |

The rendering concern is the sole SRP violation. Label assembly is a legitimate tool responsibility: it translates structured metadata (issue_type, scope, priority, is_epic, parent_issue) into label strings using `IssueConfig`, `ContractsConfig`, `LabelConfig`, and `ScopeConfig`. This mirrors how `submit_pr` still handles the git transaction — not all internal logic is inappropriate for a submission tool.

### Prior Art: submit_pr Pattern

`SubmitPRTool` (mcp_server/tools/pr_tools.py) already implements the desired split:

- `SubmitPRInput.body: str | None` — accepts pre-rendered markdown
- No Jinja2 renderer, no template logic inside the tool
- `scaffold_artifact(artifact_type='pr', ...)` generates the body upstream (co-agent slash-prompt)
- Tool concerns: git transaction + GitHub PR API call

The `issue` artifact type is already registered in the scaffolding registry (user confirmed; `scaffold_artifact(artifact_type='issue')` is a valid call). The template `mcp_server/scaffolding/templates/concrete/issue.md.jinja2` already renders conditionally based on which optional fields are populated, making it type-neutral by default.

### Blast Radius

#### Production Files

| File | Change |
|---|---|
| `mcp_server/tools/issue_tools.py` | Remove `IssueBody` model, `_render_body()`, `JinjaRenderer` import and `self._renderer`. Change `CreateIssueInput.body: IssueBody` → `body: str`. Remove `body` JSON-string coercion validator. Remove Jinja2/template imports (`introspect_template_with_inheritance`, `compute_version_hash`, `get_template_root`). |
| `mcp_server/server.py` | No constructor signature change for `CreateIssueTool` (all config deps stay for label assembly). Only internal `self._renderer` goes away — no server.py edit needed. |
| `mcp_server/scaffolding/templates/concrete/issue.md.jinja2` | Fix duplicate H1 bug: line 49 renders `# {{ title }}` but GitHub already renders the issue title as H1. This is independent of the split and can be its own cycle. |

#### Documentation Files

| File | Change |
|---|---|
| `docs/reference/mcp/tools/github.md` | Update `body` parameter: `IssueBody` object → `str` (pre-rendered markdown). Remove IssueBody fields subsection. |
| `docs/reference/mcp/MCP_TOOLS.md` | Update `create_issue` body parameter description to reflect `str`. |
| `docs/reference/mcp/config-loading-architecture.md` | Verify whether `JinjaRenderer` appears in the CreateIssueTool config dependency table; update if present. |

#### Test Files

| File | Status after refactor |
|---|---|
| `tests/mcp_server/unit/tools/test_issue_body.py` | **Deleted** — tests `_render_body()` which is removed |
| `tests/mcp_server/unit/tools/test_render_body_scaffold_header.py` | **Deleted** — tests `_render_body()` scaffold header output |
| `tests/mcp_server/unit/tools/test_issue_tools.py` | **Updated** — constructs `CreateIssueInput` with `IssueBody`; replace with `body: str` |
| `tests/mcp_server/integration/test_create_issue_e2e.py` | **Updated** — imports and uses `IssueBody`; replace with plain markdown string |
| `tests/mcp_server/unit/integration/test_all_tools.py` | **Updated** — imports `IssueBody`; update tool construction and input |
| `tests/mcp_server/test_support.py` | **Updated** — `make_create_issue_tool` factory may need adjustment |
| `tests/mcp_server/unit/integration/test_github.py` | **Verify** — CreateIssueTool test; likely uses IssueBody indirectly |

### Architectural Constraints

- **SRP**: no rendering logic in submission tools (confirmed by ARCHITECTURE_PRINCIPLES.md)
- **ISP**: `create_issue` should accept the narrowest interface needed; `body: str` is correct
- **Constructor injection**: no object construction inside `execute()` — already compliant; `self._renderer` lives in `__init__`. After removal, no new injection needed.
- **No module-level config loading**: not applicable here
- **CQS**: validate + assemble + submit is a single command; no state read mixed with write

### IssueBody Residual Value Analysis

`IssueBody` is a Pydantic model that defines six fields (`problem`, `expected`, `actual`, `context`, `steps_to_reproduce`, `related_docs`) with `extra="forbid"`. Research finds it has zero residual value after the split, for four reasons:

| Concern | Current IssueBody role | Why IssueBody is redundant |
|---|---|---|
| Field definition | Defines the same six fields passed to the Jinja2 template | `issue` artifact context schema already defines these fields with `additionalProperties: false` |
| Validation | `extra="forbid"` rejects unknown keys | Scaffolding context schema enforces the same constraint at the scaffolding boundary |
| Consumers | Used only in `CreateIssueInput.body` and `_render_body()` | Both are removed by this refactor; no external consumers exist |
| JSON string coercion | `coerce_body_from_json_string` handled MCP agents sending a JSON string | Unnecessary after `body: str`; agents pass pre-rendered markdown directly |

**Verdict:** `IssueBody` is deleted entirely. The scaffolding pipeline owns the validation concern; no intermediate model layer is needed or appropriate.

### Approved Strategy

**Boundary:** All agents and tools that currently call `create_issue` with a structured `IssueBody` object as the `body` field.

**Selected strategy:** Clean break.

**Rationale:** `IssueBody` was an internal rendering convenience with no external consumers. The scaffolding pipeline already owns field validation at the correct layer. A bridge or backward-compat variant would preserve a concern that belongs in scaffolding, not in a submission tool.

**Constraints for later phases:**
- `IssueBody` is deleted entirely — no retained schema variant
- Design must specify `body: str` field definition (required, markdown, no default)
- No backward-compatibility tests for `IssueBody` or `_render_body()`; old functionality must not be visible in the test suite after completion
- Planning must include test deletion (`test_issue_body.py`, `test_render_body_scaffold_header.py`) and test updates (`test_issue_tools.py`, `test_create_issue_e2e.py`, `test_all_tools.py`, `test_support.py`) as explicit TDD cycles
- Documentation cycle must cover `github.md`, `MCP_TOOLS.md`, `config-loading-architecture.md`
- H1 duplicate bug in `issue.md.jinja2` is a separate cycle (own scope, own TDD cycle)

## Open Questions

- ❓ Does the `issue` artifact type context schema need type-aware enrichment to guide co-agent slash-prompt usage authoritatively? Residual quality-of-life concern; not a blocker for the refactor.
- ✅ `validate_issue_params()` in `GitHubManager` is retained: semantic guard independent of rendering.
- ✅ `IssueBody` is deleted entirely: zero residual value after split (see analysis above).
- ✅ H1 duplicate fix in `issue.md.jinja2` is a separate cycle.


## Related Documentation
- **[docs/reference/mcp/tools/github.md][related-1]**
- **[mcp_server/tools/issue_tools.py][related-2]**
- **[mcp_server/tools/pr_tools.py][related-3]**
- **[mcp_server/scaffolding/templates/concrete/issue.md.jinja2][related-4]**
- **[tests/mcp_server/unit/tools/test_issue_body.py][related-5]**
- **[tests/mcp_server/unit/tools/test_render_body_scaffold_header.py][related-6]**
- **[tests/mcp_server/unit/tools/test_issue_tools.py][related-7]**

<!-- Link definitions -->

[related-1]: docs/reference/mcp/tools/github.md
[related-2]: mcp_server/tools/issue_tools.py
[related-3]: mcp_server/tools/pr_tools.py
[related-4]: mcp_server/scaffolding/templates/concrete/issue.md.jinja2
[related-5]: tests/mcp_server/unit/tools/test_issue_body.py
[related-6]: tests/mcp_server/unit/tools/test_render_body_scaffold_header.py
[related-7]: tests/mcp_server/unit/tools/test_issue_tools.py

---

## Adopted Design Decisions

Design phase is skipped; the decisions below are approved by the product owner and sufficient for planning.

| Decision | Choice | Rationale |
|---|---|---|
| `body` field type | `body: str` — required, no default | Mirrors `SubmitPRInput.body`; pre-rendered markdown passed by caller |
| `body` field description | `"Issue body as pre-rendered markdown. Use scaffold_artifact(artifact_type='issue') to generate."` | Guides agents to the correct upstream tool |
| `CreateIssueTool` constructor | Unchanged — all config deps (`IssueConfig`, `MilestoneConfig`, `ContractsConfig`, `LabelConfig`, `ScopeConfig`, `GitConfig`) stay for label assembly | No new injection needed; only `self._renderer` assignment is removed |
| `input_schema` property | Unchanged — still injects enums for `issue_type`, `priority`, `scope` and `maxLength` for `title` | `body` is now a plain `str` field; no schema customization needed for it |

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-06 | Agent | Initial draft |
| 1.1 | 2026-06-06 | Agent | Added adopted design decisions; design phase skipped (product owner approval) |