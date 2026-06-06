<!-- docs\development\issue238\planning.md -->
<!-- template=planning version=130ac5ea created=2026-06-06T11:48Z updated= -->
# Refactor create_issue: split scaffolding from submission (#238)

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-06-06

---

## Purpose

Define the implementation cycles for removing IssueBody and _render_body() from CreateIssueTool, replacing body: IssueBody with body: str, and fixing the H1 duplicate bug in issue.md.jinja2.

## Scope

**In Scope:**
mcp_server/tools/issue_tools.py, mcp_server/scaffolding/templates/concrete/issue.md.jinja2, tests/mcp_server/unit/tools/test_issue_body.py, tests/mcp_server/unit/tools/test_render_body_scaffold_header.py, tests/mcp_server/unit/tools/test_issue_tools.py, tests/mcp_server/integration/test_create_issue_e2e.py, tests/mcp_server/unit/integration/test_all_tools.py, tests/mcp_server/test_support.py
mcp_server/tools/issue_tools.py, mcp_server/scaffolding/templates/concrete/issue.md.jinja2, tests/mcp_server/unit/tools/test_issue_body.py, tests/mcp_server/unit/tools/test_render_body_scaffold_header.py, tests/mcp_server/unit/tools/test_issue_tools.py, tests/mcp_server/integration/test_create_issue_e2e.py, tests/mcp_server/unit/integration/test_all_tools.py, tests/mcp_server/unit/integration/test_github.py, tests/mcp_server/test_support.py
**Out of Scope:**
issues.yaml body_fields extension, IssueTypeEntry schema changes, dynamic input_schema description-append, model_validator hints, type-aware IssueContext schema enrichment, documentation updates (documentation phase)

## Prerequisites

Read these first:
1. docs/development/issue238/research.md — Approved Strategy and adopted design decisions
2. mcp_server/tools/pr_tools.py:SubmitPRInput — reference pattern for body: str
---

## Summary

Three TDD cycles: (C1) refactor CreateIssueTool to accept body: str; (C2) delete and update all affected tests; (C3) fix H1 duplicate in issue.md.jinja2. Documentation lands in the documentation phase.

---

## Dependencies

- C2 depends on C1 (test files reference IssueBody and _render_body which are removed in C1)
- C3 is independent of C1/C2 (template-only change)

---

## TDD Cycles


### Cycle 1: C1 — Remove IssueBody and _render_body from CreateIssueTool

**Goal:** CreateIssueTool accepts body: str. IssueBody model, _render_body(), coerce_body_from_json_string validator, and all Jinja2/template imports removed from issue_tools.py.

**Tests:**
- RED: write test asserting CreateIssueInput accepts body: str and rejects body: IssueBody-style dict — fails on current code
- GREEN: remove IssueBody, _render_body(), coerce_body_from_json_string; change body field to str; remove JinjaRenderer, introspect_template_with_inheritance, compute_version_hash, get_template_root imports
- REFACTOR: verify no dead imports remain; run quality gates on mcp_server/tools/issue_tools.py

**Success Criteria:**
- CreateIssueInput.body is str, required, no default
- IssueBody class does not exist in issue_tools.py
- _render_body method does not exist in CreateIssueTool
- coerce_body_from_json_string validator does not exist
- No Jinja2 or template utility imports remain in issue_tools.py
- grep for IssueBody and _render_body across codebase returns zero hits outside files scheduled for C2 update
- mypy and pylint pass on changed file (scope: issue_tools.py)



### Cycle 2: C2 — Delete and update affected test files

**Goal:** Test suite is clean: IssueBody-specific tests deleted, surviving tests updated to use body: str. No references to IssueBody or _render_body remain anywhere in the test suite.

**Tests:**
- RED: run full test suite — expect failures in test_issue_body.py, test_render_body_scaffold_header.py, test_issue_tools.py, test_create_issue_e2e.py, test_all_tools.py, test_support.py
- GREEN: delete test_issue_body.py and test_render_body_scaffold_header.py; update remaining files to use body: str (plain markdown string)
- REFACTOR: run full test suite — all tests pass; no IssueBody or _render_body references remain in test suite

**Success Criteria:**
- tests/mcp_server/unit/tools/test_issue_body.py does not exist
- tests/mcp_server/unit/tools/test_render_body_scaffold_header.py does not exist
- tests/mcp_server/unit/tools/test_issue_tools.py passes with body: str inputs
- tests/mcp_server/integration/test_create_issue_e2e.py passes with body: str inputs
- tests/mcp_server/unit/integration/test_all_tools.py passes with body: str inputs
- RED: run full test suite — expect failures in test_issue_body.py, test_render_body_scaffold_header.py, test_issue_tools.py, test_create_issue_e2e.py, test_all_tools.py, test_github.py, test_support.py
- GREEN: delete test_issue_body.py and test_render_body_scaffold_header.py; update remaining files to use body: str (plain markdown string), including test_github.py
- grep for IssueBody and _render_body in tests/ returns zero hits
- mypy and pylint pass on all changed test files

**Dependencies:** C1


### Cycle 3: C3 — Fix H1 duplicate in issue.md.jinja2

**Goal:** Remove the redundant # {{ title }} H1 from the markdown_header block. GitHub renders the issue title as H1 natively; the template must not duplicate it.
- tests/mcp_server/unit/integration/test_github.py passes with body: str inputs
- tests/mcp_server/unit/integration/test_all_tools.py passes with body: str inputs
- RED: write test asserting scaffold_artifact(artifact_type='issue', ...) output does not contain a markdown H1 line (^# ) — fails on current template
- GREEN: remove # {{ title }} line from markdown_header block in issue.md.jinja2; keep summary rendering
- REFACTOR: verify rendered output for minimal and full context — no H1 present, summary still renders, all other sections intact

**Success Criteria:**
- issue.md.jinja2 markdown_header block does not render a # H1 line
- Rendered output for any context does not start with # <title>
- Summary section still renders when summary is provided
- All other sections (Problem, Expected, Actual, Steps, Context, Related Docs) render correctly
- Existing passing tests for issue scaffold remain green
- mypy and pylint pass on changed template (validate_template gate)


---

## Risks & Mitigation

- **Risk:** Non-test code paths that construct IssueBody or call _render_body indirectly (e.g. integration fixtures, conftest helpers)
  - **Mitigation:** C1 exit criterion: grep for IssueBody and _render_body across entire codebase returns zero hits outside deleted/updated files
- **Risk:** test_all_tools.py constructs CreateIssueInput with IssueBody — compile error after C1 before C2
  - **Mitigation:** C1 and C2 are committed sequentially; C2 GREEN phase must resolve all import/compile errors before quality gates run

- **Risk:** test_all_tools.py and test_github.py both construct CreateIssueInput with IssueBody — compile errors after C1 before C2

## Milestones

- C1 GREEN: CreateIssueTool accepts body: str, IssueBody gone from production code
- C2 GREEN: test suite fully clean, no IssueBody traces
- C3 GREEN: issue.md.jinja2 H1 duplicate fixed
- Documentation phase: github.md, MCP_TOOLS.md, config-loading-architecture.md updated

## Related Documentation
- **[docs/development/issue238/research.md][related-1]**
- **[mcp_server/tools/issue_tools.py][related-2]**
- **[mcp_server/tools/pr_tools.py][related-3]**
- **[mcp_server/scaffolding/templates/concrete/issue.md.jinja2][related-4]**
- **[tests/mcp_server/unit/tools/test_issue_body.py][related-5]**
- **[tests/mcp_server/unit/tools/test_render_body_scaffold_header.py][related-6]**
- **[tests/mcp_server/unit/integration/test_github.py][related-7]**


<!-- Link definitions -->

[related-1]: docs/development/issue238/research.md
[related-2]: mcp_server/tools/issue_tools.py
[related-3]: mcp_server/tools/pr_tools.py
[related-4]: mcp_server/scaffolding/templates/concrete/issue.md.jinja2
[related-5]: tests/mcp_server/unit/tools/test_issue_body.py
[related-6]: tests/mcp_server/unit/tools/test_render_body_scaffold_header.py
[related-5]: tests/mcp_server/unit/tools/test_issue_body.py
[related-6]: tests/mcp_server/unit/tools/test_render_body_scaffold_header.py
[related-7]: tests/mcp_server/unit/integration/test_github.py

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|--------|
| 1.0 | 2026-06-06 | Agent | Initial draft |
| 1.1 | 2026-06-06 | Agent | QA FAIL fix: add test_github.py to C2; add deliverables payload section |

---

## Deliverables Payload

Saved via `save_planning_deliverables(issue_number=238, ...)`.

| Cycle | cycle_number | Key Deliverables |
|---|---|---|
| C1 | 1 | IssueBody removed, body: str in issue_tools.py, quality gates pass |
| C2 | 2 | IssueBody tests deleted; test_issue_tools, test_create_issue_e2e, test_all_tools, test_github, test_support updated; full suite green |
| C3 | 3 | H1 duplicate removed from issue.md.jinja2; validate_template passes |

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-06 | Agent | Initial draft |