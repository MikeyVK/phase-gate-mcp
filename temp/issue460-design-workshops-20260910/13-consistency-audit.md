<!-- C:\temp\pgmcp\temp\issue460-design-workshops-20260910\13-consistency-audit.md -->
<!-- template=design version=5827e841 created=2026-09-10T09:24Z updated= -->
# Issue 460 — Cross-package proposal audit

**Status:** PRODUCER AUDIT — not independent QA, not Design approval  
**Date:** 2026-09-10  
**Scope:** Temporary W01–W12 proposals and their seams with frozen Research/current Design  
**Entry point:** [Review guide](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/00-README.md)

## 1. Method and authority

**Canonical pass — 2026-09-12, after W12 approval:** DI-08 is now consolidated in
design-test-architecture.md. Three bounded findings-only audits plus producer source
verification found stale active naming/fingerprint/encoding/args/intake/status wording;
the canonical owners and hub were corrected without changing approved behavior. Exact
remaining schema-resource identity, JSON Schema dialect/support and full test DTO
consolidation are tracked in design.md's canonical closeout audit. They are not labelled
mere test work. Frozen inventory recount: 128 unique runtime rows (126 consumers plus
two governing sources), 151 unique test/helper rows; routing totals 22 findings,
44 strategy rows, 19 invariants, 23 expected results. Local file links checked for the
changed canonical files; new DI-08 has all fourteen required sections. No full per-test
semantic audit, native/process test, wheel build or independent review was performed.

**Current-status clarification — 2026-09-12:** The earlier preparation snapshots below
are chronological evidence, not current open decisions. W07/W08 have bounded independent
QA approval; W09/W10/W11 are human-approved and canonicalized. W12 now follows direct
native fixes without transaction/rollback, no semantic model-example validation, explicit
native args and approved effective-config admission. The Design hub owns current status.
The 2026-09-12 W12 refresh corrected obsolete native-proposal/recovery and default
materialization references in that temporary proposal. The W11 carrier map was aligned
to canonical DI-03 §7.8 and consolidated. No complete 151-test semantic re-audit,
whole-canonical-set audit, native conformance or independent review is claimed here.

This audit records work actually performed while preparing the remaining workshops. It is not a new canonical Research finding ledger or an executable validation framework.

The passes were:
1. Authority/scope: read phase instructions, Research/intake, the Design hub and package decisions; identify superseded navigation and preserved boundaries.
2. Consumer/data contracts: follow content, schema, profile, role invocation, operation result, cache and presentation; follow testing and fixing as distinct consumers.
3. Adversarial examples/removal: reason through native exclusions, missing dependencies, default interactions, stale writes, process failure, partial fixes, wheel omission and active instruction drift.
4. Artifact/source integrity: verify local references, proposal structure, template ID bounds, header arithmetic, census structure and scoped file changes.

Two bounded delegated read-only reviews supplied findings only. Their observations informed the corrections below; neither review granted GO or replaced independent @qa.

## 2. Material corrections made during the passes

| ID | Counterexample or defect in the first proposal | Correction in this bundle | Owner |
|---|---|---|---|
| A-01 | Per-tool failure text hides a structured error; nullable enum projection is not admitted | Existing global constant failure wording plus ordinary scalar/collection projection; no invented presenter branch support | W01 |
| A-02 | Public raw stderr contains a host path after adapter crash | Original private-log proposal withdrawn after human review; W01-F now approved: relative operation fields, bounded on-demand cached diagnostics with incidental host paths, no local-only guarantee | W01/W02; canonical DI-04 §4.6 |
| A-03 | Required native provenance lacked a field in the closed scaffold payload | W02-F now approved: external_tools is in ordinary role results and the canonical scaffold table; invalid_request unchanged | DI-05 and all role consumers |
| A-04 | One read-only catalog interface still exposes unrelated roles | Check/Test/Fix reader protocols over one catalog; consumers receive only needed roles | W02 |
| A-05 | Trust config initially relied on an unspecified optional settings file | W02-B now approved: required adapters.yaml under existing configroot, central loading, no duplicate trust/native settings/manifest authority | DI-05; DI-06 distribution obligation |
| A-06 | A failed member and an unavailable/unstarted member have ambiguous overall status | W03 has approved aggregation; W04 v0.2 reopens its exact summary against test-request completeness, preserving negative facts and DI-04's different summary | W03/W04 |
| A-07 | A suite or fix never started but its public result has only adapter alternatives | Consumer-only not_executed with not_started/interrupted; no fabricated native response | W03/W04/W05 |
| A-08 | Arbitrary test selector strings conceal path components | Trusted adapter interprets and contains its native selectors before execution; no generic parser or sandbox claim | W04 |
| A-09 | A fix says it addresses a capability, but its selected verifier is absent or selection-only | Exact addresses foreign-key coverage and content-capable verification admission | W05 |
| A-10 | Routine temp cleanup destroys the only evidence for a partially applied fix | Recovery state proposed under resolved_server_root/fix-recovery, not temp; durable prepare before writes and byte-based recovery observations | W05 |
| A-11 | An unresolved fix recovery record is ignored by a later safe edit | Explicit conditional narrow overlap-reader dependency and recovery_pending admission error; requires W01/W05 review | W01/W05 |
| A-12 | Every default is valid individually but insertion triggers dependentRequired/conditional invalidity | Validate the complete effective object; classify insertion-only failure as template/default preparation defect | W06 |
| A-13 | A selected profile binding changes while sf remains equal | Exact declarative pf projection and explicit source-suite-only sf promise; no native-config/adapter-code hash leakage | W06 |
| A-14 | Input schema is constructed once but an outer decorator regenerates an older static schema | One EffectiveInputContract supplies exposure, runtime validation and input-error schema feedback | W06 |
| A-15 | Package-owned examples quietly become mandatory permanent validation fixtures | Examples optional; validated when supplied; no mandatory example registry or hardcoded all-template dictionary | W07/W12 |
| A-16 | Ordinary description with triple quotes creates invalid source | Language-correct escaping is renderer-owned; only explicitly marked source fragments are caller-native code | W07 |
| A-17 | Model-example validation introduces execution or interpretation complexity | Human withdrew semantic example validation; no adapter/profile obligation remains | W07/W09 |
| A-18 | WorkUnit projection reads undefined nested stop_go and cycle number | Direct typed exit_criteria, optional operational_cycle_number, exact Deliverable/ValidationRule projection | W08/W11 |
| A-19 | Issue/PR body without H1 is sent to full-document profile | Explicit body-vs-document capability/profile mapping and warning-only link limitation | W08/W09 |
| A-20 | Official packages are discovered again as workspace extensions in self-hosting | Approved direct mcp_server/bundled_adapters authoring/distribution versus resolved_server_root/workspace_adapters; no asset copying | W02/W10 |
| A-21 | Active host instructions are mistaken for their authored source | docs/agents/<host> → active mapped files → packaged assets; no backward editing authority | W11 |
| A-22 | Replacing the old test harness omits pytest plugin registration callers | Explicit supporting conftest ownership without silently changing the frozen 126/151 census | W12 |
| A-23 | Compact enum notation breaks Markdown table columns | Escape in-cell alternatives while preserving real table delimiters; include deterministic table check | Whole bundle |
| A-24 | Proposed python_pytest_integration is 25 characters, not 24 | Use the explicit framework-qualified pytest_unit_test / pytest_integration_test pair; keep the approved 24-character limit unchanged | W07 |
| A-25 | Reusing late byte checks is incorrectly described as protection from every external write | Preserve DI-04's non-atomic compare/replace limitation in fix apply and rollback; promise refusal of observed changes | W05 |
| A-26 | Consumer operation error_code is named but not bounded | RunChecksErrorCode approved; W04 v0.2 requires revised exact test DTO/error/exit declarations after result semantics are reviewed; fix/recovery proposals remain separate | W01/W03/W04/W05 |

“Correction” means the **draft** describes the issue accurately, not automatic approval. Human approval on 2026-09-10 now covers W01-A–F. W02 is subsequently approved, including native provenance (A-03) and trust (A-05). W05 recovery (A-10/A-11), DTO examples (A-17) and other workshop proposals remain open.

## 3. Existing-source discrepancies not edited

| Observation | Interpretation and safe handling |
|---|---|
| README v1.19 says Design paused for the 2026-09-05 amendment | Form/navigation authority is valid; gate wording is stale against latest Research/user GO. Record for later navigation correction, not a renewed Design veto |
| Historical research/Design tables still contain old gate/mode/workshop descriptions | Read with their current amendment/decision sections. Do not globally replace history or treat every historical term as active runtime authority |
| Hub/README package-status wording lags closed header/checked-write workshops | Temporary guide routes remaining work from actual detailed decisions, not stale short status text |
| Some manifest identity/provenance rows still say id or gate-set | Actual manifest template_id and check/profile vocabulary remain authoritative; future canonical integration corrects active wording only |
| Conversation recollection says Worker removed; canonical F-14/catalog retains it | Preserve canonical retain/adapt; W07 explicitly asks for confirmation, with no silent removal |
| Universal persisted first-line metadata and conventional commit subject are different requirements | W08 proposes a persisted-draft/downstream-content boundary; do not claim the whole file is directly a Git message |
| Catalog instruction-source direction is reversed relative to current generator/reference | W11 uses directly inspected docs/agents authority; frozen Research not rewritten |
| Supporting conftest dependencies are outside current named census | W12 identifies them and primary integration ownership; no false claim of an updated Research census |

Source staleness is not a blanket excuse to overrule Research. A material incompatibility that cannot be resolved within approved strategy requires explicit human direction at that boundary.

## 4. Remaining review decisions and honest proof limits

Closed on 2026-09-10: W01-F diagnostic disclosure, integrated into canonical DI-04 §4.6, DI-05 and the hub. Existing bounded cached diagnostics may contain incidental absolute paths; operation fields remain relative. No new private archive, secrets permission or redaction guarantee. Research remains frozen. Subsequent W01-A–E and W02 approvals are recorded below; W05 remains unapproved.

| Decision / limit | Why not considered closed | Prepared route |
|---|---|---|
| Native selection/empty/incomplete meaning | Scope and tool semantics differ; no universal participation proof | W03/W04 exact proposals |
| Recoverable multi-file fixing | Extra state and overlap admission are substantial; not per-file atomicity | W05 bounded contract or explicit reduction of supported scope |
| Schema-valid source-fragment promise | JSON string shape is not native syntax validation; Research wording may require explicit interpretation | W07 distinguishes ordinary text defects from native fragments; no automatic Research edit |
| DTO-example input/validation | Withdrawn by human on 2026-09-11 | Preserve authoring/rendering only; no model-validation promise |
| Markdown body / TypeScript / commit capability details | All retained package profiles need honest executors and native evidence | W09 full consumer table; final installable config not claimed ready |
| Exact native setting deltas | Current native and isolated-gate values differ | W09 explicit disposition and owner review |
| Worker and tracking downstream intent | Existing authority/conversation or file/consumer seam needs agreement | W07/W08 concrete questions |
| Candidate profile/config interaction | Template renewal cannot silently overwrite native/custom configuration | W10 explicit admission reader and blocked-activation example |
| Operational Planning projection | Document prose and saved CycleModel are separate operations | W08 typed exact projection; parity proof before promotion |

These open points do not prevent preparing downstream proposals. They **do** prevent presenting the entire canonical Design as complete or sending an implementation plan through a hidden approval shortcut.

## 5. Traceability and census checks

The existing [catalog](C:/temp/pgmcp/docs/development/issue460/template-suite-catalog.md) remains SSOT for paths. A read-only structural check of its runtime and test ledgers found:

- 128 unique runtime-ledger paths = 126 consumers + 2 governing-standard sources.
- 151 unique test/helper-ledger paths.
- No duplicate path within those ledgers.
- All referenced ledger files exist.

This is a **path/count/uniqueness check**, not a fresh semantic review of all 151 tests or a new workspace-wide discovery census. Supporting dependencies are named in W12 instead of altering totals.

[W12's obligation table](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/12-test-architecture-integration.md) maps all 22 finding IDs, including F-14A/F-14B and deferred F-18. The canonical intake retains 44 strategy rows, 19 invariants and 23 expected results. The workshop guide routes every DI-01–DI-08 owner plus shared architecture/removal/research-fidelity responsibilities. This is complete **proposal routing**, not proof that all canonical obligations are satisfied.

## 6. Artifact verification record

The following record describes the initial completed bundle preparation, before W01-F approval. These checks inspect documents, not runtime behavior. Subsequent focused integration evidence is recorded separately below.

**Verification state:** document checks completed; runtime proof remains explicitly excluded.

- Fourteen Markdown files exist: twelve proposals, guide and audit.
- All 168 required workshop sections are present; every workshop is labelled PROPOSAL.
- Markdown table columns and all five code-fence pairs are balanced.
- All 90 local file links resolve to existing files and use absolute targets. Two additional links cite the official JSON Schema sources used for the limited standards check.
- No unfinished drafting marker remains. Ordinary references to obsolete placeholder behavior were manually distinguished from unfinished content.
- Proposed retained IDs stay within 24 characters after correcting the overlong integration-test name. A valid 11-character SemVer, maximum 24-character ID and two 16-character fingerprints produce exactly 100 characters in the longest approved HTML-comment header form.
- At preparation completion, PGMCP git_status reported zero modified tracked files and 2,900 untracked files, versus 2,886 at entry: this bundle's fourteen new files. Existing untracked canonical Design files and earlier probe material were not edited. Nothing was staged or committed during preparation.

The final findings-only reread confirmed the bounded semantic corrections above; the late ID-length correction was separately checked by exact character counting. These checks validate artifact structure and stated contracts, not executable conformance.

### W01-F approval integration — 2026-09-10

The user-approved disclosure policy is integrated into DI-04 v1.29, DI-05 v0.67 and
the hub v1.57. W01, W02 and this guide/audit are synchronized; W01-A–E, W02-F and W05
remain proposals. Research, runtime/config/tests, existing untracked canonical documents
and prior probe material are unchanged.

Focused document checks cover these three canonical documents and all fourteen temporary
documents: 251 local file links (with line/fragment suffixes handled), 111 table blocks
and balanced code fences. One pre-existing unescaped union separator in DI-04's table
was escaped without changing its meaning. The scoped wording review found no remaining
active blanket prohibition of incidental cached diagnostic paths in the reviewed Design
documents or temporary bundle; historical decision entries remain historical.

Before the scoped documentation commit, PGMCP git_status showed exactly the three
intended tracked Design files modified and the same 2,900 untracked files. The temporary
bundle remains uncommitted. These are documentation checks, not runtime conformance,
security certification or independent QA.

Scoped commit: `491c4879`. The PGMCP commit tool included the three selected Design
documents and its automatic `.pgmcp/state.json` metadata update. No phase transition
was requested; post-commit status reports zero modified tracked files and the same
2,900 untracked files. The temporary bundle remains outside the commit.

### W01-A–E approval and W02 review entry — 2026-09-10

Human approval closes W01's operation-result choices. DI-04 v1.30 records the normal
failure result, typed fields and ownership; DI-05 v0.68 and hub v1.58 reference it.
W02 native-tool provenance, final shared capture declarations, required-null resource
serialization and W05 recovery remain explicitly routed, not silently approved.
The concrete cache currently omits nulls: real resource round-trip evidence is required
for the already selected nullable V3 contract, not a new presenter framework.

W02 remains a proposal and now includes a consumer authority map and illustrative
package/trust YAML. Its IDs are examples, not an approved official package inventory.
Focused checks covered 17 documents, 253 local file links, 114 table blocks and balanced
fences, with no remaining structural issues. The approval-status search found no active
claim that W01-A–E still awaits human approval in the reviewed mutation/hub/bundle scope.
Before commit, only the three selected tracked Design documents were modified; the
2,900 pre-existing/uncommitted paths remained outside the staged document write-set.
Research, production, tests and configuration were not edited or executed.

Scoped W01 commit: `26bc5922`. The PGMCP commit tool also recorded its automatic state
metadata update. Post-commit status shows zero modified tracked files and the same
2,900 untracked paths; no phase transition was requested. W02 remains temporary.

### W02 partial approval and two open clarifications — 2026-09-10

Human approval covers W02-A/C/D/E; canonical DI-05 v0.69 and hub v1.59 record the
accepted source/file/capability/fingerprint and interface boundaries. W02-B trust
configuration and W02-F native-tool provenance return field remain open. The revised
temporary proposal names adapters.yaml under the existing configroot; no config file
or runtime behavior has been created. Native identities are clarified as ordinary cached
run evidence, not a new query tool or mandatory extra call. The template manifest
inventory and artifacts.yaml location authority remain unchanged; Research is frozen.

Focused document checks: 17 files, 256 local file links, 115 balanced table blocks and
balanced fences; no structural issues found. Commit 159f87d3 contains only the selected
DI-05/hub documents plus the PGMCP tool's automatic state metadata. No runtime config,
production/test changes or phase transition; trust/provenance clarifications stay proposals.

### W02 closure and W03 review entry — 2026-09-10

The subsequent human agreement closes W02-B/F. Earlier partial-approval entries above
are chronological snapshots, not current open decisions. DI-05 v0.70 defines required
adapters.yaml under the existing configroot and typed external_tools in ordinary role
results. Both the earlier closed scaffold field list and its four-alternative table
are amended; invalid_request remains minimal. DI-04 v1.31 and hub v1.60 consume this
approval. W01/W03/W04/W05 references and W10's config-distribution obligation are aligned.
No actual config file, adapter execution, native dependency installation or new query
tool was introduced. W03 now highlights the mixed-profile not_applicable/incomplete
trade-off for human review rather than treating it as an approved default.

Focused checks cover 17 documents, 256 local file links, 115 table blocks and balanced
fences, with no structural issues. Active-contract searches found no remaining old
decision/evidence-only scaffold promise or open W02 trust/provenance claim in the
canonical DI-05/DI-04/hub scope. Historical version records remain unchanged. Runtime,
Research and independent conformance evidence remain outside this documentation change.

Scoped W02 completion commit: 07f9418e, containing the three selected Design documents
plus the PGMCP commit tool's automatic state metadata update. Post-commit status reports
zero modified tracked files and the same 2,900 untracked paths. No phase transition.

### W03 approval and W04 review entry — 2026-09-10

Human approval closes W03 in full. DI-05 v0.71 §7.14 consolidates existing scope,
profile, native-first and single-invocation decisions; the caller timeout override is
the explicit additional control, not a changed internal termination budget. The hub
v1.61 and review guide now advance to W04. Earlier W03 proposal labels above are
chronological snapshots, not current open choices. W04 identifies only test-specific
selection/options/outcome decisions and cites the current RunTestsInput preservation
surface. No test/fix proposal is approved by W03 approval.

The integration makes early missing run summary explicitly required null alongside the
operation error, avoiding an invented passing/incomplete result before selection exists.
Actual frozen DTO/detail declarations, shared capture/null preservation, registered
schema evidence and native conformance remain open integration obligations. Illustrative
adapter IDs/timeouts do not decide W09's shipped capability inventory. Research,
runtime/config/tests and existing unrelated untracked files remain unchanged.

Focused artifact checks covered 17 documents, 259 local file links, 117 table blocks
and balanced fences, with no structural issues. The tracked diff contains only DI-05
and the hub; diff whitespace checks pass (only repository CRLF-conversion notices).
These are document checks, not runtime or independent QA evidence. Scoped commit
c2263f8f contains the two selected Design files and the PGMCP commit tool's automatic
state metadata update. Post-commit status: zero modified tracked files and the same
2,900 untracked paths. No phase transition was requested.

### W04 preservation-led revision — 2026-09-10

The human directed review of existing run_tests contracts against run_checks rationale,
not automatic inheritance or an unrelated test design. Temporary W04 v0.2 now starts
with direct current-code/test evidence. Current run_tests supports path (files, directories,
multiple selectors and native node IDs) versus full; no branch test scope exists. Markers,
last-failed, coverage and collection can accompany full or path selection. The old success
field follows operational-error classification, not exclusively passing tests; native exit
1 and 5 are non-operational-error results in the current runner policy.

Withdrawn producer proposals: scope=suites, workspace-options prohibition, automatic
empty-to-failed conversion and mixed requested collection/execution-to-incomplete solely
because activities differ. The revised scope=targets/workspace, suite selection and native
options composition is proposed, not approved. Exact test result/exit/success declarations
remain open; no inferred branch affected-test selection, mandatory expansion/fresh fields
or universal framework summary is introduced. Historical preparation entries above are
not authority to restore withdrawn choices.

Only W04, this audit and the temporary guide change. Research and canonical Design remain
frozen/unchanged respectively; production/tests/config are not edited, no tests/native tools
are executed, and no commit or phase transition is requested. Focused structural checks
cover 17 documents, 272 local file links, 121 table blocks and balanced fences, with
zero issues. Post-edit status remains zero modified tracked files and 2,900 untracked
paths. These checks do not prove runtime/schema/native conformance. W04 still requires
workshop decisions before W05 begins.

### W04 public input/exposure approval — 2026-09-10

The human approved the concrete startup-schema example: flat tests IDs and args mapped
to selected execution IDs. DI-05 v0.72 §7.15 and hub v1.62 now own that approval. The
test capability options_schema proposal and nested SuiteRequest/options/test_ids route
are explicitly superseded; W02/W04/W06 temporary references and this guide are aligned.
Historical entries above do not restore those proposals. No args field is added to
scaffold, safe-edit, run_checks or apply_fixes; Research remains unchanged.

Structural/recipient checks precede execution, but native switch prevalidation is not
mandatory. Native usage failure is not automatically a malformed internal request;
exact test outcome/exit classification remains open. Role/scope safety remains binding.
Test configuration root names/full transport/result DTOs are not approved by a public
schema fragment. Separate native config/defaults and configured all-active semantics
remain binding. No arbitrary-argument native knowledge is added to generic server code.

Focused artifact checks cover 17 documents, 275 local file links, 121 table blocks and
balanced fences, with zero structural issues. Cross-reference searches retain old
options_schema/SuiteRequest mentions only as explicit supersession/history. No runtime,
native invocation, test/gate run or independent QA evidence is claimed. Scoped commit
c8c5bd0b contains the two selected Design documents and PGMCP's automatic state metadata
update. Post-commit status has zero modified tracked files and 2,900 untracked paths.
No phase transition was requested.

## 7. Evidence not obtained in this task

No adapter/native execution, application tests, quality gates, actual JSON Schema compiler conformance, worker-process tests, stale-write/recovery fault injection, wheel build, install/upgrade, cross-platform support proof or independent QA was performed. Code/config inspection shows current behavior/seams; proposal examples do not prove future behavior.

No final native package versions, full language-support claim, 126/151 cycle assignment, or implementation stop/go verdict is invented. Native conformance, bounded write sets, preserved behavior, rollback points and independently proved check/test/fix migrations remain mandatory later.

## 8. Review hand-over

**Scope:** Whole remaining Design proposal set; approved Research and canonical decisions preserved except explicitly proposed review amendments.  
**Deliverables:** W01–W12 and guide; all temporary and uncommitted.  
**Evidence:** Source reading, findings-only cross-review, counterexamples and document checks above.  
**Open work:** Human decisions in §4, canonical integration and independent Design review.  
### W04 consolidation — 2026-09-10

Current state supersedes the chronological snapshots above: W04 v0.8 is one total-review proposal. D-ADAPTER-22/23/24 preserve operational success, remove generic verbose across consumers, retain passed, and use configured/targets for run_tests. DI-05 v0.74 and hub v1.64 contain only approved corrections; tests.yaml, the exact internal request and output/error proposal remain unapproved. W03/W05 no longer advertise a generic verbose field; their exact args routing remains explicit follow-up. Research, runtime code, tests and actual configs remain unchanged.

Historical obligations, corrected by the explicit-workspace amendment below: no generic verbose; configured uses native discovery; shared InvocationCompleted must not be confused with a new completed domain verdict. No silent broadcast of native args into mutation profiles. No runtime/native/schema conformance claimed by document checks.

**Review request:** review the consolidated W04 proposal as a whole; remaining approval is not inferred from consolidation.

### Approved default-argument amendment — 2026-09-10

The human closed W04, then explicitly distinguished fixed-profile mutation consumers from interactive check/test/fix callers. DI-05 §7.16 (v0.75), DI-04 v1.32 and hub v1.65 are authoritative: required binding default_args; no public mutation args/verbose; omitted recipient uses defaults, explicit list replaces them including []; no merging/broadcast; direct manager-owned args_source/effective_args. W03/W04/W05 records and guide are aligned. Prior chronology asserting omitted args always means no extra arguments or W04 still needs approval is superseded.

W06 must explicitly account for configured default_args in its still-proposed profile projection; that is not an implemented hash change. The separate run_checks scope proposal and W05 recovery are not approved by the default-argument decision. Research, production code, tests and real configurations remain untouched.

## 2026-09-10 selection transport correction

Human-approved D-ADAPTER-26 removes adapter Git/deletion knowledge and generic
fresh/expansion controls. DI-05 §7.17 is authoritative; W03/W04 now use required
operation/targets/args. Empty configured targets differs from an empty branch selection,
which never invokes adapters. Default narrow behavior remains; explicit native args
or deliberately configured use may request broader native execution.
Research/intake/catalog were amended within F-20; no census or role expansion.
This is documentary consolidation, not independent QA or executed conformance evidence.

## Explicit public workspace scope correction — 2026-09-10

The human rejected "." as public workspace shorthand. run_checks now requires
configured/workspace/targets/branch; run_tests requires configured/workspace/targets.
workspace forbids public targets and produces one resolved root target for the adapter.
configured still produces targets=[]. Public "." and equivalent root-only target
spellings reject with guidance to use workspace. Input exposure, runtime validation
and requested_scope output must agree. Adapter operation/targets/args is unchanged.
This supersedes the earlier two-scope W04 snapshots; it adds no native config semantics.
