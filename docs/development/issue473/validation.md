<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=CT9NV5LmQjKHFGqX sf=FAN5Vr-4vcbMMjZ2 -->

# Issue 473 — Validation

**Status:** Validation blocked; independent review requested  
**Version:** 0.3  
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

FAIL

## Scope

bug/473-first-call-template-quality against parent main; production/template/test content reviewed at 1a0360ac plus evidence-only 9d27e4d2. No production, template or test changes during this Validation attempt.

## Obligations

### V\_FULL\_TESTS — complete native-configured test result

**Evidence:**

- [Planning](<planning.md>)

**Outcome:** Not fulfilled: the configured run_tests call timed out at the MCP transport boundary after 300 seconds; no native result DTO or complete test totals were returned.

### V\_BRANCH\_CHECKS — configured Python review and branch Markdown links

**Evidence:**

- [Python review receipt](<pgmcp://cache/runs/bce86b0768b64271b8fdf2f1632a1d3d>)
- [Markdown review receipt](<pgmcp://cache/runs/944deb18930d44a49d17924aa388146d>)

**Outcome:** Python review incomplete: format and Pyright unavailable, lint and Mypy failed. Markdown links passed. Full native row interpretation follows in the verified receipt appendix.

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

V_CORRECTED_BEHAVIOR is supported by the unchanged actual first-output and preservation evidence reviewed independently at Implementation. V_FULL_TESTS is unfulfilled, and V_BRANCH_CHECKS contains incomplete/failed Python rows. Producer Validation status is therefore FAIL. Broad failure evidence has not demonstrated a new template defect; it has also not established the required absence of regression. Neither scoped success nor a passed Markdown gate closes those missing obligations.

All nineteen families and the fifteen Implementation deliverables remain mapped in implementation.md/manual-inspection.md. No new automated content or regression tests, fixes to pristine artifacts, production/template changes, relaxed native arguments or compatibility bridge were made in Validation. F6 remains a priority separately scoped bootstrap/proxy recovery follow-up; issue476 remains explicitly separate. Documentation/Ready/merge have not been entered.

## Bug / Validation Hand-over

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

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-03 | @imp validator | Record configured full-suite attempt, branch-wide checks, corrected-behavior mapping and unresolved Validation evidence. |
| 0.2 | 2026-10-04 | @imp validator | Restore owner-approved issue460 partitioning, persist concise cache/deadline instructions and main rollout, and retain diagnostic/gate distinctions. |
| 0.3 | 2026-10-04 | @imp validator | Recover the original timeout decision and supersede partitioning with the approved larger client window, full-run budget and durable main/host rollout. |

