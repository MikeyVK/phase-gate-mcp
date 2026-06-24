<!-- docs\development\issue406\research_get_work_context_gaps.md -->
<!-- template=research version=8b7bb3ab created=2026-06-21T07:26Z updated= -->
# Research: get_work_context Presentation Gaps

**Status:** APPROVED  
**Version:** 1.0.0  
**Last Updated:** 2026-06-21

---

## Problem Statement

Examine the presentation gaps, None-value formatting issues, and presentation boundary violations in the get_work_context tool and presenter.

## Research Goals

- Investigate options to safely expose phase_instructions in the markdown presentation without causing client-side file truncation.
- Determine how to include non-bloating metadata (current_cycle, sub_phase, invalid_phase_warning) in the presenter.
- Resolve presentation boundary leaks in discovery_tools.py.
- Address None-value formatting leaks like '#None' in templates.

---

## Background

The get_work_context tool is the entry point for all agent sessions. Currently, several of its fields (phase_instructions, current_cycle, sub_phase, handover_template) are omitted in the markdown presentation. Simply injecting large fields like phase_instructions risks triggering client-side file attachments (output.txt), which degrades the LLM's parsing performance. Furthermore, formatting errors like '#None' and inline tool fallbacks violate the codebase standards.

---

## Findings

### 1. Analysis of phase_instructions Presentation Options

To prevent the chat client from dumping the tool response into an `output.txt` file when the `phase_instructions` are large, we evaluate three options:

* **Option A: Full Direct Injection**
  * *Description:* Inject the entire markdown text of `phase_instructions` directly into the template.
  * *Pros:* Simple template rendering.
  * *Cons:* High risk of triggering `output.txt` dumps on long checklists, forcing the LLM to parse files instead of raw markdown text.
* **Option B: Dedicated Resource Reference / "All-or-Nothing" (Selected Strategy)**
  * *Description:* Keep `phase_instructions` entirely out of the markdown and only provide a structured reference URI (e.g. `pgmcp://cache/runs/{run_id}`).
  * *Pros:* 100% safe against client-side file truncation. Keeps the markdown output clean, structured, and short.
  * *Cons:* Requires a highly directive next instruction to force the LLM to read the cache resource.
* **Option C: Progressive Disclosure / Compact Checklist (Rejected)**
  * *Description:* Render a high-level summary checklist or truncated block of instructions.
  * *Pros:* Immediate context.
  * *Cons:* Hard to enforce dynamically and adds parsing complexity.

### 2. None-Value Formatting Gap
- The presenter's `SafeNoneFormatter` formats `None` values into a placeholder (such as `-`), but the template prefix `Issue: #{issue_number}` leads to `Issue: #-` or `Issue: #None` because the `#` is static in the template.
- **Correction:** The presenter must dynamically strip the prefix or allow the template to handle the optional issue number cleanly (e.g. formatting the entire line only if the value exists).

### 3. Tool Layer Presentation Leak
- `discovery_tools.py` contains hardcoded string fallbacks for missing instructions. These must be completely removed, and fallback presentation must be handled by `TextPresenter` using `presentation.yaml` configuration.

---

## Approved Strategy

Adopt the **"Nothing" approach (Option B)**: The `TextPresenter` will completely omit the `phase_instructions` from the markdown presentation to guarantee that the output remains compact and never triggers client-side file truncation. To make this work, a highly directive and strict `next_instruction` warning (e.g., a mandatory TODO discipline rule) will be printed, forcing the agent to immediately read the cached run resource (`pgmcp://cache/runs/{run_id}`) to load the phase's authoritative operational checklist. 

All other non-bloating metadata fields (like `current_cycle`, `sub_phase`, and `parent_branch`) will be rendered directly in the markdown. Hardcoded presentation fallbacks are moved from `discovery_tools.py` to `TextPresenter`, and `None` values are formatted cleanly to prevent visual leaks like `#None`.

---

## Expected Results

1. get_work_context markdown presents all non-bloating fields (current_cycle, sub_phase, parent_branch) cleanly.
2. None values are presented without prefix leaks (e.g., omitting '#None' entirely or showing 'None').
3. Large phase_instructions are completely omitted from the markdown, eliminating the risk of client-side output.txt dumps.
4. A highly directive `next_instruction` block is printed, commanding the LLM to fetch and follow the cached phase instructions resource.
5. discovery_tools.py contains no presentation fallbacks, satisfying the Presentation Boundary (§15).
