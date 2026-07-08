<!-- docs\development\issue406\rest_gaps.md -->
<!-- template=generic_doc version=43c84181 created=2026-06-24T05:42Z updated=2026-06-24T07:48Z -->
# Remaining Gaps: Presentation Layer & DTO Refactoring

**Status:** APPROVED  
**Version:** 1.0.0  
**Last Updated:** 2026-06-24

---

## High-Level Overview

Here is a high-level overview of all improvement steps and designs that we have discussed in the past chats and discussions, from the current implementation up to and including the latest DTO redesign:

---

### 1. Phase Transition & Research
* **Gap Documentation:** The branch was temporarily reverted to `research` to document the system-wide gaps ([research_arch_gap.md](file:///c:/temp/pgmcp/docs/development/issue406/research_arch_gap.md)) and the `get_work_context` gaps ([research_get_work_context_gaps.md](file:///c:/temp/pgmcp/docs/development/issue406/research_get_work_context_gaps.md)) in a structured and committed manner. Following this, the branch successfully transitioned to the `design` phase.

### 2. `get_work_context` Presentation Refactoring
* **Exposing Metadata:** Compact fields (`current_cycle`, `sub_phase`, `parent_branch`) are displayed directly in the markdown output to better orient the agent.
* **Declarative None-Handling:** We leverage the existing [SafeNoneFormatter](file:///c:/temp/pgmcp/mcp_server/presenters/text_presenter.py#L25) (`none_value: "-"`) and clean up the templates in [presentation.yaml](file:///c:/temp/pgmcp/.phase-gate/config/presentation.yaml) (e.g., omitting the `#` prefix for issues) to prevent visual prefix leaks like `#-`.
* **Large Instructions Solution ("Nothing" Approach):** We omit `phase_instructions` entirely from the markdown output to prevent client-side file truncation (`output.txt` dumps). This is combined with a highly directive `todo_discipline` next-instruction that forces the agent to read the cached run resource (`pgmcp://cache/runs/{run_id}`).
* **Sanitizing the Tool Layer:** All hardcoded fallback texts and presentation logic are removed from [discovery_tools.py](file:///c:/temp/pgmcp/mcp_server/tools/discovery_tools.py) to satisfy the Presentation Boundary (§15).

### 3. Sanitizing `BaseToolOutput` & Closing Backdoors
* **Cleaning `BaseToolOutput`:** We remove the `error_message` field from [BaseToolOutput](file:///c:/temp/pgmcp/mcp_server/schemas/tool_outputs.py#L14). This prevents tools from returning formatted error messages directly in Python.
* **Declarative Domain Failures:** Domain-level failures of tools (`success=False`) are presented exclusively via tool-specific `template_failure` templates in [presentation.yaml](file:///c:/temp/pgmcp/.phase-gate/config/presentation.yaml), formatted using raw semantic parameters from the DTO (no backdoor strings in Python).

### 4. Redesigning Error DTOs
* **Introducing `BaseErrorOutput`:** We split [error_outputs.py](file:///c:/temp/pgmcp/mcp_server/schemas/error_outputs.py). System, decorator, and platform errors inherit directly from a new `BaseErrorOutput` that contains **no** `success` bool. Only real tool errors (`ToolErrorOutput`) retain the `success=False` property.
* **Type-Safe Status and Routing:** The presenter [text_presenter.py](file:///c:/temp/pgmcp/mcp_server/presenters/text_presenter.py) and server-bridge [server.py](file:///c:/temp/pgmcp/mcp_server/server.py) determine the success status and template routing via type checks (`isinstance(data, BaseErrorOutput)`) instead of fragile string matching on `error_type`.

### 5. Pragmatic Exceptions (Against Class Bloat)
* **Generic Exceptions:** We do not introduce specific exception classes per error type. Instead, we reuse the existing generic classes from [exceptions.py](file:///c:/temp/pgmcp/mcp_server/core/exceptions.py) (such as [PreflightError](file:///c:/temp/pgmcp/mcp_server/core/exceptions.py#L122) and [ValidationError](file:///c:/temp/pgmcp/mcp_server/core/exceptions.py#L52)) by simply providing them with a specific `error_code` and a `params` dictionary.

---

This overview maps out the complete chain with which we restore the presentation boundary, close backdoors, and maximize type safety around errors.

---

## Related Documentation
- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md][related-1]**
- **[docs/development/issue406/research_get_work_context_gaps.md][related-2]**
- **[docs/development/issue406/research_arch_gap.md][related-3]**

<!-- Link definitions -->

[related-1]: docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
[related-2]: docs/development/issue406/research_get_work_context_gaps.md
[related-3]: docs/development/issue406/research_arch_gap.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-24 | Agent | Initial draft containing the English translation of the approved gaps overview. |
