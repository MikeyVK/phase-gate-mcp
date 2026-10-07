<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=CT9NV5LmQjKHFGqX sf=5--KpGf2wHUv2qAj -->

# Issue \#482 Validation

**Status:** BLOCKED — incomplete package migration  
**Version:** 0.1  
**Last Updated:** 2026-10-07

## Purpose

Demonstrate completed branch filtering, truthful no-applicable outcomes and preservation of ordinary native execution.

## Scope Out

No native configuration parser, force-exclude, compatibility route, test-impact selection, new test modules or expanded old-behavior regression coverage.

## Issue Number

#482

## Cycle

C482.1

## Validation Status

FAIL

## Scope

Implementation d09f4edbb33221b9580f978a0c9fd241d05a9205; one clean-break cycle and the authorized #481 baseline import repair.

## Obligations

### D482.1.1: immutable declarations, startup reference admission and tool-neutral injected matching.

**Evidence:**

- [Policy model](<../../../mcp_server/config/schemas/checks_config.py>)
- [Admission](<../../../mcp_server/config/validator.py>)
- [Matcher](<../../../mcp_server/execution/configured_targets.py>)
- [Composition](<../../../mcp_server/bootstrap.py>)

**Outcome:** Observed focused admission/mixed-selection evidence and healthy cutover; final verification recorded below.

### D482.1.2: per-check branch subsets, explicit descendants and truthful public no-applicable results.

**Evidence:**

- [Selection](<../../../mcp_server/execution/check_selection.py>)
- [Execution](<../../../mcp_server/execution/check_service.py>)
- [Public contract](<../../../mcp_server/schemas/execution_outputs.py>)
- [Public behavior](<../../../tests/mcp_server/integration/test_checks_public_v3.py>)

**Outcome:** Five public outcome scenarios cover empty, positive, negative, native refusal and stopped execution; ordinary requests remain unchanged.

### D482.1.3: complete caller migration, removed covering/legacy carrier and bounded behavioral coverage.

**Evidence:**

- [Planning inventory and budget](<planning.md>)
- [Admission behavior](<../../../tests/mcp_server/unit/config/test_checks_config.py>)
- [Selection behavior](<../../../tests/mcp_server/unit/execution/test_check_selection.py>)

**Outcome:** Three new functions, nine scenarios, zero new modules. Exact carrier/caller search inspected; no alias or covering helper remains.

### Authorized import repair: restore ConfigLoader-first import without changing type identity.

**Evidence:**

- [Direct schema import](<../../../mcp_server/core/tool_execution.py>)
- [Type identity owner](<../../../mcp_server/schemas/template_identity.py>)

**Outcome:** TemplateId now imports its owning schema directly; two existing focused baseline cases pass. No new repair tests.

## Evidence

### Single full native-configured suite on implementation d09f4edb.

2818 collected: 2816 passed, 1 skipped, 1 xpassed, 229 warnings in 331.24 seconds; exit 0. Native defaults retained, eight workers, effective_args=[]. Full cached DTO assembled with contiguous pages and verified SHA-256 9fe3eea6050102433647bf9c024a37852a4b91e18e2ac74fde4cd4beb2ed2b15.

**Sources:**

**Invocation:** run_tests(scope="configured", tests=["python_tests"], timeout_seconds=1200)

**Observed Result:** passed; receipt aeb13588601642ec9b4aa3e3f8469357

### Per-check branch gates on implementation d09f4edb.

All five checks passed, native exit 0 each. Ruff: 24 Python files; Mypy/Pyright: 11 production sources. Lychee: 50 occurrences, 33 successful, 17 native offline exclusions, zero errors. Mypy identity still 1.0.0/pIuqT753FXPApELy; this does not satisfy the authored migration requirement.

**Sources:**

**Invocation:** run_checks(scope="branch", checks=["python_format","python_lint","python_types","python_pyright","markdown_links"], timeout_seconds=600)

**Observed Result:** passed; receipt 674b0dc1d7ca4a81a39173a632b813d2

### Final configured workspace Python gates on implementation d09f4edb.

Four checks passed, native exit 0 each. Ruff format: 468 files; strict Mypy: 189 sources; Pyright: 189 sources, zero errors/warnings. Native configuration remains authoritative.

**Sources:**

**Invocation:** run_checks(scope="configured", profile="python_review", timeout_seconds=600)

**Observed Result:** passed; receipt c14fa86af80f4d0c8e6be1963597a496

### Focused implementation and independent QA evidence.

Producer: 15 passed, 9 warnings, exit 0, 6.76 seconds (307bc0f045dd41f8bb4d2c10fb86e598); production gates 23cbf8ee43954f13b64e623bbe48a0f4 and test gates faa2def15ea64aafb2ba8492fa79c1cf passed. Independent QA repeated 15 cases (83dddebe32ce48d8b12c4c77fdad76b8), production gates (250825aac6784a1fa7c93a7d334cd2f1), test gates (3996e4a9597a46a3a909fb64acc8dadc) and healthy admission (4e31b6a97c41470b948b165ac1e62b77).

**Sources:**

### Package migration completeness requires direct inspection.

Ruff, Pyright and Lychee are 2.0.0; Mypy remains 1.0.0 at manifest line 2. Producer inspection found the omission; independent QA confirmed a P2 blocker in turn 01a114db-03ac-7400-832f-81aa1e4494e6. Earlier Implementation GO did not prove this authored requirement.

**Sources:**

- [Four-package requirement](<design.md>)
- [Mypy declaration](<../../../mcp_server/bundled_adapters/mypy/manifest.yaml>)

**Observed Result:** blocked

## Preservation

Native protocol version 1, tool pins, native commands/guards and configured/workspace/content/test/fix meanings are retained. Branch matching consumes authored generic policies; no native config inspection or tool IDs enter the generic matcher.

## Containment

One complete cutover admitted on the controlled restart. Runtime doubles and filesystem test effects remain isolated. No changes to historical issue artifacts.

## Failures

- Open P2: Mypy package version must be 2.0.0 under the approved design. Passing tests and native gates do not satisfy this missing authored migration. Return to Implementation; do not patch in Validation.

## Caveats

- The existing native suite skipped TestProxyIntegration.test_end_to_end_restart_flow and XPASSed TestGitCommitToolC3.test_server_renders_exclusion_note_in_response. Their native markers were retained; no caller skip/filter or reduction was introduced.
- 229 native warnings include Pydantic field shadowing/collection warnings, pathlib reserved-path deprecation, deprecated MCP resource returns and existing synchronous tests carrying asyncio markers. Restart-tool tests also emit caught SystemExit task diagnostics. Native exit is 0; these facts are retained for independent QA, not suppressed.
- Cache receipts are transient and connection-local. Exact observed outcomes are recorded here; the controlled reload required for repair will invalidate the producer cache. Full suite DTO is retained by the producer.

## Deferred Work

## Related Documents

- [Approved Research 0.15](<research.md>)
- [Approved Design 0.3](<design.md>)
- [Planning 0.1 and exact verification route](<planning.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-07 | @imp validator | Record full configured verification and bounded clean-break evidence. |
