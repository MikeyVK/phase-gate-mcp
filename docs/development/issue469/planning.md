<!-- pgmcp:v1 id=planning pv=1.0.0 pf=E5cXGU37lhDmDnjF sf=9PfER5JkyAoFQLRi -->

# Native adapter robustness — implementation planning

**Status:** PLANNING — independent QA review requested
**Version:** 1.0
**Last Updated:** 2026-10-01


## Purpose

Sequence the approved correction for issues 469, 474 and 475 into bounded executable cycles with durable evidence and explicit stops.

## Scope In

The Design v1.1 boundary: all nine bundled packages/ten roles/thirteen capabilities; coordinated adapter input v2, PGMCP invocation lifecycle, native completion/version/failure behavior, full native selection transport and proportional native cache/report behavior.

## Scope Out

Production/test implementation during Planning; redesign of Approved Strategy; OS sandboxing, general write-permission APIs, installation, broad parser/framework work, workspace exclusions, archive/ACL/filesystem-adapter redesign and issue/PR closure.

## Prerequisites

- Research v1.3 Approved Strategy B1–B6, amended B1 and replacement B4; no later phase silently changes compatibility or trust policy.
- Design v1.1; independent @qa Design GO for commit 288b77aed9e1e1d566cb353cd77fb17ea2cdafaa, review turn 01a0f815-af37-7ce0-a9a3-22be1140b179 in chat 'Beoordeel designplan'. This verdict approves Design to Planning only.
- Active initialized bug/469-native-adapter-robustness branch and Planning phase confirmed through get_work_context/get_project_plan.
- Native tools/plugins are provisioned according to package declarations; unavailable prerequisites block their required evidence. Read Architecture Principles and Type Checking Playbook for affected production and test boundaries before edits.



## Summary

Five dependency-ordered cycles implement the existing Design, without choosing new interfaces or release policy.

| Cycle | Causal/acceptance boundary | Main deliverables | Depends on |
|---|---|---|---|
| 1 C_PROTOCOL | QA P1/P2; RF4/RF6/RF7; all input consumers | D1_PROTOCOL, D1_OWNERSHIP, D1_REGRESSION | Approved Design |
| 2 C_COMPLETION | RF2/RF3/RF5; E469-2/4 and E475-1; QA P3 | D2_COMPLETION, D2_VERSIONS, D2_FAILURES | 1 |
| 3 C_ARGFILES | RF1/RF2/RF6; E469-1/3 and E-CROSS | D3_ARGFILES, D3_EQUIVALENCE | 1, 2 |
| 4 C_STDIN | RF1/RF2/RF6; E469-1/3 and E-CROSS | D4_STDIN, D4_LIMITS | 1, 2, 3 |
| 5 C_EFFECTS | RF3/RF4/RF6; E474-1 and E-CROSS | D5_EFFECTS, D5_REGRESSION | 1, 2, 3, 4 |

Cycle 1 is intentionally one coordinated cutover: splitting the active v2 wire producers, consumers or loaded server across GREEN commits would leave an unsupported mixed contract. Subsequent cycles retain a working v2 boundary while changing one causal behavior family. Their dependency order enables sequential execution and cumulative evidence; it does not imply that the independent stdin grammars depend on argument-file code.

For each behavior correction, adapt a valuable existing durable regression or characterization, obtain intended RED through the current public boundary, and commit with workflow_phase='implementation', cycle_number=N, sub_phase='red'. GREEN minimally corrects the cause and includes passing focused affected tests and file gates before a sub_phase='green' commit. Mechanical fixture/schema-reference migration accompanies the coherent correction and needs no artificial separate RED. REFACTOR is limited to removing replaced guards/duplicate transport code or tightening changed types within the same package/boundary; rerun affected tests and file gates and commit sub_phase='refactor' only if files changed. No shared native parser, workflow-only assertion suite or unrelated cleanup is planned.

Use run_tests(scope='targets', tests=['python_tests'], targets=[changed regression files], args={'python_tests': [a precise -k selector only when it still covers every changed obligation]}) and run_checks(scope='targets', targets=[changed Python files], checks=['python_format','python_lint']) for cycle evidence. For changed production typing seams, add targeted python_types/python_pyright using the existing configured baseline. Tests keep full architecture/type discipline without newly making the excluded test tree a mandatory strict-Mypy gate. Use the existing applicable syntax checks for supported file grammar; do not label a TypeScript-only check as proof of CJS parsing unless the native adapter admits it. Check changed Markdown with run_checks(scope='targets', targets=[changed Markdown files], checks=['markdown_links']) in configured offline mode. Document/body checks are content capabilities and run through scaffold_artifact/safe_edit_file validation, rather than a filesystem-target run_checks selection.

Capture exact invocation arguments, native prerequisite versions and cached structured run resources in the cycle hand-over. A collected suite, unavailable tool, timed-out run, structural deliverable validator or historical probe does not prove corrected behavior. The deliverables below deliberately use validates=null where their truth requires behavioral evidence rather than file-presence/text assertions.

After each objectively satisfied cycle, transition_cycle(to_cycle=N+1) and refresh context before the next cycle. After cycle 5, request independent Implementation QA; do not enter Validation autonomously. Validation owns one full configured native suite and branch-wide review gates, and reuses fresh cycle evidence unless new changes invalidate it. Repeat broad checks only to resolve a material failure/change, with the reason recorded. Planning itself runs document/traceability checks only.

The work-unit cycle numbers, names, deliverable IDs/descriptions and exit criteria below are projected unchanged to save_planning_deliverables(issue_number=469). The structured store cannot carry dependency/scope/evidence detail; this document remains the executable index for those obligations. Verification of saved parity is required before the Planning commit.


## Dependencies

- C_PROTOCOL → C_COMPLETION → C_ARGFILES → C_STDIN → C_EFFECTS → independent Implementation review → Validation → Documentation; each transition follows the active workflow and authority.
- Existing invocation capture/termination, content scratch, selection admission and ordered fix behavior remain preservation constraints, not new subsystems.
- @co owns issue 474 GitHub wording alignment and separate issue disposition; this is required before acceptance/closure, not a Planning or implementation blocker.



## Risks


### Loaded runtime versus adapter files during coordinated v2 cutover

Use the controlled restart checkpoint in C_PROTOCOL; no native check/test invocations in the mixed interval and no compatibility bridge.


**Consequence:** An unrefreshed server would encode v1 for v2 validators and invalidate GREEN evidence.



### Native grammar or configuration precedence disproves equivalence

Require pinned real-native controls and full/literal selection coverage at each affected package boundary; stop on unsupported encoding instead of truncating or batching.



### Native suite duration or provisioning prevents full Validation evidence

Retain the configured suite and plugin semantics, inspect structured timeout/prerequisite evidence and resolve the causal problem; no quiet switch to serial/reduced execution or skip-based acceptance.





## Milestones

- Planning: scaffold authored document, save and verify identical structured deliverables, check document links, commit 'Planning for #469' and push under standing workflow authorization; request independent Planning QA.
- Implementation: five coherent cycle exits with intended RED, focused GREEN evidence and scoped commits; no full workspace gates before Validation.
- Validation and Documentation: separate issue acceptance evidence, configured broad checks, truthful operator guidance and @co issue disposition alignment.


## Work Units


### C\_PROTOCOL — Coordinated v2 input and PGMCP resource ownership

**Goal:** Complete the indivisible check/test/fix v2 cutover while preserving public MCP parameters, role responses and process safety.


**Cycle Number:** 1



**Owner:** @imp implementer



#### Scope In

All request alternatives in mcp_server/execution/contracts; strict/frozen wire DTOs in execution/models.py, check_selection.py and content_input.py; pure input encoders in execution/protocol.py; narrow directory interface in core/interfaces/execution.py, concrete execution provider, process_runtime.py, check_service.py, test_service.py and fix_service.py; composition in bootstrap.py; config/schemas/adapter_manifest.py and execution/catalog.py; services/check_operation.py and scaffold_operation.py metadata; all nine bundled package request validators and ten role declarations. Migrate tests/mcp_server/fixtures/adapter_process.py, unit/execution service/catalog/selection tests, unit/server/test_bootstrap.py, integration/execution tests, all integration/adapters entry-point fixtures and integration/test_template_activation.py and test_template_proposal.py where they carry v1.



#### Scope Out

Native transport changes, completion/version corrections and cache/report policy changes owned by later cycles. No optional wire context, v1 bridge, public environment-overrides parameter or unrelated template rewrite.

#### Deliverables

##### D1\_PROTOCOL

Complete strict v2 schemas, request encoders, manifest admission and consumer migration across every check/test/fix request alternative, nine packages and ten roles, with unchanged public MCP parameter sets and response shapes.



**Validates:** null



##### D1\_OWNERSHIP

Injected CQS directory description/create/remove and runtime lifecycle with cleanup ownership only after exclusive successful creation; no PGMCP context environment channel.



**Validates:** null



##### D1\_REGRESSION

Durable schema/DTO/entry-point parity and runtime ownership/process regressions, plus fresh-server v2 catalog and public operation smoke evidence.



**Validates:** null



#### Exit Criteria

D1_PROTOCOL, D1_OWNERSHIP and D1_REGRESSION are evidenced by intended RED, passing focused v2 contract/service/runtime/adapter-role tests and changed-file gates; a controlled restart proves the live server admits and invokes v2. No v1 bridge, optional context or environment side channel remains.


#### Dependencies

- Approved Research B1 amendment and Design v1.1; independent Design QA GO on commit 288b77aed9e1e1d566cb353cd77fb17ea2cdafaa.



#### Obligations

- RF4/RF6/RF7; QA P1 and P2. PGMCP creates and owns the directory; adapters receive its location only in required JSON execution_context.scratch_directory.
- describe(UUID) is pure and returns a frozen description; create/remove return None. Exclusive successful creation establishes ownership. Never adopt or remove an existing allocation or shared root.
- Retire active v1 admission and migrate all producers/consumers in one GREEN commit, including truthful contract_version=2 metadata. Shape-only roles validate context without inventing filesystem writes.



#### Verification


##### Meaningful RED before cutover

**Method:** Adapt existing catalog and adapter entry-point tests to assert v1 refusal and required v2 requests through current public boundaries; show intended behavior failures against the coherent v1 baseline via run_tests(scope='targets', tests=['python_tests'], targets=<changed test files>). Missing future helper imports or collection errors do not count as RED.

**Expected Result:** Failures identify the old version admission or context rejection; reuse existing useful tests rather than creating workflow-only tests.



##### Every v2 request variant and context error

**Method:** Run focused unit/execution, integration/execution and all ten adapter-role contract cases after migration; validate the same payloads against the executable schema and DTO/entry point. Cover missing/null/wrong-type/unknown/empty/relative/NUL context and POSIX/drive/UNC lexical cases, plus file-role preparation failure. Use tmp_path-created direct-caller contexts.

**Expected Result:** No native analysis on malformed input; documented invalid_request classifications agree. Usability failures use execution_error; no fallback root. Public check/test/fix metadata reports 2 and existing response assertions remain valid.



##### Resource and process invariants

**Method:** Adapt integration/execution/test_process_runtime.py, test_process_stopping.py and test_content_input.py and constructor/bootstrap tests. Exercise distinct simultaneous invocations with exact JSON propagation and no cross-invocation removal, pure repeated describe, successful create/remove, collision and foreign-root refusal, encoding failure, launch failure, native finish, timeout/cancellation, descendant termination and cleanup failure.

**Expected Result:** No allocation from a query; no foreign/pre-existing removal. Clean up only owned resources after confirmed termination, including preparation/launch failure with no child. Preserve bounded capture, deadlines and independent content-snapshot ownership; cleanup failure is visible. On unconfirmed termination retain and report the owned path; cleanup failure after confirmed finish preserves captured response and prior outcome (including cancellation) without mislabeling termination or claiming rollback.



##### Controlled running-server cutover

**Method:** Do not call native checks/tests during the mixed on-disk v2/in-memory v1 interval. Complete the coordinated source/manifest/fixture cutover, call restart_server(reason='Issue 469 coordinated adapter v2 cutover'), then get_work_context() and health_check(). Verify fresh catalog admission and run a small existing check/test/fix fixture operation before GREEN gates.

**Expected Result:** The running server and bundled packages agree on v2. Restart/bootstrap failure blocks GREEN; recover through the prescribed server tools and diagnostics rather than introducing a v1 bridge or bypassing tests.






#### Stop Conditions

- Stop if any active consumer or request alternative remains v1, or a further public compatibility break is required.
- Stop if ownership cannot be established without adopting an existing path, or process termination remains unconfirmed.
- Stop if restart/bootstrap or a required native prerequisite prevents factual GREEN evidence.



### C\_COMPLETION — Truthful native completion, versions and failure reasons

**Goal:** Prevent metadata/substitute operations from becoming PASS and report supported native prerequisites and substantive failures truthfully.


**Cycle Number:** 2



**Owner:** @imp implementer



#### Scope In

Package-local completion/version/classification seams in bundled_adapters/ruff/check.py and fix.py, mypy/check.py, pyright/check.cjs, pytest/test.py, lychee/check.py and commitlint/check.py and their existing dependency declarations. Preserve actual-version coverage for python_syntax, typescript_syntax and markdown_preflight. Adapt the corresponding tests/mcp_server/integration/adapters files and existing execution presentation tests only where observable envelopes change.



#### Scope Out

No new dependency registry, installer, universal plugin admission or shared native parser. No transport rewrite or cache/report policy change in this cycle.

#### Deliverables

##### D2\_COMPLETION

New Research-proven metadata guards and regressions for Mypy, Ruff lint/format and Pyright, with separately assessed aliases/alternate operations and preserved intentional completion policies.



**Validates:** null



##### D2\_VERSIONS

Package-local observed-versus-declared native prerequisite checks and dependency_unavailable results before version-dependent behavior or mutations.



**Validates:** null



##### D2\_FAILURES

Substantive access/configuration/usage/execution and missing-negative-evidence classifications, independent of verbose chatter, with retained native facts and bounded useful diagnostics.



**Validates:** null



#### Exit Criteria

D2_COMPLETION, D2_VERSIONS and D2_FAILURES have intended RED and passing focused affected adapter/presentation tests plus changed-file gates; the new Ruff and Pyright guards are explicit and intentional native outcomes remain unchanged.


#### Dependencies

- C_PROTOCOL



#### Obligations

- RF2/RF3/RF5; Research B3/B5/B6; QA P3. Read package dependency declarations as version SSOT; unsupported/unreadable prerequisites fail before version-dependent parsing and source mutation.
- New guards are required for Mypy --help, Ruff lint --help/--show-files, Ruff format --help and Pyright --help. Retain valuable Pytest/Lychee/Commitlint/Ruff-fix guards; assess parser-admitted aliases and alternate modes separately.
- Preserve intentional Ruff --exit-zero, Pytest collect-only and exit 5. Guard effective caller/config/environment/response-file sources where the native parser supports them.



#### Verification


##### False PASS routes and preservation

**Method:** Use existing real-native adapter entry-point tests for each proven metadata route; assert unsupported_input rather than passed, paired protocol status/exit and no analyzed-result claim. Test effective indirect routes when supported. Keep Ruff exit-zero and Pytest collect-only/exit5 controls in the focused selection.

**Expected Result:** RED reproduces the original false PASS or wrong classification; GREEN refuses the operation while the intentional controls retain their established semantics.



##### Prerequisites before effects

**Method:** Run package entry-point mismatch/unavailable/unreadable-version cases using controlled dependency/version fixtures and at least one real installed-version control per guarded package. For fix routes, observe unchanged selected bytes under prerequisite failure.

**Expected Result:** Actual and expected versions are useful; unsupported versions yield dependency_unavailable before parsing or edits. No second version table or automatic install; stdlib runtime facts stay factual.



##### Failure meaning and evidence

**Method:** Adapt Ruff/Mypy/Pyright/Pytest/Lychee native error tests with controlled access/config/usage fixtures and verbose/nonverbose counterparts; use supported-platform access fixtures and report unproved platform cases explicitly. Retain malformed/missing result evidence tests.

**Expected Result:** The same substantive failure retains the same class and useful message regardless of chatter; no false PASS from absent negative evidence. Platform prerequisite failures are explicit, not skip-based success.






#### Stop Conditions

- Stop if effective native argument/config precedence cannot be established for a claimed guard.
- Stop if a supported-version decision differs from the existing declaration or requires new installation policy.
- Stop if a proposed classification invents a public status/reason enum or hides a required prerequisite failure.



### C\_ARGFILES — Single-run native argument files for Ruff, Mypy and Pytest

**Goal:** Remove Windows target-vector launch limits without changing full native analysis/session semantics.


**Cycle Number:** 3



**Owner:** @imp implementer



#### Scope In

Ruff check lint/format and fix, Mypy check and Pytest test argument-file translation in their package entry points; tests/integration/adapters/test_ruff_checks.py, test_ruff_fixes.py, test_mypy.py and test_pytest.py under tests/mcp_server. The files remain in the v2 supplied invocation directory.



#### Scope Out

No target batching, universal selection filter, command-line truncation, workspace fallback, generic response-file parser or new process/session framework.

#### Deliverables

##### D3\_ARGFILES

Native @file transport for Ruff lint/format/fix, Mypy and Pytest using the supplied context, preserving full ordered native arguments and one invocation.



**Validates:** null



##### D3\_EQUIVALENCE

Durable real-native large-selection and literal/option/discovery/exclusion regressions, including cross-file Mypy semantics, Pytest session preservation and Ruff fix effects.



**Validates:** null



#### Exit Criteria

D3_ARGFILES and D3_EQUIVALENCE have intended launch-limit RED and passing affected Ruff/Mypy/Pytest real-native transport and preservation regressions plus changed-file gates; one run and complete selection are evidenced rather than inferred from an aggregate PASS.


#### Dependencies

- C_PROTOCOL
- C_COMPLETION



#### Obligations

- RF1/RF2/RF6; Research B2. Encode the whole already-admitted ordered argument vector and target selection using each pinned native @file grammar; one analysis/session per role.
- Preserve configured empty-selection discovery, native exclusions, option order, literal paths, Mypy whole-program imports and Pytest plugins/xdist/fresh --native child, collect-only and exit5.
- Refuse unrepresentable response-file input explicitly; caller-controlled response files cannot bypass role/selection guards. Fix admission completes before any edit and ordered failure/partial mutation remains truthful.



#### Verification


##### Oversized native selections

**Method:** Run focused real-native adapter tests with Windows explicit selections whose old encoded command line exceeds 32767 UTF-16 code units, plus small controls. Place distinguishing findings at early/middle/late selected paths and verify returned complete target/coverage facts. Observe one native analysis/session at the process boundary and cross-file imports/session fixtures so batching cannot satisfy the assertions.

**Expected Result:** Intended RED fails due to the old launch limit. GREEN launches successfully and reports every selected target truthfully with late findings retained; source analysis/session behavior stays coherent.



##### Pinned grammar and configuration equivalence

**Method:** Compare native results on spaces, Unicode, metacharacters, leading-dash/literal path cases supported by the filesystem, native exclusions, empty configured discovery and ordered options. Cover response-file newline/ambiguous-line limits and indirect guard attempts. Use existing temporary native project fixtures, not the historical probe as a test suite.

**Expected Result:** No quoting loss, trimming, silent omission or rewritten discovery. Unsupported encodings are unsupported_input before native analysis; native config/exclusion semantics remain authoritative.



##### Fix and session preservation

**Method:** Run existing Ruff fix changed/unchanged/admission/failure controls and Pytest plugin/xdist/import/collect-only/exit5 tests with transport enabled; retain meaningful partial-mutation and ordered-stop tests.

**Expected Result:** No pre-admission source change, no retry/rollback fiction and no duplicate native session; existing useful native policies still pass.






#### Stop Conditions

- Stop if the pinned native @file grammar cannot faithfully encode an admitted vector; report the specific limitation instead of dropping targets.
- Stop if Pytest loses its established process/plugin/session boundary or Mypy becomes multiple analyses.
- Stop if fix transport mutates sources before all-input admission.



### C\_STDIN — Native stdin selection for Pyright and Lychee

**Goal:** Move complete selected filenames off the command line while respecting native input-channel ownership.


**Cycle Number:** 4



**Owner:** @imp implementer



#### Scope In

Pyright check.cjs '-' filename input and Lychee check.py '--files-from -' selection; existing test_pyright.py and test_lychee.py; snapshot/content checks affected by Lychee filename transport.



#### Scope Out

No forced takeover of a caller/config-owned Lychee files-from channel, content-stdin replacement, new base/remap policy or hidden discovery fallback.

#### Deliverables

##### D4\_STDIN

Complete Pyright and available-channel Lychee native stdin filename transport with correct configured-discovery and input-channel ownership behavior.



**Validates:** null



##### D4\_LIMITS

Real-native large/literal/exclusion/discovery and Lychee content-snapshot regressions, plus explicit conflicting-channel and unrepresentable-input limitations.



**Validates:** null



#### Exit Criteria

D4_STDIN and D4_LIMITS have intended RED and passing focused Pyright/Lychee native transport, discovery, input-channel and snapshot tests plus changed-file gates; no claim of universal large-selection support is made for Lychee's occupied-channel fallback.


#### Dependencies

- C_PROTOCOL
- C_COMPLETION
- C_ARGFILES



#### Obligations

- RF1/RF2/RF6; Research B2. Pyright nonempty selection uses native filename stdin; empty selection retains native configuration discovery.
- Lychee uses stdin filenames only when that effective native channel is free. If user/config files-from already owns it, preserve the admitted argv route and document its launch-size limitation; do not overwrite user intent.
- Escape literal paths using pinned native grammar; preserve content-snapshot base/remap, no dropped blank/comment-like entries or newline ambiguity. Adapters never allocate or clean the PGMCP root.



#### Verification


##### Complete real-native selection

**Method:** Run affected Pyright/Lychee entry-point tests with old oversized Windows argv selections and small native controls, early/middle/late findings, Unicode/spaces/metacharacters and native exclusions; observe one execution and full returned selection/coverage.

**Expected Result:** RED captures the old oversized launch failure. GREEN retains all paths/results and native configured discovery, without multiple analyses.



##### Input channel and literal grammar

**Method:** Exercise Pyright empty-selection control, Lychee effective user/config files-from precedence and original argv route, newline/comment-like filenames and content snapshot base/remap. Lychee fixtures use local offline links and deliberate local destinations.

**Expected Result:** No empty stdin replacing discovery, no stolen native channel or silently filtered paths. Supported encodings preserve literals; unsupported cases and the remaining conflicting-channel launch-size limit are explicit.






#### Stop Conditions

- Stop if effective files-from ownership or native line encoding is uncertain for a claimed supported case.
- Stop if filename stdin changes content-mode semantics or base/remap behavior.
- Stop if a test requires live external network or an undisclosed dependency skip to appear green.



### C\_EFFECTS — Proportional native cache and supplemental-output policy

**Goal:** Align existing write guards with accepted local-use policy while protecting requested operation, selected sources and captured results.


**Cycle Number:** 5



**Owner:** @imp implementer



#### Scope In

Existing Ruff check/fix and Mypy cache/report guards, Lychee cache/cookie/state guards and corresponding tests; retain and sharpen contract-changing refusals in those packages only where Design identifies them. Reuse existing real-native effect fixtures and separate ordinary output cases from refusal cases.



#### Scope Out

No enforced universal cache destination, OS isolation, arbitrary-host escape suite, environment sanitation, permissions manifest or automatic deletion of native side outputs.

#### Deliverables

##### D5\_EFFECTS

Ordinary native cache/cookie/temporary-output and compatible Mypy supplemental-report behavior admitted under B4, with contract-changing routes still refused.



**Validates:** null



##### D5\_REGRESSION

Real-native CLI/config/environment effect and result-capture coverage where supported, source-byte preservation or intentional Ruff fix effects, and durable refusal regressions without a general sandbox suite.



**Validates:** null



#### Exit Criteria

D5_EFFECTS and D5_REGRESSION have intended policy RED and passing focused affected native effect/refusal tests plus changed-file gates; the claimed permitted/refused behavior matches B4 with no sandbox or universal destination guarantee.


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

**Method:** Adapt all-write-refusal tests to use native-supported CLI/config/environment precedence. Deliberately allocate cache/report/cookie destinations in tmp_path outside the selected source subtree; observe actual effects and returned native diagnostics/status, with disabled/default controls where relevant.

**Expected Result:** RED shows overbroad refusal. GREEN permits the claimed ordinary effects and compatible reports; check/test source bytes remain unchanged, and Ruff fix changes only its admitted targets.



##### Contract-changing refusal and failures

**Method:** Keep useful existing output-redirection, source replacement, metadata/replacement operation and installation refusals; test effective indirect sources where admitted. Cover missing/unwritable effect destinations without treating location alone as unsafe.

**Expected Result:** Requested operation/result capture remains correct; refusal occurs before unwanted source effects. Native operational failures have useful reasons, and no returned success implies side-output rollback.






#### Stop Conditions

- Stop if a report suppresses required status/diagnostic capture or an admitted native option substitutes operation/source selection.
- Stop and reopen the affected strategy if evidence demands a general permissions/sandbox policy rather than a targeted contract guard.
- Stop if the implementation treats issue 474's superseded fixed-destination wording as binding over approved B4.




## Phase Deliverables





### Validation

#### V\_NATIVE

One full configured native python_tests run in Validation through run_tests(scope='configured', tests=['python_tests']) with existing configured arguments/prerequisites and factual outcome; do not force an alternate serial or reduced suite to manufacture success.



**Validates:** null



#### V\_GATES

One branch-wide review pass in Validation: run_checks(scope='branch', checks=['python_format','python_lint','python_pyright']) for admitted Python targets, and run_checks(scope='configured', checks=['python_types']) for the existing strict production-only Mypy baseline. Apply existing admitted CJS/JSON/Markdown obligations to changed files; record unsupported grammar/gate coverage honestly.



**Validates:** null



#### V\_ACCEPTANCE

Validation report maps E469-1..4, E474-1, E475-1 and E-CROSS separately to durable tests and fresh receipts, including all nine packages/ten roles/thirteen capabilities applicability and explicit limitations; independent QA review requested.



**Validates:** null







### Documentation

#### DOC\_GUIDANCE

Update active protocol/execution/tool guidance for required v2 context, direct-caller/custom-adapter migration, actual metadata version, lifecycle ownership, native caches/reports, supported versions and per-tool transport limits; retire active v1 usage without rewriting historical findings.



**Validates:** null



#### DOC\_DISPOSITION

Retain separate 469/474/475 acceptance/disposition and link @co alignment of issue 474's superseded wording before acceptance/closure. Document accepted host-account access, scoped guarantees and remaining Lychee input-channel limitation honestly.



**Validates:** null








## Related Documents

- [Approved Research](research.md)
- [Approved Design](design.md)
- [Historical effect probe](effect-probe.md)
- [Architecture Principles](../../coding_standards/ARCHITECTURE_PRINCIPLES.md)
- [Quality Gates](../../coding_standards/QUALITY_GATES.md)
- [Type Checking Playbook](../../coding_standards/TYPE_CHECKING_PLAYBOOK.md)
- [Execution/runtime seams](../../../mcp_server/execution)
- [Native adapter regression suite](../../../tests/mcp_server/integration/adapters)

