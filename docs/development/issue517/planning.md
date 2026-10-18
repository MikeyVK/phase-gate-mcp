<!-- pgmcp:v1 id=planning pv=1.0.0 pf=OSfLTQ1qMuWvM9fi sf=WI5iXHBKVOU91bYE -->

# Issue 517 — Native SDK Migration Plan

**Status:** Proposed for independent Planning review  
**Version:** 0.8  
**Last Updated:** 2026-10-18

## Purpose

Deliver the approved Python3.15/SDK2.3 clean cutover with proportional behavior evidence.

## Scope In

Approved Design v0.3 at the existing SDK owners, prerequisites/direct consumers and actual installed acceptance.

## Scope Out

Release/publication, active runtime replacement, SDK1 environments, dependency-version assertion suites and #518 broad suppression fixes.

## Prerequisites

- Research v0.4 Approved Strategy and Design v0.3; independent Design GO on f91116de.
- Existing #513 selected Python3.15 environment is preparation only; final acceptance uses a clean actual wheel.
- No production edits until independent Planning → Implementation GO.

## Summary

C_1/C_2 delivered the native cutover and focused installed/proxy acceptance. The first complete Validation failed and independent QA rejected progression. C_3 repairs only the exposed consumer/prerequisite/checker gaps; renewed Validation owns the complete suite and branch/configured gates. The owner approved automatic Ruff discovery of Python files only; declare it explicitly without force-exclude.

## Dependencies

- C_2 depends on C_1; both retain their committed history.
- C_3 depends on C_1/C_2 and the first failed Validation; independent Planning review precedes Implementation re-entry with resume_cycle="C_3".
- Renewed Validation follows completed C_3 and independent QA GO.

## Risks

### Changing native pins makes the active old host unsuitable for authoritative target gates.

Use a temporary selected-stack RPC driver to call actual installed candidate run_checks/run_tests, with explicit PATH/config roots; preserve native guards and scopes.

### A package smoke can accidentally import the checkout.

Neutral working directory and explicit module/executable/metadata identity; source test imports are labeled separately.

## Work Units

### C\_1 — Native SDK and dependency cutover

**Goal:** Replace the coupled SDK boundary and its direct consumers as one coherent cutover.

**Cycle Number:** 1

#### Scope In

Three SDK production owners, direct consumers/helper, controlled metadata/native prerequisites.

#### Scope Out

SDK1 compatibility, dependency-version tests, #518 suppression policy, active host activation, release.

#### Deliverables

##### D\_1.1

Align Python/runtime/dev metadata and affected native adapter pins and language targets, preserving native guards and explicit covariance.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "pyproject.toml"

##### D\_1.2

Replace SDK1 registration and aliases at server/converter/proxy owners; deliver matching structured DTOs and explicit failure mapping, retaining initialized protocol and presentation/cache contracts.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "mcp_server/server.py"

##### D\_1.3

Adapt the identified direct SDK tests through an initialized native client lifecycle helper; remove obsolete API coupling and cover structured-output/error behavior proportionally.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "tests/mcp_server/test_support.py"

#### Exit Criteria

Coherent target source and prerequisites; focused migrated server/converter/schema/cache/attachment/admission tests and production typing pass on the selected stack through actual candidate MCP tools; no compatibility facade or guard bypass.

#### Dependencies

- Research v0.4; Design v0.3; Design QA GO on f91116de

#### Obligations

- Keep domain/presenter contracts and covariance; schema-compatible actual structured DTO.
- Keep source/prerequisites/test consumer cutover coherent; no temporary compatibility bridge.

#### Verification

##### Preservation and approved structured result

**Method:** Existing narrow host baseline before cutover; adapt valuable tests then candidate run_tests for affected SDK files; candidate run_checks on changed Python targets and production-scoped Mypy.

**Expected Result:** Meaningful scenarios pass on selected target; native client accepts structured DTO/schema, retains operation and processing errors and resource/cancellation behavior.

#### Stop Conditions

- Material target-stack conflict, required behavior outside approved strategy, or active host switch needed: reopen owner decision.
- Required native prerequisites unavailable or incomplete evidence: do not bypass guards or claim passing evidence.

### C\_2 — Proxy lifecycle and installed acceptance

**Goal:** Prove actual proxy lifecycle and clean installation without changing the active host.

**Cycle Number:** 2

#### Scope In

Existing proxy public behavior surface, isolated wheel/install and temporary RPC orchestration.

#### Scope Out

SDK1 compatibility, dependency-version tests, #518 suppression policy, active host activation, release.

#### Deliverables

##### D\_2.1

Replace shallow proxy cases with bounded public behavior evidence for restart/replacement, failed replacement, in-flight/cancellation/deadline and cleanup, using existing process injection.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "tests/mcp_server/core/test_proxy.py"

##### D\_2.2

Build/install the real wheel in an isolated Python3.15 environment; prove module/process identity, pip consistency, initialized actual pgmcp tool/resource/error and proxy lifecycle behavior; retain active host.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "scripts/build_package.py"

#### Exit Criteria

Focused lifecycle/installation evidence succeeds on the clean installed target; no orphaned children, SDK1 bridge, launcher mutation or release. Relevant file checks pass; independent QA requested before Validation.

#### Dependencies

- C_1

#### Obligations

- Use existing process_factory; deterministic observations and bounded teardown.
- Actual installed pgmcp and proxy on initialized2025 route, not only a minimal SDK example.

#### Verification

##### Lifecycle/install acceptance

**Method:** Focused tests/mcp_server/core/test_proxy.py through candidate run_tests; existing builder, clean install, pip consistency and actual stdio/proxy RPC.

**Expected Result:** Restart success/failure and in-flight/cancel/deadline/cleanup observed; installed identity correct and no child leak.

#### Stop Conditions

- Material target-stack conflict, required behavior outside approved strategy, or active host switch needed: reopen owner decision.
- Required native prerequisites unavailable or incomplete evidence: do not bypass guards or claim passing evidence.

### C\_3 — Validation consumer and prerequisite recovery

**Goal:** Repair the concrete missed consumers and verification prerequisites exposed by the first complete Validation, preserving C_1/C_2 and the approved application strategy.

**Cycle Number:** 3

#### Scope and Dependencies

Depends on C_1/C_2 and the failed Validation at commit `32083d48206fc085fcc8b89681a229d3ab6ada6d`, recorded in [Validation](validation.md). The original 82 failures, 70 setup errors, coverage shortfall and configured-gate failures remain negative evidence until replaced by a complete successful Validation. This cycle does not reinterpret focused greens as full acceptance.

| Deliverable | Scope and primary seams | Required focused evidence |
| --- | --- | --- |
| D_3.1 — Native adapter fixtures and evidence | Isolated Node/build prerequisites; Pyright native fixture; Ruff check/fix, Pytest and Mypy conformance consumers; orchestration NODE_PATH; obsolete requirements-dev text assertion | Affected native adapter families, including real diagnostic/report fidelity, native exact-version rejection and dependency-absence controls. Use actual native evidence; do not create version-only tests or reinstate the Python Pyright wrapper. |
| D_3.2 — Selected runtime startup and lifecycle evidence | Existing target-startup/v3-cutover and installed-distribution seams; test_support Client import; proxy and template-activation process cases | Selected-interpreter/public-process scenarios without private Codex config; reproduce the nine lifecycle failures in a bounded parallel selection. Capture readiness/error/termination observations before choosing any wait-budget repair. A serial pass or longer timeout alone is insufficient. |
| D_3.3 — Configured checker findings and focused closure | Concrete Python format/lint findings, template_activation contextmanager annotation and owner-approved Ruff discovery | Changed Python files receive applicable format/lint/Pyright checks; production-scoped Mypy covers annotation edits. Review unsafe syntax changes for semantic equivalence. Preserve covariance, diagnostic visibility and existing suppression policy. |

#### Selection Decision

Owner approved automatic Python-file selection on 2026-10-18: declare native Ruff include patterns for .py/.pyi files; Markdown code blocks are outside automatic discovery. Preserve deliberate targeting and do not enable force-exclude. This selects artifact types rather than disabling diagnostics; unrelated or historical Markdown rewrites and broader #518 suppression work remain excluded.

#### Execution and Cleanup

Provision build/setuptools/wheel and the configured Node tool versions only in the isolated selected-stack verification environment. Use ordinary workspace-local Node resolution and remove the diagnostic driver's global NODE_PATH; the deliberate missing-dependency fixture must stay missing. Keep active host/runtime and native prerequisites untouched.

Use existing tests/helpers and public runtime seams. Preserve adapter guards, source/native output fidelity, cleanup assertions and meaningful negative scenarios. Remove only the obsolete requirements text assertion; do not replace it with another metadata/version-content test. Localize the native Client import only within its existing helper, with a narrow import rationale if required.

For process failures, first observe imports, process exit/errors, initialization/readiness and teardown under the affected parallel selection. Compare any test-only budget to the existing production deadline; preserve the intentional silent-child timeout scenario. Stop on a reproduced production defect or contract change beyond the approved SDK boundary. On 2026-10-18 the owner explicitly included targeted repairs at any existing adapter owner required by the selected native toolchain upgrade, within D_3.1 and preserving public check/test/fix contracts. The Mypy missing-file execution_error/unavailable classification is the first concrete case. Retain complete native diagnosis and prove behavior with proportional existing cases; new policy or public-contract changes still require an owner decision.

Run affected families separately through candidate run_tests(scope="targets"), retaining their configured parallelism where needed to reproduce lifecycle failures. Use Python-file targets for Python gates and markdown_links for changed documents. Reuse unaffected evidence; no workspace-wide suite during this cycle.

#### Exit and Stop Conditions

Affected adapter, startup/installed and proxy/activation families pass through actual target MCP calls, including bounded parallel reproduction of lifecycle failures and native negative controls; changed-file gates pass. No new compatibility path, skip, threshold reduction, diagnostic suppression or active host change. Native Ruff automatic discovery is explicitly Python-only as approved by the owner. Independent QA reviews before re-entry to complete Validation.

After independent Implementation → Validation GO, rerun the complete configured suite with unchanged coverage/native parallelism, branch gates and final configured gates as specified below. Preserve the failed first run and report any remaining failures. A gate exception, new skip, lowered coverage, diagnostic disable, active-host switch or neutral-CWD GitManager repair is outside this recovery.

Cycle rollback uses the pre-recovery coherent commit; there is no SDK1 fallback. Existing committed C_1/C_2 blocks are not replaced.

### C\_4 — Complete startup callers and coverage measurement recovery

**Goal:** Resolve the remaining startup failure and the owner-retained90% combined coverage gate after the complete C_3 retry.

**Dependencies:** C_1–C_3 remain unchanged. Both failed full runs stay recorded in [Validation](validation.md). The owner retained the additional90% gate on 2026-10-18 after the absence of an earlier measured baseline was explained. Re-entry uses resume_cycle="C_4" after independent Planning → Implementation GO.

| Deliverable | Scope and seams | Focused evidence |
| --- | --- | --- |
| D_4.1 — Remaining installed startup clients | The two installed run_server_process callers in integration/test_target_startup.py; align their client window with source startup, retaining production deadlines and real handshake/error/cleanup behavior. | Existing target-startup/v3-cutover and proxy cases under native parallelism; no arbitrary sleep or serial-only acceptance. |
| D_4.2 — Complete native coverage measurement | pyproject.toml and existing process tests. pytest-cov7 removed automatic child coverage; coverage.py offers native patch=["subprocess"]. Evaluate collection/combination, installed/source identity and Windows termination before attributing missing coverage to absent tests. | Bounded actual-candidate child-process behavior and native coverage evidence. Preserve the measured mcp_server package, branch=true, fail_under=90 and visible diagnostics. Native path mapping only for proven identical source copies; never merge different versions or suppress missing source. |
| D_4.3 — Proportional behavioral coverage closure | Only genuine public-behavior gaps after measurement review, preferably adapting existing tests; no general test framework. | Focused behavior cases and file gates. Record tested behavior, not source-content, dependency-version or percentage assertions. Complete90% acceptance belongs to full Validation. |

**Execution:** Fix D_4.1 and establish a narrow process baseline. Evaluate native subprocess coverage with focused tests before retaining it; check isolated launches, selected interpreter, xdist combination and diagnostics. Preserve negative dependency controls and cleanup. Retain only trustworthy measurement. If real gaps remain, inspect owning public interfaces and add meaningful missing scenarios. Temporary diagnosis stays under .pgmcp/temp.

Native measurement selects source_pkgs=["mcp_server"] with --cov without a value, so child configuration keeps package identity rather than an absolute checkout path. Standard path aliases cover identical checkout/installed copies; source, branch scope and90% acceptance are unchanged. Native report precision=2 avoids whole-percent rounding of a sub90% result into acceptance.

**Exclusions and stops:** No threshold reduction, new exclusions/skips, diagnostic suppression, private coverage hooks, production changes for measurement, metric-only tests, compatibility, active-host upgrade, neutral-CWD GitManager repair or broad #518 work. A material public-contract/policy change or disproportionate test expansion requires owner discussion.

**Closure:** Candidate run_tests(scope="targets") covers affected tests; changed Python format/lint/Pyright and applicable configured production Mypy cover code; markdown_links covers edited documents. Independent Implementation → Validation review precedes the complete configured suite with unchanged --cov/--cov-branch and90% threshold, then required branch/configured gates. No full suite during this cycle. Rollback uses the coherent pre-C_4 commit; committed prior cycles are never replaced.

### C\_5 — Focused installed measurement and coverage-test recovery

**Goal:** Repair the two post-C_4 failures before attributing any remaining coverage shortfall to missing cases. Preserve C_1–C_4 and all negative evidence.

| Deliverable | Bounded implementation | Proof |
| --- | --- | --- |
| D_5.1 — Bounded installed measurement lifecycle | In the existing installed initialization/migration/planning-readback test only, launch the real installed proxy through its public constructor with initialization_timeout_seconds=90 and client timeout120. This tests functional integration under subprocess coverage without declaring a production startup SLA under instrumentation. Production default30, module-entrypoint controls in target_startup/v3_cutover and the explicit silent-child timeout case stay unchanged. No sleeps, retries or fallback success. | The full affected startup and pytest-adapter families plus unchanged core proxy controls pass with native workers. Run affected startup with --cov/--cov-branch and retain native data/diagnostics; a narrow selection may correctly fail the global90% threshold. Observe actual protocol, planning/cache roundtrip, migration and bounded process cleanup. |
| D_5.2 — Native coverage behavior without content coupling | Remove the stale repository coverage-dictionary comparison and its unused tomllib import. Keep this existing test's isolated native config, direct and adapter opt-in runs, absence of coverage by default and native below-threshold rejection. No replacement literal repo-content assertion. | Existing behavior cases pass via real native tools; format/lint/Pyright on the two changed test files and markdown_links on edited docs pass. No new test case/module planned. |

**Evidence and rationale:** [Post-C_4 Validation](validation.md#post-c_4-complete-validation) records2956 passed,2 failed and89.94% combined coverage. The failed child imported for approximately18s before bootstrap, then reached the existing30s deadline without readiness. Other real default startup routes passed in that same run. This establishes the need to distinguish the heavily instrumented functional integration budget from default-entrypoint timing; it does not prove a production deadlock or justify changing production timeout. The existing injectable constructor already supports this bounded test setup.

**Sequence:** Independent Planning → Implementation GO; transition with resume_cycle="C_5"; make only the two test edits; run the affected test families and scoped instrumentation/gates; record actual outcomes. The failed long installed test currently omits its substantive body, so inspect fresh measurements before proposing additional behavior cases. No percentage prediction counts as acceptance.

**Stops:** No production/config/threshold/source/parallelism change, new compatibility path, skip, suppression or arbitrary readiness sleep. Substantive public-contract/policy changes or disproportionate additional coverage work return to the owner. Independent Implementation → Validation GO precedes the next complete suite with the same90% gate and all branch/configured gates.

### C\_6 — Bounded replacement-initialization behavior coverage

**Dependency:** Completed C_5 at be29ff8696044b82831e59452fdc8a7a015dc7d9. All previous cycles and negative full runs remain intact.

**D_6.1:** Extend only tests/mcp_server/core/test_proxy.py's existing failed-replacement parameterization with two current public behavior scenarios: malformed JSON from the replacement during initialize, and a structurally valid initialize result that changes the negotiated protocol. The real controlled child is supplied by the existing process factory. Observe restart_failed and its actual diagnosis, subsequent ERR_SERVER_UNAVAILABLE/unavailable, absence of restart_completed, and termination of every real child through the existing fixture. No private method calls or source-content/percentage assertions.

**Rationale:** C_5's instrumented installed probe adds no covered production lines/branches relative to the89.94% full measurement. Its coverage-conformance fixture also needed a distinct synthetic package name (coverage_example) to prevent four sample lines/two branches from being measured as production; the native opt-in/threshold case passes after isolation. The two proposed proxy scenarios exercise genuine unproved failure handling at the changed SDK/transport boundary. This is two additional parameter cases in one existing test, with no permanent module or production change.

**Sequence and evidence:** Independent Planning → Implementation GO; resume_cycle="C_6"; adapt the existing real-child setup and parameterization; run only core/test_proxy.py through candidate run_tests with native workers and opt-in --cov/--cov-branch, retaining native XML and unchanged global90% rejection for a narrow selection. Confirm behavior assertions and actual previously missed branches, not a diagnostic union as final acceptance. Run targeted format/lint/Pyright and markdown_links for changed docs. Reuse C_5's unaffected39-case evidence with its explicit transient xdist timeout and passing targeted recheck; do not conceal either outcome.

**Exit/stop:** Two new protocol-behavior cases and original timeout/spawn/cancellation/cleanup cases pass; changed-file gates pass. Production defaults, source/branch selection, parallelism, thresholds, no-compat strategy and active host are unchanged. No broad test rewrite, private instrumentation or metric-only cases. Material policy/contract changes or disproportionate further expansion return to the owner. Independent Implementation → Validation GO precedes complete configured90% Validation and branch/configured gates. Rollback uses be29ff86; no earlier committed cycle is replaced.

### C\_7 — Exact coverage threshold and explicit initialize-error evidence

**Dependency:** Post-C_6 complete Validation at077c9220:2960 passing tests/all required checks, but raw16498/18332 (89.995636%) is below90. Native pytest-cov rounds to precision2 for its exit decision while its terminal summary compares the raw fraction and prints FAIL. Preserve this contradiction and reject forward progression despite adapter passed/exit0.

**D_7.1:** Change only pyproject.toml coverage.report.precision from2 to6; fail_under=90, source_pkgs, native subprocess/path configuration, branch scope, exclusions and parallelism stay unchanged. This makes a single missing hit distinguishable from90 for this workspace; it tightens admission rather than lowering the owner's threshold. The earlier C_4 precision2 text records that stage and is superseded here.

Add exactly one parameter to the existing public failed-replacement test in tests/mcp_server/core/test_proxy.py: a structurally valid JSON-RPC initialize error from the replacement. Its original error code, message and data must remain in the captured failure response; the proxy rejects it as initialize_response_failed/invalid_initialize_response, never announces restart_completed, returns unavailable for later work and terminates every real child. Reuse the existing controlled subprocess/event/sink/cleanup seams. This is a genuine explicit-refusal behavior at the migrated boundary, not a percentage assertion, SDK-version test or new module.

**Evidence and sequence:** Independent Planning → Implementation GO, resume_cycle="C_7"; keep all committed cycles. Execute only the existing proxy family with native workers and --cov/--cov-branch, preserving its expected narrow global threshold failure, XML and diagnosis. Run targeted format/lint/Pyright and changed-doc markdown_links. No production or adapter interpretation change is required: the adapter factually follows native exit0. Treat raw counts/complete native outcomes as the final acceptance evidence; do not teach the adapter to parse a special coverage summary.

**Exit/stops:** Existing proxy cases plus the single explicit-refusal case pass with real diagnosis/cleanup and file gates. No active-host switch, new architecture, compatibility, skips, source exclusions, deadline or threshold reduction. Material policy/contract changes return to owner. After independent Implementation → Validation GO, rerun the complete configured suite and required branch/configured gates; require actual combined coverage at least90%, tests green and no native threshold-failure text. Rollback uses the pre-C_7 snapshot; no replacement of earlier cycles.

### C\_8 — Readiness-ordered late-member stop evidence

**Dependency:** Complete C_7 Validation at46292376:2960 pass/1 failure, actual90.028366% and all required checks pass. Preserve that complete negative acceptance result and all committed cycles.

**D_8.1:** Change only tests/mcp_server/integration/execution/test_process_stopping.py. Its race-mode Node parent publishes race.ready after seeing the original children armed. The existing test awaits that factual marker asynchronously within5s after retained_children has armed both originals, then explicitly cancels the invocation. Use a20s test invocation ceiling as in the existing cancellation evidence. The injection still takes a real WindowsJob membership snapshot before requesting the genuinely later child and retains its existing2s birth-observation window.

The outcome assertion becomes InvocationCancelled with UNCONFIRMED because cancellation is now the deliberate trigger. Preserve the late-member count, retained scratch and absent late.done; do not weaken the old-snapshot confirmation invariant. Existing timeout-cause, cancellation-confirmation and shared-five-second-stop-budget tests remain unchanged. No new case/module, production code/deadline or broad helper refactor.

**Why this is ordering, not a stop-policy change:** Failed fixture markers (host local UTC+02) show spawn-late.request at16:16:56 before first.armed/second.armed at16:16:58. The1s invoke deadline started synchronous termination while the async test still needed to arm the originals; the2s polling callback blocked that event loop. The assertion occurred before a typed production outcome. Readiness before explicit cancellation removes that test-created deadlock while still exercising the same production kill/confirmation path.

**Sequence/evidence:** Independent Planning → Implementation GO; resume_cycle="C_8"; adapt the existing case/script; run only that process-stopping family with native workers and --cov/--cov-branch, keeping its expected narrow threshold rejection and XML. Targeted format/lint/Pyright and changed-doc markdown_links must pass. Confirm the marker precedes cancellation and no late child is accepted from the old snapshot. Reuse unrelated fresh evidence; no full suite during Implementation.

**Exit/stops:** Existing family passes; real race, cause/unknown confirmation, scratch retention and cleanup evidence remain meaningful. No arbitrary readiness sleep, skip, threshold/source/parallelism change, compatibility or production modification. Material contract/policy or disproportionate scope returns to owner. Independent Implementation → Validation GO precedes another full configured run requiring all tests/checks green and actual combined coverage at least90%. Rollback is the pre-C_8 snapshot; no previous cycle replacement.

## Phase Deliverables

### Validation

#### D\_1

Compact durable validation report with target identity, exact scopes/native outcomes, one full configured suite/coverage and branch/configured checks, installed/proxy acceptance and remaining risks.

**Validates:**

**Type:** file_exists

**File:** "docs/development/issue517/validation.md"

### Documentation

#### D\_1

Correct active setup/isolation/tooling docs invalidated by the delivered baseline; record outcome and handoff without rewriting historical research.

**Validates:**

**Type:** file_exists

**File:** "docs/setup/README.md"

## Evidence Timing and Rollback

During C_1, establish the narrow current-host baseline on existing server/converter/schema/attachment scenarios before changing their dependency contract. This uses the already operational host, not a new SDK1 compatibility environment. Retain that baseline only as preservation input. For genuinely uncovered structured-output/processing-failure obligations, demonstrate a meaningful failing assertion before the fix; do not manufacture RED for mechanical call-site changes.

After coherent cutover, use the selected-stack candidate's actual MCP run_tests/run_checks with the explicit targets for the changed SDK tests and Python files. Production Mypy uses scope="configured", checks=["python_types"]; tests do not become strict-Mypy targets. Ruff format/lint and Pyright use applicable Python targets. Keep Markdown under markdown_links and changed YAML/JSON under their appropriate checks. Temporary orchestration does not bypass adapters or native version guards. A C_1 build/install may prepare candidate RPC verification; C_2 still owns clean final installed acceptance.

Validation performs one full run_tests(scope="configured", tests=["python_tests"], args={"python_tests":["--cov","--cov-branch"]}, timeout_seconds=1800) through the installed selected-stack candidate. Keep native parallelism/configured coverage and use a client window longer than execution plus termination/delivery. Then run run_checks(scope="branch", checks=["python_format","python_lint","python_pyright"], timeout_seconds=600), relying on the approved per-check configured branch selection, and run_checks(scope="configured", checks=["python_types"], timeout_seconds=600). Run the final workspace-configured Python format/lint/Pyright selection once; reuse unchanged Mypy evidence. Check only changed documents/configs with applicable adapters. Record incomplete/unavailable runs as such; no gate exception.

Cycle rollback uses the prior coherent branch commit; do not keep a hybrid SDK1/SDK2 source or loosen prerequisites to get a pass. Isolated build/install output is disposable. Active host/client and credentials are not modified. Real lifecycle gaps may be repaired at their existing owner only within Design; new behavioral policy reopens the owner decision.

Independent QA is used only at phase boundaries. After cycle evidence, request Implementation → Validation GO; after Validation request Documentation GO; after active docs and final clean pushed state request Ready GO. Ready submission and end-issue merge handoff belong to the existing workflow and Coordinatie.

## Related Documents

- [Approved Research](<research.md>)
- [Design](<design.md>)
- [Quality evidence rules](<../../coding_standards/QUALITY_GATES.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-18 | @imp planner | Sequence native cutover, focused behavior evidence and clean installed proxy acceptance within the approved strategy. |
| 0.2 | 2026-10-18 | @imp planner | Add one bounded recovery cycle for failed full Validation; preserve prior cycles/evidence and record the owner's explicit Python-only Ruff discovery choice. |
| 0.3 | 2026-10-18 | @imp implementer | Record owner approval for targeted native-adapter repairs required by the selected upgrade, preserving public contracts and the C_3 boundary. |
| 0.4 | 2026-10-18 | @imp planner | Add C_4 for installed startup callers, native child coverage and proportional behavior gaps; retain owner-required90%. |
| 0.5 | 2026-10-18 | @imp planner | Add bounded C_5 for installed instrumented initialization and stale coverage-content test; preserve default startup controls and90% acceptance. |
| 0.6 | 2026-10-18 | @imp planner | Add C_6: two genuine public replacement-initialization behavior cases in the existing proxy test; keep all gates and defaults. |
| 0.7 | 2026-10-18 | @imp planner | Add C_7: native precision6 and one public explicit initialize-refusal case; preserve actual90% without rounded acceptance. |
| 0.8 | 2026-10-18 | @imp planner | Add C_8: readiness-order the existing late-member stop race with explicit cancellation; preserve timeout coverage and all production limits. |
