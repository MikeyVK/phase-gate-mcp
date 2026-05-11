<!-- c:\temp\st3\.st3\temp\issue253-pr-body.md -->
<!-- template=pr version=93bb9b4e created=2026-04-26T07:46Z updated= -->
# fix: stabilize run_tests reliability and retire stale projects.json docs

Completes issue #253 by closing the remaining RunTestsTool correctness gaps, capturing QA-approved validation evidence, and aligning active workflow documentation with the live state contract (`state.json` + `deliverables.json`).
## Changes
- Repair `summary_line` sync so JSON and text summaries stay aligned.
- Surface pytest invocation and usage failures as explicit tool errors / recovery paths instead of misleading empty-run summaries.
- Add opt-in coverage support for `scope="full"` runs and parse coverage results in the pytest runner.
- Remove remaining legacy `_run_pytest_sync` seams and migrate active call sites to injected runners.
- Add the QA-approved validation report for issue #253.
- Retire the obsolete `.st3/projects.json` file and update active MCP reference / agent docs to point at `.st3/state.json` and `.st3/deliverables.json`.

## Testing
- `run_tests(path="tests/mcp_server/unit/tools/test_test_tools.py")` → 18 passed.
- `run_tests(path="tests/mcp_server/unit/managers/test_pytest_runner.py")` → 8 passed.
- `run_tests(path="tests/mcp_server/unit/tools/test_project_tools.py")` → 28 passed.
- `run_tests(path="tests/mcp_server/unit/tools/test_dev_tools.py tests/mcp_server/unit/integration/test_all_tools.py")` → 29 passed, 3 warnings.
- `run_tests(path="tests/")` → 2876 passed, 11 skipped, 6 xfailed, 21 warnings.
- `run_quality_gates(scope="branch")` → overall pass.
- Live MCP validation covered the no-tests-collected path (`SuggestionNote`), invalid marker path (`RecoveryNote`), and coverage-enabled full run (`coverage_pct=77.0`, threshold failure surfaced correctly).
## Checklist

- [x] Targeted regression tests passing
- [x] Full suite passing on MCP tool path
- [x] Branch quality gates passing
- [x] Validation report approved by QA
- [x] Active workflow docs aligned with state.json + deliverables.json

## Related Documentation
- **[docs/development/issue253/research.md][related-1]**
- **[docs/development/issue253/planning.md][related-2]**
- **[docs/development/issue253/design.md][related-3]**
- **[docs/development/issue253/validation-report.md][related-4]**
- **[docs/reference/mcp/tools/project.md][related-5]**
- **[imp_agent.md][related-6]**
- **[qa_agent.md][related-7]**

---

Closes: #253