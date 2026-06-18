<!-- docs\development\issue404\user_facing_text_inventory.md -->
<!-- template=generic_doc version=43c84181 created=2026-06-15T19:44Z updated= -->
# User-Facing Text Inventory

**Status:** APPROVED  
**Version:** 1.0.0  
**Last Updated:** 2026-06-15

---

## Purpose

Inventory of all user-facing texts (notes, exceptions, emojis, and error messages) in all MCP tools to serve as the basis for the presenter notes migration.

---

## Summary

A complete catalog of all user-facing texts across the tools and managers codebase. Total matches found: 205.

---

## Scanned Inventory by File

### `mcp_server/managers/enforcement_runner.py`

| Line | Type | Content |
|:---|:---|:---|
| 275 | Exception Raise | `raise ValidationError(` |
| 152 | Exception Raise | `raise ValueError(` |
| 211 | Exception Raise | `raise ConfigError(` |
| 225 | Exception Raise | `raise ConfigError(` |
| 272 | Note Production | `note_context.produce(` |
| 294 | Exception Raise | `raise ConfigError(` |
| 313 | Exception Raise | `raise ValidationError(` |
| 342 | Exception Raise | `raise ValidationError(` |
| 394 | Exception Raise | `raise ConfigError(` |
| 404 | Exception Raise | `raise ValidationError(` |
| 308 | Note Production | `note_context.produce(` |
| 339 | Note Production | `note_context.produce(` |
| 401 | Note Production | `note_context.produce(` |

### `mcp_server/managers/qa_manager.py`

| Line | Type | Content |
|:---|:---|:---|
| 70 | Exception Raise | `raise ValueError("QualityConfig must be injected for quality-gate execution")` |
| 485 | Emoji Detected | `- All-skipped:  ``"✅ Nothing to check (no changed files)[scope_part] — Nms"``` |
| 486 | Emoji Detected | `- Pass:         ``"✅ Quality gates: N/N passed (V violations)[scope_part] — Nms"``` |
| 487 | Emoji Detected | `- Fail:         ``"❌ Quality gates: N/M passed — V violations in` |
| 489 | Emoji Detected | `- Skip+pass:    ``"⚠️ Quality gates: N/N active (S skipped)[scope_part] — Nms"``` |
| 492 | Emoji Detected | `- F-1: all gates skipped → ✅ "Nothing to check" instead of ⚠️.` |
| 523 | Emoji Detected | `return f"✅ Nothing to check (no changed files){scope_part}{duration_part}"` |
| 531 | Emoji Detected | `f"❌ Quality gates: {passed}/{total_active} passed"` |
| 537 | Emoji Detected | `f"⚠️ Quality gates: {passed}/{total_active} active"` |
| 542 | Emoji Detected | `f"✅ Quality gates: {passed}/{total_active} passed"` |
| 1121 | Error Message / Return | `error_message=error_message,` |

### `mcp_server/tools/admin_tools.py`

| Line | Type | Content |
|:---|:---|:---|
| 309 | Exception Raise | `raise ValueError(` |

### `mcp_server/tools/cycle_tools.py`

| Line | Type | Content |
|:---|:---|:---|
| 52 | Exception Raise | `raise ValueError("_BaseIToolTransition requires server_root.")` |
| 71 | Exception Raise | `raise ValueError("ProjectManager must be injected for transition tools")` |
| 77 | Exception Raise | `raise ValueError("PhaseStateEngine must be injected for transition tools")` |
| 83 | Exception Raise | `raise ValueError("GitManager must be injected for cycle transition tools")` |
| 119 | Exception Raise | `raise RuntimeError("Unable to determine current branch")` |
| 185 | Note Production | `context.produce(InfoNote(message=TRANSITION_ADVISORY_NOTE))` |
| 290 | Note Production | `context.produce(InfoNote(message=TRANSITION_ADVISORY_NOTE))` |
| 199 | Note Production | `context.produce(RecoveryNote(message=e.recovery))` |
| 306 | Note Production | `context.produce(RecoveryNote(message=e.recovery))` |
| 167 | Error Message / Return | `error_message="Cannot detect issue number from branch",` |
| 202 | Error Message / Return | `error_message=e.diagnostic,` |
| 211 | Error Message / Return | `error_message=f"Transition failed: {exc}",` |
| 268 | Error Message / Return | `error_message="Cannot detect issue number from branch",` |
| 309 | Error Message / Return | `error_message=e.diagnostic,` |
| 320 | Error Message / Return | `error_message=f"Forced transition failed: {exc}",` |

### `mcp_server/tools/discovery_tools.py`

| Line | Type | Content |
|:---|:---|:---|
| 89 | Exception Raise | `raise ExecutionError("Documentation directory not found")` |
| 86 | Note Production | `context.produce(RecoveryNote(message=f"Expected directory: {docs_dir}"))` |
| 87 | Note Production | `context.produce(RecoveryNote(message="Create docs/ directory in workspace root"))` |
| 88 | Note Production | `context.produce(RecoveryNote(message="Add markdown files to document project"))` |
| 287 | Emoji Detected | `f"⚠️ Invalid workflow state: workflow '{workflow}' does not contains phase '{phase}'.\n"` |

### `mcp_server/tools/git_analysis_tools.py`

| Line | Type | Content |
|:---|:---|:---|
| 104 | Error Message / Return | `error_message=str(e),` |
| 168 | Error Message / Return | `error_message=str(e),` |

### `mcp_server/tools/git_fetch_tool.py`

| Line | Type | Content |
|:---|:---|:---|
| 97 | Error Message / Return | `error_message=str(exc),` |
| 109 | Error Message / Return | `error_message=f"Fetch failed: {exc}",` |

### `mcp_server/tools/git_pull_tool.py`

| Line | Type | Content |
|:---|:---|:---|
| 89 | Exception Raise | `raise ValueError("PhaseStateEngine must be injected for git_pull")` |
| 111 | Error Message / Return | `error_message=str(exc),` |
| 123 | Error Message / Return | `error_message=f"Pull failed: {exc}",` |

### `mcp_server/tools/git_tools.py`

| Line | Type | Content |
|:---|:---|:---|
| 78 | Exception Raise | `raise CommitPhaseMismatchError(msg)` |
| 136 | Exception Raise | `raise ValueError("GitManager must be injected")` |
| 142 | Exception Raise | `raise ValueError("PhaseStateEngine must be injected for git tools that sync state")` |
| 215 | Exception Raise | `raise ValueError("GitManager must be injected")` |
| 221 | Exception Raise | `raise ValueError("PhaseStateEngine must be injected for git tools that sync state")` |
| 337 | Exception Raise | `raise ValueError("GitManager must be injected")` |
| 509 | Exception Raise | `raise ValueError("GitManager must be injected")` |
| 515 | Exception Raise | `raise ValueError("PhaseStateEngine must be injected for git tools that sync state")` |
| 576 | Exception Raise | `raise ValueError("GitManager must be injected")` |
| 583 | Exception Raise | `raise ValueError("PhaseStateEngine must be injected for git tools that sync state")` |
| 672 | Exception Raise | `raise ValueError("GitManager must be injected")` |
| 678 | Exception Raise | `raise ValueError("PhaseStateEngine must be injected for git tools that sync state")` |
| 742 | Exception Raise | `raise ValueError("GitManager must be injected")` |
| 748 | Exception Raise | `raise ValueError("PhaseStateEngine must be injected for git tools that sync state")` |
| 814 | Exception Raise | `raise ValueError("GitManager must be injected")` |
| 820 | Exception Raise | `raise ValueError("PhaseStateEngine must be injected for git tools that sync state")` |
| 890 | Exception Raise | `raise ValueError("GitManager must be injected")` |
| 896 | Exception Raise | `raise ValueError("PhaseStateEngine must be injected for git tools that sync state")` |
| 968 | Exception Raise | `raise ValueError("GitManager must be injected")` |
| 974 | Exception Raise | `raise ValueError("PhaseStateEngine must be injected for git tools that inspect state")` |
| 1046 | Exception Raise | `raise ValueError("GitManager must be injected")` |
| 92 | Exception Raise | `raise CommitPhaseMismatchError(msg)` |
| 359 | Exception Raise | `raise ValueError("PhaseStateEngine must be injected for auto-detection")` |
| 447 | Note Production | `ctx.produce(CommitNote(commit_hash=commit_hash))` |
| 181 | Error Message / Return | `error_message=str(e),` |
| 254 | Error Message / Return | `error_message=str(e),` |
| 367 | Error Message / Return | `error_message=(` |
| 406 | Error Message / Return | `error_message=(` |
| 419 | Error Message / Return | `error_message=str(e),` |
| 464 | Error Message / Return | `error_message=str(e),` |
| 535 | Error Message / Return | `error_message=str(e),` |
| 608 | Error Message / Return | `error_message=str(exc),` |
| 705 | Error Message / Return | `error_message=str(e),` |
| 772 | Error Message / Return | `error_message=str(e),` |
| 844 | Error Message / Return | `error_message=str(e),` |
| 927 | Error Message / Return | `error_message=str(e),` |
| 989 | Error Message / Return | `success=False, error_message="PhaseStateEngine must be injected", branch=""` |
| 1005 | Error Message / Return | `error_message=f"Failed to get parent branch: {exc}",` |
| 1062 | Error Message / Return | `error_message=None` |
| 1074 | Error Message / Return | `error_message=str(e),` |

### `mcp_server/tools/issue_tools.py`

| Line | Type | Content |
|:---|:---|:---|
| 214 | Exception Raise | `raise ExecutionError(f"Issue validation failed: {e}.") from e` |
| 242 | Exception Raise | `raise ExecutionError(f"Label assembly failed: {e}.") from e` |
| 244 | Exception Raise | `raise ExecutionError(str(e)) from e` |
| 284 | Exception Raise | `raise ExecutionError(str(e)) from e` |
| 356 | Exception Raise | `raise ExecutionError(str(e)) from e` |
| 413 | Exception Raise | `raise ExecutionError(str(e)) from e` |
| 454 | Exception Raise | `raise ExecutionError(str(e)) from e` |

### `mcp_server/tools/label_tools.py`

| Line | Type | Content |
|:---|:---|:---|
| 131 | Exception Raise | `raise ExecutionError(error_msg)` |
| 136 | Exception Raise | `raise ExecutionError(` |
| 142 | Exception Raise | `raise ExecutionError(` |
| 148 | Exception Raise | `raise ExecutionError(` |
| 302 | Exception Raise | `raise ExecutionError(f"Labels not valid per labels.yaml: {invalid}")` |
| 75 | Exception Raise | `raise ExecutionError(str(e)) from e` |
| 160 | Exception Raise | `raise ExecutionError(str(e)) from e` |
| 201 | Exception Raise | `raise ExecutionError(str(e)) from e` |
| 249 | Exception Raise | `raise ExecutionError(str(e)) from e` |
| 308 | Exception Raise | `raise ExecutionError(f"Label '{label}' rejected: unknown workphase. {reason}")` |
| 319 | Exception Raise | `raise ExecutionError(str(e)) from e` |

### `mcp_server/tools/milestone_tools.py`

| Line | Type | Content |
|:---|:---|:---|
| 72 | Exception Raise | `raise ExecutionError(str(e)) from e` |
| 125 | Exception Raise | `raise ExecutionError(str(e)) from e` |
| 169 | Exception Raise | `raise ExecutionError(str(e)) from e` |

### `mcp_server/tools/phase_tools.py`

| Line | Type | Content |
|:---|:---|:---|
| 75 | Exception Raise | `raise ValueError(msg)` |
| 97 | Exception Raise | `raise ValueError(` |
| 125 | Exception Raise | `raise ValueError("ProjectManager must be injected for transition tools")` |
| 131 | Exception Raise | `raise ValueError("PhaseStateEngine must be injected for transition tools")` |
| 175 | Note Production | `context.produce(InfoNote(message=TRANSITION_ADVISORY_NOTE))` |
| 270 | Note Production | `context.produce(InfoNote(message=TRANSITION_ADVISORY_NOTE))` |
| 189 | Note Production | `context.produce(RecoveryNote(message=e.recovery))` |
| 286 | Note Production | `context.produce(RecoveryNote(message=e.recovery))` |
| 31 | Emoji Detected | `"🚀 REQUIRED NEXT STEP: Call get_work_context now before any other tool call "` |
| 192 | Error Message / Return | `error_message=e.diagnostic,` |
| 200 | Error Message / Return | `error_message=f"Transition failed: {e}",` |
| 258 | Emoji Detected | `f"⚠️ ACTION REQUIRED: {len(blocking)} skipped gate(s) would have"` |
| 289 | Error Message / Return | `error_message=e.diagnostic,` |
| 299 | Error Message / Return | `error_message=f"Force transition failed: {e}",` |

### `mcp_server/tools/pr_tools.py`

| Line | Type | Content |
|:---|:---|:---|
| 93 | Exception Raise | `raise ExecutionError(str(e)) from e` |
| 157 | Exception Raise | `raise ExecutionError(str(e)) from e` |
| 197 | Exception Raise | `raise ExecutionError(str(e)) from e` |
| 276 | Exception Raise | `raise ExecutionError(str(exc)) from exc` |
| 299 | Exception Raise | `raise ExecutionError(str(exc)) from exc` |
| 307 | Exception Raise | `raise ExecutionError(f"PR created but retrieval/mapping failed: {e}") from e` |
| 290 | Note Production | `context.produce(` |

### `mcp_server/tools/project_tools.py`

| Line | Type | Content |
|:---|:---|:---|
| 70 | Exception Raise | `raise ValueError(` |
| 381 | Note Production | `context.produce(` |
| 299 | Error Message / Return | `error_message=str(e),` |
| 389 | Error Message / Return | `error_message=f"No project plan found for issue #{params.issue_number}",` |
| 397 | Error Message / Return | `error_message=str(e),` |
| 488 | Error Message / Return | `error_message="Planning deliverables not found after saving",` |
| 537 | Error Message / Return | `error_message=str(e),` |
| 628 | Error Message / Return | `error_message="Planning deliverables not found after updating",` |
| 677 | Error Message / Return | `error_message=str(e),` |

### `mcp_server/tools/quality_tools.py`

| Line | Type | Content |
|:---|:---|:---|
| 52 | Exception Raise | `raise ValueError("files must be a non-empty list when scope='files'")` |
| 55 | Exception Raise | `raise ValueError(` |
| 144 | Note Production | `context.produce(` |
| 203 | Exception Raise | `raise ValueError("files must be a non-empty list when scope='files'")` |
| 206 | Exception Raise | `raise ValueError(` |
| 116 | Note Production | `context.produce(RecoveryNote(message=e.recovery))` |
| 126 | Note Production | `context.produce(` |
| 119 | Error Message / Return | `error_message=e.diagnostic,` |
| 133 | Error Message / Return | `error_message=str(e),` |

### `mcp_server/tools/safe_edit_tool.py`

| Line | Type | Content |
|:---|:---|:---|
| 81 | Exception Raise | `raise ValueError("start_line must be >= 1")` |
| 83 | Exception Raise | `raise ValueError("end_line must be >= 1")` |
| 85 | Exception Raise | `raise ValueError("start_line must be <= end_line")` |
| 103 | Exception Raise | `raise ValueError("at_line must be >= 1")` |
| 164 | Exception Raise | `raise ValueError(` |
| 170 | Exception Raise | `raise ValueError(` |
| 177 | Exception Raise | `raise ValueError(` |
| 495 | Exception Raise | `raise ValueError(` |
| 499 | Exception Raise | `raise ValueError(` |
| 509 | Exception Raise | `raise ValueError(` |
| 541 | Exception Raise | `raise ValueError(` |
| 584 | Exception Raise | `raise ValueError(f"Invalid regex pattern: {e}") from e` |
| 72 | Emoji Detected | `"⚠️ MUST include trailing newline (\\n) unless intentionally joining with next line. "` |
| 118 | Emoji Detected | `"⚠️ CRITICAL: Bundle ALL edits for the same file in ONE call! "` |
| 285 | Error Message / Return | `error_message=(` |
| 286 | Emoji Detected | `f"❌ Edit rejected due to validation errors "` |
| 308 | Emoji Detected | `error_message=f"❌ Failed to write file: {e}",` |
| 308 | Error Message / Return | `error_message=f"❌ Failed to write file: {e}",` |
| 331 | Error Message / Return | `error_message=(` |
| 332 | Emoji Detected | `f"❌ File '{params.path}' is already being edited. "` |
| 350 | Error Message / Return | `error_message=(` |
| 362 | Error Message / Return | `error_message=(` |
| 374 | Error Message / Return | `error_message=(` |
| 387 | Error Message / Return | `error_message=f"Failed to read file: {e}",` |
| 408 | Error Message / Return | `error_message=(` |
| 426 | Error Message / Return | `error_message=f"Line edit failed: {e}",` |
| 442 | Error Message / Return | `error_message=f"Insert lines failed: {e}",` |
| 454 | Emoji Detected | `error_msg = f"❌ Pattern '{params.search}' not found in file\n\n"` |
| 458 | Error Message / Return | `error_message=error_msg,` |
| 468 | Error Message / Return | `error_message=f"Search/replace failed: {e}",` |

### `mcp_server/tools/scaffold_artifact.py`

| Line | Type | Content |
|:---|:---|:---|
| 59 | Exception Raise | `raise ValueError("ArtifactManager must be injected for scaffold_artifact")` |
| 134 | Error Message / Return | `error_message=str(e),` |
| 145 | Error Message / Return | `error_message=str(e),` |

### `mcp_server/tools/scaffold_schema_tool.py`

| Line | Type | Content |
|:---|:---|:---|
| 52 | Exception Raise | `raise ValueError("ArtifactManager must be injected for scaffold_schema")` |
| 101 | Error Message / Return | `error_message=str(e),` |

### `mcp_server/tools/template_validation_tool.py`

| Line | Type | Content |
|:---|:---|:---|
| 74 | Error Message / Return | `error_message=str(e),` |

### `mcp_server/tools/test_tools.py`

| Line | Type | Content |
|:---|:---|:---|
| 65 | Exception Raise | `raise ValueError("Either 'path' or 'scope' must be provided")` |
| 67 | Exception Raise | `raise ValueError("'path' and 'scope' are mutually exclusive — provide one, not both")` |
| 96 | Note Production | `context.produce(InfoNote("Last-failed cache was empty; ran full selection instead."))` |
| 220 | Exception Raise | `raise ExecutionError(f"pytest exited with returncode {result.exit_code}")` |
| 75 | Exception Raise | `raise ValueError(msg)` |
| 202 | Exception Raise | `raise` |
| 205 | Note Production | `context.produce(result.note)` |
| 82 | Exception Raise | `raise ValueError(msg)` |
| 89 | Exception Raise | `raise ValueError(msg)` |
| 196 | Exception Raise | `raise ExecutionError(f"Tests timed out after {effective_timeout}s") from None` |
| 201 | Exception Raise | `raise ExecutionError(f"Failed to run tests: {exc}") from exc` |
| 217 | Note Production | `context.produce(RecoveryNote(msg))` |
| 190 | Note Production | `context.produce(` |
| 198 | Note Production | `context.produce(` |
| 230 | Error Message / Return | `is_collection_error=f.is_collection_error,` |

### `mcp_server/tools/tool_result.py`

| Line | Type | Content |
|:---|:---|:---|
| 49 | Error Message / Return | `is_error=is_error,` |
| 63 | Error Message / Return | `is_error=True,` |

## Related Documentation
- **[docs/development/issue404/research.md](research.md)**
- **[docs/development/issue404/presenter_gap_analysis.md](presenter_gap_analysis.md)**
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-15 | Agent | Initial draft with complete scan results |
