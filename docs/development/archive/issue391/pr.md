<!-- docs\development\issue391\pr.md -->
<!-- template=pr version=93bb9b4e created=2026-06-10T18:07Z updated= -->
# refactor(mcp-server): Cleanup legacy naming, docs, tests, and archive files

This PR performs a comprehensive refactoring and cleanup of the standalone phase-gate-mcp codebase. It removes deprecated design documents under docs/archive/, replaces all legacy references (ST3, SimpleTraderV3, st3:// URIs) in active documentation and the test suite, completely rewrites ARCHITECTURE.md, updates total tool counts to 50 (15 Git tools), and cleans up 10 obsolete/skipped/xfailed tests. All 2870+ tests pass and branch quality gates are completely green.
## Changes
- Deleted deprecated documents in docs/archive/
- Cleaned up st3 and simpletrader names in active docs, including pyproject.toml, README.md, and docs/reference/mcp/tools/git.md
- Completely rewrote docs/mcp_server/ARCHITECTURE.md and corrected tool counts to 50 tools (15 Git operations)
- Renamed 82 occurrences of legacy naming (variables and fixtures) in the test suite
- Renamed test_cycle_tools_legacy.py to test_cycle_tools_business_logic.py
- Deleted 10 obsolete tests (6 skipped from test_qa_manager.py, 3 xfail from test_model1_branch_tip_neutralization.py, 1 xfail from test_server.py)
- Formatted and resolved all line length warnings in modified test files

## Testing
Ran full local test suite via run_tests(scope='full') with 2876 passed, 5 skipped, 2 xfailed, 1 xpassed. Ran quality gates on the branch via run_quality_gates(scope='branch') with 5/5 gates passing cleanly.
## Checklist

- [ ] All tests green
- [ ] Branch quality gates passing (ruff, pyright)
- [ ] Active docs free of legacy terms
- [ ] Obsolete tests removed
- [ ] Architecture document rewritten
- [ ] Tool counts updated in docs

## Deferred Work

- Archiving of historical issue artifacts under docs/development/ and removing them from the main branch before the production release.
## Related Documentation
- **[docs/development/issue391/validation.md][related-1]**
- **[docs/mcp_server/ARCHITECTURE.md][related-2]**

---

Closes: #391