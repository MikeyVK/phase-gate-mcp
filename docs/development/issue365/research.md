<!-- docs\development\issue365\research.md -->
<!-- template=research version=8b7bb3ab created=2026-06-05T20:15Z updated=2026-06-05T20:30Z -->
# Remove validate_dto and create_file tools from MCP server

**Status:** DRAFT
**Version:** 0.1
**Last Updated:** 2026-06-05

---

## Scope

**In Scope:**
`mcp_server/tools/validation_tools.py`, `mcp_server/tools/code_tools.py`, `mcp_server/server.py`, all test files referencing `ValidateDTOTool` or `CreateFileTool`, all active documentation referencing `validate_dto` or `create_file`.

**Out of Scope:**
`TemplateValidationTool` (`validate_template`) and its tests, `backend/` modules, `docs/development/issue346/` (historical context only), archive documentation.

---

## Problem Statement

Two MCP tools occupy agent-visible tool surface without providing real value. `ValidateDTOTool` performs only a file-exists-and-non-empty check with no structural DTO validation. `CreateFileTool` is already marked `[DEPRECATED]` in its own description and docstring in favor of `scaffold_artifact`, yet remains registered in `server.py` where agents may invoke it instead of the correct tool.

## Research Goals

- Establish why both tools provide no real value and should be removed
- Identify the full blast radius across production code, tests, and documentation
- Determine preservation goals and invariants that must remain stable after removal
- Identify risky boundaries and candidate seams for safe planning
- Capture the Approved Strategy per boundary

---

## Background

Issue #346 (2026-05) explicitly preserved `ValidateDTOTool` as "stable" when removing the unrelated `ValidationTool` stub. Issue #365 revisits that decision: the tool performs only a file-exists check, providing no structural DTO validation value over the existing test suite. `CreateFileTool` was deprecated in favour of `scaffold_artifact` and should never be invoked by agents.

---

## Findings

### Tool Responsibilities

| Tool | File | Actual behaviour | Claimed purpose | Gap |
|---|---|---|---|---|
| `ValidateDTOTool` | `mcp_server/tools/validation_tools.py` | Checks file exists + non-empty | "Validate DTO definition" | No field typing, no `frozen=True`, no `model_config` check — Pydantic already validates at import time; `test_extra_forbid.py` enforces `extra='forbid'` on all input models |
| `CreateFileTool` | `mcp_server/tools/code_tools.py` | Creates/overwrites a file; emits `DeprecationWarning`; enforces path-traversal guard | "[DEPRECATED] create or overwrite a file" | Self-described as deprecated; `scaffold_artifact` replaces all legitimate use cases |

Both files contain **only** the two classes to be removed — entire files are deletable.

### Server Registration

| Symbol | Import line | Registration line | Condition |
|---|---|---|---|
| `CreateFileTool` | `server.py` L68 | `server.py` L367 | Unconditional |
| `ValidateDTOTool` | `server.py` L130 | `server.py` L360 | Unconditional |

### Test Blast Radius

| Test file | Scope of change | Notes |
|---|---|---|
| `tests/mcp_server/unit/tools/test_validation_tools.py` | Remove `ValidateDTOTool` unit tests; **migrate** `test_validation_tool_class_removed` invariant before deleting | Hosts an existing removal invariant that must survive |
| `tests/mcp_server/unit/tools/test_code_tools.py` | Delete entire file | Contains only `CreateFileTool` unit tests |
| `tests/mcp_server/unit/tools/test_dev_tools.py` | Remove 2 `CreateFileTool` functions (L54-77) | Remainder of file is unrelated |
| `tests/mcp_server/unit/tools/test_extra_forbid.py` | Remove `CreateFileInput` import (L7) + parametrize entry (L67); remove `ValidateDTOInput` import (L55) + parametrize entry (L145) | Architecture invariant test; remaining entries unaffected |
| `tests/mcp_server/unit/integration/test_all_tools.py` | Remove imports (L16, L52-53), factory wiring (L221, L224), `test_validation_tool_flow` (L428-436), `test_create_file_tool_flow` (L453-461), parametrize entries (L528-543) | Multiple surgical deletions |
| `tests/mcp_server/tools/test_c4_description_invariants.py` | Remove `ValidateDTOTool` import (L26) + description invariant (L78-82) | Invariant about the tool's own description text — obsolete with tool removed |
| `tests/mcp_server/integration/test_pr_status_lockdown.py` | Remove `CreateFileTool` import (L52) + parametrize entry (L94) | `SafeEditTool` already present at L92 — lockdown coverage remains complete after removal |

### Documentation Blast Radius (Active Files Only)

| File | Change required |
|---|---|
| `docs/reference/mcp/tools/editing.md` | Remove deprecated `create_file` section (L18-29 header, L138 ref, L538-end full section) |
| `docs/reference/mcp/MCP_TOOLS.md` | Remove 2 table rows (`validate_dto`, `create_file`) |
| `docs/reference/mcp/tools/README.md` | Remove 2 table rows |
| `docs/reference/mcp/tools/scaffolding.md` | Remove migration example referencing `create_file` (L368-376) |
| `docs/mcp_server/README.md` | Remove tool references from category listings |
| `docs/mcp_server/TOOLS.md` | Remove 2 inventory rows |
| `docs/mcp_server/architectural_diagrams/08_naming_landscape.md` | Remove `ValidateDTOTool` + `CreateFileTool` table rows |
| `docs/mcp_server/architectural_diagrams/03_tool_layer.md` | Update tool count / remove rows |

### Preservation Goals

| Invariant | Status | Notes |
|---|---|---|
| `TemplateValidationTool` (`validate_template`) | Unaffected | Defined in separate file `template_validation_tool.py`; zero shared state with either tool being removed |
| `test_validation_tool_class_removed` invariant | Must migrate | Currently lives in `test_validation_tools.py`; must be re-homed before that file is deleted |
| PR-status lockdown coverage | Safe | `SafeEditTool` already present in lockdown parametrize list (L92); removing `CreateFileTool` (L94) leaves coverage complete |
| `extra='forbid'` invariant test coverage | Shrinks (safe) | `test_extra_forbid.py` parametrize list loses 2 entries; architectural rule itself remains enforced via the remaining entries |

### Candidate Seams

| Seam | Description | Dependencies |
|---|---|---|
| S1: Production file deletion | Delete `validation_tools.py` + `code_tools.py` + `server.py` unregistration | Independent of tests; unblocks compilation verification |
| S2: Dedicated test file deletion | Delete `test_code_tools.py`; update `test_validation_tools.py` with invariant migration | Depends on S1 |
| S3: Shared test file cleanup | Update `test_dev_tools.py`, `test_extra_forbid.py`, `test_all_tools.py`, `test_c4_description_invariants.py`, `test_pr_status_lockdown.py` | Depends on S1 |
| S4: Documentation cleanup | Remove/update 8 active documentation files | Independent; can run parallel to S2/S3 |

---

## Open Questions

- **Q1 (resolved):** Is `SafeEditTool` already in `test_pr_status_lockdown.py`? Yes, at L92. Lockdown coverage is safe after `CreateFileTool` removal.
- **Q2 (for planning):** Where should `test_validation_tool_class_removed` be migrated? Options: new `test_removed_tool_invariants.py`; inline into `test_c4_description_invariants.py`. Planning must decide.

---

## Approved Strategy

| Boundary | Selected strategy | Rationale | Constraints for later phases |
|---|---|---|---|
| `ValidateDTOTool` + `ValidateDTOInput` | Clean break | No external callers beyond LLM agents; tool provides zero structural validation value; Pydantic + pytest already cover the invariants the tool claimed to check | No compatibility shim; no opt-out; direct deletion. `test_validation_tool_class_removed` invariant must be migrated, not deleted. |
| `CreateFileTool` + `CreateFileInput` | Clean break | Tool is self-described as deprecated; `scaffold_artifact` is the approved replacement; no legitimate use case remains | No compatibility shim; no opt-out; direct deletion. Lockdown coverage confirmed safe via existing `SafeEditTool` presence. |

---

## Related Documentation
- **[mcp_server/tools/validation_tools.py][related-1]**
- **[mcp_server/tools/code_tools.py][related-2]**
- **[mcp_server/server.py][related-3]**
- **[docs/development/issue346/research.md][related-4]**

<!-- Link definitions -->

[related-1]: mcp_server/tools/validation_tools.py
[related-2]: mcp_server/tools/code_tools.py
[related-3]: mcp_server/server.py
[related-4]: docs/development/issue346/research.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-06-05 | Agent | Initial research — blast radius analysis, preservation goals, approved strategy |
