<!-- docs\development\issue460\planning.md -->
<!-- template=planning version=130ac5ea created=2026-09-13T09:32Z updated=2026-09-13 -->
# Issue 460 Refactor Planning

**Status:** DRAFT — independent Planning NOGO; targeted corrections submitted for independent recheck  
**Version:** 0.4  
**Last Updated:** 2026-09-13  
**Baseline:** ea48558cf8034e9ab695fff675db7732c2ded660  
**Workflow:** refactor / planning

## Purpose

Translate frozen [Research](research.md), its boundary-specific Approved Strategy, and approved [Design](design.md) into reversible implementation cycles. [Integration review](design-integration-review.md) and each linked package remain authoritative for contracts and durable test claims. The human explicitly reported independent Design GO on ea48558c. Startup confirmed initialized issue 460 in Planning; no new Design approval is inferred from producer documents.

## Scope

Planning owns sequence, dependencies, exact paths, preserved behavior, cleanup and stop/go evidence. It does not redesign contracts or implement the 105 refactor cycles. The requested QA correction includes the bounded readback tooling prerequisite recorded below; the active phase remains Planning. External workspace migration, publishing, new startup-health/recovery features and permanent compatibility bridges are excluded. Producer-delegated review returns findings only; independent `pgmcp-qa` owns the Planning verdict.

## Prerequisites

- Independently invoked Planning QA before Implementation.
- Before each cycle, read its package authority and the applicable architecture/test/documentation boundaries, then verify its named predecessor evidence.
- Missing native dependencies/versions, a conflicting strategy or an unavailable operational recovery action are explicit stops at the owning cycle. They are not assumed to be available now.

## Summary

105 bounded cycles, in a valid serial order. The exact index assigns **126 consumers, 151 tests/helpers, 79 legacy suite sources and 57 additional existing dependencies**, plus **279 exact proposed new source paths**. C/T/A/S identifiers are source IDs; CY identifiers are implementation cycles. The [R001–R008 supplement](planning-path-ownership.md#readback-prerequisite-supplement) assigns eight additional dependencies introduced or exposed by the readback prerequisite without renumbering the frozen census or creating new cycles.

- [Execution foundations](planning-execution.md): [CY001](planning-execution.md#cy001)–[CY030](planning-execution.md#cy030).
- [Artifacts and mutation](planning-artifacts-mutation.md): [CY031](planning-artifacts-mutation.md#cy031)–[CY061](planning-artifacts-mutation.md#cy061).
- [Distribution, activation and retirement](planning-rollout.md): [CY062](planning-rollout.md#cy062)–[CY105](planning-rollout.md#cy105).
- [Exact path ownership and creation/revisit ledger](planning-path-ownership.md).

Every artifact family has its own acceptance cycle. Native check, test and fix conformance are separate from orchestration and public composition. The public switch applies an already-rehearsed diff; legacy deletion follows working target startup. Adjacent deletion groups are bounded by actual import dependencies, not a remaining-work bucket.

The cycle cards are the source of the operational `save_planning_deliverables` payload: exact order, number, name, D1/D2 and exit criteria. Path scopes/dependencies are linked from each payload entry. No file-existence predicate substitutes for behavioral evidence.

## Dependencies

The table shows semantic dependencies. Cards additionally enumerate immediate shared-file predecessors. Every later write to an existing or newly introduced path depends on its previous write. The serial schedule permits no overlapping writers. New evidence invalidates only the affected dependent claims.

| Cycle | Coherent result | Semantic predecessors |
|---|---|---|
| [CY001](planning-execution.md#cy001) | Isolated suite roots | Independent Planning GO |
| [CY002](planning-execution.md#cy002) | Template package value contracts | CY001 |
| [CY003](planning-execution.md#cy003) | Contained JSON Schema preparation | CY002 |
| [CY004](planning-execution.md#cy004) | Parser-supported template dependency graph | CY002, CY003 |
| [CY005](planning-execution.md#cy005) | Immutable template catalog and renderer selection | CY004 |
| [CY006](planning-execution.md#cy006) | Generation fingerprints and package labels | CY004, CY005 |
| [CY007](planning-execution.md#cy007) | First-line provenance writer and reader | CY006 |
| [CY008](planning-execution.md#cy008) | Prepared tool input contract | CY002, CY003 |
| [CY009](planning-execution.md#cy009) | Operation and attachment transport | CY008 |
| [CY010](planning-execution.md#cy010) | Required-null cache fidelity | CY008, CY009 |
| [CY011](planning-execution.md#cy011) | Generic bounded presentation | CY008, CY009, CY010 |
| [CY012](planning-execution.md#cy012) | Adapter package admission and trust | CY001 |
| [CY013](planning-execution.md#cy013) | Adapter process protocol | CY012 |
| [CY014](planning-execution.md#cy014) | Bounded process stopping | CY013 |
| [CY015](planning-execution.md#cy015) | Proposed-content input and scratch lifecycle | CY014 |
| [CY016](planning-execution.md#cy016) | Check bindings and output profiles | CY012 |
| [CY017](planning-execution.md#cy017) | Explicit check selection and branch scopes | CY016 |
| [CY018](planning-execution.md#cy018) | Python syntax check adapter | CY014, CY015 |
| [CY019](planning-execution.md#cy019) | Markdown preflight adapter | CY014, CY015 |
| [CY020](planning-execution.md#cy020) | Ruff checks and native configuration | CY013, CY016, CY017 |
| [CY021](planning-execution.md#cy021) | Mypy check and native configuration | CY013, CY016, CY017 |
| [CY022](planning-execution.md#cy022) | Pyright check and native configuration | CY013, CY016, CY017 |
| [CY023](planning-execution.md#cy023) | TypeScript syntax adapter | CY014, CY015 |
| [CY024](planning-execution.md#cy024) | Commit message adapter | CY006, CY007, CY014, CY015 |
| [CY025](planning-execution.md#cy025) | Lychee content and selection adapter | CY014, CY015, CY016, CY017 |
| [CY026](planning-execution.md#cy026) | Internal check orchestration | CY016, CY017, CY018, CY019, CY020, CY021, CY022, CY023, CY024, CY025 |
| [CY027](planning-execution.md#cy027) | Pytest adapter and native settings | CY013, CY014, CY015 |
| [CY028](planning-execution.md#cy028) | Internal test orchestration | CY027 |
| [CY029](planning-execution.md#cy029) | Ruff native fix conformance | CY020 |
| [CY030](planning-execution.md#cy030) | Internal fix orchestration | CY029 |
| [CY031](planning-artifacts-mutation.md#cy031) | Shared Python generation sources | CY004, CY005, CY006, CY007 |
| [CY032](planning-artifacts-mutation.md#cy032) | Pydantic DTO artifact | CY018, CY031 |
| [CY033](planning-artifacts-mutation.md#cy033) | Pydantic configuration artifact | CY018, CY031 |
| [CY034](planning-artifacts-mutation.md#cy034) | Plain Python class artifact | CY018, CY031 |
| [CY035](planning-artifacts-mutation.md#cy035) | Python Protocol artifact | CY018, CY031 |
| [CY036](planning-artifacts-mutation.md#cy036) | Portable adapter artifact | CY018, CY031 |
| [CY037](planning-artifacts-mutation.md#cy037) | Portable worker artifact | CY018, CY031 |
| [CY038](planning-artifacts-mutation.md#cy038) | Public unit-test artifact | CY018, CY031 |
| [CY039](planning-artifacts-mutation.md#cy039) | Public integration-test artifact | CY018, CY031 |
| [CY040](planning-artifacts-mutation.md#cy040) | TypeScript DTO artifact | CY004, CY005, CY006, CY007, CY023 |
| [CY041](planning-artifacts-mutation.md#cy041) | Shared document records and rendering | CY004, CY005, CY006, CY007 |
| [CY042](planning-artifacts-mutation.md#cy042) | Research artifact | CY019, CY041 |
| [CY043](planning-artifacts-mutation.md#cy043) | Design artifact | CY019, CY041 |
| [CY044](planning-artifacts-mutation.md#cy044) | Planning artifact and operational projection | CY019, CY041 |
| [CY045](planning-artifacts-mutation.md#cy045) | Validation report artifact | CY019, CY041 |
| [CY046](planning-artifacts-mutation.md#cy046) | Architecture document artifact | CY019, CY041 |
| [CY047](planning-artifacts-mutation.md#cy047) | Reference document artifact | CY019, CY041 |
| [CY048](planning-artifacts-mutation.md#cy048) | Generic document artifact | CY019, CY041 |
| [CY049](planning-artifacts-mutation.md#cy049) | Issue body artifact | CY019, CY041 |
| [CY050](planning-artifacts-mutation.md#cy050) | PR body artifact | CY019, CY041 |
| [CY051](planning-artifacts-mutation.md#cy051) | Commit artifact | CY024, CY041 |
| [CY052](planning-artifacts-mutation.md#cy052) | Artifact location policy | CY004, CY005 |
| [CY053](planning-artifacts-mutation.md#cy053) | Internal scaffold persistence | CY006, CY007, CY026, CY052 |
| [CY054](planning-artifacts-mutation.md#cy054) | Safe-edit construction and profile selection | CY006, CY007, CY026 |
| [CY055](planning-artifacts-mutation.md#cy055) | Safe-edit guarded replacement | CY014, CY015, CY054 |
| [CY056](planning-artifacts-mutation.md#cy056) | Schema discovery public composition | CY004, CY005, CY008, CY009, CY011, CY006, CY007 |
| [CY057](planning-artifacts-mutation.md#cy057) | Scaffold public composition | CY053, CY055, CY056 |
| [CY058](planning-artifacts-mutation.md#cy058) | Safe-edit public composition | CY057 |
| [CY059](planning-artifacts-mutation.md#cy059) | Check public composition | CY008, CY009, CY011, CY026 |
| [CY060](planning-artifacts-mutation.md#cy060) | Test public composition | CY008, CY009, CY011, CY028 |
| [CY061](planning-artifacts-mutation.md#cy061) | Fix public composition | CY008, CY009, CY011, CY030 |
| [CY062](planning-rollout.md#cy062) | Built and separately installed distribution | CY032, CY033, CY034, CY035, CY036, CY037, CY038, CY039, CY040, CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050, CY051, CY059, CY060, CY061 |
| [CY063](planning-rollout.md#cy063) | Operational components and selection | CY004, CY005, CY006, CY007 |
| [CY064](planning-rollout.md#cy064) | Installation checkpoint and first-v3 bootstrap | CY063 |
| [CY065](planning-rollout.md#cy065) | Candidate staging and proposal admission | CY026, CY032, CY033, CY034, CY035, CY036, CY037, CY038, CY039, CY040, CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050, CY051, CY064 |
| [CY066](planning-rollout.md#cy066) | F-10 activation and deterministic recovery | CY065 |
| [CY067](planning-rollout.md#cy067) | Prepared renewal CLI composition | CY066 |
| [CY068](planning-rollout.md#cy068) | Workflow carriers and phase semantics | CY042, CY043, CY044, CY045, CY056, CY057, CY058, CY059, CY060, CY061 |
| [CY069](planning-rollout.md#cy069) | Host instruction source parity | CY068 |
| [CY070](planning-rollout.md#cy070) | Prepared placement and rollout configuration | CY052, CY057, CY058, CY059, CY060, CY061, CY062, CY067, CY022 |
| [CY071](planning-rollout.md#cy071) | Target startup composition and launch rehearsal | CY070, CY068, CY069, CY062, CY066, CY067 |
| [CY072](planning-rollout.md#cy072) | Public V3 cutover | CY071 |
| [CY073](planning-rollout.md#cy073) | Close legacy scaffold harness imports | CY072 |
| [CY074](planning-rollout.md#cy074) | Retire obsolete scaffold tool and manager route | CY072, CY073 |
| [CY075](planning-rollout.md#cy075) | Retire obsolete template scaffolder route | CY074 |
| [CY076](planning-rollout.md#cy076) | Retire obsolete workspace-upgrade route | CY072 |
| [CY077](planning-rollout.md#cy077) | Retire legacy registry and hash authority | CY072, CY075, CY076 |
| [CY078](planning-rollout.md#cy078) | Retire legacy metadata and lifecycle contracts | CY077 |
| [CY079](planning-rollout.md#cy079) | Retire legacy introspection and schema inference | CY078 |
| [CY080](planning-rollout.md#cy080) | Retire parallel component scaffolders | CY072, CY075 |
| [CY081](planning-rollout.md#cy081) | Retire legacy validator and validate_template stack | CY072, CY079 |
| [CY082](planning-rollout.md#cy082) | Retire project_structure and hidden naming | CY081, CY080 |
| [CY083](planning-rollout.md#cy083) | Retire generic Pytest runner | CY072 |
| [CY084](planning-rollout.md#cy084) | Close QAManager-dependent parser test imports | CY072, CY083 |
| [CY085](planning-rollout.md#cy085) | Close QAManager-dependent fix and state test imports | CY072, CY083 |
| [CY086](planning-rollout.md#cy086) | Retire quality orchestration and old check/fix tools | CY072, CY083, CY084, CY085, CY081 |
| [CY087](planning-rollout.md#cy087) | Retire generic native-parser DSL | CY086 |
| [CY088](planning-rollout.md#cy088) | Retire auto replay state | CY072, CY086, CY087 |
| [CY089](planning-rollout.md#cy089) | Scaffold and schema reference migration | CY072, CY077, CY078, CY079, CY080, CY081, CY082 |
| [CY090](planning-rollout.md#cy090) | Execution and evidence references | CY072, CY083, CY086, CY087, CY088 |
| [CY091](planning-rollout.md#cy091) | Deployment and setup references | CY062, CY067, CY072 |
| [CY092](planning-rollout.md#cy092) | Architecture diagrams | CY077, CY078, CY079, CY080, CY081, CY082, CY083, CY086, CY087, CY088 |
| [CY093](planning-rollout.md#cy093) | Architecture manuals and reference navigation | CY068, CY089, CY090, CY091, CY092 |
| [CY094](planning-rollout.md#cy094) | Retire legacy Pydantic/class sources | CY032, CY033, CY034, CY035, CY072, CY080 |
| [CY095](planning-rollout.md#cy095) | Retire legacy specialized code/test sources | CY036, CY037, CY038, CY039, CY040, CY072, CY080 |
| [CY096](planning-rollout.md#cy096) | Retire legacy phase-document roots | CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050, CY051, CY072 |
| [CY097](planning-rollout.md#cy097) | Retire legacy explanatory-document roots | CY096 |
| [CY098](planning-rollout.md#cy098) | Retire legacy tracking roots | CY097 |
| [CY099](planning-rollout.md#cy099) | Retire portable Python/test macro sources | CY031, CY041, CY094, CY095, CY096, CY097, CY098 |
| [CY100](planning-rollout.md#cy100) | Retire document macro sources | CY099 |
| [CY101](planning-rollout.md#cy101) | Remove rejected Resource/Service/Tool artifact sources | CY072, CY080, CY094, CY095, CY096, CY097, CY098 |
| [CY102](planning-rollout.md#cy102) | Remove source-project specialization patterns | CY101 |
| [CY103](planning-rollout.md#cy103) | Remove unreachable YAML and test seeds and agent hints | CY102 |
| [CY104](planning-rollout.md#cy104) | Retire exhausted tier bases | CY100, CY103 |
| [CY105](planning-rollout.md#cy105) | Retire exhausted legacy test harness | CY077, CY078, CY079, CY080, CY081, CY082, CY083, CY086, CY087, CY088, CY094, CY095, CY096, CY097, CY098, CY099, CY100, CY104, CY101, CY102, CY103 |

## One active server and controlled cutover

1. **Baseline — CY001.** Record the current server's real interpreter, import origin, working directory, explicit roots, relevant nonsecret launch configuration and usable read-only/tool contracts. No second persistent server is required. Short-lived child processes used by targeted tests are test subjects.
2. **Safe preparation.** The normal entrypoint keeps the working legacy assembly through CY071; final internal components and public compositions are tested on explicit isolated roots. Shared input/transport/presentation changes must preserve the normal legacy launch in their own cycle. The sole public target switch is CY072; there are no supported old aliases, dual readers, constructor modes or mixed same-name ToolAssemblies.
3. **Actual disk dependencies remain available.** The running old safe-edit validator can read legacy templates from disk. Keep its modules, templates and configuration readable through successful target startup. Merely retaining Python objects in memory is insufficient. Preparation artifacts record scoped preimage/postimage diffs; they are historical migration evidence, never a second runtime configuration authority.
4. **Rehearsal — CY062, CY070, CY071.** Prove a built and separately installed candidate outside checkout. Apply the exact planned activation diff only to isolated source/config copies and start the real entrypoint with matching interpreter/import/CWD/roots/environment. The existing proxy launches `sys.executable -m mcp_server`; PytestRunner modifies PATH/VIRTUAL_ENV, so blind test-environment inheritance is insufficient. Verify MCP initialization/discovery and real target calls, no duplicate names, fresh-init/startup, explicit owner-migration/startup, activation-lock exclusion, unresolved-recovery refusal and running-catalog immutability.
5. **Recovery preparation — before CY072.** Capture the exact code/config/suite/installation preimages, concurrent dirty edits and cycle-owned recovery steps. Identify and rehearse where possible the existing host/client action that can restore these bytes and relaunch the known interpreter if MCP is unavailable. The current proxy terminates the old child before starting the replacement; restart/initialize replay does not roll back code or config. A degraded server may expose only health_check. Do not pretend git_restore/safe_edit is callable after failed startup. If a workable external recovery action cannot be recorded, stop before the restart and request only that concrete missing operational decision.
6. **Activation — CY072.** Check all preimages against the rehearsal; mismatch stops application and refreshes affected preparation evidence. Apply the scoped source/config/host-copy diff, explicitly migrate only this repository's owned suite via DI-06, and run the landed normal entrypoint in a short-lived process while the current MCP route still works. Correct failures through that route. Only then request one deliberate restart_server boundary, supported client rediscovery and real separately evidenced schema/scaffold/edit/check/test/fix calls. Record the coherent before/after source/config/installation state. No external workspace is silently adopted.
7. **Retirement.** After successful activation, close fixture/plugin imports before their first deleted production dependency. Remove inactive tools/managers, then their schema/renderer/validator dependencies, checking fresh normal startup after each production deletion cycle. Keep unrelated state, workflow GateReport/GateViolation, PR atomicity and original PR-lock behavior. A remaining caller blocks deletion and requires an explicitly scoped Planning amendment.

These are operational prerequisites for Implementation, not a claim that runtime conformance or emergency recovery has already been demonstrated during Planning.

## Per-cycle verification and recovery contract

These rules are included in every cycle's exit criteria.

- **V1 — green baseline.** Record R-CYnnn (exact pre-cycle SHA), listed dirty-file preimages, applicable invariants and accepted deltas. Establish focused existing behavior. Introduce a failing characterization only for a durable uncovered obligation; no artificial RED for structural/doc changes.
- **V2 — narrow execution.** Before public cutover, use the active governed run_tests/run_quality_gates tools; afterward use the active run_tests/run_checks contracts. Run the named surviving test files or exact relevant case nodes and file gates over surviving changed production/test paths. Capture exact invocations, native/interpreter versions and full cached-resource URIs. Do not substitute manual terminal commands for governed tools.
- **V3 — independent observations.** Adapter evidence compares native inputs/results/effects directly with emitted protocol facts. Consumer tests use narrow typed doubles and actual filesystem facts; public tests use real registration/decorators, cache resource reads and presentation. No layer certifies itself merely by invoking its own wrapper. Unavailable prerequisites are not executed conformance.
- **V4 — bounded changes.** IDs expand to enumerated exact files. Each card owns only its described seam and new/revisited paths. Contract/default/package/native-version changes invalidate their affected predecessor evidence. Ruff fix entrypoint changes invalidate affected Ruff check fingerprint/conformance evidence. Reuse fresh unrelated evidence.
- **V5 — migration/removal.** Before removal, close runtime and type-only imports, package exports, helper requests, plugin registrations and config reads at the first dependency deletion. Prove named successor behavior and collect the affected surviving tests. Use the frozen catalog's hidden-aware active-source search with normal ignores and explicit historical/archive/work-product exclusions. Source absence alone is insufficient; run the fresh normal startup/handshake for production deletion cycles.
- **V6 — review and rollback.** Record D1 result and D2 evidence separately, exact diff, retained claims, R-CYnnn and outcome-neutral review request. Restore only the cycle-owned inverse diff; git_restore resets both index and working tree and must not overwrite unrelated dirty changes. If reversal conflicts with later edits, stop and construct the scoped inverse. Independent QA decides progression. F-10 complete-tree activation has its own designed recovery; F-20 native fix failures may retain earlier writes and have no automatic verification or rollback.

Full-suite execution and branch-wide gates belong once to Validation after implementation/retirement. Docs-only cycles use semantic, link and source-copy evidence without artificial tests. Tests obey production architecture/typing standards; no broad disables.

## Separate role and activation proof

| Boundary | Native/internal owner | Public composition | Retirement gate |
|---|---|---|---|
| Checks | CY018, CY019, CY020, CY021, CY022, CY023, CY024, CY025, CY026 | CY059; actual launch CY072 | CY081, CY086, CY087, CY088 |
| Tests | CY027, CY028 | CY060; actual launch CY072 | CY083 |
| Fix application F-20 | CY029, CY030 | CY061; actual launch CY072 | CY086, CY088 |
| Template activation F-10 | CY063, CY064, CY065, CY066 | CLI CY067, startup CY071, activation CY072 | CY076 |

All nine DI-05 startset packages are separately owned. Ruff check conformance does not certify its fix role; pytest remains a native test adapter rather than generic server knowledge. Preserve approved W09 stricter native defaults and report actual deltas. No auto/replay-state scope returns.

Shared §5.5 remains exact: model-only core results normalize once to operation-plus-attachments; cache/text see the operation, resource presentation sees attachments, and isError follows operation.success. Unrelated whole-tool ValidationErrorOutput.input_schema remains in its existing operation/cache contract. Selected-context failures use their dedicated operation plus schema identity attachment. Required-null serialization is schema-aware and does not change unrelated legacy DTO requiredness.

## Binding obligation coverage

[Integration §4](design-integration-review.md#4-semantic-integration-closure) owns the exact 22 findings, 44 strategy subjects, 19 invariants and 23 expected results. The following maps its primary groups to execution owners without repeating or changing contract text.

| Primary obligation group | Implementation and proof owners |
|---|---|
| DI-01: F-02/F-06/F-12/F-17; I-05/I-06/I-08; E-04/E-05/E-08; seven strategy subjects | CY002/CY003/CY008/CY009/CY056 and concrete family schema/render cycles CY031, CY032, CY033, CY034, CY035, CY036, CY037, CY038, CY039, CY040, CY041, CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050, CY051 |
| DI-02: F-04/F-05/F-11/F-16; I-03; E-02/E-07; four subjects | CY004/CY005/CY006/CY007/CY056/CY063; retirement CY077/CY078/CY079/CY099/CY100/CY104 |
| DI-03: F-01/F-07/F-14/F-14A/F-14B; I-01/I-02/I-07; E-01/E-06/E-10; thirteen subjects | CY031, CY032, CY033, CY034, CY035, CY036, CY037, CY038, CY039, CY040, CY041, CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050, CY051; explicit source retirement CY094, CY095, CY096, CY097, CY098, CY099, CY100, CY104, CY101, CY102, CY103; no generated/runtime-class deletion |
| DI-04: F-03/F-13/F-15; I-04/I-09/I-13; E-03/E-11/E-18; five subjects | CY052, CY053, CY054, CY055, CY056, CY057, CY058; location/validator legacy removal CY081/CY082 |
| DI-05: F-08/F-19/F-20; I-16/I-19; E-13/E-20/E-23; three subjects | CY012, CY013, CY014, CY015, CY016, CY017, CY018, CY019, CY020, CY021, CY022, CY023, CY024, CY025, CY026, CY027, CY028, CY029, CY030/CY059, CY060, CY061; separate check/test/fix native evidence; removal CY083, CY086, CY087, CY088 |
| DI-06: F-10; I-17/I-18; E-21/E-22; two subjects | CY062, CY063, CY064, CY065, CY066, CY067, CY072/CY091; operational equality separate from generation provenance |
| DI-07: F-09; I-12/I-15; E-09/E-15/E-16/E-19; two subjects | CY042, CY043, CY044, CY045/CY072/CY068, CY069, CY089, CY090, CY091, CY092, CY093; nineteen carrier meanings and actual source-copy direction |
| DI-08: I-14/E-17; one subject | CY001 and each touched test episode; CY105 helper/plugin retirement; no separate catch-all test migration |
| XC-01 I-11/E-14, XC-02 removals, RC-01 I-10/E-12; three subjects | Every card V1–V6; all exact path dispositions; public original-PR coverage CY049/CY050/CY053/CY057/CY058 |
| Four deferred strategies and F-18 | CY101/CY102/CY103 removes only approved rejected seeds/patterns with YAML recovery trace; no new YAML types, discovery tool, service family or portable-Python feature expansion |

Additional frozen amendments remain binding: no semantic model-example validation; no auto result reuse; explicit workspace/configured/targets/branch scope rules; fix files-only/caller-order/stop-first and partial writes; generation-only pf/sf versus full operational components; safe-edit enforce/report without mode/verify_only aliases. Startup health/recovery policy and OS sandbox isolation remain deferred.


The additional lifecycle closure owners are [CY073](planning-rollout.md#cy073), [CY074](planning-rollout.md#cy074), [CY075](planning-rollout.md#cy075), [CY076](planning-rollout.md#cy076), [CY084](planning-rollout.md#cy084), [CY085](planning-rollout.md#cy085), [CY070](planning-rollout.md#cy070), [CY071](planning-rollout.md#cy071). They refine sequencing without changing the Strategy or Design.

## Validation and Documentation deliverables

- **V460.1:** Exact 126/151/79/57 existing-source closure, new-path ledger and applicable architecture review.
- **V460.2:** Independent native, consumer and real public evidence for check/test/fix, schema/cache/presentation and both mutation contracts.
- **V460.3:** Fresh installed complete distribution, first-v3 migration/startup, F-10 recovery and actual client rediscovery; rerun evidence invalidated by later code/config/package edits.
- **V460.4:** One full suite and branch-wide gates, with per-cycle evidence retained and failures honestly resolved.
- **V460.5:** All nineteen workflow carriers and actual instruction source/copy/reference consistency.
- **D460.1:** Final active user/operator/reference reconciliation against implemented contracts and accepted deltas.
- **D460.2:** Release/version/upgrade evidence and explicit external-owner migration instructions.
- **D460.3:** Outcome-neutral final hand-over. Scope any additional concrete release files explicitly when that phase starts.

Documentation does not postpone live-cutover guidance or the enumerated implementation documentation cycles until after Validation. No publish/merge is authorized.

## Review record and current evidence

Independent QA has closed the earlier Pyright and stored-payload findings. The latest user-supplied verdict independently confirms all 105 cycles and 218 deliverables, 27 contiguous windows, 161522 Unicode codepoints and the computed SHA-256 `026fd5ddeb902a9f657c8d3aec7205208d38605064bbb3804263d4bb588da49c`. Its targeted NOGO concerns only this discovery amendment: incorrect C004 hint ownership and a stale hand-over. The corrections below await targeted independent recheck; Research and Design remain closed.

### P1 — Pyright removal ownership

The corrected cards assign one live-removal owner: **CY072**. CY022 owns the adapter, the approved native/editor Python-target migration in pyrightconfig.json, and native preserved-value proof on isolated before/after configuration copies. It is read-only for pyproject.toml. CY070 records the exact [tool.pyright]-only deletion hunk; CY071 rehearses it; CY072 applies it and checks the retained values. C006/S008 write/review episodes and the affected shared-file predecessor CY027 are synchronized. The internal findings-only reviewer rechecked these exact boundaries and found no remaining textual contradiction; this does not provide runtime evidence or independent workflow GO. There is no new cycle, source path, runtime implementation or Research/Design decision.

The operational delta for CY022/CY027/CY070/CY071/CY072 was submitted with the final card D1/D2, preservation, predecessors and exit text through update_planning_deliverables. Receipt `pgmcp://cache/runs/c52b190e41f1405b8b0fd006f4374661` reports success, 105 cycles and 218 deliverables. This receipt proves update acceptance/counts only; it does not prove full stored-state parity.

### P2 — Complete public stored-payload readback

The requested bounded tooling prerequisite now returns `planning_deliverables` from the existing persisted project query in the existing frozen `CyclePlanningModel`. It retains the input contract, phase status and compact presentation. The tool depends on a narrow read protocol. Invalid planning fails explicitly; absent planning remains supported.

A live full read exposed a second, independently observed limit: the client truncated the 158-kilobyte resource in the middle, making its JSON unusable. The same cache-resource family therefore supports optional bounded character windows. Each window contains the run ID, offset, total codepoints, full-content SHA-256, text and next offset. Full reads without query parameters remain unchanged. Cache windows apply generically to all tools, not only issue 460.

This is a prerequisite to reviewing Planning, outside the 105 implementation cycles. No phase/cycle transition, storage-format migration, new public tool, secondary planning store or refactor cutover was performed.

| Boundary | Exact correction and preservation |
|---|---|
| Output and read interface | [ProjectPlanOutput](../../../mcp_server/schemas/tool_outputs.py), [GetProjectPlanTool](../../../mcp_server/tools/project_tools.py), [IProjectPlanReader](../../../mcp_server/core/interfaces/project_plan.py). Preserve unrelated project commands and phases. |
| Deliverables query failure | [ProjectManager](../../../mcp_server/managers/project_manager.py): retain source and prior backup bytes on query corruption/version failure; retain the existing backup behavior in all three commands. This claim is limited to deliverables reads. The pre-existing state.json backup path through phase enrichment is outside scope. |
| Bounded resource reads | [CachedResponseResource](../../../mcp_server/resources/cache.py), [window/chunk values](../../../mcp_server/schemas/cache_chunk.py). Strict URI parameters, Unicode-codepoint offsets, content hash, explicit EOF and stale-cache failure. No cache-storage or publisher change. |
| Durable regression proof | [project tool tests](../../../tests/mcp_server/unit/tools/test_project_tools.py), [manager tests](../../../tests/mcp_server/unit/managers/test_project_manager.py), [cache tests](../../../tests/mcp_server/unit/resources/test_cache_resource.py), [real MCP readback](../../../tests/mcp_server/integration/test_project_plan_readback.py). The latter uses normal bootstrap and actual tool/resource handlers on isolated roots; a second assembly proves a new empty cache, not an OS process restart. |
| Clean-break preservation | [R001–R008](planning-path-ownership.md#readback-prerequisite-supplement) and CY001/CY009/CY010/CY044/CY071/CY072/CY073/CY105 assign exact write/review seams. CY071 rehearses root/test changes solely in isolated candidate copies; CY072 alone applies those exact preimage-checked live test hunks without new migration decisions. Import closure precedes removal; CY105 owns only residual exhausted helper acquisition. |

Recovery baseline for this prerequisite is `f3b1af35c3c79b4bbb6c675767953b7ffdccc729`. The repair uses six production files, four test files and their scaffolding registry records; its inverse must remain limited to those changes and the documented Planning amendment. No configuration/package/entrypoint migration was applied. All runtime imports and normal bootstrap were checked in fresh pytest workers before controlled reloads. Two sequential reloads were needed: first for the output omission, then for the newly observed client truncation. The one active server remained healthy: PID 112400 → 132356 → 7332. Current health receipt: `pgmcp://cache/runs/b7003e49381e4220a931685fe573c041`; current context confirms Planning with no active cycle.

### Executed evidence

- Baseline: 65 existing project tests passed. Added regression cases first reproduced missing/invalid payload handling and destructive deliverables-query errors (70 passed, 5 failed).
- Final scoped tests: **114 passed, zero failures/errors/skips**, using `run_tests(path="tests/mcp_server/unit/tools/test_project_tools.py tests/mcp_server/unit/managers/test_project_manager.py tests/mcp_server/integration/test_project_plan_readback.py tests/mcp_server/unit/server/test_bootstrap.py tests/mcp_server/unit/resources/test_cache_resource.py", timeout=120, verbose=true)`. Receipt: `pgmcp://cache/runs/39b83eca94af4512a1804b5230632398`.
- Final `run_quality_gates(scope="files", files=[the ten production/test paths above], verbose=true)`: all applicable Ruff, imports, line-length, Pyright and MCP typing gates passed. Generic non-MCP Types had no matching files. Receipt: `pgmcp://cache/runs/674107b2c3be41408f7ef3fe1ad757d9`.
- Updated shared-file predecessor payloads for CY009/CY010/CY071 and CY072/CY105: accepted, 105 cycles / 218 deliverables. Receipts `pgmcp://cache/runs/dda9928a3f56494faa6b449e470c3153` and `pgmcp://cache/runs/0aec8c65147a46988ec64b5345d0f776` prove update acceptance/counts only.
- Fresh public query snapshot: `pgmcp://cache/runs/6b75c234d0b94755b95f4159d4bc79b8`, reconstructed through **27 windows** into **158663 Unicode codepoints**. Full-content SHA-256: `e3da60d65603ab771b911f9f182d3295d143247192ce5e5f6f5c7b02cad2eea2`.
- Producer comparison against the actual reconstructed payload: **105/105 ordered cycle numbers and names, 210/210 ordered D1/D2 IDs and full descriptions, 105/105 exact exit criteria, 5/5 Validation and 3/3 Documentation deliverables match**. Descriptions include preserved behavior, semantic/shared-file predecessors and exact card links. No manual deliverables-file read, request echo or substitute mirror was used.
- The frozen 126/151/79/57 source index and 279 proposed paths remain intact. Eight supplemental dependencies have exact cards; the final graph has **504 unique forward semantic/shared-file edges**. No new cycle or catch-all migration was added.
- Internal review is findings-only. It examined implementation limits, bootstrap safety, window/hash semantics and preservation sequencing; it cannot lift independent NOGO. No full suite, branch-wide gates, native adapter conformance, F-10/F-20 execution or public refactor cutover is claimed.

### Reproducible independent QA readback

Run receipts are transient evidence pointers, not durable snapshot storage. The durable verification path is the public query plus its readable resource:

1. Call `get_project_plan(issue_number=460)` afresh and use the returned resource URI. The text phase summary is not the Planning payload.
2. Read that URI with `?offset=0&limit=6000`. Follow returned `next_offset` on the same URI until null. Require the same run ID, hash and total length on every window, and contiguous offsets. Offsets count Unicode codepoints; do not advance by JavaScript `string.length`.
3. Join all `text`, verify total codepoint length and SHA-256 of the UTF-8 bytes, then parse JSON. If a window is client-truncated, retry with a smaller limit. Cache loss or a changed hash requires a new public query and complete reconstruction from zero; never mix runs.
4. Compare every ordered cycle to the three card documents. D1 description is the card's bounded result, then `Preserved behavior:`, `Semantic predecessors:`, `Shared-file predecessors:`, and `Exact scope, write-set and rollback: <repository card path>#cyNNN.` D2 description is its independent-evidence line followed by `Named proof set and V1–V6: <repository card path>#cyNNN.` Compare exact names, IDs, descriptions and stop/go text; compare all phase deliverables above. Inspect each linked write/review scope, including R001–R008.
5. Record the independent comparison outcome. The payload finding is already independently closed; retain this procedure for future payload changes rather than reopening that finding for documentation-only corrections.

The generic window contract and limits are documented in [get_project_plan reference](../../reference/tools/project.md#reading-large-cached-plans).

## Fresh-chat cache discovery amendment

This amendment plans delivery; it does not implement guidance, restart the server or authorize Implementation. The retained window API alone does not teach a new agent how to use it. Until CY011 lands, the generic discovery gap remains open and Planning QA must use the explicit readback procedure above.

- **CY011:** own the self-contained generic hint beside every ordinary cache URI, within existing C106 presentation configuration and mapped presenter proofs. This small guidance slice describes the already-live API and is proved against the retained live assembly; it activates no V3 contract. Fresh-chat reconstruction without prior conversation or issue-document coaching is required before this cycle closes.
- **CY069 → CY071 → CY072:** prepare the general startup instruction procedure in existing authoritative source/copy mappings, rehearse it, then apply the exact reviewed patch at cutover. CY069 depends explicitly on CY011. CY072 repeats discovery using actual installed instructions after real client rediscovery. No persistent parallel server, new resource family or second instruction authority is introduced.
- **CY090:** reconcile generic resource and project references with the delivered behavior; it cannot postpone first discovery delivery.
- Each amended card retains its explicit write-set, R-CYnnn recovery point, preserved behavior and independent stop/go boundary. A missing or budget-truncated hint, startup mapping mismatch, incomplete reconstruction or reliance on producer coaching fails the owning proof. Recovery guidance must never replay mutating/non-repeatable producers merely to recreate a cache; use an existing result/status query or report unavailable details. Only safe read-only queries may be repeated. Existing full-read behavior, cache lifetime and window limits remain unchanged; no fixed Codex/client truncation limit is assumed.

Fresh amendment readback: `pgmcp://cache/runs/7bf793b9a9cf4688afcda0b0b1d423af`, 27 contiguous windows, 161522 Unicode codepoints, consistent server-reported SHA-256 `026fd5ddeb902a9f657c8d3aec7205208d38605064bbb3804263d4bb588da49c`. Actual reconstructed JSON exactly matches all 105 ordered cards, 210 D1/D2 descriptions and exit criteria, plus all eight phase deliverables (218 total). The graph has 504 forward edges. This amendment check verified page metadata, total length and parsed content parity; it did not independently recompute the content hash. Earlier runtime evidence above belongs to the retained quickfix and was not rerun for this planning-only amendment. Internal findings-only review identified unsafe producer replay; CY011 now prohibits mutation replay and its recipe is binding input to CY069/CY071/CY072. Independent QA has since confirmed the discovery split and exact payload parity, including an independently computed matching hash. Only its two targeted amendment-text findings require correction and recheck.

## Refactor / Planning Hand-over

### Scope

The 105-cycle refactor plan, closed Pyright ownership correction and bounded complete-readback prerequisite. Research/Design and refactor strategy remain unchanged. No Implementation progression or refactor rollout.

### Deliverables

This hub; [execution](planning-execution.md), [artifacts/mutation](planning-artifacts-mutation.md), [rollout](planning-rollout.md), [path ownership and readback supplement](planning-path-ownership.md); [public readback reference](../../reference/tools/project.md#reading-large-cached-plans); production/test entry points and frozen Research/Design inputs linked above. The branch diff is the complete change inventory.

### Evidence

114 scoped tests and all applicable scoped gates passed. Healthy live server after controlled reloads. The actual publicly reconstructed Planning payload matches all 105 cards and 218 deliverables; 504 forward dependencies and the eight supplemental paths are mapped. Exact calls, current snapshot hash and repeatable verification procedure are above.

### Open Work

Targeted independent recheck of the two discovery-amendment text corrections remains open: C004 no longer claims CY011 cache-hint ownership (C106 remains the sole configuration owner), and this hand-over now records the already-closed payload finding accurately. The latest targeted amendment NOGO is not lifted by these producer corrections. Cycle cards and the operational payload are unchanged; no full Planning re-review or repeated payload proof is requested. The known pre-existing state.json error-path backup remains outside scope.

### Review Request

Review requested from independently invoked `@qa plan-verifier`: confirm or reject closure of the C004/C106 ownership contradiction and stale hand-over findings only. The earlier payload finding is independently closed. No new workflow GO or Implementation transition is inferred.
