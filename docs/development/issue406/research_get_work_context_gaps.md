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
* **Option B: Dedicated Resource Reference (Current Fallback)**
  * *Description:* Keep `phase_instructions` out of the markdown and only provide a structured reference URI (e.g. `pgmcp://cache/runs/{run_id}`).
  * *Pros:* 100% safe against client-side file truncation.
  * *Cons:* Omit immediate context; the LLM must execute a second action to load the resource.
* **Option C: Progressive Disclosure / Compact Checklist (Selected)**
  * *Description:* The presenter renders a high-level summary checklist (e.g., only the task headers or a truncated block of the first 10 lines) and appends the cache resource link for the full, detailed instructions.
  * *Pros:* Gives immediate context of the next steps without overloading the markdown payload. Safe against client-side truncation.

### 2. None-Value Formatting Gap
- The presenter's `SafeNoneFormatter` formats `None` values into a placeholder (such as `-`), but the template prefix `Issue: #{issue_number}` leads to `Issue: #-` or `Issue: #None` because the `#` is static in the template.
- **Correction:** The presenter must dynamically strip the prefix or allow the template to handle the optional issue number cleanly (e.g. formatting the entire line only if the value exists).

### 3. Tool Layer Presentation Leak
- `discovery_tools.py` contains hardcoded string fallbacks for missing instructions. These must be completely removed, and fallback presentation must be handled by `TextPresenter` using `presentation.yaml` configuration.

---

## Approved Strategy

Adopt a hybrid approach (Option B & C): The TextPresenter will dynamically render short metadata fields (current_cycle, sub_phase, invalid_phase_warning) directly in the markdown. For phase_instructions and handover_templates, the presenter will render a compact summarized preview or checklist along with a dedicated resource link, preventing client-side file truncation. All fallback formatting is moved from discovery_tools.py to the TextPresenter, and None values are formatted cleanly to avoid visual issues like '#None'.

---

## Expected Results

1. get_work_context markdown presents all non-bloating fields (current_cycle, sub_phase, parent_branch) cleanly.
2. None values are presented without prefix leaks (e.g., omitting '#None' entirely or showing 'None').
3. Large phase_instructions are safely displayed or linked without triggering client-side output.txt dumps.
4. discovery_tools.py contains no presentation fallbacks, satisfying the Presentation Boundary (§15).

## Related Documentation
None
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-21 | Agent | Initial draft |