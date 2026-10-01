<!-- pgmcp:v1 id=planning pv=1.0.0 pf=E5cXGU37lhDmDnjF sf=9PfER5JkyAoFQLRi -->

# Native adapter robustness — implementation planning

**Status:** PLANNING — revised after owner clarification and QA findings; independent re-review requested
**Version:** 1.2
**Last Updated:** 2026-10-01

## Purpose

Sequence the approved correction for issues 469, 474 and 475 into bounded executable cycles with durable evidence and explicit stops.

## Scope In

The Design 1.3 boundary: nine bundled packages/ten roles/thirteen capabilities; direct correction of the existing unreleased adapter contract, PGMCP invocation lifecycle, native completion/version/failure behavior, full native selection transport and proportional cache/report behavior.

## Scope Out

Production/test implementation during Planning; legacy, compatibility/transition code, new contract version families or external-consumer migration; OS sandboxing, installation, general permissions/parser frameworks, unrelated archive/ACL work and issue closure.

## Prerequisites

- Research 1.5 Approved Strategy: the owner's development-only B1 refinement supersedes the earlier proposed v2 migration; B2–B6 and replacement B4 remain.
- Design 1.3 carries the required JSON context and CQS interface without new version admission. Existing contract_version 1 and schema paths remain the identity of the one unreleased contract.
- Planning 1.0 received independent QA NOGO on e5794187 for edit-preflight sequencing and Python branch-gate selection. This revision addresses both and requires renewed independent QA; earlier Design GO does not approve the refinement by inheritance.
- Active initialized issue469 bug branch remains in Planning. Native prerequisites are existing package declarations; no installation or global workflow-policy change is planned.

## Summary

This work finishes the unreleased architecture from issue 460. Correct the existing contract directly, retain its internal identity and keep one current shape. No external compatibility, transition, legacy support or migration proof is part of these cycles.

| Cycle | Correction boundary | Deliverables | Depends on |
|---|---|---|---|
| 1 C_PROTOCOL | Required JSON context, directory ownership and working development server | D1_PROTOCOL, D1_OWNERSHIP, D1_REGRESSION | Approved artifacts |
| 2 C_COMPLETION | Truthful completion, versions and failure reasons; E475-1 | D2_COMPLETION, D2_VERSIONS, D2_FAILURES | 1 |
| 3 C_ARGFILES | Ruff/Mypy/Pytest full selection | D3_ARGFILES, D3_EQUIVALENCE | 1, 2 |
| 4 C_STDIN | Pyright/Lychee full selection and channel ownership | D4_STDIN, D4_LIMITS | 1, 2, 3 |
| 5 C_EFFECTS | Accepted native caches/reports and retained contract guards; E474-1 | D5_EFFECTS, D5_REGRESSION | 1, 2, 3, 4 |

The sequence keeps one causal family per cycle; stdin encoding does not depend on argument-file implementation. Existing capability/selection/fix/process behavior remains the correctness baseline.

The owner's explicit instruction supersedes the default elaborate RED/GREEN proof framing for this development work. Mechanical contract/schema/fixture maintenance has no mandatory RED commit or historical-version refusal suite. Reuse focused existing tests; add or adapt a small functional test only for a concrete uncovered defect or ownership invariant. Existing Research reproductions may explain the cause without being recreated as a test ceremony. Record actual check/test results and limitations; do not call a failed or unavailable check a pass.

For each cycle, keep the server and normal tooling usable, perform its small correction-specific checks, and commit coherent work with workflow_phase='implementation', cycle_number=N and the applicable configured green/refactor subphase. A RED commit is useful only when an actual failing regression is already available or a small meaningful test is needed; it is not an artificial prerequisite. Refactor only replaced local guards/transport duplication or changed types, and commit refactor only if files changed.

Use run_tests(scope='targets', tests=['python_tests'], targets=[affected existing test files], args={'python_tests': [a precise -k selector when it covers the changed behavior]}). Python file gates use explicit Python targets with python_format/python_lint and applicable existing production typing obligations; no new strict-Mypy gate for the excluded test tree. Native syntax/entry-point checks and schema/fixture checks cover their actual admitted file grammar. Markdown uses offline markdown_links and scaffold/safe_edit content validation.

The full configured test run and broad review remain in Validation. All Python review calls receive an explicit recorded list of changed Python files, not a mixed branch scope. Keep the configured production Mypy baseline and handle other file types with their applicable checks. Reuse fresh evidence; repeat broad runs only after material invalidation.

After a satisfied cycle, transition_cycle(to_cycle=N+1) and refresh context. After cycle 5 request independent Implementation review rather than advancing phase autonomously. Temporary report-mode edits are operational development choices, not compatibility code. Deliverables use validates=null where file/text presence cannot establish behavior. The numbers, names, IDs, descriptions and exits below match the structured plan; detailed scope, dependencies and editing order live here.

## Dependencies

- C_PROTOCOL → C_COMPLETION → C_ARGFILES → C_STDIN → C_EFFECTS; subsequent phase transitions follow independent review and the active workflow.
- Current preflight configuration remains unchanged. The loaded editor uses the old request shape until the planned restart; package entry-point changes are ordered accordingly.
- @co owns issue474 wording alignment and separate issue disposition before acceptance/closure; no external-consumer migration dependency.

## Risks

- **An adapter request rejection still blocks report-mode editing:** Keep preflight entry points accepting the currently loaded runtime's shape until their consumers' remaining edits are finished; update python_syntax/check.py last and restart immediately. Report is not a skip mode.
- **Native grammar or channel ownership has a real limit:** Use small actual-native controls for the corrected route; keep the explicit Lychee occupied-channel limitation and refuse unrepresentable input without dropping targets.
- **Server restart or native provisioning prevents a working cycle:** Stop on failed bootstrap/health/smokes, inspect actual diagnostics and use prescribed recovery tools where available. Do not hide the failure with a bridge, skipped prerequisite or invented pass.

## Milestones

- Planning: amend strategy/design/planning, update and verify identical structured deliverables, run document checks, commit/push and request independent GO/NOGO for Implementation.
- Implementation: five coherent working cycles, temporary report-mode edits where appropriate, short focused functional checks and scoped commits.
- Validation/Documentation: one configured full suite and appropriately typed broad gates; current-contract guidance and separate issue acceptance/disposition.

## Work Units

### C_PROTOCOL — Direct contract correction and PGMCP resource ownership

**Cycle Number:** 1
**Owner:** @imp implementer
**Goal:** Add required JSON execution context to the existing unreleased contract and retain a working server, with no compatibility or version-migration code.

#### Scope In

Existing check_v1/test_v1/fix_v1 schemas in execution/contracts; strict/frozen wire DTOs separated from operation intent; pure encoders in execution/protocol.py; directory interface in core/interfaces/execution.py and concrete execution provider; process_runtime.py, check_service.py, test_service.py, fix_service.py and bootstrap.py. Update all nine bundled validators/ten roles and current fixtures in tests/mcp_server/fixtures, unit/execution, unit/server/test_bootstrap.py, integration/execution, integration/adapters and template activation/proposal tests. Inspect catalog/presentation/manifests only for required consistency; retain contract_version 1 rather than perform version-only edits.

#### Scope Out

No new v2 schemas, identity bump, old-version rejection tests, optional wire context, bridge, environment context channel or external-consumer migration. Later cycles own native transport/completion/cache changes.

#### Deliverables

##### D1_PROTOCOL

Existing strict check/test/fix schemas, encoders, bundled validators and current fixtures directly corrected for required JSON context; current contract_version 1 and public MCP parameters/results retained, with no legacy or compatibility paths.

**Validates:** null

##### D1_OWNERSHIP

Injected CQS directory description/create/remove and runtime ownership after exclusive successful creation, with confirmed-termination cleanup and no PGMCP environment context channel.

**Validates:** null

##### D1_REGRESSION

Updated useful current-contract/runtime tests and fresh-server health plus working edit/check/test/fix smokes; no separate migration or historical-version proof suite.

**Validates:** null

#### Dependencies

- Research 1.4 current B1 and Design 1.2; renewed independent Planning/strategy review.

#### Obligations

- RF4/RF6/RF7; QA P1/P2 architecture remains. PGMCP owns allocation/lifetime and carries the location in required JSON context; adapters translate it.
- Pure describe(UUID) returns a frozen description; create/remove return None. Successful exclusive creation establishes ownership; never adopt or delete an existing path.
- Retain one current development contract and existing identity 1. Report mode still executes checks and preserves request-rejection/preparation/interruption/termination blockers.
- QA Planning blocker P2/editing: follow the concrete preparation/final-edit/restart sequence below. Do not call unrelated functional checks through adapters already changed on disk while the server still uses the old request shape.

#### Verification

##### Prepare while the existing preflight remains usable

**Method:** Before any preflight-validator replacement, scaffold all new files using the discovered artifact schemas, prepare all schema/fixture/current-doc changes, and make the server DTO/encoder/provider/service/bootstrap edits. Leave checks config/template profiles and python_syntax/check.py unchanged. Complete all Markdown and TypeScript edits before changing markdown_preflight/check.py and typescript_syntax/check.cjs respectively. Other bundled entry points can then be updated; remaining Python edits still use unchanged python_syntax. safe_edit_file(validation='report') is available for ordinary failed/unavailable results or unprofiled files, with actual outcomes retained. Verify the selected profile from each receipt instead of assuming it.

**Expected Result:** Every preparation edit uses the loaded server's existing request shape with a still-compatible selected preflight. No native request-rejection blocker is treated as writable or as a skipped check.

##### Final preflight edit and immediate restart

**Method:** Finish every other source/fixture edit first. Apply the complete python_syntax/check.py context-validator change in one final safe_edit_file rewrite with validation='enforce': its existing on-disk entry point checks the proposed Python syntax before replacement. Require written=true and passed syntax. After that replacement perform no edit, scaffold, native check/test/fix or adapter-backed commit; immediately call restart_server(reason='Issue 469 direct development contract correction'). Then get_work_context() and health_check(), inspect restart/health facts and run small normal edit/check/test/fix fixture smokes with the corrected server. A new substantive uncovered error must be corrected with the now-coherent tools; failed startup remains a blocker.

**Expected Result:** The final edit cannot leave a syntax-invalid preflight via report mode. Fresh composition loads the corrected producer, all required context validators and current catalog identity together. The editor returns to normal enforce use; there is no dual request acceptance or version bridge.

##### Small current-behavior and ownership checks

**Method:** Adapt existing service/runtime/content/adapter fixtures to pass the required context and retain their meaningful assertions. Run focused affected existing tests rather than an exhaustive role×context-error matrix. Use current schema validation and a small malformed/missing-context control; cover exclusive-create collision preservation and pure description at the public resource/runtime boundary, reusing existing lifecycle evidence.

**Expected Result:** Current requests work, missing context is honestly invalid_request, owned cleanup and content snapshots remain separate, and captured errors/termination facts remain truthful. No artificial RED or old-version refusal claim is required.

#### Exit Criteria

D1_PROTOCOL, D1_OWNERSHIP and D1_REGRESSION are complete: the existing contract is directly corrected with identity 1 and required context; focused current tests pass, the final preflight edit/restart sequence completes, and fresh-server health plus normal operation smokes succeed. No compatibility, legacy or external-migration code remains.

#### Stop Conditions

- Stop on request rejection during preparation; report cannot override it. Inspect the selected profile and edit order rather than weaken editor behavior.
- Do not replace python_syntax/check.py until all other edits are complete; do not make subsequent adapter-backed calls before restart.
- Stop on failed restart/health/operation smoke, unsafe resource ownership or a change to approved responsibilities.

### C_COMPLETION — Truthful native completion, versions and failure reasons

**Cycle Number:** 2
**Owner:** @imp implementer
**Goal:** Prevent metadata/substitute operations from becoming PASS and report supported native prerequisites and substantive failures truthfully.

#### Scope In

Package-local completion/version/classification seams in bundled_adapters/ruff/check.py and fix.py, mypy/check.py, pyright/check.cjs, pytest/test.py, lychee/check.py and commitlint/check.py and their existing dependency declarations. Preserve actual-version coverage for python_syntax, typescript_syntax and markdown_preflight. Adapt the corresponding tests/mcp_server/integration/adapters files and existing execution presentation tests only where observable envelopes change.

#### Scope Out

No new dependency registry, installer, universal plugin admission or shared native parser. No transport rewrite or cache/report policy change in this cycle.

#### Deliverables

##### D2_COMPLETION

New Research-proven metadata guards and regressions for Mypy, Ruff lint/format and Pyright, with separately assessed aliases/alternate operations and preserved intentional completion policies.

**Validates:** null

##### D2_VERSIONS

Package-local observed-versus-declared native prerequisite checks and dependency_unavailable results before version-dependent behavior or mutations.

**Validates:** null

##### D2_FAILURES

Substantive access/configuration/usage/execution and missing-negative-evidence classifications, independent of verbose chatter, with retained native facts and bounded useful diagnostics.

**Validates:** null

#### Dependencies

- C_PROTOCOL

#### Obligations

- RF2/RF3/RF5; Research B3/B5/B6; QA P3. Read package dependency declarations as version SSOT; unsupported/unreadable prerequisites fail before version-dependent parsing and source mutation.
- New guards are required for Mypy --help, Ruff lint --help/--show-files, Ruff format --help and Pyright --help. Retain valuable Pytest/Lychee/Commitlint/Ruff-fix guards; assess parser-admitted aliases and alternate modes separately.
- Preserve intentional Ruff --exit-zero, Pytest collect-only and exit 5. Guard effective caller/config/environment/response-file sources where the native parser supports them.

#### Verification

##### False PASS routes and preservation

**Method:** Reuse existing real-native entry-point tests for Mypy --help, Ruff lint --help/--show-files, Ruff format --help and Pyright --help; add a small missing case only when existing coverage cannot exercise the correction. Keep intentional Ruff exit-zero and Pytest collect-only/exit5 controls. Check indirect routes only where changed guard logic needs them.

**Expected Result:** Metadata is unsupported_input rather than passed analysis; ordinary and intentionally supported results retain their semantics. A separate staged RED exercise is optional.

##### Prerequisites before effects

**Method:** Reuse package version fixtures and one installed-version control for changed guarded behavior; observe that unavailable/mismatched prerequisites produce useful version facts before analysis or source edits. No nine-package permutation matrix.

**Expected Result:** Actual and expected versions are useful; unsupported versions yield dependency_unavailable before parsing or edits. No second version table or automatic install; stdlib runtime facts stay factual.

##### Failure meaning and evidence

**Method:** Use existing native error/presentation fixtures and a small quiet/verbose substantive-cause comparison for the changed classifier. Retain useful malformed/missing-result tests; do not introduce ACL/platform matrices or environment-dependent skip proofs.

**Expected Result:** The concrete corrected failure is classified and messaged consistently; retained useful evidence stays bounded. Required unavailable prerequisites remain explicit.

#### Exit Criteria

D2_COMPLETION, D2_VERSIONS and D2_FAILURES have passing small focused native checks and useful affected tests/gates; the proven metadata routes no longer return false PASS and server/tool health remains good.

#### Stop Conditions

- Stop if effective native argument/config precedence cannot be established for a claimed guard.
- Stop if a supported-version decision differs from the existing declaration or requires new installation policy.
- Stop if a proposed classification invents a public status/reason enum or hides a required prerequisite failure.

### C_ARGFILES — Single-run native argument files for Ruff, Mypy and Pytest

**Cycle Number:** 3
**Owner:** @imp implementer
**Goal:** Remove Windows target-vector launch limits without changing full native analysis/session semantics.

#### Scope In

Ruff check lint/format and fix, Mypy check and Pytest test argument-file translation in their package entry points; tests/integration/adapters/test_ruff_checks.py, test_ruff_fixes.py, test_mypy.py and test_pytest.py under tests/mcp_server. The files remain in the supplied invocation directory.

#### Scope Out

No target batching, universal selection filter, command-line truncation, workspace fallback, generic response-file parser or new process/session framework.

#### Deliverables

##### D3_ARGFILES

Native @file transport for Ruff lint/format/fix, Mypy and Pytest using the supplied context, preserving full ordered native arguments and one invocation.

**Validates:** null

##### D3_EQUIVALENCE

Useful real-native large/small-selection and existing literal/option/discovery/exclusion checks, retaining Mypy cross-file behavior, Pytest session behavior and Ruff fix effects.

**Validates:** null

#### Dependencies

- C_PROTOCOL
- C_COMPLETION

#### Obligations

- RF1/RF2/RF6; Research B2. Encode the whole already-admitted ordered argument vector and target selection using each pinned native @file grammar; one analysis/session per role.
- Preserve configured empty-selection discovery, native exclusions, option order, literal paths, Mypy whole-program imports and Pytest plugins/xdist/fresh --native child, collect-only and exit5.
- Refuse unrepresentable response-file input explicitly; caller-controlled response files cannot bypass role/selection guards. Fix admission completes before any edit and ordered failure/partial mutation remains truthful.

#### Verification

##### Oversized native selections

**Method:** Reuse/adapt real-native fixtures for one representative complete oversized Windows selection per changed role, with a late diagnostic/change and a small control. Keep existing cross-file Mypy and Pytest session fixtures rather than building a separate batching-proof harness.

**Expected Result:** The corrected route processes the full selection in one native analysis/session and retains the late result, without launch-size failure, truncation or workspace fallback.

##### Pinned grammar and configuration equivalence

**Method:** Reuse existing literals/options/configuration/exclusion controls and add only an uncovered native grammar case caused by the new encoding. Check a concrete unrepresentable token and indirect guard route where relevant, without a broad new encoding/permutation suite.

**Expected Result:** No quoting loss, trimming, silent omission or rewritten discovery. Unsupported encodings are unsupported_input before native analysis; native config/exclusion semantics remain authoritative.

##### Fix and session preservation

**Method:** Run useful existing Ruff fix/admission/partial-mutation and Pytest plugin/import/session controls affected by the transport; no new session framework or broad proof harness.

**Expected Result:** No pre-admission source change, no retry/rollback fiction and no duplicate native session; existing useful native policies still pass.

#### Exit Criteria

D3_ARGFILES and D3_EQUIVALENCE are complete with working full-selection @file transport, small actual-native large/small controls and passing affected existing preservation tests/file gates; server/tool health remains good.

#### Stop Conditions

- Stop if the pinned native @file grammar cannot faithfully encode an admitted vector; report the specific limitation instead of dropping targets.
- Stop if Pytest loses its established process/plugin/session boundary or Mypy becomes multiple analyses.
- Stop if fix transport mutates sources before all-input admission.

### C_STDIN — Native stdin selection for Pyright and Lychee

**Cycle Number:** 4
**Owner:** @imp implementer
**Goal:** Move complete selected filenames off the command line while respecting native input-channel ownership.

#### Scope In

Pyright check.cjs '-' filename input and Lychee check.py '--files-from -' selection; existing test_pyright.py and test_lychee.py; snapshot/content checks affected by Lychee filename transport.

#### Scope Out

No forced takeover of a caller/config-owned Lychee files-from channel, content-stdin replacement, new base/remap policy or hidden discovery fallback.

#### Deliverables

##### D4_STDIN

Complete Pyright and available-channel Lychee native stdin filename transport with correct configured-discovery and input-channel ownership behavior.

**Validates:** null

##### D4_LIMITS

Real-native large/literal/exclusion/discovery and Lychee content-snapshot regressions, plus explicit conflicting-channel and unrepresentable-input limitations.

**Validates:** null

#### Dependencies

- C_PROTOCOL
- C_COMPLETION
- C_ARGFILES

#### Obligations

- RF1/RF2/RF6; Research 1.5 B2 owner amendment and Design 1.3. Pyright representable nonempty selection uses native filename stdin; reject the complete explicit selection if a filename would be split or trimmed, including ordinary spaces or CR/LF. No argv fallback, escaping or path substitution. Empty selection retains native configuration discovery, including native discovery of space-containing filenames.
- Preserve Pyright native scalar option values in argv. Refuse effective caller additions/replacements of the owned file channel for nonempty selections. Prove that dangling option values cannot consume the stdin marker and silently switch to discovery.
- Lychee uses stdin filenames only when that effective native channel is free. If user/config files-from already owns it, preserve the admitted argv route and document its launch-size limitation; do not overwrite user intent.
- Escape literal paths using pinned native grammar; preserve content-snapshot base/remap, no dropped blank/comment-like entries or newline ambiguity. Adapters never allocate or clean the PGMCP root.

#### Verification

##### Complete real-native selection

**Method:** Reuse/adapt Pyright and offline Lychee fixtures for a representative old-oversized selection with a late finding and small/configured-discovery controls. Use existing literal/exclusion cases as applicable; no exhaustive selector matrix.

**Expected Result:** Native stdin handles complete ordinary selection with the late finding and configured discovery preserved; no batching or dropped paths.

##### Input channel and literal grammar

**Method:** Use existing Lychee files-from/content/base/remap fixtures plus a small effective-channel-conflict and unrepresentable-token control. Keep tests offline/local.

**Expected Result:** No empty stdin replacing discovery, no stolen native channel or silently filtered paths. Pyright's owner-approved explicit-space/trim limitation is unsupported_input with no analysis; supported encodings preserve literals. Lychee's occupied-channel launch-size limit remains explicit.

#### Exit Criteria

D4_STDIN and D4_LIMITS have passing small native selection/discovery/channel controls and useful affected tests/file gates; the occupied-channel Lychee limit is explicit and server/tool health remains good.

#### Stop Conditions

- Stop if effective files-from ownership or native line encoding is uncertain for a claimed supported case.
- Stop if filename stdin changes content-mode semantics or base/remap behavior.
- Stop if a test requires live external network or an undisclosed dependency skip to appear green.

### C_EFFECTS — Proportional native cache and supplemental-output policy

**Cycle Number:** 5
**Owner:** @imp implementer
**Goal:** Align existing write guards with accepted local-use policy while protecting requested operation, selected sources and captured results.

#### Scope In

Existing Ruff check/fix and Mypy cache/report guards, Lychee cache/cookie/state guards and corresponding tests; retain and sharpen contract-changing refusals in those packages only where Design identifies them. Reuse existing real-native effect fixtures and separate ordinary output cases from refusal cases.

#### Scope Out

No enforced universal cache destination, OS isolation, arbitrary-host escape suite, environment sanitation, permissions manifest or automatic deletion of native side outputs.

#### Deliverables

##### D5_EFFECTS

Ordinary native cache/cookie/temporary-output and compatible Mypy supplemental-report behavior admitted under B4, with contract-changing routes still refused.

**Validates:** null

##### D5_REGRESSION

Real-native CLI/config/environment effect and result-capture coverage where supported, source-byte preservation or intentional Ruff fix effects, and durable refusal regressions without a general sandbox suite.

**Validates:** null

#### Dependencies

- C_PROTOCOL
- C_COMPLETION
- C_ARGFILES
- C_STDIN

#### Obligations

- RF3/RF4/RF6; replacement Research B4 and Design D3. Admit native-configured ordinary caches/temporary toolfiles and compatible supplemental reports at operator-selected locations, including outside selected sources.
- Retain contract-required capture and source/role guards: Ruff/Lychee output redirection, Mypy source substitution/alternate analysis and install-types, Lychee replacement/preprocess/content/base/remap/method routes as designed.
- Do not claim source rollback, filesystem confinement, isolation from executed tests/plugins or general security guarantees.

#### Verification

##### Allowed operational effects

**Method:** Adapt existing overbroad-refusal tests to demonstrate the claimed allowed cache/report/state effect in a temporary destination outside selected sources, with supported native CLI/config/environment sources only where changed behavior requires them. Reuse useful default/disabled controls.

**Expected Result:** Ordinary accepted native effects work with correct returned diagnostics; checks preserve source bytes and Ruff fixes retain admitted-source behavior, without an artificial policy-RED exercise.

##### Contract-changing refusal and failures

**Method:** Retain useful existing source/operation/output/installation refusals; exercise a small indirect guard or operational-write failure only if changed behavior needs coverage. No general sandbox, destination or precedence matrix.

**Expected Result:** Requested operation/result capture remains correct; refusal occurs before unwanted source effects. Native operational failures have useful reasons, and no returned success implies side-output rollback.

#### Exit Criteria

D5_EFFECTS and D5_REGRESSION have passing small allowed-effect/refusal checks and useful affected tests/file gates under B4, without confinement claims; server/tool health remains good.

#### Stop Conditions

- Stop if a report suppresses required status/diagnostic capture or an admitted native option substitutes operation/source selection.
- Stop and reopen the affected strategy if evidence demands a general permissions/sandbox policy rather than a targeted contract guard.
- Stop if the implementation treats issue 474's superseded fixed-destination wording as binding over approved B4.

## Phase Deliverables

### Validation

#### V_NATIVE

One full configured native python_tests run in Validation through run_tests(scope='configured', tests=['python_tests']) with existing configured arguments/prerequisites and factual outcome; do not force an alternate serial or reduced suite to manufacture success.

**Validates:** null

#### V_GATES

In Validation derive and record the complete changed Python-file list from the branch diff, then run_checks(scope='targets', targets=<that explicit .py list>, checks=['python_format','python_lint','python_pyright']); keep run_checks(scope='configured', checks=['python_types']) for the existing production Mypy baseline. Handle changed CJS/JSON/Markdown/manifests separately using their admitted syntax/schema/entry-point/link checks; no implicit adapter extension filtering.

**Validates:** null

#### V_ACCEPTANCE

Concise Validation report maps the separate E469/E474/E475 and existing cross-cutting obligations to actual useful tests/smokes and fresh receipts, records server health, unavailable prerequisites and transport limits, and requests independent QA; no compatibility or exhaustive conformance proof.

**Validates:** null

### Documentation

#### DOC_GUIDANCE

Update active protocol/execution/tool guidance for the one directly corrected unreleased contract, required context and PGMCP ownership, ordinary native caches/reports, declared native versions and concrete transport limits; retain internal identity 1, with no external migration or legacy instructions.

**Validates:** null

#### DOC_DISPOSITION

Retain separate 469/474/475 acceptance/disposition and link @co alignment of issue 474's superseded wording before acceptance/closure. Document accepted host-account access, scoped guarantees and remaining Lychee input-channel limitation honestly.

**Validates:** null

## Implementation B2 amendment

On 2026-10-01 the owner directed that paths unsupported by Pyright's pinned stdin convention must not be used, after the native space-splitting limit was explicitly raised. Research 1.5 records the strategy decision and Design 1.3 defines the bounded filename-channel contract. C_STDIN must replace earlier explicit-space-success assumptions with native supported-input and explicit-refusal evidence. The existing D4_STDIN/D4_LIMITS descriptions and five-cycle payload still apply; no cycle or new deliverable is added. Review this amendment independently with Implementation evidence; the earlier Planning GO applies to revision 1.1.

## QA and Owner Disposition

| Input | Current disposition |
|---|---|
| Planning QA P2: blocked edit/preflight sequence | C_PROTOCOL preserves the loaded preflight contract during preparation, finishes Markdown/TypeScript work before switching their adapters, changes Python syntax last under enforce and restarts immediately. report is used only with its actual blocker semantics |
| Planning QA P2: mixed branch paths passed to Python checks | V_GATES records the explicit changed-Python-file list and uses targets scope; non-Python paths get their applicable separate checks |
| Owner: unreleased development after issue 460 | Research 1.4 and Design 1.2 record direct in-place correction, identity 1, no legacy/compatibility/external migration work and proportional verification |
| Independent authority | Request renewed GO/NOGO for Planning → Implementation and the strategy refinement. No producer claim clears the prior NOGO |

## Related Documents

- [Approved Research](research.md)
- [Approved Design](design.md)
- [Historical effect probe](effect-probe.md)
- [Architecture Principles](../../coding_standards/ARCHITECTURE_PRINCIPLES.md)
- [Quality Gates](../../coding_standards/QUALITY_GATES.md)
- [Type Checking Playbook](../../coding_standards/TYPE_CHECKING_PLAYBOOK.md)
- [Execution/runtime seams](../../../mcp_server/execution)
- [Native adapter regression suite](../../../tests/mcp_server/integration/adapters)
- [Editor preflight and report policy](../../../mcp_server/services/edit_operation.py)
- [Existing report-mode blockers](../../../tests/mcp_server/integration/test_edit_operation_v3.py)
- [Current Python preflight entry point](../../../mcp_server/bundled_adapters/python_syntax/check.py)
- [Configured preflight profiles](../../../.pgmcp/config/checks.yaml)

## Bug / Planning Hand-over

### Scope

Direct development correction for 469/474/475, with server/tool health checkpoints, targeted actual-behavior checks and the existing ownership/native boundaries. Compatibility/legacy and external migration are excluded.

### Deliverables

- [Planning](planning.md)
- [Design 1.2](design.md)
- [Research 1.4 and current Approved Strategy](research.md)
- Identical five-cycle operational planning payload through update_planning_deliverables.

### Evidence

Document checks, saved-payload parity and commit/push facts are provided with the review request. Planned native/runtime checks are future implementation work, not passing evidence.

### Open Work

Renewed independent review of the owner's strategy refinement and the two corrected Planning findings. @co retains issue474 wording/disposition alignment before acceptance/closure.

### Review Request

Review requested.

