<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=CT9NV5LmQjKHFGqX sf=zJbLuUrs_I33kpX4 -->

# Issue 470 — LF safe-edit validation

**Status:** Validation evidence complete; independent review requested  
**Version:** 1.0  
**Last Updated:** 2026-10-11

## Purpose

Prove the bounded LF cutover against the approved strategy and one-cycle plan.

## Scope In

Seven production sources, three existing test sources, required Validation runs and retained edit safety.

## Scope Out

No editor/Git configuration, bulk file normalization, new adapter/writer architecture or old-policy regression tests.

## Prerequisites

- Research v1.0, Design v1.0, Planning v1.0 and independent Implementation→Validation GO on 53cad26773e6e6e7288b2f0046ee04f0c5585dd2.

## Issue Number

#470

## Scope

Validated production/test snapshot: 53cad26773e6e6e7288b2f0046ee04f0c5585dd2. Only phase audit state changed before the runs. Test/check args omitted unless explicitly recorded below.

## Obligations

### C\_1 / D\_1.1: one pure LF construction value, no source-terminator preservation.

**Evidence:**

- [Construction](<../../../../mcp_server/services/edit_construction.py>)
- [Reader snapshot](<../../../../mcp_server/core/interfaces/file_writer.py>)

**Outcome:** construct_edit returns str; original_source_text, EditProposal, wrapper and terminator mapping/reconstruction are deleted. Read-only rg over mcp_server and tests found no old symbols or aliases.

### C\_1 / D\_1.2: consumer cutover and factual byte change.

**Evidence:**

- [Operation](<../../../../mcp_server/services/edit_operation.py>)
- [Reader/writer](<../../../../mcp_server/utils/atomic_file_writer.py>)
- [Composition](<../../../../mcp_server/bootstrap.py>)

**Outcome:** One snapshot read; original bytes retained for the unchanged writer guard. Same final LF string checked and written. Completed write compares UTF-8 bytes; no write returns null. Production and integration compositions use construct_edit directly.

### C\_1 / D\_1.3: bounded behavior coverage and cleanup.

**Evidence:**

- [Construction cases](<../../../../tests/mcp_server/unit/services/test_edit_construction.py>)
- [Operation integration](<../../../../tests/mcp_server/integration/test_edit_operation_v3.py>)
- [Public transport](<../../../../tests/mcp_server/integration/test_edit_public_v3.py>)
- [Markdown composition](<../../../../tests/mcp_server/integration/test_markdown_mutations.py>)

**Outcome:** Existing cases adapted; preservation matrix reduced from 16 to eight behavior cases. Focused selection decreased 67→59 items; no new test files. Safety/public behavior coverage reused rather than duplicated.

### Validation / D\_1: full native suite and appropriate branch/configured gates.

**Evidence:**

- [Planned invocations](<planning.md#milestones>)

**Outcome:** All requested native runs completed, exit 0. Exact invocations and observed outcomes below. Post-suite get_project_plan(470) confirmed C_1, D_1.1–D_1.3 and both phase deliverables intact.

## Evidence

### Configured full suite completed once.

Configured full suite completed once.

**Sources:**

- [Native configuration](<../../../../pyproject.toml>)

**Invocation:** run_tests(scope='configured', tests=['python_tests'], timeout_seconds=1800); args omitted.

**Observed Result:** Python 3.13.7, pytest 9.0.2, eight workers, testpaths tests/mcp_server, 2,853 items. 2,851 passed, 1 skipped, 1 xpassed, 253 warnings in 454.50 s; exit 0; capture not truncated. Receipt 74c69e3c6e494dd1bd414a758e6cfda7. Read bounded header/tail windows (821,414-character DTO), not a full transient-cache download.

### Branch gates respect per-binding target selection.

Branch gates respect per-binding target selection.

**Sources:**

- [Check bindings](<../../../../.pgmcp/config/checks.yaml>)

**Invocation:** run_checks(scope='branch', checks=['python_format','python_lint','python_types','python_pyright','markdown_links'], timeout_seconds=600); args omitted.

**Observed Result:** Five passed, all native exit 0. Ruff format: 10 files already formatted; lint all checks passed. Mypy: seven source files. Pyright: seven files, zero errors/warnings/information. Lychee: 14 successful link occurrences, zero errors/excludes. Receipt d349b575ef24491bb665b38be0f2ed03.

### Configured Python gates completed.

Configured Python gates completed.

**Sources:**

- [Check bindings](<../../../../.pgmcp/config/checks.yaml>)

**Invocation:** run_checks(scope='configured', checks=['python_format','python_lint','python_types','python_pyright'], timeout_seconds=600); args omitted.

**Observed Result:** Four passed, all native exit 0. Ruff format: 469 files already formatted; lint all checks passed. Mypy: 189 source files. Pyright: 189 files, zero errors/warnings/information. Receipt 211a7795e12941e59e45db43fea85534. Native versions across gates: Ruff 0.15.6, Mypy 1.19.1, Pyright 1.1.408, Lychee 0.24.2.

### Focused behavior changed as designed without suite growth.

Focused behavior changed as designed without suite growth.

**Sources:**

- [Focused targets and production gates](<planning.md#verification>)

**Invocation:** Baseline/final: run_tests(scope='targets', targets=[construction unit, operation integration, public integration, Markdown integration paths listed in Planning], tests=['python_tests'], timeout_seconds=600), args omitted. RED: first two paths with args={'python_tests':['-k','use_lf_text or policy_retains_actual_text_bytes']}.

**Observed Result:** Baseline 67 passed (d6d30ffef7134300b9d55c3195fbe802). Adapted current-policy RED: 14 failed, 3 passed (fa20f38d44204b97849ce96f9d9f40e7); committed bdb272d9 before production cutover. Final 59 passed, 65 warnings, 7.94 s, exit 0 (e6f5098ba57c4aeea48c7547f68db37c). No retained test rejects the superseded preservation policy.

### Targeted gates closed during Implementation.

Targeted gates closed during Implementation.

**Sources:**

- [Production/test scope](<planning.md#scope-in-1>)

**Invocation:** Production seven paths: format/lint/Mypy/Pyright; changed three test paths: format/lint, scope='targets', timeout_seconds=600. Recheck format/lint only two description paths after shortening.

**Observed Result:** Initial production format/types/Pyright passed; lint found only two E501 description lines (58f4dfcfddf24e24b16ed6fc1c4b8152). Two strings shortened, affected format/lint passed (eb9a400afac14561970deaab30c367c3); no behavior/type change. Changed tests format/lint passed (a6ce29e013c245ccbe1aebc522d4fd7e). Broad Validation runs independently cover the final committed versions.

## Demonstration

The eight retained integration cases use the real reader/writer and assert the persisted bytes, check-input bytes and content_changed: replace/window/literal CRLF input; mixed-source append; CR rewrite; literal newline pattern; regex expansion emitting CRLF; no-match normalization; LF byte identity; anchored append. The existing policy matrix confirms CRLF→LF rewrite reports true only after write.

## Preservation

Existing coverage retains cardinality, regex errors/backreferences/zero-width matching, validation policy, original-profile selection, exact-original-byte race protection, single read, lock/write/cleanup failures and public DTO transport. The writer/check/adapters remain unchanged. One pure helper normalizes CRLF/CR; no IO or workflow knowledge enters construction.

## Containment

All internal consumers cut over together. No compatibility alias, legacy route, new mode/flag, test file or broad suppression was added. OriginalFileSnapshot remains frozen. No Unicode/BOM/whitespace/final-newline policy was introduced. Historical #460 documents were inspected and left unchanged.

## Failures

None.

## Caveats

- Full suite success is native exit 0, not a claim of warning-free or every item executed: one skip, one XPASS and 253 warnings remain. Native output includes existing admin restart-test delayed-exit/SystemExit(42) task diagnostics and deprecation warnings. These are outside changed sources; their age/causality was not established by this issue and they were not suppressed or repaired.
- A successful edit or no-match can normalize the entire source to LF and report changed=true. A byte-identical proposal still runs checks and performs the completed-write path; no optimization was added.
- The report stores invocations and observations durably; receipt IDs supplement them and are not durable evidence by themselves.

## Risks

### First successful edit can produce a whole-file line-ending diff.

Document explicit whole-file LF policy in the active editing reference.

**Consequence:** Accepted policy consequence; no bulk migration.

## Deferred Work

None.

## Related Documents

- [Research](<research.md>)
- [Design](<design.md>)
- [Planning](<planning.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-11 | @imp validator | Record one full suite, scoped gates, LF behavior and clean-break cleanup. |
