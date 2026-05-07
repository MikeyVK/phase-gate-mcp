<!-- docs\development\issue136\research.md -->
<!-- template=research version=8b7bb3ab created=2026-05-07T15:54Z updated=2026-05-07T16:00Z -->
# Error Taxonomy & Strict Input Validation — Research

**Status:** COMPLETE  
**Version:** 1.0  
**Last Updated:** 2026-05-07  
**Issues:** #136 (error taxonomy) + #147 (extra=forbid, bundled deliverable)  
**Epic:** #320 fase 0

---

## Problem Statement

Predictable errors in de `scaffold_artifact → ArtifactManager → TemplateScaffolder → JinjaRenderer` keten
produceren generieke error codes (`ERR_CONFIG`, `ERR_VALIDATION`) die agents niet laten onderscheiden.
Tegelijk missen ~50 tool Input-modellen `extra="forbid"`, waardoor typo-velden stilzwijgend genegeerd worden.

---

## Research Goals

1. Inventariseer alle voorspelbare foutpaden in de scaffold-keten
2. Inventariseer alle tool Input-modellen zonder `extra="forbid"` (#147)
3. Definieer fout-taxonomie: error_code → NoteEntry-subtype
4. Documenteer boundary-regel (domein vs tool-grens)
5. Maak lijst van te raken bestanden voor implementatie

---

## 1. Foutpadanalyse: scaffold_artifact keten

### 1.1 Huidige exception-hiërarchie

```
MCPError(code="ERR_INTERNAL")
├─ ConfigError(code="ERR_CONFIG")       ← te breed
├─ ValidationError(code="ERR_VALIDATION") ← te breed
│   └─ MetadataParseError
├─ PreflightError(code="ERR_PREFLIGHT") ← correct granulaat
├─ ExecutionError(code="ERR_EXECUTION") ← te breed
└─ MCPSystemError(code="ERR_SYSTEM")    ← correct granulaat
```

De `ConfigError` en `ValidationError` codes zijn te breed: beide worden hergebruikt voor
meerdere niet-samenhangende condities.

### 1.2 Alle raise-sites in de scaffold-keten

#### ScaffoldArtifactTool.execute() — `mcp_server/tools/scaffold_artifact.py`
| # | Conditie | Huidige exception | Huidig code |
|---|----------|-------------------|-------------|
| S1 | `manager is None` | `ValueError` | – (bug: niet MCPError) |

#### ArtifactManager.scaffold_artifact() — `mcp_server/managers/artifact_manager.py`
| # | Conditie | Huidige exception | Huidig code |
|---|----------|-------------------|-------------|
| A1 | `artifact_type` onbekend in registry | `ConfigError` | `ERR_CONFIG` |
| A2 | `output_type == "file"` maar geen `output_path` | `ValidationError` | `ERR_VALIDATION` |
| A3 | `template_file is None` (template_path=null in YAML) | `ConfigError` | `ERR_CONFIG` |
| A4 | V2 context schema validatie (`model_validate`) mislukt | `ValidationError` | `ERR_VALIDATION` |
| A5 | `_enrich_context_v2`: `Context` klassenaam eindigt niet op "Context" | `ValidationError` | `ERR_VALIDATION` |
| A6 | `_enrich_context_v2`: `RenderContext` klasse niet gevonden in schemas | `ValidationError` | `ERR_VALIDATION` |
| A7 | Generic artifact zonder `output_path` in context | `ValidationError` | `ERR_VALIDATION` |
| A8 | Generated code artifact faalt validatie | `ValidationError` | `ERR_VALIDATION` |

#### TemplateScaffolder.validate() — `mcp_server/scaffolders/template_scaffolder.py`
| # | Conditie | Huidige exception | Huidig code |
|---|----------|-------------------|-------------|
| T1 | Geen template geconfigureerd voor type (v1 path) | `ValidationError` | `ERR_VALIDATION` |
| T2 | Template loader niet geconfigureerd | `ValidationError` | `ERR_VALIDATION` (misclassified: moet MCPSystemError zijn) |
| T3 | Vereiste velden ontbreken (introspectie) | `ValidationError` | `ERR_VALIDATION` |
| T4 | Generic without `template_name` in context of `template_path` | `ValidationError` | `ERR_VALIDATION` |

#### JinjaRenderer.get_template() — `mcp_server/scaffolding/renderer.py`
| # | Conditie | Huidige exception | Huidig code |
|---|----------|-------------------|-------------|
| J1 | Jinja2 `TemplateNotFound` | `ExecutionError` | `ERR_EXECUTION` |

#### FilesystemAdapter — `mcp_server/adapters/filesystem.py`
| # | Conditie | Huidige exception | Huidig code |
|---|----------|-------------------|-------------|
| F1 | Path buiten workspace (security boundary) | `ValidationError` | `ERR_VALIDATION` (misclassified: zou BlockerNote moeten triggeren) |
| F2 | Schrijven mislukt (OS fout) | `MCPSystemError` | `ERR_SYSTEM` |
| F3 | Lezen mislukt | `MCPSystemError` | `ERR_SYSTEM` |

#### ArtifactRegistryConfig.get_artifact() — `mcp_server/config/schemas/artifact_registry_config.py`
| # | Conditie | Huidige exception | Huidig code |
|---|----------|-------------------|-------------|
| R1 | `type_id` niet in registry | `ConfigError` | `ERR_CONFIG` (= A1, zelfde raise-site) |

---

## 2. Input-modellen zonder `extra="forbid"` (#147)

Enige model met `extra="forbid"`: `GitCommitInput` (`mcp_server/tools/git_tools.py:231`)

**Alle overige modellen (50) missen het:**

### git_tools.py
- `CreateBranchInput` (L85)
- `GitStatusInput` (L172)
- `GitRestoreInput` (L372)
- `GitCheckoutInput` (L412)
- `GitPushInput` (L481)
- `GitMergeInput` (L523)
- `GitDeleteBranchInput` (L561)
- `GitStashInput` (L599)
- `GetParentBranchInput` (L660)

### git_analysis_tools.py
- `GitListBranchesInput` (L13)
- `GitDiffInput` (L42)

### git_fetch_tool.py
- `GitFetchInput` (L39)

### git_pull_tool.py
- `GitPullInput` (L42)

### admin_tools.py
- `RestartServerInput` (L83)

### cycle_tools.py
- `TransitionCycleInput` (L38)
- `ForceCycleTransitionInput` (L140)

### discovery_tools.py
- `SearchDocumentationInput` (L31)
- `GetWorkContextInput` (L98)

### health_tools.py
- `HealthCheckInput` (L12)

### issue_tools.py
- `CreateIssueInput` (L99)
- `GetIssueInput` (L293)
- `ListIssuesInput` (L335)
- `UpdateIssueInput` (L372)
- `CloseIssueInput` (L417)

### label_tools.py
- `ListLabelsInput` (L16)
- `CreateLabelInput` (L53)
- `DeleteLabelInput` (L116)
- `RemoveLabelsInput` (L143)
- `AddLabelsInput` (L173)
- `DetectLabelDriftInput` (L224)

### milestone_tools.py
- `ListMilestonesInput` (L14)
- `CreateMilestoneInput` (L57)
- `CloseMilestoneInput` (L94)

### phase_tools.py
- `TransitionPhaseInput` (L34)
- `ForcePhaseTransitionInput` (L42)

### pr_tools.py
- `ListPRsInput` (L22)
- `MergePRInput` (L67)
- `SubmitPRInput` (L120)

### project_tools.py
- `InitializeProjectInput` (L32)
- `GetProjectPlanInput` (L288)
- `SavePlanningDeliverablesInput` (L377)
- `UpdatePlanningDeliverablesInput` (L467)

### quality_tools.py
- `RunQualityGatesInput` (L13)

### safe_edit_tool.py
- `SafeEditInput` (L105) — bevat al complexe nested modellen; voorzichtigheid geboden

### scaffold_artifact.py
- `ScaffoldArtifactInput` (L27)

### template_validation_tool.py
- `TemplateValidationInput` (L13)

### test_tools.py
- `RunTestsInput` (L26)

### validation_tools.py
- `ValidationInput` (L14)
- `ValidateDTOInput` (L45)

### code_tools.py
- `CreateFileInput` (L16)

**Totaal: 50 modellen zonder `extra="forbid"`**

---

## 3. Fout-taxonomie

### 3.1 Nieuwe error codes (als string-constanten in `mcp_server/core/exceptions.py`)

```python
# Artifact registry / config granulatie
ERR_ARTIFACT_TYPE_NOT_FOUND = "ERR_ARTIFACT_TYPE_NOT_FOUND"  # A1, R1
ERR_TEMPLATE_NOT_CONFIGURED = "ERR_TEMPLATE_NOT_CONFIGURED"  # A3, T1

# Template rendering granulatie
ERR_TEMPLATE_NOT_FOUND      = "ERR_TEMPLATE_NOT_FOUND"       # J1

# Input-validatie granulatie
ERR_MISSING_FIELD           = "ERR_MISSING_FIELD"            # T3, T4
ERR_EXTRA_FIELD             = "ERR_EXTRA_FIELD"              # extra="forbid" violations (nieuw)
ERR_MISSING_OUTPUT_PATH     = "ERR_MISSING_OUTPUT_PATH"      # A2, A7
ERR_CONTEXT_VALIDATION      = "ERR_CONTEXT_VALIDATION"       # A4

# Schema-resolutie granulatie (V2 pipeline)
ERR_SCHEMA_RESOLUTION       = "ERR_SCHEMA_RESOLUTION"        # A5, A6

# Gegenereerde-content validatie
ERR_GENERATED_CONTENT_INVALID = "ERR_GENERATED_CONTENT_INVALID"  # A8

# Security boundary
ERR_PATH_OUTSIDE_WORKSPACE  = "ERR_PATH_OUTSIDE_WORKSPACE"   # F1
```

### 3.2 NoteEntry-subtype per error code

| Error code | NoteEntry subtype | Semantiek |
|------------|-------------------|-----------|
| `ERR_ARTIFACT_TYPE_NOT_FOUND` | `SuggestionNote` | "Available types: dto, worker, …" |
| `ERR_TEMPLATE_NOT_CONFIGURED` | `SuggestionNote` | "Add template_path to artifact definition in artifacts.yaml" |
| `ERR_TEMPLATE_NOT_FOUND` | `SuggestionNote` | "Verify template file exists at path …" |
| `ERR_MISSING_FIELD` | `SuggestionNote` | "Provide missing fields: {fields}" |
| `ERR_EXTRA_FIELD` | `SuggestionNote` | "Remove unrecognized fields: {fields}" |
| `ERR_MISSING_OUTPUT_PATH` | `SuggestionNote` | "Pass output_path explicitly for file artifacts" |
| `ERR_CONTEXT_VALIDATION` | `SuggestionNote` | "Check context fields against schema for {artifact_type}" |
| `ERR_SCHEMA_RESOLUTION` | `SuggestionNote` | "Verify RenderContext class exists in mcp_server.schemas" |
| `ERR_GENERATED_CONTENT_INVALID` | `RecoveryNote` | "Check template for syntax errors; review generated content" |
| `ERR_PATH_OUTSIDE_WORKSPACE` | `BlockerNote` | "Path escapes workspace root — security boundary" |

### 3.3 Implementatie-strategie voor error codes

`ConfigError` en `ValidationError` accepteren al het `code`-argument via `MCPError.__init__`.
De subklassen override het met een vaste string. Oplossing:

**Optie A (aanbevolen):** Voeg optionele `code`-parameter toe aan `ConfigError.__init__` en `ValidationError.__init__`.
Bestaande call-sites ongewijzigd (code blijft `ERR_CONFIG` / `ERR_VALIDATION`).
Nieuwe/gewijzigde call-sites sturen een specifieke code mee.

```python
class ConfigError(MCPError):
    def __init__(self, message: str, file_path: str | None = None, code: str = "ERR_CONFIG") -> None:
        formatted_message = message
        if file_path:
            formatted_message = f"{message}\nFile: {file_path}"
        super().__init__(formatted_message, code=code)
        self.file_path = file_path

class ValidationError(MCPError):
    def __init__(self, message: str, schema: Any = None, code: str = "ERR_VALIDATION") -> None:
        super().__init__(message, code=code)
        ...
```

**Optie B (niet aanbevolen):** Aparte subklassen per error code (TemplateNotFoundError, MissingFieldError, …).
Meer boilerplate, complexere import-graph, minder backward-compatible.

---

## 4. Boundary-regel

```
Domeinlaag (ArtifactManager, TemplateScaffolder, JinjaRenderer, FilesystemAdapter):
  1. Schrijf SuggestionNote/BlockerNote/RecoveryNote op NoteContext VOOR het raisen
  2. Raise typed MCPError subklasse met specifieke error_code
  3. Geen ToolResult.error() — domein kent de tool-laag niet

Tool-grens (ScaffoldArtifactTool.execute() via @tool_error_handler):
  4. @tool_error_handler intercepteert MCPError, produceert ToolResult.error(code=exc.code)
  5. NoteContext.render_to_response() voegt alle Renderable notes toe aan ToolResult
  6. LLM-client ziet: foutbericht + actiegerichte suggesties als extra TextContent blokken
```

**Huidig probleem:** `scaffold_artifact.py` doet `del context` — NoteContext wordt niet doorgegeven.
De domeinlaag heeft dus geen toegang tot de NoteContext.

**Oplossing (minimale invasie):** 
- Verwijder `del context` in `ScaffoldArtifactTool.execute()` 
- Geef `context: NoteContext` door aan `ArtifactManager.scaffold_artifact(note_context=context)`
- Laat ArtifactManager notes produceren op de context
- Andere tools: NoteContext al aanwezig, maar domein-managers hoeven ze niet te kennen

**Alternatief (nog minder invasie — aanbevolen voor fase 1):**
- Tool-grens schrijft SuggestionNote ná het cachen van de exception (post-hoc)
- `@tool_error_handler` detecteert error_code en produceert note vanuit handler
- Domeinlaag blijft NoteContext-agnostisch
- Nadeel: note wordt op tool-niveau geschreven, niet op oorsprong

Voor issue #136 kiezen we **optie "alternatief"** als fase 1: toevoegen van codes en post-hoc notes in de handler. NoteContext-doorgifte naar domeinlaag is fase 2 (apart issue).

---

## 5. Te raken bestanden per implementatie-stap

### Stap A: Error code constanten + uitbreiden ConfigError/ValidationError (Cycle 1)
- `mcp_server/core/exceptions.py` — voeg `code`-parameter + string-constanten toe

### Stap B: Raise-sites aanpassen met specifieke codes (Cycle 2)
- `mcp_server/config/schemas/artifact_registry_config.py` — A1/R1: `ERR_ARTIFACT_TYPE_NOT_FOUND`
- `mcp_server/managers/artifact_manager.py` — A2: `ERR_MISSING_OUTPUT_PATH`, A3: `ERR_TEMPLATE_NOT_CONFIGURED`, A4: `ERR_CONTEXT_VALIDATION`, A5/A6: `ERR_SCHEMA_RESOLUTION`, A7: `ERR_MISSING_OUTPUT_PATH`, A8: `ERR_GENERATED_CONTENT_INVALID`
- `mcp_server/scaffolders/template_scaffolder.py` — T1/T4: `ERR_TEMPLATE_NOT_CONFIGURED`, T2: fix naar `MCPSystemError`, T3: `ERR_MISSING_FIELD`
- `mcp_server/scaffolding/renderer.py` — J1: `ERR_TEMPLATE_NOT_FOUND`
- `mcp_server/adapters/filesystem.py` — F1: `ERR_PATH_OUTSIDE_WORKSPACE` (SecurityError subtype?)

### Stap C: NoteEntry post-hoc in tool_error_handler (Cycle 3)
- `mcp_server/core/error_handling.py` — detecteer specifieke codes, produceer SuggestionNote/BlockerNote

### Stap D: extra="forbid" op alle 50 Input-modellen (#147, Cycle 4)
- `mcp_server/tools/admin_tools.py`
- `mcp_server/tools/cycle_tools.py`
- `mcp_server/tools/discovery_tools.py`
- `mcp_server/tools/git_analysis_tools.py`
- `mcp_server/tools/git_fetch_tool.py`
- `mcp_server/tools/git_pull_tool.py`
- `mcp_server/tools/git_tools.py` (9 modellen, GitCommitInput al correct)
- `mcp_server/tools/health_tools.py`
- `mcp_server/tools/issue_tools.py`
- `mcp_server/tools/label_tools.py`
- `mcp_server/tools/milestone_tools.py`
- `mcp_server/tools/phase_tools.py`
- `mcp_server/tools/pr_tools.py`
- `mcp_server/tools/project_tools.py`
- `mcp_server/tools/quality_tools.py`
- `mcp_server/tools/safe_edit_tool.py`
- `mcp_server/tools/scaffold_artifact.py`
- `mcp_server/tools/template_validation_tool.py`
- `mcp_server/tools/test_tools.py`
- `mcp_server/tools/validation_tools.py`
- `mcp_server/tools/code_tools.py`

### Stap E: Tests (bij elke cycle)
- `tests/mcp_server/tools/` — per tool: testen dat extra veld → ToolResult.error met `ERR_EXTRA_FIELD`
- `tests/mcp_server/managers/` — per raise-site: testen dat error_code overeenkomt
- `tests/mcp_server/core/` — error_handling: testen dat SuggestionNote verschijnt in render

---

## Findings & Conclusies

1. **50 Input-modellen** missen `extra="forbid"` (slechts 1 correct: `GitCommitInput`)
2. **15 raise-sites** in de scaffold-keten produceren te brede codes
3. **2 misclassificaties**: T2 (ValidationError → moet MCPSystemError zijn), F1 (ValidationError → moet security-specifieke code zijn)
4. **NoteContext** wordt niet doorgegeven aan de domeinlaag; post-hoc benadering is de minst invasieve oplossing voor fase 1
5. **Optie A** (optionele `code`-parameter op ConfigError/ValidationError) is backwards-compatibel en vereist minimale wijzigingen aan bestaande call-sites
6. **Implementatie-volgorde**: exceptions.py → raise-sites → error_handler → Input-modellen

---

## Open vragen

- Moet `ERR_PATH_OUTSIDE_WORKSPACE` een aparte `SecurityError(MCPError)` subklasse krijgen, of volstaat `ValidationError(code=ERR_PATH_OUTSIDE_WORKSPACE)`?
- `SafeEditInput` bevat nested Pydantic-modellen (`LineEdit`, `InsertLine`); `extra="forbid"` op de nested modellen ook meenemen?
- Scope van Cycle 4: alle 50 tegelijk of per functioneel domein (git-tools apart, issue-tools apart)?

---

## Related Documentation

- `mcp_server/core/exceptions.py` — huidige exception-hiërarchie
- `mcp_server/core/operation_notes.py` — NoteEntry types en NoteContext
- `mcp_server/core/error_handling.py` — @tool_error_handler decorator
- `mcp_server/tools/base.py` — BaseTool + @tool_error_handler wiring
- `mcp_server/tools/scaffold_artifact.py` — tool entry point
- `mcp_server/managers/artifact_manager.py` — orchestratie-laag
- `mcp_server/scaffolders/template_scaffolder.py` — v1 validatie + scaffolding
- `mcp_server/scaffolding/renderer.py` — JinjaRenderer
- `mcp_server/adapters/filesystem.py` — FilesystemAdapter
- `mcp_server/config/schemas/artifact_registry_config.py` — ArtifactRegistryConfig.get_artifact()
- `docs/development/issue136/` — deze map

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-07 | imp-agent (researcher) | Initial research — volledig ingevuld |
