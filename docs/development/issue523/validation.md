<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=dfPHW469kz8S1nLL sf=WI5iXHBKVOU91bYE -->

# Issue \#523 — Validation evidence

**Status:** Observed evidence assembled; independent review requested  
**Version:** 1.0  
**Last Updated:** 2026-10-19

## Purpose

Record observed verification of the research-only delivery; independent QA owns progression.

## Issue Number

#523

## Scope

Research and durable evidence packaging only. No production, runtime configuration or permanent test changes. Tested product baseline: main 78f270833f2ec85c8f80a8ad72a60559c3a4ea68; final packaging commit ca863a7d0dc6e7e5365ba3d5d8d7ad2aff811385. Only the regular phase audit and this report were pending during Validation.

## Evidence

### Configured native test suite

2026-10-19: Python 3.15.0 / pytest 9.1.1, 8 workers, tests/mcp_server. No caller arguments: configured effective_args=[]. Native outcome: 2996 passed in 566.34s (0:09:26), exit 0; no reported test failures, skips or xfails in the terminal summary. termination_problem=null and request_rejection=null. Coverage remains opt-in and was not requested; no new coverage percentage is claimed. Evidence ends with a non-fatal stdout_closed text line; the adapter reports successful completion and zero captured stderr bytes.

**Sources:**

- [Native test configuration](<../../../pyproject.toml>)
- [Public attachment/transport cases included](<../../../tests/mcp_server/integration/test_tool_attachment_transport.py>)

**Invocation:** run_tests(scope="configured", timeout_seconds=1200)

**Observed Result:** Passed. Supplementary receipt 38ef6ea3991a4379a3c2f440b6ea93de. Cached result size was checked first (847,202 characters); bounded header/tail reads confirmed selected scope, workers, final count, native arguments, exit and termination fields. No bulk assembly or routine hash recomputation.

### Branch Markdown gate

Passed: native Lychee 0.24.2 exit 0; 25 link occurrences, 14 successful local occurrences, 11 external exclusions, zero errors. Effective native args: --offline --cache=false --include-fragments. External exclusions are not external reachability passes; primary source contents were inspected during Research.

**Sources:**

- [Research](<research.md>)

**Invocation:** run_checks(scope="branch", checks=["markdown_links"], timeout_seconds=120)

**Observed Result:** Cached result read and assessed; supplementary receipt f748b9fca8da427992e999b951e37dca. No Python or JSON-schema sources changed; those selectors would not prove this Markdown-only delta.

### Research observations and limitations remain traceable

Reuse fresh Research evidence: one probe passed in 13.75s; 37 tokenless / 49 credential-selected tools, zero published output schemas; four actual operation DTOs JSON-Schema-valid. Payload measurements, failure semantics, source-based client observations and unknown native-client behavior are explicit. The temporary probe is not part of the permanent test suite.

**Sources:**

- [Findings and full probe recipe](<research.md>)

**Invocation:** run_tests(scope="targets", targets=[".pgmcp/temp/issue523/test_output_observation.py"], tests=["python_tests"], args={"python_tests":["-q","-n","0","-s"]}, timeout_seconds=300)

**Observed Result:** No production changes invalidated the observation; full reproduction is durable, not dependent on receipt 94f3d34a00ef43d79b8fbdb033eaa362.

## Preservation

Actual operation structuredContent, optional schema metadata path, configured text, embedded resources and cache behavior are unchanged. The existing #517 owner decision and #462 closure remain binding. No universal schema policy, channel removal, routing bridge or compatibility suite was implemented.

## Containment

Branch inventory before this report: Research plus initialized .pgmcp/state.json and .pgmcp/deliverables.json only. Post-suite git_status reported only the expected state.json phase audit as modified; no test-induced product or planning mutation. No temporary probe, generated artifacts, host configuration or secrets are tracked.

## Caveats

- These measurements establish server/SDK field sizes and four representative DTOs, not model token counts, all tool outcomes or installed-harness compatibility.
- The full suite verifies existing behavior; it does not repair or approve the catalog metadata exposure gap.
- No separate performance, coverage or client/dependency matrix is claimed.

## Deferred Work

### Catalog output metadata exposure and success/error schema contract.

Confirmed normal wrappers hide metadata; effects and contract variants are documented in Research. Changing publication is outside this research-only issue and needs an owner decision. Impact: clients currently lack advertised output validation metadata. Co triage required; no implementation issue selected here.

**References:**

- [Research follow-up boundaries](<research.md>)

### Client delivery guarantees, presentation-only instructions and structured payload size.

VS Code source indicates full JSON forwarding and omission of content text; other native harness behavior is not fully measured. Define supported information guarantees and a measurable objective before considering a runtime policy. Co/owner triage required; no channel removal or compatibility project selected.

**References:**

- [Client matrix and payload observations](<research.md>)

### Cache failure truth remains with \#524.

Existing separately scoped follow-up; not implemented in #523. Preserve sequence and avoid conflating cache failure with the output-delivery findings.

**References:**

- [Issue #524](<https://github.com/MikeyVK/phase-gate-mcp/issues/524>)

## Related Documents

- [Authoritative Research and strategy](<research.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-19 | @imp validator | Record configured suite, branch gate, evidence freshness, limitations and scoped deferred findings. |
