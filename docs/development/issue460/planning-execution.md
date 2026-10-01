# Issue 460 Planning — Execution foundations

Status: DRAFT, producer planning. [Hub](planning.md) defines the binding verification/recovery rules and semantic coverage. [Path index](planning-path-ownership.md) expands every exact source ID. No implementation evidence or independent approval is claimed here.

## CY001

**Isolated suite roots**

- **Semantic predecessors:** Independent Planning GO.
- **Shared-file predecessors:** None.
- **Authority:** [DI-08 §§7.1,7.3,10](design-test-architecture.md).
- **CY001.D1 — bounded result:** Introduce explicit-root/package-tree support with a concrete existing public ConfigLoader consumer. Record the single active server launch/runtime baseline and preserve old harness/plugin callers.
- **Preserved behavior:** Unrelated workflow fixtures and collection; no implicit CWD/config authority.
- **CY001.D2 — independent evidence:** TEST-E01/02/07: two isolated roots consumed by the real existing loader cannot leak configuration or CWD. Record interpreter/import origin/CWD/explicit roots/relevant nonsecret launch settings and current read-only tool contract; no standalone helper-only test or parallel persistent server.
- **Rollback:** R-CY001: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY001.D1 and CY001.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Readback prerequisite supplement: [R001–R008](planning-path-ownership.md#readback-prerequisite-supplement). Bind R004/R005/R006 to the explicit test-root fixture seam while preserving their legacy assembly until the scheduled cutover. D1/D2 and this cycle's R-CY001, preserved behavior and independent stop/go apply to these exact additional seams.

Existing source IDs: S012, S037, T004, T048, T095, R004, R005, R006.

Read-only review/preservation IDs: C063. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `tests/mcp_server/fixtures/suite_roots.py`
- `tests/mcp_server/unit/fixtures/test_suite_roots.py`

Previously introduced paths revisited in this cycle:

None.

- The listed legacy review-only paths retain their current constructors, runtime reads and normal registration. New behavior is exercised through the separately named final internal components; no V2/V3 ToolAssembly union, public alias, fallback reader or constructor mode.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/tools/test_project_tools.py`
- `tests/mcp_server/unit/managers/test_project_manager.py`
- `tests/mcp_server/integration/test_project_plan_readback.py`
- `tests/mcp_server/unit/fixtures/test_suite_roots.py`

Existing affected test/helper sources: S012, T004, T048, T095. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY001, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY002

**Template package value contracts**

- **Semantic predecessors:** [CY001](planning-execution.md#cy001).
- **Shared-file predecessors:** None.
- **Authority:** [DI-01/02 §§5.1,5.2,7.2](design-suite-resolution.md).
- **CY002.D1 — bounded result:** Introduce pure closed manifest/version/policy values and finite JSON context presence rules. Preserve all active legacy readers and constructor contracts.
- **Preserved behavior:** Absent/empty/null/false/zero distinctions, no materialized defaults; no artifact-ID dispatch.
- **CY002.D2 — independent evidence:** Closed values reject removed/extra fields and invalid identity/version syntax; absent/empty/null/false/zero remain distinct. Legacy lifecycle cases remain until their named retirement.
- **Rollback:** R-CY002: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY002.D1 and CY002.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C060, C085, T061, T062, T063, T090.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/config/schemas/template_suite.py`
- `mcp_server/core/interfaces/template_catalog.py`
- `tests/mcp_server/unit/config/test_template_suite.py`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/config/test_template_suite.py`

Existing affected test/helper sources: T061, T062, T063, T090. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY002, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY003

**Contained JSON Schema preparation**

- **Semantic predecessors:** [CY002](planning-execution.md#cy002).
- **Shared-file predecessors:** None.
- **Authority:** [DI-01/02 §§5.1,5.2,7.2](design-suite-resolution.md).
- **CY003.D1 — bounded result:** Implement contained 2020-12 static reference resolution and authored/resolved admission parity; add explicit ConfigLoader entry without changing active startup readers.
- **Preserved behavior:** Absent/empty/null/false/zero distinctions, no materialized defaults; no artifact-ID dispatch.
- **CY003.D2 — independent evidence:** I-01/04/05/06/08/11; unknown fields, unsupported/dynamic/external/cyclic refs rejected; independent authored/resolved validation parity.
- **Rollback:** R-CY003: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY003.D1 and CY003.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C057, C058, S002, S011, T064, T068, T069, T073.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/services/template_contract_loader.py`
- `tests/mcp_server/unit/services/test_template_contract_loader.py`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/services/test_template_contract_loader.py`
- `tests/mcp_server/unit/utils/test_schema_utils.py`

Existing affected test/helper sources: S011, T064, T068, T069, T073. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY003, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY004

**Parser-supported template dependency graph**

- **Semantic predecessors:** [CY002](planning-execution.md#cy002), [CY003](planning-execution.md#cy003).
- **Shared-file predecessors:** None.
- **Authority:** [DI-01/02 §§5.3–5.5,7.5,10](design-suite-resolution.md).
- **CY004.D1 — bounded result:** Resolve only supported contained Jinja inheritance/import edges; no live renderer or startup selection change.
- **Preserved behavior:** Arbitrary manifest IDs, intended inherited/imported content and actionable startup failures.
- **CY004.D2 — independent evidence:** Independently authored graph fixtures prove missing, ambiguous, cyclic, escaping, dynamic and prohibited lateral edges are rejected; retained literal import/inheritance works.
- **Rollback:** R-CY004: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY004.D1 and CY004.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: T019, T089, T105.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/services/template_graph.py`
- `tests/mcp_server/unit/services/test_template_graph.py`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/services/test_template_graph.py`

Existing affected test/helper sources: T019, T089, T105. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY004, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY005

**Immutable template catalog and renderer selection**

- **Semantic predecessors:** [CY004](planning-execution.md#cy004).
- **Shared-file predecessors:** [CY003](planning-execution.md#cy003), [CY002](planning-execution.md#cy002), [CY001](planning-execution.md#cy001).
- **Authority:** [DI-01/02 §§5.3–5.5,7.5,10](design-suite-resolution.md).
- **CY005.D1 — bounded result:** Compose the admitted schema and dependency graph into an immutable catalog with explicit renderer injection; keep the currently registered legacy tool route intact.
- **Preserved behavior:** Arbitrary manifest IDs, intended inherited/imported content and actionable startup failures.
- **CY005.D2 — independent evidence:** Arbitrary manifest IDs, missing/invalid package failure, intended inherited rendering, selected renderer/introspection equality and restart-stable snapshots; no Python ID registry.
- **Rollback:** R-CY005: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY005.D1 and CY005.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C057, C058, C060, C087, T002, T010, T048, T064, T068, T069, T071, T082, T083, T085, T086, T092.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/services/template_catalog.py`
- `tests/mcp_server/unit/services/test_template_catalog.py`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/services/test_template_catalog.py`

Existing affected test/helper sources: T002, T010, T048, T064, T068, T069, T071, T082, T083, T085, T086, T092. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY005, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY006

**Generation fingerprints and package labels**

- **Semantic predecessors:** [CY004](planning-execution.md#cy004), [CY005](planning-execution.md#cy005).
- **Shared-file predecessors:** None.
- **Authority:** [DI-01/02 §5.6/10](design-suite-resolution.md).
- **CY006.D1 — bounded result:** Implement generation-only pf/sf and independent SemVer labels from admitted sources; no legacy registry writes or historic lookup.
- **Preserved behavior:** Existing generated files untouched; invalid/unrecognized metadata has no selected template.
- **CY006.D2 — independent evidence:** Independent fixed vectors; root/line-ending normalization; exact source inclusion; policy/version exclusion; lateral/transitive effects; four label/fingerprint relations.
- **Rollback:** R-CY006: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY006.D1 and CY006.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: T015, T049, T059, T077.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/services/artifact_identity.py`
- `tests/mcp_server/unit/services/test_artifact_identity.py`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/services/test_artifact_identity.py`

Existing affected test/helper sources: T015, T049, T059, T077. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY006, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY007

**First-line provenance writer and reader**

- **Semantic predecessors:** [CY006](planning-execution.md#cy006).
- **Shared-file predecessors:** None.
- **Authority:** [DI-01/02 §5.6/10](design-suite-resolution.md).
- **CY007.D1 — bounded result:** Implement the pure bounded four-field header reader and shared generation framing; keep existing artifact bytes and live legacy templates unchanged.
- **Preserved behavior:** Existing generated files untouched; invalid/unrecognized metadata has no selected template.
- **CY007.D2 — independent evidence:** Independent expected first-line bytes, maximum bounds/native comment frames, malformed/extra/duplicate/non-first-line rejection and no partial recognition; no lifecycle timestamps.
- **Rollback:** R-CY007: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY007.D1 and CY007.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C107, T013, T050, T051, T052, T065, T088.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/core/interfaces/artifact_header_reader.py`
- `mcp_server/services/artifact_header_reader.py`
- `tests/mcp_server/unit/services/test_artifact_header_reader.py`
- `.pgmcp/template_suite/shared/templates/bases/tier0_root.jinja2`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/services/test_artifact_header_reader.py`

Existing affected test/helper sources: T013, T050, T051, T052, T065, T088. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY007, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY008

**Prepared tool input contract**

- **Semantic predecessors:** [CY002](planning-execution.md#cy002), [CY003](planning-execution.md#cy003).
- **Shared-file predecessors:** [CY007](planning-execution.md#cy007).
- **Authority:** [Shared §§5.4–5.5; DI-01/02 §7.2](design-shared-contracts.md).
- **CY008.D1 — bounded result:** Introduce the immutable prepared input contract and explicit admitted-schema entrypoint. Preserve current tool constructors and schema behavior for their existing inputs.
- **Preserved behavior:** Unaffected typed tools, enforcement skip/error behavior and whole-tool schema identity.
- **CY008.D2 — independent evidence:** One supplied contract governs exposure and real admission; strict unknown fields, schema://validation and unaffected existing tools remain consistent.
- **Rollback:** R-CY008: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY008.D1 and CY008.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C085, C107, S001, S009, S025, S026.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/core/interfaces/tool_input_contract.py`
- `tests/mcp_server/integration/test_prepared_tool_contract.py`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/test_prepared_tool_contract.py`

Existing affected test/helper sources: S009. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY008, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY009

**Operation and attachment transport**

- **Semantic predecessors:** [CY008](planning-execution.md#cy008).
- **Shared-file predecessors:** [CY001](planning-execution.md#cy001).
- **Authority:** [Shared §§5.4–5.5; DI-01/02 §7.2](design-shared-contracts.md).
- **CY009.D1 — bounded result:** Normalize existing operation-only returns once into the designed internal carrier; add attachments and real wrapper/server transport without changing existing public tool input vocabulary. Switch only the resource-presenter injection in the normal bootstrap alongside the carrier; replace obsolete ValidationResourcePresenter and all its imports in this same coherent cycle.
- **Preserved behavior:** Unaffected typed tools, enforcement skip/error behavior and whole-tool schema identity. Whole-tool ValidationErrorOutput.input_schema stays unchanged in its operation/cache. New attachment presentation is generic and does not dispatch on DTO/error type.
- **CY009.D2 — independent evidence:** Real wrappers prove one normalization, unchanged operational facts, correct empty/nonempty attachments, error and enforcement skip behavior, MCP isError and unrelated server/cycle behavior. A short-lived normal legacy startup still serves its current contracts.
- **Rollback:** R-CY009: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY009.D1 and CY009.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Readback prerequisite supplement: [R001–R008](planning-path-ownership.md#readback-prerequisite-supplement). Adapt R003/R004/R006 only at the shared transport boundary. Preserve complete planning reads and all unrelated project command semantics; review R001/R002/R007/R008 without edits. D1/D2 and this cycle's R-CY009, preserved behavior and independent stop/go apply to these exact additional seams.

Existing source IDs: C055, C085, C086, S001, S003, S007, S009, S013, S025, S026, S027, S028, S029, S043, S044, S045, S046, S047, S053, S054, S055, S056, T091, T097, T098, R003, R004, R006.

Read-only review/preservation IDs: S052, R001, R002, R007, R008. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/core/tool_execution.py`
- `mcp_server/presenters/schema_resource_presenter.py`
- `tests/mcp_server/integration/test_tool_attachment_transport.py`

Previously introduced paths revisited in this cycle:

None.

- Add carrier/attachment capability while retaining currently exposed old output models and fields for the normal legacy assembly. Target operation DTOs live separately; removal of legacy output/schema fields is not performed against active old callers.
- This shared transport migration affects the existing server pipeline and must pass a normal legacy startup/handshake before commit. C055/T091 writes here are limited to presenter injection and its regression; final target assembly/config dispatch remains reserved for rollout.

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

Existing affected test/helper sources: S007, S009, S013, S044, S054, S055, T091, T097, T098. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY009, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY010

**Required-null cache fidelity**

- **Semantic predecessors:** [CY008](planning-execution.md#cy008), [CY009](planning-execution.md#cy009).
- **Shared-file predecessors:** [CY009](planning-execution.md#cy009).
- **Authority:** [Shared §§5.6,10,12](design-shared-contracts.md).
- **CY010.D1 — bounded result:** Schema-aware operation cache serialization and resource delivery; no presentation changes.
- **Preserved behavior:** Required-null/variant facts, unrelated cached error DTOs, cache FIFO and publisher/read separation; attachments remain separate.
- **CY010.D2 — independent evidence:** Real resource reads retain required null and nested variants; same complete operation survives roundtrip; existing FIFO and matching/read semantics retained.
- **Rollback:** R-CY010: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY010.D1 and CY010.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Readback prerequisite supplement: [R001–R008](planning-path-ownership.md#readback-prerequisite-supplement). Adapt R006 only to the cache serialization boundary; preserve full/default reads, bounded Unicode windows, hash consistency, explicit EOF and cache-miss rejection in S010/S030/R007/R008. D1/D2 and this cycle's R-CY010, preserved behavior and independent stop/go apply to these exact additional seams.

Existing source IDs: C041, C086, S010, S030, S031, S032, S043, S044, T134, T136, T141, T149, R006.

Read-only review/preservation IDs: R003, R004, R007, R008. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `tests/mcp_server/integration/test_cache_fidelity_v3.py`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/test_project_plan_readback.py`
- `tests/mcp_server/integration/test_cache_fidelity_v3.py`

Existing affected test/helper sources: S010, S032, S044, T134, T136, T141, T149. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY010, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY011

**Generic bounded presentation**

- **Semantic predecessors:** [CY008](planning-execution.md#cy008), [CY009](planning-execution.md#cy009), [CY010](planning-execution.md#cy010).
- **Shared-file predecessors:** None.
- **Authority:** [Shared §§5.6,11.1](design-shared-contracts.md).
- **CY011.D1 — bounded result:** Generic Annotated/nullable scalar and enum admission with explicit null guard; bounded declarative text only. Session-approved refinement (2026-09-17): retain a short cache URI on all cached results and show a short reference to `pgmcp://docs/cache-reading` only when the canonical complete JSON exceeds the configured read budget. The packaged reference owns the unchanged window/integrity/safe-retry instructions. No session-read tracking or pagination protocol change.
- **Preserved behavior:** Existing collection/container shape rules, ordering, byte budgets and unsupported model-union rejection; no DTO/native/error-class dispatch.
- **CY011.D2 — independent evidence:** Actual configured rows accept approved strict/nullable shapes and reject unsafe structures; null enum has no block; unaffected tool text keeps existing bounds. Adapt the existing presentation cases to prove small results omit pagination guidance and large complete results retain the short guide link within text budgets; follow that link through the registered MCP resource. Reuse existing window/reassembly/truncation/cache-loss evidence. Session-approved bounded patch on the current branch; no separate issue or cycle.
- **Rollback:** R-CY011: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY011.D1 and CY011.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C085, C086, C106, S003, S004, S005, S006, S007, S042, T072, T097, T131, T132, T134, T136, T141, T149.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `tests/mcp_server/integration/test_execution_presentation_v3.py`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/test_execution_presentation_v3.py`

Existing affected test/helper sources: S006, S007, T072, T097, T131, T132, T134, T136, T141, T149. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY011, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY012

**Adapter package admission and trust**

- **Semantic predecessors:** [CY001](planning-execution.md#cy001).
- **Shared-file predecessors:** [CY005](planning-execution.md#cy005), [CY008](planning-execution.md#cy008), [CY003](planning-execution.md#cy003), [CY009](planning-execution.md#cy009).
- **Authority:** [DI-05 §§7.3–7.4.3](design-execution-adapters.md).
- **CY012.D1 — bounded result:** Immutable role-versioned manifests/catalog, contained files, package identity and explicit workspace trust.
- **Preserved behavior:** No startup execution/native survey; duplicate IDs fail; one official/workspace catalog.
- **CY012.D2 — independent evidence:** TEST-E02/03; invalid manifests/entrypoints/trust/role references rejected; relocated package fingerprint stable; pure injected readers.
- **Rollback:** R-CY012: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY012.D1 and CY012.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C057, C058, C060, C107, S037, T048, T064, T068, T073, T091, T109, T110.

Read-only review/preservation IDs: C055, C063. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/config/schemas/adapter_manifest.py`
- `mcp_server/core/interfaces/execution.py`
- `mcp_server/execution/catalog.py`
- `tests/mcp_server/unit/execution/test_catalog.py`
- `mcp_server/execution/__init__.py`
- `mcp_server/bundled_adapters/__init__.py`
- `.pgmcp/config/adapters.yaml`
- `mcp_server/execution/contracts/check_v1.schema.json`
- `mcp_server/execution/contracts/test_v1.schema.json`
- `mcp_server/execution/contracts/fix_v1.schema.json`

Previously introduced paths revisited in this cycle:

None.

- The listed legacy review-only paths retain their current constructors, runtime reads and normal registration. New behavior is exercised through the separately named final internal components; no V2/V3 ToolAssembly union, public alias, fallback reader or constructor mode.
- Author the approved adapter trust declaration before activation; the legacy startup does not read it. The three distinct role schemas are versioned wire contracts, not generic native-result parsers.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/execution/test_catalog.py`

Existing affected test/helper sources: T048, T064, T068, T073, T091, T109, T110. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY012, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY013

**Adapter process protocol**

- **Semantic predecessors:** [CY012](planning-execution.md#cy012).
- **Shared-file predecessors:** None.
- **Authority:** [DI-05 §7.13](design-execution-adapters.md).
- **CY013.D1 — bounded result:** Generic launch/JSON transport, typed attempted outcomes and ProcessCapture; add controlled process support.
- **Preserved behavior:** No native/language parser in generic runtime; valid domain failures differ from protocol failure.
- **CY013.D2 — independent evidence:** TEST-E03/04; direct non-Python fixture, stdout/stderr/oversize/malformed/crash/launch errors and package evidence independently observed.
- **Rollback:** R-CY013: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY013.D1 and CY013.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C107, T110, T115, T128.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/execution/protocol.py`
- `mcp_server/execution/process_runtime.py`
- `tests/mcp_server/fixtures/adapter_process.py`
- `tests/mcp_server/integration/execution/test_process_runtime.py`
- `mcp_server/execution/models.py`

Previously introduced paths revisited in this cycle:

- `mcp_server/core/interfaces/execution.py`

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/execution/test_process_runtime.py`

Existing affected test/helper sources: T110, T115, T128. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY013, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY014

**Bounded process stopping**

- **Semantic predecessors:** [CY013](planning-execution.md#cy013).
- **Shared-file predecessors:** None.
- **Authority:** [DI-05 §7.13; DI-08 §7.5](design-execution-adapters.md).
- **CY014.D1 — bounded result:** Add deadline/cancel/descendant stopping to the generic process runtime, retaining typed invocation/capture facts.
- **Preserved behavior:** Logical target remains unchanged/absent; cleanup warning cannot overwrite primary result; unconfirmed termination blocks dependent mutation.
- **CY014.D2 — independent evidence:** Real supported-OS processes prove timeout, cancellation, descendant stopping, stream bounds and rejection of late results; no mocked-only process certificate.
- **Rollback:** R-CY014: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY014.D1 and CY014.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: T128.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `tests/mcp_server/integration/execution/test_process_stopping.py`

Previously introduced paths revisited in this cycle:

- `mcp_server/execution/process_runtime.py`
- `mcp_server/execution/protocol.py`

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/execution/test_process_stopping.py`

Existing affected test/helper sources: T128. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY014, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY015

**Proposed-content input and scratch lifecycle**

- **Semantic predecessors:** [CY014](planning-execution.md#cy014).
- **Shared-file predecessors:** [CY012](planning-execution.md#cy012).
- **Authority:** [DI-05 §7.13; DI-08 §7.5](design-execution-adapters.md).
- **CY015.D1 — bounded result:** Add direct-content and unique temp/validation file routes with intended logical target and separately reported cleanup.
- **Preserved behavior:** Logical target remains unchanged/absent; cleanup warning cannot overwrite primary result; unconfirmed termination blocks dependent mutation.
- **CY015.D2 — independent evidence:** Complete supplied text, logical target, no authoritative target overwrite, unique ownership, temp/artifacts separation and cleanup-warning preservation; physical scratch is never the content policy.
- **Rollback:** R-CY015: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY015.D1 and CY015.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: S037.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/execution/content_input.py`
- `tests/mcp_server/integration/execution/test_content_input.py`

Previously introduced paths revisited in this cycle:

- `mcp_server/execution/process_runtime.py`

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/execution/test_content_input.py`

Existing affected test/helper sources: None. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY015, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY016

**Check bindings and output profiles**

- **Semantic predecessors:** [CY012](planning-execution.md#cy012).
- **Shared-file predecessors:** [CY013](planning-execution.md#cy013).
- **Authority:** [DI-05 §§7.5,7.14,7.16–7.17](design-execution-adapters.md).
- **CY016.D1 — bounded result:** Add pure check/profile configuration and catalog-reference validation to explicit new loader methods; no active quality.yaml dual read.
- **Preserved behavior:** Configured [] differs from empty branch; no .py filter, auto replay or hidden main fallback.
- **CY016.D2 — independent evidence:** Closed config, nonempty obligations, role/capability references, explicit defaults and configured arguments admitted consistently; fixes/tests cannot enter check profiles.
- **Rollback:** R-CY016: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY016.D1 and CY016.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C057, C058, C060, C107, T064, T109, T110.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/config/schemas/checks_config.py`
- `tests/mcp_server/unit/config/test_checks_config.py`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/config/test_checks_config.py`

Existing affected test/helper sources: T064, T109, T110. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY016, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY017

**Explicit check selection and branch scopes**

- **Semantic predecessors:** [CY016](planning-execution.md#cy016).
- **Shared-file predecessors:** [CY014](planning-execution.md#cy014).
- **Authority:** [DI-05 §§7.5,7.14,7.16–7.17](design-execution-adapters.md).
- **CY017.D1 — bounded result:** Implement required explicit scopes, ordered binding selection, native argument replacement and Git-owned branch target derivation.
- **Preserved behavior:** Configured [] differs from empty branch; no .py filter, auto replay or hidden main fallback.
- **CY017.D2 — independent evidence:** I-16/19; invalid role/profile/args selection before launch; rename/deletion/working changes and Git failure vs empty selection; no check-state access.
- **Rollback:** R-CY017: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY017.D1 and CY017.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: T107, T111, T117, T128, T145, T150.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/execution/check_selection.py`
- `tests/mcp_server/unit/execution/test_check_selection.py`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/execution/test_check_selection.py`

Existing affected test/helper sources: T107, T111, T117, T128, T145, T150. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY017, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY018

**Python syntax check adapter**

- **Semantic predecessors:** [CY014](planning-execution.md#cy014), [CY015](planning-execution.md#cy015).
- **Shared-file predecessors:** None.
- **Authority:** [DI-05 §7.20 A/B/F](design-execution-adapters.md).
- **CY018.D1 — bounded result:** python_syntax check/v1 package and direct content conformance.
- **Preserved behavior:** ast.parse syntax only; unchanged text/filename; no generated-model/example execution.
- **CY018.D2 — independent evidence:** Valid/invalid complete text, no import/execution, bad args, runtime provenance; declared dependency behavior independently exercised.
- **Rollback:** R-CY018: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY018.D1 and CY018.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: T142, T143.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/bundled_adapters/python_syntax/manifest.yaml`
- `mcp_server/bundled_adapters/python_syntax/check.py`
- `mcp_server/bundled_adapters/python_syntax/requirements.txt`
- `tests/mcp_server/integration/adapters/test_python_syntax.py`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/adapters/test_python_syntax.py`

Existing affected test/helper sources: T142, T143. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY018, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY019

**Markdown preflight adapter**

- **Semantic predecessors:** [CY014](planning-execution.md#cy014), [CY015](planning-execution.md#cy015).
- **Shared-file predecessors:** None.
- **Authority:** [DI-05 §7.20 A–C/F](design-execution-adapters.md).
- **CY019.D1 — bounded result:** Extract document/body checks behind check/v1 without importing old validator stack.
- **Preserved behavior:** H1 anywhere, H2 body, warning-only local missing links, schemes/anchors/fragments/images and intended-parent resolution.
- **CY019.D2 — independent evidence:** Positive and negative fixtures prove precise retained observations and no stronger implicit lint; source bytes unchanged.
- **Rollback:** R-CY019: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY019.D1 and CY019.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: None.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/bundled_adapters/markdown_preflight/manifest.yaml`
- `mcp_server/bundled_adapters/markdown_preflight/check.py`
- `mcp_server/bundled_adapters/markdown_preflight/requirements.txt`
- `tests/mcp_server/integration/adapters/test_markdown_preflight.py`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/adapters/test_markdown_preflight.py`

Existing affected test/helper sources: None. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY019, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY020

**Ruff checks and native configuration**

- **Semantic predecessors:** [CY013](planning-execution.md#cy013), [CY016](planning-execution.md#cy016), [CY017](planning-execution.md#cy017).
- **Shared-file predecessors:** [CY018](planning-execution.md#cy018).
- **Authority:** [DI-05 §7.20 B/E/F](design-execution-adapters.md).
- **CY020.D1 — bounded result:** Ruff check format/lint roles and approved native settings migration in isolated fixtures; author target defaults separately. Edit only pyproject.toml tool.ruff sections in this cycle; preserve unrelated project/build/test settings.
- **Preserved behavior:** No check writes; line-length=100/py311; record approved stricter ignores removal and drop-isolated difference.
- **CY020.D2 — independent evidence:** Direct native vs adapter same-version input evidence; no-fix/source-switch refusal; 0/1/inability/notes; exact targets; changing native config affects results.
- **Rollback:** R-CY020: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY020.D1 and CY020.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C006, T115, T121, T122, T128, T143.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/bundled_adapters/ruff/manifest.yaml`
- `mcp_server/bundled_adapters/ruff/check.py`
- `mcp_server/bundled_adapters/ruff/requirements.txt`
- `tests/mcp_server/integration/adapters/test_ruff_checks.py`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/adapters/test_ruff_checks.py`

Existing affected test/helper sources: T115, T121, T122, T128, T143. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY020, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY021

**Mypy check and native configuration**

- **Semantic predecessors:** [CY013](planning-execution.md#cy013), [CY016](planning-execution.md#cy016), [CY017](planning-execution.md#cy017).
- **Shared-file predecessors:** [CY020](planning-execution.md#cy020).
- **Authority:** [DI-05 §7.20 B/E/F](design-execution-adapters.md).
- **CY021.D1 — bounded result:** Mypy check adapter and approved strict native defaults, with tests.* override. Edit only tool.mypy sections in this cycle.
- **Preserved behavior:** Remove blanket missing-import suppression; explicit tests/workspace selection can widen coverage as approved.
- **CY021.D2 — independent evidence:** Direct native/adapter failures, notes, configured files vs literal targets, import behavior and native settings change; no generic regex parser.
- **Rollback:** R-CY021: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY021.D1 and CY021.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C006, T115, T124, T128, T143.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/bundled_adapters/mypy/manifest.yaml`
- `mcp_server/bundled_adapters/mypy/check.py`
- `mcp_server/bundled_adapters/mypy/requirements.txt`
- `tests/mcp_server/integration/adapters/test_mypy.py`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/adapters/test_mypy.py`

Existing affected test/helper sources: T115, T124, T128, T143. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY021, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY022

**Pyright check and native configuration**

- **Semantic predecessors:** [CY013](planning-execution.md#cy013), [CY016](planning-execution.md#cy016), [CY017](planning-execution.md#cy017).
- **Shared-file predecessors:** [CY021](planning-execution.md#cy021), [CY020](planning-execution.md#cy020).
- **Authority:** [DI-05 §7.20 B/E/F](design-execution-adapters.md).
- **CY022.D1 — bounded result:** Implement the Node Pyright adapter and workspace module resolution. Apply only the DI-05-approved Python 3.11/Windows settings in pyrightconfig.json, retaining diagnostic toggles/execution environments. Prove the preserved values with and without the duplicate [tool.pyright] section on isolated configuration copies. Do not edit pyproject.toml here; CY072 alone owns deletion of [tool.pyright].
- **Preserved behavior:** Native JSON/text severity/location facts, explicit --warnings and the effective legacy MCP target remain unchanged. The approved editor Python-target change belongs to this cycle; the live duplicate TOML section remains byte-for-byte intact until CY072.
- **CY022.D2 — independent evidence:** Direct native/adapter output modes, exits and missing dependencies; no synthetic findings or severity remapping. Compare actual effective native settings before/after duplicate removal on isolated copies, including reportFunctionMemberAccess=false, Python 3.11/Windows, diagnostic toggles and warning handling. Prove the working legacy call still resolves its approved settings; record the source/config/native-version evidence for CY070.
- **Rollback:** R-CY022: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY022.D1 and CY022.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: S008, T115, T116, T120, T121, T122, T125, T128, T143.

Read-only review/preservation IDs: C006. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/bundled_adapters/pyright/manifest.yaml`
- `mcp_server/bundled_adapters/pyright/check.cjs`
- `mcp_server/bundled_adapters/pyright/package.json`
- `tests/mcp_server/integration/adapters/test_pyright.py`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/adapters/test_pyright.py`

Existing affected test/helper sources: T115, T116, T120, T121, T122, T125, T128, T143. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY022, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY023

**TypeScript syntax adapter**

- **Semantic predecessors:** [CY014](planning-execution.md#cy014), [CY015](planning-execution.md#cy015).
- **Shared-file predecessors:** None.
- **Authority:** [DI-05 §7.20 A/B/F](design-execution-adapters.md).
- **CY023.D1 — bounded result:** Node Language Service in-memory syntax check and workspace-native resolution.
- **Preserved behavior:** No emit or semantic/import-availability checking; target may not exist.
- **CY023.D2 — independent evidence:** Valid/invalid syntax with missing imports; target absent before/after; invalid config and runtime/module absence distinct.
- **Rollback:** R-CY023: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY023.D1 and CY023.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: None.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/bundled_adapters/typescript_syntax/manifest.yaml`
- `mcp_server/bundled_adapters/typescript_syntax/check.cjs`
- `mcp_server/bundled_adapters/typescript_syntax/package.json`
- `tests/mcp_server/integration/adapters/test_typescript_syntax.py`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/adapters/test_typescript_syntax.py`

Existing affected test/helper sources: None. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY023, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY024

**Commit message adapter**

- **Semantic predecessors:** [CY006](planning-execution.md#cy006), [CY007](planning-execution.md#cy007), [CY014](planning-execution.md#cy014), [CY015](planning-execution.md#cy015).
- **Shared-file predecessors:** None.
- **Authority:** [DI-05 §7.20 B/E/F; DI-03 documents §7.6](design-document-tracking-artifacts.md).
- **CY024.D1 — bounded result:** commitlint adapter consumes installed pure header reader; minimal conventional rules and native config.
- **Preserved behavior:** Arbitrary type/case, multiline body/footer, marker-only breaking intent; strip only valid header; no Git publication.
- **CY024.D2 — independent evidence:** Known valid/invalid messages/headers and native overrides; no copied grammar or Git-tool enum authority; missing dependencies truthful.
- **Rollback:** R-CY024: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY024.D1 and CY024.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: None.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/bundled_adapters/commitlint/manifest.yaml`
- `mcp_server/bundled_adapters/commitlint/check.py`
- `mcp_server/bundled_adapters/commitlint/package.json`
- `mcp_server/bundled_adapters/commitlint/requirements.txt`
- `tests/mcp_server/integration/adapters/test_commitlint.py`
- `commitlint.config.cjs`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/adapters/test_commitlint.py`

Existing affected test/helper sources: None. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY024, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY025

**Lychee content and selection adapter**

- **Semantic predecessors:** [CY014](planning-execution.md#cy014), [CY015](planning-execution.md#cy015), [CY016](planning-execution.md#cy016), [CY017](planning-execution.md#cy017).
- **Shared-file predecessors:** None.
- **Authority:** [DI-05 §§7.13,7.20 B/C/F](design-execution-adapters.md).
- **CY025.D1 — bounded result:** Native links adapter with scratch logical base/self-remap, optional stronger profile.
- **Preserved behavior:** Broken links fail; no default mutation-profile broadening; authoritative target unchanged.
- **CY025.D2 — independent evidence:** Native supported-version self/TOC/neighbor positive/negative cases; native settings and literal target behavior; no fictitious availability pass.
- **Rollback:** R-CY025: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY025.D1 and CY025.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: None.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/bundled_adapters/lychee/manifest.yaml`
- `mcp_server/bundled_adapters/lychee/check.py`
- `mcp_server/bundled_adapters/lychee/dependencies.json`
- `tests/mcp_server/integration/adapters/test_lychee.py`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/adapters/test_lychee.py`

Existing affected test/helper sources: None. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY025, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY026

**Internal check orchestration**

- **Semantic predecessors:** [CY016](planning-execution.md#cy016), [CY017](planning-execution.md#cy017), [CY018](planning-execution.md#cy018), [CY019](planning-execution.md#cy019), [CY020](planning-execution.md#cy020), [CY021](planning-execution.md#cy021), [CY022](planning-execution.md#cy022), [CY023](planning-execution.md#cy023), [CY024](planning-execution.md#cy024), [CY025](planning-execution.md#cy025).
- **Shared-file predecessors:** [CY012](planning-execution.md#cy012), [CY011](planning-execution.md#cy011), [CY013](planning-execution.md#cy013).
- **Authority:** [DI-05 §§7.14,7.19–7.20](design-execution-adapters.md).
- **CY026.D1 — bounded result:** Shared factual check executor; explicit selection and mutation-profile consumers use same bindings.
- **Preserved behavior:** Mixed failed/unavailable/not-executed evidence, args/defaults, native facts and no auto-state/fix side effects.
- **CY026.D2 — independent evidence:** Direct role doubles prove reductions and empty branch; real configured renamed/recomposed profile invokes intended adapter; no whole-workspace fallback.
- **Rollback:** R-CY026: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY026.D1 and CY026.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: T048, T107, T115, T117, T128, T131, T133, T142.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/execution/check_service.py`
- `tests/mcp_server/unit/execution/test_check_service.py`
- `tests/mcp_server/integration/execution/test_check_profiles.py`
- `.pgmcp/config/checks.yaml`

Previously introduced paths revisited in this cycle:

- `mcp_server/execution/models.py`

- Author the approved configurable startset/default profiles here; exact logical-target/native behavior follows DI-05 §7.20. Existing V2 startup keeps its single quality configuration reader until cutover.
- Selection, native facts, capture and role results keep their own declared contracts; do not normalize check/test/fix into one success reducer.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/execution/test_check_service.py`
- `tests/mcp_server/integration/execution/test_check_profiles.py`

Existing affected test/helper sources: T048, T107, T115, T117, T128, T131, T133, T142. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY026, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY027

**Pytest adapter and native settings**

- **Semantic predecessors:** [CY013](planning-execution.md#cy013), [CY014](planning-execution.md#cy014), [CY015](planning-execution.md#cy015).
- **Shared-file predecessors:** [CY021](planning-execution.md#cy021), [CY026](planning-execution.md#cy026).
- **Authority:** [DI-05 §§7.15,7.20 B/E/F](design-execution-adapters.md).
- **CY027.D1 — bounded result:** test/v1 Pytest package, scoped recording double and declared native test/coverage defaults. Edit only native Pytest/coverage sections of pyproject.toml; no default coverage binding.
- **Preserved behavior:** Collection/failure/skip/no-tests=passed, LF/CRLF, --lf, verbosity, xdist; source=mcp_server and coverage 90 only on request.
- **CY027.D2 — independent evidence:** Direct Pytest and adapter fixtures cover native outcomes/options/coverage rejection and descendant stopping; no old scalar DTO/verbose cap.
- **Rollback:** R-CY027: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY027.D1 and CY027.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C006, T048, T106, T127, T140.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/bundled_adapters/pytest/manifest.yaml`
- `mcp_server/bundled_adapters/pytest/test.py`
- `mcp_server/bundled_adapters/pytest/requirements.txt`
- `tests/mcp_server/fixtures/test_role_double.py`
- `tests/mcp_server/integration/adapters/test_pytest.py`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/fixtures/test_role_double.py`
- `tests/mcp_server/integration/adapters/test_pytest.py`

Existing affected test/helper sources: T048, T106, T127, T140. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY027, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY028

**Internal test orchestration**

- **Semantic predecessors:** [CY027](planning-execution.md#cy027).
- **Shared-file predecessors:** [CY016](planning-execution.md#cy016), [CY026](planning-execution.md#cy026).
- **Authority:** [DI-05 §§7.15–7.17](design-execution-adapters.md).
- **CY028.D1 — bounded result:** Pure tests.yaml models and framework-neutral test service with configured/workspace/targets selection.
- **Preserved behavior:** No Pytest option knowledge in generic server; empty native selection and complete typed results remain distinct.
- **CY028.D2 — independent evidence:** Native proof from CY027 plus public service selection/result matrix, invalid inputs and declared null/variant semantics.
- **Rollback:** R-CY028: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY028.D1 and CY028.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C057, C058, C060, C107, T048, T064, T106, T109, T110, T127, T137, T140.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/config/schemas/tests_config.py`
- `mcp_server/execution/test_service.py`
- `tests/mcp_server/unit/execution/test_test_service.py`
- `.pgmcp/config/tests.yaml`

Previously introduced paths revisited in this cycle:

- `mcp_server/execution/models.py`

- Selection, native facts, capture and role results keep their own declared contracts; do not normalize check/test/fix into one success reducer.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/execution/test_test_service.py`

Existing affected test/helper sources: T048, T064, T106, T109, T110, T127, T137, T140. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY028, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY029

**Ruff native fix conformance**

- **Semantic predecessors:** [CY020](planning-execution.md#cy020).
- **Shared-file predecessors:** [CY011](planning-execution.md#cy011).
- **Authority:** [DI-05 §§7.18,7.20 B/F](design-execution-adapters.md).
- **CY029.D1 — bounded result:** Add fix/v1 Ruff entrypoints and explicit addresses relations; separately prove native source mutation.
- **Preserved behavior:** Only admitted explicit existing files; residual lint can fail after writing; no automatic recheck/rollback.
- **CY029.D2 — independent evidence:** Observe native bytes independently, unsupported/source-expanding args refusal, no-change success and partial failure; recheck shared Ruff package check conformance after manifest/fingerprint change.
- **Rollback:** R-CY029: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY029.D1 and CY029.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: T112, T136.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/bundled_adapters/ruff/fix.py`
- `tests/mcp_server/integration/adapters/test_ruff_fixes.py`

Previously introduced paths revisited in this cycle:

- `mcp_server/bundled_adapters/ruff/manifest.yaml`
- `mcp_server/bundled_adapters/ruff/requirements.txt`

- The Ruff manifest is a revisited path created by CY020. Its role/address additions change the whole package fingerprint and invalidate affected check identity/conformance evidence; rerun that bounded evidence.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/adapters/test_ruff_fixes.py`

Existing affected test/helper sources: T112, T136. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY029, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY030

**Internal fix orchestration**

- **Semantic predecessors:** [CY029](planning-execution.md#cy029).
- **Shared-file predecessors:** [CY028](planning-execution.md#cy028).
- **Authority:** [DI-05 §7.18](design-execution-adapters.md).
- **CY030.D1 — bounded result:** fixes.yaml and files-only ordered fix service; full admission before first launch.
- **Preserved behavior:** Caller order, first non-success stops later fixes; earlier/attempted writes may remain; no required prior check or clean worktree.
- **CY030.D2 — independent evidence:** Typed fake plus native 3-step case: first writes, second fails after write, third unstarted; timeout/cancel/invalid response; no hidden Git/check/rollback.
- **Rollback:** R-CY030: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY030.D1 and CY030.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C057, C058, C060, C107, T048, T064, T109, T110, T112, T136.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/config/schemas/fixes_config.py`
- `mcp_server/execution/fix_service.py`
- `tests/mcp_server/unit/execution/test_fix_service.py`
- `.pgmcp/config/fixes.yaml`

Previously introduced paths revisited in this cycle:

- `mcp_server/execution/models.py`

- Selection, native facts, capture and role results keep their own declared contracts; do not normalize check/test/fix into one success reducer.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/execution/test_fix_service.py`

Existing affected test/helper sources: T048, T064, T109, T110, T112, T136. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY030, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.
