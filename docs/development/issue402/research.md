<!-- c:\temp\pgmcp\docs\development\issue402\research.md -->
<!-- template=research version=8b7bb3ab created=2026-06-12T05:54:00Z updated=2026-06-12T06:00:00Z -->
# Research — Issue #402: Expose JSON data in MCP tools

**Status:** APPROVED  
**Version:** 1.0  
**Last Updated:** 2026-06-12

---

## Purpose

Investigate the migration of MCP tools to StructuredTool and establish a stable research nucleus.

## Scope

**In Scope:**
- All registered MCP tools in the `mcp_server/tools/` directory.
- Standardisation of JSON output payloads for tools.
- Presentation of options for defining JSON schemas.
- Blast radius and test suite impact evaluation.

**Out of Scope:**
- External libraries, protocols outside MCP, or changes to client implementations.

---

## Problem Statement

Expose structured JSON data alongside human-readable text fallbacks in the ToolResult responses of MCP tools (in accordance with the design contract established in #301).

## Research Goals

- Identify how existing tools produce JSON data and standardise them.
- Formulate an exclusion list of tools that do not require JSON output.
- Compare options for defining JSON schemas (raw dicts vs Pydantic models).
- Analyse the data to be returned by each tool and design the accompanying text output.

---

## Background

Initial research under Issue #301 laid the groundwork, and Issue #390 introduced `StructuredTool` and `mcp_converters.py`.

---

## Findings

### 1. Existing Behavior and Patterns
Our MCP server uses a two-tiered tool response model:
- **`BaseTool` / `BaseTool.execute`:** Returns `ToolResult.text(...)`, which produces a single content block of type `"text"`. Standard MCP clients receive `structuredContent = None`.
- **`StructuredTool` / `StructuredTool.execute_structured`:** Returns a tuple `(data_dict, summary_text)`. The base class maps this to `ToolResult.json_data(data_dict, text=summary_text)`, creating two content blocks: `content[0]` of type `"json"`, and `content[1]` of type `"text"`. The server's `convert_tool_result_to_mcp_result` extracts the JSON block to `CallToolResult.structuredContent` and leaves the text fallback block in `CallToolResult.content`.

### 2. Comprehensive Tool-by-Tool Analysis
| Tool Class | File | Target Output | Available Data | Text Fallback Focus | Exclusion Rationale / Notes |
|---|---|---|---|---|---|
| `RestartServerTool` | `admin_tools.py` | Excluded | None | N/A | Signal tool; no domain data. |
| `TransitionCycleTool` | `cycle_tools.py` | JSON + Text | `{"success": true, "branch": str, "old_cycle": str, "new_cycle": str}` | Samenvatting van de transitie inclusief branch-naam, oude en nieuwe cycle-fase. | |
| `ForceCycleTransitionTool` | `cycle_tools.py` | JSON + Text | `{"success": true, "branch": str, "old_cycle": str, "new_cycle": str}` | Samenvatting van de geforceerde transitie inclusief branch-naam, oude en nieuwe cycle-fase. | |
| `SearchDocumentationTool` | `discovery_tools.py` | JSON + Text | `{"query": str, "results": [{"title": str, "path": str, "score": float, "snippet": str}]}` | Lijst met titels, paden en scores van relevante gevonden documentatie-overeenkomsten. | |
| `GetWorkContextTool` | `discovery_tools.py` | JSON + Text | *Already Structured* | Gestructureerd overzicht van de huidige actieve branch, fase en taakcontext. | Structured in #390. |
| `GitListBranchesTool` | `git_analysis_tools.py` | JSON + Text | `{"branches": [str], "current_branch": str}` | Overzicht van alle beschikbare branches en de momenteel actieve branch. | |
| `GitDiffTool` | `git_analysis_tools.py` | JSON + Text | `{"target_branch": str, "source_branch": str, "stats": str}` | Statistisch overzicht van gewijzigde regels en bestanden tussen de doel- en bronbranch. | |
| `GitFetchTool` | `git_fetch_tool.py` | JSON + Text | `{"success": true, "remote": str}` | Bevestiging van de bijgewerkte remote en eventueel opgeschoonde branches. | |
| `GitPullTool` | `git_pull_tool.py` | JSON + Text | `{"success": true, "remote": str, "branch": str}` | Status van de binnengehaalde wijzigingen inclusief remote- en branchnaam. | |
| `CreateBranchTool` | `git_tools.py` | JSON + Text | `{"success": true, "branch_name": str, "base_branch": str}` | Bevestiging van de nieuw aangemaakte branch en de specifieke bronbranch. | |
| `GitStatusTool` | `git_tools.py` | JSON + Text | `{"branch": str, "is_clean": bool, "modified_files": [str], "untracked_files": [str]}` | Overzicht van de huidige branch-status en gewijzigde/ongetrackte bestanden. | |
| `GitCommitTool` | `git_tools.py` | JSON + Text | `{"sha": str, "branch": str, "message": str, "files": [str]}` | Details van de nieuwe commit zoals SHA, branch, commit-bericht en beïnvloede bestanden. | |
| `GitRestoreTool` | `git_tools.py` | JSON + Text | `{"success": true, "files": [str]}` | Lijst van herstelde bestanden. | |
| `GitCheckoutTool` | `git_tools.py` | JSON + Text | `{"branch": str}` | Naam van de nieuw actieve branch. | |
| `GitPushTool` | `git_tools.py` | JSON + Text | `{"success": true, "remote": str, "branch": str}` | Status van de push-operatie inclusief remote- en branchnaam. | |
| `GitMergeTool` | `git_tools.py` | JSON + Text | `{"success": true, "merge_sha": str}` | Bevestiging van de succesvolle merge en de resulterende commit SHA. | |
| `GitDeleteBranchTool` | `git_tools.py` | JSON + Text | `{"success": true, "branch": str}` | Bevestiging van de verwijderde branch. | |
| `GitStashTool` | `git_tools.py` | JSON + Text | `{"success": true, "action": str}` | Status van de stash-operatie en de uitgevoerde actie. | |
| `GetParentBranchTool` | `git_tools.py` | JSON + Text | `{"branch": str, "parent_branch": str}` | Naam van de actieve branch en de geïdentificeerde parentbranch. | |
| `CheckMergeTool` | `git_tools.py` | JSON + Text | `{"target_branch": str, "source_branch": str, "is_ancestor": bool}` | Status of de bronbranch volledig is opgenomen (merged) in de doelbranch. | |
| `HealthCheckTool` | `health_tools.py` | Excluded | None | N/A | Standard ping tool; no complex data. |
| `CreateIssueTool` | `issue_tools.py` | JSON + Text | `{"issue": {"number": int, "title": str, "state": str, "labels": [str]}}` | Overzicht van het nieuw aangemaakte GitHub-issue, inclusief nummer, titel en labels. | |
| `GetIssueTool` | `issue_tools.py` | JSON + Text | *Already Structured* | Uitgebreide details van het opgevraagde issue inclusief status, beschrijving en toewijzingen. | Structured in #390. |
| `ListIssuesTool` | `issue_tools.py` | JSON + Text | `{"issues": [{"number": int, "title": str, "state": str}]}` | Lijst met open/gesloten issues gefilterd op labels of milestone. | |
| `UpdateIssueTool` | `issue_tools.py` | JSON + Text | `{"issue": {"number": int, "title": str, "state": str}}` | Samenvatting van de gewijzigde issue-eigenschappen en status. | |
| `CloseIssueTool` | `issue_tools.py` | JSON + Text | `{"issue_number": int, "success": bool}` | Bevestiging dat het specifieke issue is gesloten. | |
| `ListLabelsTool` | `label_tools.py` | JSON + Text | `{"labels": [{"name": str, "color": str, "description": str}]}` | Overzicht van beschikbare labels met bijbehorende kleuren en beschrijvingen. | |
| `CreateLabelTool` | `label_tools.py` | JSON + Text | `{"label": {"name": str, "color": str}}` | Details van het nieuw aangemaakte label. | |
| `DeleteLabelTool` | `label_tools.py` | JSON + Text | `{"success": true, "label": str}` | Bevestiging van het verwijderde label. | |
| `RemoveLabelsTool` | `label_tools.py` | JSON + Text | `{"issue_number": int, "labels": [str]}` | Lijst van labels die van het issue zijn verwijderd. | |
| `AddLabelsTool` | `label_tools.py` | JSON + Text | `{"issue_number": int, "labels": [str]}` | Lijst van labels die aan het issue zijn toegevoegd. | |
| `DetectLabelDriftTool` | `label_tools.py` | JSON + Text | `{"github_only": [str], "yaml_only": [str], "mismatches": [dict]}` | Overzicht van inconsistenties tussen lokale configuratie en GitHub-labels. | |
| `ListMilestonesTool` | `milestone_tools.py` | JSON + Text | `{"milestones": [{"number": int, "title": str, "state": str}]}` | Lijst met actieve milestones en hun status. | |
| `CreateMilestoneTool` | `milestone_tools.py` | JSON + Text | `{"milestone": {"number": int, "title": str, "state": str}}` | Bevestiging van de nieuwe milestone met titel en eventuele vervaldatum. | |
| `CloseMilestoneTool` | `milestone_tools.py` | JSON + Text | `{"milestone": {"number": int, "title": str, "state": str}}` | Bevestiging van de gesloten milestone. | |
| `TransitionPhaseTool` | `phase_tools.py` | JSON + Text | `{"success": true, "branch": str, "old_phase": str, "new_phase": str}` | Status van de faseovergang inclusief branch-naam, oude fase en nieuwe fase. | |
| `ForcePhaseTransitionTool` | `phase_tools.py` | JSON + Text | `{"success": true, "branch": str, "old_phase": str, "new_phase": str, "skip_reason": str}` | Details van de geforceerde faseovergang, inclusief branch-naam, oude/nieuwe fase en de reden voor overslaan. | |
| `ListPRsTool` | `pr_tools.py` | JSON + Text | `{"pull_requests": [{"number": int, "title": str, "state": str}]}` | Overzicht van pull requests en hun actuele status. | |
| `MergePRTool` | `pr_tools.py` | JSON + Text | `{"success": true, "pr_number": int}` | Bevestiging van de succesvol gemergde pull request. | |
| `GetPRTool` | `pr_tools.py` | JSON + Text | *Already Structured* | Details van de opgevraagde pull request inclusief status en reviews. | Structured in #390. |
| `SubmitPRTool` | `pr_tools.py` | JSON + Text | `{"pull_request": {"number": int, "title": str, "state": str}}` | Details van de ingediende pull request met link en PR-nummer. | |
| `InitializeProjectTool` | `project_tools.py` | JSON + Text | *Already Structured* | Bevestiging van de projectinitialisatie met de gekozen workflow en issues. | Structured in #390. |
| `GetProjectPlanTool` | `project_tools.py` | JSON + Text | *Already Structured* | Overzicht van de fasen en taken in het projectplan. | Structured in #390. |
| `SavePlanningDeliverablesTool` | `project_tools.py` | JSON + Text | *Already Structured* | Status van de opgeslagen planning-deliverables. | Structured in #390. |
| `UpdatePlanningDeliverablesTool` | `project_tools.py` | JSON + Text | *Already Structured* | Status van de bijgewerkte planning-deliverables. | Structured in #390. |
| `RunQualityGatesTool` | `quality_tools.py` | JSON + Text | `{"overall_pass": bool, "gates": [dict]}` | Samenvatting van de uitgevoerde kwaliteitspoortjes en of deze zijn behaald. | Currently custom dual-result. |
| `SafeEditTool` | `safe_edit_tool.py` | JSON + Text | `{"passed": bool, "issues": str, "diff": str}` | Resultaat van de bestandswijziging, inclusief diff-preview en eventuele validatiefouten. | |
| `ScaffoldArtifactTool` | `scaffold_artifact.py` | JSON + Text | *Already Structured* | Bevestiging van de gegenereerde bestanden en hun template-type. | Structured in #390. |
| `ScaffoldSchemaTool` | `scaffold_schema_tool.py` | JSON + Text | *Already Structured* | Gestructureerd schema voor het opgegeven artifact-type. | Structured in #390. |
| `TemplateValidationTool` | `template_validation_tool.py` | JSON + Text | `{"passed": bool, "issues": [{"severity": str, "message": str}]}` | Rapport van de sjabloonvalidatie met eventuele waarschuwingen of fouten. | |
| `RunTestsTool` | `test_tools.py` | JSON + Text | `{"exit_code": int, "summary": dict}` | Samenvatting van de testresultaten inclusief het aantal geslaagde/mislukte tests en de exitcode. | Currently custom dual-result. |

### 3. JSON Schema Options & Architecture Principles
To define JSON schemas for tool output data, we consider two options:

#### Option A: Raw untyped Python dicts (`dict[str, Any]`)
- **Pros:** Fast implementation, zero boilerplate, high flexibility.
- **Cons:** Violates `ARCHITECTURE_PRINCIPLES.md` §8 (Explicit over Implicit) and §5 (Command/Query Separation). Boundaries remain untyped, risking serialization errors and client incompatibilities.

#### Option B: Declarative Pydantic Models for Tool Output (Recommended)
- **Pros:** Statically typed output schemas, validation at boundaries, clear self-documenting interface, fully compliant with ARCHITECTURE_PRINCIPLES.md §8 and §5. Frozen models prevent command/query state contamination.
- **Cons:** Additional boilerplate file (`mcp_server/schemas/tool_outputs.py`) to manage.

**Architectural Alignment:** Option B is recommended because it respects type safety at system boundaries and avoids implicit data structures, fulfilling the prime directives.

### 4. Blast Radius and Test-Suite Impact
- **The Issue:** Dual-payload `ToolResult` (from `ToolResult.json_data()`) sets the JSON block as `content[0]` and the text block as `content[1]`.
- **The Blast Radius:** More than 200 unit test assertions in `tests/mcp_server/unit/tools/` check `result.content[0]["text"]` to verify text outputs. Converting all tools to `StructuredTool` will cause all these assertions to fail with a `KeyError`, as index 0 becomes a JSON block.
- **Mitigation:** Implement a custom test helper `get_text_content(result: ToolResult) -> str` that extracts the text block regardless of its index position in `content`, and update unit tests to use this helper.

---

## Open Questions

1. Should the test helper be globally registered in `tests/mcp_server/test_support.py`?
2. Do we require strict schema validation on the output payload at runtime, or only for unit test assertions?

---

## Approved Strategy

### Boundary / consumer scope
All MCP tools in `mcp_server/tools/` except `HealthCheckTool` and `RestartServerTool`.

### Selected strategy
Option B: Pydantic-defined schemas for tool outputs, with migration of all remaining tools to `StructuredTool`.

### Rationale
Provides explicit boundary validation, preventing drift and ensuring client compatibility without violating SRP/CQS.

### Constraints for later phases
- Do not instantiate outputs inside `execute_structured` directly if they bypass defined schema models.
- All unit tests must use the new index-agnostic assertion helper.
