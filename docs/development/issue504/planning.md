<!-- pgmcp:v1 id=planning pv=1.0.0 pf=OSfLTQ1qMuWvM9fi sf=KoFPQ3-cAAWFeesb -->

# Issue 504 — Interactive native configuration refactor

**Status:** IMPLEMENTATION — PHASE REVIEW REQUESTED  
**Version:** 0.4  
**Last Updated:** 2026-10-16

## Purpose

Sequence the approved design into bounded interactive implementation cycles and phase-owned evidence.

## Scope In

Approved Research/Design; native composition, source/model/direct consumer cutover, GitHub/init exceptions, focused tests and Documentation PR closing correction.

## Scope Out

release_manifest.yaml; builders, releases, distribution/upgrade work, compatibility bridges, public state/planning/commit redesign and suite-wide cleanup.

## Prerequisites

- Independent renewed Research and Design GO on the reviewed commit.
- User starts interactive Implementation after independent Planning GO; this preparation run stops in Planning.

## Summary

Three dependent cycles separate the native composition seam, coherent active config/model/consumer cutover, and GitHub/init exceptions. Each deliverable is an owner-interactive checkpoint. No cycle starts automatically after this plan is approved.

## Dependencies

- Research and Design are binding; reopen conflicts before changing strategy.
- C_1 -> C_2 -> C_3; no activated mixed source/model state.

## Risks

### A source/model-only partial cutover could make the server unable to load configuration.

Keep C_2 schema/source/consumer changes coordinated, prove via isolated fixtures before activation; discuss each substep interactively; retain known commit recovery and restart/refresh on agreed activation.

### Shared preparation can silently load the live repository or create excessive fixture churn.

Use existing explicit temp-root/factory seams; update affected preparation once; no legacy source converter or suite-wide cleanup.

### The Planning approval could be mistaken for permission to start Implementation.

Stop in Planning after QA GO; no transition or execution until the owner returns.

## Work Units

### C\_1 — Native composition and narrow operations

**Goal:** Introduce the pure native merge boundary with strict deletion and reusable order validation, before switching active runtime sources.

**Cycle Number:** 1

**Owner:** @imp implementer

#### Scope In

Direct dependency declaration, config/composition.py, reusable config-owned order helper and focused existing loader/config behavior tests.

#### Scope Out

No active source/model/consumer cutover, GitHub settings, init lifecycle or full suite.

#### Deliverables

##### D\_1.1

Native merge boundary: Use pinned public Pydantic Settings source composition for add/update/inheritance, with ambient sources excluded; strict parser remains loader-owned. Prove nested mapping preservation, whole leaf-list/null replacement and caller-data immutability.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "mcp_server/config/composition.py"

##### D\_1.2

Explicit deletion and order: Implement only explicit tombstone preprocessing and shared strict order validation/use; prove unknown/mixed command rejection, inherited/new ranks, collisions and final required/reference rejection through meaningful config boundaries.

**Owner:** @imp implementer

**Validates:**

**Type:** file_glob

**Directory:** "tests/mcp_server/unit/config"

**Pattern:** "test_*.py"

#### Exit Criteria

Focused composition/order behavior passes, applicable Python file gates pass, no active runtime cutover or extra custom merge/materializer is introduced. Owner reviews the proposed step and actual outcome before the next implementation step.

#### Dependencies

#### Obligations

- Use native recursive mapping merge; own logic only delete/order plus existing parse/model admission.
- No broad suite, no legacy rejection tests and no private Pydantic APIs.

#### Verification

##### Native and narrow-extension behavior

**Method:** Adapt a compact test matrix at the config boundary; exercise nested inheritance, literal null/list, explicit deletion, ranks and no writes.

**Expected Result:** Public behavior proves each independent operation without snapshots or per-file copies.

##### Directed execution selection

**Method:** run_tests(scope='targets', targets=['tests/mcp_server/unit/config/test_loader_behaviors.py','tests/mcp_server/unit/config/test_checks_config.py'], tests=['python_tests'], timeout_seconds=600); add only actually adapted composition/order test module targets. Run Python format/lint/pyright with scope='targets' and actual changed .py files only.

**Expected Result:** Focused behavior and per-file gates pass; no configuration/Markdown targets are sent to Python checks.

#### Stop Conditions

- Owner has not started interactive Implementation or has not agreed to the next step.
- Native API/versions do not support the documented boundary; discuss rather than implement own merge.

### C\_2 — Atomic configuration and consumer cutover

**Goal:** Switch required config source selection and typed object collections coherently while preserving effective repository behavior.

**Cycle Number:** 2

**Owner:** @imp implementer

#### Scope In

ConfigLoader, directly affected config schemas/validators/helpers, defaults/root source split, enforcement/presentation/workflow/issue/catalog consumers, resolver/bootstrap CheckSpec projection, affected fixtures.

#### Scope Out

No release_manifest/build changes, package-declaration layering, state/planning DTO changes or new migration/translation layer.

#### Deliverables

##### D\_2.1

Canonical source and model cutover: Create canonical complete defaults and actual root differences, normalize object collections to key identity and explicit meaningful order, retain leaf lists and strict parsing; preserve complete-file/package routes and optional enforcement; remove redundant technical identities and ignored phase_source.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** ".pgmcp/config/defaults/contracts.yaml"

##### D\_2.2

Consumer and fixture cutover: Adapt only changed map/order consumers and affected shared fixture preparation, including enforcement, presentation, issue/workflow/catalog helpers and both CheckSpec resolver paths; prove current effective policy/references/order and no live-root fixture fallback.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "mcp_server/managers/phase_contract_resolver.py"

#### Exit Criteria

The running/configured source shape and consuming models agree; focused config/enforcement/presentation/workflow/issue/resolver tests pass, applicable file gates pass and current effective policy/order/references are demonstrated. No compatibility path remains. Owner inspects each coordinated substep before further work.

#### Dependencies

- C_1

#### Obligations

- Keep model/source/consumer changes together; no independently activated partial cutover.
- Shared CheckSpec/planning/state/commit DTOs stay unchanged; resolver uses validated config keys/payloads.
- Preserve configuration_choice:null and safe-edit report behavior.

#### Verification

##### Source and consuming behavior

**Method:** Existing loader/schema/consumer tests and isolated root fixtures; compare selected effective policy outcomes, not file contents.

**Expected Result:** Preserved enforcement/presentation/transitions and reference validity; errors never mutate source.

##### Coherent changed-container consumers

**Method:** Select actual affected tests from unit/config, unit/managers/test_enforcement_runner.py, unit/managers/test_phase_contract_resolver.py, unit/presenters/test_collection_text_renderer.py and the three enforcement integration files. Run only affected modules, adding catalog/workflow/issue helper tests where their behavior changed.

**Expected Result:** Existing admission/dispatch/render/phase/reference outcomes survive the keyed cutover, with explicit order honored.

#### Stop Conditions

- Unexpected additional consumers/public boundaries appear.
- A temporary compatibility bridge, generic converter or arbitrary nested payload interpretation would be needed.
- Active server/schema refresh is required: pause to restart/refresh before live tool use.

### C\_3 — GitHub source and initialization cleanup

**Goal:** Complete the approved configuration source exceptions and remove temporary mutation behavior.

**Cycle Number:** 3

**Owner:** @imp implementer

#### Scope In

github.yaml source values, pure token resolution, Settings/ConfigLayer/bootstrap injection and registration/resource gates, CLI init reset deletion, directed existing tests.

#### Scope Out

No credential probes, vault implementation, automatic tool-unlisting redesign, native tool setup, releases or distribution acceptance.

#### Deliverables

##### D\_3.1

Single GitHub source: Resolve workspace GitHub identity and optional token alternative with environment-first GITHUB_TOKEN; remove owner/repo launcher/environment fallbacks and feed one resolved value to manager, registration and resources.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "mcp_server/config/github_resolution.py"

##### D\_3.2

Initialization and obsolete-path cleanup: Remove temporary init acknowledgement rewriting and reset-only tests; adapt current Settings/bootstrap/init behavior evidence and finish directed obsolete identity/container preparation cleanup.

**Owner:** @imp implementer

**Validates:**

**Type:** absent_text

**File:** "mcp_server/cli.py"

**Text:** "_reset_binding_choices"

#### Exit Criteria

Focused GitHub/Settings/bootstrap/init tests and applicable file gates pass; no old identity fallback/reset remains; credentials are neither probed nor written to evidence; all implementation obligations are ready for phase-owned Validation after owner-controlled work.

#### Dependencies

- C_2

#### Obligations

- Missing GitHub settings retain existing startup/use-time behavior, no inference or enforcement bypass.
- Retain standard safe-edit report/setup availability and no configuration_choice mutation on init.

#### Verification

##### Single integration source and read-only init choices

**Method:** Existing Settings/bootstrap/init tests with injected nonsecret environment/config; retain useful null/report behavior coverage.

**Expected Result:** All token-dependent consumers agree; init preserves explicitly authored choices.

##### GitHub/init checks

**Method:** run_tests(scope='targets', targets=['tests/mcp_server/unit/config/test_settings.py','tests/mcp_server/unit/server/test_bootstrap.py','tests/mcp_server/unit/test_cli.py'], tests=['python_tests'], timeout_seconds=600), narrowed to actually affected modules when possible; directed Python checks.

**Expected Result:** Environment-first token, single source use and preserved authored acknowledgement values pass.

#### Stop Conditions

- A credential/registration policy decision beyond Design is needed.
- Test/consumer failures show scope beyond the approved boundary.

## Phase Deliverables

### Validation

#### D\_1

**Deliverable Name:** Durable validation evidence

Compact durable validation report maps native composition, deletion/order, current behavior, cleanup and focused checks to observed outcomes, explicitly recording the owner-directed exclusion of broad scopes.

**Owner:** @imp validator

**Validates:**

**Type:** file_exists

**File:** "docs/development/issue504/validation.md"

### Documentation

#### D\_1

**Deliverable Name:** Active documentation and PR closing correction

Update active configuration/setup/launcher references and PR template: every closes entry emits an operative Closes #N, proved by the adapted existing multi-issue rendering test.

**Owner:** @imp documenter

**Validates:**

**Type:** file_exists

**File:** "docs/reference/server-configuration.md"

## Execution Contract

The owner has authorized autonomous execution through Ready and a merge request to Coordination. The earlier per-deliverable interactive checkpoints are superseded. Preserve the approved design and raise real policy choices or scope contradictions; do not add new architecture.

C_2 source/model/direct-consumer edits form one coordinated cutover. Discuss and inspect them in small substeps, but do not activate a half-converted server or commit a knowingly unusable mixed contract. Establish isolated fixture behavior before the agreed activation, restart with the existing tool when needed, and refresh tool schemas if the client requires it. Recover only the current agreed step from its known commit; do not overwrite user work or restore an old format as a compatibility feature.

Do not impose artificial RED on pure structural moves. Adapt existing valuable behavior tests and shared fixtures first. Add a failing test only for a durable new obligation not already covered, then keep the focused evidence green. No test-count target, source-string compliance test or retained legacy-negative suite.

## Exact Evidence Selection

### Implementation

Use actual changed files and affected behavior modules. Example request shape:

```json
{
  "scope": "targets",
  "targets": ["tests/mcp_server/unit/config/test_loader_behaviors.py"],
  "tests": ["python_tests"],
  "timeout_seconds": 600
}
```

Preserve the binding's native arguments; do not override args merely to remove coverage, parallelism or strictness. Add the exact adapted modules for the current deliverable, never all config/consumer folders by habit.

For Python file gates, select only actually changed .py files and checks python_format, python_lint and python_pyright. Production Mypy stays production-scoped; do not make strict Mypy over tests a new gate. YAML source/schema and Markdown link checks get their own applicable targets. A mutation/fix is not passing evidence; recheck affected files. Reuse fresh results until later edits invalidate them.

The core C_2 test inventory comprises the existing loader/contracts/issue/catalog modules; tests/mcp_server/unit/managers/test_enforcement_runner.py and test_phase_contract_resolver.py; tests/mcp_server/unit/presenters/test_collection_text_renderer.py; and tests/mcp_server/integration/test_context_loaded_enforcement.py, test_ready_phase_enforcement.py and test_pr_status_lockdown.py. Select the concrete affected tests from this inventory. Check both phase-exit and cycle-exit projection, terminal/cycle-owner validation, real action/render order and optional/complete-file/package source routes.

The stored file_exists/file_glob/absent_text validators are navigation/structural gates only. Existing filenames or an absent symbol alone do not prove a deliverable; the specified behavioral evidence and exit criteria do.

### Validation

Owner direction during Implementation supersedes the broad Validation requests in v0.2: continue autonomously through Ready, use only focused target scopes, and request independent QA only at phase boundaries. Do not run the full suite, branch-wide checks or configured workspace gates. The report must identify each selected behavior module, file gate and native outcome, reuse valid evidence, and state that workspace-wide coverage has not been established. This is an explicit execution-scope exception, not equivalent evidence for a full suite.

### Documentation

Update active setup/config/launcher references and examples for defaults/root overrides, keyed objects, literal lists/null, delete/order and github.yaml. Keep historical issue documents as context. Correct the active PR source template using its current closes array; each issue emits its own operative Closes #N. Adapt and run only the existing tests/mcp_server/integration/templates/test_pr.py behavior evidence for this bounded change, with applicable Python/template/document checks. That later narrow change needs fresh rendering evidence; production implementation evidence remains reusable unless the change invalidates it. No additional documentation report is required merely to satisfy a filename.

## Review and Stored-Plan Evidence

Independent QA chat: QA (the existing review authority previously referred to as Beoordeel designplan). Research v0.19 received renewed Research-to-Design GO and Design v0.6 received a separate Design-to-Planning GO on a1fe27ccfe189cfd7d6614a19b67a0620d1564b4. Those reviews found no P0/P1/P2 blockers; they do not assert implementation behavior.

save_planning_deliverables created three cycles and eight deliverables. Full get_project_plan readback confirmed C_1/D_1.1–D_1.2, C_2/D_2.1–D_2.2, C_3/D_3.1–D_3.2, and phase-local D_1 in Validation and Documentation, with matching names, descriptions, validation targets and exit criteria. Total and IDs are server-derived. This paragraph records the durable outcome rather than treating transient run IDs as evidence.

Independent QA granted Planning-to-Implementation GO on 5ac30a4a2226a51961fd205fb04e09ad884292c0. Subsequent owner authorization permits autonomous continuation; independent GO remains required at phase boundaries.

## Related Documents

- [Research](<research.md>)
- [Design](<design.md>)
- [Quality evidence](<../../coding_standards/QUALITY_GATES.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-15 | @imp planner | Sequence native composition and clean source/consumer cutover with interactive checkpoints; reserve full suite/gates for Validation and stop before Implementation. |
| 0.2 | 2026-10-15 | @imp planner | Fix QA P2: suite budget 1200 seconds inside prescribed client window 1800; add literal phase deliverable names for exact readback parity. |

| 0.3 | 2026-10-16 | @imp implementer | Record autonomous focused-only execution and source-bound implementation checkpoint. |
| 0.4 | 2026-10-16 | @imp implementer | Repair both independent QA P2 findings and the directly affected policy-read fixtures. |


## Implementation Checkpoint

The owner authorized autonomous execution through Ready, focused target scopes only (including Validation), and independent QA exclusively at phase boundaries. Earlier interactive stops and broad Validation commands are superseded; source strategy and exclusions are unchanged.

C_1 delivered public native Pydantic Settings composition, strict tombstones and model-owned explicit order. Its focused 16-case composition and seven-case ordering tests passed; the existing deletion case now also proves that aliased source objects do not redirect a deletion to an unaddressed sibling. Input trees remain unchanged. Production typing and file gates passed.

C_2 is committed at cce658f6ffa2da4302b8cac338eb23eb021e71a8. Complete product sources live under defaults/; root files are workspace overrides. Canonical keyed/order-aware models and direct consumers were cut over together. Targeted loader, catalog, contract/resolver, enforcement, presentation, public execution and startup/resource behavior passed. Native YAML checks passed on all 36 changed source documents. After independent QA rejected a duplicated workspace policy, the root enforcement override was reduced to an empty mapping. The complete product basis independently supplies all current guards, proved through the public loader; no guard is removed. This supersedes the earlier conservative duplicate retained after automatic approval rejections.

C_3 uses one resolved GitHubSettings from layered github.yaml and the nonempty environment token, shared by the manager and registration/resource decisions. Settings no longer owns GitHub identity; initialization no longer resets copied choices. Focused Settings/bootstrap/CLI modules passed (53 cases), direct server/discovery/argument/lifecycle modules passed (52), and six affected PR/rollout/fixture/execution modules passed (81). Settings was rerun after extending its existing secret-safe validation test to malformed YAML: 27 passed. Both model and parser diagnostics excluded the fixture token; no speculative parser refactor was needed. Ruff format/lint and Pyright passed on the 21 changed Python files; Mypy passed on six affected production files.

The full suite and workspace/branch-wide gates were intentionally not executed. Existing SchemaAttachment.schema-shadow and previously observed MCP resource/Windows path deprecation warnings remain outside scope. No release_manifest, package-builder, distribution or upgrade behavior is changed; follow-up #505 and other deferred work are not delivered by this branch.

### Independent Implementation Review Repairs

Independent QA returned NOGO on 54a9551df96948117ade14d8b221831f3e88af2e for two P2 contract deviations. Both are repaired without changing strategy: enforcement.yaml is now a no-op workspace override over the unchanged guarded product basis; resolve_config_root always honors explicit context, including absent fixture preparation. The existing root-isolation test was extended with absent workspace/config selections: it failed before the helper fix and passed afterward. No general fixture rewrite or new compatibility path was introduced. The helper/loader isolation test passes. Eight selected context/server/enforcement modules exposed only three remaining test modules incorrectly reading the root override as a standalone complete policy; these now use the normal layered loader. Their focused rerun passed, as did the YAML and affected Python gates. Independent recheck is requested on the repair commit.
