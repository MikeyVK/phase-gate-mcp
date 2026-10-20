<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=dfPHW469kz8S1nLL sf=WI5iXHBKVOU91bYE -->

# Issue \#528 — compact recovery validation

**Status:** Validation complete — independent review requested  
**Version:** 1.0  
**Last Updated:** 2026-10-20

## Purpose

Verify truthful post-operation recovery without replaying original payloads or adding a second presentation pipeline.

## Scope In

C_1 / D_1.1–D_1.3 on implementation commit 3426baea7698bd46e65da44496b3ba10848202dc; existing normal profiles, output schemas and startup presentation.

## Scope Out

No legacy bridge, dependency/harness matrix, domain-operation change, new cache publication/retrieval or broad test rewrite.

## Issue Number

#528

## Cycle

C_1

## Validation Status

PASS

## Obligations

### Actual operation outcome survives later response failure

**Evidence:**

- [Real SDK cases](<../../../tests/mcp_server/integration/test_tool_attachment_transport.py>)

**Outcome:** Known success and failure retained across three shipped profiles and successful/failed cache receipts; schema validated even when isError=true.

### Recovery avoids the failing large-data path

**Evidence:**

- [Small recovery entrypoint](<../../../mcp_server/presenters/response_presenter.py>)
- [Presenter behavior tests](<../../../tests/mcp_server/unit/test_presenter.py>)

**Outcome:** Original serializer called once; original operation, notes and attachments absent from recovery. No normal rendering/resource conversion or repeated execution/publication. Diagnostic codepoint prefixes bounded before encoding; message and traceback share one UTF-8 allowance.

### Finite failure boundary and configuration-independent startup

**Evidence:**

- [Server boundary](<../../../mcp_server/server.py>)
- [Startup presenter](<../../../mcp_server/presenters/startup_recovery_presenter.py>)

**Outcome:** One failed recovery attempt ends at existing SDK/log boundary with primary/secondary causes and known outcome. Startup compact output uses fixed both-channel contract.

## Evidence

### Behavioral RED then focused GREEN

RED 5b28120c: 1 failed, 4 deselected in 1.48 s at incorrect is_error=true after successful operation (receipt 9ec02d903a494d90a46657586471ebb9). Corrected: 16 passed, 4 deselected in 2.33 s (a7461800564c411fa4661fa68b61b393). Poisoned original grows from 700 to 7,000,000 chars; output stays below 20,000 chars and sizes differ by less than 100; full original serialization is not retried.

**Sources:**

- [SDK reproduction](<../../../tests/mcp_server/integration/test_tool_attachment_transport.py>)

**Invocation:** run_tests(scope='targets', targets=['tests/mcp_server/integration/test_tool_attachment_transport.py'], tests=['python_tests'], args={'python_tests':['-n','0','-k','processing_failure']}, timeout_seconds=300). Corrected selection uses -k 'processing or secondary_recovery or startup_presenter'.

### Direct consumers and existing normal-profile behavior

167 passed in 34.07 s, native eight workers (632f5d2520e24626a06021c4f7dab90f). Supplementary presenter/model scope: 34 passed in 14.33 s (7345ab4fd727480f83a7f13c3c12db82).

**Sources:**

- [Presenter/model behavior](<../../../tests/mcp_server/unit/test_presenter.py>)
- [Existing channel/SDK cases](<../../../tests/mcp_server/integration/test_execution_presentation_v3.py>)

**Invocation:** run_tests(scope='targets', tests=['python_tests'], timeout_seconds=600), no args; targets: tests/mcp_server/{integration/test_tool_attachment_transport.py,unit/schemas/test_presentation_output.py,unit/config/test_presentation_config.py,unit/core/interfaces/test_presenter_interfaces.py,unit/test_presenter.py,integration/test_execution_presentation_v3.py,integration/test_cache_fidelity_v3.py}. Brace notation denotes seven explicit paths, not a native glob.

### Branch gates

All five passed; native exits 0; per-check branch filters retained (bffbc074985a408bb18687146100652b).

**Sources:**

- [Check configuration](<../../../.pgmcp/config/checks.yaml>)

**Invocation:** run_checks(scope='branch', checks=['python_format','python_lint','python_pyright','markdown_links','yaml_configuration'], timeout_seconds=600)

### Workspace configured Python gates

All four passed, including production-scoped Mypy; no test-Mypy expansion or checker relaxation (fe92aee32d024c31810490c0ef73cca9).

**Sources:**

- [Native tool configuration](<../../../pyproject.toml>)

**Invocation:** run_checks(scope='configured', checks=['python_format','python_lint','python_types','python_pyright'], timeout_seconds=600)

### Full native suite

First required run: **1 failed, 3097 passed in 615.14 s**, native exit 1, no termination problem (c79015b2283642a1950ebbc9835f56ee). The unchanged Windows lifecycle case `test_failure_stops_live_children_and_keeps_primary_cause[late-timeout]` failed waiting for child PID files. A targeted recheck of all four variants with native eight workers passed: **4 passed in 51.37 s** (868668b7397e4c99b4b192401eee6844), using the same test file and `-k test_failure_stops_live_children_and_keeps_primary_cause`. Exact configured full-suite repeat, with the same unchanged native settings: **3098 passed in 554.83 s**, native exit 0, eight workers, no termination problem, no warnings/skips reported (3f1bdcb51de64043b28271dbab84710a). The repeat is a positive verification result, not causal repair of the earlier readiness failure.

**Sources:**

- [Native test configuration](<../../../pyproject.toml>)

**Invocation:** run_tests(scope='configured', tests=['python_tests'], timeout_seconds=1800), no args override

### Active instance and catalog evidence boundaries

New active Imp instance PID 12808 healthy, normal structuredContent.processing_error=null; receipt 3da596ce2f7445ec9c79a6ad439cd52f. Actual tools/list and response-schema conformance exercised through real SDK clients against current source. QA's separate existing MCP process PID 70284 still returned earlier envelope; no claim all client catalogs were refreshed or that a live presenter crash was injected.

**Sources:**

- [SDK listing and schema validation](<../../../tests/mcp_server/integration/test_tool_attachment_transport.py>)

**Invocation:** restart_server(reason='Activate #528 compact response-processing recovery after focused GREEN commit 3426baea; public tool inputs unchanged.'), then health_check() and get_work_context().

## Demonstration

Reviewable isolated reproduction: run_tests(scope='targets', targets=['tests/mcp_server/integration/test_tool_attachment_transport.py'], tests=['python_tests'], args={'python_tests':['-n','0','-k','processing or secondary_recovery or startup_presenter']}, timeout_seconds=300). This uses real SDK calls with controlled presentation faults; it does not corrupt the active server or repeat live mutations.

## Preservation

Operation DTO/cache ownership and normal rendering remain unchanged. Only compact processing recovery may substitute an existing resource reference/null for normal inline delivery. Shared frozen model remains field/schema authority; configuration owns ordinary recovery wording. No original DTO is mutated.

## Containment

Diagnostic details alone are bounded. Complete recovery JSON, known outcome and short notice are protected; arbitrary full-result/guidance delivery after presenter failure is explicitly not promised. A reference is only a location hint for the already-cached operation, not attachments/notes/later diagnosis or guaranteed client access.

## Failures

- First full native run: the lifecycle preparation timed out before the asserted stop checks, as detailed above. Source inspection shows that the late variant's one-second invocation budget includes parent/child startup, while the test requires published child PIDs before retaining their handles. Earlier runtime termination can therefore race test readiness; this is a source-supported mechanism, not a traced timing proof of this run. No production or test code, deadline, parallelism or quality policy was changed. The same case had also failed transiently during #529. The exact full native repeat passed, as recorded above. The intermittent readiness risk remains unresolved and requires explicit independent QA disposition; no rerun-until-green sequence or causal repair is claimed.
- Earlier eight-file scope added integration/test_target_startup.py to the seven-file selection: 176 passed, 2 initialize-timeout failures in 249.91 s (d7779e7b19f14150a3d868007553006a). Both unchanged cases passed -n0 targeted recheck: 2 passed, 29 deselected in 21.44 s (485010ab40594cfd94d62c668ae6e2f1); independent QA repeated the same two with native eight workers: 2 passed in 22.29 s. Neither recheck proves the original timing cause; full native suite remains mandatory.
- Initial SDK test setup 19a99bb37c97410bbb85b178279ffe81: 7 failed, 9 passed, 4 deselected in 3.10 s; six invalid failed-cache test receipts and one wrong expectation of a tool result instead of terminal SDK exception. Test setup corrected, no policy change.
- Initial presenter/model tests 18d77ef7dd5f4b8aa4d185d822e70a7b: 2 failed, 32 passed in 12.62 s; over-exact text assertions ignored existing pagination guidance. Assertions corrected to input-derived behavior, no product change.
- Initial target gates a340d83009124c8d938158aa2cc3a61d found one formatting issue, loop capture and optional narrowing in tests. Fixed without suppressions. All 11 changed Python files subsequently passed format/lint/Pyright (aef966fc2a20471faac171390325decd); final affected three-file recheck 8a1a8372e2e2445b9d93ca6ff89150be also passed.

## Caveats

- The first full suite failed and the unchanged exact repeat passed. The authored PASS reports the current native/gate outcomes; independent QA must explicitly decide whether the recurring readiness failure blocks progression. No phase approval or fix of that failure is claimed.
- In-process recovery cannot guarantee delivery after SDK/transport failure or memory exhaustion. A secondary recovery fault remains terminal; no third fallback.

## Related Documents

- [Approved strategy](<research.md>)
- [Compact design](<design.md>)
- [Execution plan](<planning.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-20 | @imp validator | Record compact recovery, both full native results, exact gates, negative history and explicit unresolved readiness risk for independent review. |


