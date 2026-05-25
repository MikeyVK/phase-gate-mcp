<!-- docs\development\issue353\planning.md -->
<!-- template=planning version=130ac5ea created=2026-05-25T19:29Z updated= -->
# create_branch: remove implicit auto-checkout (#353)

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-05-25

---

## Scope

**In Scope:**
mcp_server/adapters/git_adapter.py, mcp_server/tools/git_tools.py, 4 test files

**Out of Scope:**
.github/prompts/start-issue.prompt.md (no content change needed), IGitAdapter protocol (does not exist)

---

## Summary

Remove the implicit auto-checkout from GitAdapter.create_branch() (single line), correct the tool return text and adapter log, and update 4 tests that assert the defect behavior. One TDD cycle. Clean break, no migration shim.

---

## TDD Cycles


### Cycle 1: C1 — Remove auto-checkout

**Goal:** Remove new_branch.checkout() from GitAdapter.create_branch(), correct tool return text and adapter log message, update 4 tests to assert checkout is NOT called.

**Tests:**
- tests/mcp_server/unit/adapters/test_git_adapter.py::test_create_branch_with_head — checkout.assert_called_once() → checkout.assert_not_called()
- tests/mcp_server/unit/adapters/test_git_adapter.py::test_create_branch_with_branch_name — checkout.assert_called_once() → checkout.assert_not_called()
- tests/mcp_server/unit/adapters/test_git_adapter.py::test_create_branch_with_commit_hash — checkout.assert_called_once() → checkout.assert_not_called()
- tests/mcp_server/unit/tools/test_git_tools.py::test_create_branch_tool_calls_manager_with_explicit_base — 'Created and switched to branch' → 'Created branch'

**Success Criteria:**
- new_branch.checkout() does not appear in GitAdapter.create_branch()
- Tool return text contains 'Created branch' and not 'switched'
- Adapter log message is 'Created branch' not 'Created and checked out branch'
- All 4 updated tests pass
- Full test suite passes with zero regressions
- Quality gates PASS (ruff, pylint, mypy) on changed files


## Related Documentation
- **[docs/development/issue353/research.md][related-1]**
- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md][related-2]**

<!-- Link definitions -->

[related-1]: docs/development/issue353/research.md
[related-2]: docs/coding_standards/ARCHITECTURE_PRINCIPLES.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 |  | Agent | Initial draft |