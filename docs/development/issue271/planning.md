<!-- docs\development\issue271\planning.md -->
<!-- template=planning version=130ac5ea created=2026-05-02T09:03Z updated= -->
# contracts.yaml as SSOT for workflow-phase membership — Implementation Planning

**Status:** DRAFT  
**Version:** 2.2  
**Last Updated:** 2026-05-02

---

## Purpose

Break down de 12 migratiestappen uit design.md §3.5 in 6 sequentiële TDD-cycli. Elke cyclus richt zich op een coherente laag van de stack. C5a isoleert de 12 blast-radius testbestanden met verouderde API-verwijzingen, zodat C5 uitvoerbaar blijft als nette TDD-cyclus.

## Scope

**In Scope:**
Schema-klassen in contracts_config.py (rename + nieuwe klassen + PhaseContractPhase frozen); Loader: load_contracts_config + contracts.yaml YAML-restructuur (alle 6 workflows); Resolver: PhaseConfigContext + PhaseContractResolver; Runtime consumers: PhaseStateEngine, ProjectManager, CreateIssueTool; Blast-radius testfile updates (12 bestanden in C5a); Validator-inversie + WorkflowTemplate.phases-verwijdering + server.py composition root

**Out of Scope:**
Geen compat-shims of dual-read paths; geen wijzigingen in workphases.yaml-inhoud of schema; geen wijzigingen in enforcement.yaml buiten §3.2-beslissingen; geen frontend- of CLI-wijzigingen

## Prerequisites

Read these first:
1. design.md v2.3 QA GO (subphase formalisering doorstaan)
2. Branch refactor/271-phase-contracts-ssot-workflow-membership actief
3. research.md v3.2 committed (blast radius 12 prod + 17 testfiles; subphase scan)
---

## Summary

Refactor voor issue #271: migratie van twee-SSOT (workflows.yaml + phase_contracts.yaml) naar één SSOT (contracts.yaml). De migratie verloopt in 6 TDD-cycli, strict afhankelijk geordend. Geen shims; clean break in één PR. Blast radius: 13 productiefiles (inclusief YAML-rename), 17 testfiles (verdeeld over C1 t/m C5a).

---

## Dependencies

- C1 moet compleet zijn vóór elke andere cyclus
- C2 hangt af van C1
- C3 hangt af van C1 + C2
- C4 hangt af van C1 + C3
- C5a hangt af van C1 + C2 + C3 + C4 — alle productie-API’s zijn stabiel vóór testfile-update
- C5 hangt af van C1 + C2 + C3 + C4 + C5a

---

## TDD Cycles


### Cycle 1: C1 — Schema foundation: contracts_config.py

**Goal:** Hernoem module phase_contracts_config.py → contracts_config.py; voeg ConfigDict(extra='forbid', frozen=True) toe aan PhaseContractPhase; voeg WorkflowPhaseEntry, WorkflowEntry, ContractsConfig toe met volledige API (get_first_phase, get_phases, validate_transition, _get_workflow, model_validator); update interne + publieke re-exports (__init__.py x2).

**Tests:**
- PhaseContractPhase: assert frozen — assignment raises ValidationError
- PhaseContractPhase: extra='forbid' rejects unknown fields
- PhaseContractPhase: bestaande model_validator enforces cycle_based → non-empty commit_type_map
- WorkflowPhaseEntry: erft frozen + extra='forbid' van parent
- WorkflowPhaseEntry: name-veld verplicht; ontbrekende naam geeft ValidationError
- WorkflowEntry: extra='forbid'; frozen; phases min_length=1 gehandhaafd
- ContractsConfig: model_validator enforces laatste fase == merge_policy.pr_allowed_phase
- ContractsConfig: model_validator gooit ValueError met beschrijvende melding bij mismatch
- ContractsConfig.get_first_phase: retourneert eerste faasnaam; gooit ValueError voor onbekende workflow
- ContractsConfig.get_phases: retourneert geordende lijst; gooit ValueError voor onbekende workflow
- ContractsConfig.validate_transition: happy path sequentieel retourneert True
- ContractsConfig.validate_transition: niet-sequentieel gooit ValueError met hint
- ContractsConfig.validate_transition: onbekende fase gooit ValueError met beschikbare lijst
- Import van oud pad mcp_server.config.schemas.phase_contracts_config gooit ImportError
- Import van nieuw pad mcp_server.config.schemas.contracts_config werkt voor alle publieke symbolen
- WorkflowPhaseEntry: name='research' met cycle_based=true en subphases=['explore', 'consolidate'] is geldig — schema bevat geen fasename-checks op 'implementation'

**Success Criteria:**
- Alle 16 nieuwe tests slagen
- Bestaande tests voor BranchLocalArtifact, MergePolicy, CheckSpec nog steeds groen (geen regressie)
- mypy/ruff clean op contracts_config.py, config/schemas/__init__.py en schemas/__init__.py
- ContractsConfig, WorkflowEntry, WorkflowPhaseEntry importeerbaar via mcp_server.config.schemas en mcp_server.schemas



### Cycle 2: C2 — Loader + YAML: load_contracts_config + contracts.yaml restructuur

**Goal:** Hernoem load_phase_contracts_config → load_contracts_config in loader.py; update bestandsnaamconstante naar contracts.yaml; verwijder _inject_terminal_phase volledig; hernoem .st3/config/phase_contracts.yaml → contracts.yaml en herstructureer naar list-of-objects conform design.md §3.3. Roundtrip-verificatie voor alle 6 productie-workflows.

**Tests:**
- load_contracts_config: laadt contracts.yaml succesvol en retourneert ContractsConfig
- load_contracts_config: gooit ConfigError (niet FileNotFoundError) als contracts.yaml ontbreekt — zelfde contract als voorganger
- load_contracts_config: gooit ConfigError met pad-display-string bij YAML-parsefout
- load_contracts_config: geladen object heeft correcte faseorde voor feature-workflow (research first, ready last)
- load_contracts_config: geladen object passeert ContractsConfig.model_validator
- _inject_terminal_phase: functie bestaat niet meer in loader-module
- load_phase_contracts_config: functie bestaat niet meer in loader-module (verwijderd, niet hernoemd)
- ContractsConfig roundtrip feature-workflow: parsed object matches handcrafted expected-object field-for-field
- ContractsConfig roundtrip bug-workflow: parsed object matches handcrafted expected-object field-for-field
- ContractsConfig roundtrip hotfix-workflow: parsed object matches handcrafted expected-object field-for-field
- ContractsConfig roundtrip refactor-workflow: parsed object matches handcrafted expected-object field-for-field
- ContractsConfig roundtrip docs-workflow: parsed object matches handcrafted expected-object field-for-field
- ContractsConfig roundtrip epic-workflow: parsed object matches handcrafted expected-object field-for-field

**Success Criteria:**
- Alle 13 loader/YAML-tests slagen
- contracts.yaml parsed clean; alle 6 workflow-fasesequenties volledig behouden
- Geen _inject_terminal_phase-calls meer in codebase (grep-verificatie: 0 hits)
- mypy/ruff clean op loader.py

**Dependencies:** C1


### Cycle 3: C3 — Resolver: PhaseConfigContext + PhaseContractResolver

**Goal:** Hernoem PhaseConfigContext.phase_contracts: PhaseContractsConfig → contracts: ContractsConfig (D9). Update _PHASE_CONTRACTS_DISPLAY_PATH naar .st3/config/contracts.yaml. Update alle interne usages van het hernoemde veld in phase_contract_resolver.py.

**Tests:**
- PhaseConfigContext: veld contracts accepteert ContractsConfig-instantie
- PhaseConfigContext: veld phase_contracts bestaat niet meer (AttributeError bij toegang)
- PhaseContractResolver: resolveert fase-contract via nieuw contracts-veld
- PhaseContractResolver: display-pad-constante gelijk aan '.st3/config/contracts.yaml'

**Success Criteria:**
- Alle 4 resolver-tests slagen
- Geen verwijzingen naar PhaseConfigContext.phase_contracts meer in productiecode
- mypy/ruff clean op phase_contract_resolver.py

**Dependencies:** C1, C2


### Cycle 4: C4 — Runtime consumers: PhaseStateEngine, ProjectManager, CreateIssueTool

**Goal:** Vervang workflow_config: WorkflowConfig door contracts_config: ContractsConfig in __init__ van PhaseStateEngine (param 4/11), ProjectManager (param 2/6), CreateIssueTool (param 4/4). Tests verificiëren niet alleen constructor-signaturen maar ook eindgedrag: correcte retourwaarden, foutpropagatie en persistentie van required_phases.

**Tests:**
- PhaseStateEngine: accepteert contracts_config: ContractsConfig in constructor; workflow_config kwarg raises TypeError
- PhaseStateEngine: validate_transition retourneert None voor geldige transitie (research → design, feature-workflow)
- PhaseStateEngine: ValueError van contracts_config.validate_transition propagates ongewijzigd naar aanroeper
- ProjectManager: accepteert contracts_config: ContractsConfig in constructor; workflow_config kwarg raises TypeError
- ProjectManager: get_first_phase retourneert 'research' voor feature-workflow via contracts_config.get_first_phase
- ProjectManager: get_phases retourneert volledig geordende fasesequentie voor feature-workflow via contracts_config.get_phases
- ProjectManager: create_project_plan() slaat required_phases op conform contracts_config.get_phases() resultaat
- CreateIssueTool: accepteert contracts_config: ContractsConfig in constructor; workflow_config kwarg raises TypeError
- CreateIssueTool: issue-aanmaak leidt correcte eerste fase af via contracts_config.get_first_phase (retourwaarde geverifieerd, niet alleen delegatie)
- Mock DI fixture: manually assemble ContractsConfig into all three consumers — no server.py import (server.py wiring verified in C5)

**Success Criteria:**
- Alle 10 consumer-tests slagen
- Geen verwijzingen naar workflow_config-parameternaam in de drie consumerfiles
- Geen aanroepen van WorkflowConfig.get_first_phase of validate_transition in productiecode
- mypy/ruff clean op phase_state_engine.py, project_manager.py, issue_tools.py

**Dependencies:** C1, C3


### Cycle 5: C5a — Blast-radius testfile updates

**Goal:** Update alle 12 blast-radius testbestanden die verwijzen naar verouderde API (phase_contracts.yaml pad, PhaseContractsConfig, load_phase_contracts_config, workflow_config, PhaseConfigContext.phase_contracts). Alle bestanden moeten slagen met de nieuwe productie-API. Geen functionele wijzigingen aan productiecode in deze cyclus.

**Tests:**
- test_workflow_config.py: get_first_phase + validate_transition tests verwijderd of geadapteerd; WorkflowTemplate.phases-test verwijderd
- workflow_fixtures.py: helper-functies bijgewerkt naar ContractsConfig; geen PhaseContractsConfig-verwijzingen meer
- test_support.py: phase_contracts.yaml pad vervangen door contracts.yaml; load_phase_contracts_config vervangen; PhaseContractsConfig vervangen door ContractsConfig
- test_phase_contracts_schema.py: imports bijgewerkt; PhaseContractsConfig-constructie vervangen door ContractsConfig
- test_label_startup.py: 7+ fixture-methoden bijgewerkt; ContractsConfig gebruikt in plaats van PhaseContractsConfig
- test_validator_c3.py: PhaseContractsConfig import vervangen; instanties herbouwd als ContractsConfig
- test_submit_pr_atomic_flow.py: 4 hardcoded 'phase_contracts.yaml' paden vervangen door 'contracts.yaml'
- test_c_loader_structural.py: 'phase_contracts.yaml' pad vervangen; load_phase_contracts_config vervangen; PhaseContractsConfig vervangen
- test_phase_state_engine_c1.py: temp 'phase_contracts.yaml' fixture vervangen door contracts.yaml
- test_phase_state_engine_c2.py: temp 'phase_contracts.yaml' fixture vervangen door contracts.yaml
- test_phase_state_engine_c4_issue257.py: temp 'phase_contracts.yaml' fixture vervangen door contracts.yaml
- test_cycle_tools_legacy.py: temp 'phase_contracts.yaml' fixture vervangen door contracts.yaml

**Success Criteria:**
- Alle 12 blast-radius testbestanden slagen na bijwerken
- Geen string-verwijzingen naar 'phase_contracts.yaml' in de 12 bestanden (grep: 0 hits)
- Geen imports van PhaseContractsConfig of load_phase_contracts_config in de 12 bestanden
- mypy/ruff clean op alle bijgewerkte testbestanden

**Dependencies:** C1, C2, C3, C4


### Cycle 6: C5 — Validator inversie + WorkflowTemplate cleanup + composition root

**Goal:** Inverteer startup-validator: validator.py controleert nu dat fases in contracts.yaml bestaan in workphases.yaml-catalogus. Verwijder WorkflowTemplate.phases-veld en WorkflowConfig.get_first_phase / validate_transition uit workflows.py. Update .st3/config/workflows.yaml (verwijder phases:-lijsten). Update server.py composition root. Update agent.md: bestandsnaamverwijzing (r.370) bijwerken naar contracts.yaml én §2.3 implementation-only subphase-formulering (r.121, r.132, r.263) vervangen door cycle_based-config-gedreven formulering.

**Tests:**
- Validator: fasenaam in contracts.yaml die ontbreekt in workphases.yaml gooit ConfigError bij startup
- Validator: alle fases aanwezig in workphases.yaml → validatie slaagt
- WorkflowTemplate: phases-veld bestaat niet meer (AttributeError)
- WorkflowConfig.get_first_phase: methode bestaat niet meer (AttributeError)
- WorkflowConfig.validate_transition: methode bestaat niet meer (AttributeError)
- WorkflowConfig.has_workflow + get_workflow: bestaan nog en retourneren correcte metadata
- Integratie: server.py-fixture start succesvol met contracts.yaml als ContractsConfig
- Integratie: fase-transitie end-to-end (initialize → transition → validate) gebruikt ContractsConfig door de hele stack

**Success Criteria:**
- Alle 6 unit-tests + 2 integratietests slagen
- Geen phases:-sleutel in .st3/config/workflows.yaml
- Geen WorkflowTemplate.phases of WorkflowConfig.get_first_phase / validate_transition in productiecode
- Volledige testsuite groen (C5a reeds afgerond: geen blast-radius schuld in deze cyclus)
- mypy/ruff clean op validator.py, workflows.py, server.py
- agent.md documentatieverwijzing bijgewerkt naar contracts.yaml én §2.3 implementation-only subphase-formulering (r.121, r.132, r.263) vervangen door cycle_based-config-gedreven formulering
- Geen `if phase_name == "implementation"` of equivalent fasename-hardcoding voor subphase-dispatch in productiecode

**Dependencies:** C1, C2, C3, C4, C5a

---

## Risks & Mitigation

- **Risk:** PhaseContractPhase frozen=True kan bestaande tests breken die PhaseContractPhase construeren met post-init mutatie
  - **Mitigation:** Audit bestaande PhaseContractPhase-testfixtures in C1 RED-fase; vervang mutatiepatronen door nieuwe modelinstantie
- **Risk:** contracts.yaml YAML-restructuur (list-of-objects) moet alle fase-contracten exact bewaren voor alle 6 workflows; een omissie breekt runtime-validatie pas bij fase-gebruik
  - **Mitigation:** C2 bevat 6 afzonderlijke roundtrip-tests (één per workflow): geparsed ContractsConfig moet veld-voor-veld overeenkomen met een handcrafted expected-object
- **Risk:** C4 gedragstests gebruiken een mock ContractsConfig; een te permissieve mock maskeert een productie-bug totdat C5 integratietests falen
  - **Mitigation:** Gebruik dezelfde YAML-structuur als in de C2-roundtrip-tests als basis voor C4-fixtures; geen hand-gemaakte stub-workflows die afwijken van productie-contracts.yaml
- **Risk:** Runtime-consumers (`scope_encoder.py`, `phase_state_engine.py`) bevatten mogelijk fasename-specifieke conditionals die §3 Config-First schenden en pas zichtbaar worden bij het toevoegen van een tweede `cycle_based`-fase
  - **Mitigation:** Verifieer aan het begin van C1 RED dat geen `if phase_name == "implementation"`-equivalent bestaat in de subphase-dispatch-paden (scan: `phase_contract_resolver.py`, `scope_encoder.py`, `phase_detection.py`, `phase_state_engine.py`). Huidige scan: `scope_encoder` en `phase_detection` zijn clean; `phase_state_engine` heeft een naming-issue (`on_enter_implementation_phase`) maar geen logische fasename-check — geen C1-blocker, scope in C4 (rename hooks).

---

## Milestones

- C1 GREEN: ContractsConfig importeerbaar en volledig getypeerd — blokkeert alle downstream cycli
- C2 GREEN: contracts.yaml laadt end-to-end voor alle 6 workflows — blokkeert resolver en integratietests
- C5a GREEN: alle 12 blast-radius testbestanden bijgewerkt en slagend — blokkeert C5
- C5 GREEN + volledige suite groen: PR-ready state

## Related Documentation
- **[docs/development/issue271/research.md — blast radius mapping en open vragen][related-1]**
- **[docs/development/issue271/design.md — schema-specs (§3.2), migratievolgorde (§3.5), constructor-signaturen (§3.7)][related-2]**

<!-- Link definitions -->

[related-1]: docs/development/issue271/research.md — blast radius mapping en open vragen
[related-2]: docs/development/issue271/design.md — schema-specs (§3.2), migratievolgorde (§3.5), constructor-signaturen (§3.7)

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-02 | Agent | Initial scaffold (QA NOGO: 5 cycli onvoldoende, C5a ontbrak, blast-radius onvolledig) |
| 2.0 | 2026-05-02 | Agent | QA NOGO resolved: 6 cycli (C1–C5+C5a); 12 blast-radius testbestanden in C5a; milestone-sectie toegevoegd |
| 2.1 | 2026-05-02 | Agent | QA Hercheck N-1/N-2/N-3 resolved: C5a.files → 12 bestanden incl. test_cycle_tools_legacy.py; C5a cycle_number=5 / C5 cycle_number=6 (deliverables.json was omgewisseld) |
| 2.2 | 2026-05-02 | Agent | Subphase formalisering: C1 test 16 (schema-genericiteit name='research'); success criteria 15→16; C5 goal + success criteria uitgebreid naar agent.md §2.3 r.121/r.132/r.263; risk-entry voor subphase-dispatch hardcoding |