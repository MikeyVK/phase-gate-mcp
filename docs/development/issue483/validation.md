<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=CT9NV5LmQjKHFGqX sf=5--KpGf2wHUv2qAj -->

# Issue 483 — Native Markdown validation

**Status:** Validation — independent review requested  
**Version:** 0.1  
**Last Updated:** 2026-10-08

## Purpose

Provide durable evidence for C483.1 and V483.1 on implementation commit d6f64173ba944449be4c5854185cfb3c503004cf; run IDs below are supplemental.

## Scope Out

Compatibility, legacy/fallback handling, runtime H1 or template-structure checking, authored-content snapshots, generic runtime/Lychee adapter/DTO/API changes and unrelated baseline repairs.

## Issue Number

#483

## Cycle

C483.1

## Validation Status

PASS

## Scope

Complete owned-checker removal, nine Markdown policy migrations, .md routing and affected test cleanup. Independent Implementation QA gave GO on d6f64173. Validation changed only this report and workflow state.

## Evidence

### Corrected mutation behavior

Six real native cases exercise scaffold/edit with valid-enforce, invalid-enforce and invalid-report. Enforce leaves a missing target absent or original bytes intact on native failure; report writes the exact proposed bytes while preserving failure facts. Native JSON identifies missing.md and #absent. Metadata/extension and document/body routes are covered. Self/TOC links use proposed content; neighbor bytes remain unchanged and both scratch directories are empty. Lychee adapter 2.0.0/native 0.24.2 use --offline, --cache=false, --include-fragments; binding timeout remains 60.

**Sources:**

- [Central mutation tests](<../../../tests/mcp_server/integration/test_markdown_mutations.py>)

**Invocation:** run_tests(scope="targets", targets=["tests/mcp_server/integration/test_markdown_mutations.py"], tests=["python_tests"], timeout_seconds=180)

**Observed Result:** Validation rerun: 6 passed, 21 warnings, 6.65s, exit 0; configured arguments. Receipt c66ea5950b5e4ba092e1403d766f28e0. Repeated because the large full-run read omitted individual case lines.

### Native snapshot and affected consumers

The two existing snapshot cases now include angle/reference destinations and a space/parenthesis neighbor name; adapter evidence matches independently invoked native evidence. The existing dependency/wire case also passes. The earlier focused selection of ten changed template test files plus profile composition and central mutation tests passed: 49 tests, 21 warnings, 9.14s, exit 0 (e6a2379cd9bf437986d60cbb73b0e8f7). Existing renderer coverage was retained; checker-only imports/invocations and fixed binding/count assertions were removed.

**Sources:**

- [Native witness](<../../../tests/mcp_server/integration/adapters/test_lychee.py>)
- [Profile composition](<../../../tests/mcp_server/integration/execution/test_check_profiles.py>)

**Invocation:** run_tests(scope="targets", targets=["tests/mcp_server/integration/adapters/test_lychee.py"], tests=["python_tests"], args={"python_tests":["-k","test_native_self_toc_and_neighbor_snapshot or test_missing_native_and_malformed_wire"]}, timeout_seconds=180)

**Observed Result:** 3 passed, 9 warnings, 5.88s, exit 0; receipt 19c677cf273a4239bd9334abe9c514fb. Independent Implementation QA separately reproduced ten relevant native cases and all three Python checks on the 13 changed Python files.

### Required branch and additional workspace gates

Branch filtering selected the 13 changed existing Python files for Ruff; production-scoped Mypy and Pyright were not applicable because production Python changes are deletions. Implementation target checks additionally ran Pyright on all 13 changed Python test files and passed. The configured run verified formatting for 467 files and checked 188 production source files with Mypy and Pyright. Native versions: Ruff 0.15.6, Mypy 1.19.1, Pyright 1.1.408.

**Sources:**

- [Check configuration](<../../../.pgmcp/config/checks.yaml>)
- [Mandatory plan](<planning.md>)

**Invocation:** run_checks(scope="branch", profile="python_review", timeout_seconds=600); run_checks(scope="configured", timeout_seconds=600)

**Observed Result:** Branch: passed; format/lint passed, types/pyright not_executed(reason=not_applicable), f69e1e4a6caa4f92945f49e9f749af50. Configured: all four passed, zero Pyright errors/warnings and no Mypy issues, 493d7701ff5d4bc6847b93318f13a2c3. No native args or configuration relaxed.

### Required complete configured test suite

One unchanged native-configured run used pyproject.toml, testpaths tests/mcp_server, Python 3.13.7, pytest 9.0.2 and eight workers. The client setting is tool_timeout_sec=1800. Native capture reports exit 0, 806088 stdout bytes and no capture truncation; the normal cached read omitted middle text, so bounded header/tail evidence and the explicit six-case rerun supply readable results.

**Sources:**

- [Native pytest configuration](<../../../pyproject.toml>)
- [Test binding](<../../../.pgmcp/config/tests.yaml>)
- [Execution budget](<../../setup/README.md#option-c-codex-setup>)

**Invocation:** run_tests(scope="configured", tests=["python_tests"], timeout_seconds=1200)

**Observed Result:** 2813 items: 2811 passed, 1 skipped, 1 xpassed, 241 warnings in 408.49s (0:06:48); exit 0. args_source=configured, effective_args=[]. Receipt 71cf2a336e68485fb75f69fae52f08d6. No split, shortened scope or caller argument override.

## Demonstration

Reproduce the six central cases using the first invocation above with the pinned native prerequisite available. All writes are confined to isolated temporary workspaces. These cases demonstrate native diagnostics and enforce/report persistence through actual public ScaffoldOperation/EditOperation APIs.

## Preservation

D483.1.1 is proven by central native behavior and the snapshot witness; D483.1.2 by the complete config/policy/package diff; D483.1.3 by cleanup, retained renderer/profile tests and passing focused/full evidence. Existing Lychee adapter, generic execution/mutation code and DTO/API contracts are unchanged. H1 remains the template package responsibility.

## Failures

## Caveats

- Intermediate test-only diagnostic refinement failed four cases because evidence.data is immutable FrozenJson rather than dict; 77 other lifecycle/policy cases passed. The new tests were corrected with public thaw_json, then all six cases and targeted format/lint/Pyright passed. No production correction followed.
- Full-suite warnings include existing SchemaAttachment field shadowing, collection names, pathlib/AnyIO/PyGithub/MCP deprecations and sync tests carrying asyncio marks. Restart tests also emitted an unawaited delayed_exit RuntimeWarning and a Task exception/SystemExit(42) traceback from their mock_exit; native pytest still returned exit 0 with no failed cases. These facts are retained, not silently repaired or suppressed.
- The skip is TestProxyIntegration.test_end_to_end_restart_flow, an existing manual integration placeholder. The only existing non-strict xfail is test_server_renders_exclusion_note_in_response; XPASS does not fail this configured native run.
- Markdown links for Research/Design/Planning passed with configured arguments (3c806b1e535849d7b872ce8386bc8080). Research references to retired sources are commit-pinned historical URLs. run_checks(scope="targets", targets=["docs/development/issue483/validation.md"], checks=["markdown_links"], timeout_seconds=120) passed with configured arguments (9558d3fccf6e459c80ad798863d7dbeb).
- No blanket gate exception is requested or inherited from #481. Current required native results pass. Independent Validation QA remains requested; authored PASS describes execution evidence only.

## Deferred Work

### Generated template structure after later free-text rewrites

Separate structural-conformance concern; the existing package maintenance procedure owns generated H1. Research indexes #121 as a candidate and excludes runtime structure enforcement from #483.

**References:**

- [Research deferred finding](<research.md>)

### Active scaffold/edit tool references

DOC483.1 belongs to the subsequent Documentation phase; this request finishes through Validation.

**References:**

- [Documentation deliverable](<planning.md#doc4831>)

## Related Documents

- [Research and Approved Strategy](<research.md>)
- [Design v0.3](<design.md>)
- [Planning v0.3](<planning.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-08 | @imp validator | Record corrected native behavior, mandatory full-suite and gate outcomes, and explicit limitations. |
