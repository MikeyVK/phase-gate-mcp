<!-- docs/development/issue136/SESSIE_OVERDRACHT_QA_20260508.md -->
<!-- template=planning version=130ac5ea created=2026-05-08T17:00Z updated= -->
# Issue136 Sessieoverdracht QA (2026-05-08)

**Status:** ACTIVE  
**Version:** 1.0  
**Last Updated:** 2026-05-08

---

## Purpose

Read-only QA-overdracht voor issue #136 (Error Taxonomy & Strict Input Validation) na tweede validatieronde.  
Eerste ronde (eerder vandaag): GO geconcludeerd na reparatie van B-1/N-1/N-3.  
Tweede ronde (deze sessie): NOGO — validiatiefase commit `dbee6a81` introduceert twee nieuwe blockers en één scope-overtreding.

---

## QA-oordeel

**Oordeel: NOGO**

Cycle 1, 2, 3 zijn inhoudelijk correct geïmplementeerd. De validiatiefase heeft echter wijzigingen aangebracht die buiten de issuescope vallen en bestaande groene tests breken.

---

## Bevestigd groen (Cycle 1–3)

- **Cycle 1 (Change B):** Alle 50 input models `extra="forbid"`, `schema_utils.py` aangemaakt, `BaseTool.input_schema` normaliseert via `resolve_schema_refs`. C9-test groen. ✅
- **Cycle 2 (Change A):** `_validate_tool_arguments` retourneert `ToolResult(is_error=True)` met `schema://validation` EmbeddedResource bij validatiefout. `isinstance(validated, ToolResult)` guard. ✅
- **Cycle 3 (Change C):** `del context` weg uit `ScaffoldArtifactTool`, `ArtifactManager.scaffold_artifact` + `TemplateScaffolder.validate/scaffold` accepteren `note_context`, `BlockerNote`/`RecoveryNote`/`SuggestionNote` geproduceerd. ✅
- **Issue #147:** `extra="forbid"` op alle ~50 models (C1) + `ToolResult.error` op validatiefout (C2) dekt de #147 acceptatiecriteria volledig. ✅
- **Testsuite (voor validiatiefase regressions):** 2198 passed, pre-existing `test_workflow_cycle_e2e` failure is identiek op `main`. ✅

---

## Blockers die NOGO veroorzaken

### B-1 — `error_handling.py`: EmbeddedResource vervangen door text breekt 2 groene tests

**Commit:** `b17d712b` + `9fcd6f51`  
**Gewijzigde file:** `mcp_server/core/error_handling.py`

De `tool_error_handler` produceerde eerder (op `main`) een `schema://validation` EmbeddedResource als tweede content-item bij een `ValidationError` met schema. Commit `b17d712b` verving dit door een text-item (`"Input schema:\n{schema_text}"`); commit `9fcd6f51` verwijderde vervolgens het EmbeddedResource-item volledig.

**Gevolg:** `tests/mcp_server/integration/test_scaffold_validation_e2e.py` — 2 tests die op `main` groen waren en niet gewijzigd zijn op deze branch falen nu:

```
AssertionError: Should return resource with schema
assert 'text' == 'resource'
```

Deze tests waren groen op `main` en zijn niet door deze branch geïntroduceerd. Dit is een aantoonbare regressie.

**Design-contract:** Design.md D1-rationale stelt: *"Schema in ToolResult.content is consistent met `tool_error_handler` schema-resource precedent (DRY §2)"*. De EmbeddedResource in `tool_error_handler` was het gevestigde precedent; dat is nu verbroken.

**Vereiste fix:**  
Herstel `mcp_server/core/error_handling.py` naar de staat van `origin/main`:

```python
content: list[dict[str, Any]] = [
    {"type": "text", "text": message},
    {
        "type": "resource",
        "resource": {
            "uri": "schema://validation",
            "mimeType": "application/json",
            "text": json.dumps(exc.schema.to_dict(), indent=2),
        },
    },
]
```

Als text-readability gewenst is als extra, voeg dan een derde item toe — vervang de resource niet.

---

### B-2 — Scope-overtreding: 4 artifact-types disabled + V1-fallback verwijderd

**Commit:** `dbee6a81`  
**Gewijzigde files:** `mcp_server/managers/artifact_manager.py`, `.st3/config/artifacts.yaml`, `.st3/config/project_structure.yaml`, `tests/mcp_server/unit/config/test_artifacts_type_field_cycle1.py`

Commit `dbee6a81` verwijderde de V1-fallback (`use_v2_pipeline = False`) in `ArtifactManager.scaffold_artifact()` wanneer `context_class is None`. Als cascade-effect zijn vier artifact-types uitgeschakeld die geen V2-context-schema hebben: `adapter`, `resource`, `interface`, `tracking`.

**Wat er gewijzigd is:**
- `artifacts.yaml`: `adapter`, `resource`, `interface`, `tracking` zijn uitgecommentarieerd met verwijzing naar issue #325
- `project_structure.yaml`: alle `allowed_artifact_types` referenties naar deze types verwijderd
- `test_artifacts_type_field_cycle1.py`: verwachtingslijsten aangepast om de disabled types weg te laten

**Waarom dit buiten scope valt:**  
Design.md "Out of Scope" vermeldt de V1-fallback of artifact-type disabling niet. Het design beschrijft Change C als NoteContext-propagatie, niet als V2-pipeline herstructurering. De V1-fallback was defensieve backward-compatibility code; verwijdering ervan is een gedragswijziging met brede impact (al gebruikte workflows, tests, en artifact-configuratie) die een eigen issue/design/planning verdient.

**Vereiste fix:**  
Herstel de V1-fallback tak in `artifact_manager.py` (de `else: use_v2_pipeline = False` + `logger.warning`-tak uit `origin/main`), herstel de vier artifact-types in `artifacts.yaml` en `project_structure.yaml`, en herstel de testexpectaties.

De `TemplateSchema`-toevoeging aan de `ValidationError` (ook in `dbee6a81`) is wél in scope — die mag blijven.

---

## Observatie (niet-blokkerend)

### O-1 — `temp/test_output.txt` committed

**Commit:** `dbee6a81`

Een 4610-regel pytest-outputbestand is als onderdeel van een feature-commit opgenomen. `temp/` is deels getrackt in dit repo, maar `temp/test_output.txt` is duidelijk een debug-artefact.

**Fix:** `git rm temp/test_output.txt` in een opruimcommit voor de PR.

---

## Concrete backlog voor implementatie-agent

Volgorde van uitvoering:

1. **Herstel `error_handling.py`** (B-1): Zet het `schema://validation` EmbeddedResource-item terug. Controleer met `pytest tests/mcp_server/integration/test_scaffold_validation_e2e.py` — alle 3 moeten groen zijn.

2. **Herstel V1-fallback + artifact-types** (B-2): Zet `artifact_manager.py` regels 668–675 (de `if context_class is None: logger.warning + use_v2_pipeline = False`) terug naar `origin/main`. Herstel `artifacts.yaml` (4 types activeren), `project_structure.yaml` (referenties terugplaatsen), `test_artifacts_type_field_cycle1.py` (verwachtingen herstellen). De `TemplateSchema`-wijziging in `ValidationError` aanroep mag blijven.

3. **Verwijder `temp/test_output.txt`** (O-1): `git rm temp/test_output.txt`.

4. **Valideer finale staat**: `pytest tests/mcp_server/unit/ tests/mcp_server/integration/ -q --tb=no` — verwacht: alleen pre-existing `test_workflow_cycle_e2e` failure, alle overige groen.

---

## Teststatus op moment van overdracht

```
Branch: refactor/136-error-taxonomy-and-strict-input-validation
HEAD:   9fcd6f51

pytest tests/mcp_server/unit/ tests/mcp_server/integration/ -q --tb=no
  FAILED tests/mcp_server/integration/test_scaffold_validation_e2e.py::test_system_fields_filtered_from_schema   ← regressie B-1
  FAILED tests/mcp_server/integration/test_scaffold_validation_e2e.py::test_validation_error_returns_schema     ← regressie B-1
  FAILED tests/mcp_server/integration/test_workflow_cycle_e2e.py::test_full_workflow_cycle_with_scope_detection  ← pre-existing (identiek op main)
  5 failed, 2194 passed, 10 skipped, 6 xfailed
```

Na B-1 + B-2 fix verwachting:
```
  FAILED tests/mcp_server/integration/test_workflow_cycle_e2e.py::test_full_workflow_cycle_with_scope_detection  ← pre-existing
  1 failed, 2198+ passed
```

---

## Related Documentation

- [docs/development/issue136/design.md](design.md)
- [docs/development/issue136/planning.md](planning.md)
- [docs/development/issue136/research.md](research.md)
- [mcp_server/managers/artifact_manager.py](../../../mcp_server/managers/artifact_manager.py)
- [mcp_server/core/error_handling.py](../../../mcp_server/core/error_handling.py)
- [tests/mcp_server/integration/test_scaffold_validation_e2e.py](../../../tests/mcp_server/integration/test_scaffold_validation_e2e.py)

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-08 | QA Agent | Initiële QA-overdracht: NOGO na validiatiefase, 2 blockers + 1 observatie |
