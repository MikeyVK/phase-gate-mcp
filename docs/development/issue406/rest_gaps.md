<!-- docs\development\issue406\rest_gaps.md -->
<!-- template=generic_doc version=43c84181 created=2026-06-24T05:42Z updated=2026-06-24T07:48Z -->
# Remaining Gaps: Presentation Layer & DTO Refactoring

**Status:** APPROVED  
**Version:** 1.0.0  
**Last Updated:** 2026-06-24

---

## Purpose

To document the remaining architectural gaps identified during Issue #406 regarding text presentation and error DTO structures, outlining the approved design for future implementation sessions.

## Scope

**In Scope:**
Sanitization of BaseToolOutput, creation of BaseErrorOutput, status resolution updates in server.py and text_presenter.py, and declarative template mapping in presentation.yaml.

**Out of Scope:**
Implementation changes on the active branch (feature/406), which is being closed. These steps will be implemented in subsequent issues.

---

## Summary

This document records the design and implementation roadmap for resolving the backdoor in BaseToolOutput (error_message) and decoupling system errors from tool-level domain errors using the BaseErrorOutput hierarchy.

---

## Key Changes

### 1. Fase-transitie & Onderzoek
* **Gap-documentatie:** De branche is tijdelijk teruggezet naar `research` om de systeembrede gaps ([research_arch_gap.md](file:///c:/temp/pgmcp/docs/development/issue406/research_arch_gap.md)) en de `get_work_context` gaps ([research_get_work_context_gaps.md](file:///c:/temp/pgmcp/docs/development/issue406/research_get_work_context_gaps.md)) gestructureerd en gecommit vast te leggen. Daarna is de branche succesvol overgegaan naar de `design` fase.

### 2. `get_work_context` Presentatie-refactoring
* **Exponeren van metadata:** Compacte velden (`current_cycle`, `sub_phase`, `parent_branch`) worden direct in de markdown getoond om de agent beter te oriënteren.
* **Declaratieve None-afhandeling:** We gebruiken de bestaande [SafeNoneFormatter](file:///c:/temp/pgmcp/mcp_server/presenters/text_presenter.py#L25) (`none_value: "-"`) en schonen de templates in [presentation.yaml](file:///c:/temp/pgmcp/.phase-gate/config/presentation.yaml) op (bijv. `#` weglaten bij issues) om prefix-leaks zoals `#-` te voorkomen.
* **Oplossing voor grote instructies ("Niets-aanpak"):** We laten `phase_instructions` volledig uit de markdown weg om client-side file-truncation (`output.txt` dumps) te voorkomen. Dit combineren we met uiterst dwingende `todo_discipline` next-instruction die de agent dwingt de cache-resource (`pgmcp://cache/runs/{run_id}`) uit te lezen.
* **Sanering van de Tool-laag:** Alle hardcoded fallback-teksten en weergave-logica worden verwijderd uit [discovery_tools.py](file:///c:/temp/pgmcp/mcp_server/tools/discovery_tools.py) om te voldoen aan de Presentation Boundary (§15).

### 3. Sanering van `BaseToolOutput` & Backdoor-blokkade
* **Opschonen `BaseToolOutput`:** We verwijderen het veld `error_message` uit [BaseToolOutput](file:///c:/temp/pgmcp/mcp_server/schemas/tool_outputs.py#L14). Dit voorkomt dat tools in Python geformatteerde foutboodschappen direct teruggeven.
* **Declaratieve Domeinfouten:** Domein-fouten van tools (`success=False`) worden uitsluitend gepresenteerd via tool-specifieke `template_failure` templates in [presentation.yaml](file:///c:/temp/pgmcp/.phase-gate/config/presentation.yaml), geformatteerd met de specifieke data-attributen van die tool (geen backdoor-strings in Python).

### 4. Herontwerp van de Error-DTO's
* **Introductie van `BaseErrorOutput`:** We splitsen [error_outputs.py](file:///c:/temp/pgmcp/mcp_server/schemas/error_outputs.py) op. Systeem-, decorator- en platformfouten overerven direct van een nieuwe `BaseErrorOutput` die **geen** `success` bool bevat. Alleen echte tool-fouten (`ToolErrorOutput`) behouden de `success=False` property.
* **Type-safe status en routing:** De presenter [text_presenter.py](file:///c:/temp/pgmcp/mcp_server/presenters/text_presenter.py) en server-bridge [server.py](file:///c:/temp/pgmcp/mcp_server/server.py) bepalen de succes-status en de template-routing via type-checks (`isinstance(data, BaseErrorOutput)`) in plaats van broze string-filters op `error_type`.

### 5. Simpele exceptions (Tegen Class Bloat)
* **Generieke uitzonderingen:** We introduceren geen specifieke exception-klassen per fouttype. In plaats daarvan hergebruiken we de reeds bestaande generieke klassen uit [exceptions.py](file:///c:/temp/pgmcp/mcp_server/core/exceptions.py) (zoals [PreflightError](file:///c:/temp/pgmcp/mcp_server/core/exceptions.py#L122) en [ValidationError](file:///c:/temp/pgmcp/mcp_server/core/exceptions.py#L52)) door ze simpelweg te voorzien van een specifieke `error_code` en `params`.

---

## Related Documentation
- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md][related-1]**
- **[docs/development/issue406/research_get_work_context_gaps.md][related-2]**

<!-- Link definitions -->

[related-1]: docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
[related-2]: docs/development/issue406/research_get_work_context_gaps.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-24 | Agent | Initial draft |
