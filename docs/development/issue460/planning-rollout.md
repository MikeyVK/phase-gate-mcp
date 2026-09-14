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
- **Shared-file predecessors:** None.
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
- **Shared-file predecessors:** [CY055](planning-artifacts-mutation.md#cy055), [CY064](planning-rollout.md#cy064).
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

Existing source IDs: C003, C004, C005, C006, C008, C009, C010, C011, C012, C013, C014, C015, C016, C017, C019, C020, C021, C022, C023, C024, C025, C055, C056, C063, C106, C121, C122, C123, S051, T006, T091, T096, R004, R005, R006.

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

Existing affected test/helper sources: T006, T091, T096. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

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

Existing source IDs: S012, S013, S016, T004, T014, T048, T075, T099.

Read-only review/preservation IDs: R004, R005, R006. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

- Remove each legacy helper import at the first deleted production dependency, even though final removal of empty/exhausted helper files and registrations is separately scheduled. Other helper seams such as QAManager are owned by their later consumer-removal cycles.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/tools/test_project_tools.py`
- `tests/mcp_server/unit/managers/test_project_manager.py`
- `tests/mcp_server/integration/test_project_plan_readback.py`
- `tests/mcp_server/integration/test_scaffold_public_v3.py`
- `tests/mcp_server/integration/test_edit_public_v3.py`
- `tests/mcp_server/integration/test_pr_status_lockdown.py`
- `tests/mcp_server/unit/test_server.py`
- `tests/mcp_server/unit/tools/test_cycle_tools.py`

Existing affected test/helper sources: S012, S013, S016, T004, T014, T048, T075, T099. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

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

Existing source IDs: C055, C064, C097, C098, T001, T005, T008, T012, T013, T015, T020, T021, T048, T076, T077, T078, T079, T080, T091, T103, T104.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

- Only retire named obsolete bodies/imports/tests. Existing test rows may already have migrated; delete only superseded claims and retain their Design-mandated observable successors. A remaining caller stops this cycle and requires an explicit bounded amendment before removal.

- Close the last ArtifactManager imports in T013/T015/T077/T080 here even when later registry/metadata/location-only assertions survive. Their later cycles may handle only claims independent of the deleted manager.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/test_schema_public_v3.py`
- `tests/mcp_server/integration/test_scaffold_public_v3.py`

Existing affected test/helper sources: T001, T005, T008, T012, T013, T015, T020, T021, T048, T076, T077, T078, T079, T080, T091, T103, T104. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

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

Existing source IDs: C066, C088, C089, C090, T048, T082, T083, T084, T085, T086.

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

Existing affected test/helper sources: T048, T082, T083, T084, T085, T086. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

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

Existing source IDs: C055, C057, C058, C060, C061, C080, C081, C085, C086, C107, S049, S050, T015, T048, T049, T059, T061, T062, T063, T064, T068, T069, T077, T091, T095, T099.

Read-only review/preservation IDs: C064, C066. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

- Close this cycle's specific retired exports/imports in shared schemas/interfaces/test_support and mixed tool-input tests at the same boundary; preserve unrelated GateReport/GateViolation workflow contracts.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/config/test_template_suite.py`
- `tests/mcp_server/unit/services/test_template_contract_loader.py`
- `tests/mcp_server/unit/utils/test_schema_utils.py`
- `tests/mcp_server/unit/services/test_artifact_identity.py`
- `tests/mcp_server/integration/test_schema_public_v3.py`

Existing affected test/helper sources: S050, T015, T048, T049, T059, T061, T062, T063, T064, T068, T069, T077, T091, T095, T099. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY077, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY078

**Retire legacy metadata and lifecycle contracts**

- **Semantic predecessors:** [CY077](planning-rollout.md#cy077).
- **Shared-file predecessors:** [CY072](planning-rollout.md#cy072), [CY074](planning-rollout.md#cy074), [CY007](planning-execution.md#cy007), [CY002](planning-execution.md#cy002).
- **Authority:** [DI-01/02 §9; Shared §12](design-suite-resolution.md).
- **CY078.D1 — bounded result:** Remove legacy source-header metadata config/parser and lifecycle exports plus their explicitly named test imports; retain V3 first-line reader and separate context/provenance.
- **Preserved behavior:** Generation/header/schema claims already proved; no history replacement or edits to existing artifacts.
- **CY078.D2 — independent evidence:** Collect T090 and all surviving listed test files after removal; no imports of removed base/lifecycle/parser. Header adversarial cases and real scaffold context isolation remain covered.
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

Existing source IDs: C055, C057, C058, C060, C085, C086, C091, C092, C096, C099, C100, C101, C102, C103, C104, C105, C106, C107, S057, T048, T057, T058, T064, T067, T068, T073, T091, T099, T100, T102, T142.

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

Existing source IDs: C055, C057, C058, C060, C079, C107, S017, S018, S019, S020, S021, S022, S023, T003, T047, T067, T068, T073, T080, T095, T099.

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

Existing source IDs: C055, C085, C086, C106, C107, C108, C110, C114, T048, T075, T091, T099, T106, T110, T127, T137, T140.

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

## CY092

**Architecture diagrams**

- **Semantic predecessors:** [CY077](planning-rollout.md#cy077), [CY078](planning-rollout.md#cy078), [CY079](planning-rollout.md#cy079), [CY080](planning-rollout.md#cy080), [CY081](planning-rollout.md#cy081), [CY082](planning-rollout.md#cy082), [CY083](planning-rollout.md#cy083), [CY086](planning-rollout.md#cy086), [CY087](planning-rollout.md#cy087), [CY088](planning-rollout.md#cy088).
- **Shared-file predecessors:** None.
- **Authority:** [DI-07 §7.5; XC-01](design-workflow-documentation.md).
- **CY092.D1 — bounded result:** Update seven catalogued subsystem/config/tool/naming diagrams to exact responsibility/dependency boundaries.
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

## CY094

**Retire legacy Pydantic/class sources**

- **Semantic predecessors:** [CY032](planning-artifacts-mutation.md#cy032), [CY033](planning-artifacts-mutation.md#cy033), [CY034](planning-artifacts-mutation.md#cy034), [CY035](planning-artifacts-mutation.md#cy035), [CY072](planning-rollout.md#cy072), [CY080](planning-rollout.md#cy080).
- **Shared-file predecessors:** None.
- **Authority:** [DI-03 code §9; DI-01/02 §9](design-code-test-artifacts.md).
- **CY094.D1 — bounded result:** Remove only old DTO/config/class/protocol configs/roots and related obsolete fixture assertions.
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

## CY096

**Retire legacy phase-document roots**

- **Semantic predecessors:** [CY042](planning-artifacts-mutation.md#cy042), [CY043](planning-artifacts-mutation.md#cy043), [CY044](planning-artifacts-mutation.md#cy044), [CY045](planning-artifacts-mutation.md#cy045), [CY046](planning-artifacts-mutation.md#cy046), [CY047](planning-artifacts-mutation.md#cy047), [CY048](planning-artifacts-mutation.md#cy048), [CY049](planning-artifacts-mutation.md#cy049), [CY050](planning-artifacts-mutation.md#cy050), [CY051](planning-artifacts-mutation.md#cy051), [CY072](planning-rollout.md#cy072).
- **Shared-file predecessors:** None.
- **Authority:** [DI-03 documents §9](design-document-tracking-artifacts.md).
- **CY096.D1 — bounded result:** Delete only old Research/Design/Planning/Validation concrete roots/configs; close their actual root-rendering tests.
- **Preserved behavior:** Nineteen workflow meanings, original PR defects, structured links/refs/checklists and commit semantics.
- **CY096.D2 — independent evidence:** DOC family evidence and no active legacy render paths; approved phase content not discarded as obsolete prose.
- **Rollback:** R-CY096: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY096.D1 and CY096.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: A005, A012, A015, A022, A027, A034, A037, A044, T045, T046.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

- Before deleting any listed source, require its named successor evidence and zero remaining runtime/template/fixture imports. Tests for the same removed source are adapted or removed in this same cycle; unrelated portions remain.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/templates/test_research_artifact.py`
- `tests/mcp_server/integration/templates/test_design_artifact.py`
- `tests/mcp_server/integration/templates/test_planning_artifact.py`
- `tests/mcp_server/integration/templates/test_validation_artifact.py`

Existing affected test/helper sources: T045, T046. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY096, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

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

## CY099

**Retire portable Python/test macro sources**

- **Semantic predecessors:** [CY031](planning-artifacts-mutation.md#cy031), [CY041](planning-artifacts-mutation.md#cy041), [CY094](planning-rollout.md#cy094), [CY095](planning-rollout.md#cy095), [CY096](planning-rollout.md#cy096), [CY097](planning-rollout.md#cy097), [CY098](planning-rollout.md#cy098).
- **Shared-file predecessors:** [CY039](planning-artifacts-mutation.md#cy039), [CY037](planning-artifacts-mutation.md#cy037), [CY033](planning-artifacts-mutation.md#cy033).
- **Authority:** [DI-01/02 §9; DI-03 code/doc §9](design-code-test-artifacts.md).
- **CY099.D1 — bounded result:** Remove only legacy Python/testing macros after every concrete Python consumer has migrated.
- **Preserved behavior:** Shared syntax/link/fixture/omission claims already in public family coverage.
- **CY099.D2 — independent evidence:** Graph reachability/import scan plus affected family proof; remove direct macro tests only after named successor coverage.
- **Rollback:** R-CY099: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY099.D1 and CY099.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: A066, A071, A072, A073, A074, A076, T031, T036, T037, T038, T039, T041.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

None.

Previously introduced paths revisited in this cycle:

None.

- Before deleting any listed source, require its named successor evidence and zero remaining runtime/template/fixture imports. Tests for the same removed source are adapted or removed in this same cycle; unrelated portions remain.

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

Existing source IDs: A058, A059, A060, A061, A062, A063, A064, T026, T029, T055.

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

Existing affected test/helper sources: T026, T029, T055. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY100, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

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

## CY103

**Remove unreachable YAML and test seeds and agent hints**

- **Semantic predecessors:** [CY102](planning-rollout.md#cy102).
- **Shared-file predecessors:** [CY039](planning-artifacts-mutation.md#cy039).
- **Authority:** [Research F-14/F-14A/F-14B/deferred YAML; DI-03 §9](design-integration-review.md).
- **CY103.D1 — bounded result:** Delete the explicitly unreachable YAML bases, empty test seeds and agent-hint pattern; record exact Git recovery trace for deferred YAML only.
- **Preserved behavior:** No retained generated/runtime classes deleted; future YAML recovery trace records exact historical source/removal commit.
- **CY103.D2 — independent evidence:** Approved no-retained-behavior dispositions, zero source imports, CODE-E07 fixture capacity retained and exact source SHA/path recovery trace; no new deferred feature implementation.
- **Rollback:** R-CY103: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY103.D1 and CY103.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: A048, A054, A057, A065, A075, S048, T030, T040.

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
- `tests/mcp_server/integration/test_schema_public_v3.py`

Existing affected test/helper sources: T030, T040. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY103, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

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
