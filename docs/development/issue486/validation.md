<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=CT9NV5LmQjKHFGqX sf=5--KpGf2wHUv2qAj -->

# ASCII Python identifier contract — Validation (#486)

**Status:** VALIDATION COMPLETE — independent review requested  
**Version:** 1.0  
**Last Updated:** 2026-10-05

## Purpose

Validate the implemented #486 contract against the approved Research strategy, Design and Planning. This producer report records facts; independent QA owns GO/NOGO.

## Scope In

Two suite schema sources, three changed Python tests, all eight Python/pytest family consumers, complete configured native suite and branch Markdown links.

## Scope Out

Runtime/resolver/renderer/cache/presentation changes, compatibility bridges, TypeScript policy and release assembly.

## Prerequisites

- Independent Research, Design and Planning GO; approved ASCII-only structured identifier clean break.
- Implementation f73d53913370cfcdd5b6fa55d70831e407ef5b73, with cycle cleanup included.
- Independent Implementation GO from Beoordeel designplan on f73d5391; nine-file QA rerun 81 passed, 9 warnings in 13.62s and all three changed-test gates passed.

## Issue Number

#486

## Cycle

C_ASCII / 1

## Obligations

### D\_ASCII\_SHARED — compact shared lexical admission with dotted/relative imports, decorators/factories and exact reserved-name guards.

**Evidence:**

- [Shared Python schema](<../../../.pgmcp/template_suite/shared/definitions/python.schema.json>)
- [Public-boundary regression tests](<../../../tests/mcp_server/integration/templates/test_shared_python.py>)

**Outcome:** Implemented at existing schema owner; validated through public loader/schema and native family tests.

### D\_CLASS\_DUNDER — preserve plain-class ASCII dunder exclusion.

**Evidence:**

- [Plain-class schema](<../../../.pgmcp/template_suite/python_class/context.schema.json>)
- [Public-boundary regression tests](<../../../tests/mcp_server/integration/templates/test_shared_python.py>)

**Outcome:** Compact consumer-local exclusion; other composition unchanged.

### D\_REGRESSION — durable shared/all-eight acceptance, rejection, size and Unicode-content coverage.

**Evidence:**

- [Public-boundary regression tests](<../../../tests/mcp_server/integration/templates/test_shared_python.py>)

**Outcome:** Native lexical oracle, public schema boundary and rendered AST/compile evidence; no private test access or runtime policy added.

### D\_CLEANUP — migrate obsolete Unicode pytest class acceptance contexts.

**Evidence:**

- [Unit-family tests](<../../../tests/mcp_server/integration/templates/test_pytest_unit_test.py>)
- [Integration-family tests](<../../../tests/mcp_server/integration/templates/test_pytest_integration_test.py>)

**Outcome:** ASCII positive discovery scenarios preserved; Unicode names rejected; normalization-only ceremony removed.

## Evidence

### Schema size — all eight live discovery resources materially reduced.

Count Unicode codepoints in the complete attached JSON resource strings, matching Research serialization (json.dumps ensure_ascii=False); recursively count pattern strings separately. The supported producer restart refreshed its immutable catalog; all eight after-values are fresh resources. These are neither bytes nor token counts.

| Package | Before codepoints | After codepoints | Reduction | Patterns before → after | Pattern codepoints before → after |
| --- | ---: | ---: | ---: | ---: | ---: |
| python_class | 107615 | 12635 | 88.26% | 27 → 26 | 96952 → 2096 |
| python_protocol | 107412 | 12508 | 88.36% | 26 → 25 | 96914 → 2079 |
| python_adapter | 126860 | 16462 | 87.02% | 35 → 32 | 112433 → 2217 |
| python_worker | 126764 | 16366 | 87.09% | 35 → 32 | 112433 → 2217 |
| python_pydantic_dto | 107957 | 11892 | 88.98% | 27 → 26 | 98219 → 2286 |
| python_pydantic_config | 107839 | 11774 | 89.08% | 27 → 26 | 98219 → 2286 |
| pytest_unit_test | 135575 | 16588 | 87.76% | 38 → 37 | 121314 → 2505 |
| pytest_integration_test | 135582 | 16595 | 87.76% | 38 → 37 | 121314 → 2505 |

Catalog generation: producer process PID 28508, server 2.0.0, supported restart after suite edits. Independent QA connection PID 10104 retained the original immutable startup catalog. QA independently reproduced the <25000 public fresh-loader bound and accepted implementation, but did not claim the exact live percentages as independently reproduced. Fresh producer discovery identities (authored package version 1.0.0 throughout):

| Package | Resolved fingerprint | Receipt |
| --- | --- | --- |
| python_class | `u_KOYBekCfsMbBaW` | `pgmcp://cache/runs/6019849b7a66421ca447cedd4cda24f3` |
| python_protocol | `MCI7ao7ktCGpVdAM` | `pgmcp://cache/runs/e09a5c805f3140d4a35e499937c58547` |
| python_adapter | `ZLqBKfYUY8QFmoRy` | `pgmcp://cache/runs/9ab1f8ceeedb4f2598553db75d6c9b85` |
| python_worker | `nje81vHOtlNTERvf` | `pgmcp://cache/runs/495258002db541fa90bb2482c218f093` |
| python_pydantic_dto | `QqfSP7PZ6WteOp8N` | `pgmcp://cache/runs/d629fb22100e4cb0bf36b38621f80786` |
| python_pydantic_config | `yu0P_hDamXNCU0Kn` | `pgmcp://cache/runs/eabb106b188c4149952fb81858211d07` |
| pytest_unit_test | `KRDrELWyqBOkV_fS` | `pgmcp://cache/runs/ecd0484a372f4c37beb9fd411ec43ec9` |
| pytest_integration_test | `70EjvGU6LK1YPSz3` | `pgmcp://cache/runs/408dd4478d0348b79cb60896adf243cf` |

**Sources:**

- [Research baseline and strategy](<research.md>)
- [Shared Python schema](<../../../.pgmcp/template_suite/shared/definitions/python.schema.json>)
- [Plain-class schema](<../../../.pgmcp/template_suite/python_class/context.schema.json>)
- [Public-boundary regression tests](<../../../tests/mcp_server/integration/templates/test_shared_python.py>)

**Invocation:** scaffold_schema(artifact_type=<each of eight registered Python/pytest IDs>)

**Observed Result:** All eight resources between 11774 and 16595 codepoints; reductions 87.02%–89.08%. No model tokenizer installed, no token estimate or latency/model-quality claim.

### Final focused verification and changed-test quality.

Final nine-file suite d64e62b6fbe7402b9527bbfcde4704c3: 81 passed, 9 warnings in 13.46s, exit 0, capture not truncated, args_source=configured, effective_args=[], no rejection/termination problem. Three-file format/lint/Pyright 007ad35d3f40435a84d150424443189a passed; final shared-only frozen-context correction recheck 6ccc845d4cc5485692cbb8e5cb74d224 passed. Other two test sources unchanged since three-file checks.

**Sources:**

- [Public-boundary regression tests](<../../../tests/mcp_server/integration/templates/test_shared_python.py>)
- [Planning verification route](<planning.md>)

**Invocation:** run_tests(scope='targets', targets=[shared test and eight family files], timeout_seconds=600); run_checks(scope='targets', checks=['python_format','python_lint','python_pyright'], timeout_seconds=300)

**Observed Result:** Complete passing native evidence, reusable until source invalidated.

### V\_FULL — complete configured suite and branch links.

One run_tests(scope='configured', timeout_seconds=1200), no targets/partitions/argument overrides, receipt df43f212154c4713804a67bc03e71a76: 2807 passed, 1 skipped, 1 xpassed, 229 warnings in 378.41s (6m18s), native exit 0. Python 3.13.7, pytest 9.0.2, eight workers, 2809 collected items, configured testpaths tests/mcp_server; capture not truncated, no request rejection or termination problem, args_source=configured and effective_args=[]. Complete 804926-codepoint DTO assembled with contiguous bounded pages and verified SHA-256 once. Branch markdown_link_review receipt 341b5283f341473d90c57cad94c51af6: passed, 8 successful link occurrences, 3 configured exclusions, 0 errors/unknown/unsupported/timeouts, native exit 0; configured offline/cache=false/include-fragments arguments unchanged. Post-scaffold branch markdown_link_review 30742d67bc3b4f14b8b4a52812aa4d9d also passed, including this report.

**Sources:**

- [Native Pytest configuration](<../../../pyproject.toml>)
- [Approved gate selection](<planning.md>)

**Invocation:** run_tests(scope='configured', timeout_seconds=1200); run_checks(scope='branch', profile='markdown_link_review', timeout_seconds=300)

**Observed Result:** Native adapters report passed; exact skipped/xpassed/warning totals retained as caveats. Independent QA disposition requested.

## Demonstration

Four actual live scaffold_artifact calls after producer catalog restart generated minimal/populated plain class and DTO artifacts in ignored .pgmcp/temp/issue486-scaffolds. Receipts fb84588898d34819baa46480336c00f7, 73de7e55e6914172ac89c4e3fc202c17, d7f30f4fa1854234b90f7bc4a3e13129 and 34676baf50d24289bb9eee1801f5ee0d: written=true with enforce native syntax passed. Source inspection confirmed ASCII declarations, distinct Unicode module/class prose, relative import/alias, raw list[雪] type expression, Unicode defaults/examples and frozen DTO output. Scratch artifacts are not repository deliverables. Syntax does not prove arbitrary dependency execution.

## Preservation

Shared definitions and unchanged existing family tests retain keywords/soft keywords, relative imports and star restrictions, discovery prefixes, injected self/constructors, exact reserved Pydantic names, frozen configuration, ordering, provenance and native syntax rejection. Unicode prose, literals/defaults/examples, raw bodies and type expressions retain their contracts. No templates, manifest, policy, production Python, resolver, renderer or generic test helper changed.

## Containment

Production/config diff is limited to two schema owners; test diff is limited to three established regression files. Targeted schema edits used supported report mode because JSON has no configured native preflight selection: validation_status=not_executed, not a pass. Public loader/schema and native family evidence establish JSON/schema validity; no check policy or gate was disabled.

## Failures

- RED 4d7f0ff3c1ba40bcb4f029d668fb5421: 28 failed, 13 passed, 9 warnings. New ASCII/size failures were intended; one populated config setup omitted required frozen and is not valid ASCII RED evidence.
- Schema enforce preflight declined without writing (not_executed/no checks); f154a0b7322049eeabe075a7f7af8997 then still tested unchanged schemas and failed. It is not GREEN evidence.
- Initial actual GREEN b7e513ed7ae646a2b19ba35321aec9e3: 3 failed, 78 passed; 7ac5246038894303a5312a0932acb0e5: 1 failed, 80 passed. Obsolete fullwidth pytest scenarios and missing frozen positive context were corrected before final passing run.

## Caveats

- Coverage is opt-in in native pyproject.toml. No coverage percentage is asserted; configured invocation preserves native workers/arguments without overrides.
- Nine focused warnings report the existing SchemaAttachment schema/BaseModel shadowing warning; no new production Python change.
- Push/PR remains blocked by automatic egress review pending explicit trusted-destination human authorization; no CLI, UI or cross-chat bypass.
- Full-suite SKIPPED: tests/mcp_server/core/test_proxy.py::TestProxyIntegration::test_end_to_end_restart_flow (existing explicit manual integration placeholder). Full-suite XPASS: tests/mcp_server/unit/managers/test_enforcement_runner_unit.py::TestGitCommitToolC3::test_server_renders_exclusion_note_in_response, existing xfail(strict=False) C8 separate-issue note. Both source files unchanged; no new skip, xfail or suppression in changed tests. XPASS is retained, not converted to an ordinary pass. Independent #486 QA must disposition these facts.
- 229 full-suite warnings include existing Pydantic field shadowing, deprecated MCP read_resource/AnyIO/GitHub APIs, pre-existing asyncio marker warnings and an unawaited restart coroutine warning. No unrelated warning cleanup is included in #486.

## Related Documents

- [Approved Research](<research.md>)
- [Design](<design.md>)
- [Planning](<planning.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-05 | @imp validator | Record native verification, public discovery measurements and preservation evidence. |
