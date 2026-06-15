<!-- docs\development\issue404\research.md -->
<!-- template=research version=8b7bb3ab created=2026-06-15T19:45:50Z updated= -->
# Research: Resolving TextPresenter Formatting Gaps

**Status:** APPROVED  
**Version:** 1.0.0  
**Last Updated:** 2026-06-15  

---

## Problem Statement

Investigate formatting and visualization gaps in TextPresenter and operation notes, identify presentation logic leakage in Python codebase, analyze user-facing text patterns in all tools, and define the architecture constraints for a configuration-driven notes system.

## Research Goals

* Identify all user-facing text, emojis, and templates currently hardcoded in Python tool files and note classes.
* Formulate an architectural strategy to extract visual presentation from Python code and centralize it in `presentation.yaml`.
* Establish clear definitions, roles, and multiplicity rules for context notes and next instructions.
* Resolve the formatting behavior of None values and error results in `MCPServer` and `TextPresenter`.

---

## 1. Background & Findings

During the migration of MCP tools to the `ITool` architecture under Issue #402, several formatting and visual issues were identified where python code directly controlled user-facing formatting. 

We performed a systematic codebase scan across all 22 tool and manager files, identifying a total of **205 user-facing strings, exceptions, and emojis**. The complete catalog of these matches is documented in [user_facing_text_inventory.md](user_facing_text_inventory.md).

### 1.1 Hardcoded URI References in `server.py`
In `mcp_server/server.py`, the cache resource reference URI (`pgmcp://cache/runs/{run_id}`) is appended manually to tool text results using string concatenation. This violates the separation of concerns since the transport server should contain zero presentation logic. It also bypasses `presentation.yaml` templates.

### 1.2 Hardcoded Emojis and Opmaak in Python
Notes (defined in `mcp_server/core/operation_notes.py`) and tools (such as `safe_edit_tool.py` and `discovery_tools.py`) hardcode emojis (e.g. `🩹`, `❌`, `⚠️`) and diagnostic messages in Python. When the presenter attempts to prepend status emojis (such as `global.emojis.failure: "❌"`), it results in double emojis in the chat (e.g. `❌ File edit rejected: ❌ Failed to write...`).

### 1.3 Double Rendering of Post-Execution Instructions
Transition tools (like `TransitionPhaseTool` and `TransitionCycleTool`) write `InfoNote(message=TRANSITION_ADVISORY_NOTE)` to the context. However, `presentation.yaml` also defines `next_instructions: ["context_reset"]` for these tools. Because both represent the exact same instruction (*"Call get_work_context now..."*), the text is rendered twice.

### 1.4 Literal "None" Rendering
In `text_presenter.py`, formatting variables are resolved via `format_dict[key] = data_dict.get(key, "")`. If a DTO property is explicitly `None` (such as `parent_branch` or `skip_reason` when empty), python formats this as the literal string `"None"`, which is ugly and confusing.

### 1.5 ToolResult Success Fallback
When a tool execution fails due to an exception, the server wraps it in a `ToolResult` DTO. Because `ToolResult` does not have a `success` attribute, the presenter's `getattr(data_dto, "success", True)` check falls back to `True`. The presenter then erroneously formats the error message using the tool's success template.

---

## 2. Architectural & Design Constraints

This design must conform strictly to [ARCHITECTURE_PRINCIPLES.md](../coding_standards/ARCHITECTURE_PRINCIPLES.md):

* **Single Responsibility Principle (SRP):** Note classes must represent pure data events/containers. They must not contain any formatting, text templates, or emojis. All visual assembly belongs entirely to `TextPresenter`.
* **Config-First & SSOT:** All emojis, headers, and text templates must live in `.phase-gate/config/presentation.yaml`. Python code must only reference keys.
* **Fail-Fast (Drift Validation):** The presenter must validate at startup (via `validate_presentation_alignment`) that all note keys in Python exist in the YAML configuration and that placeholder fields are aligned.
* **Open/Closed Principle (OCP):** Adding a new note or modifying text must be config-driven, requiring zero modifications to the presenter or Note classes.

---

## 3. Strategy Options & Policy Analysis

### Topic 1: Note Class to Message Fallback
* **Option 1: Clean Break (Remove `to_message` on Note classes).**
  * *Pros:* Enforces strict compliance with presenter rendering; no dead code in Python.
  * *Cons:* Breaks legacy tests and non-standard consumers that inspect note text directly.
* **Option 2: Temporary Bridge (Retain a simplified `to_message` as fallback).**
  * *Pros:* Preserves compatibility for unit tests and legacy code paths during migration.
  * *Cons:* Leaves duplicate presentation logic in Python.
* **Selected Strategy:** Option 2. We retain a simplified `to_message()` fallback on Note classes, but the primary server dispatch path (`NoteContext.render_to_response`) is updated to use the presenter.

### Topic 2: Representation of `None` Values
* **Option 1: Replace `None` with empty string `""`.**
  * *Pros:* Keeps inline text flow clean (e.g. `Approved: `).
  * *Cons:* In structured fields or tables, an empty space looks like a missing label or error.
* **Option 2: Replace `None` with hyphen `"-"`.**
  * *Pros:* Clear indicator of an empty value in structured project blocks (e.g. `Milestone: -`, `Parent Branch: -`).
  * *Cons:* Can look awkward in doorlopende prose.
* **Selected Strategy:** Option 2. We replace `None` values with `"-"` for structured labels, configured globally via `global.formatting.none_value: "-"`.

### Topic 3: Transition Tool Post-Execution Instructions
* **Option 1: Clean Break (Remove manual InfoNotes from transition tools).**
  * *Pros:* Eliminates duplicate rendering; makes `presentation.yaml` `next_instructions` the single source of truth.
  * *Cons:* Requires updating transition tool unit tests to expect instructions in the main presenter block instead of the notes block.
* **Selected Strategy:** Option 1. Post-execution transition advice belongs strictly in `presentation.yaml`. We remove the duplicate python notes.

---

## 4. Approved Strategy

### Boundary 1: Note Visuals and Emojis
* **Boundary:** All note templates and emojis.
* **Selected Strategy:** Clean Break. All formatting strings and emojis are moved to `presentation.yaml` under `tools.<tool_name>` and `global.notes`.
* **Constraints:** Must use note-key constants in Python (e.g. `NoteKeys` enum) to ensure static type-safety and prevent key drift.

### Boundary 2: TextPresenter Exception & None Handling
* **Boundary:** `MCPServer` call tool error wrapping and `None` string formatting.
* **Selected Strategy:** Clean Break. The presenter checks `isinstance(dto, ToolResult)` to determine success status and formats `None` values as `"-"` dynamically.

---

## 5. Open Questions

1. **How to test next instructions in unit tests?**
   Since next instructions are added dynamically by the presenter based on the yaml config, how should unit tests verify tool-level next instructions without coupling to the actual file contents of `presentation.yaml`? (Design phase must define mock config injection for tests).

---

## Related Documentation
- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md](../coding_standards/ARCHITECTURE_PRINCIPLES.md)**
- **[docs/development/issue404/user_facing_text_inventory.md](user_facing_text_inventory.md)**
- **[docs/development/issue404/presenter_gap_analysis.md](presenter_gap_analysis.md)**

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-15 | Agent | Initial research draft approved |
