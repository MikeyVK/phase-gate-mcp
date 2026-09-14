# Issue 460 Planning — Artifacts and mutation

Status: DRAFT, producer planning. [Hub](planning.md) defines the binding verification/recovery rules and semantic coverage. [Path index](planning-path-ownership.md) expands every exact source ID. No implementation evidence or independent approval is claimed here.

## CY031

**Shared Python generation sources**

- **Semantic predecessors:** [CY004](planning-execution.md#cy004), [CY005](planning-execution.md#cy005), [CY006](planning-execution.md#cy006), [CY007](planning-execution.md#cy007).
- **Shared-file predecessors:** None.
- **Authority:** [DI-03 code §§7.2–7.7,7.9](design-code-test-artifacts.md).
- **CY031.D1 — bounded result:** Portable shared Python bases/import/signature/field/testing definitions used by next family cycles.
- **Preserved behavior:** Caller owns imports, defaults, bodies where allowed; no project-specific lifecycle or inferred markers.
- **CY031.D2 — independent evidence:** CODE-E02/03/04/05/07/10 against isolated consumer roots; no generated passing placeholders or schema oracle duplication.
- **Rollback:** R-CY031: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY031.D1 and CY031.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C087, T031, T036, T037, T038, T039, T041, T056.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `tests/mcp_server/integration/templates/test_shared_python.py`
- `.pgmcp/template_suite/shared/definitions/python.schema.json`
- `.pgmcp/template_suite/shared/templates/bases/tier1_code.jinja2`
- `.pgmcp/template_suite/shared/templates/bases/tier2_python.jinja2`
- `.pgmcp/template_suite/shared/templates/bases/tier2_typescript.jinja2`
- `.pgmcp/template_suite/shared/templates/patterns/python/imports.jinja2`
- `.pgmcp/template_suite/shared/templates/patterns/python/signatures.jinja2`
- `.pgmcp/template_suite/shared/templates/patterns/python/pydantic.jinja2`
- `.pgmcp/template_suite/shared/templates/patterns/python/logging.jinja2`
- `.pgmcp/template_suite/shared/templates/patterns/testing/pytest.jinja2`

The Python definition path completes the shared-record prerequisite already required by
CY031.D1 and DI-03 §7.9. Independent QA confirmed this bounded inventory correction during
implementation under the user's standing authorization. It adds no contract or strategy;
concrete-package restrictions remain with CY032 onward. The pre-cycle baseline is
`d121a1a7cb4423348a3d60d66f6d1a7476d0b6c9`; the definition file was absent there and its
cycle-owned addition belongs to the same scoped inverse diff.

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/templates/test_shared_python.py`

Existing affected test/helper sources: T031, T036, T037, T038, T039, T041, T056. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY031, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY032

**Pydantic DTO artifact**

- **Semantic predecessors:** [CY018](planning-execution.md#cy018), [CY031](planning-artifacts-mutation.md#cy031).
- **Shared-file predecessors:** None.
- **Authority:** [DI-03 code §§7.1,7.4](design-code-test-artifacts.md).
- **CY032.D1 — bounded result:** Migrate only the python_pydantic_dto concrete package: manifest, version, policy, finite context schema and renderer together. Shared definitions are consumed, not copied into generic Python.
- **Preserved behavior:** DTO immutable and examples for nonempty fields; config explicit frozen/extra policy and optional examples; no semantic example execution.
- **CY032.D2 — independent evidence:** CODE-E01/03/04/09/10; empty and populated, required description, exact defaults/factories and rejected old context. Limit the family matrix to python_pydantic_dto; the paired family's evidence is independently required in its own cycle.
- **Rollback:** R-CY032: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY032.D1 and CY032.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: T009, T017, T023, T038, T054.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `.pgmcp/template_suite/python_pydantic_dto/manifest.yaml`
- `.pgmcp/template_suite/python_pydantic_dto/.version`
- `.pgmcp/template_suite/python_pydantic_dto/policy.yaml`
- `.pgmcp/template_suite/python_pydantic_dto/context.schema.json`
- `.pgmcp/template_suite/python_pydantic_dto/template.jinja2`
- `tests/mcp_server/integration/templates/test_python_pydantic_dto.py`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/templates/test_python_pydantic_dto.py`

Existing affected test/helper sources: T009, T017, T023, T038, T054. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY032, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY033

**Pydantic configuration artifact**

- **Semantic predecessors:** [CY018](planning-execution.md#cy018), [CY031](planning-artifacts-mutation.md#cy031).
- **Shared-file predecessors:** [CY032](planning-artifacts-mutation.md#cy032).
- **Authority:** [DI-03 code §§7.1,7.4](design-code-test-artifacts.md).
- **CY033.D1 — bounded result:** Migrate only the python_pydantic_config concrete package: manifest, version, policy, finite context schema and renderer together. Shared definitions are consumed, not copied into generic Python.
- **Preserved behavior:** DTO immutable and examples for nonempty fields; config explicit frozen/extra policy and optional examples; no semantic example execution.
- **CY033.D2 — independent evidence:** CODE-E01/03/04/09/10; empty and populated, required description, exact defaults/factories and rejected old context. Limit the family matrix to python_pydantic_config; the paired family's evidence is independently required in its own cycle.
- **Rollback:** R-CY033: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY033.D1 and CY033.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: T009, T017, T023, T038, T054.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `.pgmcp/template_suite/python_pydantic_config/manifest.yaml`
- `.pgmcp/template_suite/python_pydantic_config/.version`
- `.pgmcp/template_suite/python_pydantic_config/policy.yaml`
- `.pgmcp/template_suite/python_pydantic_config/context.schema.json`
- `.pgmcp/template_suite/python_pydantic_config/template.jinja2`
- `tests/mcp_server/integration/templates/test_python_pydantic_config.py`

Previously introduced paths revisited in this cycle:

- `.pgmcp/template_suite/shared/definitions/python.schema.json`
- `.pgmcp/template_suite/python_pydantic_dto/context.schema.json`

Independent QA identified these two bounded prerequisites to keep the Pydantic field-name
restriction authoritative in the shared ModelField consumed by both families. This is
authorized under the standing proportional QA-correction rule; it preserves DTO acceptance
and adds no runtime semantics. R-CY033 is `957b1db23d16e06673ebfaba7ca3481842651917`;
both existing files were clean and their cycle-owned inverse diff is the recovery route.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/templates/test_python_pydantic_config.py`

Existing affected test/helper sources: T009, T017, T023, T038, T054. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY033, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY034

**Plain Python class artifact**

- **Semantic predecessors:** [CY018](planning-execution.md#cy018), [CY031](planning-artifacts-mutation.md#cy031).
- **Shared-file predecessors:** [CY033](planning-artifacts-mutation.md#cy033).
- **Authority:** [DI-03 code §7.5](design-code-test-artifacts.md).
- **CY034.D1 — bounded result:** Migrate only the python_class concrete package: manifest, version, policy, finite context schema and renderer together. Shared definitions are consumed, not copied into generic Python.
- **Preserved behavior:** Explicit imports/bases/async; no Service routing, hidden project assumptions or fabricated bodies.
- **CY034.D2 — independent evidence:** CODE-E01/02/05/09/10; valid empty skeleton and explicit signatures; unsupported bodies rejected. Limit the family matrix to python_class; the paired family's evidence is independently required in its own cycle.
- **Rollback:** R-CY034: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY034.D1 and CY034.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: T009, T017, T023, T031, T054, T056.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `.pgmcp/template_suite/python_class/manifest.yaml`
- `.pgmcp/template_suite/python_class/.version`
- `.pgmcp/template_suite/python_class/policy.yaml`
- `.pgmcp/template_suite/python_class/context.schema.json`
- `.pgmcp/template_suite/python_class/template.jinja2`
- `tests/mcp_server/integration/templates/test_python_class.py`
- `tests/mcp_server/fixtures/delivered_templates.py`

Previously introduced paths revisited in this cycle:

- `tests/mcp_server/integration/templates/test_python_pydantic_dto.py`
- `tests/mcp_server/integration/templates/test_python_pydantic_config.py`

Independent QA identified the repeated delivered-package composition as a bounded test
maintenance prerequisite. One shared factory replaces that wiring; family assertions and
acceptance behavior remain in each test. The standing proportional QA-correction rule
authorizes these exact paths. R-CY034 is `c8683722ab81c7bec8436396862f60a157ec0b80`;
the two existing tests were clean and the factory was absent. Recover only this cycle's
inverse diff, including its owned factory addition.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/templates/test_python_class.py`

Existing affected test/helper sources: T009, T017, T023, T031, T054, T056. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY034, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY035

**Python Protocol artifact**

- **Semantic predecessors:** [CY018](planning-execution.md#cy018), [CY031](planning-artifacts-mutation.md#cy031).
- **Shared-file predecessors:** [CY034](planning-artifacts-mutation.md#cy034).
- **Authority:** [DI-03 code §7.5](design-code-test-artifacts.md).
- **CY035.D1 — bounded result:** Migrate only the python_protocol concrete package: manifest, version, policy, finite context schema and renderer together. Shared definitions are consumed, not copied into generic Python.
- **Preserved behavior:** Explicit imports/bases/async; no Service routing, hidden project assumptions or fabricated bodies.
- **CY035.D2 — independent evidence:** CODE-E01/02/05/09/10; valid empty skeleton and explicit signatures; unsupported bodies rejected. Limit the family matrix to python_protocol; the paired family's evidence is independently required in its own cycle.
- **Rollback:** R-CY035: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY035.D1 and CY035.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: T009, T017, T023, T031, T054, T056.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `.pgmcp/template_suite/python_protocol/manifest.yaml`
- `.pgmcp/template_suite/python_protocol/.version`
- `.pgmcp/template_suite/python_protocol/policy.yaml`
- `.pgmcp/template_suite/python_protocol/context.schema.json`
- `.pgmcp/template_suite/python_protocol/template.jinja2`
- `tests/mcp_server/integration/templates/test_python_protocol.py`

Previously introduced paths revisited in this cycle:

- `.pgmcp/template_suite/shared/definitions/python.schema.json`
- `.pgmcp/template_suite/python_class/context.schema.json`

Independent QA identified one shared InstanceParameter specialization to preserve the
existing self-name restriction without duplicating it across instance-method consumers.
Parameter and Signature remain unchanged; Generic keeps its local dunder exclusion.
The standing proportional QA-correction rule authorizes these two existing paths.
R-CY035 is `77f2e0f522c7ca7ca8e9fa8e73d1ae754ba8901e`; both files were clean and the
cycle-owned inverse diff is the recovery route. Existing class rejection evidence is reused.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/templates/test_python_protocol.py`

Existing affected test/helper sources: T009, T017, T023, T031, T054, T056. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY035, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY036

**Portable adapter artifact**

- **Semantic predecessors:** [CY018](planning-execution.md#cy018), [CY031](planning-artifacts-mutation.md#cy031).
- **Shared-file predecessors:** [CY035](planning-artifacts-mutation.md#cy035).
- **Authority:** [DI-03 code §7.6](design-code-test-artifacts.md).
- **CY036.D1 — bounded result:** Migrate only the python_adapter concrete package: manifest, version, policy, finite context schema and renderer together. Shared definitions are consumed, not copied into generic Python.
- **Preserved behavior:** Caller-owned constructor/methods, opt-in logging; no strategy_cache/Translator/ID/lifecycle defaults.
- **CY036.D2 — independent evidence:** CODE-E01/02/05/06/09/10; supplied operations render and absent logging stays absent; project dependency absence. Limit the family matrix to python_adapter; the paired family's evidence is independently required in its own cycle.
- **Rollback:** R-CY036: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY036.D1 and CY036.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: T009, T017, T023, T031, T036, T054, T056.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `.pgmcp/template_suite/python_adapter/manifest.yaml`
- `.pgmcp/template_suite/python_adapter/.version`
- `.pgmcp/template_suite/python_adapter/policy.yaml`
- `.pgmcp/template_suite/python_adapter/context.schema.json`
- `.pgmcp/template_suite/python_adapter/template.jinja2`
- `tests/mcp_server/integration/templates/test_python_adapter.py`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/templates/test_python_adapter.py`

Existing affected test/helper sources: T009, T017, T023, T031, T036, T054, T056. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY036, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY037

**Portable worker artifact**

- **Semantic predecessors:** [CY018](planning-execution.md#cy018), [CY031](planning-artifacts-mutation.md#cy031).
- **Shared-file predecessors:** [CY036](planning-artifacts-mutation.md#cy036).
- **Authority:** [DI-03 code §7.6](design-code-test-artifacts.md).
- **CY037.D1 — bounded result:** Migrate only the python_worker concrete package: manifest, version, policy, finite context schema and renderer together. Shared definitions are consumed, not copied into generic Python.
- **Preserved behavior:** Caller-owned constructor/methods, opt-in logging; no strategy_cache/Translator/ID/lifecycle defaults.
- **CY037.D2 — independent evidence:** CODE-E01/02/05/06/09/10; supplied operations render and absent logging stays absent; project dependency absence. Limit the family matrix to python_worker; the paired family's evidence is independently required in its own cycle.
- **Rollback:** R-CY037: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY037.D1 and CY037.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: T009, T017, T023, T031, T036, T054, T056.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `.pgmcp/template_suite/python_worker/manifest.yaml`
- `.pgmcp/template_suite/python_worker/.version`
- `.pgmcp/template_suite/python_worker/policy.yaml`
- `.pgmcp/template_suite/python_worker/context.schema.json`
- `.pgmcp/template_suite/python_worker/template.jinja2`
- `tests/mcp_server/integration/templates/test_python_worker.py`

Previously introduced paths revisited in this cycle:

- `.pgmcp/template_suite/shared/definitions/python.schema.json`
- `.pgmcp/template_suite/python_adapter/context.schema.json`

Independent QA identified the shared constructor-conflict rule needed by both portable families.
Under the standing authorization for proportional corrections, CY037 factors the existing rule
without changing adapter admission or the general method/constructor records.
R-CY037 is `6f96903c7ca1b8979b2d7a40ab76ee8417592f47`; restore only this cycle's owned inverse diff.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/templates/test_python_worker.py`

Existing affected test/helper sources: T009, T017, T023, T031, T036, T054, T056. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY037, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY038

**Public unit-test artifact**

- **Semantic predecessors:** [CY018](planning-execution.md#cy018), [CY031](planning-artifacts-mutation.md#cy031).
- **Shared-file predecessors:** [CY037](planning-artifacts-mutation.md#cy037).
- **Authority:** [DI-03 code §7.7](design-code-test-artifacts.md).
- **CY038.D1 — bounded result:** Migrate only the pytest_unit_test concrete package: manifest, version, policy, finite context schema and renderer together. Shared definitions are consumed, not copied into generic Python.
- **Preserved behavior:** At least one real case; explicit sync/async, scope/autouse/params/imports; no forced E2E/class/pytest marker.
- **CY038.D2 — independent evidence:** CODE-E01/02/05/07/09; actual schema/render output plus meaningful representative execution; no success placeholders. Limit the family matrix to pytest_unit_test; the paired family's evidence is independently required in its own cycle.
- **Rollback:** R-CY038: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY038.D1 and CY038.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: T009, T017, T023, T031, T037, T039, T040, T041, T054.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `.pgmcp/template_suite/pytest_unit_test/manifest.yaml`
- `.pgmcp/template_suite/pytest_unit_test/.version`
- `.pgmcp/template_suite/pytest_unit_test/policy.yaml`
- `.pgmcp/template_suite/pytest_unit_test/context.schema.json`
- `.pgmcp/template_suite/pytest_unit_test/template.jinja2`
- `tests/mcp_server/integration/templates/test_pytest_unit_test.py`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/templates/test_pytest_unit_test.py`

Existing affected test/helper sources: T009, T017, T023, T031, T037, T039, T040, T041, T054. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY038, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY039

**Public integration-test artifact**

- **Semantic predecessors:** [CY018](planning-execution.md#cy018), [CY031](planning-artifacts-mutation.md#cy031).
- **Shared-file predecessors:** [CY038](planning-artifacts-mutation.md#cy038).
- **Authority:** [DI-03 code §7.7](design-code-test-artifacts.md).
- **CY039.D1 — bounded result:** Migrate only the pytest_integration_test concrete package: manifest, version, policy, finite context schema and renderer together. Shared definitions are consumed, not copied into generic Python.
- **Preserved behavior:** At least one real case; explicit sync/async, scope/autouse/params/imports; no forced E2E/class/pytest marker.
- **CY039.D2 — independent evidence:** CODE-E01/02/05/07/09; actual schema/render output plus meaningful representative execution; no success placeholders. Limit the family matrix to pytest_integration_test; the paired family's evidence is independently required in its own cycle.
- **Rollback:** R-CY039: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY039.D1 and CY039.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: T009, T017, T023, T031, T037, T039, T040, T041, T054.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `.pgmcp/template_suite/pytest_integration_test/manifest.yaml`
- `.pgmcp/template_suite/pytest_integration_test/.version`
- `.pgmcp/template_suite/pytest_integration_test/policy.yaml`
- `.pgmcp/template_suite/pytest_integration_test/context.schema.json`
- `.pgmcp/template_suite/pytest_integration_test/template.jinja2`
- `tests/mcp_server/integration/templates/test_pytest_integration_test.py`

Previously introduced paths revisited in this cycle:

- `.pgmcp/template_suite/shared/definitions/python.schema.json`
- `.pgmcp/template_suite/pytest_unit_test/context.schema.json`

Independent QA identified the shared class-discovery and instance-case rules needed by both
pytest families. Under the standing authorization for proportional corrections, CY039 factors
the existing unit rules without changing admission or the general test/fixture records.
R-CY039 is `4a284a9f278d0708bbc339ef347796d5fcf9d8ac`; restore only this cycle's owned inverse diff.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/templates/test_pytest_integration_test.py`

Existing affected test/helper sources: T009, T017, T023, T031, T037, T039, T040, T041, T054. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY039, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY040

**TypeScript DTO artifact**

- **Semantic predecessors:** [CY004](planning-execution.md#cy004), [CY005](planning-execution.md#cy005), [CY006](planning-execution.md#cy006), [CY007](planning-execution.md#cy007), [CY023](planning-execution.md#cy023).
- **Shared-file predecessors:** [CY039](planning-artifacts-mutation.md#cy039).
- **Authority:** [DI-03 code §§7.8–7.9](design-code-test-artifacts.md).
- **CY040.D1 — bounded result:** Single concrete TS package replaces pseudo-pattern; explicit typed property records.
- **Preserved behavior:** Readonly/mutable, optionality, constructor and interfaces; no mini-language or project assumptions.
- **CY040.D2 — independent evidence:** CODE-E01/08/09/10; accepted/rejected contexts, syntactic output, caller content and one resolved entrypoint.
- **Rollback:** R-CY040: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY040.D1 and CY040.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: T009, T017, T023, T054, T081.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `tests/mcp_server/integration/templates/test_typescript_artifact.py`
- `.pgmcp/template_suite/typescript_dto/manifest.yaml`
- `.pgmcp/template_suite/typescript_dto/.version`
- `.pgmcp/template_suite/typescript_dto/policy.yaml`
- `.pgmcp/template_suite/typescript_dto/context.schema.json`
- `.pgmcp/template_suite/typescript_dto/template.jinja2`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/templates/test_typescript_artifact.py`

Existing affected test/helper sources: T009, T017, T023, T054, T081. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY040, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY041

**Shared document records and rendering**

- **Semantic predecessors:** [CY004](planning-execution.md#cy004), [CY005](planning-execution.md#cy005), [CY006](planning-execution.md#cy006), [CY007](planning-execution.md#cy007).
- **Shared-file predecessors:** [CY031](planning-artifacts-mutation.md#cy031), [CY037](planning-artifacts-mutation.md#cy037).
- **Authority:** [DI-03 documents §§7.1–7.2,7.7](design-document-tracking-artifacts.md).
- **CY041.D1 — bounded result:** Link/issue/checklist records and document/tracking bases; paired schema/render support.
- **Preserved behavior:** Positive issue IDs, explicit checked state, absent vs empty, valid Markdown escaping/reference identity.
- **CY041.D2 — independent evidence:** DOC-E02/03/04/05/11; multiple concrete consumers, invalid primitive rejection and independent link construction assertions.
- **Rollback:** R-CY041: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY041.D1 and CY041.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C087, T026, T027, T055, T056.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `tests/mcp_server/integration/templates/test_shared_documents.py`
- `.pgmcp/template_suite/shared/templates/bases/tier1_document.jinja2`
- `.pgmcp/template_suite/shared/templates/bases/tier1_tracking.jinja2`
- `.pgmcp/template_suite/shared/templates/bases/tier2_markdown_document.jinja2`
- `.pgmcp/template_suite/shared/templates/bases/tier2_markdown_tracking.jinja2`
- `.pgmcp/template_suite/shared/templates/bases/tier2_text_tracking.jinja2`
- `.pgmcp/template_suite/shared/templates/patterns/markdown/links.jinja2`
- `.pgmcp/template_suite/shared/templates/patterns/markdown/sections.jinja2`
- `.pgmcp/template_suite/shared/definitions/link.schema.json`
- `.pgmcp/template_suite/shared/definitions/issue-reference.schema.json`
- `.pgmcp/template_suite/shared/definitions/checklist-item.schema.json`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/templates/test_shared_documents.py`

Existing affected test/helper sources: T026, T027, T055, T056. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY041, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY042

**Research artifact**

- **Semantic predecessors:** [CY019](planning-execution.md#cy019), [CY041](planning-artifacts-mutation.md#cy041).
- **Shared-file predecessors:** [CY040](planning-artifacts-mutation.md#cy040).
- **Authority:** [DI-03 documents §§7.3,7.8](design-document-tracking-artifacts.md).
- **CY042.D1 — bounded result:** Research package with strategy/evidence/consumer/risk carriers.
- **Preserved behavior:** Initial valid basis distinct from finished Research; explicit human strategy content.
- **CY042.D2 — independent evidence:** DOC-E01/02/03/06/10; all applicable Research workflow meanings render without embedded invocation or fabricated approval.
- **Rollback:** R-CY042: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY042.D1 and CY042.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: T011, T017, T027, T054, T055.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `tests/mcp_server/integration/templates/test_research_artifact.py`
- `.pgmcp/template_suite/research/manifest.yaml`
- `.pgmcp/template_suite/research/.version`
- `.pgmcp/template_suite/research/policy.yaml`
- `.pgmcp/template_suite/research/context.schema.json`
- `.pgmcp/template_suite/research/template.jinja2`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/templates/test_research_artifact.py`

Existing affected test/helper sources: T011, T017, T027, T054, T055. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY042, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY043

**Design artifact**

- **Semantic predecessors:** [CY019](planning-execution.md#cy019), [CY041](planning-artifacts-mutation.md#cy041).
- **Shared-file predecessors:** [CY042](planning-artifacts-mutation.md#cy042).
- **Authority:** [DI-03 documents §§7.3,7.8](design-document-tracking-artifacts.md).
- **CY043.D1 — bounded result:** Design package contracts/options/production/test/preservation carriers.
- **Preserved behavior:** Author-owned decisions, no required premature decision; no prose snapshot authority.
- **CY043.D2 — independent evidence:** DOC-E01/02/03/06/10; required workflow meanings supported; omission and explicit empty values retained.
- **Rollback:** R-CY043: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY043.D1 and CY043.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: T011, T017, T027, T054.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `tests/mcp_server/integration/templates/test_design_artifact.py`
- `.pgmcp/template_suite/design/manifest.yaml`
- `.pgmcp/template_suite/design/.version`
- `.pgmcp/template_suite/design/policy.yaml`
- `.pgmcp/template_suite/design/context.schema.json`
- `.pgmcp/template_suite/design/template.jinja2`
- `.pgmcp/template_suite/shared/definitions/risk.schema.json`

Previously introduced paths revisited in this cycle:

- `.pgmcp/template_suite/research/context.schema.json`

Independent QA confirmed that Research and Design actually reuse the same Risk record under
DI-03 section 7.2. Under the standing authorization for proportional corrections, CY043 extracts
that record unchanged into a shared definition and points both consumers at it. The two planning
ledgers record only this ownership amendment; no broader schema framework is introduced.
R-CY043 is `8881113feeb43b48862d68d4edb0f88d678ac5d2`; restore only this cycle's owned inverse diff.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/templates/test_design_artifact.py`

Existing affected test/helper sources: T011, T017, T027, T054. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY043, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY044

**Planning artifact and operational projection**

- **Semantic predecessors:** [CY019](planning-execution.md#cy019), [CY041](planning-artifacts-mutation.md#cy041).
- **Shared-file predecessors:** [CY043](planning-artifacts-mutation.md#cy043).
- **Authority:** [DI-03 documents §7.5/7.8](design-document-tracking-artifacts.md).
- **CY044.D1 — bounded result:** Planning package work units and phase deliverables matching operational cycle shape.
- **Preserved behavior:** cycle_number/name/deliverables/validates/exit_criteria preserved; narrative not hidden tool payload.
- **CY044.D2 — independent evidence:** DOC-E06/07/10; initial scaffold, refined plan and actual save/load projection separately exercised; no old success_criteria union.
- **Rollback:** R-CY044: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY044.D1 and CY044.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Readback prerequisite supplement: [R001–R008](planning-path-ownership.md#readback-prerequisite-supplement). R008 remains the planning-schema authority; verify operational projection and public readback retain its ordered cycles and phase deliverables without changing it. D1/D2 and this cycle's R-CY044, preserved behavior and independent stop/go apply to these exact additional seams.

Existing source IDs: T011, T017, T027, T054.

Read-only review/preservation IDs: R008. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `tests/mcp_server/integration/templates/test_planning_artifact.py`
- `.pgmcp/template_suite/planning/manifest.yaml`
- `.pgmcp/template_suite/planning/.version`
- `.pgmcp/template_suite/planning/policy.yaml`
- `.pgmcp/template_suite/planning/context.schema.json`
- `.pgmcp/template_suite/planning/template.jinja2`
- `.pgmcp/template_suite/shared/definitions/evidence-requirement.schema.json`

Previously introduced paths revisited in this cycle:

- `.pgmcp/template_suite/design/context.schema.json`

Independent QA confirmed actual reuse of EvidenceRequirement by Design.validation and
Planning WorkUnit.verification under DI-03 sections 7.2 and 7.5. Under the standing authorization
for proportional corrections, CY044 extracts that closed record unchanged into a shared definition.
The two planning ledgers record only this ownership amendment; operational schemas remain read-only.
R-CY044 is `0eeff39b8765d1fe49bb38ee1d2c3b325e76eaad`; restore only this cycle's owned inverse diff.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/templates/test_planning_artifact.py`

Existing affected test/helper sources: T011, T017, T027, T054. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY044, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY045

**Validation report artifact**

- **Semantic predecessors:** [CY019](planning-execution.md#cy019), [CY041](planning-artifacts-mutation.md#cy041).
- **Shared-file predecessors:** [CY044](planning-artifacts-mutation.md#cy044).
- **Authority:** [DI-03 documents §§7.3,7.8](design-document-tracking-artifacts.md).
- **CY045.D1 — bounded result:** Validation package obligation/evidence/preservation/containment carriers.
- **Preserved behavior:** Producer outcome never grants QA authority; explicit issue/cycle/status.
- **CY045.D2 — independent evidence:** DOC-E01/06/10; all validation workflow meanings, no runtime-populated evidence or invented PASS.
- **Rollback:** R-CY045: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY045.D1 and CY045.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: T011, T017, T027, T054.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `tests/mcp_server/integration/templates/test_validation_artifact.py`
- `.pgmcp/template_suite/validation_report/manifest.yaml`
- `.pgmcp/template_suite/validation_report/.version`
- `.pgmcp/template_suite/validation_report/policy.yaml`
- `.pgmcp/template_suite/validation_report/context.schema.json`
- `.pgmcp/template_suite/validation_report/template.jinja2`
- `.pgmcp/template_suite/shared/definitions/evidence.schema.json`

Previously introduced paths revisited in this cycle:

- `.pgmcp/template_suite/research/context.schema.json`

Independent QA confirmed actual reuse of Evidence by Research and Validation Report under
DI-03 sections 7.2 and 7.3. Under the standing authorization for proportional corrections,
CY045 extracts that closed record with unchanged field and date semantics into a shared definition.
The two planning ledgers record only this ownership amendment; no runtime or broader schema changes.
R-CY045 is `3f233e720a333f1f7a4140176a6294f81e4a5679`; restore only this cycle's owned inverse diff.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/templates/test_validation_artifact.py`

Existing affected test/helper sources: T011, T017, T027, T054. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY045, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY046

**Architecture document artifact**

- **Semantic predecessors:** [CY019](planning-execution.md#cy019), [CY041](planning-artifacts-mutation.md#cy041).
- **Shared-file predecessors:** [CY045](planning-artifacts-mutation.md#cy045), [CY042](planning-artifacts-mutation.md#cy042).
- **Authority:** [DI-03 documents §7.4](design-document-tracking-artifacts.md).
- **CY046.D1 — bounded result:** Migrate only the architecture concrete package: manifest, version, policy, finite context schema and renderer together. Shared definitions are consumed, not copied into generic Python.
- **Preserved behavior:** Concrete caller content and usable sources; no static tool inventory inferred.
- **CY046.D2 — independent evidence:** DOC-E01/02/04/08/10; empty initial vs populated records and required source semantics. Limit the family matrix to architecture; the paired family's evidence is independently required in its own cycle.
- **Rollback:** R-CY046: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY046.D1 and CY046.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: T011, T017, T027, T054, T055, T056.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `.pgmcp/template_suite/architecture/manifest.yaml`
- `.pgmcp/template_suite/architecture/.version`
- `.pgmcp/template_suite/architecture/policy.yaml`
- `.pgmcp/template_suite/architecture/context.schema.json`
- `.pgmcp/template_suite/architecture/template.jinja2`
- `.pgmcp/template_suite/shared/definitions/decision.schema.json`
- `tests/mcp_server/integration/templates/test_architecture.py`

Previously introduced paths revisited in this cycle:

- `.pgmcp/template_suite/design/context.schema.json`

Independent QA confirmed actual reuse of Decision by Design and Architecture under DI-03
sections 7.2 and 7.3. Under the standing authorization for proportional corrections, CY046 extracts
that closed record unchanged into a shared definition. The two planning ledgers record only this
ownership amendment; sources remain optional and no new diagram-check dependency is introduced.
R-CY046 is `ceaa29ae0ef2a66fca83337f026a986d76f1cc9f`; restore only this cycle's owned inverse diff.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/templates/test_architecture.py`

Existing affected test/helper sources: T011, T017, T027, T054, T055, T056. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY046, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY047

**Reference document artifact**

- **Semantic predecessors:** [CY019](planning-execution.md#cy019), [CY041](planning-artifacts-mutation.md#cy041).
- **Shared-file predecessors:** [CY046](planning-artifacts-mutation.md#cy046).
- **Authority:** [DI-03 documents §7.4](design-document-tracking-artifacts.md).
- **CY047.D1 — bounded result:** Migrate only the reference concrete package: manifest, version, policy, finite context schema and renderer together. Shared definitions are consumed, not copied into generic Python.
- **Preserved behavior:** Concrete caller content and usable sources; no static tool inventory inferred.
- **CY047.D2 — independent evidence:** DOC-E01/02/04/08/10; empty initial vs populated records and required source semantics. Limit the family matrix to reference; the paired family's evidence is independently required in its own cycle.
- **Rollback:** R-CY047: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY047.D1 and CY047.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: T011, T017, T027, T054, T055, T056.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `.pgmcp/template_suite/reference/manifest.yaml`
- `.pgmcp/template_suite/reference/.version`
- `.pgmcp/template_suite/reference/policy.yaml`
- `.pgmcp/template_suite/reference/context.schema.json`
- `.pgmcp/template_suite/reference/template.jinja2`
- `tests/mcp_server/integration/templates/test_reference.py`

Previously introduced paths revisited in this cycle:

- `tests/mcp_server/integration/templates/test_research_artifact.py`
- `tests/mcp_server/integration/templates/test_design_artifact.py`
- `tests/mcp_server/integration/templates/test_planning_artifact.py`
- `tests/mcp_server/integration/templates/test_validation_artifact.py`
- `tests/mcp_server/integration/templates/test_architecture.py`

The user clarified that tests must verify behavior, not template editorial content. Independent QA
confirmed this bounded maintenance slice removes fixed heading/label wording and duplicated expected
prose while retaining schema admission, caller-data preservation, presence behavior, escaping, link
integrity and actual operational save/readback. No production behavior, shared helper, new test case,
or broader test framework is introduced by this slice. Both planning ledgers record the ownership.
R-CY047 is `dfa12e8790db99d62b12ba1cacf15bc93107199a`; restore only this cycle's owned inverse diff.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/templates/test_reference.py`

Existing affected test/helper sources: T011, T017, T027, T054, T055, T056. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY047, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY048

**Generic document artifact**

- **Semantic predecessors:** [CY019](planning-execution.md#cy019), [CY041](planning-artifacts-mutation.md#cy041).
- **Shared-file predecessors:** [CY047](planning-artifacts-mutation.md#cy047).
- **Authority:** [DI-03 documents §7.3](design-document-tracking-artifacts.md).
- **CY048.D1 — bounded result:** Generic Document finite sections/migration/FAQ/checklist contract.
- **Preserved behavior:** Optional omission and explicit fields; no scalar coercion or silently ignored legacy content.
- **CY048.D2 — independent evidence:** DOC-E01/02/03/04/05/10; schema rejection and faithful actual package render.
- **Rollback:** R-CY048: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY048.D1 and CY048.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: T011, T017, T027, T054, T055, T094.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `tests/mcp_server/integration/templates/test_generic_document.py`
- `.pgmcp/template_suite/generic_doc/manifest.yaml`
- `.pgmcp/template_suite/generic_doc/.version`
- `.pgmcp/template_suite/generic_doc/policy.yaml`
- `.pgmcp/template_suite/generic_doc/context.schema.json`
- `.pgmcp/template_suite/generic_doc/template.jinja2`
- `.pgmcp/template_suite/shared/definitions/section.schema.json`

Previously introduced paths revisited in this cycle:

- `.pgmcp/template_suite/design/context.schema.json`
- `docs/development/issue460/planning-artifacts-mutation.md`
- `docs/development/issue460/planning-path-ownership.md`

Bounded actual-reuse amendment: extract the unchanged Section contract shared by Design and Generic Document, preserving closed records and the presence-based anyOf rule. Keep FAQ local. The existing Design populated-render and schema-rejection cases cover the reference substitution; no new test framework or unrelated legacy retirement is included. The CY048-owned T094 test is retired after its named successor passes; mixed legacy tests remain with their later owners. Independent QA confirmed this bounded scope under the user's standing authorization. R-CY048 is `d435424df31f22ac1e433e0ac8f8f55ae733359d`; these paths were clean at entry.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/templates/test_generic_document.py`

Existing affected test/helper sources: T011, T017, T027, T054, T055, T094. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY048, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY049

**Issue body artifact**

- **Semantic predecessors:** [CY019](planning-execution.md#cy019), [CY041](planning-artifacts-mutation.md#cy041).
- **Shared-file predecessors:** [CY048](planning-artifacts-mutation.md#cy048).
- **Authority:** [DI-03 documents §7.6](design-document-tracking-artifacts.md).
- **CY049.D1 — bounded result:** Migrate only the issue concrete package: manifest, version, policy, finite context schema and renderer together. Shared definitions are consumed, not copied into generic Python.
- **Preserved behavior:** No H1 body requirement; explicit none/populated deferred state; positive refs and unchecked items.
- **CY049.D2 — independent evidence:** DOC-E01/02/05/09/11; original four PR defects covered, metadata stripping never publication. Limit the family matrix to issue; the paired family's evidence is independently required in its own cycle.
- **Rollback:** R-CY049: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY049.D1 and CY049.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: T017, T044, T101.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `.pgmcp/template_suite/issue/manifest.yaml`
- `.pgmcp/template_suite/issue/.version`
- `.pgmcp/template_suite/issue/policy.yaml`
- `.pgmcp/template_suite/issue/context.schema.json`
- `.pgmcp/template_suite/issue/template.jinja2`
- `tests/mcp_server/integration/templates/test_issue.py`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/templates/test_issue.py`

Existing affected test/helper sources: T017, T044, T101. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY049, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY050

**PR body artifact**

- **Semantic predecessors:** [CY019](planning-execution.md#cy019), [CY041](planning-artifacts-mutation.md#cy041).
- **Shared-file predecessors:** [CY049](planning-artifacts-mutation.md#cy049).
- **Authority:** [DI-03 documents §7.6](design-document-tracking-artifacts.md).
- **CY050.D1 — bounded result:** Migrate only the pr concrete package: manifest, version, policy, finite context schema and renderer together. Shared definitions are consumed, not copied into generic Python.
- **Preserved behavior:** No H1 body requirement; explicit none/populated deferred state; positive refs and unchecked items.
- **CY050.D2 — independent evidence:** DOC-E01/02/05/09/11; original four PR defects covered, metadata stripping never publication. Limit the family matrix to pr; the paired family's evidence is independently required in its own cycle.
- **Rollback:** R-CY050: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY050.D1 and CY050.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C094, T017, T044, T101.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `.pgmcp/template_suite/pr/manifest.yaml`
- `.pgmcp/template_suite/pr/.version`
- `.pgmcp/template_suite/pr/policy.yaml`
- `.pgmcp/template_suite/pr/context.schema.json`
- `.pgmcp/template_suite/pr/template.jinja2`
- `.pgmcp/template_suite/shared/definitions/deferred-item.schema.json`
- `tests/mcp_server/integration/templates/test_pr.py`

Previously introduced paths revisited in this cycle:

- `.pgmcp/template_suite/validation_report/context.schema.json`
- `docs/development/issue460/planning-artifacts-mutation.md`
- `docs/development/issue460/planning-path-ownership.md`

Bounded actual-reuse amendment: extract the unchanged DeferredItem contract shared by Validation and PR; existing Validation render/rejection cases cover the reference replacement. Independent QA confirmed this scope under the user's standing authorization. C094 changes only the two authored-body descriptions, not publication behavior. Retire T101 and the eighteen issue/PR/Markdown cases in T044 after successor evidence; retain its nine commit/tier1/text cases until CY051. R-CY050 is `fb4937d423a5c449ccc8f351f642bbb26f92b820`; these paths were clean at entry.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/templates/test_pr.py`

Existing affected test/helper sources: T017, T044, T101. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY050, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY051

**Commit artifact**

- **Semantic predecessors:** [CY024](planning-execution.md#cy024), [CY041](planning-artifacts-mutation.md#cy041).
- **Shared-file predecessors:** [CY050](planning-artifacts-mutation.md#cy050).
- **Authority:** [DI-03 documents §7.6](design-document-tracking-artifacts.md).
- **CY051.D1 — bounded result:** Commit package conventional framing and required structured caller content.
- **Preserved behavior:** Arbitrary conventional type, case, marker/body/footer; no coupling to Git allowed types.
- **CY051.D2 — independent evidence:** DOC-E01/09/11; actual package output through commit adapter, valid/invalid header/message boundaries.
- **Rollback:** R-CY051: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY051.D1 and CY051.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: T017, T044.

Read-only review/preservation IDs: None. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `tests/mcp_server/integration/templates/test_commit_artifact.py`
- `.pgmcp/template_suite/commit/manifest.yaml`
- `.pgmcp/template_suite/commit/.version`
- `.pgmcp/template_suite/commit/policy.yaml`
- `.pgmcp/template_suite/commit/context.schema.json`
- `.pgmcp/template_suite/commit/template.jinja2`

Previously introduced paths revisited in this cycle:

None.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/templates/test_commit_artifact.py`

Existing affected test/helper sources: T017, T044. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY051, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY052

**Artifact location policy**

- **Semantic predecessors:** [CY004](planning-execution.md#cy004), [CY005](planning-execution.md#cy005).
- **Shared-file predecessors:** [CY030](planning-execution.md#cy030), [CY015](planning-execution.md#cy015), [CY012](planning-execution.md#cy012), [CY001](planning-execution.md#cy001).
- **Authority:** [DI-04 §§2–3.4](design-mutation-validation.md).
- **CY052.D1 — bounded result:** Pure location schema/resolver and catalog foreign-key validation using explicit roots.
- **Preserved behavior:** Exact filename, configured/default/temp fallback, explicit force only in workspace; no overwrite authority.
- **CY052.D2 — independent evidence:** DI-04 §8; all routing branches, stale config refs, containment, unmapped packages and unaffected enforcement.
- **Rollback:** R-CY052: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY052.D1 and CY052.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C004, C057, C058, C060, C107, S016, S021, S037, T003, T047, T048, T064, T067, T068, T073, T074, T080, T091, T095.

Read-only review/preservation IDs: C055, C063. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/config/schemas/artifact_locations.py`
- `mcp_server/services/artifact_target_resolver.py`
- `tests/mcp_server/unit/services/test_artifact_target_resolver.py`

Previously introduced paths revisited in this cycle:

None.

- The listed legacy review-only paths retain their current constructors, runtime reads and normal registration. New behavior is exercised through the separately named final internal components; no V2/V3 ToolAssembly union, public alias, fallback reader or constructor mode.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/services/test_artifact_target_resolver.py`

Existing affected test/helper sources: S016, S021, T003, T047, T048, T064, T067, T068, T073, T074, T080, T091, T095. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY052, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY053

**Internal scaffold persistence**

- **Semantic predecessors:** [CY006](planning-execution.md#cy006), [CY007](planning-execution.md#cy007), [CY026](planning-execution.md#cy026), [CY052](planning-artifacts-mutation.md#cy052).
- **Shared-file predecessors:** [CY041](planning-artifacts-mutation.md#cy041), [CY001](planning-execution.md#cy001).
- **Authority:** [DI-04 §§2/4.1/4.4/7.1](design-mutation-validation.md).
- **CY053.D1 — bounded result:** Generic unchanged-context render/check/create route with narrow injected dependencies.
- **Preserved behavior:** Enforce/report facts, create-only collision safety, no operation controls in render data.
- **CY053.D2 — independent evidence:** Actual bytes/result for pass/fail/unavailable/not-executed, early/late collision, render/persist failures and postcommit reporting; no write inference from result alone.
- **Rollback:** R-CY053: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY053.D1 and CY053.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C087, S033, S034, S035, T001, T004, T005, T008, T012, T020, T021, T048, T076, T078, T079, T142.

Read-only review/preservation IDs: C064, C066, C086, C097. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/services/scaffold_operation.py`
- `tests/mcp_server/integration/test_scaffold_operation_v3.py`
- `mcp_server/schemas/mutation_outputs.py`

Previously introduced paths revisited in this cycle:

- `mcp_server/services/artifact_target_resolver.py`
- `mcp_server/core/interfaces/execution.py`
- `mcp_server/execution/content_input.py`
- `tests/mcp_server/integration/execution/test_content_input.py`
- `tests/mcp_server/unit/execution/test_check_service.py`

Independent QA identified a missing preparation-stage fact required by DI-04 §7.1.
The user's standing authorization for bounded QA corrections covers preserving allocation
versus write failure and factual rollback-cleanup failure at the existing scratch boundary,
and checking their existing propagation without inventing an adapter invocation.
Preserve the already-resolved early-collision path in the standard exception filename field
so the mutation consumer can report it without parsing diagnostic text.
No execution policy, adapter protocol, startup activation, or public behavior changes.
Keep the corresponding rows in `planning-path-ownership.md` aligned with this bounded revisit.

- The listed legacy review-only paths retain their current constructors, runtime reads and normal registration. New behavior is exercised through the separately named final internal components; no V2/V3 ToolAssembly union, public alias, fallback reader or constructor mode.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/test_scaffold_operation_v3.py`

Existing affected test/helper sources: S035, T001, T004, T005, T008, T012, T020, T021, T048, T076, T078, T079, T142. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY053, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY054

**Safe-edit construction and profile selection**

- **Semantic predecessors:** [CY006](planning-execution.md#cy006), [CY007](planning-execution.md#cy007), [CY026](planning-execution.md#cy026).
- **Shared-file predecessors:** None.
- **Authority:** [DI-04 §§4.6–4.8](design-mutation-validation.md).
- **CY054.D1 — bounded result:** Complete replace/append/rewrite/pattern edit construction and metadata/explicit/extension profile selection.
- **Preserved behavior:** Existing operation/newline semantics, unmatched-anchor rejection, no-change results and unknown metadata fallback.
- **CY054.D2 — independent evidence:** Exact original/proposed content, absent/invalid/current ID cases; no caller native args; construction failures prevent checks.
- **Rollback:** R-CY054: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY054.D1 and CY054.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: None.

Read-only review/preservation IDs: C096. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/services/edit_construction.py`
- `tests/mcp_server/unit/services/test_edit_construction.py`

Previously introduced paths revisited in this cycle:

- `mcp_server/config/schemas/checks_config.py`

Independent QA identified that DI-04's selected extension requires the matched configured
suffix as well as its profile. Under the user's standing bounded-correction authorization,
expose that pair from the existing pure config lookup and delegate its existing profile-only
accessor to it. Preserve basename validation, original suffix spelling and longest casefold
matching. No second matching algorithm, runtime activation or selection policy change.
Keep the corresponding ownership row aligned with this bounded revisit.

- The listed legacy review-only paths retain their current constructors, runtime reads and normal registration. New behavior is exercised through the separately named final internal components; no V2/V3 ToolAssembly union, public alias, fallback reader or constructor mode.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/unit/services/test_edit_construction.py`

Existing affected test/helper sources: None. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY054, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY055

**Safe-edit guarded replacement**

- **Semantic predecessors:** [CY014](planning-execution.md#cy014), [CY015](planning-execution.md#cy015), [CY054](planning-artifacts-mutation.md#cy054).
- **Shared-file predecessors:** [CY053](planning-artifacts-mutation.md#cy053).
- **Authority:** [DI-04 §§4.9–4.10/7.1](design-mutation-validation.md).
- **CY055.D1 — bounded result:** Original snapshot, controlled replacement, concurrency and filesystem failure handling.
- **Preserved behavior:** Enforce no-write, report may persist invalid content, both retain independent safety blockers.
- **CY055.D2 — independent evidence:** Actual bytes under external writer/collision/symlink/lock/write/cleanup failures and unconfirmed child termination; no false no-write after commit.
- **Rollback:** R-CY055: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY055.D1 and CY055.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: S033, S034, S035, T007, T022, T048, T102, T142.

Read-only review/preservation IDs: C086, C096. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/services/edit_operation.py`
- `tests/mcp_server/integration/test_edit_operation_v3.py`

Previously introduced paths revisited in this cycle:

- `mcp_server/schemas/mutation_outputs.py`
- `mcp_server/services/scaffold_operation.py`

Independent QA approved exposing its existing pure mutation-check projection and
execution-blocker helpers for the safe-edit consumer. Preserve their behavior and reuse
the existing validation reducer; do not duplicate the check fact graph or move execution
projection into output schemas. This bounded revisit uses the user's standing authorization.

- The listed legacy review-only paths retain their current constructors, runtime reads and normal registration. New behavior is exercised through the separately named final internal components; no V2/V3 ToolAssembly union, public alias, fallback reader or constructor mode.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/test_edit_operation_v3.py`

Existing affected test/helper sources: S035, T007, T022, T048, T102, T142. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY055, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY056

**Schema discovery public composition**

- **Semantic predecessors:** [CY004](planning-execution.md#cy004), [CY005](planning-execution.md#cy005), [CY008](planning-execution.md#cy008), [CY009](planning-execution.md#cy009), [CY011](planning-execution.md#cy011), [CY006](planning-execution.md#cy006), [CY007](planning-execution.md#cy007).
- **Shared-file predecessors:** [CY003](planning-execution.md#cy003), [CY053](planning-artifacts-mutation.md#cy053), [CY055](planning-artifacts-mutation.md#cy055).
- **Authority:** [Shared §§7.2,7.4,7.6; DI-01 §7.2](design-shared-contracts.md).
- **CY056.D1 — bounded result:** Introduce final ScaffoldSchemaTool in mcp_server/tools/template_schema_tool.py using real decorators and selected-context attachments on isolated target composition; the existing scaffold_schema_tool.py and its normal registration stay intact until cutover.
- **Preserved behavior:** Complete finite ref-free schema, purpose, correct URI; successful scaffold excludes schema DTO duplication.
- **CY056.D2 — independent evidence:** Registered/lazy exposure==admission==resource; invalid input whole-tool vs context schema separate; supported client restart/cache behavior.
- **Rollback:** R-CY056: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY056.D1 and CY056.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C006, C106, S001, S002, S003, S009, T004, T006, T016, T018, T048, T060, T075, T084, T099, T104.

User-directed amendment (2026-09-14): keep wire-schema admission and typed binding in InputValidationDecorator; server.py only disables the SDK's early input rejection. C006 is limited to bounding the existing MCP dependency to >=1.0.0,<2. Context-schema validation remains separate.

Read-only review/preservation IDs: C086, C098. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `tests/mcp_server/integration/test_schema_public_v3.py`
- `mcp_server/tools/template_schema_tool.py`

Previously introduced paths revisited in this cycle:

None.

- The listed legacy review-only paths retain their current constructors, runtime reads and normal registration. New behavior is exercised through the separately named final internal components; no V2/V3 ToolAssembly union, public alias, fallback reader or constructor mode.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/test_schema_public_v3.py`

Existing affected test/helper sources: S009, T004, T006, T016, T018, T048, T060, T075, T084, T099, T104. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY056, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY057

**Scaffold public composition**

- **Semantic predecessors:** [CY053](planning-artifacts-mutation.md#cy053), [CY055](planning-artifacts-mutation.md#cy055), [CY056](planning-artifacts-mutation.md#cy056).
- **Shared-file predecessors:** [CY011](planning-execution.md#cy011), [CY010](planning-execution.md#cy010).
- **Authority:** [DI-04 §§4.10,7.1; Shared §11.1](design-mutation-validation.md).
- **CY057.D1 — bounded result:** Introduce final ScaffoldArtifactTool in mcp_server/tools/scaffold_tool.py, composed only in isolated target tests before cutover. Do not alter the legacy scaffold_artifact.py constructor, public contract or registration.
- **Preserved behavior:** 14 exact mutation error details, validation_policy/status and actual persistence facts; unrelated wrapper semantics.
- **CY057.D2 — independent evidence:** Actual wrapper/cache/text/schema attachment proves scaffold creation, domain rejection and operation fault, required nulls and capture; preserve active legacy scaffold behavior before cutover.
- **Rollback:** R-CY057: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY057.D1 and CY057.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C106, S003, S004, S007, S009, S010, T004, T006, T048, T072, T075, T099, T103, T134.

Read-only review/preservation IDs: C086. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/tools/scaffold_tool.py`
- `tests/mcp_server/integration/test_scaffold_public_v3.py`

Previously introduced paths revisited in this cycle:

- `mcp_server/schemas/mutation_outputs.py`

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/test_scaffold_public_v3.py`

Existing affected test/helper sources: S007, S009, S010, T004, T006, T048, T072, T075, T099, T103, T134. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY057, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY058

**Safe-edit public composition**

- **Semantic predecessors:** [CY057](planning-artifacts-mutation.md#cy057).
- **Shared-file predecessors:** [CY055](planning-artifacts-mutation.md#cy055).
- **Authority:** [DI-04 §§4.10,7.1; Shared §11.1](design-mutation-validation.md).
- **CY058.D1 — bounded result:** Introduce final SafeEditTool in mcp_server/tools/edit_tool.py, composed only in isolated target tests before cutover. Do not alter the registered legacy safe_edit_tool.py route.
- **Preserved behavior:** 14 exact mutation error details, validation_policy/status and actual persistence facts; unrelated wrapper semantics.
- **CY058.D2 — independent evidence:** Real wrapper/cache/text proves every edit operation, enforce/report, all applicable exact error details, no-change/concurrency/partial reporting and required-null facts; legacy modes rejected only in target composition.
- **Rollback:** R-CY058: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY058.D1 and CY058.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C106, S003, S004, S007, S009, S010, T007, T022, T048, T072, T099, T102, T134.

Read-only review/preservation IDs: C086. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/tools/edit_tool.py`
- `tests/mcp_server/integration/test_edit_public_v3.py`

Previously introduced paths revisited in this cycle:

- `mcp_server/schemas/mutation_outputs.py`

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/test_edit_public_v3.py`

Existing affected test/helper sources: S007, S009, S010, T007, T022, T048, T072, T099, T102, T134. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY058, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY059

**Check public composition**

- **Semantic predecessors:** [CY008](planning-execution.md#cy008), [CY009](planning-execution.md#cy009), [CY011](planning-execution.md#cy011), [CY026](planning-execution.md#cy026).
- **Shared-file predecessors:** [CY058](planning-artifacts-mutation.md#cy058), [CY057](planning-artifacts-mutation.md#cy057), [CY017](planning-execution.md#cy017).
- **Authority:** [DI-05 §13.1](design-execution-adapters.md).
- **CY059.D1 — bounded result:** Thin run_checks tool and exact eight operation error-detail shapes in isolated V3 registration.
- **Preserved behavior:** Native negative findings remain operational success; scope/args/defaults and no-state-touch evidence.
- **CY059.D2 — independent evidence:** Real decorated calls and cache reads cover check results, process capture, required nulls, invalid_request and not_started; direct native evidence reused.
- **Rollback:** R-CY059: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY059.D1 and CY059.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C106, C124, S003, S004, S007, S009, S010, T006, T048, T072, T075, T099, T107, T115, T117, T128, T131, T133, T134, T139, T148, T151.

Read-only review/preservation IDs: C086. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/tools/check_tools.py`
- `tests/mcp_server/integration/test_checks_public_v3.py`
- `mcp_server/schemas/execution_outputs.py`
- `mcp_server/services/check_operation.py`

Previously introduced paths revisited in this cycle:

- `mcp_server/execution/check_selection.py`
- `tests/mcp_server/unit/execution/test_check_selection.py`

Additional existing paths:

- `mcp_server/core/interfaces/git.py`
- `mcp_server/adapters/git_adapter.py`

Independent QA identified this bounded scope completion on 2026-09-14 under the user's standing authorization for proportionate QA corrections. The inward operation owns projection; selection retains its chosen profile and factual scope failures; Git distinguishes observed missing parent/merge-base facts. Preserve exception compatibility and other Git failures. No second resolver, shared executor change, new selection policy or live registration cutover.

- Selection, native facts, capture and role results keep their own declared contracts; do not normalize check/test/fix into one success reducer.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/test_checks_public_v3.py`

Existing affected test/helper sources: S007, S009, S010, T006, T048, T072, T075, T099, T107, T115, T117, T128, T131, T133, T134, T139, T148, T151. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY059, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY060

**Test public composition**

- **Semantic predecessors:** [CY008](planning-execution.md#cy008), [CY009](planning-execution.md#cy009), [CY011](planning-execution.md#cy011), [CY028](planning-execution.md#cy028).
- **Shared-file predecessors:** [CY059](planning-artifacts-mutation.md#cy059).
- **Authority:** [DI-05 §§7.15,13.1](design-execution-adapters.md).
- **CY060.D1 — bounded result:** Framework-neutral run_tests and concrete public records in isolated V3 registration.
- **Preserved behavior:** Native outcomes/coverage/collection/no-tests distinct from operational error; closed variant serialization.
- **CY060.D2 — independent evidence:** Real wrappers/cache/presenter; remove test-authored execute substitutes in touched suites; preserve ordinary non-test-tool behavior.
- **Rollback:** R-CY060: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY060.D1 and CY060.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C106, S003, S004, S007, S009, S010, T006, T048, T072, T075, T099, T106, T127, T134, T137, T140.

Read-only review/preservation IDs: C086. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/tools/run_tests_tool.py`
- `tests/mcp_server/integration/test_tests_public_v3.py`

Previously introduced paths revisited in this cycle:

- `mcp_server/schemas/execution_outputs.py`

- Selection, native facts, capture and role results keep their own declared contracts; do not normalize check/test/fix into one success reducer.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/test_tests_public_v3.py`

Existing affected test/helper sources: S007, S009, S010, T006, T048, T072, T075, T099, T106, T127, T134, T137, T140. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY060, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.

## CY061

**Fix public composition**

- **Semantic predecessors:** [CY008](planning-execution.md#cy008), [CY009](planning-execution.md#cy009), [CY011](planning-execution.md#cy011), [CY030](planning-execution.md#cy030).
- **Shared-file predecessors:** [CY060](planning-artifacts-mutation.md#cy060).
- **Authority:** [DI-05 §§7.18,13.1](design-execution-adapters.md).
- **CY061.D1 — bounded result:** Thin apply_fixes, exact attempted/unstarted rows and public stop behavior.
- **Preserved behavior:** Partial source effects truthful; no recheck/rollback guarantee or inferred changed-file census.
- **CY061.D2 — independent evidence:** Registered 3-step native/fault cases, cache/required null/FIFO evidence, no duplicate success source.
- **Rollback:** R-CY061: record the exact pre-cycle SHA, listed dirty-file preimages and cycle-owned inverse diff; apply the hub's scoped recovery procedure. Revert newly introduced files only if still cycle-owned. F-10 activation recovery and F-20 partial-write behavior remain separate.
- **Stop/go boundary:** CY061.D1 and CY061.D2 satisfy the card's exact scope, preserved behavior and Design authority; all semantic/shared-file predecessors are complete and still valid. Stop on any missing/failed observation, unresolved caller/import, unavailable native/startup prerequisite, out-of-set write, unusable recorded recovery route or Strategy/Design contradiction. Independent QA determines progression; file presence is not behavioral proof.

### Explicit write-set

Existing source IDs: C106, S003, S004, S007, S009, S010, T006, T048, T072, T075, T099, T112, T134, T136.

Read-only review/preservation IDs: C086. For a previously deleted source this means absence/import-closure review, never recreation.

New exact paths:

- `mcp_server/tools/fix_tools.py`
- `tests/mcp_server/integration/test_fixes_public_v3.py`

Previously introduced paths revisited in this cycle:

- `mcp_server/schemas/execution_outputs.py`

- Selection, native facts, capture and role results keep their own declared contracts; do not normalize check/test/fix into one success reducer.

Scope is limited to D1 and these enumerated paths. All unrelated behavior, all other file slices and all paths outside this set are excluded. Shared-file ownership grants only the stated seam; it is never blanket refactoring permission.

### Focused verification

Named durable proof files:

- `tests/mcp_server/integration/test_fixes_public_v3.py`

Existing affected test/helper sources: S007, S009, S010, T006, T048, T072, T075, T099, T112, T134, T136. Adapt or retire only their mapped Design claims. A removed test is not executable evidence: run its named successor, retain unrelated assertions, and record the removal/import-closure observation separately.

Apply hub V1–V6. Run focused surviving tests and gates on the surviving production/test write-set; docs-only slices use semantic/link/source-copy checks. Capture exact calls, native/interpreter versions, cached result resources, per-claim outcomes, R-CY061, invalidated prior evidence and an outcome-neutral independent review request. No full-suite or branch-wide run belongs to this cycle.
