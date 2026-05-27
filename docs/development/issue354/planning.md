<!-- docs\development\issue354\planning.md -->
<!-- template=planning version=130ac5ea created=2026-05-27T09:30Z updated= -->
# Issue #354 — Shared GitHub Read-Contract Refactor: Planning

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-05-27

---

## Purpose

Define the implementation cycle structure for issue #354: introduce PRReadModel + GetPRTool (additive), refactor GetIssueTool to IssueReadModel (clean break), and update all consuming documentation and prompts.

## Scope

**In Scope:**
mcp_server/state/github_read_models.py; mcp_server/adapters/github_adapter.py; mcp_server/managers/github_manager.py; mcp_server/tools/pr_tools.py; mcp_server/tools/issue_tools.py; mcp_server/server.py; tests/mcp_server/unit/adapters/test_github_adapter.py; tests/mcp_server/unit/managers/test_github_manager.py; tests/mcp_server/unit/tools/test_pr_tools.py; tests/mcp_server/unit/tools/test_issue_tools.py; docs/reference/mcp/tools/github.md; .github/prompts/end-issue.prompt.md; .github/prompts/start-issue.prompt.md

**Out of Scope:**
All other existing MCP tools and DTOs; platform/worker/config code; integration tests (only unit tests in scope); WorkflowStatusDTO or other state models not named in design

## Prerequisites

Read these first:
1. Research artifact: docs/development/issue354/research.md (v1.2, Approved Strategy recorded)
2. Design artifact: docs/development/issue354/design.md (v2.0, QA PASS, committed c7e8191a)
---

## Summary

Three TDD cycles implementing the approved three-change design: (C1) get_pr full stack + MergePRTool Demeter fix (additive), (C2) get_issue clean break to IssueReadModel, (C3) docs and prompt updates.

---

## TDD Cycles


### Cycle 1: C1: get_pr stack + MergePRTool Demeter fix

**Goal:** Add PRReadModel frozen DTO, GitHubAdapter.get_pr(), GitHubManager.get_pr() -> PRReadModel, GetPRTool, server registration, and fix MergePRTool.execute() to call manager.get_pr() instead of manager.adapter.repo.get_pull(). Zero breaking changes to existing tool contracts.

**Tests:**
- tests/mcp_server/unit/adapters/test_github_adapter.py — add test_get_pr_success, test_get_pr_not_found, test_get_pr_api_error
- tests/mcp_server/unit/managers/test_github_manager.py — add test_get_pr (normalization: PRReadModel fields all mapped)
- tests/mcp_server/unit/tools/test_pr_tools.py — add test_get_pr_tool; REPLACE test_merge_pr_tool (remove adapter.repo.get_pull mock, use manager.get_pr.return_value = PRReadModel(...))
- tests/mcp_server/unit/test_server.py — assert GetPRTool is registered when github_token is set; assert GetPRTool is NOT registered when github_token is absent

**Success Criteria:**
- GetPRTool registered and returns ToolResult.text(json.dumps(model.model_dump(), indent=2))
- MergePRTool.execute() has zero references to self.manager.adapter
- test_merge_pr_tool uses PRReadModel fixture — no legacy adapter.repo.get_pull mock remains
- PRReadModel is frozen (ConfigDict frozen=True, extra='forbid'))
- Quality gates pass (pylint 10.00/10 + Pyright strict) on all C1 changed files



### Cycle 2: C2: get_issue clean break to IssueReadModel

**Goal:** Extend github_read_models.py with IssueReadModel (12 fields) + MilestoneReadModel. Refactor GitHubManager.get_issue() to normalize Issue -> IssueReadModel. Refactor GetIssueTool.execute() to return flat JSON text. Replace all tests that mock raw Issue host objects.

**Tests:**
- tests/mcp_server/unit/managers/test_github_manager.py — REPLACE test_get_issue (delegation test -> normalization test: mock adapter returns MagicMock Issue with all 12 field values; assert returned IssueReadModel has correct field values)
- tests/mcp_server/unit/tools/test_issue_tools.py — REPLACE entire TestGetIssueTool class (remove bare Issue mock; manager.get_issue.return_value = IssueReadModel(...); assert json.loads(result.content[0].text) matches expected dict)

**Success Criteria:**
- GetIssueTool.execute() has zero access to PyGithub host-object fields
- GitHubManager.get_issue() return type is IssueReadModel (not Issue)
- JSON output for get_issue matches IssueReadModel.model_dump() exactly (all 12 fields, flat, no 'success' wrapper)
- IssueReadModel and MilestoneReadModel are frozen (ConfigDict frozen=True, extra='forbid')
- test_get_issue_tool asserts text content is valid JSON with correct field values
- Quality gates pass (pylint 10.00/10 + Pyright strict) on all C2 changed files

**Dependencies:** C1 (github_read_models.py already exists with PRReadModel)


### Cycle 3: C3: Docs and prompt updates

**Goal:** Rewrite docs/reference/mcp/tools/github.md (get_issue section to flat IssueReadModel JSON; add get_pr section with PRReadModel fields). Update end-issue.prompt.md: call get_pr() AFTER merge_pr and BEFORE git_checkout; compare head_branch from get_pr with active branch from get_work_context and stop on mismatch; use base_branch from get_pr for git_checkout (design §3.8). Update start-issue.prompt.md step 1 to reference JSON field names.

_Note: start-issue.prompt.md is included because it is a semantic consumer of get_issue (B1 clean break). After C2 the output changes from prose to JSON; step 1 must reference JSON field names to remain correct._

**Tests:**
- Manual review: github.md get_issue example JSON matches IssueReadModel.model_dump() field names and types
- Manual review: github.md get_pr section present with PRReadModel fields
- Manual review: end-issue prompt calls get_pr() after merge_pr and before git_checkout; compares head_branch with active branch from get_work_context; stops on mismatch; uses base_branch for git_checkout
- Manual review: start-issue prompt step 1 reads title from JSON field, labels from JSON array

**Success Criteria:**
- docs/reference/mcp/tools/github.md get_issue example has no 'success' key and no nested 'issue' wrapper
- docs/reference/mcp/tools/github.md has get_pr entry with all 8 PRReadModel fields documented
- end-issue.prompt.md calls get_pr(PR_NUMBER) after merge_pr and before git_checkout (design §3.8)
- end-issue.prompt.md compares head_branch from get_pr with active branch from get_work_context; stops on mismatch
- end-issue.prompt.md uses base_branch from get_pr for git_checkout
- start-issue.prompt.md step 1 mentions 'title' and 'labels' as JSON fields to read from get_issue response
- No regressions in end-issue or start-issue prompt logic

**Dependencies:** C2 (IssueReadModel and PRReadModel must exist before docs are written)

---

## Risks & Mitigation

- **Risk:** C2 breaks the get_issue output format — any prompt reading prose must be updated
  - **Mitigation:** Validate start-issue.prompt.md and end-issue.prompt.md against flat JSON field names before C3 commit; confirm all 12 IssueReadModel fields are accessible from prompts
- **Risk:** PyRight strict mode may flag manager return types
  - **Mitigation:** Add real runtime imports for IssueReadModel and PRReadModel in github_manager.py; do NOT add `from __future__ import annotations` to github_read_models.py, github_manager.py, or pr_tools.py — runtime instantiation of Pydantic models requires real non-deferred annotations (per TYPE_CHECKING_PLAYBOOK)
- **Risk:** test_merge_pr_tool uses deep adapter.repo.get_pull() mock chain — must be fully replaced, no partial residue
  - **Mitigation:** In C1 RED: delete the old mock setup entirely before writing the new one; assert no adapter attribute access in MergePRTool.execute()

## Related Documentation
- **[docs/development/issue354/research.md][related-1]**
- **[docs/development/issue354/design.md][related-2]**

<!-- Link definitions -->

[related-1]: docs/development/issue354/research.md
[related-2]: docs/development/issue354/design.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-27 | Agent | Initial draft |
| 1.1 | 2026-05-27 | Agent | Fix F1 (get_pr post-merge per design §3.8); fix F2 (add no-token server test); fix F3 (name test_server.py); fix F4 (start-issue note); fix F5 (Pyright annotation risk); fix F6 (REPLACE TestGetIssueTool class) |