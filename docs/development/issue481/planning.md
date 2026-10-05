<!-- pgmcp:v1 id=planning pv=1.0.0 pf=CscfYyDLqj0OeHml sf=5--KpGf2wHUv2qAj -->

# Startup admission diagnostics and recovery — Planning (#481)

**Status:** PLANNING DRAFT — review requested  
**Version:** 0.3  
**Last Updated:** 2026-10-05

## Purpose

### Files and seams

| Work | Primary files/seams |
| --- | --- |
| Diagnostic/recovery contract | mcp_server/cli.py; mcp_server/schemas/tool_outputs.py and the new pure startup-diagnostic schema; mcp_server/tools/health_tools.py; mcp_server/server.py; mcp_server/bootstrap.py health composition; mcp_server/presenters/ recovery presentation. |
| Transport lifecycle | mcp_server/core/proxy.py; existing IPresenter/presentation leaf for actionable output. Preserve restart_server input/output and marker semantics. |
| Current callers | Repository search; known existing callers include tests/mcp_server/unit/test_cli.py, unit/test_server.py and unit/tools/test_health_tools.py. Modify only affected constructor/schema expectations, with no new scenarios or test runs. Do not rewrite unrelated proxy tests. |
| Operational documentation | docs/reference/tools/discovery.md and docs/reference/proxy_restart.md. Read historical issue473 F6 evidence as context; leave it unchanged. |

Within C481.1, establish the diagnostic/output contract first, wire the existing recovery composition and current callers, then complete proxy forwarding/lifecycle ownership. These are local dependencies inside one cycle, not separate phases or reviews. Capture public schema/serialization at the actual MCP boundary, including invalid restart input/error DTO presentation, rather than relying on a model-only assertion.

### Single Validation demonstration

Use a disposable workspace and child processes running the changed branch through the real CLI/proxy entrypoints. Keep the live workspace configuration untouched. Temporary drivers, controlled child behavior and captures are disposable; retain only concise outcomes/evidence in the required validation record. Do not commit a test/probe framework.

| Scenario | Required observable result |
| --- | --- |
| Valid baseline | Direct CLI and proxy complete initialize; alive PID and healthy health result. Capture actual startup time. |
| Rejected F6 template input | Direct CLI and proxy expose only health_check/restart_server; original ERR_CONFIG/message/template/field/line and available cause survive in the public response. Strict admission rejects ordinary work. |
| Repeated rejection | Through proxy, restart without source correction returns an accurate request receipt and a freshly initialized unhealthy recovery child. Direct CLI relaunch produces the same accessible diagnosis. |
| External source correction | Correct only the disposable source; explicit restart through proxy and external CLI relaunch produce fresh valid admission and healthy status. Refresh tools/list; ordinary tools are available only afterwards. |
| Recovery input/presentation failure | Invalid restart input produces the existing validation/error DTO and a readable MCP error result without loading rejected configuration. |
| Early exit / initialize error / malformed or wrong-ID response | Stderr, including buffered final output, remains visible; no false ready/restart_completed; affected requests complete once with correlated failure. Retain the actual response/exit/error evidence. |
| Nonresponsive initialize | The real proposed 30-second deadline expires; capture elapsed time and unavailable outcome. A normally completing initialize proceeds immediately, without waiting out the deadline. |
| Request/exit/restart overlap | Capture request IDs and generation/PID across a controlled pending request and restart/exit. No swallowed/duplicate completion, ordinary replay or retired-generation response; undeliverable notifications receive no response. |

Initial recovery/server health and transport readiness are separate outcomes. An initialized unhealthy replacement is reachable recovery, not successful admission. Fatal launch/transport failures require external correction/relaunch; clients with stale tool discovery may need reconnect. Stop if the measured valid startup exceeds the proposed initialization budget; report the measurement rather than silently changing the design.

### Exact gate ownership

| Phase | Evidence and timing |
| --- | --- |
| Planning | Scaffold preflight plus run_checks(scope='targets', targets=['docs/development/issue481/planning.md'], profile='markdown_link_review', timeout_seconds=300). Verify document/payload cycle IDs, descriptions and ordering via get_project_plan. |
| Implementation | Select existing changed files from the current Git diff/status at the check moment. Production .py targets: run_checks(scope='targets', targets=<production Python selection>, profile='python_review', timeout_seconds=600). Mechanically changed test .py targets: retain the passing syntax preflight from safe_edit_file/scaffold_artifact, then run_checks(scope='targets', targets=<mechanical test Python selection>, checks=['python_format','python_lint'], timeout_seconds=600). python_syntax is an edit-content preflight, not a supported run_checks selection. No test Mypy gate or test execution. Record actual targets and receipts; no runtime acceptance claim yet. |
| Validation | Refresh the Git selection; rerun appropriate scope='targets' checks only for changed/invalidated production or mechanical-test Python evidence. At the end of Validation, run once: run_checks(scope='configured', checks=['python_format','python_lint','python_pyright'], timeout_seconds=600) and the separate run_checks(scope='configured', checks=['python_types'], timeout_seconds=600). These workspace-wide runs use native configured selection; Mypy retains its configured production scope. Add the single process demonstration above. No regression suite. |
| Documentation | Native edit validation and run_checks(scope='targets', targets=<current Git-selected changed Markdown files needing fresh evidence>, profile='markdown_link_review', timeout_seconds=300). Include the two changed reference files; reuse valid prior document evidence. |
| Ready | Inspect final status/diff and reuse fresh evidence; create no extra tests or checks merely to repeat a completed phase. |

Use git_diff_stat(target_branch=<recorded parent>, source_branch='HEAD') and git_status at each applicable check moment to select committed and working-tree changes. Deduplicate existing paths; separate production .py, mechanically changed test .py and Markdown into the targets suitable for each check. Do not send deleted paths, Markdown or workflow JSON to Python checks. Record the selected paths and any exclusions; skip empty target groups. Never use scope='branch' as an implicit file-type filter. The final scope='configured' runs supply no targets and preserve native configured arguments/selection.

Use required MCP tools for scaffolding/edits, phase/cycle state, commits and checks. No workflow/configuration change is planned to encode an issue-local testing exception. Deliverable validators are intentionally null: file presence or keyword assertions would not prove these behavioral contracts; review the recorded native and process evidence instead.

## Scope In

One coherent production correction and current-caller migration; one isolated Validation demonstration; current reference parity and focused native static/document checks.

## Scope Out

Legacy/compatibility bridges, in-session repair, proxy-owned recovery endpoint, admission relaxation, unrelated transport/exception cleanup, regression-test additions/runs, persistent demonstration harnesses and artificial RED/GREEN steps.

## Summary

Execute the owner-approved lightest complete A in one implementation cycle. Research 0.2 and Design 0.1 received independent @qa Design → Planning GO in chat 'Beoordeel designplan' on commit 6c97e366 (review turn 01a10b8f-60f0-7341-b013-2ec9cf5ac089); the owner then instructed 'go voor planning'. Planning operationalizes those contracts without redesign.

## Dependencies

- Binding inputs: [Research](research.md), [Design](design.md) and the independent Design GO. No blocking Design findings remain.
- Owner-approved verification overrides default RED/regression/full-suite workflow instructions for #481: no run_tests, pytest, unittest or regression runs in any phase. Static gates and the isolated practical demonstration remain required.
- Only @imp owns technical mutations; independent @qa owns phase GO/NOGO. Planning itself grants no implementation or merge approval.

## Risks

### FrozenJsonObject can appear incorrectly in public schema/serialization despite internal immutability.

Capture the actual advertised outputSchema and recovery response; require a normal JSON object preserving original nested values.

### Response/exit/restart races can duplicate answers or attach old stderr/state to a new child.

Keep generation and request ownership explicit in C481.1 and inspect correlated captures in the one Validation demonstration.

### Clients may retain stale tool discovery; an unexpectedly slow valid bootstrap may exceed the chosen deadline.

Document tools/list refresh/reconnect and measure valid startup plus the real timeout. Reopen only a demonstrated budget conflict.

## Milestones

- C481.1: implement and statically verify the complete recovery correction; one implementation review/commit boundary.
- Validation: perform the one isolated process demonstration and final configured workspace checks; refresh Git-selected per-type targets only when prior evidence is invalidated, then record actual acceptance evidence once.
- Documentation: reconcile the two current operational references and their links.
- Ready: assemble the verified PR and coordination hand-over using fresh evidence; no repeated verification or duplicate approval ceremony.

## Work Units

### C481.1 — Complete minimal startup recovery

**Goal:** Deliver the approved CLI/degraded/proxy correction as one coherent change; keep functional process verification in Validation.

**Cycle Number:** 1

#### Scope In

CLI bootstrap classification/capture; StartupDiagnostic and health output; configuration-independent recovery presentation; degraded health/restart composition; proxy lifecycle and request ownership; current callers affected by the clean break.

#### Scope Out

Admission redesign, proxy-owned recovery tools, file repair service, compatibility aliases, regression-test scenarios/runs, persistent probe harnesses and reference-document work owned by Documentation.

#### Deliverables

##### D481.1.1

CLI captures recognized bootstrap failures losslessly; immutable diagnostic/health output, injected Settings and the independent recovery presenter expose complete diagnostics with the two existing recovery tools.

**Validates:** null

##### D481.1.2

Proxy drains generation-bound streams, completes a validated live initialize exchange within the deadline, logs truthful lifecycle outcomes and correlates unavailable responses exactly once without request replay.

**Validates:** null

##### D481.1.3

All current health/degraded composition callers use the clean-break contracts; removed fields/parameters have no compatibility path; focused native static checks pass on current Git-selected production Python targets and applicable mechanical test-callers targets, with exact selections recorded.

**Validates:** null

#### Exit Criteria

D481.1.1–D481.1.3 implemented together; all current callers migrated, relevant source review completed and focused python_review passed on current Git-selected production .py targets, with passing edit-content syntax preflight and targeted run_checks format/lint evidence for mechanically changed test .py targets. Record exact per-check target lists and receipts in the implementation hand-over. Behavioral acceptance and final configured workspace checks remain pending Validation; no pytest/unittest/regression run or artificial RED commit.

#### Dependencies

- Research 0.2 and Design 0.1; independent QA GO at 6c97e366; owner instruction to proceed to Planning.

#### Obligations

- Follow the Approved Strategy without changing ERR_CONFIG, relaxing admission or bypassing upgrade-lock/renewal records.
- Compose recovery without rejected template/presentation/workflow configuration. Preserve original diagnostic fields and cause; deeply immutable internal params serialize as an ordinary JSON object.
- Keep exactly health_check and restart_server in recovery. Render normal recovery DTOs and the existing decorator validation/error DTOs through the presentation boundary.
- Maintain one response per client request across response/exit/restart races; generation-bound readers and late-response rejection; no ordinary-request replay.
- Apply removed health fields/constructor parameters to all current callers together. Existing test edits are mechanical contract maintenance only; do not add scenarios or execute tests.

#### Verification

##### Recovery and public diagnostic contract

**Method:** Review final CLI/composition/DTO/presenter code and generated public output-schema/serialization in the later process capture.

**Expected Result:** Preserved original keys/nested data/cause; unhealthy health query succeeds; recovery remains independent of failed configuration.

##### Current caller parity and production quality

**Method:** Repository search for removed health contracts; select existing changed paths using current Git diff/status. Run python_review with scope='targets' on production .py only; retain passing edit-content syntax preflight and run_checks(scope='targets', targets=<mechanical test Python selection>, checks=['python_format','python_lint'], timeout_seconds=600) on mechanically changed test .py only. Do not send python_syntax to run_checks; it accepts content only through native edit/scaffold preflight. Preserve native arguments, use timeout_seconds=600 and record the actual selected paths.

**Expected Result:** No live legacy caller; production format/lint/types/pyright pass with native configured arguments; mechanical test callers have applicable syntax/format/lint evidence. Strict test Mypy is not made mandatory. No test execution or invented regression evidence.

##### Proxy generation/request ownership

**Method:** Source review against Design's Proxy contracts; use the single later process demonstration to inspect IDs, generations, stderr and lifecycle events.

**Expected Result:** Single stdout consumer, immediate stderr drain, exactly-once completion, correct restart receipt semantics and no false ready/completed events.

#### Stop Conditions

- Stop and reopen the approved boundary decision if complete diagnostics or recovery composition requires relaxing admission, loading rejected configuration or adding an editor/proxy recovery endpoint.
- Stop for a concrete unresolved architecture/check failure; do not add ignores, compatibility shims or synthetic passing evidence.
- A runtime gap found in Validation returns to this cycle for correction; repeat only invalidated evidence.

## Phase Deliverables

### Validation

#### V481.1

One concise validation record contains the isolated direct-CLI/proxy rejection, complete diagnostics, repeated rejection and corrected restart captures; exit/initialize-failure/timeout/race outcomes and timings; current Git-selected per-type target evidence and final scope=configured workspace static checks, retaining separate configured production Mypy; exact outcomes and any limitations, with no regression-test runs.

**Validates:** null

### Documentation

#### DOC481.1

Current health/restart and proxy references match the new diagnostic schema, recovery availability, truthful readiness/deadline, external retry/discovery limits and clean break; affected Markdown links pass.

**Validates:** null

## Related Documents

- [Approved Research strategy](<research.md>)
- [Reviewed Design](<design.md>)
- [Quality/evidence standards](<../../coding_standards/QUALITY_GATES.md>)
- [Recorded F6 evidence](<../issue473/tool-practice-findings.md#f6--template-admission-failure-terminates-bootstrap-and-leaves-a-falsely-ready-proxy>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-05 | @imp planner | Plan one implementation cycle and bounded validation/documentation after independent Design GO. |
$1
$2 2026-10-05 | @imp implementer | Correct the independently identified unsupported syntax selection: preserve native edit-content preflight, then run supported targeted format/lint gates. |
