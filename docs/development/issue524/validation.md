<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=dfPHW469kz8S1nLL sf=WI5iXHBKVOU91bYE -->

# Issue \#524 — Cache-notice validation

**Status:** Observed evidence complete; independent review requested  
**Version:** 1.0  
**Last Updated:** 2026-10-19

## Issue Number

#524

## Scope

Validate C_1 notice-value correction (cf6ccde6be0ac295d1d82d3b3466c910d4e32667) and C_2 existing-test consumer repair (5b8dbaaee235095d68d70da9635874f7ee5a84ce). Production change remains two configured strings and one existing presenter fallback literal. No interface, transport, limiter, cache, configuration-admission or public output change.

## Obligations

### C\_1 / D\_1.1: truthful existing notices

**Evidence:**

- [Configured messages](<../../../.pgmcp/config/defaults/presentation.yaml>)
- [Generic fallback](<../../../mcp_server/presenters/text_presenter.py>)
- [Approved wording and limits](<design.md>)

**Outcome:** Direct review confirms cache/text facts only: no complete-data loss, full-inline or client/model-access claim.

### C\_1 / D\_1.2 and C\_2 / D\_2.1: preserve response behavior

**Evidence:**

- [Shipped-config server/SDK cases](<../../../tests/mcp_server/integration/test_execution_presentation_v3.py>)
- [Pipeline controls](<../../../tests/mcp_server/integration/test_pipeline_e2e.py>)
- [Presenter marker/fallback cases](<../../../tests/mcp_server/unit/test_presenter.py>)

**Outcome:** Existing test families cover success/failure publication, small/large payload, original success/error and exact structured operation, valid cache/readback/paging or no URI, selected configured warning/tail, and omitted optional warning key. Existing no-operation/processing-error and limiter controls remain.

## Evidence

### Final native configured suite

3000 passed in 607.36s (0:10:07), native exit 0; Python 3.15.0 / pytest 9.1.1, eight workers, effective_args=[] / args_source=configured. No termination or request-rejection problem. All five shipped-cache cases, pipeline cache-fallback and no-structured-response processing/unknown-tool controls appear as PASSED in this full run. Coverage is opt-in and was not requested.

**Sources:**

- [Native test settings](<../../../pyproject.toml>)

**Invocation:** run_tests(scope="configured", timeout_seconds=1200)

**Observed Result:** Passed. Receipt 6d19f80fc18746f3988b8c6d207cd731 is supplementary. Cache size checked first (848,316 characters); bounded header/tail reads confirmed native scope, count, result and metadata without bulk assembly.

### Final relevant branch gates

All five checks passed, each native exit 0. Ruff formatted four changed Python files with no lint findings; branch Pyright selected the changed production file and reported zero errors/warnings. YAML passed. Markdown: 16 successful local link occurrences, one external offline exclusion, zero errors. Python tests also have fresh explicit-target Pyright passes from C_1/C_2; no test strict-Mypy requirement was introduced.

**Sources:**

- [Planning selections](<planning.md>)

**Invocation:** run_checks(scope="branch", checks=["python_format","python_lint","python_pyright","yaml_configuration","markdown_links"], timeout_seconds=600)

**Observed Result:** Cached result read and assessed; supplementary receipt 9249e310f1af423d92ecc4ee03f12b46. External exclusion is not a reachability pass.

### Fresh production-Mypy evidence reused

Passed on 192 production source files, native exit 0. The tests.* unused-section note is retained; it is a native informational note under the production-only selection. C_2 changed only a test file, so neither production nor native checker config invalidated this pass.

**Sources:**

- [Mypy native scope](<../../../pyproject.toml>)

**Invocation:** run_checks(scope="configured", checks=["python_types"], timeout_seconds=600)

**Observed Result:** Receipt a49d42d32a644519927919c81aec8738; cached result read. Reuse explicitly reviewed by independent QA at C_2 progression.

### Focused proof and negative history

C_1 four-module focus: 55 passed in 17.56s; changed-file format/lint/Pyright and YAML passed. C_2 pipeline scope: all three existing cases passed in 57.07s, with its file gates passed. Initial Implementation had two overstrict ordinary-warning assertions under truncation; they were corrected to the required reserved tail. The first full Validation was genuinely failed: 1 failed / 2999 passed in 579.99s, exit 1, receipt 1f1a5644fb0e405fa413a07002e7e610. It exposed a missed old-prose assertion and an unconditional cache-reference test instruction. Audited return to Planning appended C_2 while preserving committed C_1; no forward gate waiver. Final full suite above is new passing evidence, not a reinterpretation of that failure.

**Sources:**

- [Recovery and exact focused calls](<planning.md>)

**Observed Result:** Focused receipts 002a24c1faa447f3b3af3e00a24a2a42 and 3ea265b4012342b79c6118ee99d9e4c5. No new test modules; four net parameter cases added to existing families.

## Demonstration

Safely reproduce the cache cases through the controlled publisher interface and real server/SDK fixture: run_tests(scope="targets", targets=["tests/mcp_server/integration/test_execution_presentation_v3.py"], tests=["python_tests"], args={"python_tests":["-k","test_shipped_cache_delivery_preserves_operation"]}, timeout_seconds=300). Successful publication provides a real readback; failed publication supplies no cache URI. Short text retains its configured warning; overflow retains the no-cache truncation tail within 8000 UTF-8 bytes. The original structured operation and isError are checked in every case. No live workspace cache is deliberately broken.

## Preservation

Original DTOs, diagnostics and success/error flags are unchanged. Server-owned structuredContent is independent of the text budget; this establishes delivery by the server, not a client/model access guarantee. The optional-key generic fallback stays in its existing presentation owner. No new suppression, legacy path, version matrix, threshold change or compatibility layer.

## Containment

Post-suite git_status showed only the expected state.json phase audit as modified. Project-plan readback still contained unchanged C_1/D_1.1–D_1.2 and appended C_2/D_2.1. No production/test/planning mutation occurred during the suite.

## Deferred Work

### Planning-update informational note formatting

While appending C_2, update_planning_deliverables succeeded and readback confirmed both cycles, but its informational note rendered: Flat scalar sequence formatting requires formatting policy and max_items. This is outside the three notice-value correction. Impact: degraded guidance text, not a failed plan update; exact receipt 86f004bbd3b844e9b1f46ea5db458d9e supplements the observation. Co triage required; no separate issue selected or repair performed here.

**References:**

- [Recorded recovery](<planning.md>)

### Existing \#523 output-policy questions remain separate

Metadata publication, client-instruction guarantees and total payload policy were already transferred for owner/Co consideration. #524 selects none of those policies.

**References:**

- [#523 Research](<../issue523/research.md>)

## Related Documents

- [Planning and stored deliverable mapping](<planning.md>)
- [Approved Research](<research.md>)
- [Design](<design.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-19 | @imp validator | Record final full/gate evidence, retained failures and bounded test recovery. |
