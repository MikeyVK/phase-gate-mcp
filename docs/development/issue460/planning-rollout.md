# Issue 460 Planning — Distribution, activation and retirement

Status: DRAFT, producer planning. [Hub](planning.md) defines the binding verification/recovery rules and semantic coverage. [Path index](planning-path-ownership.md) expands every exact source ID. No implementation evidence or independent approval is claimed here.

## CY062

**Built and separately installed distribution**

- **Semantic predecessors:** [CY032](planning-artifacts-mutation.md#cy032), [CY033](planning-artifacts-mutation.md#cy033), [CY034](planning-artifacts-mutation.md#cy034), [CY035](planning-artifacts-mutation.md#cy035), [CY036](planning-artifacts-mutation.md#cy036), [CY037](planning-artifacts-mutation.md#cy037), [CY038](planning-artifacts-mutation.md#cy038), [CY039](planning-artifacts-mutation.md#cy039), [CY040](planning-artifacts-mutation.md#cy040), [CY042](planning-artifacts-mutation.md#cy042), [CY043](planning-artifacts-mutation.md#cy043), [CY044](planning-artifacts-mutation.md#cy044), [CY045](planning-artifacts-mutation.md#cy045), [CY046](planning-artifacts-mutation.md#cy046), [CY047](planning-artifacts-mutation.md#cy047), [CY048](planning-artifacts-mutation.md#cy048), [CY049](planning-artifacts-mutation.md#cy049), [CY050](planning-artifacts-mutation.md#cy050), [CY051](planning-artifacts-mutation.md#cy051), [CY059](planning-artifacts-mutation.md#cy059), [CY060](planning-artifacts-mutation.md#cy060), [CY061](planning-artifacts-mutation.md#cy061).
- **Shared-file predecessors:** [CY027](planning-execution.md#cy027).
- **Authority:** [DI-06 §§7.6–7.7; DI-08 TEST-E06](design-distribution.md).
- **CY062.D1 — bounded result:** Build source suite/defaults plus all bundled manifests/scripts/schemas/dependencies; isolated installed fixture outside checkout. This installation proof is independent of F-10 activation; it may be executed before CY063, CY064, CY065, CY066, CY067 when its dependencies are complete.
- **Preserved behavior:** Official adapters stay outside copied assets; dotfiles retained; workspace adapters/config remain owner-owned.
- **CY062.D2 — independent evidence:** Inspect wheel and invoke installed entrypoints with actual imported header library; no source fallback or auto dependency installation; real first-v3 candidate validated.
- **Rollback:** R-CY062: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY062.D1 and CY062.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C006, S038, S039, S040, S041, T017.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `tests/mcp_server/fixtures/installed_distribution.py`
- `tests/mcp_server/integration/test_installed_distribution_v3.py`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/test_installed_distribution_v3.py`

Existing affected test/helper sources: S039, T017. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY062, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY063

**Operational components and selection**

- **Semantic predecessors:** [CY004](planning-execution.md#cy004), [CY005](planning-execution.md#cy005), [CY006](planning-execution.md#cy006), [CY007](planning-execution.md#cy007).
- **Shared-file predecessors:** [CY006](planning-execution.md#cy006).
- **Authority:** [DI-06 §§5.2–5.4,7.1,10](design-distribution.md).
- **CY063.D1 — bounded result:** Full-file operational fingerprints and pure adopted/actual/candidate component selection.
- **Preserved behavior:** Policy/.version included, absence first-class, manifest-ID keys; no pf/sf overwrite authority or per-file merge.
- **CY063.D2 — independent evidence:** Independent vectors plus five relations/add/remove/conflict matrix; unrelated local component preserved.
- **Rollback:** R-CY063: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY063.D1 and CY063.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: T093.

Read-only review/preservation IDs: C093. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/services/template_components.py`
- `tests/mcp_server/unit/services/test_template_components.py`
- `mcp_server/services/template_renewal.py`

Previously introduced paths revisited in this cycle:

- `mcp_server/services/artifact_identity.py`

Independent QA identified this bounded shared-primitive exposure under the user's standing authorization: reuse D-SUITE-30 record framing and source normalization through public names, preserving existing generation bytes. No second fingerprint engine or broader generation change is permitted.

Implementation process record: the initial CY063 production implementation preceded its first test run and had no RED commit. The independent QA repair subsequently demonstrated the real empty-shared defect before fixing production, but that RED state was not committed separately. The first repair run also contained an incorrect lifecycle expectation, which was corrected independently of the production fix. No historical test-first sequence or RED commit is claimed. Final behavior and scoped evidence remain subject to independent QA review.

- The listed legacy review-only paths retain their current constructors, runtime reads and normal registration. New behavior is exercised through the separately named final internal components; no V2/V3 ToolAssembly union, public alias, fallback reader or constructor mode.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/services/test_template_components.py`

Existing affected test/helper sources: T093. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY063, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY064

**Installation checkpoint and first-v3 bootstrap**

- **Semantic predecessors:** [CY063](planning-rollout.md#cy063).
- **Shared-file predecessors:** [CY052](planning-artifacts-mutation.md#cy052), [CY061](planning-artifacts-mutation.md#cy061), [CY063](planning-rollout.md#cy063).
- **Authority:** [DI-06 §§7.2,9–10](design-distribution.md).
- **CY064.D1 — bounded result:** Closed installation.json contract, trustworthy bootstrap and one-time compatibility-value migration.
- **Preserved behavior:** Checkpoint-less pre-v3 not fresh; preserve actual; no fabricated checkpoint from metadata/.version.
- **CY064.D2 — independent evidence:** Fresh/equal/trusted/unknown/external cases; candidate invalid cannot advance checkpoint; first-v3 checkpoint_required and acknowledgement-only effects.
- **Rollback:** R-CY064: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY064.D1 and CY064.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C057, C060, S036, S037, T048, T064, T070, T091, T093, T096.

Read-only review/preservation IDs: C055, C063, C093. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/config/schemas/installation.py`
- `mcp_server/services/installation_state.py`
- `tests/mcp_server/unit/services/test_installation_state.py`

Previously introduced paths revisited in this cycle:

- `mcp_server/services/template_renewal.py`
- `mcp_server/services/template_components.py`

Independent QA identified one bounded predecessor correction: reuse the existing `TemplateId` type for component-state and selection identities instead of rejecting manifest IDs with an additional path-like restriction. Preserve the authored ID unchanged through component and checkpoint construction; do not modify `TemplateId` or filesystem path admission.

- The listed legacy review-only paths retain their current constructors, runtime reads and normal registration. New behavior is exercised through the separately named final internal components; no V2/V3 ToolAssembly union, public alias, fallback reader or constructor mode.
- Introduce installation-state reading independently. The existing normal startup version/root reader is unchanged here; complete target startup integration is explicitly owned by CY071 and public activation by CY072.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/services/test_installation_state.py`

Existing affected test/helper sources: T048, T064, T070, T091, T093, T096. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY064, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY065

**Candidate staging and proposal admission**

- **Semantic predecessors:** [CY026](planning-execution.md#cy026), [CY032](planning-artifacts-mutation.md#cy032), [CY033](planning-artifacts-mutation.md#cy033), [CY034](planning-artifacts-mutation.md#cy034), [CY035](planning-artifacts-mutation.md#cy035), [CY036](planning-artifacts-mutation.md#cy036), [CY037](planning-artifacts-mutation.md#cy037), [CY038](planning-artifacts-mutation.md#cy038), [CY039](planning-artifacts-mutation.md#cy039), [CY040](planning-artifacts-mutation.md#cy040), [CY042](planning-artifacts-mutation.md#cy042), [CY043](planning-artifacts-mutation.md#cy043), [CY044](planning-artifacts-mutation.md#cy044), [CY045](planning-artifacts-mutation.md#cy045), [CY046](planning-artifacts-mutation.md#cy046), [CY047](planning-artifacts-mutation.md#cy047), [CY048](planning-artifacts-mutation.md#cy048), [CY049](planning-artifacts-mutation.md#cy049), [CY050](planning-artifacts-mutation.md#cy050), [CY051](planning-artifacts-mutation.md#cy051), [CY064](planning-rollout.md#cy064).
- **Shared-file predecessors:** [CY005](planning-execution.md#cy005), [CY063](planning-rollout.md#cy063).
- **Authority:** [DI-06 §§5.5,7.3,7.7](design-distribution.md).
- **CY065.D1 — bounded result:** Flat candidate staging/supersession and complete off-root proposal under effective actual configuration.
- **Preserved behavior:** Config/native/trust bytes unchanged; external config root honored; candidate vs proposal invalid distinct.
- **CY065.D2 — independent evidence:** Real complete suite/profile resolution, missing profile identifies source; native absence causes no renewal probe; no alternative component search.
- **Rollback:** R-CY065: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY065.D1 and CY065.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: T093.

Read-only review/preservation IDs: C093. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/services/template_proposal.py`
- `tests/mcp_server/integration/test_template_proposal.py`

Previously introduced paths revisited in this cycle:

- `mcp_server/services/template_renewal.py`
- `mcp_server/services/template_catalog.py`

Independent QA identified a bounded diagnostic seam: enrich the existing policy-validation exception inside `_load_package` with the already admitted manifest ID, output profile and suite-relative policy source, preserving its class, code, message and cause. The proposal service supplies effective configuration-source context. No callback-order state, duplicate parser or catalog constructor change is permitted.

Execution evidence limitation: the initial RED run (`91ca04aff17e4218887e70dbf557e34d`, commit `8548c31fc436fc3c8ee750d4afd1cf9647f0914d`) failed during collection on a scaffold import of `backend`; it is not valid behavioral RED evidence. The subsequent QA corrections use independently observed defects and fresh focused regression evidence. Historical RED is not reconstructed.

- The listed legacy review-only paths retain their current constructors, runtime reads and normal registration. New behavior is exercised through the separately named final internal components; no V2/V3 ToolAssembly union, public alias, fallback reader or constructor mode.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/test_template_proposal.py`

Existing affected test/helper sources: T093. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY065, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY066

**F-10 activation and deterministic recovery**

- **Semantic predecessors:** [CY065](planning-rollout.md#cy065).
- **Shared-file predecessors:** [CY055](planning-artifacts-mutation.md#cy055), [CY064](planning-rollout.md#cy064), [CY065](planning-rollout.md#cy065).
- **Authority:** [DI-06 §§7.5,8,10](design-distribution.md).
- **CY066.D1 — bounded result:** Cross-process exclusion, fixed same-filesystem next/previous trees, recovery record and atomic checkpoint publication.
- **Preserved behavior:** One coherent authoritative tree/checkpoint; running catalog stable; forced backup separate; native fixes unrelated.
- **CY066.D2 — independent evidence:** DI-06 fault matrix through public activation service and real OS processes: recognized interruption restores prior tree/checkpoint or completes target pair, unknown state remains untouched, concurrent activations are excluded. This does not certify normal bootstrap; CY071 and CY072 explicitly own actual startup-lock/recovery integration.
- **Rollback:** R-CY066: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY066.D1 and CY066.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: S033, S034, S035, S036, T048, T093.

Read-only review/preservation IDs: C093. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/services/template_activation.py`
- `tests/mcp_server/integration/test_template_activation.py`

Previously introduced paths revisited in this cycle:

- `mcp_server/services/template_renewal.py`
- `tests/mcp_server/integration/test_template_proposal.py`

Independent QA authorized extracting only the existing real admission factory assembly into the public T048 helper with explicit config and adapter roots. The proposal test retains a thin delegate; production admission and its evidence computation stay unchanged. Reuse this composition for activation evidence and rerun the affected proposal tests once.

- The listed legacy review-only paths retain their current constructors, runtime reads and normal registration. New behavior is exercised through the separately named final internal components; no V2/V3 ToolAssembly union, public alias, fallback reader or constructor mode.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/test_template_activation.py`

Existing affected test/helper sources: S035, T048, T093. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY066, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY067

**Prepared renewal CLI composition**

- **Semantic predecessors:** [CY066](planning-rollout.md#cy066).
- **Shared-file predecessors:** [CY064](planning-rollout.md#cy064).
- **Authority:** [DI-06 §§7.4,8–10](design-distribution.md).
- **CY067.D1 — bounded result:** Introduce final CLI renewal command/composition and dedicated result presenter, tested on isolated roots. Leave normal cli.py dispatch and legacy WorkspaceUpgrader active until CY072.
- **Preserved behavior:** Exit 0/2/1, actual_changed-only restart hint; explicit owner actions never overwrite external/config content.
- **CY067.D2 — independent evidence:** CLI public-result/filesystem tests; mutually exclusive modifiers, verified force backup, checkpoint-only no-copy, full actionable component output.
- **Rollback:** R-CY067: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY067.D1 and CY067.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: T048, T093, T096.

Read-only review/preservation IDs: C056, C063, C093. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/presenters/renewal_presenter.py`
- `tests/mcp_server/integration/test_renewal_cli.py`
- `mcp_server/cli_renewal.py`

Previously introduced paths revisited in this cycle:

- `mcp_server/services/template_renewal.py`
- `mcp_server/services/template_activation.py` — independent QA-directed CY067 revisit: project prior/target recovery effects into the immutable result before cleanup; no recovery algorithm change. Covered by one real CLI recovery regression and retained CY066 process evidence.

- The listed legacy review-only paths retain their current constructors, runtime reads and normal registration. New behavior is exercised through the separately named final internal components; no V2/V3 ToolAssembly union, public alias, fallback reader or constructor mode.
- Prepared --init/--upgrade handling is not yet publicly dispatched. Installed rehearsal must prove init-to-startup and upgrade-to-explicit-owner-migration-to-startup before the actual switch.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/test_renewal_cli.py`

Existing affected test/helper sources: T048, T093, T096. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY067, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY068

**Workflow carriers and phase semantics**

- **Semantic predecessors:** [CY042](planning-artifacts-mutation.md#cy042), [CY043](planning-artifacts-mutation.md#cy043), [CY044](planning-artifacts-mutation.md#cy044), [CY045](planning-artifacts-mutation.md#cy045), [CY056](planning-artifacts-mutation.md#cy056), [CY057](planning-artifacts-mutation.md#cy057), [CY058](planning-artifacts-mutation.md#cy058), [CY059](planning-artifacts-mutation.md#cy059), [CY060](planning-artifacts-mutation.md#cy060), [CY061](planning-artifacts-mutation.md#cy061).
- **Shared-file predecessors:** None.
- **Authority:** [DI-07 §§7.1–7.2/10](design-workflow-documentation.md).
- **CY068.D1 — bounded result:** Prepare and verify the exact bounded target-source diff for nineteen workflow carriers, tool names, input-removal and conditional schema guidance. Store the reviewed patch/checksums as implementation evidence; do not advertise inactive V3 contracts in live source/copies.
- **Preserved behavior:** Substantive phase actions, approval gates and workflow differences; valid scaffold distinct from phase completion.
- **CY068.D2 — independent evidence:** DOCFLOW-E01/02; actual contract loading plus schema/render carrier evidence, no copied complete invocation payloads. Apply the prepared diff only to explicit isolated source copies for evidence. Live source/copy application and byte parity are CY072 obligations. The recorded patch is temporary migration evidence, never runtime configuration or a second instruction authority.
- **Rollback:** R-CY068: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY068.D1 and CY068.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: T066, T138.

Read-only review/preservation IDs: C003. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `docs/development/issue460/rollout-workflow-input.md`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/config/test_contracts_loader.py`
- `tests/mcp_server/unit/tools/test_discovery_tools.py`

Existing affected test/helper sources: T066, T138. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY068, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY069

**Host instruction source parity**

- **Semantic predecessors:** [CY068](planning-rollout.md#cy068), [CY011](planning-execution.md#cy011).
- **Shared-file predecessors:** None.
- **Authority:** [DI-07 §7.3/10](design-workflow-documentation.md).
- **CY069.D1 — bounded result:** Prepare and verify the exact bounded target-source diff for source-authoritative host instructions and their real mapped copies. Store the reviewed patch/checksums as implementation evidence; do not advertise inactive V3 contracts in live source/copies. Prepare the general Resource Caching procedure in the authoritative host instruction sources and exact mapped copies already listed here, using CY011's proven generic read recipe; no role-specific protocol forks or dependency on issue460 documentation. This is preparation only; CY072 owns live installation.
- **Preserved behavior:** QA read-only authority, research/coordination permissions and unaffected reboot; exclude machine connections/credentials.
- **CY069.D2 — independent evidence:** DOCFLOW-E03/05; source-first exact pair byte equality and role checks; no whole-directory overwrite. Apply the prepared diff only to explicit isolated source copies for evidence. Live source/copy application and byte parity are CY072 obligations. The recorded patch is temporary migration evidence, never runtime configuration or a second instruction authority. In isolated mapped host assets, verify a fresh agent receives the general procedure through its normal startup instruction route, with no prior chat or injected recipe. Match the procedure semantically to CY011's live hint and existing window contract, including truncation retry and expired-cache recovery.
- **Rollback:** R-CY069: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY069.D1 and CY069.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: None.

Read-only review/preservation IDs: C008, C009, C010, C011, C012, C013, C014, C015, C016, C017, C019, C020, C021, C022, C023, C024, C025, C121, C122, C123, S040. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `docs/development/issue460/rollout-host-input.md`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Documentation evidence: compare the exact named sources against their Design dispositions, verify actionable examples/links and actual source-copy direction. No artificial test is required.

Existing affected test/helper sources: None. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY069, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY070

**Prepared placement and rollout configuration**

- **Semantic predecessors:** [CY052](planning-artifacts-mutation.md#cy052), [CY057](planning-artifacts-mutation.md#cy057), [CY058](planning-artifacts-mutation.md#cy058), [CY059](planning-artifacts-mutation.md#cy059), [CY060](planning-artifacts-mutation.md#cy060), [CY061](planning-artifacts-mutation.md#cy061), [CY062](planning-rollout.md#cy062), [CY067](planning-rollout.md#cy067), [CY022](planning-execution.md#cy022).
- **Shared-file predecessors:** None.
- **Authority:** [DI-04 §3.3, DI-05 §7.20 and DI-06 §§7.7/9](design-integration-review.md).
- **CY070.D1 — bounded result:** Prepare the exact replacement artifacts.yaml and presentation/root/version compatibility changes against actual owner configuration; reconcile every target profile and installed-source declaration. Keep incompatible live config bytes unchanged until activation. Include the exact [tool.pyright]-only deletion hunk in rollout-config-input.md using CY022 preserved-value evidence; no other TOML settings may be removed. Capture the current section's preimage and resulting native-value checks for CY071 rehearsal and CY072 application.
- **Preserved behavior:** Actual configuration/customization remains owner-controlled; first-v3 actual is not a fresh install, and no native dependency or missing profile is silently filled.
- **CY070.D2 — independent evidence:** Apply the exact prospective config diff on isolated copies of actual config; public target loaders accept every reference and reject obsolete inputs. Record exact preimage/postimage hashes and mismatch refusal; no whole-file overwrite of concurrent edits. Verify Pyright preserved-value evidence against the current pyproject.toml/pyrightconfig.json pair; drift requires fresh CY022-scoped value proof before rehearsal.
- **Rollback:** R-CY070: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY070.D1 and CY070.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: None.

Read-only review/preservation IDs: C004, C005, C006, C063, C106, S008, S017, S051. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `docs/development/issue460/rollout-config-input.md`
- `tests/mcp_server/integration/test_rollout_configuration.py`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/test_rollout_configuration.py`

Existing affected test/helper sources: None. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY070, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY071

**Target startup composition and launch rehearsal**

- **Semantic predecessors:** [CY070](planning-rollout.md#cy070), [CY068](planning-rollout.md#cy068), [CY069](planning-rollout.md#cy069), [CY062](planning-rollout.md#cy062), [CY066](planning-rollout.md#cy066), [CY067](planning-rollout.md#cy067).
- **Shared-file predecessors:** [CY009](planning-execution.md#cy009), [CY064](planning-rollout.md#cy064), [CY052](planning-artifacts-mutation.md#cy052), [CY011](planning-execution.md#cy011), [CY001](planning-execution.md#cy001), [CY056](planning-artifacts-mutation.md#cy056), [CY005](planning-execution.md#cy005), [CY061](planning-artifacts-mutation.md#cy061), [CY030](planning-execution.md#cy030), [CY010](planning-execution.md#cy010).
- **Authority:** [DI-05 §7.6, DI-06 §7.5 and DI-08 §7.4](design-integration-review.md).
- **CY071.D1 — bounded result:** Add the final explicit runtime composition at bootstrap without changing its normal entrypoint yet. Compose one target ToolAssembly with the six target schema/mutation/check/test/fix tools, unchanged unrelated tools, explicit root/config/installation readers and the DI-06 startup lock. Never union V2 and V3 same-name tools.
- **Preserved behavior:** The current normal entrypoint still constructs only its working legacy assembly. New startup takes the activation lock, rejects unresolved recovery without mutation, preserves unrelated enforcement/Git/GitHub behavior and probes no native availability.
- **CY071.D2 — independent evidence:** Short-lived real process/MCP handshake on explicit roots and a separately installed candidate; final planned dispatch diff applied only to an isolated source copy. Match interpreter/import/CWD/roots/relevant launch environment to the active launcher rather than inheriting PytestRunner PATH blindly. Prove current normal startup remains usable, target no duplicate names, init/startup and upgrade/owner-migration/startup, concurrent startup exclusion, unresolved recovery refusal and old immutable catalog stability. Record exact rehearsed input hashes. Rehearse the exact [tool.pyright] deletion prepared by CY070 and recheck the native values already proved by CY022; the live TOML section is still retained. Rehearse CY069's cache-read instruction patch with the candidate's actual rendered cache hint and mapped startup assets; any mismatch returns to the owning preparation cycle before activation.
- **Rollback:** R-CY071: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY071.D1 and CY071.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Readback prerequisite supplement: [R001–R008](planning-path-ownership.md#readback-prerequisite-supplement). R004/R005/R006 are read-only live inputs. Prepare their exact fixture/config/template acquisition hunks and preimages, apply them only to the isolated candidate alongside the exact dispatch diff, and run the candidate's normal bootstrap/readback tests there. The active legacy checkout retains its unchanged passing tests. Preserve save/update/full readback, invalid-query source bytes and command recovery. Only CY072 may apply these prepared test hunks to live source; neither a new product mode nor a second registered server is introduced. D1/D2 and this cycle's R-CY071, preserved behavior and independent stop/go apply to these exact additional seams.

Existing source IDs: C055, C057, C058, C060, C085, C107, S012, S013, S016, S037, S049, S050, T048, T060, T064, T067, T068, T069, T073, T074, T075, T091, T095, T097, T098, T099, T109, T110, T134.

Read-only review/preservation IDs: C063, C064, C066, C086, C087, C093, C094, C096, C097, C098, S008, S017, S018, R001, R002, R003, R007, R008, R004, R005, R006. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `tests/mcp_server/fixtures/server_process.py`
- `tests/mcp_server/integration/test_target_startup.py`
- `docs/development/issue460/rollout-rehearsal.md`

Previously introduced paths revisited in this cycle:

- `mcp_server/services/template_catalog.py`
- `mcp_server/services/installation_state.py`
- `mcp_server/cli_renewal.py`

- Before release from this cycle, prepare the exact scoped code/config/suite/installation recovery instructions and identify the existing host/client action available if MCP is down. This is operational documentation; no parallel persistent server, new recovery daemon or startup-health feature.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/tools/test_project_tools.py`
- `tests/mcp_server/unit/managers/test_project_manager.py`
- `tests/mcp_server/integration/test_project_plan_readback.py`
- `tests/mcp_server/integration/test_target_startup.py`

Existing affected test/helper sources: S012, S013, S016, S050, T048, T060, T064, T067, T068, T069, T073, T074, T075, T091, T095, T097, T098, T099, T109, T110, T134. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY071, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY072

**Public V3 cutover**

- **Semantic predecessors:** [CY071](planning-rollout.md#cy071).
- **Shared-file predecessors:** [CY052](planning-artifacts-mutation.md#cy052), [CY062](planning-rollout.md#cy062), [CY061](planning-artifacts-mutation.md#cy061), [CY067](planning-rollout.md#cy067), [CY026](planning-execution.md#cy026), [CY028](planning-execution.md#cy028), [CY030](planning-execution.md#cy030), [CY012](planning-execution.md#cy012), [CY001](planning-execution.md#cy001), [CY009](planning-execution.md#cy009), [CY010](planning-execution.md#cy010).
- **Authority:** [DI-01/04/05 cutover; DI-06 §9; DI-07 §7.3](design-suite-resolution.md).
- **CY072.D1 — bounded result:** Apply only the previously rehearsed activation diff: normal bootstrap/CLI dispatch, owned config/root/version selection, removal of quality.yaml from active config, and prepared workflow/host source-copy changes. No new execution, migration, schema, presenter or test-helper algorithm is introduced here. This cycle is the sole owner of removing duplicate [tool.pyright] from live pyproject.toml: apply only CY070's recorded hunk already rehearsed by CY071.
- **Preserved behavior:** Unrelated tools/enforcement/cache/state; new names only, run_tests new contract, actionable V2 config rejection, no aliases/dual reads.
- **CY072.D2 — independent evidence:** Preimage hashes match the rehearsed set; otherwise stop and refresh only invalidated preparation evidence. Migrate only this repository's owned root by the approved explicit DI-06 route with captured code/config/suite/installation recovery basis. Run the real target entrypoint against the landed bytes before restart. While the existing MCP route remains available correct any failures; then one deliberate restart_server boundary, client rediscovery and real V3 schema/scaffold/edit/check/test/fix calls with separately identified evidence. Verify fresh init/startup and owner-migration/startup. If MCP is absent/degraded after restart, stop mutations and use the pre-recorded existing host/client recovery action; no automatic rollback claim. Verify the duplicate TOML section is absent and Pyright still uses the preserved pyrightconfig.json values; drift from the rehearsed hunk stops activation. After rediscovery, a fresh chat using the actual installed host instructions and ordinary tool output must discover and reconstruct a large resource without this conversation, the issue hub or a supplied window recipe. Capture the actual calls and verified complete contents; missing guidance, stale/mixed windows or dependence on producer coaching blocks progression. Apply only CY069's instruction patch already rehearsed in CY071; do not design instructions at cutover.
- **Rollback:** R-CY072: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY072.D1 and CY072.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Readback prerequisite supplement: [R001–R008](planning-path-ownership.md#readback-prerequisite-supplement). R004/R005/R006 have one live cutover owner: CY072. Check their recorded preimages, apply only the exact test hunks rehearsed with the candidate in CY071, and run those same assertions against the landed normal bootstrap, including public full-response/window reconstruction. R002/R003 remain read-only. A new hunk, changed fixture policy or mismatched preimage stops the cycle and returns preparation to CY071; no new migration decision belongs here. D1/D2 and this cycle's R-CY072, preserved behavior and independent stop/go apply to these exact additional seams.

Existing source IDs: C003, C004, C005, C006, C008, C009, C010, C011, C012, C013, C014, C015, C016, C017, C019, C020, C021, C022, C023, C024, C025, C055, C056, C063, C106, C121, C122, C123, S051, T006, T066, T091, T096, T138, R004, R005, R006.

Owner-authorized bounded QA finding (2026-09-23): T066 and T138 contain CY068 preparation-only assertions that reapply the prospective contracts patch to the live preimage and therefore fail after the CY072 cutover. CY072 may update only those stale assertions to verify the landed V3 contract, retaining the nineteen workflow-carrier and public `get_work_context` claims. Their original owner remains CY068; this addition changes no production boundary or migration strategy. The earlier owner authorization for proportionate, independently identified test maintenance applies to these two files.

Independent QA also identified stale CY070 preparation-only assertions in `tests/mcp_server/integration/test_rollout_configuration.py` after the exact live config cutover. CY072 may maintain only that file's affected preimage/drift checks so they prove the landed V3 config while retaining the isolated drift and native-Pyright claims; its original owner remains CY070. This is the same owner-authorized proportional test-maintenance exception, with no new production seam.

Owner-approved CY072 correction (2026-09-23; provenance: CY071 installed-candidate rehearsal and CY066 activation): independent QA found that R006's exact rehearsal hunk selects only packaged `assets/template_suite`, absent in this source checkout. Keep packaged assets preferred and use the checked-out `.pgmcp/template_suite` only for this source-layout fixture; preserve all readback assertions. A separate mixed-root force attempt exposed an unconditional legacy-inventory comparison after the prior V3 suite had already been backed up. Limit the activation correction to checking live legacy inventory only when that inventory is part of the backup, and add one public force-activation regression with a prior V3 suite plus retained legacy files. These two exact corrections are explicitly approved for CY072 instead of a return to CY071; all other stop/go rules and the no-new-algorithm boundary remain.

Read-only review/preservation IDs: S008, S049, S050, R002, R003. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `tests/mcp_server/integration/test_v3_cutover.py`

Previously introduced paths revisited in this cycle:

- `.pgmcp/config/checks.yaml`
- `.pgmcp/config/tests.yaml`
- `.pgmcp/config/fixes.yaml`
- `.pgmcp/config/adapters.yaml`

- The activation write-set includes mechanically paired instruction copies because they must become truthful at the same public switch. Their content and semantic review belong to the preceding preparation cycles; this cycle owns only exact application, parity and normal-launch evidence.
- Keep legacy templates and inactive modules on disk through the successful new-server handshake and targeted calls. Remove them only in their named later cycles; the old live safe-edit validator still reads templates from disk before restart.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/tools/test_project_tools.py`
- `tests/mcp_server/unit/managers/test_project_manager.py`
- `tests/mcp_server/integration/test_project_plan_readback.py`
- `tests/mcp_server/integration/test_v3_cutover.py`
- `tests/mcp_server/unit/config/test_contracts_loader.py`
- `tests/mcp_server/unit/tools/test_discovery_tools.py`

Existing affected test/helper sources: T006, T066, T091, T096, T138. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY072, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY073

**Close legacy scaffold harness imports**

- **Semantic predecessors:** [CY072](planning-rollout.md#cy072).
- **Shared-file predecessors:** [CY071](planning-rollout.md#cy071), [CY057](planning-artifacts-mutation.md#cy057).
- **Authority:** [DI-08 §7.3 and TEST-E07/08](design-test-architecture.md).
- **CY073.D1 — bounded result:** Remove only ArtifactManager/TemplateScaffolder/ValidationService/legacy-registry imports and builders from artifact_test_harness and shared support after migrating their named public tests. Rewire root plugin registration to the narrow support already introduced; preserve workflow_fixtures and unrelated environment/GitHub behavior.
- **Preserved behavior:** Unrelated PR-lock, merge escape hatch, workflow roots, cache/atomic helpers and real server registration remain independently observable.
- **CY073.D2 — independent evidence:** Fixture-request/import/plugin search closes the retired builder set. Collect all surviving tests that requested those fixtures; run PR-lock, server/cycle and public scaffold/error successors. No delayed import hack or broad replacement harness is allowed.
- **Rollback:** R-CY073: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY073.D1 and CY073.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Readback prerequisite supplement: [R001–R008](planning-path-ownership.md#readback-prerequisite-supplement). Include R004/R005/R006 in test_support import/fixture closure before the first scaffold dependency is deleted. Keep project-manager support that still has callers; these rows authorize review only. D1/D2 and this cycle's R-CY073, preserved behavior and independent stop/go apply to these exact additional seams.

Existing source IDs: C055, C124, C126, S012, S013, S016, T001, T004, T005, T008, T012, T013, T014, T015, T016, T019, T020, T021, T022, T048, T075, T076, T078, T099, T151.

CY073 scope amendment (user-authorized, 2026-09-23): retire the thirteen legacy tests that directly consume `artifact_test_harness` or `make_artifact_manager`, together with their now-exhausted test builders. Their surviving public claims are covered by the V3 scaffold, operation, catalog, identity and header tests; add only a missing public unknown-selection case if that claim is not yet explicit. This advances test retirement from CY074/CY079 (or assigns previously unowned T016/T022), not production retirement or any Approved Strategy. Later cycles treat these removed paths as absence/import-closure review, never recreation. No template-content assertions are added.

CY073 resource prerequisite (independent QA finding, covered by the user's standing authorization for bounded QA-designated corrections): the live `pgmcp://rules/coding_standards` resource still reads removed `quality.yaml`. Advance only C124's versioned V3 resource projection, the C055 target composition handoff, C126's resource-reference section, T151's existing resource test and the existing server-startup read assertion. Construct the resource from the already validated immutable `checks.yaml`, `tests.yaml` and `fixes.yaml` models at target startup. Expose a versioned, bounded configured-policy summary without old numbered gates, fixed coverage, a second config read or a legacy alias. Only target bootstrap injects this resource into shared resource assembly; the inactive V2 path gets no replacement resource and is retired in CY074. CY090 retains unrelated standards/documentation reconciliation. The three server-startup tests must pass before CY073 progression; older private V2 bootstrap tests remain for their later removal owner and are not CY073 evidence.

Read-only review/preservation IDs: R004, R005, R006. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

- `tests/mcp_server/integration/test_scaffold_public_v3.py` (one public unknown-selection envelope case).
- `tests/mcp_server/integration/mcp_server/test_server_startup.py` (one V3 standards-resource read assertion).

- Remove each legacy helper import at the first deleted production dependency, even though final removal of empty/exhausted helper files and registrations is separately scheduled. Other helper seams such as QAManager are owned by their later consumer-removal cycles.

Scope is limited to D1, the QA-found resource prerequisite above, and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/tools/test_project_tools.py`
- `tests/mcp_server/unit/managers/test_project_manager.py`
- `tests/mcp_server/integration/test_project_plan_readback.py`
- `tests/mcp_server/integration/test_scaffold_public_v3.py`
- `tests/mcp_server/integration/test_edit_public_v3.py`
- `tests/mcp_server/integration/test_pr_status_lockdown.py`
- `tests/mcp_server/integration/mcp_server/test_server_startup.py`
- `tests/mcp_server/unit/resources/test_standards.py`
- `tests/mcp_server/unit/test_server.py`
- `tests/mcp_server/unit/tools/test_cycle_tools.py`

Existing affected test/helper sources: S012, S013, S016, T001, T004, T005, T008, T012, T013, T014, T015, T016, T019, T020, T021, T022, T048, T075, T076, T078, T099, T151 and `tests/mcp_server/integration/mcp_server/test_server_startup.py`. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY073, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY074

**Retire obsolete scaffold tool and manager route**

- **Semantic predecessors:** [CY072](planning-rollout.md#cy072), [CY073](planning-rollout.md#cy073).
- **Shared-file predecessors:** [CY053](planning-artifacts-mutation.md#cy053), [CY007](planning-execution.md#cy007), [CY006](planning-execution.md#cy006), [CY052](planning-artifacts-mutation.md#cy052), [CY057](planning-artifacts-mutation.md#cy057), [CY056](planning-artifacts-mutation.md#cy056).
- **Authority:** [DI-01/02 migration](design-suite-resolution.md), [DI-04 cleanup](design-mutation-validation.md), [DI-08 dispositions](design-integration-review.md).
- **CY074.D1 — bounded result:** Remove the inactive legacy scaffold/schema public wrappers and ArtifactManager, plus their now-exhausted old test slices and bootstrap imports. Keep TemplateScaffolder until the following renderer-retirement cycle.
- **Preserved behavior:** Already-proved public schema/scaffold/error/persistence behavior and unrelated tools; no production algorithm is added during deletion.
- **CY074.D2 — independent evidence:** Require successful public cutover first. Prove zero remaining production imports and test collection references to each deleted module, preserving any unrelated assertions in shared tests. Run the named successor proofs and a fresh normal server startup/handshake before accepting the commit.
- **Rollback:** R-CY074: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY074.D1 and CY074.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C055, C064, C097, C098, T001, T005, T008, T012, T013, T014, T015, T017, T020, T021, T048, T060, T075, T076, T077, T078, T079, T080, T091, T095, T099, T103, T104.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

- `tests/mcp_server/integration/test_scaffold_public_v3.py` (only catalog-derived admitted enum and strict extra-field behavior, as successors for T060/T099).
- `tests/mcp_server/fixtures/installed_distribution.py` (only optional active-launcher interpreter for the installed-candidate wheel build/install/probes; default behavior for other callers remains unchanged).
- `tests/mcp_server/integration/test_target_startup.py` (only retire obsolete pre-cutover candidate preparation and duplicate candidate-readback rehearsal while retaining installed fresh/migration/stdio assertions).

- Only retire named obsolete bodies/imports/tests. Existing test rows may already have migrated; delete only superseded claims and retain their Design-mandated observable successors. T009 is limited to its TemplateScaffolder-dependent output cases and imports; preserve its unrelated cases for CY095. T079 contains only TemplateScaffolder signature/NoteContext cases and retires after the already-proved public error/schema successors. This amendment closes the two additional direct test imports found before deletion; any further caller still stops this cycle for a bounded amendment.

- Close the last ArtifactManager imports in T013/T015/T077/T080 here even when later registry/metadata/location-only assertions survive. Their later cycles may handle only claims independent of the deleted manager.

- CY074 startup-fixture amendment (independent QA NOGO; user-approved clean post-cutover disposition, 2026-09-24): `tests/mcp_server/integration/test_target_startup.py` is a newly added exact test path; T048 names the separate `test_support.py` file. Retire the candidate-only R004/R005/R006 source-copy rehearsal and pre-cutover host/pyproject/config/CLI patch steps. The landed live R004/R005/R006 claims remain executable (15 focused tests passed). Build the installed candidate from current V3 source; retain fresh installation, owner-migrated upgrade/readback and real stdio handshake assertions. Compare the interpreter observed inside the launched candidate with the configured launcher, not with the separate pytest runner; preserve PATH and installed module-origin checks. No production change or skipped installed migration test is permitted.

- CY074 import-closure amendment (independent QA preflight, 2026-09-24): six additional existing test files still import the modules retired here. Retire T017's legacy all-type manager smoke only after mapping its family rendering and complete installed-catalog claims to the existing V3 package-family and catalog tests, and its public routing claim to `test_scaffold_public_v3.py`; no template-content assertions are added. In T014 substitute the V3 scaffold tool class while retaining PR-lock coverage. In T060 retire only the old registry-derived enum assertions after checking the V3 catalog-derived public schema successor, preserving phase/issue/workflow assertions. In T075 retire only the old schema tool member of the mixed tool list, retaining all unrelated tools and schema/name checks. In T095 retire only the ArtifactManager-specific root class after checking explicit-root V3 target and atomic-writer proofs, retaining unrelated state/root tests. In T099 retire only the old scaffold input row after checking V3 strict public admission, retaining other input models. These six changes are import closure, not new production scope; a missing successor stops the affected deletion.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/test_schema_public_v3.py`
- `tests/mcp_server/integration/test_scaffold_public_v3.py`

Existing affected test/helper sources: T001, T005, T008, T012, T013, T014, T015, T017, T020, T021, T048, T060, T075, T076, T077, T078, T079, T080, T091, T095, T099, T103, T104. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY074, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY075

**Retire obsolete template scaffolder route**

- **Semantic predecessors:** [CY074](planning-rollout.md#cy074).
- **Shared-file predecessors:** [CY005](planning-execution.md#cy005), [CY056](planning-artifacts-mutation.md#cy056).
- **Authority:** [DI-01/02 migration](design-suite-resolution.md), [DI-04 cleanup](design-mutation-validation.md), [DI-08 dispositions](design-integration-review.md).
- **CY075.D1 — bounded result:** Remove TemplateScaffolder and its BaseScaffolder/ScaffoldResult support; remove obsolete eager exports together. Retain the separate scaffolding.base/components stack until its own retirement.
- **Preserved behavior:** Already-proved public schema/scaffold/error/persistence behavior and unrelated tools; no production algorithm is added during deletion.
- **CY075.D2 — independent evidence:** Require successful public cutover first. Prove zero remaining production imports and test collection references to each deleted module, preserving any unrelated assertions in shared tests. Run the named successor proofs and a fresh normal server startup/handshake before accepting the commit.
- **Rollback:** R-CY075: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY075.D1 and CY075.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C066, C088, C089, C090, T009, T048, T079, T082, T083, T084, T085, T086.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

- Only retire named obsolete bodies/imports/tests. Existing test rows may already have migrated; delete only superseded claims and retain their Design-mandated observable successors. A remaining caller stops this cycle and requires an explicit bounded amendment before removal.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/services/test_template_catalog.py`
- `tests/mcp_server/integration/test_scaffold_operation_v3.py`
- `tests/mcp_server/integration/test_schema_public_v3.py`

Existing affected test/helper sources: T009, T048, T079, T082, T083, T084, T085, T086. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY075, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY076

**Retire obsolete workspace-upgrade route**

- **Semantic predecessors:** [CY072](planning-rollout.md#cy072).
- **Shared-file predecessors:** [CY067](planning-rollout.md#cy067).
- **Authority:** [DI-06 §§9–10](design-distribution.md), [T093/T096 dispositions](design-integration-review.md).
- **CY076.D1 — bounded result:** Remove inactive WorkspaceUpgrader and old blanket-copy/registry-preservation branches and tests now replaced by explicit renewal CLI. Preserve unrelated CLI commands and owner configuration.
- **Preserved behavior:** Renewal exits 0/2/1, owner-controlled actual/config, adopted checkpoint and forced backup/recovery guarantees remain distinct from F-20 native fixes.
- **CY076.D2 — independent evidence:** No retained imports of WorkspaceUpgrader or legacy suite-copy route; run public renewal CLI and target init/startup and owner-migration/startup proofs. Existing unrelated CLI cases collect and pass.
- **Rollback:** R-CY076: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY076.D1 and CY076.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C056, C093, T093, T096.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/test_renewal_cli.py`
- `tests/mcp_server/integration/test_target_startup.py`

Existing affected test/helper sources: T093, T096. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY076, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY077

**Retire legacy registry and hash authority**

- **Semantic predecessors:** [CY072](planning-rollout.md#cy072), [CY075](planning-rollout.md#cy075), [CY076](planning-rollout.md#cy076).
- **Shared-file predecessors:** [CY074](planning-rollout.md#cy074), [CY071](planning-rollout.md#cy071), [CY011](planning-execution.md#cy011), [CY006](planning-execution.md#cy006), [CY002](planning-execution.md#cy002), [CY073](planning-rollout.md#cy073).
- **Authority:** [DI-01/02 §9; Shared §12](design-suite-resolution.md).
- **CY077.D1 — bounded result:** Remove only obsolete registry/hash/artifact-registry paths and their last imports/tests after public target startup; preserve generation/schema successor evidence.
- **Preserved behavior:** Generation/header/schema claims already proved; no history replacement or edits to existing artifacts.
- **CY077.D2 — independent evidence:** Exact registry reader/writer/import closure; no state/history replacement. Collect affected test sources with zero stale imports; run admitted schema, identity and public introspection successors.
- **Rollback:** R-CY077: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY077.D1 and CY077.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C055, C057, C058, C060, C061, C080, C081, C085, C086, C107, S049, S050, T002, T003, T010, T015, T018, T048, T049, T059, T061, T062, T063, T064, T067, T068, T069, T073, T074, T077, T091, T095, T097, T098, T099.

Additional existing exact path discovered by import closure: `tests/mcp_server/test_artifacts_yaml_type_field.py` (retired registry-only test; no frozen source ID).

Read-only review/preservation IDs: C064, C066. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

- Close this cycle's specific retired exports/imports in shared schemas/interfaces/test_support and mixed tool-input tests at the same boundary; preserve unrelated GateReport/GateViolation workflow contracts.
- Import-closure amendment: T002 and T010 contain only retired artifact-registry loader claims; T003, T067, T073 and T074 are limited to their registry-dependent setup/assertions and retain unrelated project-structure, label, workflow and validator behavior. T018 is retired because its two public validation claims are already proved by current V3 `test_schema_public_v3.py` and `test_scaffold_public_v3.py` (including whole-schema resource equality and extra-field rejection); T097 and T098 retain their server/cycle claims by composing focused dispatch without the removed quality.yaml source, while their registration cases use isolated V3 target startup. The unindexed existing `tests/mcp_server/test_artifacts_yaml_type_field.py` is limited to retired artifact-registry type assertions. No new test or product behavior is authorized by this amendment.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/config/test_template_suite.py`
- `tests/mcp_server/unit/services/test_template_contract_loader.py`
- `tests/mcp_server/unit/utils/test_schema_utils.py`
- `tests/mcp_server/unit/services/test_artifact_identity.py`
- `tests/mcp_server/integration/test_schema_public_v3.py`

Existing affected test/helper sources: S050, T002, T003, T010, T015, T018, T048, T049, T059, T061, T062, T063, T064, T067, T068, T069, T073, T074, T077, T091, T095, T097, T098, T099, plus the unindexed exact test path above. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY077, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY078

**Retire legacy metadata and lifecycle contracts**

- **Semantic predecessors:** [CY077](planning-rollout.md#cy077).
- **Shared-file predecessors:** [CY072](planning-rollout.md#cy072), [CY074](planning-rollout.md#cy074), [CY007](planning-execution.md#cy007), [CY002](planning-execution.md#cy002).
- **Authority:** [DI-01/02 §9; Shared §12](design-suite-resolution.md).
- **CY078.D1 — bounded result:** Remove legacy source-header metadata config/parser and lifecycle exports plus their explicitly named test imports; retain V3 first-line reader and separate context/provenance.
- **Preserved behavior:** Generation/header/schema claims already proved; no history replacement or edits to existing artifacts.
- **CY078.D2 — independent evidence:** Record T090 retirement as an absence/import-closure observation and collect all surviving listed test files after removal; no imports of removed base/lifecycle/parser. Header adversarial cases and real scaffold context isolation remain covered.
- **Rollback:** R-CY078: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY078.D1 and CY078.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C007, C055, C057, C058, C059, C060, C078, C082, C083, C084, C085, C086, C106, C107, T013, T048, T050, T051, T052, T064, T065, T068, T069, T088, T090, T091, T095, T099.

Read-only review/preservation IDs: C064, C066. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

- Close this cycle's specific retired exports/imports in shared schemas/interfaces/test_support and mixed tool-input tests at the same boundary; preserve unrelated GateReport/GateViolation workflow contracts.
- Test disposition: T013 was already absent. T050–T052, T065, T088 and T090 contain only retired Tier 0 metadata/lifecycle assertions and are removed, without replacement content tests. Existing V3 header-reader and public scaffold tests carry the retained behavioral claims; T064 keeps its unrelated loader assertions.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/services/test_artifact_header_reader.py`
- `tests/mcp_server/integration/test_scaffold_public_v3.py`

Existing affected test/helper sources: T013, T048, T050, T051, T052, T064, T065, T068, T069, T088, T090, T091, T095, T099. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY078, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY079

**Retire legacy introspection and schema inference**

- **Semantic predecessors:** [CY078](planning-rollout.md#cy078).
- **Shared-file predecessors:** [CY053](planning-artifacts-mutation.md#cy053), [CY005](planning-execution.md#cy005), [CY004](planning-execution.md#cy004), [CY075](planning-rollout.md#cy075).
- **Authority:** [DI-01/02 §9; Shared §12](design-suite-resolution.md).
- **CY079.D1 — bounded result:** Remove only the superseded introspection/default/graph inference route and complete its named renderer/config test migration.
- **Preserved behavior:** Generation/header/schema claims already proved; no history replacement or edits to existing artifacts.
- **CY079.D2 — independent evidence:** No legacy introspection imports; real target catalog/schema/render contracts survive; surviving mixed-file tests collect and preserve their unrelated claims.
- **Rollback:** R-CY079: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY079.D1 and CY079.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C055, C057, C058, C067, C087, T002, T010, T019, T071, T082, T083, T084, T085, T086, T089, T092, T099, T105.

Read-only review/preservation IDs: C064, C066. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

- Close this cycle's specific retired exports/imports in shared schemas/interfaces/test_support and mixed tool-input tests at the same boundary; preserve unrelated GateReport/GateViolation workflow contracts.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/services/test_template_graph.py`
- `tests/mcp_server/unit/services/test_template_catalog.py`
- `tests/mcp_server/integration/test_schema_public_v3.py`

Existing affected test/helper sources: T002, T010, T019, T071, T082, T083, T084, T085, T086, T089, T092, T099, T105. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY079, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY080

**Retire parallel component scaffolders**

- **Semantic predecessors:** [CY072](planning-rollout.md#cy072), [CY075](planning-rollout.md#cy075).
- **Shared-file predecessors:** [CY079](planning-rollout.md#cy079).
- **Authority:** [DI-01/02 §9; DI-03 §9; XC-02](design-suite-resolution.md).
- **CY080.D1 — bounded result:** Remove only the separate scaffolding/base.py and components stack, including its hidden routing. Retain services/template_engine.py as the already-migrated generic injected renderer used by the new catalog.
- **Preserved behavior:** Only one generic resolved scaffold authority; current runtime Tool/Service/Resource classes untouched.
- **CY080.D2 — independent evidence:** CY032, CY033, CY034, CY035, CY036, CY037, CY038, CY039, CY040, CY041, CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050/CY053/CY057/CY058 retained behavior evidence plus exact dead import/call closure; source-project defaults not preserved.
- **Rollback:** R-CY080: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY080.D1 and CY080.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C068, C069, C070, C071, C072, C073, C074, C075, C076, C077, C087, T087.

Read-only review/preservation IDs: C066, C088, C089, C090. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

- C087 is a retained generic renderer, not a deletion target. The similarly named scaffolders/BaseScaffolder route was removed in the explicit earlier renderer-retirement cycle.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/templates/test_python_pydantic_dto.py`
- `tests/mcp_server/integration/templates/test_python_adapter.py`
- `tests/mcp_server/integration/test_scaffold_public_v3.py`

Existing affected test/helper sources: T087. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY080, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY081

**Retire legacy validator and validate_template stack**

- **Semantic predecessors:** [CY072](planning-rollout.md#cy072), [CY079](planning-rollout.md#cy079).
- **Shared-file predecessors:** [CY078](planning-rollout.md#cy078), [CY071](planning-rollout.md#cy071), [CY058](planning-artifacts-mutation.md#cy058), [CY055](planning-artifacts-mutation.md#cy055).
- **Authority:** [DI-04 §§3.3–3.4; DI-05 §9](design-mutation-validation.md).
- **CY081.D1 — bounded result:** Remove only the old validator/analyzer/registry/service and validate_template tool after native checks, mutation policy and new public routes are independently proven. Delete the inactive legacy safe_edit_tool.py wrapper in this cycle before removing its ValidationService/ValidationIssue dependencies. Remove obsolete SafeEditOutput.issues/ValidationIssue imports and validation package eager exports together; preserve unrelated models in tool_outputs.py and their required fields.
- **Preserved behavior:** New profile/persistence/location claims and unrelated EnforcementRunner/operation policy behavior.
- **CY081.D2 — independent evidence:** No retained runtime/config imports of legacy validators; check adapter native outcomes and scaffold/edit policy+file effects survive. Collect affected tests before accepting deletion.
- **Rollback:** R-CY081: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY081.D1 and CY081.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C055, C057, C058, C060, C085, C086, C091, C092, C096, C099, C100, C101, C102, C103, C104, C105, C106, C107, S057, T007, T014, T048, T057, T058, T064, T067, T068, T072, T073, T091, T099, T100, T102, T105, T134, T142.

CY081 bounded late-discovery correction (independent QA finding, user-authorized proportional prerequisite): retire only T007 `tests/mcp_server/integration/mcp_server/validation/test_safe_edit_validation_integration.py` when deleting the legacy `tools/safe_edit_tool.py` it imports. Its five cases exercise the obsolete ValidationService/LayeredTemplateValidator/TEMPLATE_METADATA route and provide no unique reliable current behavior proof. The current public edit, check and scaffold V3 tests own enforce/report, no-write/write and preservation claims. Record T007's earlier CY055/CY058 ownership as provenance, not retroactive CY081 scope; do not recreate its template-content assertions. Prove exact import closure and collect-only after removal.

CY081 import/catalog closure (independent QA finding): C106 already owns the active `presentation.yaml` entry; remove only obsolete `validate_template`, whose presence blocks target startup after tool retirement. Add narrow CY081 write episodes for T014 (switch PR-lock test to the current safe-edit class), T072 (remove retired `validate_template` plus five obsolete V2 mechanics rows and four V2-only DTO methods; retain four current green presentation cases, every current tool row and inline-sequence behavior), T105 (retire wholly old analyzer tests), T134 (retire only the old ValidationIssue/SafeEditOutput case), and `tests/mcp_server/integration/test_target_startup.py` (remove only old tool-name expectations). The four previously uncatalogued files `tests/mcp_server/unit/validation/test_validator_registry.py`, `test_validation_service.py`, `test_syntax_validation.py` and `test_markdown_validator.py` are retired only because their old APIs disappear; preserve native Python syntax and Markdown preflight evidence and current V3 catalog/check/edit/scaffold proofs. Preserve all other PR-lock, presentation, structured-output and startup assertions. The historical owner rows remain provenance; these late episodes authorize no broader edits.

Read-only review/preservation IDs: C064. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

- Close this cycle's specific retired exports/imports in shared schemas/interfaces/test_support and mixed tool-input tests at the same boundary; preserve unrelated GateReport/GateViolation workflow contracts.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/adapters/test_python_syntax.py`
- `tests/mcp_server/integration/adapters/test_markdown_preflight.py`
- `tests/mcp_server/integration/test_scaffold_public_v3.py`
- `tests/mcp_server/integration/test_edit_public_v3.py`

Existing affected test/helper sources: T048, T057, T058, T064, T067, T068, T073, T091, T099, T100, T102, T142. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY081, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY082

**Retire project_structure and hidden naming**

- **Semantic predecessors:** [CY081](planning-rollout.md#cy081), [CY080](planning-rollout.md#cy080).
- **Shared-file predecessors:** [CY052](planning-artifacts-mutation.md#cy052), [CY074](planning-rollout.md#cy074), [CY078](planning-rollout.md#cy078).
- **Authority:** [DI-04 §§3.3–3.4; DI-05 §9](design-mutation-validation.md).
- **CY082.D1 — bounded result:** Remove only project_structure schema/readers/directory resolver and hidden naming; migrate each retained operation/parent-policy field and affected test, preserving unrelated PolicyEngine and EnforcementRunner claims.
- **Preserved behavior:** New profile/persistence/location claims and unrelated EnforcementRunner/operation policy behavior.
- **CY082.D2 — independent evidence:** DI-04 field/consumer map complete; obsolete reads/imports absent; location containment/temp/exact-name behavior and unrelated operation-policy cases pass.
- **Rollback:** R-CY082: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY082.D1 and CY082.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C055, C057, C058, C060, C079, C107, S017, S018, S019, S020, S021, S022, S023, T003, T047, T048, T064, T067, T068, T073, T074, T080, T091, T095, T099.

CY082 bounded test-import closure (independent QA finding under the user's proportional-correction authorization): T048 `tests/mcp_server/test_support.py` removes only old project-structure/resolver imports and its exhausted resolver builder while preserving the PolicyEngine helper with current operation/Git config; T064 removes only old loader/schema/fixture/assertion rows; T074 removes only the retired `structure` startup fixture; T091 removes only the old schema import, ConfigLayer field mock and loader-method mock. Their original owner episodes remain provenance. The rollout-configuration integration test mentions project_structure only in comments, so it is not a CY082 behavior or import blocker and is outside this write-set. Retain all unrelated workflow, config, bootstrap and policy claims.

Read-only review/preservation IDs: C064. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

- Close this cycle's specific retired exports/imports in shared schemas/interfaces/test_support and mixed tool-input tests at the same boundary; preserve unrelated GateReport/GateViolation workflow contracts.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/services/test_artifact_target_resolver.py`

Existing affected test/helper sources: S021, S022, S023, T003, T047, T067, T068, T073, T080, T095, T099. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY082, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY083

**Retire generic Pytest runner**

- **Semantic predecessors:** [CY072](planning-rollout.md#cy072).
- **Shared-file predecessors:** [CY082](planning-rollout.md#cy082), [CY081](planning-rollout.md#cy081), [CY073](planning-rollout.md#cy073), [CY060](planning-artifacts-mutation.md#cy060), [CY071](planning-rollout.md#cy071).
- **Authority:** [DI-05 §9; DI-08 §9](design-execution-adapters.md).
- **CY083.D1 — bounded result:** Remove old runner/IPytestRunner/test_tools native command building and obsolete test fake calls.
- **Preserved behavior:** Pytest-native behavior remains CY027, service CY028, public CY060; no numeric/verbose alias.
- **CY083.D2 — independent evidence:** Imports absent, native/test/public evidence retained, xdist stopping tested; no generic Pytest knowledge.
- **Rollback:** R-CY083: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY083.D1 and CY083.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C055, C085, C086, C106, C107, C108, C110, C114, T048, T075, T091, T099, T106, T110, T127, T134, T137, T140.

CY083 bounded DTO/test-fixture import closure (independent QA finding under the user's proportional-correction authorization): C086 removes only the old `TestFailureDTO` and `RunTestsOutput` paired with the retiring `test_tools.py`; the active V3 models in `execution.models` remain. T134 receives a narrow CY083 episode to retire only its old numeric-duration/RunTestsOutput case while preserving unrelated workflow and structured-output assertions. T137 and T140 solely test the removed runner/tool; after both retire, T106 `fake_pytest_runner.py` has no consumers and its type-only import prevents closure, so retire it in CY083. CY105 reviews T106 absence rather than recreating it. No numeric/verbose compatibility alias or replacement fake is added.

CY083 xdist stop-proof amendment (independent QA NOGO on `c8f46c6a6c4355f54146a5e994320a684b495a26`, under the user's proportional-correction authorization): the existing `tests/mcp_server/integration/adapters/test_pytest.py` cancellation test previously used `args=()` and proved only plain Pytest descendant stopping, while its separate `-n 2` test proved normal completion. In that named durable proof file, adapt the existing cancellation test to launch `-n 2`, observe the xdist worker and its child as distinct live PIDs, then cancel and confirm both stopped via OS process handles. This is the only added test-file write in CY083; no new harness, production change or legacy content test is introduced.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

- Remove/migrate final PytestRunner, result, IPytestRunner and old tool imports in T075/T140/T137/T106, including TYPE_CHECKING references. Keep unrelated tool, subprocess-control and interface claims.
- Close this cycle's specific retired exports/imports in shared schemas/interfaces/test_support and mixed tool-input tests at the same boundary; preserve unrelated GateReport/GateViolation workflow contracts.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/fixtures/test_role_double.py`
- `tests/mcp_server/integration/adapters/test_pytest.py`
- `tests/mcp_server/unit/execution/test_test_service.py`
- `tests/mcp_server/integration/test_tests_public_v3.py`

Existing affected test/helper sources: T048, T075, T091, T099, T106, T110, T127, T137, T140. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY083, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY084

**Close QAManager-dependent parser test imports**

- **Semantic predecessors:** [CY072](planning-rollout.md#cy072), [CY083](planning-rollout.md#cy083).
- **Shared-file predecessors:** [CY022](planning-execution.md#cy022), [CY021](planning-execution.md#cy021).
- **Authority:** [DI-05 migration](design-execution-adapters.md), [T111–T140 dispositions](design-integration-review.md).
- **CY084.D1 — bounded result:** Finish migration/retirement of the eight enumerated parser-test sources that still import QAManager; keep parser configuration-only tests for the following parser-authority removal.
- **Preserved behavior:** Durable native findings, explicit scope, truthful operation outcomes and state noninterference; obsolete QAManager private-call/parser/replay expectations retire only after their named successor proof.
- **CY084.D2 — independent evidence:** Named replacement native/consumer/public proofs pass. Collect the changed test sources; their last runtime and type-only QAManager imports/fixtures are gone before manager removal. Retain unrelated public assertions.

CY084 bounded source observation and QA-designated proof correction (2026-09-24): of T116/T119–T125, T116/T120/T121/T122/T124/T125 were already absent at cycle entry; do not recreate them. T119 contains only private-symbol tombstones, and T123 only the obsolete generic text-default DSL plus an unused QAManager fixture; retire both and record import closure separately from native/public proof. The named `tests/mcp_server/integration/adapters/test_pyright.py` proof failed at baseline because it expected the live `[tool.pyright]` duplicate that CY072 intentionally removed. Independent QA identified the stale CY022/CY072 preimage assumption and designated this single additional test-file slice. Confirm the section is absent, remove only the historical duplicate-section before/after rehearsal, and retain native Pyright configuration, adapter-evidence and editor-target assertions. CY022 remains the original owner; no production or live configuration change is authorized here.
- **Rollback:** R-CY084: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY084.D1 and CY084.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: T116, T119, T120, T121, T122, T123, T124, T125.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

- This cycle owns only the named legacy test-source slices and their last dependency removal; it does not introduce a second test harness or implement runtime behavior.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/adapters/test_pyright.py`
- `tests/mcp_server/integration/test_checks_public_v3.py`

Existing affected test/helper sources: T116, T119, T120, T121, T122, T123, T124, T125. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY084, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY085

**Close QAManager-dependent fix and state test imports**

- **Semantic predecessors:** [CY072](planning-rollout.md#cy072), [CY083](planning-rollout.md#cy083).
- **Shared-file predecessors:** [CY061](planning-artifacts-mutation.md#cy061), [CY059](planning-artifacts-mutation.md#cy059).
- **Authority:** [DI-05 migration](design-execution-adapters.md), [T111–T140 dispositions](design-integration-review.md).
- **CY085.D1 — bounded result:** Finish the final manager-import slices in fix propagation, baseline replay, diagnostic paths and summary tests. Preserve their native fix/public response/no-state-touch replacements before QAManager disappears.
- **Preserved behavior:** Durable native findings, explicit scope, truthful operation outcomes and state noninterference; obsolete QAManager private-call/parser/replay expectations retire only after their named successor proof.
- **CY085.D2 — independent evidence:** Named replacement native/consumer/public proofs pass. Collect the changed test sources; their last runtime and type-only QAManager imports/fixtures are gone before manager removal. Retain unrelated public assertions.

CY085 bounded source observation and QA-designated proof correction (2026-09-24): T112 was already absent at cycle entry; do not recreate it. T113 contains obsolete auto-baseline/replay and private QAManager calls; T131 contains old compact-summary/all-skipped/auto/message-sanitization claims; T133 contains blanket compact-path rewriting. Retire these three files only after the named V3 fix/check public proofs cover native mutation and stop, truthful incomplete status/scope/diagnostics, no quality-state writes and safe operation paths. The named `tests/mcp_server/unit/execution/test_fix_service.py` proof failed at baseline because it hardcoded Ruff `0.15.6` while the current host reports `0.14.13`; independent QA designated this one additional test slice. Compare `external_tools` with an independent `python -m ruff --version` observation from the same runtime, retaining native byte-transition, partial-write and stop assertions. The bundled adapter dependency pin and production behavior remain unchanged; CY030 remains the test file's original owner.
- **Rollback:** R-CY085: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY085.D1 and CY085.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: T112, T113, T131, T133.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

- This cycle owns only the named legacy test-source slices and their last dependency removal; it does not introduce a second test harness or implement runtime behavior.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/execution/test_fix_service.py`
- `tests/mcp_server/integration/test_checks_public_v3.py`
- `tests/mcp_server/integration/test_fixes_public_v3.py`

Existing affected test/helper sources: T112, T113, T131, T133. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY085, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY086

**Retire quality orchestration and old check/fix tools**

- **Semantic predecessors:** [CY072](planning-rollout.md#cy072), [CY083](planning-rollout.md#cy083), [CY084](planning-rollout.md#cy084), [CY085](planning-rollout.md#cy085), [CY081](planning-rollout.md#cy081).
- **Shared-file predecessors:** [CY082](planning-rollout.md#cy082), [CY071](planning-rollout.md#cy071), [CY059](planning-artifacts-mutation.md#cy059), [CY061](planning-artifacts-mutation.md#cy061), [CY022](planning-execution.md#cy022).
- **Authority:** [DI-05 §9; XC-02](design-execution-adapters.md).
- **CY086.D1 — bounded result:** Remove old quality tools, QAManager and execution interface once no live consumer remains; preserve check/test/fix role separation and unrelated PR atomicity.
- **Preserved behavior:** Approved Ruff/Mypy/Pyright facts remain in adapters; workflow quality-gate policy remains.
- **CY086.D2 — independent evidence:** Check/fix native and public proofs precede deletion. Collect affected test imports; old names absent from final ToolAssembly; unrelated PR flow and bounded cache facts survive.

CY086 bounded closure and provenance (2026-09-24): R-CY086 starts at `ce3a85c249a5b63b6054fb8b009ce210e1f64ac5`; the cycle-owned changes are the exact committed path diff against that SHA. T115/T117/T143 were already absent. Independent QA mapped additional import-only slices T075/T134/T129, obsolete old-only oracles T107/T139/T141/T132/T149, and two obsolete suites T109/T128. T109 was retired after the surviving checks-config admission test gained one malformed-YAML case; T128 was retired after current V3 selection, process stop and cache proofs. T091 now exercises the real target bootstrap for token-dependent GitHub registration while retaining ToolAssembly and frozen graph contracts. Native Ruff adapter evidence uses the pinned project `.venv` (`ruff 0.15.6`); the MCP test runner's system Python has `ruff 0.14.13` and is not representative for that adapter. Focused closure: 144 startup/config/import/cache tests (`pgmcp://cache/runs/148018b7df8546729befeff83d8257b7`), 53 public check/fix/PR/cache tests (`pgmcp://cache/runs/617126723f084e3eb44619bf29f0d0ec`), 33 pinned-native Ruff tests, 9 serial process-stop tests (`pgmcp://cache/runs/aeb4b4c72f0f46758774655bfe5972c8`), test collection (`pgmcp://cache/runs/54e03d68f7b043d4975f40d6dd9a492d`), and changed-file format/lint/Pyright (`pgmcp://cache/runs/1679f05b4b004da5a676a54752da9d54`). No template content assertions were added. QA also designated T097/T098 autouse-fixture removal because those fixtures patched the deleted `ConfigLoader.load_quality_config`; their 24 preserved server/cycle tests now pass (`pgmcp://cache/runs/d3ad227c649c4055a10eb84996f0dc6a`) with changed-file gates green (`pgmcp://cache/runs/364d2607a1234798924a42e52859279f`). The unrelated rollout-configuration tests passed (10/10) in the pre-fix discovery run. These observations request independent review; they do not declare GO.
- **Rollback:** R-CY086: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY086.D1 and CY086.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C006, C055, C057, C058, C060, C065, C085, C086, C095, C106, C107, C109, T048, T064, T091, T099, T109, T110, T114, T115, T117, T118, T126, T128, T130, T136, T143.

Read-only review/preservation IDs: C005, T131. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

- Close this cycle's specific retired exports/imports in shared schemas/interfaces/test_support and mixed tool-input tests at the same boundary; preserve unrelated GateReport/GateViolation workflow contracts.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/test_checks_public_v3.py`
- `tests/mcp_server/integration/test_fixes_public_v3.py`

Existing affected test/helper sources: T048, T064, T091, T099, T109, T110, T114, T115, T117, T118, T126, T128, T130, T136, T143. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY086, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY087

**Retire generic native-parser DSL**

- **Semantic predecessors:** [CY086](planning-rollout.md#cy086).
- **Shared-file predecessors:** [CY059](planning-artifacts-mutation.md#cy059).
- **Authority:** [DI-05 §9; XC-02](design-execution-adapters.md).
- **CY087.D1 — bounded result:** Delete the now-unreferenced generic violation parser and parser/gate schema fields plus their exact tests; retain native-specific diagnostics in the owning adapters.
- **Preserved behavior:** Approved Ruff/Mypy/Pyright facts remain in adapters; workflow quality-gate policy remains.
- **CY087.D2 — independent evidence:** No active generic regex/field-map/native interpretation authority remains. Each affected native adapter still supplies independently verified diagnostics; unrelated schema fields and cache presence semantics survive.

CY087 bounded closure and provenance (2026-09-24): R-CY087 starts at `0fb1d4c00fed748355d0c033317e1933611a9e83`; the cycle-owned inverse diff is the exact committed path diff against that SHA. C062's remaining quality-gate and parser DTOs and C115's generic regex/field-map parser had no active production caller; both were retired with only their C060/C085 exports. T144/T146/T147/T148 asserted that removed DSL and DTO construction, so they were retired rather than converted to symbol tombstones. T109/T128 were already absent from CY086; T099 retains its current typed-input checks. The post-removal Python reference scan found no old parser/gate names, and full test collection passed (`pgmcp://cache/runs/f7d138de5ab44f5196b7413f2019f857`). Native Ruff diagnostics passed 23/23 in the pinned project `.venv` (`ruff 0.15.6`); Mypy/Pyright, public V3 checks and typed-input tests passed 96/96 (`pgmcp://cache/runs/39af3ce629114c40a9d5f2fcd02cd28f`). Changed export-file format/lint/Pyright passed (`pgmcp://cache/runs/80dac8c12b5a46afbd03f14033f8d212`). These observations request independent review; they do not declare GO.
- **Rollback:** R-CY087: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY087.D1 and CY087.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C055, C057, C058, C060, C062, C085, C086, C115, T099, T109, T128, T144, T146, T147, T148.

Read-only review/preservation IDs: T116, T119, T120, T121, T122, T123, T124, T125. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

- Close this cycle's specific retired exports/imports in shared schemas/interfaces/test_support and mixed tool-input tests at the same boundary; preserve unrelated GateReport/GateViolation workflow contracts.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/adapters/test_ruff_checks.py`
- `tests/mcp_server/integration/adapters/test_mypy.py`
- `tests/mcp_server/integration/adapters/test_pyright.py`

Existing affected test/helper sources: T099, T109, T128, T144, T146, T147, T148. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY087, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY088

**Retire auto replay state**

- **Semantic predecessors:** [CY072](planning-rollout.md#cy072), [CY086](planning-rollout.md#cy086), [CY087](planning-rollout.md#cy087).
- **Shared-file predecessors:** [CY010](planning-execution.md#cy010), [CY066](planning-rollout.md#cy066), [CY068](planning-rollout.md#cy068).
- **Authority:** [Research check-retesting; DI-08 integration rows129/136](design-integration-review.md).
- **CY088.D1 — bounded result:** Remove quality state repository/DTO and only its branch-local registration.
- **Preserved behavior:** PR atomicity, general atomic-write/locking/state and cache FIFO retained; no new result validity store.
- **CY088.D2 — independent evidence:** Public run_checks no-state-touch; independent atomic writer/state/cache owner tests present before deletion; submit_pr cases keep unrelated behavior.

CY088 bounded closure and provenance (2026-09-24): R-CY088 starts at `4dcc5a817e41e067e833e89224d878bf86dea977`; the cycle-owned inverse diff is the exact committed path diff against that SHA. C111/C112 and their auto-state-only T129/T135 tests were retired; C003 lost only the `.pgmcp/quality_state.json` branch-local entry. T108 lost only two obsolete registration assertions; its transaction, rollback, artifact-neutralization and status cases remain. C055/C107/S024/T048/T066/T099/T110 were reviewed for closure and require no edit. Current public `run_checks` still proves that an unrelated pre-existing file at the old path remains byte-identical; QA designated removal of the duplicate sentinel from `test_tests_public_v3.py`, retaining all other test-scope and byte-preservation assertions. No auto-state persistence was reintroduced. Post-removal full test collection passed (`pgmcp://cache/runs/8d7a5f39cbb5435e85686d852d696155`); 170 targeted selection/check/fix/public/PR/atomic/state/cache tests passed (`pgmcp://cache/runs/ce5680393245410b978df6e86e6cab51`), 72 contracts/typed-input/interface/rollout tests passed (`pgmcp://cache/runs/c0a0d0ebeb024f7c854fc3d0f70a96fd`), and the initial changed Python file passed format/lint/Pyright (`pgmcp://cache/runs/a42775e1598744d08e0ffc4f234119c8`). After the QA-designated duplicate-test removal, both public check/test files passed 30/30 (`pgmcp://cache/runs/a8334750a5394983bbabb613b562e540`) and both changed Python files passed format/lint/Pyright (`pgmcp://cache/runs/a5562bed63d7419aa5bb6342642aa634`). These observations request independent review; they do not declare GO.
- **Rollback:** R-CY088: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY088.D1 and CY088.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C003, C055, C107, C111, C112, S024, S031, S032, S033, S035, S036, T048, T066, T099, T108, T110, T129, T135.

Read-only review/preservation IDs: T113. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

- Close this cycle's specific retired exports/imports in shared schemas/interfaces/test_support and mixed tool-input tests at the same boundary; preserve unrelated GateReport/GateViolation workflow contracts.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/execution/test_check_selection.py`
- `tests/mcp_server/unit/execution/test_check_service.py`
- `tests/mcp_server/integration/execution/test_check_profiles.py`
- `tests/mcp_server/unit/execution/test_fix_service.py`
- `tests/mcp_server/integration/test_checks_public_v3.py`
- `tests/mcp_server/integration/test_fixes_public_v3.py`

Existing affected test/helper sources: S032, S035, T048, T066, T099, T108, T110, T129, T135. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY088, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY089

**Scaffold and schema reference migration**

- **Semantic predecessors:** [CY072](planning-rollout.md#cy072), [CY077](planning-rollout.md#cy077), [CY078](planning-rollout.md#cy078), [CY079](planning-rollout.md#cy079), [CY080](planning-rollout.md#cy080), [CY081](planning-rollout.md#cy081), [CY082](planning-rollout.md#cy082).
- **Shared-file predecessors:** None.
- **Authority:** [DI-07 §7.5; DI-03 §9](design-workflow-documentation.md).
- **CY089.D1 — bounded result:** Update canonical scaffold/edit/discovery guidance; retire duplicate inventory/validation references with inbound links.
- **Preserved behavior:** Live schema owns exact fields; refinement, provenance and location explanations remain accurate.
- **CY089.D2 — independent evidence:** DOCFLOW-E04/05; active inbound link scan and public examples match V3; history stays historical.

CY089 bounded closure and provenance (2026-09-24): R-CY089 starts at `b312084d812e96c8b2f33759822560683fd0b9c9`; the cycle-owned inverse diff is the exact committed path diff against that SHA. C035/C043/C053's obsolete duplicate authorities were removed; their active inbound references in C044/C045 were migrated to current schema/usage guidance. Independent QA designated only three C042 navigation-row corrections at this boundary (the two removed pages and the changed provenance-page description); CY093 retains the broader index rewrite. C034/C037/C038/C044–C047/C051/C052 now describe the live package schema, scaffold/edit/discovery, config and navigation contracts. The targeted active-reference scan found no inbound link to the removed pages outside historical issue/archive documents; all local Markdown links in the surviving edited pages resolve. The design-package example was compared with the resolved `design/context.schema.json` required fields. Independent QA identified two in-scope wording corrections: C037 now names the target bootstrap's `template_suite` default, and C052 states the mandatory first-line `pgmcp:v1` record. No artificial tests were added or run for this documentation-only slice. These observations request independent review; they do not declare GO.
- **Rollback:** R-CY089: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY089.D1 and CY089.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C034, C035, C037, C038, C043, C044, C045, C046, C047, C051, C052, C053.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Documentation evidence: compare the exact named sources against their Design dispositions, verify actionable examples/links and actual source-copy direction. No artificial test is required.

Existing affected test/helper sources: None. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY089, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY090

**Execution and evidence references**

- **Semantic predecessors:** [CY072](planning-rollout.md#cy072), [CY083](planning-rollout.md#cy083), [CY086](planning-rollout.md#cy086), [CY087](planning-rollout.md#cy087), [CY088](planning-rollout.md#cy088).
- **Shared-file predecessors:** [CY010](planning-execution.md#cy010), [CY059](planning-artifacts-mutation.md#cy059).
- **Authority:** [DI-07 §§7.4–7.5](design-workflow-documentation.md).
- **CY090.D1 — bounded result:** Migrate check/test/fix/resource standards and usage references. Reconcile the generic cache-window procedure in C126 resource documentation and C050 project reference with the already-live CY011 hint and CY072 installed instructions; this cycle is reference reconciliation, not first discovery delivery.
- **Preserved behavior:** Native settings ownership, role-specific scopes/partial fix behavior and workflow gate evidence policy unchanged except approved deltas.
- **CY090.D2 — independent evidence:** Examples verified against registered schemas; no numbered-gate/quality.yaml authority, no fabricated executable pass.

CY090 bounded closure and provenance (2026-09-24): R-CY090 starts at `4f2e32731946ad25f49d9e127f0fd1f44b3e5296`; the cycle-owned inverse diff is the exact committed path diff against that SHA. The affected reference pages now use the registered V3 check/test/fix schemas, distinguish operational success from native findings, preserve partial-fix/recheck guidance, and point to the packaged cache-window guide only when needed. QA designated removal of C050's obsolete pseudo-workflow examples rather than retaining invalid V2 calls; the remaining skip/force examples now use the current phase contract. QA also identified and closed invalid C049 scaffold pseudo-calls, unsupported `create_issue` parameter rows, and a Unicode issue example that omitted required fields. C113's docstrings no longer advertise the unregistered Python restart-marker helper as an MCP tool; its runtime behavior remains unchanged. C124's standards projection and T151's current policy assertions were reviewed without code changes; T151 passed 2/2 (`pgmcp://cache/runs/1e36302517f9447dbd0a91ae4cc421d1`). C113 format/lint/Pyright passed (`pgmcp://cache/runs/1d0e28aa13d34d848e4d15cf2586a3d1`). Local links in the eight edited reference/manual pages resolve, and the scoped stale-term scan found no active V2 authority or invalid V2 example. The out-of-set manuals index remains CY093-owned. These observations request independent review; they do not declare GO.
- **Rollback:** R-CY090: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY090.D1 and CY090.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C041, C048, C049, C050, C113, C116, C118, C119, C124, C126, T151.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Documentation evidence: compare the exact named sources against their Design dispositions, verify actionable examples/links and actual source-copy direction. No artificial test is required.

Existing affected test/helper sources: T151. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY090, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY091

**Deployment and setup references**

- **Semantic predecessors:** [CY062](planning-rollout.md#cy062), [CY067](planning-rollout.md#cy067), [CY072](planning-rollout.md#cy072).
- **Shared-file predecessors:** None.
- **Authority:** [DI-06 §9; DI-07 §7.5](design-distribution.md).
- **CY091.D1 — bounded result:** First-v3/manual migration, dependency/install/root/config preservation and restart guidance.
- **Preserved behavior:** No automatic external rollout, native install, forced config overwrite or health-first policy.
- **CY091.D2 — independent evidence:** Match real installed/CLI results and owner-action boundaries; active links resolve.
- **Rollback:** R-CY091: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY091.D1 and CY091.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C018, C054, C117, C120, S041.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Documentation evidence: compare the exact named sources against their Design dispositions, verify actionable examples/links and actual source-copy direction. No artificial test is required.

Existing affected test/helper sources: None. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY091, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

### CY091 execution evidence

Pre-cycle commit: `6a2f42d8a9c66cffb3f07f83f5702e88e7758625`. The cycle-owned inverse is the committed diff for `README.md`, `docs/setup/workspace-upgrade.md`, `docs/manuals/github-setup.md`, `docs/setup/dev-isolation.md`, and `docs/reference/release-assets-procedure.md`; the separately tracked `.pgmcp/state.json` carries cycle state. No other dirty or untracked workspace file is part of this recovery set. The current CLI, settings resolver, release manifest, build path, and installed-launch boundary were compared with the instructions. All local links in these five pages resolve. The changes are documentation-only, so no runtime test or quality gate was rerun; earlier runtime evidence remains unchanged. Independent review is requested without a producer GO claim.

## CY092

**Architecture diagrams**

- **Semantic predecessors:** [CY077](planning-rollout.md#cy077), [CY078](planning-rollout.md#cy078), [CY079](planning-rollout.md#cy079), [CY080](planning-rollout.md#cy080), [CY081](planning-rollout.md#cy081), [CY082](planning-rollout.md#cy082), [CY083](planning-rollout.md#cy083), [CY086](planning-rollout.md#cy086), [CY087](planning-rollout.md#cy087), [CY088](planning-rollout.md#cy088).
- **Shared-file predecessors:** None.
- **Authority:** [DI-07 §7.5; XC-01](design-workflow-documentation.md).
- **CY092.D1 — bounded result:** Update six catalogued subsystem/config/tool/naming diagrams to exact responsibility/dependency boundaries.
- **Preserved behavior:** No diagram becomes alternate catalog/schema/policy; unrelated architecture preserved.
- **CY092.D2 — independent evidence:** Diagram-to-public composition/owners crosscheck, local links, no obsolete active registry/parser authority.
- **Rollback:** R-CY092: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY092.D1 and CY092.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C026, C027, C028, C029, C030, C031.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Documentation evidence: compare the exact named sources against their Design dispositions, verify actionable examples/links and actual source-copy direction. No artificial test is required.

Existing affected test/helper sources: None. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY092, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

### CY092 execution evidence

Pre-cycle commit: `69fbdf3f0f4a2fa3c903a325db06ed8328127e6f`. The cycle-owned inverse is the committed diff for the six enumerated diagram paths; `.pgmcp/state.json` records the cycle transition. No other dirty or untracked workspace file is in this recovery set. The diagrams were checked against `mcp_server/bootstrap.py`, the active config/catalog/tool implementations, and the approved suite and workflow design. Their local Markdown links resolve; obsolete registry/parser references occur only as explicit retired-boundary notes. This documentation-only cycle adds no runtime code, tests, or gates. Independent review is requested without a producer GO claim.

## CY093

**Architecture manuals and reference navigation**

- **Semantic predecessors:** [CY068](planning-rollout.md#cy068), [CY089](planning-rollout.md#cy089), [CY090](planning-rollout.md#cy090), [CY091](planning-rollout.md#cy091), [CY092](planning-rollout.md#cy092).
- **Shared-file predecessors:** None.
- **Authority:** [DI-07 §7.5](design-workflow-documentation.md).
- **CY093.D1 — bounded result:** Reconcile bounded architecture/vision/navigation and standards wording.
- **Preserved behavior:** Unrelated manual content and historical migration_v2.0; no universal TDD/phase or complete import-guarantee claims.
- **CY093.D2 — independent evidence:** DOCFLOW-E04/05; active inbound references and preserved-unaffected reasons; navigation identifies one owner.
- **Rollback:** R-CY093: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY093.D1 and CY093.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C001, C002, C032, C033, C036, C039, C040, C042, C125.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Documentation evidence: compare the exact named sources against their Design dispositions, verify actionable examples/links and actual source-copy direction. No artificial test is required.

Existing affected test/helper sources: None. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY093, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

### CY093 execution evidence

Pre-cycle commit: `d8ca47766571cb144dbae0e31a40841554a4a62a`. The cycle-owned inverse is the committed diff for C001, C002, C032, C033, C036, C040, and C042; `.pgmcp/state.json` records the cycle transition. C039 remains unchanged because its historical banner already directs operational readers to current contracts; C125 remains unchanged because its conditional workflow and host-source/direct-copy guidance already matches DI-07. No unrelated dirty or untracked file is part of recovery. The active pages were compared with current bootstrap, tool registration, configuration, and owner references. All local links across the nine catalogued pages resolve. This documentation-only cycle requires no runtime tests or gates. Independent review is requested without a producer GO claim.

## CY094

**Retire legacy Pydantic/class sources**

- **Semantic predecessors:** [CY032](planning-artifacts-mutation.md#cy032), [CY033](planning-artifacts-mutation.md#cy033), [CY034](planning-artifacts-mutation.md#cy034), [CY035](planning-artifacts-mutation.md#cy035), [CY072](planning-rollout.md#cy072), [CY080](planning-rollout.md#cy080).
- **Shared-file predecessors:** None.
- **Authority:** [DI-03 code §9; DI-01/02 §9](design-code-test-artifacts.md).
- **CY094.D1 — bounded result:** Remove only the nine owned old DTO/config/class/protocol template sources. Related obsolete T009/T023 source assertions are owned by CY095 and are retired there, not expanded into this write-set.
- **Preserved behavior:** CY032/CY033/CY034/CY035 semantic contracts and explicit fields/imports/defaults remain.
- **CY094.D2 — independent evidence:** Replacement package evidence plus no active legacy config/render imports; captured Git source rollback.
- **Rollback:** R-CY094: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY094.D1 and CY094.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: A004, A006, A007, A009, A010, A028, A029, A032, A039.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/templates/test_python_pydantic_dto.py`
- `tests/mcp_server/integration/templates/test_python_pydantic_config.py`
- `tests/mcp_server/integration/templates/test_python_class.py`
- `tests/mcp_server/integration/templates/test_python_protocol.py`

Existing affected test/helper sources: None. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY094, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

### CY094 execution evidence

Pre-cycle commit: `03c31da676a1ec446fb68530976ba27804abb5e6`. Before deletion, each of the nine enumerated source paths was resolved under `C:\\temp\\pgmcp` and SHA-256 checked; their exact preimages remain recoverable from that Git commit. The cycle-owned inverse is the committed nine-file deletion diff plus this card clarification; `.pgmcp/state.json` records the transition. No unrelated dirty or untracked file is in the recovery set. A search over active server, test, host-agent, and documentation sources found no production import or current config/render selection of the nine old paths. The four named V3 successor test modules passed together: 20/20, Python 3.13.7 and pytest 9.0.2, cached result `pgmcp://cache/runs/0085441d44fb4b9591452a77bdaa4a10`. T009 and T023 still contain collectable old source-file and metadata/tier assertions; both are explicitly owned for review/removal in CY095. Neither was used as behavioral proof or edited out of scope. Independent review is requested without a producer GO claim.

## CY095

**Retire legacy specialized code/test sources**

- **Semantic predecessors:** [CY036](planning-artifacts-mutation.md#cy036), [CY037](planning-artifacts-mutation.md#cy037), [CY038](planning-artifacts-mutation.md#cy038), [CY039](planning-artifacts-mutation.md#cy039), [CY040](planning-artifacts-mutation.md#cy040), [CY072](planning-rollout.md#cy072), [CY080](planning-rollout.md#cy080).
- **Shared-file predecessors:** None.
- **Authority:** [DI-03 code §9](design-code-test-artifacts.md).
- **CY095.D1 — bounded result:** Remove only old adapter/worker/unit/integration/TS roots/configs and TS pseudo-pattern.
- **Preserved behavior:** Portable behavior and first-class fixture options proved; actual existing production files remain.
- **CY095.D2 — independent evidence:** CY036, CY037, CY038, CY039 evidence and source/fixture request closure, no orphan active imports.
- **Rollback:** R-CY095: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY095.D1 and CY095.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: A001, A018, A019, A021, A023, A024, A031, A042, A043, A045, A079, T009, T023, T024, T025.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/templates/test_python_adapter.py`
- `tests/mcp_server/integration/templates/test_python_worker.py`
- `tests/mcp_server/integration/templates/test_pytest_unit_test.py`
- `tests/mcp_server/integration/templates/test_pytest_integration_test.py`
- `tests/mcp_server/integration/templates/test_typescript_artifact.py`

Existing affected test/helper sources: T009, T023, T024, T025. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY095, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

### CY095 execution evidence

Pre-cycle commit: `4aba405779ffee5848fd92877c40db73d2cb5cf9`. Each of the 15 enumerated source/test paths was resolved under `C:\\temp\\pgmcp` and SHA-256 checked before deletion; its exact preimage remains recoverable from that Git commit. The cycle-owned inverse is the committed deletion diff and `.pgmcp/state.json` transition. T009, T023, T024, and T025 contained only old concrete-root existence, tier-import, metadata, or direct-render claims; none carried a surviving independent behavior assertion. The five named V3 successor test modules passed together: 24/24, Python 3.13.7 and pytest 9.0.2, cached result `pgmcp://cache/runs/314297b9cf44444eb7744e8ba52816ff`. Active server/config/suite/host-agent/test search found no import or selection of these removed paths or test modules. No runtime production code changed; no broader gate was rerun. Independent review is requested without a producer GO claim.

## CY096

**Retire legacy phase-document roots**

- **Semantic predecessors:** [CY042](planning-artifacts-mutation.md#cy042), [CY043](planning-artifacts-mutation.md#cy043), [CY044](planning-artifacts-mutation.md#cy044), [CY045](planning-artifacts-mutation.md#cy045), [CY046](planning-artifacts-mutation.md#cy046), [CY047](planning-artifacts-mutation.md#cy047), [CY048](planning-artifacts-mutation.md#cy048), [CY049](planning-artifacts-mutation.md#cy049), [CY050](planning-artifacts-mutation.md#cy050), [CY051](planning-artifacts-mutation.md#cy051), [CY072](planning-rollout.md#cy072).
- **Shared-file predecessors:** None.
- **Authority:** [DI-03 documents §9](design-document-tracking-artifacts.md).
- **CY096.D1 — bounded result:** Delete only the owned Research/Design/Planning/Validation concrete roots/configs and close source-only T026 plus T045/T046. T011/T027 are mixed, CY097-owned direct-render tests and remain temporary test-only exceptions until their CY097 disposition.
- **Preserved behavior:** Nineteen workflow meanings, original PR defects, structured links/refs/checklists and commit semantics.
- **CY096.D2 — independent evidence:** DOC family evidence and no runtime/catalog or active fixture-selector dependency on the removed roots; identify T011/T027 as temporary legacy test requests, not behavioral proof, and preserve approved phase content.
- **Rollback:** R-CY096: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY096.D1 and CY096.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: A005, A012, A015, A022, A027, A034, A037, A044, T026, T045, T046.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

- Before deleting any listed source, require its named successor evidence and zero remaining runtime/catalog/active fixture-selector imports. Close CY096-owned T026/T045/T046 in this cycle. T011/T027 are the only named temporary test-only direct-render exceptions: they also exercise CY097-owned Architecture/Reference/Generic roots and their mixed assertions are reviewed/adapted or retired in CY097; they are not CY096 behavioral evidence. Preserve unrelated assertions.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/templates/test_research_artifact.py`
- `tests/mcp_server/integration/templates/test_design_artifact.py`
- `tests/mcp_server/integration/templates/test_planning_artifact.py`
- `tests/mcp_server/integration/templates/test_validation_artifact.py`

Existing affected test/helper sources: T026, T045, T046. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY096, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

### CY096 execution evidence

Pre-cycle commit: `1cd49f955c1c22f238cd8e825a446b4a60fb5924`. Each of the eleven enumerated paths was resolved within `C:\\temp\\pgmcp` and SHA-256 checked before deletion; their exact preimages remain recoverable from that Git commit. The cycle-owned inverse is the committed eleven-file deletion plus the scoped D1/D2/prerequisite and T026-ownership clarification. Independent QA identified T026's three obsolete tier-import source assertions; this one-file cleanup moves from CY100 to CY096 without changing public behavior. T026 contained only Research/Planning/Design tier-import source assertions; T045/T046 contained only retired Design source/tier/render claims. The surviving V3 document-family tests own behavior. The four named V3 document-family modules passed together: 17/17, cached result `pgmcp://cache/runs/bd20fba7caf246bfa157834c0943d2b4`. Active source/config/suite/host-agent search found no runtime or catalog selection of removed roots; the only remaining direct render references are T011 and T027, the two explicitly named CY097 test-only exceptions. They were not run as CY096 behavior proof or edited out of scope. No broader suite or gate was rerun. Independent review is requested without a producer GO claim.

## CY097

**Retire legacy explanatory-document roots**

- **Semantic predecessors:** [CY096](planning-rollout.md#cy096).
- **Shared-file predecessors:** [CY048](planning-artifacts-mutation.md#cy048).
- **Authority:** [DI-03 documents §9](design-document-tracking-artifacts.md).
- **CY097.D1 — bounded result:** Delete only old Architecture/Reference/Generic Document concrete roots/configs; preserve their explicitly migrated semantic capacities.
- **Preserved behavior:** Nineteen workflow meanings, original PR defects, structured links/refs/checklists and commit semantics.
- **CY097.D2 — independent evidence:** DOC family evidence and no active legacy render paths; approved phase content not discarded as obsolete prose.
- **Rollback:** R-CY097: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY097.D1 and CY097.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: A002, A008, A014, A025, A030, A036, T011, T027.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

- Before deleting any listed source, require its named successor evidence and zero remaining runtime/template/fixture imports. Tests for the same removed source are adapted or removed in this same cycle; unrelated portions remain.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/templates/test_architecture.py`
- `tests/mcp_server/integration/templates/test_reference.py`
- `tests/mcp_server/integration/templates/test_generic_document.py`

Existing affected test/helper sources: T011, T027. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY097, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

### CY097 execution evidence

Pre-cycle commit: `34eadaca6f6a812f7aed9b0ec53916b07b940188`. All eight enumerated source/test paths were resolved under `C:\\temp\\pgmcp` and SHA-256 checked before deletion; Git preserves their exact preimages. The cycle-owned inverse is the committed eight-file deletion and `.pgmcp/state.json` transition. T011/T027 contained only direct rendering and old source-layout assertions; Research/Planning/Design semantics already had CY096's 17/17 V3 family proof. The three named current Architecture/Reference/Generic Document modules passed together: 12/12, cached result `pgmcp://cache/runs/9959b7b315f445fa9e4e3ee943071084`. Active production, config, suite, host-agent, and test search found no remaining selection of these or CY096's removed document roots and no import of T011/T027. No broader suite or gate was rerun. Independent review is requested without a producer GO claim.

## CY098

**Retire legacy tracking roots**

- **Semantic predecessors:** [CY097](planning-rollout.md#cy097).
- **Shared-file predecessors:** None.
- **Authority:** [DI-03 documents §9](design-document-tracking-artifacts.md).
- **CY098.D1 — bounded result:** Delete only old Issue/PR/Commit roots/configs after body/message contracts and native framing are proven.
- **Preserved behavior:** Nineteen workflow meanings, original PR defects, structured links/refs/checklists and commit semantics.
- **CY098.D2 — independent evidence:** DOC family evidence and no active legacy render paths; approved phase content not discarded as obsolete prose.
- **Rollback:** R-CY098: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY098.D1 and CY098.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: A003, A011, A013, A026, A033, A035.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

- Before deleting any listed source, require its named successor evidence and zero remaining runtime/template/fixture imports. Tests for the same removed source are adapted or removed in this same cycle; unrelated portions remain.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/templates/test_issue.py`
- `tests/mcp_server/integration/templates/test_pr.py`
- `tests/mcp_server/integration/templates/test_commit_artifact.py`

Existing affected test/helper sources: None. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY098, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

### CY098 execution evidence

Pre-cycle commit: `ef13e9de7d3473a59e9b731b1a91f66ae0696020`. The six enumerated legacy Issue/PR/Commit roots/configs were resolved under `C:\\temp\\pgmcp` and SHA-256 checked before deletion; Git retains their exact preimages. The cycle-owned inverse is the committed six-file deletion and `.pgmcp/state.json` transition. No test or production source in the scoped active search selected these paths. The current Issue, PR, and Commit package tests passed together: 12/12, cached result `pgmcp://cache/runs/7894070454014430a9f56e9344c15d57`; they exercise body/message semantics and native framing. A post-deletion active source/config/suite/host-agent scan found no old-root selector or import. No broader suite or gate was rerun. Independent review is requested without a producer GO claim.

## CY099

**Retire portable Python/test macro sources**

- **Semantic predecessors:** [CY031](planning-artifacts-mutation.md#cy031), [CY041](planning-artifacts-mutation.md#cy041), [CY094](planning-rollout.md#cy094), [CY095](planning-rollout.md#cy095), [CY096](planning-rollout.md#cy096), [CY097](planning-rollout.md#cy097), [CY098](planning-rollout.md#cy098).
- **Shared-file predecessors:** [CY039](planning-artifacts-mutation.md#cy039), [CY037](planning-artifacts-mutation.md#cy037), [CY033](planning-artifacts-mutation.md#cy033).
- **Authority:** [DI-01/02 §9; DI-03 code/doc §9](design-code-test-artifacts.md).
- **CY099.D1 — bounded result:** Remove only legacy Python/testing macros after every admitted or selected concrete Python consumer has migrated. The rejected, unregistered CY101-owned Resource/Service/Tool roots are not active consumers.
- **Preserved behavior:** Shared syntax/link/fixture/omission claims already in public family coverage.
- **CY099.D2 — independent evidence:** Graph reachability/import scan proves no runtime, catalog, or active fixture selector reaches removed macros, plus affected family proof. The only temporary source-only imports are A016 resource→A071 logging, A017 service_command→A066 async and A071 logging, and A020 tool→A071 logging; CY101 closes those rejected roots. Their legacy renderability is not claimed after CY099.
- **Rollback:** R-CY099: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY099.D1 and CY099.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: A066, A071, A072, A073, A074, A076, T031, T036, T037, T038, T039, T041.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

- Before deleting any listed source, require its named successor evidence and zero reachable runtime/catalog/active fixture-selector imports. The only temporary source-only edges are A016/A017/A020 to A066/A071 as identified in CY099.D2; these rejected, unregistered CY101-owned roots are not active behavior, and CY101 closes them. Tests for the removed macros are adapted or removed in this cycle; unrelated portions remain.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/templates/test_python_pydantic_dto.py`
- `tests/mcp_server/integration/templates/test_python_pydantic_config.py`
- `tests/mcp_server/integration/templates/test_python_class.py`
- `tests/mcp_server/integration/templates/test_python_protocol.py`
- `tests/mcp_server/integration/templates/test_python_adapter.py`
- `tests/mcp_server/integration/templates/test_python_worker.py`
- `tests/mcp_server/integration/templates/test_pytest_unit_test.py`
- `tests/mcp_server/integration/templates/test_pytest_integration_test.py`

Existing affected test/helper sources: T031, T036, T037, T038, T039, T041. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY099, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

### CY099 execution evidence

Pre-cycle commit: `b8d26fee1aff7bfed92470ea401005e73e1265af`. All twelve enumerated macro/test paths were resolved within `C:\\temp\\pgmcp` and SHA-256 checked before deletion; Git retains their exact preimages. The cycle-owned inverse is the committed twelve-file deletion plus the QA-advised reachability clarification. The six retired tests asserted old macro source/Jinja details; current package behavior is owned by the eight named V3 modules, which passed together: 40/40, cached result `pgmcp://cache/runs/a2d565dd285f43b394e6e35b314d0491`. A post-deletion active source/config/suite/test/host-agent search found no reachable macro selector. The only surviving source-only imports are exactly A016 resource→A071 logging, A017 service_command→A066 async and A071 logging, and A020 tool→A071 logging. These excluded, unregistered legacy roots are scheduled for deletion in CY101 and cannot be rendered after this cycle; no active behavior or legacy renderability is claimed. No broader suite or gate was rerun. Independent review is requested without a producer GO claim.

## CY100

**Retire document macro sources**

- **Semantic predecessors:** [CY099](planning-rollout.md#cy099).
- **Shared-file predecessors:** [CY041](planning-artifacts-mutation.md#cy041), [CY048](planning-artifacts-mutation.md#cy048).
- **Authority:** [DI-01/02 §9; DI-03 code/doc §9](design-code-test-artifacts.md).
- **CY100.D1 — bounded result:** Remove only legacy Markdown shared patterns and their source-topology tests after all document/tracking roots migrate.
- **Preserved behavior:** Shared syntax/link/fixture/omission claims already in public family coverage.
- **CY100.D2 — independent evidence:** Graph reachability/import scan plus affected family proof; remove direct macro tests only after named successor coverage.
- **Rollback:** R-CY100: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY100.D1 and CY100.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: A058, A059, A060, A061, A062, A063, A064, T029, T055.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

- Before deleting any listed source, require its named successor evidence and zero remaining runtime/template/fixture imports. Tests for the same removed source are adapted or removed in this same cycle; unrelated portions remain.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/templates/test_shared_documents.py`
- `tests/mcp_server/integration/templates/test_research_artifact.py`
- `tests/mcp_server/integration/templates/test_design_artifact.py`
- `tests/mcp_server/integration/templates/test_planning_artifact.py`
- `tests/mcp_server/integration/templates/test_validation_artifact.py`
- `tests/mcp_server/integration/templates/test_architecture.py`
- `tests/mcp_server/integration/templates/test_reference.py`
- `tests/mcp_server/integration/templates/test_generic_document.py`
- `tests/mcp_server/integration/templates/test_issue.py`
- `tests/mcp_server/integration/templates/test_pr.py`
- `tests/mcp_server/integration/templates/test_commit_artifact.py`

Existing affected test/helper sources: T029, T055. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY100, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

### CY100 execution evidence

Pre-cycle commit: `b1427e69f12b84922d627f6989a18e8aeb34c699`. The seven Markdown macro paths and two test paths were resolved under `C:\\temp\\pgmcp` and SHA-256 checked before deletion; Git preserves exact preimages. The cycle-owned inverse is the committed nine-file deletion and `.pgmcp/state.json` transition. T029's eighth A057 assertion was only file-existence inventory and A057 remains CY103-owned; T055 asserted the old A051 tier-two link layout and A051 remains CY104-owned. Neither assertion is durable behavior. The current shared-document module passed 5/5 (`pgmcp://cache/runs/eaddfda26c3a4e509a61fe29b4eb9f5e`). Fresh unaffected V3 document-family evidence from CY096 17/17, CY097 12/12, and CY098 12/12 covers the other ten named successor modules; only retired source/test paths changed since those runs. Active source/config/suite/host-agent/template graph search found no remaining imports of the seven deleted macros. No broader suite or gate was rerun. Independent review is requested without a producer GO claim.

## CY101

**Remove rejected Resource/Service/Tool artifact sources**

- **Semantic predecessors:** [CY072](planning-rollout.md#cy072), [CY080](planning-rollout.md#cy080), [CY094](planning-rollout.md#cy094), [CY095](planning-rollout.md#cy095), [CY096](planning-rollout.md#cy096), [CY097](planning-rollout.md#cy097), [CY098](planning-rollout.md#cy098).
- **Shared-file predecessors:** None.
- **Authority:** [Research F-14/F-14A/F-14B/deferred YAML; DI-03 §9](design-integration-review.md).
- **CY101.D1 — bounded result:** Delete only rejected Resource/Service/Tool concrete roots/configs; no runtime class or generated-source deletion.
- **Preserved behavior:** No retained generated/runtime classes deleted; future YAML recovery trace records exact historical source/removal commit.
- **CY101.D2 — independent evidence:** Approved exclusions plus absence from admitted catalog/registration; retained plain class and specialized artifact behavior remains; existing production tools/services/resources untouched.
- **Rollback:** R-CY101: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY101.D1 and CY101.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: A016, A017, A020, A038, A040, A041.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

- Before deleting any listed source, require its named successor evidence and zero remaining runtime/template/fixture imports. Tests for the same removed source are adapted or removed in this same cycle; unrelated portions remain.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/test_schema_public_v3.py`
- `tests/mcp_server/integration/test_scaffold_public_v3.py`

Existing affected test/helper sources: None. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY101, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

### CY101 execution evidence

Pre-cycle commit: `df2fc1fdadd4e40e82523cd603afde32310f9fed`; removal commit: `1811e99f7410f4af79b9979005ccf3d2f70b3525`. The six exact rejected Resource/Service/Tool template and YAML paths were resolved under `C:\\temp\\pgmcp` and SHA-256 checked before deletion; the pre-cycle Git commit preserves their source for targeted recovery and future provenance. The cycle-owned inverse is that six-file deletion plus `.pgmcp/state.json`. No production tool, service, resource class, generated source, or admitted template package changed. The named V3 public schema/scaffold modules passed 16/16 (`pgmcp://cache/runs/51e02ab514dd4943859bd1f5fdaa7f93`); a single existing catalog admission test passed 1/1, nine deselected (`pgmcp://cache/runs/10d5e43d97404cda9e2b74a8173aac70`). Active source/config/suite/test/host-agent search found no remaining old source or macro selector, closing CY099's temporary source-only imports. The separate future YAML recovery trace is owned by CY103; its historical-source and removal-commit facts must be recorded there, not by widening this six-path deletion. No broader suite or gate was rerun. Independent review is requested without a producer GO claim.

## CY102

**Remove source-project specialization patterns**

- **Semantic predecessors:** [CY101](planning-rollout.md#cy101).
- **Shared-file predecessors:** None.
- **Authority:** [Research F-14/F-14A/F-14B/deferred YAML; DI-03 §9](design-integration-review.md).
- **CY102.D1 — bounded result:** Delete exactly the six source-project patterns and their tests after all legacy callers are gone.
- **Preserved behavior:** No retained generated/runtime classes deleted; future YAML recovery trace records exact historical source/removal commit.
- **CY102.D2 — independent evidence:** CODE-E06/10 portable actual-package evidence and zero remaining pattern imports; no lost portable logging/explicit-body behavior.
- **Rollback:** R-CY102: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY102.D1 and CY102.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: A067, A068, A069, A070, A077, A078, T032, T033, T034, T035, T042, T043.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

- Before deleting any listed source, require its named successor evidence and zero remaining runtime/template/fixture imports. Tests for the same removed source are adapted or removed in this same cycle; unrelated portions remain.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/templates/test_python_worker.py`
- `tests/mcp_server/integration/templates/test_pytest_unit_test.py`
- `tests/mcp_server/integration/templates/test_pytest_integration_test.py`

Existing affected test/helper sources: T032, T033, T034, T035, T042, T043. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY102, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

### CY102 execution evidence

Pre-cycle commit: `cee6387d79e9848678e489cbbee43369a5214191`. Each of the twelve enumerated source/test paths was resolved under `C:\\temp\\pgmcp` and SHA-256 checked before deletion; Git preserves exact preimages. The cycle-owned inverse is the committed twelve-file deletion and `.pgmcp/state.json` transition. The six old tests asserted source-project-specific Jinja macros (DI, exception, lifecycle, log enricher, translator, automatic typed ID); no runtime or current package imports them. The three named V3 worker/unit/integration modules passed together: 15/15, cached result `pgmcp://cache/runs/31c1223a0d07400c9dbd58d55bf88ecb`. Fresh unaffected CY099 DTO/config/adapter-family evidence covers explicitly supplied defaults and logging; no rejected project defaults are reintroduced. Active source/config/suite/test/host-agent/template graph search found no remaining import of the six removed macros. No broader suite or gate was rerun. Independent review is requested without a producer GO claim.

## CY103

**Remove unreachable YAML and test seeds and agent hints**

- **Semantic predecessors:** [CY102](planning-rollout.md#cy102).
- **Shared-file predecessors:** [CY039](planning-artifacts-mutation.md#cy039).
- **Authority:** [Research F-14/F-14A/F-14B/deferred YAML; DI-03 §9](design-integration-review.md).
- **CY103.D1 — bounded result:** Delete the explicitly unreachable YAML bases, empty test seeds and agent-hint pattern; record exact Git recovery trace for deferred YAML only. T054/T056 retain only temporary test-only references to A048/A054 until their CY104-owned adaptation or removal; their unrelated assertions remain in CY104.
- **Preserved behavior:** No retained generated/runtime classes deleted; future YAML recovery trace records exact historical source/removal commit.
- **CY103.D2 — independent evidence:** Approved no-retained-behavior dispositions, zero active runtime/catalog/fixture selections or imports, CODE-E07 fixture capacity retained and exact source SHA/path recovery trace; no new deferred feature implementation. T054/T056 are the only temporary source-reading test exceptions and provide no CY103 behavior evidence.
- **Rollback:** R-CY103: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY103.D1 and CY103.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: A048, A054, A057, A065, A075, S048, T030, T040.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

- Before deleting any listed source, require its named successor evidence and zero remaining active runtime/template/catalog/fixture selections or imports. T054/T056 are the only temporary test-only source references to A048/A054; CY104 closes them while preserving unrelated assertions. Tests for the other removed sources are adapted or removed in this same cycle.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/services/test_template_catalog.py`
- `tests/mcp_server/integration/test_schema_public_v3.py`

Existing affected test/helper sources: T030, T040. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY103, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

### CY103 execution evidence

Pre-cycle commit: `4ba22137757400d975d7ab8178c508f58999fb67`; removal commit: `d6602c5e92b8bbe235d9f453747a0ec8e6b62a4d`. Seven exact source/test paths were resolved within `C:\\temp\\pgmcp`, SHA-256 checked, then removed; the pre-cycle Git commit preserves their preimages. The cycle-owned inverse is that seven-file deletion plus the CY103 plan amendment and `.pgmcp/state.json` transition. The two deferred YAML files have exact path/hash and source/removal-commit recovery records in `deferred-work.md`; no YAML feature was implemented. Active runtime, catalog, template and fixture-selection search found no reference to the five removed source files. T054 and T056 are the only temporary source-reading test exceptions for A048/A054 and are CY104-owned; they are not CY103 behavior evidence.

The named current catalog/schema modules passed 45/45 (`pgmcp://cache/runs/bf690c3354c94bb0b0561caeb2270900`). Existing V3 unit/integration generation modules passed 10/10 (`pgmcp://cache/runs/ee20b3b2eecc4c07b963bf9c66f1d17d`) for CODE-E07 fixture scope, autouse and explicit content. T030/T040 tested only removed macro source and supply no executable evidence. No broader suite or gate was rerun. Independent review is requested without a producer GO claim.

## CY104

**Retire exhausted tier bases**

- **Semantic predecessors:** [CY100](planning-rollout.md#cy100), [CY103](planning-rollout.md#cy103).
- **Shared-file predecessors:** [CY048](planning-artifacts-mutation.md#cy048), [CY047](planning-artifacts-mutation.md#cy047).
- **Authority:** [DI-01/02 §9; DI-03 code/doc §9](design-code-test-artifacts.md).
- **CY104.D1 — bounded result:** Remove exact legacy tier0/tier1/tier2 portable bases after all retained and rejected old roots are gone; keep new shared generation sources.
- **Preserved behavior:** Shared syntax/link/fixture/omission claims already in public family coverage.
- **CY104.D2 — independent evidence:** Graph reachability/import scan plus affected family proof; remove direct macro tests only after named successor coverage.
- **Rollback:** R-CY104: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY104.D1 and CY104.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: A046, A047, A049, A050, A051, A052, A053, A055, A056, T028, T053, T054, T056.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

- Before deleting any listed source, require its named successor evidence and zero remaining runtime/template/fixture imports. Tests for the same removed source are adapted or removed in this same cycle; unrelated portions remain.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/services/test_template_catalog.py`
- `tests/mcp_server/integration/templates/test_shared_python.py`
- `tests/mcp_server/integration/templates/test_shared_documents.py`

Existing affected test/helper sources: T028, T053, T054, T056. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY104, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

### CY104 execution evidence

Pre-cycle commit: `7a0b94b01aeb051afecf6e77a898714309255fea`. Nine exact legacy tier-base paths and four source-bound test paths were resolved within `C:\\temp\\pgmcp`, SHA-256 checked and removed; Git preserves their preimages. The cycle-owned inverse is these thirteen deletions and the `.pgmcp/state.json` transition. T028/T053/T054/T056 contained only direct old-tier rendering, inheritance, metadata, block-token or deferred-YAML assertions. Their concrete Python, TypeScript, document, link, omission and fixture behaviors already belong to current V3 family tests; no unrelated workflow assertions were removed. The temporary CY103 T054/T056 YAML references are closed. Search across active `mcp_server`, template and test sources found no remaining import, render or source read of the removed tier files.

The three named current catalog/shared-Python/shared-document proof modules passed 53/53 after deletion (`pgmcp://cache/runs/12cc2f4396b541bc851b043f63038fdd`); the pre-deletion shared-family baseline passed 14/14 (`pgmcp://cache/runs/9aba887f95bf4beeb89c8f9c3db6a50f`). No full suite or branch-wide gate was run. Independent review is requested without a producer GO claim.

## CY105

**Retire exhausted legacy test harness**

- **Semantic predecessors:** [CY077](planning-rollout.md#cy077), [CY078](planning-rollout.md#cy078), [CY079](planning-rollout.md#cy079), [CY080](planning-rollout.md#cy080), [CY081](planning-rollout.md#cy081), [CY082](planning-rollout.md#cy082), [CY083](planning-rollout.md#cy083), [CY086](planning-rollout.md#cy086), [CY087](planning-rollout.md#cy087), [CY088](planning-rollout.md#cy088), [CY094](planning-rollout.md#cy094), [CY095](planning-rollout.md#cy095), [CY096](planning-rollout.md#cy096), [CY097](planning-rollout.md#cy097), [CY098](planning-rollout.md#cy098), [CY099](planning-rollout.md#cy099), [CY100](planning-rollout.md#cy100), [CY104](planning-rollout.md#cy104), [CY101](planning-rollout.md#cy101), [CY102](planning-rollout.md#cy102), [CY103](planning-rollout.md#cy103).
- **Shared-file predecessors:** [CY073](planning-rollout.md#cy073), [CY071](planning-rollout.md#cy071), [CY072](planning-rollout.md#cy072).
- **Authority:** [DI-08 §§7.3,9–10](design-test-architecture.md).
- **CY105.D1 — bounded result:** Remove only the remaining exhausted legacy test-helper files/functions and obsolete plugin registration left after the earlier explicitly bounded import migrations; preserve the retained narrow support and unrelated workflow fixtures. Point S012's test-session template root at the active V3 suite and adapt only the QA-designated SDK stdio-handshake test in `test_tool_attachment_transport.py` to an isolated V3 workspace.
- **Preserved behavior:** Unrelated workflow plugin, GitHub mocking, server/cycle/PR behavior, cache/atomic helpers and scoped env fixtures.
- **CY105.D2 — independent evidence:** TEST-E07/08: fixture/import/plugin request closure plus affected public server/workflow/PR tests and the retained real MCP-SDK stdio handshake; no global test cleanup.
- **Rollback:** R-CY105: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY105.D1 and CY105.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Readback prerequisite supplement: [R001–R008](planning-path-ownership.md#readback-prerequisite-supplement). Remove only residual exhausted helper acquisition in R004/R005/R006 after the earlier root/transport migrations. Preserve direct project lifecycle/readback assertions; no late bootstrap-root or transport migration belongs here. D1/D2 and this cycle's R-CY105, preserved behavior and independent stop/go apply to these exact additional seams.

Existing source IDs: S012, S013, S016, T004, T014, T048, T074, T095, T097, T098, T106, R004, R005, R006.

CY105 QA-designated bounded test revisit: `tests/mcp_server/integration/test_tool_attachment_transport.py`, only the legacy-named stdio handshake test. Its legacy-only template copy sees degraded startup. Preserve its real `stdio_client`/`ClientSession` initialize and list-tools claim against a fresh isolated V3 workspace with copied current config/template suite/version and matching `installation.json`, then launch with explicit workspace/config/template environment roots. This reuses the existing readback fixture pattern; public `--init` remains proved separately by the installed startup tests because the source checkout has no bundled `mcp_server/assets`. Do not change its attachment tests or production transport. This is the sole additional path and closes the named CY105 proof; S012 changes only its obsolete template-root value.

Read-only review/preservation IDs: S014, S015, R002. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

- The old artifact-manager/renderer/validator helper imports were closed before their first production removal. This final cycle cannot defer any earlier import or behavioral migration.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/tools/test_project_tools.py`
- `tests/mcp_server/unit/managers/test_project_manager.py`
- `tests/mcp_server/integration/test_project_plan_readback.py`
- `tests/mcp_server/integration/test_tool_attachment_transport.py`
- `tests/mcp_server/unit/decorators/test_pipeline_decorators.py`
- `tests/mcp_server/integration/test_pipeline_e2e.py`
- `tests/mcp_server/unit/test_presenter.py`
- `tests/mcp_server/integration/test_scaffold_public_v3.py`
- `tests/mcp_server/integration/test_tests_public_v3.py`

Existing affected test/helper sources: S012, S013, S016, T004, T014, T048, T074, T095, T097, T098, T106. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY105, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

### CY105 execution evidence

Pre-cycle commit: `8a9005014fe8b8f4c9d27cf8874d1033bb877131`. The cycle-owned inverse is the exact T048 unused-function removal, S012 test-session template-root correction, one QA-designated transport test fixture adaptation, two planning provenance edits and the `.pgmcp/state.json` transition. T004 and T106 were already absent; import/plugin search found no remaining callers. S012 registers only the active workflow and suite-root fixtures; S013/S016 and T014/T074/T095/T097/T098 remain unchanged with active claims. R004/R005/R006 still call the retained `make_project_manager` helper, so none was removed. T048's `get_template_root()` had zero Python callers and was the sole demonstrably exhausted surviving helper.

The first nine-module run had 132 passed and four startup failures (`pgmcp://cache/runs/d855b2ffc2ef41799df18be6f6e109a8`): S012 pointed at retired `.pgmcp/templates`, and the old SDK-handshake fixture copied only legacy assets. After the bounded corrections, the seven unaffected named modules passed 129/129 (`pgmcp://cache/runs/6379d9a9011848b1a39a51c64fc64a2f`), pipeline passed 3/3 (`pgmcp://cache/runs/9f70310f56294869b0a170b8818755f6`), and the complete real MCP-SDK transport module passed 4/4 (`pgmcp://cache/runs/392e07cb7dfa496b88e5b0726e3a71eb`). Settings and suite-root tests passed 30/30 (`pgmcp://cache/runs/9846a27c61774100b7fc7f55835af235`). Thus all nine named CY105 modules have current passing evidence without a broad suite. File format, lint and Pyright checks passed (`pgmcp://cache/runs/37cc671f7cfe4e36bd06421179422787`). Mypy reported 14 errors (`pgmcp://cache/runs/f6c97540d26144909958563f67cea4ab`), all in unchanged lines of the three files (12 T048, one S012, one transport); it remains a failed pre-existing gate and is not claimed as passing. No production file or retained workflow/PR assertion changed. Independent review is requested without a producer GO claim.

## Validation fix-cycle amendment — 2026-09-26

The owner authorized these bounded corrections after validation of CY001–CY105. They preserve the approved Research and Design strategy. The diagnostic inventory and deferred adapter work remain in [validation.md](validation.md); only the five cards below are active issue-460 implementation scope. Each card inherits hub V1–V6, including the exact pre-cycle SHA, scoped inverse diff, focused governed-tool evidence, and independent QA review. The serial order is CY106 → CY107 → CY108 → CY109 → CY110. Complete parallel suite and branch/configured gates remain Validation obligations after CY110. Stop and amend Planning if a finding needs a path or boundary outside the listed write-set.

## CY106

**Restore startup audit and satisfy production typing**

- **Predecessor:** CY105 and independent approval of this Planning amendment.
- **Shared-file predecessors:** No overlapping new amendment-cycle writer; previous production and logging-test writes are covered by the completed CY001–CY105 chain.
- **Authority:** Approved Research F-20/DI-08, existing audit behavior, and the binding typing playbook. No adapter contract or audit schema change.
- **CY106.D1 — bounded result:** Restore the configured audit startup event lost during the V3 cut-over and resolve the seven observed configured production Mypy diagnostics. Exact production write-set: `mcp_server/bootstrap.py`, `mcp_server/server.py`, `mcp_server/core/interfaces/tool_input_contract.py`, `mcp_server/config/validator.py`, `mcp_server/core/decorators/input_validation_decorator.py`, and `mcp_server/core/logging.py`. Exact regression-test write-set: `tests/mcp_server/unit/core/test_logging.py` and `tests/mcp_server/integration/mcp_server/test_server_lifecycle.py`, only for observable repeated-initialization evidence. The logging facility owns and closes only its own handlers when configuration changes or bootstrap repeats; non-owned handlers remain untouched.
- **Preserve/exclude:** Preserve the active startup lock duration, audit payload/level contract, public tool input schema, validator behavior, and dependency injection. A later bootstrap with another audit path or no audit path must not write to an earlier destination; identical reconfiguration must not duplicate output. Non-owned logger handlers remain active. No generic runner or adapter changes.
- **CY106.D2 — evidence:** Both existing startup audit lifecycle cases and a durable observable repeated-bootstrap/reconfiguration regression pass; configured production Mypy passes; affected startup, input-validation, schema and logging tests plus exact-file gates on all six production paths and two test paths pass. Cover same-path, changed-path and disabled-audit follow-up configurations; prove old owned handlers are closed and non-owned handlers are preserved. Record native versions and full cache resources.
- **Rollback:** R-CY106, the scoped inverse of the six production and two test paths plus cycle state only; retain the already-committed first repair as an auditable intermediate state.
- **Stop/go:** Stop on changed audit semantics, non-owned handler removal, stale/duplicate audit output, new schema/adapter behavior, out-of-set writes, or failed D2. Independent QA decides progression.

### CY106 execution evidence

R-CY106 begins at commit `e65b1ebc0f5c1ba2938077c72ad74bbbd7b0def9`. The first committed repair changed five planned production files; the QA-amended continuation adds only `mcp_server/core/logging.py` and the two existing tests. The complete cycle-owned inverse is those eight code/test paths plus cycle state, with the evidence paragraphs removable separately. No unrelated tracked file was dirty before the cycle; the pre-existing untracked installation, lock and backup files were left untouched.

D1: The existing audit tests provided a genuine RED baseline. An initial concurrent tool invocation hit the active startup lock (`pgmcp://cache/runs/01289052653d4de9a1097d0ee9295fe3`); the serial retry reached both assertions and failed because no audit log was created (`pgmcp://cache/runs/3aa3331270ee45b4a7d48c07f2ca43a2`). The configured Mypy baseline reported exactly seven errors across the five write-set files (`pgmcp://cache/runs/cbc959e2e80d4adb9ececeb6d3b44a16`). The repair invokes the existing configured logging facility during target bootstrap, restores the startup lifecycle event, imports ContentInputPreparer from its defining module, exposes the concrete shared response cache only at the composition graph, narrows the known immutable object schema into a native mapping, and casts the validated health tool only at its dynamic decorator boundary. Public schemas, audit message/level, startup lock, cache consumer interface widths and adapter contracts are unchanged.

D2: Both audit lifecycle tests pass (`pgmcp://cache/runs/d746579e2d8c4a1ea3dd4183d8d84bfd`); 25 prepared-input/schema/decorator/startup tests pass (`pgmcp://cache/runs/934409dc94b3409694da29c92f83cb8d`); 19 logging/server/boundary tests pass (`pgmcp://cache/runs/a4c06dd17bd04812b27dfa1a02cb19b2`). All four configured exact-file gates pass on the five production paths: Ruff format/lint 0.15.6, Mypy 1.19.1 and Pyright 1.1.408 (`pgmcp://cache/runs/8e92a5eb18514adab66285899a2b952e`). Pytest 9.0.2 used `scope=targets`, `python_tests`, `args={python_tests:[-n,0]}` for focused evidence; parallel safety is CY107, and the complete parallel suite remains Validation. The diff contains no added test, ignored type error, adapter change or out-of-set production edit. Independent implementation-cycle review is requested without a producer GO claim.

The independent CY106 review of commit `894bf7f3864a93091b17b286b9eef4562d4c2ea0` returned NOGO: repeated bootstrap appends persistent owned handlers to the process logger, duplicates same-path output and leaks prior audit destinations across changed/disabled configurations. The preceding green receipts remain evidence for their selected cases only and do not prove the amended D2. The owner-authorized correction reopens Planning for the exact `core/logging.py` and two-test write-set above; implementation must add observable reconfiguration proof and obtain a fresh independent CY106 verdict before CY107.

Amended CY106 RED/GREEN: the two new observable regression cases failed against the committed first repair because the first audit file received two events after a second setup/bootstrap (`pgmcp://cache/runs/2566da49f79746f6b23284936666cccb`, Pytest 9.0.2). The RED-only tests were committed as `0b0b6a2ab1ba923d900ad546ffbfd2d4baee6b8c`. The logging facility now marks its own stderr/file handlers by dedicated types, removes and closes only those handlers on reconfiguration, then installs the currently configured destinations. The same-path, changed-path and disabled-audit observations pass; old file handles close and a non-owned handler remains attached (`pgmcp://cache/runs/ac5281ffb0e147be8aa94adefd20eb5a`). After the final logging change, all 46 focused audit, logging, prepared-input, schema, decorator, startup and server cases pass serially (`pgmcp://cache/runs/089ab3ae58064675b9a1236c140aff51`). Ruff 0.15.6 format/lint, Mypy 1.19.1 and Pyright 1.1.408 pass on all six production and two test paths (`pgmcp://cache/runs/735f337ad7ea4cefabc4a6dc1405f5c7`); configured production Mypy also passes across 184 sources (`pgmcp://cache/runs/b914277f20014c10b16260b23d967fc0`). Parallel workspace isolation and the full suite remain CY107/Validation obligations. A fresh independent CY106 implementation review is requested without a producer GO claim.

## CY107

**Make server tests safe for parallel workers**

- **Predecessor:** CY106; test-workspace isolation follows DI-08.
- **Shared-file predecessors:** CY105 for retained test support and server harness; CY106 for `test_server_lifecycle.py`; no concurrent amendment-cycle writer.
- **Authority:** [DI-08](design-test-architecture.md), especially isolated roots and retained real proxy/stdio observations.
- **CY107.D1 — bounded result:** Replace shared-repository bootstrap only in `tests/mcp_server/unit/test_server.py`, `tests/mcp_server/integration/test_pipeline_e2e.py`, `tests/mcp_server/integration/test_target_startup.py`, `tests/mcp_server/integration/test_v3_cutover.py`, `tests/mcp_server/integration/mcp_server/test_server_tool_registration.py`, `tests/mcp_server/integration/mcp_server/test_server_lifecycle.py`, and `tests/mcp_server/unit/server/test_validate_tool_arguments.py`. Revisit `tests/mcp_server/test_support.py` and `tests/mcp_server/integration/mcp_server/conftest.py` only if shared isolated-root support is necessary. In `tests/mcp_server/unit/test_pytest_config.py`, retire only the obsolete `test_qa.py` path assertion; preserve current config-selection proof.
- **Preserve/exclude:** Keep real proxy/stdio V3 tool-catalog and launcher assertions. Give each worker/test a private writable root, with only the minimal config/suite/install inputs needed for startup. No whole-repository copy, production lock change, test exclusion marker, or forced serial suite.
- **CY107.D2 — evidence:** The seven observed lock-sensitive cases and any additional shared-root cases in the named files pass under at least four workers; all affected modules pass. Ruff format/lint and Pyright pass on the exact changed test/support paths, and configured production Mypy remains green. Explicit-target test Mypy is reported as failed against an identical pre-CY107 target/config/tool-version baseline; compare normalized diagnostic multisets, fix any new error, and record any remaining existing debt without calling this gate green. This narrow exception applies only to CY107's pre-existing test-source typing debt; no test filter, ignore, adapter change, or wider gate waiver is authorized. Verify that live subprocess cases still exercise the real handshake. Full suite waits for Validation.
- **Rollback:** R-CY107, the scoped inverse of the enumerated test/support paths and cycle state only.
- **Stop/go:** Stop if isolation changes production startup semantics, loses a real handshake assertion, or requires an unlisted write. Independent QA decides progression.

### CY107 execution evidence

R-CY107 begins at `57d661ca55bac0c6e95aa138abf2b3e8b50af54d`; the inverse diff is limited to the nine changed test/support paths and cycle state. The tests use private writable roots and copy only startup inputs, never the active repository lock. Both real proxy/stdio tests retain launcher and V3 tool-catalog observations. No production path, runner, adapter, lock setting, marker, or forced serial-suite policy changed.

D2: All eight named test modules pass together under four Pytest workers: 49 passed, Pytest 9.0.2/xdist 3.8.0 (`pgmcp://cache/runs/1cb5cafab42049abb5488edee9716943`). The two full live-startup modules contribute eight passing cases under four workers (`pgmcp://cache/runs/ac619e945bae4718926ebc630d76ebaa`); the two specifically retained real handshakes also passed as a separate four-worker selection (`pgmcp://cache/runs/2b0b65a301694a95a29192d1e25600ac`). Ruff 0.15.6 format/lint and Pyright 1.1.408 pass on the exact nine changed paths (`pgmcp://cache/runs/0d9387d52c4f483fa06a74a417b500cb`). Configured production Mypy 1.19.1 passed on 184 sources in CY106 and no production/config input has changed since (`pgmcp://cache/runs/b914277f20014c10b16260b23d967fc0`). Explicit-target test Mypy remains **failed**, per the approved narrow D2 exception: the same nine targets, native configuration and Mypy 1.19.1 reported 418 errors at the pre-CY107 commit (`pgmcp://cache/runs/efbcbfde6e1b440ab5af5035ce2637c3`) and 417 in the current worktree (`pgmcp://cache/runs/014078f4d038429995b3f4d427e1198b`). Comparing diagnostic multisets after stripping only line numbers yields zero new diagnostics and one removed `unused-ignore` in `test_validate_tool_arguments.py`; file identity, code, message and multiplicity were preserved. The existing typing debt remains a failed diagnostic, not a green gate. Complete-suite proof remains Validation. Independent implementation-cycle review is requested without a producer GO claim.

The independent review of commit `1b6bebccf88b31dfaf0d389401eea26c9a22763f` returned NOGO because two in-process bootstrap/registration tests still opened a relative audit file in the shared repository process directory despite private workspace settings. Their helper now disables audit output, which those registration cases do not assert; the separately owned CY106 audit tests and real proxy/stdio handshakes remain intact. The complete eight-module four-worker selection passes again, 49/49 (`pgmcp://cache/runs/68673880ff1140df807c69bd7ad8f4de`); Ruff format/lint and Pyright pass on the repaired path (`pgmcp://cache/runs/5a85b6ccfb81439b920401bf3f098dfe`). Fresh exact-target test Mypy remains failed with 417 diagnostics (`pgmcp://cache/runs/03975a0fad284c78b3d27393ce5e72b0`); the same multiset comparison against pre-CY107 `pgmcp://cache/runs/efbcbfde6e1b440ab5af5035ce2637c3` still yields zero new and one removed `unused-ignore`. A fresh independent review of this correction is requested.

Independent CY107 review subsequently confirmed the audit side-effect was removed and ran the pre-CY107 Mypy baseline itself after all nine test/support files were temporarily restored from `57d661ca55bac0c6e95aa138abf2b3e8b50af54d`. With the same nine ordered targets, native Mypy 1.19.1, adapter fingerprint and effective arguments, its baseline had 418 errors in seven files (`pgmcp://cache/runs/f847b792de234b908baed22fc19208b9`) versus 417 in its earlier current-tree run (`pgmcp://cache/runs/8855f8f721bb49bf93223fb841c460ef`). Its complete 106,012-codepoint baseline resource was read in 18 contiguous windows; a diagnostic multiset comparison stripping only line numbers found zero additions and the same one removed `unused-ignore`. QA reported CY107 GO for `b5d92724da54e05b2564575a11377a200b40cb6e`, while expressly leaving test-target Mypy failed. All nine temporarily restored files were returned to HEAD afterward; tracked status is clean. This QA verdict is independent review evidence, not a producer claim that the test-Mypy gate passed.

## CY108

**Discriminate actual child-process lifetime**

- **Predecessor:** CY107, because parallel tests expose process-lifetime races.
- **Shared-file predecessors:** No overlapping new amendment-cycle writer; previous lifecycle test writes are in the completed CY001–CY105 chain.
- **Authority:** Existing process-stopping design and approved five-second stop budget.
- **CY108.D1 — bounded result:** In `tests/mcp_server/integration/execution/test_process_stopping.py`, retain handles to original child processes before invocation finishes and assert their true signaled/live state for confirmed and intentionally `TerminationProblem.UNCONFIRMED` outcomes. The RED finding authorizes one additional production write-set path, `mcp_server/execution/process_runtime.py`: make Windows Job membership confirmation cover the original member processes' actual completion, not only a zero active-process accounting value. Retain member identity before it can be recycled; close all owned handles. The same managed execution/stop boundaries remain public.
- **Preserve/exclude:** Preserve all nine lifecycle claims, the two intentionally unconfirmed stop outcomes, original failure cause, the single shared five-second stop deadline, accepted-response completeness, and explicit teardown. Do not expose new config/tool inputs, change adapter contracts or error DTOs, alter process creation/Job assignment, or widen the fix beyond runtime membership confirmation. A native observation failure cannot silently become confirmed termination; no accepted response may coexist with unconfirmed completion.
- **CY108.D2 — evidence:** The three observed RED failures become GREEN without weakening original-handle assertions. All nine lifecycle cases and the wider process-runtime integration selection pass under at least four workers. Exact-file Ruff format/lint/Mypy/Pyright pass on the production and test paths; configured production Mypy remains green. Confirm both original child handles are signaled before a confirmed outcome and remain live in the two intentionally unconfirmed fault-injection cases until teardown; preserve cause and one five-second budget. A PID-only lookup, job count alone, or late process exit after return is insufficient.
- **Rollback:** R-CY108, the scoped inverse of `mcp_server/execution/process_runtime.py`, this one test path and cycle state; preserve the committed RED characterization as an auditable intermediate state.
- **Stop/go:** Stop on a still-live original child after a confirmed outcome, a falsely stopped intentionally unconfirmed child, changed DTO/adapter/config semantics, a second stop budget, unclosed process handles, out-of-set writes, or failing D2. If the Windows Job cannot retain/confirm member identity within this write-set and five-second contract, reopen Design rather than weakening the observation. Independent QA decides progression.

### CY108 RED finding

R-CY108 begins at `a4898aa33476183f42d62d8aa1ae224f1fc0f2a7`. The pre-change nine lifecycle cases passed under four workers (`pgmcp://cache/runs/27dab1333ad54c7496c11a56e4cb46a8`). The test-only change retains Windows process handles for the original children while the invocation runs; a short child/parent acknowledgement barrier ensures handles are acquired before a fast parent response or stop. Confirmed outcomes now assert the retained handles are signaled; the two intentionally `UNCONFIRMED` outcomes assert the originals remain live before explicit teardown. No production path has been edited. Ruff format/lint, Mypy and Pyright pass on the test file (`pgmcp://cache/runs/bcb57671f9b64b7494ede45d4f819207`). The nine cases now yield three failures and six passes under four workers (`pgmcp://cache/runs/45be8eac08a14f65a2cfd7efb056582b`): crash, invalid response and deadline expiry report confirmed stop while at least one original child handle remains unsignaled at return. An exploratory check on the invalid-response case found three job-accounted processes and `IsProcessInJob` true for both children before completion (`pgmcp://cache/runs/6a53ce70ada64cf0b383d515e8ed0d6d`); that private-introspection instrumentation was then removed from the durable test. Per the stop/go rule, implementation stops for a bounded Planning amendment; no runtime change may proceed on the existing CY108 write-set.

### CY108 GREEN evidence

The independently reviewed Planning amendment at `bd3a4111ec286fecb133078b8c98c8e10c838761` adds only `mcp_server/execution/process_runtime.py` to the original test write-set. R-CY108 is the scoped inverse of those two code/test paths and cycle state, preserving the committed RED characterization. WindowsJob now observes the complete native Job member PID list before termination and while waiting, opens only synchronization/query handles, verifies that each retained handle still belongs to its Job, and closes every owned handle. Actual original-handle signal state is required alongside zero Job active processes; neither a reused PID nor a zero accounting value alone confirms completion. Native observation failure cannot silently become confirmed, and a natural completion observation failure becomes the existing typed process failure before an accepted adapter result can be published. The existing five-second shared stop deadline, invocation result DTOs, process creation/assignment and adapter contracts remain unchanged. Microsoft documents the [Job member list](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_process_id_list) and [membership query](https://learn.microsoft.com/en-us/windows/win32/api/jobapi/nf-jobapi-isprocessinjob) used for identity verification.

The nine lifecycle cases and the wider process-runtime integration selection pass together under four Pytest workers, 25/25, Pytest 9.0.2/xdist 3.8.0 (`pgmcp://cache/runs/3b1508d44d504c9a8bfe7427e3f0561e`). The three original-handle RED failures are now GREEN without relaxing their assertions; both intentionally unconfirmed cases still observe live original children before fixture teardown. Exact-file Ruff format/lint 0.15.6, Mypy 1.19.1 and Pyright 1.1.408 pass on the two changed paths (`pgmcp://cache/runs/9f9c93bc5c6944dcab0c457cc75e70e7`); configured production Mypy passes across its native scope (`pgmcp://cache/runs/13ef17b699684c9e80be5900677a4431`). Complete-suite proof remains Validation. Independent implementation-cycle review is requested without a producer GO claim.

Independent QA returned NOGO for `70296d886a0023110ea8cf8e9e66ac5ff0e9bf6f`: a Job member could be born after the pre-termination PID snapshot but before `TerminateJobObject`, be terminated, and disappear from accounting before its original handle is retained. The second repair retains the leader handle at assignment and compares cumulative native Job process counts from before the stop snapshot through termination and final confirmation. Any count increase or native observation failure is reported as `UNCONFIRMED`; the runtime does not claim that an unobserved original process was signaled. Normal accepted completion does not compare cumulative history, because already-finished transient helpers must remain valid. A real Node race fixture starts an additional child in the snapshot/termination gap and expects the original timeout plus `UNCONFIRMED`; a separate short-lived-child fixture proves a valid completed response still succeeds. Both cases remain within the two approved paths and the existing five-second stop budget.

The widened lifecycle/process-runtime selection now passes 27/27 under four workers (`pgmcp://cache/runs/a728e3e0272b4859bb98b036bbc16485`). All four exact-file gates pass on the two paths (`pgmcp://cache/runs/7935a662102d41f896727e5188fa8dfe`) and configured production Mypy remains green (`pgmcp://cache/runs/74bb6538b9fb4a91a4c1348242e577d7`). The test-only attempt to temporarily weaken this guard as a mutation check was rejected by automatic review and wrote nothing; the actual regression uses a live child and native count growth, with no weakened production state. Independent QA reviewed the corrected commit `f99dd98aa76d8d12989156488e1306d78782e67d` and returned GO for CY108. QA confirmed the cumulative-count guard closes the snapshot/termination race, the real late-child and transient-child regressions exercise both sides of the rule, and the five-second stop budget and two-path write set remain intact. QA independently ran 27/27 lifecycle/process-runtime tests with four workers (`pgmcp://cache/runs/cc3e4800a5cf4f2fa2b1d69c39b5d701`), all four exact-file gates (`pgmcp://cache/runs/706fa3a9a1d146659570ff0cb8c15339`), and configured production Mypy over 184 files (`pgmcp://cache/runs/f149d34c99eb435fa72aed2a91500eab`). The independent verdict supersedes the earlier NOGO for CY108; full-suite proof remains Validation.

## CY109

**Resolve test-source Ruff import debt**

- **Predecessor:** CY108; the lint inventory is the Ruff 0.15.6 resource `pgmcp://cache/runs/1684a3432c8a4c709c32888350c55fcf`.
- **Shared-file predecessors:** No overlapping new amendment-cycle writer; previous test writes are in the completed CY001–CY105 chain.
- **CY109.D1 — bounded result:** Resolve the 50 E402 findings in exactly `tests/mcp_server/config/test_operation_policies.py`, `tests/mcp_server/integration/test_ready_phase_enforcement.py`, `tests/mcp_server/unit/adapters/test_git_adapter_neutralize_to_base.py`, `tests/mcp_server/unit/adapters/test_git_adapter_skip_paths.py`, `tests/mcp_server/unit/config/test_c_loader_structural.py`, `tests/mcp_server/unit/config/test_loader.py`, `tests/mcp_server/unit/managers/test_deliverable_checker.py`, `tests/mcp_server/unit/managers/test_enforcement_runner_unit.py`, `tests/mcp_server/unit/managers/test_git_manager_skip_paths.py`, and `tests/mcp_server/unit/managers/test_phase_contract_resolver_c3.py`.
- **Preserve/exclude:** Preserve imports' required initialization order, collection, and assertions. No global Ruff ignore, rule relaxation, or unrelated cleanup.
- **CY109.D2 — evidence:** Native Ruff lint/format on these exact files passes; their affected tests pass. Review import-order side effects explicitly.
- **Rollback:** R-CY109, scoped inverse of these ten test paths and cycle state.
- **Stop/go:** Stop on semantic import-order dependency that needs a larger redesign or out-of-set write. Independent QA decides progression.

### CY109 implementation evidence

The ten-file baseline passed 50 tests with one existing xpass under four workers (`pgmcp://cache/runs/337798bf483242c59eb5a07420efb67a`); native Ruff format passed and lint reported the expected E402 inventory (`pgmcp://cache/runs/c9a0741141da4d9eb60168a033058531`). Each file had `get_default_server_root` imported before its module docstring. The import now follows the docstring inside Ruff's sorted import block. The diff contains only that import move in the ten approved paths. The moved import binds `get_default_server_root` but does not call it at import time; the helper body calls `Settings.from_env` only when tests invoke it. Ruff places that helper import after the other imports. No test module sets state between imports, and the same collected tests pass before and after the reorder, so no required import-order dependency was observed. The same selection passed 50 tests with one xpass under four workers after the edit (`pgmcp://cache/runs/b481d48b4fce473190bb658e3435ee4c`); native Ruff lint and format both pass (`pgmcp://cache/runs/4ac793cd0ada4fcfa245104e5cdc9ef2`). Independent QA returned GO for CY109 on `18f8c2ec3f5e60a1f0496449bc482445854a99cc`: the ten-file diff changes only the helper import placement, no intermediate initialization depends on the former position, and no tests or Ruff rules were suppressed. QA independently ran the ten test modules under four workers (50 passed, one existing xpass; `pgmcp://cache/runs/f2f51069c05042fdb1ccf734c15fbbbe`) and Ruff 0.15.6 lint/format on all ten files (both passed; `pgmcp://cache/runs/5b20bb693966455da0446324128a0acd`). The xpass and five Pydantic warnings predate this import-only cycle; removing the xfail marker is outside CY109.

## CY110

**Resolve production-source Ruff lint debt**

- **Predecessor:** CY109; same bounded Ruff inventory.
- **Shared-file predecessors:** No overlapping new amendment-cycle writer; previous production writes are in the completed CY001–CY105 chain.
- **CY110.D1 — bounded result:** Resolve six T201, three ANN401, one ARG002, and one PLC0415 finding in exactly `mcp_server/#Archief/supervisor_old.py`, `mcp_server/core/proxy.py`, `mcp_server/managers/phase_state_engine.py`, and `mcp_server/tools/cycle_tools.py`.
- **Preserve/exclude:** Preserve proxy stdout/stderr transport bytes, the public constructor and extension behavior, phase/cycle behavior, and archived module's observable behavior. No blanket suppression or generic contract change.
- **CY110.D2 — evidence:** Native Ruff lint/format on these exact files passes; affected proxy, phase, and cycle tests pass. Record an independent path-by-path equivalence analysis of all five changed proxy stdout/stderr writes, including stream destination, text, newline, flush, and any source transformation; existing tests do not assert all five byte paths.
- **CY110.D3 — line-ending preservation:** In the same cycle, preserve existing CRLF/LF/CR terminators in unchanged spans for targeted `safe_edit_file` operations. The user explicitly approved this 2026-09-27 Research/Design amendment. Write-set: `mcp_server/core/interfaces/file_writer.py`, `mcp_server/utils/atomic_file_writer.py`, `mcp_server/services/edit_construction.py`, `mcp_server/services/edit_operation.py`, `mcp_server/bootstrap.py`, and `tests/mcp_server/integration/test_edit_operation_v3.py`; add `tests/mcp_server/unit/services/test_edit_construction.py` only if a pure mapping edge case is not covered durably by integration. Preserve public tool inputs/outputs, exact `rewrite`, UTF-8, race guard, validation policy, and logical `content_changed`.
- **CY110.D4 — preservation evidence:** Characterize the current CRLF defect as RED, then prove CRLF replace/append/pattern replacement, mixed-source untouched terminators, no-match identity, exact rewrite, and check-input/write-byte agreement as GREEN with focused tests and native exact-file Ruff format/lint/Mypy/Pyright. Keep four-worker suite and branch gates for Validation. Confirm `phase_state_engine.py` retains original CRLF and only three added/five removed semantic lines in its final diff.
- **Rollback:** R-CY110, scoped inverse of the four lint paths, the D3/D4 safe-edit paths, and cycle state. Stop on a public contract change, out-of-set write, whole-file newline churn, weakened race guard, or failed affected tests. Independent QA decides progression.
- **Stop/go:** Stop on behavior-changing lint fixes, an unlisted write, or failed affected tests. Independent QA decides progression.

### CY110 implementation evidence and line-ending correction

The four-file Ruff 0.15.6 baseline reported exactly six T201, three ANN401, one ARG002 and one PLC0415 findings; format already passed (`pgmcp://cache/runs/b220c800688e4ee9b0b86350bee97586`). The affected proxy/phase/cycle test selection passed 152 tests with one existing skip under four workers before the edit (`pgmcp://cache/runs/f4b121b8de5d48ef99cd99aeb9a4a111`). The implemented changes replace each stderr/stdout `print` with explicit writes of the same formatted text plus newline and immediate flush; retain `PhaseStateEngine.__init__`'s public `state_reconstructor` keyword while typing and explicitly discarding the unused value; move the independent mutator import to module scope; and use `object` for the pre-validation Pydantic input/output. After the edits, the same 153-item test selection reports 152 passed and one skipped (`pgmcp://cache/runs/313fa724b67c475493bf587921c5ba4a`), while exact-file Ruff lint/format, Mypy and Pyright all pass (`pgmcp://cache/runs/24a75d234fdd4dfa82e9fba91ea013b7`). The byte-equivalent proxy writes still require independent review; existing proxy tests are shallow and do not themselves assert each transport byte path.

`safe_edit_file` normalized the existing CRLF line endings in `mcp_server/managers/phase_state_engine.py` to LF during these targeted edits. A read-only Git comparison ignoring line-ending whitespace shows only the planned import, annotation, unused-argument and local-import changes, but the ordinary diff shows the whole 730-line file as changed. Automatic approval review rejected two attempts to restore the original CRLF line endings, even after the narrow semantic diff was shown, on grounds that a whole-file newline rewrite is outside CY110. The owner then explicitly authorized both CRLF restoration in `phase_state_engine.py` and safe-edit line-ending preservation within CY110 on 2026-09-27. The exact original CRLF convention was restored through `safe_edit_file` and committed in `d4f26771628d635858c48fa1f87605e0dd24c5a3`; the ordinary diff is now limited to the planned semantic lines. The earlier automatic-review denial no longer blocks this authorized correction. Final CY110 GO still requires independent review of the expanded D3/D4 implementation. Independent QA provisionally found no substantive blocker in the four planned source paths: it inspected all five proxy stream replacements, archived supervisor output, constructor compatibility, mutator import and Pydantic validator; it observed no hidden semantic expansion when line endings were ignored. QA independently ran a 16-module selection (126 passed, one existing skip; `pgmcp://cache/runs/15b0d78491714d308d2ba8a704e60d2d`), supplemental constructor/mutator tests (39 passed; `pgmcp://cache/runs/5fa703c861f942a39e78316ba2080aea`), and all four exact-file gates (`pgmcp://cache/runs/87b32a5297f942bcb7cc71bb93f96967`). QA withheld final GO at that point until the line endings were resolved and the committed diff could be confirmed against the reviewed code.

### CY110 completion evidence (D1–D4, 2026-09-27)

The owner explicitly authorized this bounded CY110 expansion. The original CRLF convention in `mcp_server/managers/phase_state_engine.py` is restored in commit `d4f26771628d635858c48fa1f87605e0dd24c5a3`: 728 CRLF terminators, no LF-only terminators, and the ordinary semantic diff is three added/five removed lines. The four lint source paths retain the earlier independent provisional review and exact-file gate evidence above. The full five-path proxy analysis required by D2 is source-based, not a claim that existing tests assert every byte path:

| Changed path | Destination and text | Preserved transformations and flush |
|---|---|---|
| Audit-log failure | stderr: `[PROXY ERROR] Audit log failed: {e}\n` | Same exception formatting, one newline, immediate flush. |
| Proxy log | stderr: `[PROXY] {message}\n` | Same message and subsequent audit call, one newline, immediate flush. |
| JSON-RPC forward | stdout: `{line}\n` | Existing strip, empty-line filtering and JSON validation remain before write; immediate flush. |
| Server stderr | stderr: `[SERVER] {line}\n` | Existing strip, empty-line and restart-marker handling remain before write; immediate flush. |
| JSON error response | stdout: serialized `err_response` plus `\n` | Existing JSON serialization and error payload remain; immediate flush. |

D3/D4 RED evidence: the first seven-case integration characterization failed in six CRLF/mixed cases and passed in the LF control (`pgmcp://cache/runs/75b35884d3be4b759ff417ed04efddce`). Two explicit-CRLF cases then exposed a second defect (`pgmcp://cache/runs/189c67541f1e47c89a2a18c4c4e1d66e`), and the mixed multiline replacement exposed incorrect diff-inferred ownership of a replaced newline (`pgmcp://cache/runs/43fed75395464057a6c06cf52545df9a`). The final operation-span implementation, committed in `937149bf888a1610b587c87de93db73eb6aad3cf`, reads one snapshot with logical and source-preserving views, constructs logical/physical proposals from the same exact operation spans, validates and writes the physical text, and retains logical `content_changed` and exact `rewrite`. The final focused four-module selection passed 71 tests under four workers (`pgmcp://cache/runs/210d05acedbd41779424293c8e5c3f1d`); native Ruff format/lint, Mypy and Pyright passed on all seven changed D3/D4 paths (`pgmcp://cache/runs/0138a6aabc0943ee8df4060ccb95d7fc`). A bounded read-only preflight found no remaining D3/D4 finding and independently ran 46 relevant tests and all four file gates (`pgmcp://cache/runs/2257bbadf956437c9a7378fe9677d035`, `pgmcp://cache/runs/aedc2bb3d7474f02a954e61930816aa5`). The full parallel suite and branch/configured gates remain Validation obligations, and this producer evidence is not an independent QA GO.

After reloading the committed server with `restart_server` (process 30168), a live `safe_edit_file` replace inserted a temporary class-line comment into the existing CRLF `phase_state_engine.py` and then removed it (`pgmcp://cache/runs/48ee993f8b2c4e06b75e4dbd8069b35c`, `pgmcp://cache/runs/562191fd80ae4806908a8aad7bec1c59`). Both calls passed enforced Python preflight. The edited file retained 728 CRLF and zero LF-only terminators throughout; its SHA-256 before and after was `477215F70FAE6BA8848E9EE0FE4517C72E59AE3603A704D08A0954E2468A0EA9`. The final PGMCP git status reported zero modified tracked files. This proves the active tool uses the new preservation path without leaving the temporary edit behind.
Independent QA subsequently issued a CY110 NOGO on commit `89657a433ec2122bedd0e49740b56a6cd35ccbe7`: an identical logical targeted replacement could rewrite an existing LF in a mixed-terminator file as CRLF while reporting `content_changed=False`. The source-derived example `b"a\r\nb\nc\r\n"` with `b\n` replaced by `b\n` was reproduced for `replace`, literal `pattern_replace`, and regex `pattern_replace` by three failing integration cases (13 other cases passed; `pgmcp://cache/runs/5bd0dbe13e4e4de28b130ece5e81a5ef`); the RED regression is commit `af1c9e437b2e237f2b4ed1efaec3e53378bede5f`. The bounded GREEN correction in `5bc44c1fc042b1c7f3da2c15dae0dfacc09fffe9` returns the original source text for a logically unchanged targeted proposal while retaining the separate exact `rewrite` path. The regression and surrounding edit/atomic-writer selection then passed 53 tests under four workers (`pgmcp://cache/runs/1504138ddc874e0daf01bc5ad3e4a846`); native Ruff format/lint, Mypy and Pyright passed on the two newly changed files (`pgmcp://cache/runs/8adf9f9131f048c38f7b1efe4773ca60`). Independent QA then re-reviewed the corrected CY110 D1–D4 on commit `ed6c4b0101f30d073d7e74e58f59986dcaf79f19` and issued GO with no remaining blocker. QA independently confirmed the three identity regressions, exact rewrite behavior, check-input/write-byte identity, unchanged prior D1/D2 evidence, and CRLF preservation in `phase_state_engine.py`; its four-worker focused run passed 53 tests (`pgmcp://cache/runs/5448d5fa10864e95a1f54c8439613392`), and all four exact-file gates on the two newly changed paths passed (`pgmcp://cache/runs/2e0fe9b233564745b8a5ebc00daee2ba`). The full parallel suite and branch gates remain Validation obligations.


## CY111

**Correct active scaffold guidance against the V3 public contract**

- **Predecessor:** CY110 implementation GO and the Validation F-VAL-05 finding. The return from Validation to Planning is the owner-authorized, audited phase transition of 2026-09-27; no Research/Design strategy change is required.
- **Authority:** [DI-07 §7.3–§7.4 and DOCFLOW-E03/E05](design-workflow-documentation.md#74-consumer-guidance), the live strict `ScaffoldArtifactInput` in `mcp_server/tools/scaffold_tool.py`, and the active `scaffold_schema` artifact-type enum.
- **CY111.D1 — bounded result:** In the authoritative `docs/agents/vscode/copilot/AGENTS.md`, `docs/agents/codex/AGENTS.md`, and `docs/agents/antigravity/AGENTS.md`, replace only the stale always-on scaffolding examples, copied type inventory and retired registry guidance. Point ordinary callers to live tool-schema admission; state the exact `file_name` basename-with-extension and context-schema requirements. Keep the configured `.pgmcp/template_suite/` source location accurate without turning filesystem discovery into a competing invocation contract. Propagate source-first to the mapped active copies `AGENTS.md` and `.agents/AGENTS.md`. No Antigravity active copy is present in the direct-pair map.
- **Preserve/exclude:** Preserve all other always-on instructions, role authority, phase procedure and host-specific content. Do not add aliases, tool behavior, registry entries, production/test code or a second static artifact-ID inventory. F-VAL-06 count provenance, expanded test-Mypy debt, D-VAL-01 and D-VAL-02 are outside this cycle.
- **CY111.D2 — evidence:** Confirm the five exact files contain no rejected `name=` scaffold examples, unregistered example IDs or `.pgmcp/templates/config/` registry claim; check the revised wording against the live input/schema contract. Run focused Markdown document checks on the five changed files, verify both direct source/copy pairs are byte-identical, and review source and copied wording semantically under DOCFLOW-E05. No artificial RED or full suite for this documentation-only correction; Validation retains the branch/suite obligations and independent QA reviews this cycle.
- **Rollback:** R-CY111 is the scoped inverse of the five documentation files, the planning amendment and workflow state only. Stop on an unlisted edit, broken source/copy parity, a still-invalid invocation instruction, or a failed focused check. Independent QA determines progression.

## Validation correction cycles — 2026-09-27

The owner requested closure of the two remaining concrete Validation findings after receiving the targeted architecture fix approach. Research's approved clean break and DI-02/DI-06 identity semantics remain binding. The audit of everyday tool behavior is bounded to the six #460-affected public routes in D-VAL-04 and is not an implementation dependency of these cycles. CY112 and CY113 are serial, reversible corrections; the full configured parallel suite and branch gates return to Validation. No new public input, output, metadata or adapter contract is authorized.

## CY112

**Put shared template identity values below the service boundary**

- **Predecessor:** CY111 and this Planning amendment's independent review. No concurrent writer of the affected files.
- **Authority:** Architecture Principles §1.5 and §5, [DI-02 runtime catalog and provenance](design-suite-resolution.md#55-runtime-catalog), [DI-06 operational checkpoint](design-distribution.md), V460.1, and the Validation structural finding. The exact DTO/module names are implementation-owned; dependency direction and four-field identity semantics are fixed.
- **CY112.D1 — bounded structure:** Introduce one pure shared `mcp_server/schemas/template_identity.py` module owning the existing `TemplateId`, `TemplatePackageVersion`, `CompactFingerprint`, and frozen `ArtifactIdentity` value contracts plus the literal edge-kind type. Move, do not duplicate, their validation rules. `config.schemas.template_suite` may re-export the first two aliases for existing callers but must not define a second validation authority. Keep generation computation, manifest/policy models, and graph parsing in their current owners.
- **CY112.D2 — directed imports:** Make `core/interfaces/artifact_header_reader.py` and `config/schemas/installation.py` import only the pure values, and remove the `services/artifact_identity.py` import of `services/template_graph.py` by importing the shared edge kind in both service modules. Migrate direct identity/fingerprint consumers to the canonical value module, without changing calls, computed bytes, or JSON schemas. Exact production write-set: `mcp_server/schemas/template_identity.py` (new), `mcp_server/config/schemas/template_suite.py`, `mcp_server/config/schemas/installation.py`, `mcp_server/core/interfaces/artifact_header_reader.py`, `mcp_server/services/artifact_identity.py`, `mcp_server/services/template_graph.py`, `mcp_server/services/artifact_header_reader.py`, `mcp_server/services/template_components.py`, `mcp_server/services/template_proposal.py`, `mcp_server/services/scaffold_operation.py`, `mcp_server/schemas/mutation_outputs.py`, `mcp_server/tools/template_schema_tool.py`, `mcp_server/bootstrap.py`, and `mcp_server/cli_renewal.py`. Existing test/fixture import write-set, only where a moved type was imported from its old owner: `tests/mcp_server/fixtures/delivered_templates.py`, `tests/mcp_server/fixtures/installed_distribution.py`, `tests/mcp_server/test_support.py`, `tests/mcp_server/integration/test_schema_public_v3.py`, `tests/mcp_server/integration/test_scaffold_public_v3.py`, `tests/mcp_server/integration/test_scaffold_operation_v3.py`, `tests/mcp_server/unit/config/test_contracts_loader.py`, and `tests/mcp_server/unit/services/test_artifact_header_reader.py`. Leave service-only generation-model imports in their service module.
- **CY112.D3 — evidence:** Establish focused pre-change baseline for the existing identity, header, component, installation, catalog, public schema/scaffold, and renewal tests; after migration rerun affected tests and native exact-file format/lint/type gates. Compare the `ArtifactIdentity` and checkpoint JSON schemas and representative id/pv/pf/sf outputs before/after. Inspect import closure from the `core` and `config` consumers: neither may resolve through an identity service or Jinja graph for these values. Do not add an import-only or mirrored-implementation test where source inspection and public behavior suffice.
- **Preserve/exclude:** Preserve bounded ID/SemVer/fingerprint validation, frozen values, exact header recognition and generation-only pf/sf semantics, separate operational checkpoint, complete public schema and installed startup. No renderer/parser behavior change, new alias in the public tool contract, adapter change, or generic layer rewrite.
- **Rollback:** R-CY112 is the scoped inverse of D1/D2 paths and cycle state. Stop on changed JSON schema, provenance bytes, public registration, source imports beyond the listed seam, or a failing focused gate. Independent QA decides progression.

## CY113

**Make the late-child process test wait for a complete PID**

- **Predecessor:** CY112 independent GO. This is test synchronization only, under DI-08 and V460.4.
- **CY113.D1 — bounded result:** Change only `tests/mcp_server/integration/execution/test_process_stopping.py` so the late-child handshake reads a nonempty parseable `late.pid` within its existing two-second deadline before opening the process handle. If the child never publishes a valid PID, fail with the existing explicit stop-window assertion. Apply the same complete-file rule to the first/second child helper only if focused evidence shows the identical race there.
- **CY113.D2 — evidence:** Preserve the real child-process path and the existing `InvocationFailed`, `TIMEOUT`, `UNCONFIRMED`, and `late.done` fail-closed assertions. Run the affected process-runtime/lifecycle tests repeatedly with four or more Pytest workers and exact-file Ruff format/lint and configured typing gates; record any test-source Mypy policy result without silently expanding the configured selection. A passing focused run is not full-suite proof.
- **Preserve/exclude:** No production stop logic, Job semantics, timeout budget, marker/skip, serial-only suite, test isolation framework, or other test file changes.
- **Rollback:** R-CY113 is the scoped inverse of the single test path and cycle state. Stop on changed process assertion meaning, hidden skip, a new flaky result, or out-of-set write. Independent QA decides progression.

After CY113, return to Validation for the configured eight-worker suite, exact branch-selection check equivalence and archived Ruff finding disposition, retained carrier/structure review, current report, and independent Validation verdict.
