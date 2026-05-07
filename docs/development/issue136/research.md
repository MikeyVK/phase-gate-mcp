<!-- docs\development\issue136\research.md -->
<!-- template=research version=8b7bb3ab created=2026-05-07T15:54Z updated=2026-05-07T17:10Z -->
# Error Taxonomy & Strict Input Validation — Research

**Status:** COMPLETE  
**Version:** 2.0  
**Last Updated:** 2026-05-07  
**Issues:** #136 (error taxonomy) + #147 (extra=forbid, bundled deliverable)  
**Epic:** #320 fase 0

---

## Problem Statement

Voorspelbare fouten in de `scaffold_artifact`-keten produceren generieke error codes
(`ERR_CONFIG`, `ERR_VALIDATION`) die agents niet laten onderscheiden. Daarnaast missen
~50 tool Input-modellen `extra="forbid"`, waardoor typo-velden stilzwijgend genegeerd worden.

---

## Research Goals

1. Inventariseer de NoteContext-infrastructuur end-to-end — hoe functioneert het mechanisme
   dat al is gebouwd om context te geven bij fouten?
2. Stel vast welke tools/managers het mechanisme al correct gebruiken en hoe
3. Documenteer de exacte gap: waar ontbreekt note-gebruik in de scaffold-keten?
4. Inventariseer alle tool Input-modellen zonder `extra="forbid"` (#147)
5. Documenteer de agent-experience: wat ziet de LLM-client bij fouten?

---

## 1. NoteContext mechanisme — hoe het werkt (feiten)

### 1.1 Levenscyclus (server.py, handle_call_tool)

```
1. note_context = NoteContext()             ← gecreëerd NA argument-validatie (L630)
2. pre_result = _run_tool_enforcement(...)  ← enforcement mag notes produceren (L636)
3. raw_result = await tool.execute(validated, note_context)  ← tool ontvangt context
4. post_result = _run_tool_enforcement(...) ← alleen bij is_error=False (L645)
5. result = note_context.render_to_response(raw_result)  ← ALTIJD, ook bij is_error=True (L653)
6. response_content = _convert_tool_result_to_mcp_result(result)
```

**Kritiek feit:** `render_to_response` wordt **onvoorwaardelijk** aangeroepen — ook als
`raw_result.is_error == True`. Notes die vóór de exception zijn geproduceerd, worden
altijd aan het antwoord toegevoegd.

### 1.2 render_to_response — wat het doet

```python
def render_to_response(self, base: ToolResult) -> ToolResult:
    renderable = [n for n in self._entries if isinstance(n, Renderable)]
    if not renderable:
        return base  # geen wijziging
    notes_text = "\n".join(n.to_message() for n in renderable)
    augmented = list(base.content) + [{"type": "text", "text": notes_text}]
    return base.model_copy(update={"content": augmented})
```

Alleen `Renderable`-notes worden gerenderd. `CommitNote` implementeert `Renderable` niet (bewust).

### 1.3 NoteEntry subtypen en Renderable status

| Subtype | Renderable | to_message() prefix |
|---------|-----------|---------------------|
| `ExclusionNote` | ja | `"Excluded from commit index: {file_path}"` |
| `CommitNote` | **nee** | — (alleen voor test-assertions) |
| `SuggestionNote` | ja | `"Suggestion: {message}"` (+ `" ({subject})"`) |
| `BlockerNote` | ja | `"Blocker: {message}"` |
| `RecoveryNote` | ja | `"Recovery: {message}"` |
| `InfoNote` | ja | `"{message}"` |

### 1.4 tool_error_handler — interactie met NoteContext

`tool_error_handler` wraps `execute()`. Bij exception:
- Produceert `ToolResult.error(message=..., error_code=exc.code, file_path=...)` en **returnt** dit
- Heeft **geen toegang tot NoteContext** — `args` bevat `[self, params, context]`, maar de handler
  leest `args[2]` niet en produceert geen notes
- `error_code` wordt opgeslagen in `ToolResult.error_code` maar **niet doorgegeven** aan
  `CallToolResult` (zie §1.5) — codes zijn daarmee onzichtbaar voor de LLM-client

### 1.5 Wat de LLM-client werkelijk ziet

`_convert_tool_result_to_mcp_result` produceert:
```python
CallToolResult(
    content=self._convert_tool_result_to_content(result),
    isError=result.is_error,
)
```
`ToolResult.error_code` en `ToolResult.file_path` worden **niet** opgenomen in de
`CallToolResult`. De MCP-spec kent geen error_code veld op `CallToolResult`.

De agent ziet bij een fout dus:
- `isError=True`
- De fout-tekst als eerste `TextContent`
- Eventuele `Renderable` notes als extra `TextContent`-blokken (als die er zijn)

`error_code` is **uitsluitend zichtbaar voor test-assertions** via `ToolResult.error_code`.

---

## 2. Bestaand correct gebruik van NoteContext (precedenten)

### 2.1 GitManager (mcp_server/managers/git_manager.py) — het referentie-patroon

`GitManager` accepteert `NoteContext` als parameter bij domein-methodes en produceert
notes vlak voor het raisen:

```python
# GitManager.create_branch(note_context, branch_type, name, base_branch)
if not self._git_config.has_branch_type(branch_type):
    note_context.produce(
        SuggestionNote(message=f"Allowed types: {', '.join(self._git_config.branch_types)}")
    )
    raise ValidationError(f"Invalid branch type: {branch_type}")
```

Patroon: **`produce(note)` → `raise exception`** in de domeinlaag.
Effect: note staat al in context vóór propagatie naar `tool_error_handler`.
Server-side `render_to_response` voegt de note toe aan de `ToolResult.error()`.

Geïdentificeerde note-producerende managers: `GitManager`.

### 2.2 Tools die notes produceren in execute()

| Tool | Bestand | Note-typen gebruikt |
|------|---------|---------------------|
| `RunTestsTool` | `test_tools.py` | `InfoNote`, `RecoveryNote` (inclusief via `PytestResult.note`) |
| `RunQualityGatesTool` | `quality_tools.py` | `RecoveryNote` |
| `SubmitPRTool` | `pr_tools.py` | `RecoveryNote` (rollback) |
| `InitializeProjectTool` | `project_tools.py` | `SuggestionNote` |
| `TransitionPhaseTool` | `phase_tools.py` | `RecoveryNote` (via `e.recovery`) |
| `ForceCycleTransitionTool` | `cycle_tools.py` | `RecoveryNote` (via `e.recovery`) |
| `GetWorkContextTool` | `discovery_tools.py` | `RecoveryNote` (meerdere) |
| `GitCommitTool` | `git_tools.py` | `CommitNote` (niet-Renderable) |

### 2.3 PytestRunner — factory-patroon voor notes (mcp_server/managers/pytest_runner.py)

`PytestRunner.run()` returnt `PytestResult.note: NoteEntry | None`. De tool roept dan
`context.produce(result.note)` aan. `PytestRunner` heeft geen directe dependency op NoteContext.

---

## 3. Gap-analyse: scaffold_artifact keten

### 3.1 ScaffoldArtifactTool.execute()

```python
async def execute(self, params: ScaffoldArtifactInput, context: NoteContext) -> ToolResult:
    del context  # ← NoteContext wordt weggegooid
    ...
    artifact_path = await self.manager.scaffold_artifact(params.artifact_type, **kwargs)
```

Gevolg: `ArtifactManager` kan geen notes produceren (heeft geen NoteContext).
Wanneer een exception optreedt, is er dus nooit een note bij de foutmelding.

### 3.2 ArtifactManager.scaffold_artifact()

Heeft geen `NoteContext`-parameter. Alle raise-sites produceren alleen exception-tekst,
geen begeleidende notes.

### 3.3 TemplateScaffolder, JinjaRenderer, FilesystemAdapter

Geen van deze klassen accepteert of gebruikt NoteContext.
Ze zijn NoteContext-agnostisch.

### 3.4 Contrast met GitManager

`GitManager` laat zien dat managers NoteContext wél kunnen ontvangen. Voor de scaffold-keten
is dat patroon **niet geïmplementeerd**.

---

## 4. Raise-sites in de scaffold-keten (feitelijke inventarisatie)

### 4.1 ArtifactManager.scaffold_artifact() — mcp_server/managers/artifact_manager.py

| Site | Conditie | Exception | Code | Heeft note? |
|------|----------|-----------|------|-------------|
| A1 | `artifact_type` onbekend (via `get_artifact()`) | `ConfigError` | `ERR_CONFIG` | nee |
| A2 | `output_type=="file"` zonder `output_path` | `ValidationError` | `ERR_VALIDATION` | nee |
| A3 | `template_file is None` (`template_path=null` in YAML) | `ConfigError` | `ERR_CONFIG` | nee |
| A4 | V2 context `model_validate` mislukt | `ValidationError` | `ERR_VALIDATION` | nee |
| A5 | `_enrich_context_v2`: Context-klasse eindigt niet op "Context" | `ValidationError` | `ERR_VALIDATION` | nee |
| A6 | `_enrich_context_v2`: RenderContext-klasse niet gevonden in schemas | `ValidationError` | `ERR_VALIDATION` | nee |
| A7 | Generic artifact zonder `output_path` in context | `ValidationError` | `ERR_VALIDATION` | nee |
| A8 | Gegenereerde code-content faalt validatie | `ValidationError` | `ERR_VALIDATION` | nee |

### 4.2 TemplateScaffolder.validate()/scaffold() — mcp_server/scaffolders/template_scaffolder.py

| Site | Conditie | Exception | Code | Heeft note? |
|------|----------|-----------|------|-------------|
| T1 | Geen template geconfigureerd (geen `template_path`) | `ValidationError` | `ERR_VALIDATION` | nee |
| T2 | Template loader niet geconfigureerd | `ValidationError` | `ERR_VALIDATION` | nee |
| T3 | Vereiste velden ontbreken (introspectie, v1) | `ValidationError` | `ERR_VALIDATION` | **gedeeltelijk** — `schema` attached, niet als Note |
| T4 | Generic zonder `template_name` én zonder `template_path` | `ValidationError` | `ERR_VALIDATION` | nee |

Opmerking T3: bij `missing` velden wordt een `ValidationError` met `schema`-attribuut geraised.
`tool_error_handler` vertaalt dit naar een EmbeddedResource (`schema://validation`) — het schema
is dus al beschikbaar als machine-leesbare content, maar niet als `Renderable` note.

### 4.3 JinjaRenderer — mcp_server/scaffolding/renderer.py

| Site | Conditie | Exception | Code | Heeft note? |
|------|----------|-----------|------|-------------|
| J1 | `TemplateNotFound` (Jinja2) | `ExecutionError` | `ERR_EXECUTION` | nee |

### 4.4 FilesystemAdapter — mcp_server/adapters/filesystem.py

| Site | Conditie | Exception | Code | Heeft note? |
|------|----------|-----------|------|-------------|
| F1 | Path buiten workspace | `ValidationError` | `ERR_VALIDATION` | nee |
| F2 | OS-fout bij schrijven | `MCPSystemError` | `ERR_SYSTEM` | nee |

### 4.5 ArtifactRegistryConfig.get_artifact() — mcp_server/config/schemas/artifact_registry_config.py

| Site | Conditie | Exception | Code | Heeft note? |
|------|----------|-----------|------|-------------|
| R1 | `type_id` niet gevonden in registry (= zelfde als A1) | `ConfigError` | `ERR_CONFIG` | nee |

**Totaal: 14 raise-sites, 0 met notes.**

---

## 5. Input-modellen zonder `extra="forbid"` (#147)

### 5.1 Hoe extra-veld-fouten door de server lopen

`_validate_tool_arguments` wordt aangeroepen **vóór** `NoteContext()` wordt gecreëerd (L630).
Bij Pydantic `extra="forbid"` triggert `model_cls(**(arguments or {}))` een `pydantic.ValidationError`.
Deze wordt gevangen en teruggegeven als `[TextContent(type="text", text=f"Invalid input for {name}: {error_details}")]` — zonder NoteContext, zonder `error_code`.

### 5.2 Huidig model met `extra="forbid"`

Enige model: `GitCommitInput` (`mcp_server/tools/git_tools.py:231`)

### 5.3 Modellen zonder `extra="forbid"` (50 stuks, per bestand)

**mcp_server/tools/admin_tools.py**
- `RestartServerInput` (L83)

**mcp_server/tools/cycle_tools.py**
- `TransitionCycleInput` (L38)
- `ForceCycleTransitionInput` (L140)

**mcp_server/tools/discovery_tools.py**
- `SearchDocumentationInput` (L31)
- `GetWorkContextInput` (L98)

**mcp_server/tools/git_analysis_tools.py**
- `GitListBranchesInput` (L13)
- `GitDiffInput` (L42)

**mcp_server/tools/git_fetch_tool.py**
- `GitFetchInput` (L39)

**mcp_server/tools/git_pull_tool.py**
- `GitPullInput` (L42)

**mcp_server/tools/git_tools.py** (9 modellen — `GitCommitInput` is al correct)
- `CreateBranchInput` (L85)
- `GitStatusInput` (L172)
- `GitRestoreInput` (L372)
- `GitCheckoutInput` (L412)
- `GitPushInput` (L481)
- `GitMergeInput` (L523)
- `GitDeleteBranchInput` (L561)
- `GitStashInput` (L599)
- `GetParentBranchInput` (L660)

**mcp_server/tools/health_tools.py**
- `HealthCheckInput` (L12)

**mcp_server/tools/issue_tools.py**
- `CreateIssueInput` (L99)
- `GetIssueInput` (L293)
- `ListIssuesInput` (L335)
- `UpdateIssueInput` (L372)
- `CloseIssueInput` (L417)

**mcp_server/tools/label_tools.py**
- `ListLabelsInput` (L16)
- `CreateLabelInput` (L53)
- `DeleteLabelInput` (L116)
- `RemoveLabelsInput` (L143)
- `AddLabelsInput` (L173)
- `DetectLabelDriftInput` (L224)

**mcp_server/tools/milestone_tools.py**
- `ListMilestonesInput` (L14)
- `CreateMilestoneInput` (L57)
- `CloseMilestoneInput` (L94)

**mcp_server/tools/phase_tools.py**
- `TransitionPhaseInput` (L34)
- `ForcePhaseTransitionInput` (L42)

**mcp_server/tools/pr_tools.py**
- `ListPRsInput` (L22)
- `MergePRInput` (L67)
- `SubmitPRInput` (L120)

**mcp_server/tools/project_tools.py**
- `InitializeProjectInput` (L32)
- `GetProjectPlanInput` (L288)
- `SavePlanningDeliverablesInput` (L377)
- `UpdatePlanningDeliverablesInput` (L467)

**mcp_server/tools/quality_tools.py**
- `RunQualityGatesInput` (L13)

**mcp_server/tools/safe_edit_tool.py**
- `SafeEditInput` (L105) — bevat geneste modellen `LineEdit` (L?), `InsertLine` (L?)

**mcp_server/tools/scaffold_artifact.py**
- `ScaffoldArtifactInput` (L27)

**mcp_server/tools/template_validation_tool.py**
- `TemplateValidationInput` (L13)

**mcp_server/tools/test_tools.py**
- `RunTestsInput` (L26)

**mcp_server/tools/validation_tools.py**
- `ValidationInput` (L14)
- `ValidateDTOInput` (L45)

**mcp_server/tools/code_tools.py**
- `CreateFileInput` (L16)

**Totaal: 50 modellen zonder `extra="forbid"`**

### 5.4 Geneste modellen in SafeEditInput

`SafeEditInput` bevat geneste Pydantic-modellen (`LineEdit`, `InsertLine`).
Of `extra="forbid"` ook op de geneste modellen gezet moet worden is een open vraag
voor de planningsfase.

---

## 6. Agent-experience: samenvatting van de huidige situatie

| Scenario | Wat de agent ziet |
|----------|------------------|
| Scaffold-fout (A1–A8, T1–T4, J1, F1–F2) | `isError=True` + fout-tekst (generiek) + **geen notes** |
| Git-fout met note (GitManager-patroon) | `isError=True` + fout-tekst + **SuggestionNote/BlockerNote als extra TextContent** |
| Vereiste velden ontbreken (T3, schema beschikbaar) | `isError=True` + fout-tekst + EmbeddedResource met JSON-schema |
| `extra="forbid"` schending (toekomst) | `isError=True` + Pydantic-fout-tekst (geen NoteContext) |
| `ToolResult.error_code` | **Niet zichtbaar** voor agent — alleen voor test-assertions |

---

## 7. Open vragen (niet beantwoord door research)

1. **Scope codes vs notes:** Welk mechanisme is leidend voor agent-feedback bij domeinfouten —
   specifieke error codes (niet zichtbaar in MCP), notes (zichtbaar), of beide? De huidige
   architectuur laat zien dat notes de enige weg zijn naar de agent.

2. **Scope van NoteContext-doorgifte:** De scaffold-keten heeft geen NoteContext.
   Het GitManager-patroon laat zien hoe dat eruit zou zien.
   Is de scaffold-keten de enige keten die dit mist, of zijn er anderen?

3. **extra="forbid" en geneste modellen:** Moeten `LineEdit` en `InsertLine` in `SafeEditInput`
   ook `extra="forbid"` krijgen?

4. **Scope van #147:** Alle 50 modellen in één keer, of gefaseerd per domein?

5. **T2 classificatie:** `TemplateScaffolder` raise `ValidationError` als de template loader
   niet geconfigureerd is. Dit is een infrastructuurfout, geen input-fout.
   Is herclassificatie (naar `MCPSystemError`) onderdeel van deze scope?

---

## Related Documentation

- `mcp_server/core/operation_notes.py` — NoteEntry typen en NoteContext
- `mcp_server/core/error_handling.py` — @tool_error_handler
- `mcp_server/core/exceptions.py` — exception-hiërarchie
- `mcp_server/server.py` — handle_call_tool (L602–L700): NoteContext-levenscyclus
- `mcp_server/managers/git_manager.py` — referentie-patroon: NoteContext in domeinlaag
- `mcp_server/managers/pytest_runner.py` — alternatief patroon: note als return-waarde
- `mcp_server/tools/scaffold_artifact.py` — `del context` gap
- `mcp_server/managers/artifact_manager.py` — scaffold-orchestratie
- `mcp_server/scaffolders/template_scaffolder.py` — v1 validatie (T3: schema al als resource)
- `mcp_server/adapters/filesystem.py` — F1 security boundary
- `mcp_server/tools/base.py` — BaseTool + @tool_error_handler wiring

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-07 | imp-agent | Initiële research — foutpaden + Input-inventarisatie + taxonomie-voorstel (te breed: bevatte ontwerpen) |
| 2.0 | 2026-05-07 | imp-agent | Herschreven: NoteContext end-to-end onderzocht, gap-analyse, agent-experience, open vragen zonder ontwerp-beslissingen |
