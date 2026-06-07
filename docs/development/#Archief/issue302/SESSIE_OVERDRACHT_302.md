# Sessie Overdracht — Issue #302
# Align labels config, GitHub labels, and docs

**Datum:** 2026-05-06
**Branch:** `fix/302-align-labels-config-github-docs`
**Fase:** research (voltooid, klaar voor transitie naar design)
**Machine:** overdracht naar andere machine

---

## Status

Research en design zijn geschreven en door QA gereviewd (twee rondes).

| Deliverable | Status |
|-------------|--------|
| `docs/development/issue302/research.md` | FINAL |
| `docs/development/issue302/design.md` | FINAL (behoudens B-1 fix hieronder) |
| QA ronde 1 (door impl-agent zelf) | CONDITIONAL GO → alle findings verwerkt |
| QA ronde 2 (door gebruiker + externe QA) | **NOGO** op B-1 |

---

## Open Blocker — B-1 (`phase:done` bestaat niet in labels.yaml)

**Probleem:** Design Decision 3b vervangt `status:resolved` op lijn 270 van `github.md`
door `phase:done`. Maar `phase:done` staat **niet** in `labels.yaml`.

Aanwezige `phase:*` labels in `labels.yaml`:
```
phase:research, phase:planning, phase:design, phase:tdd,
phase:red, phase:green, phase:refactor, phase:integration, phase:documentation
```

Ontbrekend in `labels.yaml` (wel in `workphases.yaml`):
```
phase:validation, phase:ready, phase:coordination
```

Ontbrekend in `workphases.yaml` (wel in `labels.yaml`):
```
phase:integration  (= stale, staat nergens in de workflow)
phase:tdd          (= alias voor implementation, commit-level granulariteit)
```

**Besluit voor B-1 (lijn 270 github.md):**
Vervang `status:resolved` door **niets** (remove-only) of door `phase:documentation`
(dichtstbijzijnde geldige fase). Gebruiker-voorkeur: `phase:documentation`.

**Besluit voor lijn 292 github.md (pre-existing `phase:done`):**
Eveneens vervangen door `phase:documentation` — dit is dezelfde correctie.

**Acties in design.md:**
- Decision 3b tabel: lijn 270 → `"phase:documentation"` i.p.v. `"phase:done"`
- Decision 3b tabel: lijn 292 → `"phase:documentation"` (pre-existing fout, ook fixen)
- Risk tabel rij 3: claim "All replacement labels verified" is dan correct

---

## Nieuwe Finding — SSOT-schending: labels.yaml vs workphases.yaml

**Gevonden tijdens B-1 analyse.** Nog niet opgenomen in research of design.

### Wat er speelt

`labels.yaml` (`label_patterns` + `labels[].name`) en `workphases.yaml` (`phases` dict)
zijn twee onafhankelijke bronnen voor fase-namen. Elke fase-toevoeging in `workphases.yaml`
vereist een handmatige update in `labels.yaml` — dat is een §2 DRY+SSOT schending.

### Divergenties (huidig)

| Fase | workphases.yaml | labels.yaml |
|------|-----------------|-------------|
| `research` | ✅ | ✅ `phase:research` |
| `planning` | ✅ | ✅ `phase:planning` |
| `design` | ✅ | ✅ `phase:design` |
| `implementation` | ✅ (met subphases red/green/refactor) | ✅ `phase:tdd` (alias), `phase:red`, `phase:green`, `phase:refactor` |
| `validation` | ✅ | ❌ ontbreekt |
| `documentation` | ✅ | ✅ `phase:documentation` |
| `coordination` | ✅ | ❌ ontbreekt |
| `ready` | ✅ (terminal) | ❌ ontbreekt |
| `integration` | ❌ ontbreekt | ✅ `phase:integration` (stale) |

### Aanbevolen aanpak (besproken)

Drie opties zijn geanalyseerd:

**Optie A — Dynamic pattern** (`^phase:[a-z][a-z0-9-]*$` in `label_patterns`)
- Pro: labels.yaml declareert geen fase-namen meer; workphases.yaml is enige bron
- Con: verliest typo-validatie; elke string als `phase:xyz` is geldig

**Optie B — ConfigLoader cross-validatie (aanbevolen, als apart issue)**
- `ConfigLoader` valideert bij startup: `labels.yaml phase:* set == workphases.yaml phases`
- Pro: Fail-Fast (§4); beide bestanden blijven leesbaar; mismatch bij startup zichtbaar
- Con: twee-plaatsen-schrijven blijft bestaan; check compenseert structureel

**Optie C — Sync nu, in #302 scope (minimale fix)**
- Voeg `phase:validation`, `phase:ready`, `phase:coordination` toe aan `labels.yaml`
- Verwijder `phase:integration` (niet in workphases.yaml → stale)
- Pro: inhoudelijk correct, minimale impact
- Con: structurele duplicatie blijft

### Besluit voor #302

- **Minimale sync in #302** (Optie C beperkt): voeg `phase:validation` en `phase:ready`
  toe aan `labels.yaml` (nodig om doc-voorbeelden niet te laten liegen). `phase:coordination`
  optioneel. `phase:integration` laten staan tenzij er een actieve beslissing over genomen
  is.
- **Nieuw issue aanmaken** voor Optie B (ConfigLoader cross-validatie). Nog niet gedaan.

---

## Nog te doen (volgende sessie)

### Stap 1 — design.md bijwerken (B-1 fix)

In `docs/development/issue302/design.md`:
- Decision 3b tabel: lijn 270 en 292 → `phase:documentation` (niet `phase:done`)
- Risk tabel: rij 3 claim aanpassen

### Stap 2 — labels.yaml uitbreiden (Optie C, beperkt)

In `.st3/config/labels.yaml`:
- Toevoegen: `phase:validation` (color: `C5DEF5`, description: "Validation phase")
- Toevoegen: `phase:ready` (color: `0E8A16`, description: "Ready for merge / terminal phase")
- Besluit over `phase:integration` en `phase:coordination`: nader bepalen

### Stap 3 — research.md bijwerken

Voeg §3.4 toe: "Sub-problem D — labels.yaml vs workphases.yaml divergentie" met verwijzing
naar de nieuwe issue voor ConfigLoader cross-validatie.

### Stap 4 — design.md bijwerken

Voeg Decision 4 toe: sync `labels.yaml` met `workphases.yaml` (de minimale Optie C stap).
Nieuw TDD-cycle niet nodig (geen code-change; alleen config + test_labels_yaml_conventions.py
checken of tests nog passen).

### Stap 5 — QA goedkeuring opnieuw halen

Laat QA sub-agent opnieuw reviewen met de bijgewerkte research + design.

### Stap 6 — Transitie naar planning en implementatie

Na QA GO: `transition_phase(to_phase="design")` → `transition_phase(to_phase="planning")`.

---

## Relevante bestanden

| Bestand | Doel |
|---------|------|
| `docs/development/issue302/research.md` | Onderzoek (FINAL, aanvulling nodig voor stap 3) |
| `docs/development/issue302/design.md` | Ontwerp (B-1 fix + Decision 4 nodig) |
| `mcp_server/tools/label_tools.py` | Productie-bug (AddLabelsTool L186 + DetectLabelDriftTool) |
| `tests/mcp_server/unit/tools/test_label_tools_integration.py` | Tests (L146 + L184 bijwerken + 2 nieuwe tests) |
| `docs/mcp_server/GITHUB_SETUP.md` | Doc §4.4 herschrijven |
| `docs/reference/mcp/tools/github.md` | 7 locaties status:* vervangen |
| `.st3/config/labels.yaml` | phase:validation + phase:ready toevoegen |
| `.st3/config/workphases.yaml` | Referentie SSOT voor fases (niet wijzigen) |

---

## Git-staat bij overdracht

- Branch: `fix/302-align-labels-config-github-docs`
- Commits op branch:
  - `e9944a14` — initialize project for issue #302
  - (plus deze commit met research + design)
- Geen werkende tree wijzigingen na commit
