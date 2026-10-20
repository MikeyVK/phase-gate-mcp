<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Issue \#518 — remaining suppression boundaries on the migrated baseline

**Status:** Research complete — independent review requested  
**Version:** 1.0  
**Last Updated:** 2026-10-20

## Purpose

Establish the actual remaining source/checker boundaries without repeating migration work or treating diagnostic populations as runtime defects.

## Scope In

Remaining Ruff/Mypy/Pyright global and local suppression groups, directly relevant warning filters, ordinary affected helpers, model-only input, Literal attributes, dynamic JSON boundaries, typed logging producers/runtime diagnosis and their existing tests.

## Scope Out

SDK/Python migration, initialization-free protocol/proxy redesign, release/deployment, zero-suppression quota, unrelated test/type/coverage debt, suite-wide import rewriting, whole-test Mypy or #533 gate-policy changes, and the historical Windows process-readiness risk.

## Problem Statement

#513 measured the removal impact and obtained the owner’s per-boundary strategy. #517 completed migration, but the current native files still hide strict diagnostics and retain source-level exceptions. Repair must follow the real remaining owners/consumers, preserving runtime rejection, variance, operational facts and useful tests rather than deleting all suppressions.

## Goals

- Reconcile migration-obsolete work and every remaining equivalent suppression group with a concrete remove/narrow/retain direction.
- Locate shared dynamic boundaries and direct consumers; preserve native validation and diagnostics without host dependencies, unchecked casts or a generic framework.
- Carry the existing human-approved strategy into Design, with explicit evidence limits and proportional test impact.

## Background

Co created and initialized this refactor branch from accepted main after #530, reporting base 17106f5f784841c6b8a9fd178b41e5befe019384. get_work_context confirms #518/research/parent main; the initial worktree contained only Co-created untracked state.json and deliverables.json. The live #517 issue is closed (2026-10-18T15:38:10Z); its final Validation and the inherited #513 final strategy are prerequisites. No deleted #518 branch or stash was restored.

## Findings

### Current policy and migration reconciliation

| Surface | Current observation | Remaining direction / trigger |
| --- | --- | --- |
| Native Ruff | py315, Python-only discovery, ignore=[], existing selections; tests/**/*.py still ignores ANN and ARG. | Preserve tool/discovery policy. Replace broad test exemptions with ordinary helper typing and exact necessary fixture/interface/invalid-input exceptions; reassess the actual final native selection. |
| Native Mypy | Python3.15, strict production files, strict Pydantic plugin and unused-ignore checking; tests.* still relaxes untyped definitions. | Annotate the three indexed helpers and remove this relaxation, retaining the production-only configured gate. |
| Native Pyright | Python3.15 strict mode and 27 explicit false flags remain. | Restore the approved strict signals after source repairs. Deleting the four native-default-none flags is not opt-in to their separately measured policy. |
| Migration-obsolete | AdapterBinding misc workaround and four old server decorator Mypy comments are gone; template_activation already uses Generator. | Do not repeat obsolete SDK/AnyIO/ISC004/UP037/contextmanager repairs. Preserve explicit covariance/frozen behavior. |
| New precise boundaries | server.py:115 and response_cache.py:47,67 retain native SDK/publication diagnostics. | Include these current exceptions in disposition; do not blindly apply the old line index. |
| Warning filters | Focused active source/test/native-config search found no directly relevant filterwarnings/simplefilter/catch_warnings/PYTHONWARNINGS policy. | No warning-filter repair is demonstrated; do not add filters. |

### Local families and exact remaining candidates

The seven policy-independent historical RUF100 candidates are still present: core/error_handling.py:136; managers/project_manager.py:295; tools/git_tools.py:442,446 (BLE001 components); tools/discovery_tools.py:84 and tools/project_tools.py:117,223 (ANN401 components). Mixed ARG002 components require their own disposition.

The twelve test directives masked by the broad ANN/ARG policy also remain: test_support.py:571 and unit/core/test_note_context_unit.py:24 (ANN401); unit/adapters/test_github_adapter.py:32,62, unit/config/test_settings.py:43, unit/managers/test_enforcement_runner.py:93 and test_phase_state_engine_c1.py:162 (ARG001); unit/managers/test_workflow_status_resolver.py:104, unit/resources/test_base.py:21, test_resources_base.py:17, unit/server/test_validate_tool_arguments.py:78 and unit/tools/test_initialize_project_tool.py:229 (ARG002). Paths in this paragraph are under tests/mcp_server/. They are not nineteen interchangeable removal approvals.

| Equivalent family | Concrete remaining scope and disposition |
| --- | --- |
| B017 | Five broad Exception assertions: unit/tools/test_git_tools.py:80,87,94,98 and test_issue_tools.py:237. Use the already-observed ValidationError and preserve rejection without exact prose assertions. |
| BLE001/T201 | Preserve source-demonstrated terminal/cleanup/presentation/cancellation and outward CLI/restart-marker boundaries. Remove only demonstrated redundant components; retain original cause/traceback and real outcomes. |
| ANN401/ARG | Known audit/Jinja/Pydantic/foreign-schema boundaries need honest types; do not import a higher-layer model into core. Remove ConfigValidator._validate_phase_contracts.workflow, unlike required interface/public-keyword parameters. |
| Variance/library | Seven UP046 declarations still preserve explicit covariance/invariance or demonstrated full AdapterRole/Pydantic limitation. Update obsolete 2.11 rationale against supported 2.14.1 evidence; do not assume the limitation disappeared. Settings prop-decorator remains source-specific. |
| Mypy source | git_adapter.py:221 assignment, settings.py:66 prop-decorator, input_validation_decorator.py:115 arg-type and icore_tool.py:25 misc remain. Use the resolved HEAD hash; preserve property/protocol limitations and remove the None route under the approved contract. |
| Mypy test cleanup | Original unused candidates persist at unit/config/test_workflow_config_c6.py:183,192, test_workflow_config.py:21 and unit/managers/test_project_manager.py:945. Three untyped helpers remain at unit/core/interfaces/test_interface_imports.py:29, unit/decorators/test_pipeline_decorators.py:280 and unit/test_cli.py:99. Other required/frozen/invalid-input cases need precise codes, including the bare abstract-construction ignore at unit/resources/test_base.py:47. |
| Mock/private/module switches | Prefer existing injected/public behavior; preserve only necessary precise invalid/abstract/private-injection exceptions. Include current presentation-config frozen mutation sites, rather than treating the old index as complete. Preserve public keyword contracts. |
| Dormant Pylint | Nine comments persist in github_adapter, cli, github_manager, resource-base and label integration tests. No active Pylint binding: remove dormant directives, not a tool/runtime feature. |
| Imports | Preserve CLI route-specific delay and test_support invocation-time Settings attribute lookup. Ordinary server recovery/error/schema imports can move with focused startup/patch evidence; no mass unrelated test import hoist. |
| Other exact cleanup | Preserve GateViolation identity and correct its rationale; remove genuinely unreferenced _track_branch_local_artifacts; type the three indexed test_git_manager lambda diagnoses. |

### Shared source boundaries and preservation

The historical candidate capture had 418 production Unknown messages at 296 positions; this is not a current #518 count and not 418 runtime bugs. The ten-way classification remains a useful owner map, with post-migration source changes requiring current native measurements during repair.

| Existing owner | Current facts / invariant / direct evidence seam |
| --- | --- |
| Adapter JSON | Eight package files validate root/fields/items before use; decoded JSON, prerequisites and native reports remain separate untrusted boundaries. Ruff/Mypy/Pytest/python-syntax/check-jsonschema/Lychee/Commitlint existing integration cases protect root/index diagnostics, pins, effective settings and mutation refusal. Keep independent adapters self-contained/stdlib-only; no new host model/framework. Commitlint already deliberately injects the host ArtifactHeaderReader: do not falsely describe every package as having no host dependency or redesign that coupling here. |
| Config/model input | Composition, loader and before-validators receive raw objects before Pydantic admission. Preserve deletion/order/default/admission semantics and existing consumer models. |
| Presentation/cache | Dynamic field reads and recursive JSON retain null distinctions, protected notes, item diagnostics and primary exceptions. #528/#529/#530 changed these paths after the historical capture; no replay or new projection policy follows. |
| Stored JSON/context | Plan/state/gate reads must narrow at their existing boundaries; preserve query purity, corrupt/version diagnoses and no empty-success fallback. |
| Local inference | Annotate existing empty containers with actual element types; preserve order and values. No new DTO/runtime layer merely for inference. |
| Field factories | Preserve fresh-per-instance defaults and public constructors; use precise supported factory typing rather than a shared mutable object or blanket ignore. |
| SDK/server | Old API repair is complete; current supported-tool metadata/output projection remains at its existing owner. Do not duplicate schema inventories or place SDK knowledge in managers/tools. |
| Core/schema | ICoreTool.args_model, IToolInputContract’s BaseModel|None bound and InputValidationDecorator’s execute(None) route remain. Concrete no-argument tools already have HealthCheckInput/GetWorkContextInput/GitStatusInput/ListLabelsInput. Preserve schema/admission identity, rejected-input attachments and skip-before-execution. |
| Logging | Current formatter still flat-updates dynamic record.props. Search now finds 24 extra-bearing calls in nine files; 23 use props. process_runtime.py:284 supplies directory/cause directly, which the formatter omits. Restart audit props still supply timestamp and can overwrite formatter metadata. Preserve primary message/severity/traceback, expose malformed payload and retain process context; metadata shape/timestamp ownership are scoped Design questions. |
| External YAML | Contain SafeDumper’s partially typed represent_scalar signature at the existing emission owner; preserve escaping/chomping and rejection, no YAML reimplementation. |

Literal reason/stage constructor types are still widened by unannotated stored attributes in BranchBasisUnavailableError, FileCreationError, OriginalReadError and FileReplacementError. Their check/edit/scaffold consumers already require narrow Literals. The existing response values, housekeeping/cause chains and persistence outcomes must remain identical.

### Test structure, coupling and bounded impact

Existing factories/isolated adapter packages and real SDK seams supply behavioral evidence; they are not a reason to introduce a shared adapter framework. The direct None consumers in test_pipeline_decorators (including RecordingCore and explicit PreparedToolInputContract[None]) must migrate to genuine typed-empty inputs without preserving an old route. Existing prepared-contract rejection/readback tests protect actual semantics.

Logging tests cover valid props, base metadata, audit files and owned-handler reconfiguration; malformed/collision/non-JSON preservation coverage is missing. Existing restart tests read props.event_type and verify exactly three events, stderr marker and exit42; they are direct consumers of any logging shape change.

Restoring Pyright signals can also expose existing dynamic setup in changed test files. Branch checks and configured production checks have distinct selections. Do not infer a whole-test Mypy gate or sweep every historical test diagnosis from a diagnostic run; an unavoidable scope/strategy conflict must be exposed rather than hidden with another broad exemption.

Focused host-native text search currently finds 284 directive-bearing candidate lines in 79 files (211 noqa,55 type-ignore,13 pyright and9 pylint family matches; families overlap). This is a reproducible navigation index, not a token-aware census: quoted fixture text/rationales can match. Final native/source disposition must inspect real directives and reassess previously unused codes under the final combined policy.

## Questions

- Design must define typed producer/runtime logging metadata and timestamp ownership without lost facts or a parallel logging framework.
- Design must specify model-only transport/core interfaces and proportional direct consumer changes, preserving variance and prepared schema identity.
- Design/Planning must select source-group evidence and honest stop conditions for newly exposed unrelated test debt; no test-gate policy expansion.

## Approved Strategy

The human-approved final #513 Research Outcome/Approved Strategy and final inventory, explicitly inherited by the published #518 scope and Co handoff, are binding. No routine reapproval is needed and no new strategic contradiction was found.

| Boundary | Approved strategy applied here |
| --- | --- |
| Migration/base | Work only after accepted #517; preserve the new Python/SDK/dependency contracts and remove no obsolete code twice. No legacy/version bridge or automatic active environment upgrade. |
| Core input | Clean break to model-only input and typed empty models; migrate direct None-based consumers, with no compatibility route. Preserve intentional variance and prepared exposure/admission identity. |
| Literal/source typing | Preserve narrow values on stored attributes and consumers. Fix types at existing owners before narrowing/precise justified exceptions; never cast untrusted input or stringify it silently. |
| Logging | Preserve primary event/message/severity/traceback and explicitly diagnose malformed extra data. Typed producers and runtime handling both matter; metadata/timestamp representation is delivery Design, not permission to discard data. |
| Runtime/library | Preserve meaningful immutable JSON/PyGithub guards and established exception identities. Retain only necessary source-demonstrated variance/library/terminal exceptions with concrete reassessment triggers. |
| Native/test policy | Restore approved disabled strict signals, remove broad ANN/ARG/untyped-helper relaxations proportionally, retain exact necessary fixture/interface/invalid-input exceptions. Four native-default-none rules are not newly enabled. No zero-suppression quota, blanket disable or whole-test Mypy gate. |
| Evidence/authority | Existing valuable behavior/type tests, non-masked positive/negative controls and actual configured tool versions prove each changed boundary. Focused Implementation; full native suite and required gates in Validation. Independent QA alone decides each phase GO/NOGO. |

## Expected Results

A bounded repair removes or narrows each remaining equivalent exception for a demonstrated reason, restores useful checker sensitivity and preserves runtime/type contracts. Final disposition records every retained exception’s exact rationale and reassessment trigger. Research does not claim new native diagnosis counts, implemented fixes or #518 acceptance.

## Evidence

### The migrated prerequisite is closed; current branch is initialized for Research

get_issue(517) reports closed; get_work_context reports #518/refactor/research/parent main. Initial git_status lists only Co-created state/deliverables as untracked.

- [Accepted migration Validation](<../issue517/validation.md>)

**Invocation:** get_issue(issue_number=517); get_work_context(); git_status(); get_project_plan(issue_number=518)

**Observed Result:** Current source inspection only; no new tests/checks or production/configuration edits.

### Historical removal measurements and owner decisions are available, not a new baseline measurement

Final #513 sections distinguish seven independent Ruff candidates from twelve test-policy-dependent comments and partition historical418 Unknown diagnostics into ten boundaries. Current source reconciliation above identifies remaining and migration-obsolete groups.

- [Final strategy](<../issue513/research.md#approved-strategy>)
- [Final inventory](<../issue513/suppression-inventory.md#final-disposition-proposal-for-owner-decision>)

**Invocation:** Host-native rg/source reads of current pyproject.toml, pyrightconfig.json, directive-bearing production/tests, direct consumers and final #513 sections.

**Observed Result:** No stale version/API repairs copied; no zero-suppression conclusion or newly passing quality claim.

### Current preservation risks have direct source/test seams

Unchecked record.props merge, direct cleanup extra and execute(None) are still present; Literal response consumers and meaningful runtime guards already exist.

- [Logging owner](<../../../mcp_server/core/logging.py>)
- [Input admission owner](<../../../mcp_server/core/decorators/input_validation_decorator.py>)
- [Prepared model contract](<../../../mcp_server/core/interfaces/tool_input_contract.py>)
- [Logging behavior](<../../../tests/mcp_server/unit/core/test_logging.py>)
- [Decorator consumers](<../../../tests/mcp_server/unit/decorators/test_pipeline_decorators.py>)

**Observed Result:** Actual sources substantiate a repair boundary; historical runtime probes remain indexed in #513, not rerun or represented as #518 acceptance.

## Consumers

### Native configs and package adapters

Checker policy, independent wire/native admission and version prerequisites

**Impact:** Existing native settings and local dynamic validators; package-isolation integration cases, no framework.

### Core tool/decorator/prepared input contracts

Typed schema/admission and execution

**Impact:** Model-only signatures, typed-empty direct doubles/calls, unchanged response/error attachments.

### Structured logging and current producers

Primary event metadata, audit/process context and traceback

**Impact:** Nine producer files and existing formatter/restart tests; explicit malformed-payload admission.

### Config/model/state/presentation/YAML boundaries

Existing raw input narrowing and truthful output

**Impact:** Local source annotations/validation and focused existing public tests; no domain/config/projection policy redesign.

### Ordinary test helpers and exceptions

Faithful preparation/negative input and runtime behavior

**Impact:** Indexed three helper annotations, narrow invalid/interface/fixture cases; no suite rewrite or mandatory test-Mypy.

## Risks

### A global restore can surface multiple correlated diagnostics or unrelated existing test preparation debt.

Group by the existing source owner, measure after each bounded slice and preserve exact failures; stop for genuine strategy/scope contradictions instead of broad suppression or a suite rewrite.

### Convenient typing can change runtime rejection, covariance, mutable defaults or Git HEAD timing.

Use existing valid/invalid and public behavior tests plus non-masked type controls; retain declared invariants and already-resolved values.

### Logging cleanup can hide the original exception, overwrite base metadata or discard process/audit fields.

Treat typed producers and runtime payload admission as one bounded responsibility; Design must preserve all primary event facts and explicitly expose malformed data.

## Related Documents

- [Inherited final strategy](<../issue513/research.md>)
- [Historical inventory and import/Unknown classification](<../issue513/suppression-inventory.md>)
- [Accepted migration](<../issue517/validation.md>)
- [Architecture contract](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)
- [Type checking resolution order](<../../coding_standards/TYPE_CHECKING_PLAYBOOK.md>)
- [Evidence and gate scope](<../../coding_standards/QUALITY_GATES.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-20 | @imp researcher | Reconcile inherited #513 strategy with migrated sources, current native/local groups, direct consumers and preservation risks; no remediation or new policy. |
