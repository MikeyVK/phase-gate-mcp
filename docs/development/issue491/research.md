<!-- pgmcp:v1 id=research pv=1.0.0 pf=lgBwxWMfTAmNNg_O sf=5--KpGf2wHUv2qAj -->

# Issue \#491 — Planning creation and mutation contracts

**Status:** DRAFT — owner strategy discussion pending  
**Version:** 1.8  
**Last Updated:** 2026-10-09

## Purpose

Establish the evidenced contract gaps and owner decisions needed for a bounded refactor of planning creation, updates and readback.

## Scope In

save_planning_deliverables/update_planning_deliverables input admission, persisted effects, merged-plan validity, identity/order, lifecycle ownership, nested validation specs and complete public readback; relevant existing tests and historical rationale. Supporting scope includes the shared lossless encoder/decoder contract, unused state/status decoder injection cleanup and the inaccurate record_sub_phase timing docstring. Explicit scope extension: add a complete active-branch commit-read capability in the existing Git layer, a narrowly injected execution-evidence consumer at the planning command, and the update force/retry contract with direct wiring, test/helper and reference changes. This is new runtime IO/protection behavior, not merely extending a search limit.

## Scope Out

Implementation/design/cycle planning; a generic deletion tool, new event-sourcing architecture, broad workflow/fixture modernization, unrelated adapter/transport work and compatibility bridges not approved by the owner.

## Problem Statement

Planning creation validates a complete plan, while mutation validates only a partial payload and writes its merged result without complete-plan validation. Some admitted fields have no effect and historical lifecycle constraints do not map directly to current state. Research must distinguish defects from deliberate merge policy before changing the contract.

## Goals

- Map every admitted field to its persisted effect and downstream consumers.
- Separate evidenced contract gaps, deliberate constraints and owner product choices.
- Present boundary-specific strategy options with proportional cost and risk; retain a pending approval state until the owner decides.

## Background

Source inspection on 2026-10-08 uses base commit 2366ef78baaf1df79704d06133f1136399a9ea37 and follows #491's Research leads. #229 deliberately separated write-once save from iterative merge-update; its C8 decision classified cycle deletion as append-only audit policy. #390 introduced strict frozen input models and renamed tdd_cycles to cycles with a clean break. #257 described mutable open cycles and read-only completed cycles, but the current cycle history records entered events rather than completed status. Historical decisions are material inputs, not automatic present-day requirements.

## Findings

### Current responsibilities and invariants

| Boundary | Current contract / source evidence | Consequence |
|---|---|---|
| Creation | ProjectManager.save_planning_deliverables validates CyclePlanningModel, checks a prior save, and requires cycles when workflow configuration has a cycle-based phase. | Preserve explicit create-versus-update ownership unless the owner chooses otherwise. |
| Update admission | UpdatePlanningModel permits partial cycle entries and optional/null fields; tools serialize with model_dump(exclude_none=True). | Omission and explicit null collapse at the public tool boundary; no optional-field clearing intent survives. |
| Existing cycles | Lookup uses cycle_number; deliverables merge by id; exit_criteria is copied if present. name is never copied. | An admitted name-only update has no effect while the tool can report success. |
| New cycles | Unknown cycle_number entries append as partial dictionaries. | Missing required fields, gaps, zero/negative indices or invalid order can survive update admission and reach storage. |
| Derived total | Incoming cycles.total is not assigned. The updater keeps max(existing total, highest cycle_number); output total_cycles is list length. | The historical derivation was deliberate. Assertion/rejection versus removal from writable input is a product decision; silent admission is misleading. |
| Deliverable replacement | A matching id replaces the entire supplied deliverable object; description is required. Omitted validates disappears on replacement. | This is documented whole-object replacement, not nested field patching. New partial-deliverable semantics would change the public contract. |
| Empty collections | Empty cycle/deliverable lists do not delete existing entries; an empty update can still write successfully. | Deletion, clearing, idempotent no-op reporting and replacement must be explicit choices. |
| Identity | Complete save enforces sequential cycle positions and total == length; no deliverable-ID uniqueness validator exists. Updates have no equivalent final validation. | Duplicate IDs or repeated cycle updates have ambiguous lookup effects; the intended uniqueness domain needs a decision. |
| Merged-plan validity | Update validates UpdatePlanningModel before merge, then writes without CyclePlanningModel validation. StateVersionValidator validates JSON/envelope version only. | An update can persist a plan that creation and the public complete readback would reject. |
| Readback / success | get_project_plan strictly validates stored planning with CyclePlanningModel; mutation summaries contain counts, not names/specs. | Complete readback already exists. A successful mutation must yield a valid, faithful readback; expanding presentation/cache architecture is unnecessary. |
| Nested validates | ValidatesModel admits file_glob with file and forbids dir/pattern. DeliverableChecker's file_glob requires dir/pattern. | The public planning schema and existing gate executor disagree. This is a directly affected nested contract, not a request for a new checker. |
| Lifecycle protection | save/update are branch_mutating tools subject to context-loaded and PR-lock enforcement. ProjectManager.update reads no cycle history and records no per-update audit. | Those guards do not implement completed-cycle immutability. The archived guard cannot be reinstated by assuming a nonexistent completed status. |

These are source-confirmed observations, not live malformed-input reproductions or newly executed failure tests. Illustrative consequences: a rename of existing C1 is ignored; appending C3 to C1 can store total=3 with two entries; appending a number-only cycle can store a missing deliverables/exit_criteria entry. Neither invalid append outcome satisfies the complete creation/readback model.

### Structural seams and preservation limits

The two per-ID merge loops and save/update response assembly are duplicated. Candidate seams are the existing planning value models, ProjectManager's command boundary, injected read-only lifecycle state and existing public readback. No new generic mutation language or workspace deletion subsystem is required merely to reconcile these contracts. Pure models must not read state/config files; phase/workflow policy stays config-driven; persistence remains atomic and owned by the existing command path.

cycle_number is both lookup identity and execution order. PhaseStateEngine reads stored total for range checks and stores cycle number/name in entered history; PhaseContractResolver selects checks by cycle number and deliverable ID. Renumbering or reordering started cycles therefore changes the meaning of existing references. Git history preserves historical bytes, but does not itself prevent reinterpretation of active lifecycle references. Atomic file replacement protects against partial bytes, not an invalid merged plan or concurrent read/modify/write races.

### Strategy options for owner review

| Boundary | Narrow coherent option | Alternative and cost/risk |
|---|---|---|
| Public create/update ownership | Keep write-once save plus explicit update; fix ignored admitted fields and validate the resulting plan before writing. | Whole-plan replacement simplifies some edits but expands accidental deletion/overwrite risk. |
| Field intent | Preserve omitted fields; define null explicitly per optional field. Keep deliverables as complete replacement by id if desired. | Uniform deep patch needs new partial-deliverable semantics and nested clearing rules; more schema/test/consumer change. |
| total | Derive canonical count; optionally retain supplied total as a checked assertion of the resulting count. | Remove total from writable requests in a clean break, requiring mechanical caller/doc updates. Both avoid silent acceptance. |
| Identity/order | Stable cycle_number and scoped IDs; unambiguous duplicates rejected; validate a complete sequential result. | Separate stable cycle IDs from order is a larger feature/architecture change and not required for current gaps. |
| Delete/renumber/reorder | Retain append/update semantics for this issue after explicitly reassessing the original audit rationale. | Allow replacement of not-yet-started work only, with explicit reference/lifecycle validation. Feasible but a new feature with higher cost; not preapproved or permanently excluded. |
| Lifecycle | Define which cycles are protected using actual entered/current/forced/phase events and an injected narrow state reader. | Freeze all entered cycles is simpler but also freezes active work. Completed-only protection needs a precise completion/reopen policy; no guessed status field or hardcoded phase checks. |
| Nested validation specs | Align planning admission with the existing executor's supported shapes. | Deferring the mismatch keeps an admitted unusable planning rule; requires explicit exclusion rather than a false holistic-completion claim. |
| Compatibility / verification | Clean break for corrected semantics, no bridge/alias for silently ignored inputs; preserve supported create/update/readback behavior. Adapt valuable behavior tests. | Preserving ignored inputs needs an explicit compatibility promise with low functional value. No new tests for the purpose of preserving obsolete behavior. |

The strategy table records the options originally presented. The owner initially defined supplied total as the desired whole-plan size after save/update. The subsequent 2026-10-09 discussion supersedes that input direction: total is computed from the valid resulting plan and returned/persisted, not supplied as a deletion signal. Complete-block mutation and common result validation remain. Git-backed deletion protection was initially a tentative exploration. The owner now includes reliable decoded implementation-cycle evidence in scope; see Approved Strategy and the remaining evidence boundaries below.

### Git-backed cycle protection — direction and remaining boundaries

The owner requires completed cycles to remain non-deletable, but does not assume a reliable completed status. The selected evidence direction is narrower: an implementation execution commit attributable to this issue and cycle protects the cycle from deletion, even while work is ongoing. The owner includes supporting codec corrections and dependency cleanup in scope to make this derivation reliable. Evidence of execution is not proof of completion; precise history access, attribution and failure policy remain to be defined.

| Evidence / boundary | Observed fact or unresolved requirement |
|---|---|
| Existing commit trace | GitCommitTool requires cycle_number in a configured cycle-based phase. GitManager formats type(scope): message (#issue); ScopeEncoder emits, for example, P_IMPLEMENTATION_SP_C1_GREEN. Local history includes 631b32f0 with this scope and issue #483. |
| Missing trace without subphase | ScopeEncoder.generate_scope returns P_PHASE immediately when sub_phase is None, ignoring a supplied cycle_number. Commit admission permits this case. Absence of a cycle marker is therefore not currently proof that no cycle execution commit exists. |
| Existing decoder | ScopeDecoder detects phase and a composite sub_phase such as c1_green; PhaseDetectionResult has no cycle_number field. A trustworthy cycle query is not already provided by this decoder. |
| Existing history reader | GitAdapter.get_recent_commits returns a limited list of subject strings (default five), without commit identities or an issue-branch history boundary. It is insufficient for an exhaustive deletion decision. |
| Trace meaning and workphase | A commit merely listing a future cycle in planning is not execution evidence. The decoded workphase is an active filter: only implementation-cycle commits may mark this issue's cycle as historical/protected. Require a distinct decoded cycle_number, not a subphase label such as c2. Evidence must also belong to the relevant issue and execution history; inherited C1 commits from other issues must not protect this issue's C1. Exact reachable-history and branch-basis semantics remain to be chosen. |
| Revert and exceptional repair | Reverting changes does not erase the execution commit from reachable history, so the proposed protection remains. Removing/replacing history is exceptional repair outside this issue; no normal-workflow bypass is proposed. Reflogs, dangling objects and unrelated refs are not assumed to define the guard. |
| Deletion versus edit | Evidence-based non-deletion does not itself freeze a cycle's name, criteria or deliverables, nor prove completion. Renumbering/replacement must not silently reinterpret an evidenced cycle identity. |
| State coherence without extra protection | Active/entered/touched state is not an independent reason to block planning mutations. Commit evidence alone defines cycle deletion/renumbering protection. Keep state references coherent when an uncommitted current/last cycle is removed or shifted; the exact mapping/reset behavior remains open and must not silently become a state-only immutability rule. |
| Failure, force and history boundary | Investigate the active branch history without a last-N cutoff and qualify evidence by relevant issue/workphase/cycle. If reliable commit derivation fails, reject the update by default. The owner permits an explicit force input after agent-human or agent-agent investigation establishes that the mutation is justified, or manual repair through safe_edit_file. Force overrides the uncertain-evidence block, not known commit protection or plan validity. Closed issues/historical formats still have no compatibility requirement. |

Candidate seam: a narrow injected read-only execution-evidence boundary at the planning command, with Git access owned by the existing Git layer and shared identity/encoding conventions. Pure planning models remain free of Git/state IO. Correcting trace completeness and defining exhaustive evidence would add a bounded Git-contract surface; this cost must be weighed before adopting the route. No new completion registry or general audit architecture is implied.

### Subphase admission and cycle-trace completeness

cycle_number identifies the planning/execution cycle; sub_phase identifies the kind of work within it. They are independent inputs. Their current coupling is an encoding choice: ScopeEncoder includes Cn only inside a scope with a subphase.

| Current boundary | Source-confirmed behavior |
|---|---|
| Public input | GitCommitInput permits omitted cycle_number and sub_phase. Dynamic requirements belong to runtime resolution, not a pure input model reading configuration/state. |
| Runtime phase/cycle admission | GitCommitTool resolves the active workflow, requires cycle_number when its phase has cycle_based=true, and applies the injected phase/cycle mismatch guard. No analogous subphase-required check exists. Both explicit-phase and auto-detected-phase routes use the cycle requirement. |
| Config split | contracts.yaml defines workflow-specific cycle_based, subphases and commit_type_map; workphases.yaml defines the phase catalog and the subphase whitelist used by ScopeEncoder. Current feature/bug/hotfix/refactor implementation contracts are cycle-based with red/green/refactor; chore implementation is not cycle-based. A rule keyed only to the name implementation would be incorrect. |
| Validity versus requirement | ScopeEncoder validates a supplied subphase against the workphase catalog. resolve_commit_type uses the workflow's commit_type_map when no explicit commit_type is given. Neither makes omitted subphase mandatory. An explicit commit_type must not bypass future subphase admission. |
| Config guarantees | PhaseContractPhase currently requires a nonempty commit_type_map for cycle-based phases. It does not prove nonempty subphases or agreement between workflow subphases, mapping keys and the workphase catalog. The inspected ConfigLoader validates these models separately. |
| Intentional old encoding | test_cycle_number_without_subphase_ignored explicitly expects P_IMPLEMENTATION when cycle_number=1 and no subphase is supplied. This is existing documented behavior, not an untested accidental branch. The new trace promise would require an explicit clean-break decision. |
| Side effects | GitCommitTool performs its cycle-required check before record_sub_phase, staging and commit. The equivalent subphase admission belongs before these mutations. current_sub_phase is recorded by the commit command and cleared at phase/cycle transitions; it is not a separate enforced execution mode. |

The earlier proposed mandatory-subphase route is withdrawn as the recommendation. The owner correctly challenged its premise: a cycle is not a subphase, and requiring one merely to preserve a cycle marker would impose workflow behavior to accommodate an encoding limitation.

Historical origin is source-confirmed: #138 described cycle_number as optional multi-cycle TDD metadata and used P_TDD_SP_C1_RED; the initial encoder commit c13fdeff7caab97aeb0cd41542568c56068efb1f (2026-02-15) already returned a phase-only scope before inspecting cycle_number when sub_phase was absent. #146 then strengthened cycle admission around TDD subphases using that format. This explains the implementation history, not a necessary dependency between cycle identity and subphase.

Current state already models current_cycle and current_sub_phase independently. WorkflowStatusResolver reads those distinct fields directly from state; commit decoding is not its current status source. Conversely, ScopeDecoder has no typed cycle field and returns c1_green as a composite sub_phase for P_IMPLEMENTATION_SP_C1_GREEN. Thus both encoding and any reader used for future Git evidence must distinguish cycle identity from subphase without inferring that one requires the other.

| Independent semantic combination | Required meaning, subject to active workflow admission |
|---|---|
| Phase only | Preserve phase identity; no cycle or subphase asserted. |
| Phase + cycle | Preserve the explicit cycle identity even when subphase is absent. |
| Phase + subphase | Preserve the configured subphase; do not infer a cycle from labels such as planning subphase c1. |
| Phase + cycle + subphase | Preserve both distinct values. |

Revised bounded direction for owner review: retain the existing runtime requirement for cycle_number in cycle-based phases and remove the encoder's loss of cycle identity when sub_phase is omitted. Keep subphase validation when supplied; a future subphase requirement would need its own workflow-policy rationale, not Git trace retention. No new execution mode, forced RED/GREEN/REFACTOR sequence, completion registry or extra config flag is implied.

Two bounded representation choices remain: extend the current spelling with an unambiguous cycle-only form while leaving combined spelling unchanged, or adopt one uniform spelling with separate cycle and subphase components. The latter has a broader encoder/decoder/doc/test impact; the former minimizes changed combined scopes. The owner now requires a shared lossless semantic contract and excludes historical compatibility requirements; exact syntax and result shape remain Design inputs. Future scopes need not recover omitted cycle identity from old commits.

The earlier optional encoder rejection for cycle_number without sub_phase is also withdrawn as a preferred solution: it rejects a semantically valid combination instead of representing it. Public input DTOs and state field meanings need not be coupled or redesigned to fix this boundary. Existing behavioral tests that expect information loss would be adapted to the new contract, with proportional encoding/decoding and command admission coverage; no old-behavior compatibility tests or content-mirroring coverage are proposed.

### Scope consumer register — required before selecting the route

Owner prerequisite: fully inventory active code and test consumers before choosing independent scope representation. This register is tied to source revision 6dc9930448ddc37741730d083854766902253e42; later production/test changes require refreshing it. No encoding strategy is approved merely because this inventory exists.

**Audit method and completeness boundary.** Start with `git ls-files -- '*.py'`: 475 tracked Python files, of which all 469 under mcp_server/, tests/ and scripts/ were parsed with Python ast. The other six are historical examples under docs/development/archive/issue52 or issue72. Inspect Import/ImportFrom aliases, constructor and method Call nodes for ScopeEncoder, ScopeDecoder, PhaseDetectionResult, CommitPhaseDetector, generate_scope, detect_phase, detect_from_commit, commit_with_scope and prepare_submission. Cross-check with `rg -n 'ScopeEncoder|ScopeDecoder|PhaseDetectionResult|CommitPhaseDetector|generate_scope|detect_phase|detect_from_commit|commit_with_scope|prepare_submission|raw_scope' mcp_server tests -g '*.py'`, scope literals, result constructors, private injected fields, get_recent_commits/iter_commits/message readers, exports and dynamic scope references. Separately enumerate shared helper calls, every explicit scope_decoder/commit_phase_detector keyword injection, and search tracked active Markdown/config/template/JS files.

Observed: zero active Python parse errors, zero tracked active text read errors, no alternate scope parser, no alias/dynamic scope call missed by the literal cross-check, and no scope exports in mcp_server/core/__init__.py or schemas/__init__.py. The initial filesystem-wide rg encountered an inaccessible generated .pytest_cache_ci directory; the tracked-file audit does not depend on that cache and git_status reported no untracked workspace files. These are source-inventory results, not executed tests or proof of a future implementation. Repository-external callers and historical Git messages remain a separate compatibility/evidence decision.

#### Active code, transport and policy boundaries

| Entry point / file | Role | Dependency and impact |
|---|---|---|
| [mcp_server/core/scope_encoder.py](<../../../mcp_server/core/scope_encoder.py>) — ScopeEncoder.generate_scope | Definition / writer | Encodes phase/subphase/cycle; missing-subphase information loss is the changed contract. |
| [mcp_server/managers/git_manager.py](<../../../mcp_server/managers/git_manager.py>) — commit_with_scope; prepare_submission | Direct encoder caller; internal indirect writer | Two encoder calls are validation/normal formatting within the same command. prepare_submission generates a phase-only Ready neutralization commit; do not accidentally require a cycle there. |
| [mcp_server/tools/git_tools.py](<../../../mcp_server/tools/git_tools.py>) — GitCommitTool.execute; GitCommitInput; guard/type callbacks | Public indirect writer / policy | Passes phase, cycle and subphase independently. Runtime phase/cycle policy and input admission are separate from scope spelling. |
| [mcp_server/tools/pr_tools.py](<../../../mcp_server/tools/pr_tools.py>) — SubmitPRTool.execute | Indirect writer | Calls prepare_submission, which may commit before PR creation. Its phase-only scope is a material preservation case. |
| [mcp_server/adapters/git_adapter.py](<../../../mcp_server/adapters/git_adapter.py>) — commit; get_recent_commits | Opaque transport / history reader | Persists the supplied message and returns subject strings. Does not parse phase/cycle/subphase; no hidden alternate scope grammar found. |
| [mcp_server/core/phase_detection.py](<../../../mcp_server/core/phase_detection.py>) — ScopeDecoder; PhaseDetectionResult | Definition / reader / result shape | Owns the only repository scope regex parser. Six-field TypedDict currently returns composite c1_green as sub_phase; all success/unknown result constructors belong here. |
| [mcp_server/core/commit_phase_detector.py](<../../../mcp_server/core/commit_phase_detector.py>) — CommitPhaseDetector.detect_from_commit | Only direct production decoder invocation | Constructs ScopeDecoder and returns its result; has its own unknown-result constructor requiring coordination if the result shape changes. |
| [mcp_server/bootstrap.py](<../../../mcp_server/bootstrap.py>) — manager/tool construction | Composition | Creates/injects ScopeDecoder, CommitPhaseDetector and commit command guards. Imports do not establish a live parsing consumer. |
| [mcp_server/managers/phase_state_engine.py](<../../../mcp_server/managers/phase_state_engine.py>) — constructor; _scope_decoder | Passive injection | Stores the decoder at line 105; no invocation/reference beyond declaration/assignment in this module. Cycle execution itself uses plan/state. |
| [mcp_server/managers/workflow_status_resolver.py](<../../../mcp_server/managers/workflow_status_resolver.py>) — constructor; resolve_current; _detector | Passive injection / state reader | Stores the detector but never calls it. resolve_current uses state exclusively; no active status fallback from commit scope. |
| [mcp_server/managers/project_manager.py](<../../../mcp_server/managers/project_manager.py>) — get_project_plan | State-status consumer, not decoder consumer | Uses WorkflowStatusResolver and its state-derived DTO, not PhaseDetectionResult. An old test comment naming ScopeDecoder does not change that route. |
| [mcp_server/tools/discovery_tools.py](<../../../mcp_server/tools/discovery_tools.py>) — GetWorkContextTool.execute | State-status consumer, not decoder consumer | Reports state-derived phase/subphase/cycle; does not read commit messages. |
| [mcp_server/schemas/tool_outputs.py](<../../../mcp_server/schemas/tool_outputs.py>) — GitCommitOutput; WorkContextOutput | Public DTO / presentation boundary | Cycle and subphase are already separate fields. No encoded-scope field or PhaseDetectionResult is exposed here. |
| [mcp_server/core/interfaces/git.py](<../../../mcp_server/core/interfaces/git.py>) — IGitContextReader.get_recent_commits | Read-only transport contract | Exposes subject strings, not a scope parse result. No cycle-attribution query exists. |
| [mcp_server/managers/phase_contract_resolver.py](<../../../mcp_server/managers/phase_contract_resolver.py>) — is_cycle_based_phase; resolve_commit_type | Sibling policy consumer | Reads configured cycle policy and supplied subphase, never an encoded/decoded scope. |
| [mcp_server/config/schemas/workphases.py](<../../../mcp_server/config/schemas/workphases.py>) — WorkphasesConfig / PhaseDefinition | Encoder/decoder config input | Injected phase catalog and subphase whitelist; no cycle encoding grammar in config. |
| [mcp_server/config/schemas/contracts_config.py](<../../../mcp_server/config/schemas/contracts_config.py>) — WorkflowPhaseEntry | Runtime policy input | Workflow-specific cycle_based/subphases/map; does not consume scope text. |

The producer chain is GitCommitTool.execute → GitManager.commit_with_scope → ScopeEncoder.generate_scope → GitAdapter.commit. The second writer chain is SubmitPRTool.execute → GitManager.prepare_submission → commit_with_scope. The decoder chain is CommitPhaseDetector.detect_from_commit → ScopeDecoder.detect_phase, but the current production composition only injects this wrapper into a state-only resolver: no normal production caller invokes detect_from_commit. The decoder remains directly exercised by tests and is a potential future Git-evidence reader. Passive injection must not be presented as active parsing, and cleanup of these passive dependencies is not implied by this issue.

#### Test and fixture consumers

| File | Actual role | Impact / preservation boundary |
|---|---|---|
| [tests/mcp_server/core/test_scope_encoder.py](<../../../tests/mcp_server/core/test_scope_encoder.py>) | Direct encoder behavior | Exact combined-scope expectation and deliberate ignored-cycle-without-subphase expectation; adapt affected behavior rather than preserve information loss. |
| [tests/mcp_server/core/test_phase_detection.py](<../../../tests/mcp_server/core/test_phase_detection.py>) | Direct decoder / TypedDict | Phase-only/subphase grammar, six-field typed fixture and unknown fallback. Result-shape changes invalidate fixture construction even when existing asserts do not fail. |
| [tests/mcp_server/integration/test_workflow_cycle_e2e.py](<../../../tests/mcp_server/integration/test_workflow_cycle_e2e.py>) | Real encoder → Git → decoder | Explicitly expects sub_phase=c1_red/c1_green/c1_refactor. This is a real semantic consumer, not merely a scope string fixture. |
| [tests/mcp_server/unit/managers/test_workflow_status_resolver.py](<../../../tests/mcp_server/unit/managers/test_workflow_status_resolver.py>) | Mixed wrapper and state-only tests | TestCommitPhaseDetector calls the wrapper directly. Resolver tests inject it but use state; commit-string fixtures there are not live decoder calls. |
| [tests/mcp_server/unit/managers/test_git_manager.py](<../../../tests/mcp_server/unit/managers/test_git_manager.py>) | Real encoder through manager; PR preparation | Checks full message forms, cycle scope, type override, issue suffix and prepare_submission. Several phase-only preservation cases. |
| [tests/mcp_server/managers/test_git_manager_config.py](<../../../tests/mcp_server/managers/test_git_manager_config.py>) | Real encoder through manager | Configuration-backed phase/subphase validation and message expectations. |
| [tests/mcp_server/unit/managers/test_git_manager_no_file_open.py](<../../../tests/mcp_server/unit/managers/test_git_manager_no_file_open.py>) | Real encoder through manager | No-IO boundary plus exact combined C1/C2 scope expectations; syntax changes can affect these otherwise unrelated invariants. |
| [tests/mcp_server/unit/managers/test_git_manager_skip_paths.py](<../../../tests/mcp_server/unit/managers/test_git_manager_skip_paths.py>) | Real encoder through manager / transport | Calls cycle commits while asserting skip-path forwarding; no independent decoder. |
| [tests/mcp_server/unit/integration/test_git.py](<../../../tests/mcp_server/unit/integration/test_git.py>) | Real encoder through manager | Exact cycle-scoped message expectation. |
| [tests/mcp_server/unit/tools/test_git_tools.py](<../../../tests/mcp_server/unit/tools/test_git_tools.py>) | Mixed real manager and mocked manager | Most tests assert parameter forwarding/policy; test_git_commit_integration_workflow_phases uses a real manager/encoder and asserts a complete cycle-scoped message. |
| [tests/mcp_server/test_support.py](<../../../tests/mcp_server/test_support.py>) | Shared passive constructors | make_project_manager creates the detector; make_phase_state_engine creates the decoder. Full caller register below. |
| [tests/mcp_server/unit/tools/test_discovery_tools.py](<../../../tests/mcp_server/unit/tools/test_discovery_tools.py>) | State-only consumer / old scope fixtures | Commit-shaped strings are provided to fake Git context; phase/cycle/subphase come from state. No actual decoder invocation. |
| [tests/mcp_server/unit/managers/test_project_manager.py](<../../../tests/mcp_server/unit/managers/test_project_manager.py>) | State-only consumer / stale documentation | Old ScopeDecoder wording is a comment; the current behavior follows injected state-status resolver. |
| [tests/mcp_server/unit/integration/test_all_tools.py](<../../../tests/mcp_server/unit/integration/test_all_tools.py>) | Mocked commit command | make_git_commit_tool and commit_with_scope.assert_called_once_with verify forwarded values, not encoded scope spelling. |
| [tests/mcp_server/unit/managers/test_enforcement_runner_unit.py](<../../../tests/mcp_server/unit/managers/test_enforcement_runner_unit.py>) | Mocked commit command / notes | NoteContext wiring; does not execute an encoder or decode scope. |
| [tests/mcp_server/unit/tools/test_submit_pr_tool.py](<../../../tests/mcp_server/unit/tools/test_submit_pr_tool.py>) | Mocked PR preparation | Asserts delegation to prepare_submission and no direct tool call to commit_with_scope. |
| [tests/mcp_server/integration/test_submit_pr_atomic_flow.py](<../../../tests/mcp_server/integration/test_submit_pr_atomic_flow.py>) | Mocked PR transaction | Uses mocked prepare_submission results/failures; no hidden encoder assertion despite integration path/name. |
| [tests/mcp_server/unit/adapters/test_git_adapter.py](<../../../tests/mcp_server/unit/adapters/test_git_adapter.py>) | Opaque Git primitives | prepare_submission mention documents raw operations; no scope grammar consumption. |
| [tests/mcp_server/unit/adapters/test_git_adapter_neutralize_to_base.py](<../../../tests/mcp_server/unit/adapters/test_git_adapter_neutralize_to_base.py>) | Opaque phase-only message fixture | Ready message is supplied directly; no encoding/decoding call. |
| [tests/mcp_server/unit/test_c260_c2_state_root_injection.py](<../../../tests/mcp_server/unit/test_c260_c2_state_root_injection.py>) | Direct mocked decoder injection / adjacent guard | Two PhaseStateEngine constructor calls inject MagicMock as scope_decoder; also uses build_phase_guard. State-root/contract behavior, not scope parsing. |
| [tests/mcp_server/unit/managers/test_consumers_c4.py](<../../../tests/mcp_server/unit/managers/test_consumers_c4.py>) | Direct mocked decoder injection | _build_engine passes MagicMock as scope_decoder directly to PhaseStateEngine, outside shared helpers. Constructor/transition contract test; decoder is stored, not invoked. |
| [tests/mcp_server/integration/templates/test_commit_artifact.py](<../../../tests/mcp_server/integration/templates/test_commit_artifact.py>) | Parallel generic commit-template route | Caller-authored scope, independent of ScopeEncoder/ScopeDecoder. |
| [tests/mcp_server/integration/adapters/test_commitlint.py](<../../../tests/mcp_server/integration/adapters/test_commitlint.py>) | Parallel native commit check | Configured commitlint behavior, independent of pgmcp phase/cycle decoding. |
| [tests/mcp_server/integration/test_installed_distribution_v3.py](<../../../tests/mcp_server/integration/test_installed_distribution_v3.py>) | Distribution / generic commit route | Packaging/install surface for configured commit check; not another workflow scope parser. |

#### Complete shared-helper caller register

The AST audit found 28 files and 246 direct calls to make_project_manager, make_phase_state_engine or make_git_commit_tool, including helper-to-helper calls. Counts identify construction coupling, not test count or decode executions. The first two construct passive detector/decoder dependencies as described above; the third creates a mocked-manager commit tool. These callers do not automatically need edits when only scope representation changes.

| Caller file | Observed helper calls |
|---|---|
| [tests/mcp_server/integration/templates/test_planning_artifact.py](<../../../tests/mcp_server/integration/templates/test_planning_artifact.py>) | make_project_manager: 2 call(s) |
| [tests/mcp_server/integration/test_context_loaded_enforcement.py](<../../../tests/mcp_server/integration/test_context_loaded_enforcement.py>) | make_project_manager: 1 call(s); make_phase_state_engine: 1 call(s) |
| [tests/mcp_server/integration/test_issue39_cross_machine.py](<../../../tests/mcp_server/integration/test_issue39_cross_machine.py>) | make_project_manager: 1 call(s); make_phase_state_engine: 1 call(s) |
| [tests/mcp_server/integration/test_project_plan_readback.py](<../../../tests/mcp_server/integration/test_project_plan_readback.py>) | make_project_manager: 1 call(s) |
| [tests/mcp_server/integration/test_target_startup.py](<../../../tests/mcp_server/integration/test_target_startup.py>) | make_project_manager: 1 call(s) |
| [tests/mcp_server/integration/test_workflow_cycle_e2e.py](<../../../tests/mcp_server/integration/test_workflow_cycle_e2e.py>) | make_project_manager: 1 call(s); make_phase_state_engine: 1 call(s) |
| [tests/mcp_server/test_support.py](<../../../tests/mcp_server/test_support.py>) | make_project_manager: 1 call(s) |
| [tests/mcp_server/unit/integration/test_all_tools.py](<../../../tests/mcp_server/unit/integration/test_all_tools.py>) | make_git_commit_tool: 3 call(s) |
| [tests/mcp_server/unit/managers/test_phase_state_engine.py](<../../../tests/mcp_server/unit/managers/test_phase_state_engine.py>) | make_project_manager: 33 call(s); make_phase_state_engine: 31 call(s) |
| [tests/mcp_server/unit/managers/test_phase_state_engine_c1.py](<../../../tests/mcp_server/unit/managers/test_phase_state_engine_c1.py>) | make_project_manager: 1 call(s) |
| [tests/mcp_server/unit/managers/test_phase_state_engine_c2.py](<../../../tests/mcp_server/unit/managers/test_phase_state_engine_c2.py>) | make_project_manager: 1 call(s); make_phase_state_engine: 3 call(s) |
| [tests/mcp_server/unit/managers/test_phase_state_engine_c3.py](<../../../tests/mcp_server/unit/managers/test_phase_state_engine_c3.py>) | make_project_manager: 3 call(s); make_phase_state_engine: 3 call(s) |
| [tests/mcp_server/unit/managers/test_phase_state_engine_c3_issue257.py](<../../../tests/mcp_server/unit/managers/test_phase_state_engine_c3_issue257.py>) | make_project_manager: 1 call(s); make_phase_state_engine: 2 call(s) |
| [tests/mcp_server/unit/managers/test_phase_state_engine_c4_issue257.py](<../../../tests/mcp_server/unit/managers/test_phase_state_engine_c4_issue257.py>) | make_project_manager: 2 call(s); make_phase_state_engine: 2 call(s) |
| [tests/mcp_server/unit/managers/test_phase_state_engine_parent_branch.py](<../../../tests/mcp_server/unit/managers/test_phase_state_engine_parent_branch.py>) | make_project_manager: 3 call(s); make_phase_state_engine: 3 call(s) |
| [tests/mcp_server/unit/managers/test_phase_state_engine_persistence.py](<../../../tests/mcp_server/unit/managers/test_phase_state_engine_persistence.py>) | make_project_manager: 1 call(s); make_phase_state_engine: 1 call(s) |
| [tests/mcp_server/unit/managers/test_phase_state_engine_workflow.py](<../../../tests/mcp_server/unit/managers/test_phase_state_engine_workflow.py>) | make_project_manager: 1 call(s); make_phase_state_engine: 1 call(s) |
| [tests/mcp_server/unit/managers/test_project_manager.py](<../../../tests/mcp_server/unit/managers/test_project_manager.py>) | make_project_manager: 13 call(s) |
| [tests/mcp_server/unit/managers/test_state_repository.py](<../../../tests/mcp_server/unit/managers/test_state_repository.py>) | make_project_manager: 1 call(s); make_phase_state_engine: 1 call(s) |
| [tests/mcp_server/unit/test_server.py](<../../../tests/mcp_server/unit/test_server.py>) | make_project_manager: 2 call(s); make_phase_state_engine: 2 call(s) |
| [tests/mcp_server/unit/tools/test_c7_tool_conflict_handling.py](<../../../tests/mcp_server/unit/tools/test_c7_tool_conflict_handling.py>) | make_phase_state_engine: 1 call(s); make_project_manager: 4 call(s) |
| [tests/mcp_server/unit/tools/test_cycle_tools.py](<../../../tests/mcp_server/unit/tools/test_cycle_tools.py>) | make_project_manager: 3 call(s); make_phase_state_engine: 3 call(s) |
| [tests/mcp_server/unit/tools/test_cycle_tools_business_logic.py](<../../../tests/mcp_server/unit/tools/test_cycle_tools_business_logic.py>) | make_project_manager: 20 call(s); make_phase_state_engine: 20 call(s) |
| [tests/mcp_server/unit/tools/test_discovery_tools.py](<../../../tests/mcp_server/unit/tools/test_discovery_tools.py>) | make_project_manager: 4 call(s); make_phase_state_engine: 4 call(s) |
| [tests/mcp_server/unit/tools/test_force_phase_transition_tool.py](<../../../tests/mcp_server/unit/tools/test_force_phase_transition_tool.py>) | make_project_manager: 15 call(s); make_phase_state_engine: 10 call(s) |
| [tests/mcp_server/unit/tools/test_initialize_project_tool.py](<../../../tests/mcp_server/unit/tools/test_initialize_project_tool.py>) | make_project_manager: 1 call(s); make_phase_state_engine: 1 call(s) |
| [tests/mcp_server/unit/tools/test_project_tools.py](<../../../tests/mcp_server/unit/tools/test_project_tools.py>) | make_project_manager: 30 call(s); make_phase_state_engine: 1 call(s) |
| [tests/mcp_server/unit/tools/test_transition_phase_tool.py](<../../../tests/mcp_server/unit/tools/test_transition_phase_tool.py>) | make_project_manager: 2 call(s); make_phase_state_engine: 2 call(s) |

#### Other active surfaces and closure

The commit template ([schema](<../../../.pgmcp/template_suite/commit/context.schema.json>), [renderer](<../../../.pgmcp/template_suite/commit/template.jinja2>)) accepts a caller-owned generic scope and does not call either codec. [checks.yaml](<../../../.pgmcp/config/checks.yaml>) routes commit_preflight to commitlint; [commitlint.config.cjs](<../../../commitlint.config.cjs>) configures nonempty type/subject without a pgmcp scope grammar. Workphases/config and active [Git reference](<../../reference/tools/git.md>), [GitHub reference](<../../reference/tools/github.md>), [enforcement diagram](<../../manuals/architectural_diagrams/04_enforcement_layer.md>) and [runtime diagram](<../../manuals/architectural_diagrams/06_runtime_flows.md>) contain scope descriptions/examples. Active .agents/.github instructions and scripts/build_package.py contain no additional codec/parser consumer; no tracked .github/workflows scope rule was found. Historical docs are rationale, not migration targets.

Independent review by Beoordeel designplan on commit d108a3ba88b04d930e8908549d2ebc6c867b1dc9 reproduced 475 tracked/469 active Python files, zero parse errors and the exact 28-file/246-call helper register. It confirmed writer/reader chains, passive injections, fallback/result shape and real-versus-mocked test classifications. One P3 omission was found: direct mocked decoder injection in test_consumers_c4.py. The row above resolves it; the state-root test row now also states its direct injections explicitly. A follow-up AST keyword scan over all 469 files found 12 explicit decoder/detector injection sites across bootstrap and four test/helper files (test_support.py, test_workflow_status_resolver.py, test_consumers_c4.py and test_c260_c2_state_root_injection.py); each is registered. No code or tests changed or ran for this correction.

QA assessed the inventory as sufficient for owner discussion, with the P3 addition needed for literal completeness. This assessment is not approval of a scope strategy or a phase transition; Research remains open.

Inventory closure requires every new codec/result consumer or scope literal discovered later to be assigned to one of these entries before Design/implementation changes. Syntax-only and semantic changes have different impact: changing combined spelling affects exact message assertions; separating decoded cycle/subphase also affects the E2E assertions and typed/fallback result constructors. Existing useful behavior coverage is the starting point; mocked/passive consumers do not justify blanket test rewrites.

### Caution and bounded dependency cleanup

The owner asks for caution about changing encoder/decoder cycle/subphase agreements and now explicitly includes the shared lossless codec contract and removal of unused state/status injections in #491's supporting scope. This authorizes their inclusion in the subsequent design/implementation, not a production patch during Research or a specific new scope spelling.

The material decisions are distinct: changing decoded c1_green to separate values changes a tested result contract; omitted subphase currently bypasses the workflow commit_type_map and falls back to the workphase hint (or chore); complete cycle identity must survive before Git-backed deletion protection can rely on it. The owner excludes closed issues and historical commits from migration requirements and accepts manual updates in all other workspaces. Evaluate scope spellings for clarity and bounded consumer cost rather than historical compatibility; no broader notation rewrite is approved merely by that exclusion.

The verified narrow cleanup surface is three production files: remove the unused ScopeDecoder constructor parameter/import/stored field from PhaseStateEngine, remove the unused CommitPhaseDetector parameter/import/stored field from WorkflowStatusResolver, and remove the corresponding construction/injection from bootstrap. Four shared/direct test files carry the affected injection setup: test_support.py, test_workflow_status_resolver.py, test_consumers_c4.py and test_c260_c2_state_root_injection.py. The 28 helper caller files do not all require edits when helpers retain their used contract. This cleanup can preserve runtime behavior and needs no ignored constructor parameters, legacy aliases or compatibility bridge.

Removing those injections does not imply deleting ScopeDecoder, which has real E2E/direct test consumers. The wrapper's retention/removal is a separate choice: it has direct behavior tests but no current production callers; do not silently broaden injection cleanup into module deletion or speculative future wiring. The scope consumer register describes the current source until an approved implementation changes it.

### Planning spans cycles and phase deliverables

CyclePlanningModel admits four independent optional blocks: cycles, design, validation and documentation. The cycles block alone has total and numbered cycles; each cycle has its own deliverables and exit_criteria. The other three blocks each contain a deliverables list without cycle numbers or a cycle total. The project envelope also carries issue/workflow metadata; deliverables.json is not an implementation-only artifact.

PhaseContractResolver selects the cycles list when the active workflow phase is configured cycle_based and a cycle number is supplied; otherwise it selects the phase-named block. The current cycle-based contracts are implementation in feature/bug/hotfix/refactor; chore implementation is not cycle-based. There is one shared cycles block rather than a separate numbered-cycle plan per workphase. Supporting multiple independently numbered cycle-based phases is not implied or added by this issue.

Save and update act on the issue's whole planning_deliverables aggregate, not only the active phase. The owner-approved total/range/non-deletion rules apply to the cycles block. A cycle-only update leaves the phase blocks unchanged. A phase-only update has no cycle-range/removal intent; the supplied blocks are incorporated before common whole-result validation. Current phase lists merge by deliverable ID, just as cycle deliverable lists do; that current merge behavior must not be confused with the requested complete-block mutation.

Bounded proposal, still requiring owner agreement: apply the same complete-block rule to a supplied phase block, replacing that phase's full deliverables list and retaining unprovided phase blocks. This allows deliberate removal within the supplied list without nested patch semantics. Do not extend cycle total or Git-backed cycle protection to phase deliverables. Omission, explicit null, empty-list meaning and any separate phase-deliverable protection remain explicit boundary choices.

### Approved single-cycle-phase configuration limit

On 2026-10-09 the owner includes a bounded behavioral repair: each workflow may configure at most one cycle_based workphase. Zero remains valid. Reject a workflow with multiple such phases at the existing WorkflowEntry configuration-validation boundary; report the conflicting phase entries rather than sharing one plan/state position across them. This is a clean restriction of an unsafe admitted combination, with no compatibility bridge or workphase-specific cycle storage. The current workspace contracts already satisfy it.

The limit concerns multiplicity, not a hardcoded phase name: a workflow with Design as its sole cycle-based phase remains admissible. Current workspace workflows use Implementation as the sole cycle-based phase. Runtime phase ownership stays configuration-driven; this repair does not introduce independently numbered cycles per workphase.

Daily agent guidance and runtime admission have separate roles. GetWorkContextTool returns the active workflow phase's phase_instructions from contracts.yaml. These instructions direct cycle planning/execution, focused evidence, subphase-labelled commits and when to request a cycle transition. The structured cycle_based field determines whether tooling enables cycle progression, selects cycle deliverables and requires a cycle number for commits. Instructions are interpreted by the agent, not parsed as executable guards; instruction/config coherence must remain explicit. The new cardinality constraint belongs to the structured configuration model, not repeated prose checks.

### Owner-confirmed state and codec boundary

The owner identifies the unused decoder injections as remnants of the earlier attempt to derive workflow position from commits. This explanation is consistent with the verified current-source boundary: workflow status comes from state.json and neither PhaseStateEngine nor WorkflowStatusResolver invokes its injected decoding dependency. This records the owner's migration rationale, not an additional historical-source audit.

State.json remains the single source of truth for current branch workflow state. The retained decoder's proposed new role is reading execution metadata from commits for cycle evidence; it must not determine or advance current workflow state.

Owner-approved codec invariant: encoder and decoder use the same configured vocabulary and reproduce the same distinct phase, optional cycle number and optional subphase. For every admitted combination, decoding the generated scope must return those values, including absence, without conflating cycle with subphase or dropping cycle identity. A cycle does not require a subphase. The commit type, subject and issue attribution are separate full-commit concerns; this invariant does not imply that a scope decoder alone establishes trustworthy issue/cycle evidence.

The owner confirms that closed issues and historical commits do not require compatibility. Other workspaces will be upgraded and manually adjusted where necessary. The codec boundary therefore needs no old-format fallback or legacy composite-subphase result. Exact spelling, typed result shape and any shared configuration seam belong to Design; choosing them must use the completed consumer register. The owner now includes reliable implementation-cycle evidence in scope, with decoded workphase as an active filter. Exhaustive issue-attributed history access and failure policy remain unresolved boundaries; the scope round-trip contract alone does not settle them.

### Latest owner direction — explicit operations, derived numbering and typed references

The detailed illustrative update JSON Schema was not approved. The owner explicitly returns to incremental Research discussion of data and behavior before selecting exact DTO/operation shapes. Do not treat required nullable fields, set/append spellings, missing-target policy or the illustrative ValidationSpec union as approved merely because they appeared in that proposal.

The owner requires explicit removal intent for both phase blocks and cycles. A lower total must not implicitly delete cycles. Total is derived after composing and validating the complete result, persisted for project readback and included in the response. Initial save uses list order for server-owned cycle numbering; later mutations must unambiguously identify affected existing cycles, with the exact request form still open.

Deletion may compact the numbering of unexecuted surviving cycles while retaining relative order. Reject the entire mutation if either a removed cycle has relevant execution commits or an evidenced surviving cycle would change number. The owner explicitly accepts this edge case: C_1 and C_3 have commits, so deleting uncommitted C_2 is rejected because C_3 would become C_2. Unworked cycles after the highest commit-protected cycle may compact subject to independent state-reference validity. This does not add a completed status. Handling references to a current/last uncommitted cycle remains open.

Public names are cycle_name and deliverable_name, replacing the existing cycle name and deliverable id vocabulary. The server supplies numeric references in save results and readback; names express intent, while numbers provide references. Owner convention: C_<cycle number> for a cycle, and D_<cycle number>.<deliverable number> for a deliverable belonging to that cycle, for example C_2 and D_2.1. This prevents deliverables from appearing to be subcycles. Commit scope must preserve the distinct workphase/cycle facts through the shared codec rather than relying on free-text subject references.

The owner requires server-generated cycle/deliverable identifiers to be persisted in deliverables.json, so a direct file read supplies the same references as tool readback. Generate identifiers during save and relevant updates before persistence; project tools expose the stored values rather than inventing a separate identity. Numeric/reference consistency is a resulting-plan invariant, not an independently editable caller field. Exact field spelling remains open. The owner confirms that a deliverable reference has meaning only inside its enclosing cycle or phase; no global uniqueness mechanism is required. Identical local identifiers in different phase blocks are acceptable because the parent block supplies deterministic context. Meaningful names aid human interpretation, but correctness does not rely on their statistical uniqueness. Exact phase reference formatting and behavior across temporal whole-block replacement remain to be finalized. Prefer clear public field names over speculative token savings; no tokenizer measurement or new performance claim is made.

### Owner-selected uncertainty and force policy

The owner deliberately simplifies the error policy on 2026-10-09 instead of requiring a taxonomy of hypothetical failures. Read deeply enough through commits on the active branch to establish the relevant evidence; the last-five-subject helper is insufficient and must not be the protection query. Keep the already agreed issue/workphase/cycle qualification.

The owner explicitly requires the read to start at the active branch HEAD. Capture the branch and its head SHA, then query from that exact commit backwards; do not search all refs or unrelated branch tips. This is local history reading, not a network git fetch. Starting at HEAD alone still includes inherited ancestry. Producer proposal for the lower boundary: exclude the branch basis derived from its configured parent and read the complete basis..head range without max-count, retaining issue/workphase/cycle qualification. This range restriction is a proposal to settle, not silently approved by the HEAD-start requirement.

If reliable derivation cannot be completed, reject update/mutation by default. This supersedes the producer's earlier proposal to allow some update kinds based on whether their effect needed Git evidence. A force flag in the update input explicitly permits bypassing that uncertainty rejection. Every invocation, including force=true, must attempt commit derivation again. If that attempt succeeds, apply normal commit protection; only if the attempt still fails may force permit writing despite the uncertainty. This is not an inference that missing evidence means no commits.

The intervening process is agent-human or agent-agent investigation using tools to diagnose why derivation failed. If that investigation justifies the mutation, the caller may use force; alternatively, continue rejecting the normal update and carry out an agreed manual repair with safe_edit_file. Manual repair is outside the guarded update path, not a hidden tool fallback. No new confirmation workflow or large failure-classification subsystem is requested.

Force concerns inability to establish evidence reliably. Confirmed commit-backed deletion/renumbering protection and complete-result schema validity remain binding; force must not discard already established positive protection or manufacture a valid plan. The forced result should identify the override and unresolved evidence problem rather than report a normal reliable-evidence result. Exact force field and output shape belong to Design.

### Explicit history-read extension — feasibility and impact

The owner requires evidence and impact analysis before treating a complete history reader as feasible within #491. On snapshot c84b407b1f1ecfc3335b2cd07587af34c50165c5, two read-only exploratory probes returned 4,337 commit subjects reachable from HEAD, with 15 commits in main..HEAD and the same 15 current-issue subjects. The checkout is not shallow. Native git log HEAD --format=%H%x09%s completed with exit 0 in 315 ms. A batch log call through the existing GitAdapter.repo.git and installed GitPython 3.1.45 returned the same counts in 159 ms. The existing get_recent_commits() returned only five subjects.

Execution examples at positions 26–28 belong to #483: d6f64173ba944449be4c5854185cfb3c503004cf, 631b32f08a92ec751fae95190ebc17eca0dfc9dd and 4a899fd8269fbe48e97632cfba2edb169db25789. This proves that a last-five selection misses real execution scopes and that inherited execution cycles must not protect #491. All 15 #491 commits at this snapshot are Research; no positive #491 implementation protection was demonstrated.

These probes establish local read feasibility using an existing dependency. They are one-checkout observations, not a latency guarantee, production evidence-query implementation, or end-to-end protection test. The Python probe used -B and made no production/test changes; no native test suite was run. The application import emitted an existing Pydantic field-shadow warning unrelated to history retrieval; no repair was attempted.

Durable reproduction route: inspect snapshot HEAD identity, run git rev-parse --is-shallow-repository, read git log HEAD --format=%H%x09%s without a max-count, compare git log main..HEAD --format=%H%x09%s, and locate the three subjects above. The installed-library probe instantiated GitAdapter with the repository path and used its existing Repo.git.log batch capability; get_recent_commits() remained unchanged.

| Boundary / entry point | Required impact / architectural limit |
|---|---|
| Git IO: [GitAdapter](<../../../mcp_server/adapters/git_adapter.py>) and [Git interfaces](<../../../mcp_server/core/interfaces/git.py>) | Introduce a narrow complete-history read contract returning commit identity/subject and sufficient branch-basis metadata. Keep Git traversal/commands in the adapter. The current last-N subject contract is insufficient; no large numeric cap may stand in for completeness. |
| Evidence interpretation: shared scope codecs and workflow/issue conventions | Decode workphase and distinct cycle, qualify issue ownership and produce protected cycle evidence. Configure phase vocabulary; no phase-name hardcoding or heuristic cycle attribution. Exact reader/result shape belongs to Design. |
| Planning command: [ProjectManager](<../../../mcp_server/managers/project_manager.py>) / [public update tool](<../../../mcp_server/tools/project_tools.py>) | Consume injected read-only evidence before persistence. Add explicit force with a fresh query on every call. Pure planning models retain structural validation and no Git/state IO. |
| Wiring: [bootstrap](<../../../mcp_server/bootstrap.py>) and [shared test support](<../../../tests/mcp_server/test_support.py>) | Construct/inject only the new evidence dependency and directly invalidated fixtures. Do not restore unused status-decoding injections. Avoid a ProjectManager/PhaseStateEngine dependency cycle. |
| Existing last-N consumers | GitManager forwards get_recent_commits; the real cycle E2E reads latest commits, and manager/discovery tests use the old helper/mocks. They do not need a blanket migration: use a distinct complete-history capability for protection and retain focused current-helper behavior. |
| Behavioral evidence | Prove evidence beyond five commits, exclusion of inherited/other-issue work, and protection against deletion/renumbering. Prove force invokes the reader again: recovered success uses ordinary protection; repeated failure with force may write. Adapt valuable existing tests; no historical-compatibility suite or per-Git-error test explosion. |
| References / producer artifacts | Update directly affected planning/Git references and #491 artifacts. No new public history tool, external service, dependency, persistent evidence cache, generic audit framework or broad agent/phase-instruction rewrite is required. |

Material remaining risks: branch-basis semantics and issue attribution must be explicit; a query must be tied to a known HEAD and errors must not become an empty success. This measurement does not settle simultaneous history changes or atomic coordination of planning with state-reference mapping. Preserve those limits for Design without developing a new event-sourcing/transaction architecture in Research.

Stored targets already identify blocks: a generated C_n/current cycle number identifies a cycle; the configured phase key identifies its phase block. Names convey meaning and need not serve as unique technical lookup keys. Remaining update discussion concerns the explicit operation form, not inventing a new target identity.

### Issue-qualified commit lookup and duplicate title markers

- The existing writer already appends the structured issue as ` (#N)`: [GitManager.commit_with_scope](../../../mcp_server/managers/git_manager.py). [GitCommitTool](../../../mcp_server/tools/git_tools.py) derives that issue from workflow state or branch conventions and forwards the caller's message unchanged. No duplicate-marker normalization exists. Active Research instructions in [contracts.yaml](../../../.pgmcp/config/contracts.yaml) explicitly request `message='Research findings (#N)'`, creating a reproducible double-suffix path. Read-only local inspection at HEAD `aafe9432c0fb5d96e4863702088b8d3df5455237` confirmed recent titles end in `(#491) (#491)`; producer messages also supplied the marker.
- Git natively supports issue preselection: `git log HEAD --fixed-strings --grep="(#491)" --format="%H %s"` searches HEAD ancestry without a last-N cutoff. A bounded display-only probe with `-n 4` returned the four recent #491 titles; production evidence selection must omit that limit. Since grep searches the complete message, selected subjects still require exact issue-marker validation and scope decoding. Issue filtering may make a mandatory parent-basis dependency unnecessary; this remains a producer alternative, not an approved replacement of the history boundary.
- Owner-proposed bounded repair: normalize occurrences of the matching structured issue number in the caller-supplied commit title, then append one canonical ` (#N)`. Preserve other issue references, larger numbers and the message body; do not rewrite existing commits. Exact admitted marker forms and title whitespace handling remain Design details. The existing GitManager title-assembly boundary owns this responsibility; GitAdapter remains an opaque Git transport and scope codecs retain only scope semantics.
- Existing behavior coverage in [test_git_manager.py](../../../tests/mcp_server/unit/managers/test_git_manager.py) verifies suffix addition and the no-issue case, but not duplicate normalization. Any later repair should adapt that bounded behavior surface. No production, configuration or test changes or test runs were made during this investigation.

### Existing evidence and proportional test surface

| Existing coverage | Value to retain | Material gap / coupling |
|---|---|---|
| test_project_manager.py complete save tests | Prior-save guard, required cycles, total consistency, sequential numbering, nonempty deliverables/exit criteria | No final merged-plan proof in the current update route. |
| test_project_tools.py save/update groups | Append, scoped merge/replacement, phase entries, exit-criteria change and invalid validates input | No direct name/null/total-conflict/invalid-new-cycle/lifecycle protection cases among inspected tests. Several assertions inspect persisted JSON directly. |
| GetProjectPlanTool readback tests | Full stored planning, order/criteria, initialized-without-planning support, invalid stored-plan rejection | Reuse this public query to observe approved future mutation behavior. |
| DeliverableChecker file_glob tests | Existing dir + pattern execution contract | Planning input schema tests do not prove the end-to-end admitted rule is executable. |
| Cycle integration/state tests | Cycle range/order and lifecycle consumers | make_project_manager/make_phase_state_engine plus legacy_suite_workspace couple setup to injected configs/state. Refactor only fixtures/helpers invalidated by the selected boundary; avoid a broad rewrite. |

No tests were added or run in this Research pass. No production/configuration/agent source was modified. Concrete behavioral counterexamples can be demonstrated with isolated fixtures after the contract scope is agreed; do not corrupt #491's live planning as an exploratory probe.

## Questions

- Complete the incremental data discussion: explicit whole-block operation form and omitted/empty/null meanings. Existing stored cycle references and phase keys already identify targets; no new identity mechanism is needed. total is derived from the valid final plan, not caller input.
- Use the completed scope consumer register to shape the approved lossless codec contract; refresh it if any affected consumer changes.
- Use active-branch history without a last-N cutoff and qualify evidence by issue/workphase/cycle. The default rejection on unreliable derivation and explicit force escape after investigation are owner-approved; exact read-only Git boundary, codec representation and output shape belong to Design. Mandatory subphase solely for Git trace retention is no longer recommended.
- Define state-reference mapping/reset for removed or shifted uncommitted cycles without adding an active/entered-state mutation block. The owner-approved commit protection forbids deleting or renumbering any evidenced cycle; unprotected survivors may compact. Finalize locally scoped deliverable numbering on whole-block replacement.
- Confirm remaining planning-input compatibility policy per affected boundary and explicitly include or defer the admitted file_glob shape mismatch. Codec/history migration policy is already explicit.

## Approved Strategy

Owner direction on 2026-10-08 and 2026-10-09 confirms:
- Preserve the #229 distinction: write-once initial save and an explicit later mutation operation.
- Mutations provide complete blocks so their internal context is coherent; nested partial-field patching is not the requested route. Remaining block/omission details still need an explicit contract.
- total is server-derived from the valid resulting plan, persisted and returned for consultation. It is not required caller input and does not trigger deletion. This supersedes the earlier supplied desired-total/removal-above-range direction. Explicit removal intent is required for both phase blocks and cycles; exact request forms remain open.
- For the first save, the ordered cycle list determines server-assigned cycle numbers. Agent-supplied cycle numbers are unnecessary there. Targeting existing cycles in updates remains an explicit boundary to finish.
- Both operations apply one common complete-result validation before persistence: the final cycle sequence must be complete and a contiguous 1-based sequence, with valid complete blocks and no duplicate identities. Derived total reflects that validated result; missing cycle content is never manufactured.
- Deletion may compact the numbering of unworked survivors, retaining their relative order. Reject deletion of a commit-evidenced cycle and any mutation that renumbers an evidenced survivor. C_1/C_3 evidenced with C_2 unworked therefore cannot permit deleting C_2. State coherence remains an additional requirement.
- Naming/reference boundary: use cycle_name and deliverable_name for meaningful public names. The server supplies numerical references. Use C_<number> for cycles and D_<cycle number>.<deliverable number> for their deliverables; do not present deliverables as subcycles. Persist these generated identifiers in deliverables.json so direct file reads and project tools yield the same references. Exact field spelling and phase-deliverable convention remain open.
- Completed cycles must never be deleted. Use attributable implementation execution commits as the selected evidence direction for non-deletion, without claiming those commits prove completion. The decoded workphase is part of qualification; commits from other phases or composite/subphase-only labels cannot mark an implementation cycle as historical. Read active-branch history without a last-N cutoff; exact query/interface is Design work.
- Protection boundary: active, entered or previously touched cycle state does not independently block mutations of deliverables.json. Commit evidence is the protection criterion.
- Evidence failure boundary: reject update/mutation when reliable commit derivation fails. Allow an explicit force flag to override that uncertainty block after agent-human or agent-agent investigation justifies proceeding. Every force=true invocation still attempts derivation; if successful, ordinary protection applies; if it still fails, force may permit the write. Alternatively retain rejection and perform an agreed manual safe_edit_file repair. This supersedes the earlier cause/effect-based producer proposal. Force does not bypass known commit protection or complete-plan validity; no hypothetical failure taxonomy or skipped evidence attempt is permitted.
- Deliverable reference boundary: identifiers are local to the enclosing phase/cycle. Identical local IDs across different blocks are allowed; no global disambiguation registry is required. Parent context supplies the distinction, with names for human interpretation. Mutations still replace whole phase/cycle blocks, and numbering remains server-owned.
- Supporting scope explicitly includes correcting the record_sub_phase docstring to match its pre-commit write/rollback behavior, removing unused decoder/detector injections from state/status consumers and defining/correcting the shared encoder/decoder scope contract. These changes serve reliable cycle derivation from commit scopes; no unrelated cleanup or status reconstruction is included.
- Workflow configuration boundary (owner-approved 2026-10-09): permit zero or one cycle_based workphase per workflow and reject multiple entries in the existing configuration model. Preserve configuration-driven phase identity; no phase-name hardcoding, compatibility bridge or per-workphase cycle architecture. Current contracts remain valid.
- Current branch workflow state remains owned by state.json. Commit decoding is not a status resolver; the proposed new use is reading commit execution metadata for cycle evidence.
- Encoder/decoder boundary: use the same configured vocabulary and preserve distinct phase, optional cycle and optional subphase in a lossless round trip for all admitted combinations. No required subphase is introduced merely to retain a cycle. Exact scope spelling and typed result shape remain Design work.
- Codec/history migration boundary: no support or migration guarantee for closed issues and historical commits. The owner is the sole current server user and accepts upgrading and manually adjusting other workspaces. No old-format fallback or legacy result compatibility layer is required.

Current save checks a caller-supplied total against list length; changing total to server-derived output requires an explicit input/storage/readback distinction. The existing creation schema is an evidence input to reconcile, not assumed flawless: the admitted file_glob/executor mismatch and identity uniqueness still require resolution.

Pending owner decisions: coherent state-reference mapping/reset for removed/compacted unworked cycles without state-only protection; precise whole-block update targeting and phase omission/empty/null semantics; local deliverable numbering across block replacement and exact phase reference format; nested validation alignment and compatibility policy for the remaining planning boundaries. The active-branch completeness/default-rejection/force direction is settled; exact Git/codec/force interface details are Design work. The illustrative detailed schema is not an approved Design. These remain product/strategy choices, not an approved implementation. Research remains open; no Design transition is requested.

## Expected Results

Every supported planning mutation has an explicit observable effect or a truthful rejection; creation and resulting-update plans obey one coherent validity contract; failed validation leaves persisted planning unchanged; identity/order and lifecycle protection match the owner decision; complete public readback faithfully represents saved state. No generic deletion architecture or compatibility layer is assumed.

## Consumers

### Planning agents and native save/update callers

Create and evolve authoritative planning through public tools.

**Impact:** Field/null/total/replacement changes alter request meaning; migration must be explicit.

### ProjectManager and existing atomic writer

Read/validate/merge/persist issue plans.

**Impact:** Final-plan validation and policy coordination must remain at proper command boundaries.

### GetProjectPlanTool / IProjectPlanReader

Read complete typed planning without mutation.

**Impact:** Existing readback is an observable validity and fidelity boundary to preserve.

### PhaseStateEngine / workflow state and cycle history

Execute numbered cycle progression and record lifecycle evidence.

**Impact:** Structural mutation must preserve reference meaning and define protection without assuming completed status.

### PhaseContractResolver / DeliverableChecker

Select and execute issue-specific checks.

**Impact:** Cycle/ID identity and admitted validates shapes must agree with downstream selection/execution.

### Existing test support, active project reference and phase instructions

Exercise and describe planning contracts.

**Impact:** Update only directly invalidated behavior tests/docs/instructions; historical artifacts remain reviewed context.

## Risks

### A nominally successful update can persist a plan rejected by complete readback.

Agree one resulting-plan validity promise before Design; observe mutation through the public query.

**Consequence:** Agents may rely on invalid planning or require direct repairs.

### Renumbering/deletion changes the meaning of lifecycle and gate references.

Obtain explicit owner policy; preserve stable references and assess not-started-work boundaries.

**Consequence:** Historical/current execution evidence can be reinterpreted.

### A guessed completion guard recreates archived intent inaccurately.

Use actual entered/current/forced/phase evidence and define reopened-cycle handling explicitly.

**Consequence:** Valid active edits could be blocked or completed work left mutable.

### A holistic issue can grow into general mutation/audit/concurrency infrastructure.

Keep shared plan semantics in scope; document unproven concerns separately and avoid hypothetical architecture.

**Consequence:** Effort grows beyond evidenced contract defects.

## Related Documents

- [ProjectManager create/update/readback](<../../../mcp_server/managers/project_manager.py>)
- [Planning value models](<../../../mcp_server/schemas/deliverables.py>)
- [Public project tools](<../../../mcp_server/tools/project_tools.py>)
- [Current project-tool reference](<../../reference/tools/project.md>)
- [#229 original update design](<../archive/issue229/design-c5-c7.md>)
- [#229 append-only decision](<../archive/issue229/planning.md>)
- [#257 historical lifecycle decision](<../archive/issue257/%23archive/research_config_first_pse.md>)
- [#390 strict-schema design](<../archive/issue390/design.md>)
- [Existing project-tool behavior tests](<../../../tests/mcp_server/unit/tools/test_project_tools.py>)
- [Existing complete-save tests](<../../../tests/mcp_server/unit/managers/test_project_manager.py>)
- [Existing gate executor](<../../../mcp_server/managers/deliverable_checker.py>)
- [Current cycle lifecycle](<../../../mcp_server/managers/phase_state_engine.py>)
- [Issue gate selection](<../../../mcp_server/managers/phase_contract_resolver.py>)
- [Commit admission and lifecycle guard](<../../../mcp_server/tools/git_tools.py>)
- [Commit scope encoding](<../../../mcp_server/core/scope_encoder.py>)
- [Current scope decoding](<../../../mcp_server/core/phase_detection.py>)
- [Existing Git history access](<../../../mcp_server/adapters/git_adapter.py>)
- [Workflow contract schema](<../../../mcp_server/config/schemas/contracts_config.py>)
- [Workflow-specific policies](<../../../.pgmcp/config/contracts.yaml>)
- [Workphase catalog](<../../../.pgmcp/config/workphases.yaml>)
- [Encoder behavior evidence](<../../../tests/mcp_server/core/test_scope_encoder.py>)
- [Commit-tool behavior evidence](<../../../tests/mcp_server/unit/tools/test_git_tools.py>)
- [#138 original scope contract](<../archive/issue138/design.md>)
- [#146 TDD cycle admission research](<../archive/issue146/research.md>)
- [Current state-derived workflow status](<../../../mcp_server/managers/workflow_status_resolver.py>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-08 | @imp researcher | Record source-confirmed creation/update/readback gaps, historical rationale, affected consumers and unapproved boundary options. |
| 0.2 | 2026-10-08 | @imp researcher | Capture owner-confirmed complete-block mutation and shared result validation/count derivation; keep collection replacement and lifecycle protection explicit open decisions. |
| 0.3 | 2026-10-08 | @imp researcher | Refine total to desired whole-plan size and record tentative Git-backed non-deletion protection, observed trace limitations and unresolved evidence/state boundaries. |
| 0.4 | 2026-10-08 | @imp researcher | Map intentional subphase/cycle encoding, runtime/config policy boundaries and bounded enforcement options without approving or implementing them. |
| 0.5 | 2026-10-08 | @imp researcher | Trace the TDD origin and withdraw mandatory-subphase/rejection recommendations; assess independent lossless cycle/subphase representation and bounded reader impact. |
| 0.6 | 2026-10-08 | @imp researcher | Inventory active codec/writer/reader consumers, test behavior, passive injections and every shared-helper caller before representation strategy selection. |
| 0.7 | 2026-10-08 | @imp researcher | Resolve independent QA's P3 missing direct mock-injection consumer and close an exhaustive decoder/detector keyword-injection crosscheck. |
| 0.8 | 2026-10-08 | @imp researcher | Record owner caution, concrete historical/result/type-policy constraints and narrowly verified unused-injection cleanup boundaries. |
| 0.9 | 2026-10-08 | @imp researcher | Capture state.json ownership, the owner-approved lossless shared codec contract and explicit exclusion of historical compatibility; retain unresolved evidence and planning decisions. |
| 1.0 | 2026-10-08 | @imp researcher | Include approved codec/injection/docstring support and workphase-qualified cycle evidence; distinguish cycle planning from phase-deliverable blocks and their still-open replacement semantics. |
| 1.1 | 2026-10-09 | @imp researcher | Record approved zero-or-one cycle-based workphase invariant and distinguish agent phase guidance from structured runtime admission. |
| 1.2 | 2026-10-09 | @imp researcher | Reconcile explicit removal, derived total/server numbering, protected compaction and typed cycle/deliverable references; distinguish owner directions from the unapproved illustrative schema. |
| 1.3 | 2026-10-09 | @imp researcher | Require generated cycle/deliverable identifiers in persistent planning, shared by direct file reads and project readback. |
| 1.4 | 2026-10-09 | @imp researcher | Confirm local deliverable references, commit-only cycle protection and cause-sensitive evidence handling; exclude active/entered-state immutability. |
| 1.5 | 2026-10-09 | @imp researcher | Replace uncertainty taxonomy with complete active-branch evidence, default rejection and explicit force after investigation; retain manual repair as an external alternative. |
| 1.6 | 2026-10-09 | @imp researcher | Require a fresh evidence attempt under force, demonstrate local complete-history reading and explicitly inventory the runtime IO/protection scope extension and limits. |
| 1.7 | 2026-10-09 | @imp researcher | Make the active-branch HEAD start explicit and separate it from the proposed branch-basis stop boundary; local reads require no network fetch. |
| 1.8 | 2026-10-09 | @imp researcher | Trace duplicate issue markers to caller text plus automatic suffix injection; record native issue lookup and the owner-proposed bounded title normalization without implementing it. |
