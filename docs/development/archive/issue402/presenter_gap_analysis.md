<!-- docs\development\issue402\presenter_gap_analysis.md -->
<!-- template=generic_doc version=43c84181 created=2026-06-15T16:52Z updated= -->
# Gap Analysis: Architectural Correctness & Completeness of TextPresenter

**Status:** APPROVED  
**Version:** 1.0.0  
**Last Updated:** 2026-06-15

---

## Purpose

Analyze formatting of tool responses, identify architectural patterns that bypass TextPresenter, and document gaps for a future issue.

---

## Summary

During validation of Issue 402, an architectural review of TextPresenter and NoteContext revealed several gaps where presentation is hardcoded in Python.

---

## Detailed Findings & Gaps

### 1. Hardcoded URI Reference
- **Location:** `mcp_server/server.py`
- **Code:**
  ```python
  full_text = (
      f"{text}\n\n"
      f"JSON data for this run is available as an MCP Resource: {uri}"
  )
  ```
- **Description:** The URI reference text is hardcoded directly in Python instead of using the template configured in `presentation.yaml` under `global.next_instruction_texts.uri_reference`.

### 2. Bypassing Presenter via Note rendering (`to_message`)
- **Location:** `mcp_server/core/operation_notes.py`
- **Description:** Each note class implements a hardcoded `to_message` formatting method in Python (e.g., `ExclusionNote` returning `"Excluded from commit index: {file}"`). This formatting ignores `presentation.yaml`.

### 3. Hardcoded Emojis in Note Classes
- **Location:** `mcp_server/core/operation_notes.py`
- **Description:** Emojis (like `🩹` or `🚀`) are hardcoded in note messages. This prevents changing them from `presentation.yaml` and causes design inconsistency.

### 4. Duplicate Output Defect (Presenter vs. Notes)
- **Location:** `mcp_server/tools/phase_tools.py` and `mcp_server/tools/cycle_tools.py`
- **Description:** Transition tools (like `TransitionPhaseTool`) do two redundant things:
  1. Configure `next_instructions: ["context_reset"]` in `presentation.yaml`.
  2. Call `context.produce(InfoNote(message=TRANSITION_ADVISORY_NOTE))` during execution.
  This causes the exact same message to be printed **twice** in the final tool result (once in the main block and once in the notes block).

### 5. Emojis Hardcoded in DTOs and Tool Code
- **Location:** `mcp_server/tools/safe_edit_tool.py` and `mcp_server/tools/discovery_tools.py`
- **Description:** Tools hardcode success or failure emojis directly in their `error_message` or warning strings. Because the presenter also automatically prepends emojis on failure (configured via `global.emojis.failure: "❌"`), this leads to double emojis in tool responses (e.g. `❌ File edit rejected: ❌ Failed to write file: ...`).

### 6. Missing `get_work_context` Details in Template
- **Location:** `.phase-gate/config/presentation.yaml`
- **Description:** The template for `get_work_context` is missing placeholders for `{phase_instructions}` and `{invalid_phase_warning}`. As a result, when an agent or human calls `get_work_context`, the actual step-by-step instructions (e.g., `"Run run_quality_gates..."`) are completely hidden from the text output, even though they exist in the Pydantic DTO.

### 7. `None` Value Formatting Bug
- **Location:** `mcp_server/presenters/text_presenter.py`
- **Code:**
  ```python
  format_dict[key] = data_dict.get(key, "")
  ```
- **Description:** When a DTO field is explicitly `None`, `data_dict.get(key, "")` still returns `None` (since the key exists). The Python string formatter then prints `"None"` instead of an empty string.

### 8. ToolResult Success Mapping Bug
- **Location:** `mcp_server/server.py`
- **Code:**
  ```python
  success = getattr(data_dto, "success", True)
  ```
- **Description:** If a tool raises an exception caught by `@tool_error_handler`, it returns a `ToolResult` with `is_error=True`. Since `ToolResult` does not have a `success` attribute, `success` evaluates to `True`. The presenter then attempts to format the error using the tool's success template, which prints empty fields or fallback strings.




## Related Documentation
None
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-15 | Agent | Initial draft |