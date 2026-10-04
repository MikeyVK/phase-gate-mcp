<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=CT9NV5LmQjKHFGqX sf=FAN5Vr-4vcbMMjZ2 -->

# Issue 473 — Validation

**Status:** Validation complete under reviewed gate disposition; independent review requested  
**Version:** 0.6  
**Last Updated:** 2026-10-04

## Purpose

Assess the approved first-call template corrections with the configured full native suite, branch-wide checks and the existing actual-output inspection evidence.

## Scope In

Configured full-suite execution, configured branch Python and Markdown checks, corrected-behavior and preservation mapping, current-tool limitations and independent Validation review.

## Scope Out

Generic issue476 consumption enforcement, unrelated CLI/proxy/adapter repairs, additional automated content/regression tests, Documentation/Ready progression and merge.

## Issue Number

#473

## Validation Status

PASS

## Scope

bug/473-first-call-template-quality against parent main; production/template/test content reviewed at 1a0360ac plus evidence-only 9d27e4d2. No production, template or test changes during this Validation attempt.

## Obligations

### V\_FULL\_TESTS — complete native-configured test result

**Evidence:**

- [Planning](<planning.md>)

**Outcome:** Fresh post-cycle5 configured suite passed: 2775 passed, 1 skipped, 1 xpassed, 229 warnings in 326.96 seconds. Earlier incomplete/negative attempts remain historical evidence; see Latest Validation after cycle 5.

### V\_BRANCH\_CHECKS — configured Python review and branch Markdown links

**Evidence:**

- [Python review receipt](<pgmcp://cache/runs/bce86b0768b64271b8fdf2f1632a1d3d>)
- [Markdown review receipt](<pgmcp://cache/runs/944deb18930d44a49d17924aa388146d>)

**Outcome:** Explicit issue473-specific replacement gate coverage accepted by independent QA and passed: all 25 changed Python files have format/lint/Pyright coverage, three production files have Mypy coverage, and the reviewed 24-file Markdown selection passes. Original negative branch calls and four source/runtime link exceptions remain recorded; see Latest Validation after cycle 5.

### V\_CORRECTED\_BEHAVIOR — all nineteen families and approved preservation obligations

**Evidence:**

- [Final manual inventory](<manual-inspection.md>)
- [Exact contexts and outputs](<first-output-evidence.md>)
- [Deliverable mapping](<implementation.md>)

**Outcome:** Reuse unchanged actual minimal/filled first outputs for 19 families (38 files), six final document boundaries and explicit code boundaries; independent Implementation QA verified the current package identities and repeated bytes. This is scoped correction evidence, not a substitute for V_FULL_TESTS/V_BRANCH_CHECKS.

## Evidence

### Full configured test attempt preserves configured arguments

The call returned an MCP error: timed out awaiting tools/call after 300s. There is no result URI. No pass/fail/skip/warning totals or native completion status can be inferred.

**Sources:**

- [Configured tests](<../../../.pgmcp/config/tests.yaml>)
- [Native Pytest configuration](<../../../pyproject.toml>)

**Invocation:** run_tests({"scope":"configured"})

**Observed Result:** Transport timeout; full native result unavailable

### Configured branch-wide checks use the approved broad scopes

The original Python and Markdown calls are unchanged; no extension filtering, alternate args, timeout override or weakening was introduced.

**Sources:**

- [Configured checks](<../../../.pgmcp/config/checks.yaml>)

**Invocation:** run_checks({"scope":"branch"}); run_checks({"scope":"branch","profile":"markdown_link_review"})

**Observed Result:** Python incomplete; Markdown passed

### Actual corrected outputs remain fresh

There were no production/template/test edits after independent Implementation review. QA independently checked all 19 current fingerprints, 38 final pairs, six final boundaries and 26 repeated document/boundary outputs, plus 234 passing targeted tests (27 existing warnings). Overlapping producer/QA runs are not summed as unique coverage.

**Sources:**

- [Manual inspection](<manual-inspection.md>)
- [Lossless final outputs](<first-output-evidence.md>)

**Observed Result:** Scoped unchanged correction and preservation evidence

## Demonstration

Replay the exact selected scaffold requests in first-output-evidence.md into an isolated output directory after discovering the current context schema and refreshing that MCP client's catalog. Inspect pristine output before any fixes. The archive distinguishes intermediate outputs from the final c2_verified_* code and c3_final_* document/tracking outputs. Seven full-document families have metadata and a visible Version History; Issue/PR/Commit keep their separate contracts. Native Python formatting/lint evidence applies to the clean caller examples; arbitrary authored prose, code and dependencies remain caller-owned.

## Preservation

The manual and lossless archive evidence covers blank-edge normalization with retained interior CRLF, Markdown hard-break spaces, indentation, fenced content, Unicode and literal values; defined emptiness versus absence; False/0/None and raw ValidationSpec JSON values; explicit module/class prose; revision order and final-supplied current revision; raw generic engine output. The approved clean break rejects old root fields before writing and adds no compatibility bridge.

## Containment

The new normalization lives as one pure generic text_block filter in the existing engine registration; shared Jinja owns generated joins and terminal LF. Real bootstrap, CLI/delivered/installed and shared fixture admission use that registration before rendering. Current concrete known consumers and active instructions were migrated; historical issue460 artifacts were not mass-rewritten.

## Failures

- The full configured native suite has no returned complete result after the 300-second transport timeout.
- The required branch Python review is incomplete and includes native lint and Mypy failures; exact verified rows must remain visible.

## Caveats

- Validation status is a producer evidence assessment and does not grant independent QA approval.
- The three independent native calls were dispatched concurrently; the observed test timeout does not establish whether contention, transport deadline, suite duration or another native cause dominated.
- Content syntax/preflight success cannot prove arbitrary dependencies or all document semantics.
- Offline Markdown links prove configured local/fragment availability, not live remote availability.
- No new automated content assertions, snapshots or permanent matrix harness were added.

## Deferred Work

### F6 — invalid template admission can terminate bootstrap while proxy loses diagnostics and logs false readiness.

The approved template correction restores this branch's admission. CLI/proxy lifecycle repair remains separately scoped and must preserve invalid-suite rejection while exposing actionable diagnostics and a recovery path.

**References:**

- [F6 reproduction and ownership](<tool-practice-findings.md>)

### F1–F5/F7 and any confirmed broad-scope check or timeout friction

Retain exact current observations for later coordination triage; distinguish supported usage limits and producer sequencing from confirmed product defects. No historical pre460 score is claimed.

**References:**

- [Tool-practice findings](<tool-practice-findings.md>)

### Issue476 — generic schema/template consumption analysis and enforcement

Explicitly excluded by the approved issue473 scope. Concrete packages and known inputs were corrected here.

**References:**

- [Approved Strategy](<research.md#approved-strategy>)

## Related Documents

- [Research and Approved Strategy](<research.md#approved-strategy>)
- [Design](<design.md>)
- [Planning](<planning.md>)
- [Implementation](<implementation.md>)
- [Manual inspection](<manual-inspection.md>)
- [Exact first-output evidence](<first-output-evidence.md>)
- [Current tool findings](<tool-practice-findings.md>)

## Verified native outcome appendix

The three independent calls were dispatched concurrently with their configured defaults. The configured test call reached the MCP client deadline after 300 seconds. No returned test DTO/cache URI exists, so this report does not assert native timeout, native completion, test totals or a new server crash. A subsequent health_check reported healthy PID21692; its receipt is pgmcp://cache/runs/70d94f67da894b09951eab269e7b1800. The full-suite obligation remains open.

| Check | Exact observed outcome | Native information / evidence limit |
| --- | --- | --- |
| python_format | unavailable / execution_error | Ruff 0.15.6; exit3; “Failed to format .agents\workflows\create-issue.md: Markdown formatting is experimental, enable preview mode.” Diagnostic output also proposes formatting the JSON deliverables file. No fix was applied. |
| python_lint | failed | Ruff 0.15.6; exit1; B018 at .pgmcp\deliverables.json:1:1, followed by substantial diagnostics on non-Python source files. The result is a native failure, not an accepted branch-wide Python pass. |
| python_types | failed | Mypy 1.19.1; exit1; .agents\workflows\create-issue.md:15: “Invalid character '—' (U+2014) [syntax]”; “Found 1 error in 1 file (errors prevented further checking)”. This abort does not prove remaining Python targets. |
| python_pyright | unavailable / response_too_large | adapter_stdout_limit_exceeded; runtime observed 8,912,896 stdout bytes, truncated=true. A partial response is not an accepted native result or usable complete diagnostics. |
| markdown_links | passed | Lychee configured offline review: 443 total links, 231 unique, 415 successful, 28 exclusions, 0 errors/timeouts/unknown. Exclusions include remote schema/issue links and internal cache URIs; remote availability is not certified. |

Configured effective args: format/lint/Mypy []; Pyright ["--level","warning","--warnings"]; Markdown ["--offline","--cache=false","--include-fragments"]. The branch checks were performed before creating this Validation report, so a separate narrow report link check is recorded below; no Python content changed afterward.

### Complete cache integrity and bounded report evidence

The complete Python DTO was assembled and independently verified before JSON interpretation: 12,196,717 Unicode codepoints; UTF-8 SHA256 45aaec115787d34cf6234bc7095d45707ee0b1a4c04324e3a92bac0ab65a7b77. The complete Markdown DTO was likewise verified: 8,386 codepoints; SHA256 fdf222e2327d66fa809198d494180e934cf0f25705b287950a34d626d6b2b6bf. The original request and exact operation statuses, diagnostic messages, native versions, arguments, response-limit facts and supporting observations are retained here. Transient cache links are the full DTO sources while available; this report does not copy the multi-megabyte irrelevant diagnostics or pretend that its excerpts are the full raw logs.

The first sequential reader used 5,000-codepoint pages without an initial size guard. It was abandoned and the same unchanged cached result was fully read in bounded 12,000-codepoint windows with limited concurrent reads and contiguous length/hash verification. A complete 12,196,717-codepoint result requires 1,017 maximum-size windows. The initial abandoned attempt added unnecessary calls. The human correctly challenged that volume. No additional bulk read, native rerun, permanent reader or resource policy change was introduced. Subsequent reporting reuses the verified DTO in session memory.

## Additional current-tool findings from Validation

### V-F8 — branch Python profile sends mixed source kinds to native Python tools

Reproduction: on this branch against parent main, invoke run_checks({"scope":"branch"}) with the configured python_review profile. Its selected changed paths include Markdown, JSON and Jinja sources alongside Python. Native Ruff/Mypy process explicit non-Python paths and generate irrelevant diagnostics; Pyright exceeds the adapter response limit. The exact causal examples are in the native table above. Host-native read-only inspection of ScopeResolver.resolve confirms branch targets are the existing changed paths, without language filtering at that generic scope seam.

Impact: the required broad Python review cannot supply reliable complete Python evidence on this mixed branch, while the configured selected Python production/test checks and pristine generated examples had passed in Implementation and independent QA. Those narrow results remain scoped evidence and do not replace the failed broad obligation. This is a present mixed-input usability/correctness finding; it does not establish when the behavior originated or whether every adapter/profile should use the same admission strategy.

Disposition: independent Validation review should assess ownership and the required route to complete V_BRANCH_CHECKS. No file-selection/filtering strategy, configuration, adapter or approved plan was silently changed here. Do not enable experimental Markdown formatting as a workaround for a Python review.

### V-F9 — configured test deadline leaves no returned full-suite evidence

Reproduction: invoke run_tests({"scope":"configured"}) with the current tests.yaml timeout300 and native Pytest defaults. This actual attempt returned “timed out awaiting tools/call after 300s” without a result URI. The native default arguments were not reduced; tests, selections and xdist policy were not modified.

Impact: the caller has no complete run status, counts or native diagnostics to assess the full configured suite. The observed healthy server afterward rules out inferring a dead server from this timeout alone. Transport/native deadline overlap, actual suite duration and concurrent workload remain possible factors; the single observed call does not prove their individual causal contribution.

Disposition: a supported completion/recovery route or explicitly agreed rerun configuration is needed before V_FULL_TESTS can be fulfilled. This report retains the original failed evidence; it does not increase a timeout or rerun blindly.

### V-F10 — large result paging made evidence retrieval disproportionate

The cache contains the multi-megabyte Python diagnostics and the response-limit capture described above. The documented bounded read maximum is 12,000 codepoints, so complete retrieval needs over one thousand calls. Starting at 5,000 codepoints without checking total_chars first was a producer efficiency error and increased the cost further. A useful tool follow-up would assess selective diagnostic presentation or supported complete-result export while preserving honest statuses and accessible original evidence. No new export endpoint, cache layer or truncation policy was implemented here.

## Validation disposition and pre-commit reality check

Historical disposition before the larger-window rerun: V_CORRECTED_BEHAVIOR was supported, V_FULL_TESTS was missing and V_BRANCH_CHECKS contained incomplete/failed Python rows. The current disposition and complete negative suite result are in Latest Validation execution below.

All nineteen families and the fifteen Implementation deliverables remain mapped in implementation.md/manual-inspection.md. No new automated content or regression tests, fixes to pristine artifacts, production/template changes, relaxed native arguments or compatibility bridge were made in Validation. F6 remains a priority separately scoped bootstrap/proxy recovery follow-up; issue476 remains explicitly separate. Documentation/Ready/merge have not been entered.

## Bug / Validation Hand-over (historical attempt)

### Scope

- Executed the approved configured full-suite attempt and branch-wide Python/Markdown checks.
- Mapped unchanged corrected-behavior/preservation evidence and recorded precise broad-check/tool limitations.
- Excluded production fixes, new automated content coverage, generic476 work and later-phase progression.

### Deliverables

- [Validation report](validation.md)
- [Approved Strategy](research.md#approved-strategy), [Design](design.md), [Planning](planning.md)
- [Implementation mapping](implementation.md), [Manual inspection](manual-inspection.md), [Lossless first outputs](first-output-evidence.md)
- [Prior current-tool findings](tool-practice-findings.md); V-F8/V-F9/V-F10 are recorded above.

### Evidence

- Full configured test request: transport timeout at300s, no returned complete native result.
- Branch Python profile: format unavailable, lint failed, Mypy failed, Pyright response unavailable.
- Branch Markdown profile: 415 successful, 28 excluded, 0 errors.
- Reused unchanged nineteen-family manual/preservation evidence and independent Implementation review; no broad-pass inference.

### Open Work

- Complete V_FULL_TESTS and V_BRANCH_CHECKS through a reviewed supported route.
- Independent assessment of broad mixed-input/deadline/response-limit findings and their ownership.
- Separate F6 recovery triage and generic476 work.
- Documentation/Ready/merge await the applicable independent phase verdicts.

### Review Request

- Review requested. Producer FAIL records missing/failed required evidence; the independent QA authority determines the workflow verdict.


## Report verification

The newly scaffolded report and the outcome appendix passed their selected enforce content preflights. A separate configured offline markdown_link_review on docs/development/issue473/validation.md passed (receipt pgmcp://cache/runs/a05872435c48431a9ce5a43cf0ecb0c5). This verifies the report's links only; it does not change the failed/missing broad Validation obligations. The final verification note introduces no new linked target.

## Owner refinement — full-run budgets and main rollout, 2026-10-04

The human approved a larger Codex client window and full-run execution budget after reviewing the historical [issue460 decision](../issue460/validation.md#owner-decision--client-timeout-2026-09-26). That original decision raised the client setting from 120 to 300 seconds and allowed partitions. It was recovered from the original human message and the MCP safe_edit_file write of 2026-09-26. The current checkout still had 300 seconds; no local reset was observed. Because the client configuration is Git-ignored, its value is not distributed by branch integration.

The current approval supersedes the earlier partition policy for issue473: execute the single full native-configured suite with enough time for its workload. The previous version of this report applied the historical policy too broadly; its 300-second/partition instructions are replaced here. Prior failed/incomplete execution evidence remains unchanged.

### Applied route

- Set the local .codex/config.toml client window to tool_timeout_sec=1800 through safe_edit_file. The on-disk setting is not proof of activation in the current Codex connection.
- Persist the value, rationale, host rollout and activation requirement in docs/setup/README.md; keep machine paths/secrets outside Git.
- Replace the partition instructions in all five AGENTS sources with concise scope/budget guidance; retain the cache/hash rules.
- Update Planning V_FULL_TESTS and its tool-managed deliverable to the single configured full-suite route.
- After client activation, use run_tests(scope="configured", timeout_seconds=1200), preserving native execution arguments. Normal focused calls keep their configured defaults.
- Budget for the complete MCP call, bounded stopping and result delivery; consider all selected bindings. A timeout or missing result remains incomplete evidence.
- No source, adapter-contract, native selection or additional automated content/regression test changes are included in this refinement.

### Python gate diagnostic clarification

The already executed all24 changed-Python diagnostic passed format, lint and Pyright; its complete DTO is approximately13KB (receipt pgmcp://cache/runs/0205064b31494471917a8338922e0a60). Mypy found44 errors in11 test files. Strict test Mypy is diagnostic under the [current quality policy](../../coding_standards/QUALITY_GATES.md), not a newly mandatory gate. A separate Mypy selection on the3 changed production files passed (receipt pgmcp://cache/runs/684f2302ac784d37983cd7ae22b4c828). Those facts do not silently replace the prescribed branch-check route; its formal disposition remains open.

### Plan to integrate on main

1. Review the tracked policy/setup changes and issue473 Planning refinement independently; retain prior incomplete run evidence.
2. After client activation, complete the configured full-suite and remaining Validation obligations, then follow Documentation/Ready and normal reviewed issue473 integration into main.
3. Keep the shared configured-full-suite workflow requirement. No global contract change to permit mandatory partitioning is needed.
4. Carry all five AGENTS sources and the setup policy together through release asset assembly, following the [release assets procedure](../../reference/release-assets-procedure.md).
5. On each host using main, apply the tracked setup policy to its ignored local Codex connection: tool_timeout_sec=1800, preserved command/cwd/environment and confirmed client activation.
6. Confirm a complete result is delivered for the configured full run. Preserve failures/timeouts honestly; an on-disk setting, merge or PGMCP-only restart does not certify client activation or test completion.

Native target filtering and an explicit-selection escape route remain under owner discussion. The existing adapter request is unchanged; no configured selection is treated as an unconditional allowlist in this issue.

No main checkout/merge, global workflow-contract edit, generated asset rebuild or new content/regression tests were performed here. F6 recovery and generic issue476 remain separately scoped. The Validation status remains FAIL until the required evidence is complete.


### Verification of the timeout policy refinement

All eight tracked text edits passed their safe_edit_file enforce content preflights; the ignored local client setting was written with report validation. An offline markdown_link_review over all eight edited files reported 41 missing-path diagnostics, all in the four non-root AGENTS source/mirror files (receipt pgmcp://cache/runs/9de6564e3f854e9ba1c5c6710ee67cbc). Every reported relative link target was already present in the pre-edit source snapshot; none belongs to the changed budget/cache clauses. The source files retain workspace-root link conventions that do not resolve from their source/mirror directories. This result is retained as a documentation limitation, not represented as a passing eight-file link gate. It does not prove completion of the full native suite or activation of the new client window.

The separate offline link check of the root AGENTS file and the changed setup, Planning and Validation documents passed (receipt pgmcp://cache/runs/0e390d96dbeb4ddaafd234dcd05bcf43). This narrower passing result does not replace the recorded eight-file failure or the pending full Validation obligations.

## Owner continuation and deferred branch-check solution — 2026-10-04

The owner added explicit deferral as the fourth completion obligation and instructed that it be performed first. The complete research, discussed selection-intent direction, nine-package applicability, native evidence, generic target-collapse finding, unresolved resolver/wire migration decisions and separate-issue disposition are recorded in [the deferred hand-off](tool-practice-findings.md#deferred-branch-wide-check-solution--owner-disposition-2026-10-04). No production, adapter, test or native configuration change is part of this continuation.

Execution order: commit the deferral; perform the approved single configured full-suite run; complete current-tool branch-gate evidence without hiding limitations; commit the updated Validation report and request the external Beoordeel designplan review. Existing scoped Python successes remain evidence, not an undeclared replacement for the prescribed broad gate. Later Documentation/Ready carries the deferred work to coordination.

## Validation execution before cycle 5 — 2026-10-04

Historical pre-repair evidence. The latest outcome follows in Latest Validation after cycle 5.

This section supersedes earlier current-outcome statements; the earlier attempts remain historical evidence. The deferred branch-check solution was recorded and pushed first in commit a1581d64. No production, adapter, template, test or native configuration was changed during this continuation.

### Single configured full-suite outcome

Exact call:

```json
{"scope":"configured","timeout_seconds":1200}
```

No args override, target restriction or partition was used. Pytest 9.0.2 used pyproject.toml, testpaths=tests/mcp_server and eight xdist workers, collecting 2777 items. The complete native response reports **6 failed, 2769 passed, 1 skipped, 1 xpassed, 229 warnings in 320.27 seconds** (exit 1). PGMCP operation success=true with a failed python_tests row, args_source=configured, effective_args=[], no request rejection or termination problem. Receipt: pgmcp://cache/runs/03731e6f09214698be363140f3ae16b5.

The accepted stdout capture records 803612 observed bytes, truncated=false; native evidence is retained in the cached result. Delivery after a 320.27-second native run demonstrates that this active call survived the former 300-second client boundary. It does not independently measure the exact client's 1800-second limit. The 804155-character cache was size-checked and only bounded diagnostic windows were read; no complete verbose-log download or routine hash calculation was performed.

### Six reproducible existing-consumer failures

All six failures are parameter variants of [test_selected_graph_renders_retained_root_and_round_trips](../../../tests/mcp_server/unit/services/test_artifact_header_reader.py): maximum=False/True crossed with Python, TypeScript and HTML comment framing. A focused existing-test reproduction used:

```json
{
  "scope":"targets",
  "targets":["tests/mcp_server/unit/services/test_artifact_header_reader.py"],
  "args":{"python_tests":["-q","-n","0","--tb=short","-k","selected_graph_renders_retained_root_and_round_trips"]},
  "timeout_seconds":120
}
```

Observed: **6 failed, 62 deselected, 1 warning in 0.60 seconds**, receipt pgmcp://cache/runs/08652be30dc6484992f69012b557b0de. Every variant raises jinja2.exceptions.TemplateAssertionError: No filter named 'text_block'. The test renders the delivered [tier0 root](../../../.pgmcp/template_suite/shared/templates/bases/tier0_root.jinja2) using its own fresh Environment without [register_template_filters](../../../mcp_server/services/template_engine.py). The shared root now requires that registration. This is a missed existing test consumer of the issue473 rendering contract, not a branch-filtering defect to defer.

Source inspection also shows that this test's exact expected string uses one LF between provenance and body, whereas the delivered root now generates a blank separator. That is a further expectation-alignment question for review; it is not a newly executed post-fix assertion failure. No test patch, fake local filter or production change was made in Validation.

### Fresh branch-gate outcomes

| Exact call | Current result | Evidence |
| --- | --- | --- |
| run_checks(scope="branch", profile="python_review", timeout_seconds=300) | incomplete: python_format unavailable, python_lint failed, python_types failed, python_pyright unavailable; configured native arguments retained | pgmcp://cache/runs/960376869dbb47dea4a9cead1148ce27 |
| run_checks(scope="branch", profile="markdown_link_review", timeout_seconds=300) | failed: 489 successful, 46 excluded, 41 errors, 0 timeouts; native Lychee exit 1 | pgmcp://cache/runs/9bda2cb245ca417480053b5aa23e6b60 |

The Python broad call again delivers mixed branch paths to native Python tools. Its first diagnostic is Ruff's experimental Markdown-formatting refusal; the large Pyright capture also contains Python syntax diagnostics against first-output-evidence.md. The result is 12242619 characters; only bounded diagnostic windows were read. These fresh row statuses and representative diagnostics reproduce the already documented tool limitation; they do not turn the original failure into a pass.

All 41 current link errors are in four non-root AGENTS copies: docs/agents/codex/AGENTS.md (11), docs/agents/vscode/copilot/AGENTS.md (8), docs/agents/antigravity/AGENTS.md (11) and .agents/AGENTS.md (11). Their workspace-root destinations are interpreted relative to the source/mirror directory. The same unchanged link-target limitation was recorded in the prior eight-file policy check. Native extension applicability and source/mirror link conventions require separate assessment; no skip/exclusion was added to force a passing branch run.

Fresh passing Python evidence is reused because production and test files are unchanged: format/lint/Pyright on all 24 changed Python files and strict Mypy on the three changed production files. The independent checks are indexed in the owner-refinement section. Test-only Mypy diagnostics are not reclassified as mandatory gate failures. These scoped results remain supporting evidence until the required branch-gate route has an explicit reviewed disposition.

### Current disposition and review request

V_FULL_TESTS now has a complete negative result rather than missing output. V_BRANCH_CHECKS has explicit current failed/incomplete broad rows and passing scoped Python evidence. V_CORRECTED_BEHAVIOR retains the unchanged 19-family manual, 38-output, boundary and independent Implementation evidence. Producer Validation status remains **FAIL**: the six missed-consumer failures are unresolved, and no successful required branch-gate disposition is claimed.

Pre-commit reality check: the full configured suite was not weakened, partitioned or rerun to hide failures; the narrow repetition diagnoses an existing failure rather than adding coverage. No production, template, test or adapter repair was performed. The deferred branch-check proposal stays outside issue473 implementation. Required failures are presented for independent review, not silently deferred as unrelated.

### Bug / Validation Hand-over (current)

#### Scope

- Full native-configured suite with the owner-approved budget, fresh branch Python/Markdown gates, narrow reproduction of the six real failures and unchanged corrected-output evidence.
- Deferred branch-check research is documented; no production implementation of that proposal.
- Documentation, Ready and merge remain pending.

#### Deliverables

- [Validation report](validation.md), [Planning](planning.md), [Design](design.md), [Approved Strategy](research.md#approved-strategy).
- [Implementation mapping](implementation.md), [Manual inspection](manual-inspection.md), [Exact first-output evidence](first-output-evidence.md).
- [Separate-issue deferred research](tool-practice-findings.md#deferred-branch-wide-check-solution--owner-disposition-2026-10-04).
- [Failing existing test consumer](../../../tests/mcp_server/unit/services/test_artifact_header_reader.py) and [shared root](../../../.pgmcp/template_suite/shared/templates/bases/tier0_root.jinja2).

#### Evidence

- Full suite: 6 failed, 2769 passed, 1 skipped, 1 xpassed, 229 warnings, 320.27 seconds.
- Focused reproduction: 6 failed, 62 deselected, 1 warning, 0.60 seconds; missing text_block registration.
- Branch Python: incomplete; format/Pyright unavailable and lint/Mypy failed.
- Branch links: 489 successful, 46 excluded, 41 errors.
- Reused passing format/lint/Pyright for 24 changed Python files, strict Mypy for three production files and independently reviewed actual scaffold evidence.

#### Open Work

- Assess and route the six existing-consumer failures within issue473; do not defer them with the branch-selection proposal.
- Determine the accepted branch-gate disposition and source/mirror link responsibility while preserving the original failed evidence.
- Carry the deferred selection solution to a separate issue through coordination.
- Independent QA determines the applicable workflow verdict; producer does not claim GO.

#### Review Request

- External Beoordeel designplan review requested. Read the current primary evidence and exact negative results; report findings and the authority-appropriate assessment.

## Latest Validation after cycle 5 — 2026-10-04

### Authority and bounded correction

The owner authorized one focused repair cycle after the independent NOGO on 9c164c4c. Repair commits 3d3162ac and b3e3719f migrate only the existing header-reader test environment and exact separator expectation, with phase documents and tool-managed deliverables/state. Production, templates, adapters and native configuration are unchanged. No new test, fake filter, skip, compatibility bridge or deferred selection implementation was added.

Independent external Beoordeel designplan QA returned **Implementation → Validation GO for cycle 5** on b3e3719f. Its configured eight-worker module run passed 68 tests with 9 warnings in 4.50 seconds (pgmcp://cache/runs/a1073300f0314217a39f3b9f198d5654); format/lint/Pyright passed (pgmcp://cache/runs/5bb4ed4d0f5348feb7fa313ad0093460). The independent vectors, three comment frames, both length cases and header-reader round-trip assertions were retained. This GO authorizes renewed Validation; it is not a Validation verdict.

### Fresh single configured suite

```json
{"scope":"configured","timeout_seconds":1200}
```

No argument override, targets, deselection or partition. Native Pytest 9.0.2 used pyproject.toml, tests/mcp_server, eight workers and **2777 items**. Result: **2775 passed, 1 skipped, 1 xpassed, 229 warnings in 326.96 seconds**, no failures, exit 0. Operation success=true; python_tests passed; args_source=configured; effective_args=[]; no request rejection or termination problem. Receipt pgmcp://cache/runs/8d4a6cb1a32e40eaac12bdf9bb1d1743.

The counts reconcile with the prior same-sized negative suite: six failures became six additional passes; one skip, one XPASS and 229 warnings remain. Skip/XPASS are native outcomes and are not counted as ordinary passed tests or silently removed. The accepted stdout capture has 795557 observed bytes and truncated=false; the cached response has 796100 characters. Only a size-aware opening window and a terminal diagnostic window were read for structured facts/counts, without downloading the verbose session or computing routine hashes. The complete returned native result remains available through the receipt; excerpts are not presented as the complete log.

### Explicit reviewed replacement gate coverage

Independent QA accepted the following **issue473-specific** disposition in its cycle5 verdict. The historical mixed branch Python failures and 41 source/mirror link failures remain failures. They are not reclassified as native passes. The reviewed replacement proves the applicable changed-file obligations without introducing the deferred adapter solution or changing shared configuration.

| Surface | Accepted coverage and current evidence |
| --- | --- |
| All 25 changed Python files | Reuse valid format/lint/Pyright results on the 24 unmodified files; combine the new header-reader checks, all passed. |
| Three changed production files | Reuse unchanged strict Mypy success for bootstrap.py, cli_renewal.py and services/template_engine.py. No test Mypy gate is invented. |
| Changed Markdown | Native offline markdown_link_review on root AGENTS.md and every other changed Markdown file except the four explicitly reviewed source/runtime copies: 24 files, passed; 504 successful links, 37 excluded by existing native configuration, 0 errors, 0 timeouts. |
| Four instruction copies | Source/deployment-context disposition accepted: their nine unique link targets equal the root link target set and all exist relative to workspace root. Preserve their source/runtime text and the recorded original 41 directory-relative failures. |

Python receipts: prior producer pgmcp://cache/runs/0205064b31494471917a8338922e0a60 and pgmcp://cache/runs/684f2302ac784d37983cd7ae22b4c828; independent 24-file review pgmcp://cache/runs/d9162d4276d940e7acde1f48bd7254bb and production Mypy pgmcp://cache/runs/d03c47fac6b14fdaa0a9a77d69debe81; new header-reader gates pgmcp://cache/runs/fc486b1fdf984812a56a937dee34f200 and independent pgmcp://cache/runs/5bb4ed4d0f5348feb7fa313ad0093460. No production/test edit after those respective checks invalidates their evidence.

The exact fresh Markdown call uses scope=targets, targets equal the 24-file inventory below, profile=markdown_link_review, timeout_seconds=120, with no args override. Receipt pgmcp://cache/runs/05686421ee68496fa1d939860f4a8fb9. Its existing native excluded links include non-file schemes/remote references; no new native ignore was added for this route.

The four reviewed exceptions are .agents/AGENTS.md, docs/agents/codex/AGENTS.md, docs/agents/antigravity/AGENTS.md and docs/agents/vscode/copilot/AGENTS.md. [Release source and dev-sync responsibility](../../reference/release-assets-procedure.md#1-specification-agent-instruction-sources-ssot) explains why blindly changing source-relative destinations would change active-host behavior. Host-native source comparison confirms VS Code source equals root AGENTS.md and Codex source equals .agents/AGENTS.md. All four contain the same nine unique targets, with no additional link targets. The exception is limited to this accepted issue-specific gate route; it does not certify arbitrary source-directory hyperlink navigation or all host deployments.

### Complete changed-file inventories against main

The MCP git_diff_stat inventory for b3e3719f against main records 101 changed files (pgmcp://cache/runs/e244406424a148c48de18737a7d67dc6). Host-native repository search resolves shortened stat names against actual files. The following 25 Python files and 28 Markdown files (24 checked, four explicitly named exceptions) account for all changed files of those types. Later Validation document/state commits do not add another source or Markdown file.

Python inventory:

- [mcp_server/bootstrap.py](../../../mcp_server/bootstrap.py)
- [mcp_server/cli_renewal.py](../../../mcp_server/cli_renewal.py)
- [mcp_server/services/template_engine.py](../../../mcp_server/services/template_engine.py)
- [tests/mcp_server/fixtures/delivered_templates.py](../../../tests/mcp_server/fixtures/delivered_templates.py)
- [tests/mcp_server/fixtures/installed_distribution.py](../../../tests/mcp_server/fixtures/installed_distribution.py)
- [tests/mcp_server/integration/templates/test_architecture.py](../../../tests/mcp_server/integration/templates/test_architecture.py)
- [tests/mcp_server/integration/templates/test_design_artifact.py](../../../tests/mcp_server/integration/templates/test_design_artifact.py)
- [tests/mcp_server/integration/templates/test_generic_document.py](../../../tests/mcp_server/integration/templates/test_generic_document.py)
- [tests/mcp_server/integration/templates/test_planning_artifact.py](../../../tests/mcp_server/integration/templates/test_planning_artifact.py)
- [tests/mcp_server/integration/templates/test_pytest_integration_test.py](../../../tests/mcp_server/integration/templates/test_pytest_integration_test.py)
- [tests/mcp_server/integration/templates/test_python_adapter.py](../../../tests/mcp_server/integration/templates/test_python_adapter.py)
- [tests/mcp_server/integration/templates/test_python_class.py](../../../tests/mcp_server/integration/templates/test_python_class.py)
- [tests/mcp_server/integration/templates/test_python_protocol.py](../../../tests/mcp_server/integration/templates/test_python_protocol.py)
- [tests/mcp_server/integration/templates/test_python_pydantic_config.py](../../../tests/mcp_server/integration/templates/test_python_pydantic_config.py)
- [tests/mcp_server/integration/templates/test_python_pydantic_dto.py](../../../tests/mcp_server/integration/templates/test_python_pydantic_dto.py)
- [tests/mcp_server/integration/templates/test_python_worker.py](../../../tests/mcp_server/integration/templates/test_python_worker.py)
- [tests/mcp_server/integration/templates/test_reference.py](../../../tests/mcp_server/integration/templates/test_reference.py)
- [tests/mcp_server/integration/templates/test_research_artifact.py](../../../tests/mcp_server/integration/templates/test_research_artifact.py)
- [tests/mcp_server/integration/templates/test_shared_documents.py](../../../tests/mcp_server/integration/templates/test_shared_documents.py)
- [tests/mcp_server/integration/templates/test_shared_python.py](../../../tests/mcp_server/integration/templates/test_shared_python.py)
- [tests/mcp_server/integration/templates/test_typescript_artifact.py](../../../tests/mcp_server/integration/templates/test_typescript_artifact.py)
- [tests/mcp_server/integration/templates/test_validation_artifact.py](../../../tests/mcp_server/integration/templates/test_validation_artifact.py)
- [tests/mcp_server/test_support.py](../../../tests/mcp_server/test_support.py)
- [tests/mcp_server/unit/config/test_contracts_loader.py](../../../tests/mcp_server/unit/config/test_contracts_loader.py)
- [tests/mcp_server/unit/services/test_artifact_header_reader.py](../../../tests/mcp_server/unit/services/test_artifact_header_reader.py)

Checked Markdown inventory:

- [.agents/workflows/create-issue.md](../../../.agents/workflows/create-issue.md)
- [.github/prompts/create-issue.prompt.md](../../../.github/prompts/create-issue.prompt.md)
- [AGENTS.md](../../../AGENTS.md)
- [docs/coding_standards/ARCHITECTURE_PRINCIPLES.md](../../../docs/coding_standards/ARCHITECTURE_PRINCIPLES.md)
- [docs/coding_standards/CODE_STYLE.md](../../../docs/coding_standards/CODE_STYLE.md)
- [docs/coding_standards/DOCUMENTATION_STANDARD.md](../../../docs/coding_standards/DOCUMENTATION_STANDARD.md)
- [docs/development/issue473/design-document-comparison.md](../../../docs/development/issue473/design-document-comparison.md)
- [docs/development/issue473/design.md](../../../docs/development/issue473/design.md)
- [docs/development/issue473/document-family-comparison.md](../../../docs/development/issue473/document-family-comparison.md)
- [docs/development/issue473/first-output-evidence.md](../../../docs/development/issue473/first-output-evidence.md)
- [docs/development/issue473/first-output-survey.md](../../../docs/development/issue473/first-output-survey.md)
- [docs/development/issue473/implementation.md](../../../docs/development/issue473/implementation.md)
- [docs/development/issue473/manual-inspection.md](../../../docs/development/issue473/manual-inspection.md)
- [docs/development/issue473/native-tooling-follow-up.md](../../../docs/development/issue473/native-tooling-follow-up.md)
- [docs/development/issue473/planning.md](../../../docs/development/issue473/planning.md)
- [docs/development/issue473/python-class-comparison.md](../../../docs/development/issue473/python-class-comparison.md)
- [docs/development/issue473/python-family-comparison.md](../../../docs/development/issue473/python-family-comparison.md)
- [docs/development/issue473/research.md](../../../docs/development/issue473/research.md)
- [docs/development/issue473/tool-practice-findings.md](../../../docs/development/issue473/tool-practice-findings.md)
- [docs/development/issue473/tracking-typescript-comparison.md](../../../docs/development/issue473/tracking-typescript-comparison.md)
- [docs/development/issue473/validation.md](../../../docs/development/issue473/validation.md)
- [docs/development/issue473/whitespace-comparison.md](../../../docs/development/issue473/whitespace-comparison.md)
- [docs/reference/tools/scaffolding.md](../../../docs/reference/tools/scaffolding.md)
- [docs/setup/README.md](../../../docs/setup/README.md)

### Current deliverable outcome

| Obligation | Current producer outcome |
| --- | --- |
| V_FULL_TESTS | Complete fresh configured suite passed after the six consumer failures were corrected. |
| V_BRANCH_CHECKS | Accepted replacement Python coverage and 24-file Markdown route passed; retain original negative broad calls and the four explicit deployment-context exceptions. |
| V_CORRECTED_BEHAVIOR | Unchanged nineteen-family actual/manual preservation evidence plus independently reviewed existing-consumer migration; no new content harness. |

Producer Validation assessment is **PASS under the explicit independently reviewed gate disposition**, with a new independent Validation review requested. The first incomplete test attempt, subsequent negative full suite, negative broad Python runs and 41 link failures remain historical evidence. A producer PASS is not independent Validation GO and does not authorize Documentation/Ready/merge by itself.

### Bug / Validation Hand-over (after cycle 5)

#### Scope

- Complete the missed consumer in one authorized cycle and validate it with the full native suite and accepted changed-file gate coverage.
- Preserve all historical failures and the separate deferred branch-check research.
- Exclude production/template/adapter changes, new coverage, Documentation/Ready progression and merge.

#### Deliverables

- [Validation](validation.md), [Planning cycle5](planning.md#owner-authorized-repair-cycle-c_header_consumer--2026-10-04), [Repair Implementation](implementation.md#c_header_consumer--owner-authorized-cycle-5-repair-2026-10-04).
- [Changed header-reader consumer](../../../tests/mcp_server/unit/services/test_artifact_header_reader.py).
- [Manual evidence](manual-inspection.md), [Actual first outputs](first-output-evidence.md), [Approved Strategy](research.md#approved-strategy), [Design](design.md).
- [Deferred branch-check hand-off](tool-practice-findings.md#deferred-branch-wide-check-solution--owner-disposition-2026-10-04).

#### Evidence

- Fresh single configured suite: 2775 passed, 1 skipped, 1 xpassed, 229 warnings, 326.96 seconds, native exit0.
- Existing module producer: 68 passed, 1 warning; independent configured module: 68 passed, 9 warnings.
- Combined accepted 25-file format/lint/Pyright and three-production-file Mypy coverage passed.
- Accepted 24-file Markdown route passed: 504 successful links, 37 excluded, 0 errors.
- Independent cycle5 GO permits Validation; a fresh Validation verdict is pending.

#### Open Work

- Independent targeted Validation re-review of the repair closure, fresh suite and explicit replacement gate disposition.
- Carry separately deferred adapter selection and existing F1–F7/issue476 items through Documentation/Ready to coordination.
- Remaining skip, XPASS and warnings are disclosed native caveats, not hidden failures.
- Documentation/Ready/merge follow their own required review boundaries.

#### Review Request

- Targeted external Validation review requested. Reuse unchanged evidence; review only invalidated surfaces and this phase's new results.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-03 | @imp validator | Record configured full-suite attempt, branch-wide checks, corrected-behavior mapping and unresolved Validation evidence. |
| 0.2 | 2026-10-04 | @imp validator | Restore owner-approved issue460 partitioning, persist concise cache/deadline instructions and main rollout, and retain diagnostic/gate distinctions. |
| 0.3 | 2026-10-04 | @imp validator | Recover the original timeout decision and supersede partitioning with the approved larger client window, full-run budget and durable main/host rollout. |
| 0.4 | 2026-10-04 | @imp validator | Record the owner's separate-issue deferral and execution order before completing current-tool Validation and requesting external review. |

| 0.5 | 2026-10-04 | @imp validator | Record the complete 2777-item native suite, six reproducible missed-consumer failures, current branch Python/link outcomes and outcome-neutral external review hand-over. |
| 0.6 | 2026-10-04 | @imp validator | Close the six consumer failures with a fresh passing configured suite, explicit independent gate-route acceptance, complete changed-file inventories and targeted Validation hand-over. |

