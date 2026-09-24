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
- **CY105.D1 — bounded result:** Remove only the remaining exhausted legacy test-helper files/functions and obsolete plugin registration left after the earlier explicitly bounded import migrations; preserve the retained narrow support and unrelated workflow fixtures.
- **Preserved behavior:** Unrelated workflow plugin, GitHub mocking, server/cycle/PR behavior, cache/atomic helpers and scoped env fixtures.
- **CY105.D2 — independent evidence:** TEST-E07/08: fixture/import/plugin request closure plus affected public server/workflow/PR tests; no global test cleanup.
- **Rollback:** R-CY105: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY105.D1 and CY105.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Readback prerequisite supplement: [R001–R008](planning-path-ownership.md#readback-prerequisite-supplement). Remove only residual exhausted helper acquisition in R004/R005/R006 after the earlier root/transport migrations. Preserve direct project lifecycle/readback assertions; no late bootstrap-root or transport migration belongs here. D1/D2 and this cycle's R-CY105, preserved behavior and independent stop/go apply to these exact additional seams.

Existing source IDs: S012, S013, S016, T004, T014, T048, T074, T095, T097, T098, T106, R004, R005, R006.

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
