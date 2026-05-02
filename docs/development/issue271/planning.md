<!-- docs\development\issue271\planning.md -->
<!-- template=planning version=130ac5ea created=2026-05-02T08:47Z updated= -->
# contracts.yaml as SSOT for workflow-phase membership — Implementation Planning

**Status:** DRAFT  
**Version:** 1.1  
**Last Updated:** 2026-05-02

---

## Purpose

Break down de 12 migratiestappen uit design.md §3.5 in 5 sequentiële TDD-cycli. Elke cyclus richt zich op een coherente laag van de stack, zodat tests groen zijn vóórdat de volgende laag wordt aangeraakt.

## Scope

**In Scope:**
Schema-klassen in contracts_config.py (rename + nieuwe klassen + PhaseContractPhase frozen); Loader: load_contracts_config + contracts.yaml YAML-restructuur; Resolver: PhaseConfigContext + PhaseContractResolver; Runtime consumers: PhaseStateEngine, ProjectManager, CreateIssueTool; Validator-inversie + WorkflowTemplate.phases-verwijdering + server.py composition root

**Out of Scope:**
Geen compat-shims of dual-read paths; geen wijzigingen in workphases.yaml-inhoud of schema; geen wijzigingen in enforcement.yaml buiten §3.2-beslissingen; geen frontend- of CLI-wijzigingen

## Prerequisites

Read these first:
1. design.md v2.2 QA GO (architectuurprincipes-check doorstaan)
2. Branch refactor/271-phase-contracts-ssot-workflow-membership actief
3. research.md v3.1 committed (blast radius 12 prod + 17 testfiles)
---

## Summary

Refactor voor issue #271: migratie van twee-SSOT (workflows.yaml + phase_contracts.yaml) naar één SSOT (contracts.yaml). De migratie verloopt in 5 TDD-cycli, strict afhankelijk geordend. Geen shims; clean break in één PR. Blast radius: 13 productiefiles (inclusief YAML-rename), 17 testfiles.

---

## Dependencies

- C1 moet compleet zijn vóór elke andere cyclus
- C3 hangt af van C1 + C2
- C4 hangt af van C1 + C3
- C5 hangt af van C1 + C2 + C3 + C4

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

**Success Criteria:**
- Alle 15 nieuwe tests slagen
- Bestaande tests voor BranchLocalArtifact, MergePolicy, CheckSpec nog steeds groen (geen regressie)
- mypy/ruff clean op contracts_config.py
- ContractsConfig, WorkflowEntry, WorkflowPhaseEntry importeerbaar via mcp_server.config.schemas en mcp_server.schemas



### Cycle 2: C2 — Loader + YAML: load_contracts_config + contracts.yaml restructuur

**Goal:** Hernoem load_phase_contracts_config → load_contracts_config in loader.py; update bestandsnaamconstante naar contracts.yaml; verwijder _inject_terminal_phase volledig; hernoem .st3/config/phase_contracts.yaml → contracts.yaml en herstructureer naar list-of-objects conform design.md §3.3.

**Tests:**
- load_contracts_config: laadt contracts.yaml succesvol en retourneert ContractsConfig
- load_contracts_config: gooit ConfigError (niet FileNotFoundError) als contracts.yaml ontbreekt — zelfde contract als voorganger
- load_contracts_config: gooit ConfigError met pad-display-string bij YAML-parsefout
- load_contracts_config: geladen object heeft correcte faseorde voor feature-workflow (research first, ready last)
- load_contracts_config: geladen object passeert ContractsConfig.model_validator
- _inject_terminal_phase: functie bestaat niet meer in loader-module
- load_phase_contracts_config: functie bestaat niet meer in loader-module (verwijderd, niet hernoemd)
- ContractsConfig roundtrip: parsed object matches handcrafted expected-object field-for-field (all workflow phases, all phase fields)

**Success Criteria:**
- Alle 8 nieuwe/bijgewerkte loader-tests slagen
- contracts.yaml parsed clean; alle bestaande workflow-fasesequenties behouden
- Geen _inject_terminal_phase-calls meer in codebase (grep-verificatie)
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
- Alle 4 nieuwe/bijgewerkte resolver-tests slagen
- Geen verwijzingen naar PhaseConfigContext.phase_contracts meer in productiecode
- mypy/ruff clean op phase_contract_resolver.py

**Dependencies:** C1, C2


### Cycle 4: C4 — Runtime consumers: PhaseStateEngine, ProjectManager, CreateIssueTool

**Goal:** Vervang workflow_config: WorkflowConfig door contracts_config: ContractsConfig in __init__ van PhaseStateEngine (param 4/11), ProjectManager (param 2/6), CreateIssueTool (param 4/4). Update interne usages van oude parameternaam en WorkflowConfig-API-methoden naar equivalente ContractsConfig-API. Volledige signaturen in design.md §3.7.

**Tests:**
- PhaseStateEngine: accepteert contracts_config: ContractsConfig in constructor; workflow_config kwarg raises TypeError
- PhaseStateEngine: validate_transition delegeert naar contracts_config.validate_transition
- ProjectManager: accepteert contracts_config: ContractsConfig in constructor; workflow_config kwarg raises TypeError
- ProjectManager: get_first_phase delegeert naar contracts_config.get_first_phase
- ProjectManager: get_phases delegeert naar contracts_config.get_phases
- CreateIssueTool: accepteert contracts_config: ContractsConfig in constructor; workflow_config kwarg raises TypeError
- CreateIssueTool: issue-aanmaak gebruikt contracts_config.get_first_phase voor eerste-fase-afleiding
- Mock DI fixture: manually assemble ContractsConfig into all three consumers — no server.py import (server.py wiring verified in C5)

**Success Criteria:**
- Alle 8 nieuwe/bijgewerkte consumer-tests slagen
- Geen verwijzingen naar workflow_config-parameternaam in de drie consumerfiles
- Geen aanroepen van WorkflowConfig.get_first_phase of validate_transition in productiecode
- mypy/ruff clean op phase_state_engine.py, project_manager.py, issue_tools.py

**Dependencies:** C1, C3


### Cycle 5: C5 — Validator inversie + WorkflowTemplate cleanup + composition root

**Goal:** Inverteer startup-validator: validator.py controleert nu dat fases in contracts.yaml bestaan in workphases.yaml-catalogus. Verwijder WorkflowTemplate.phases-veld en WorkflowConfig.get_first_phase / validate_transition uit workflows.py. Update .st3/config/workflows.yaml (verwijder phases:-lijsten). Update server.py composition root. Update agent.md documentatieverwijzing.

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
- Alle 8 nieuwe/bijgewerkte tests slagen inclusief 2 integratietests
- Geen phases:-sleutel in .st3/config/workflows.yaml
- Geen WorkflowTemplate.phases of WorkflowConfig.get_first_phase / validate_transition in productiecode
- Volledige testsuite groen (alle 17 blast-radius testfiles bijgewerkt en slagend)
- mypy/ruff clean op validator.py, workflows.py, server.py
- agent.md documentatieverwijzing bijgewerkt naar contracts.yaml

**Dependencies:** C1, C2, C3, C4

---

## Risks & Mitigation

- **Risk:** PhaseContractPhase frozen=True kan bestaande tests breken die PhaseContractPhase construeren met post-init mutatie
  - **Mitigation:** Audit bestaande PhaseContractPhase-testfixtures in C1 RED-fase; vervang mutatiepatterness door nieuwe modelinstantie
- **Risk:** contracts.yaml YAML-restructuur (list-of-objects) moet alle fase-contracten exact bewaren; eventuele omissie breekt runtime-validatie pas bij fase-gebruik
  - **Mitigation:** C2 RED bevat een roundtrip-test: geparsed ContractsConfig moet veld-voor-veld overeenkomen met een handcrafted expected-object
- **Risk:** 17 testfiles in blast radius; sommige kunnen indirecte afhankelijkheden hebben die niet in de 5 cycli zijn ondervangen
  - **Mitigation:** Run volledige testsuite aan het einde van elke cyclus (niet alleen gerichte tests); fix regressies vóór volgende cyclus

---

## Milestones

- C1 GREEN: ContractsConfig importeerbaar en volledig getypeerd — blokkeert alle downstream cycli
- C2 GREEN: contracts.yaml laadt end-to-end — blokkeert resolver en integratietests
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
| 1.0 |  | Agent | Initial draft |