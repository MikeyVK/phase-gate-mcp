<!-- docs/coding_standards/DOCUMENTATION_STANDARD.md -->
<!-- template=generic_doc version=43c84181 created=2026-05-21T00:00:00Z updated= -->
# Documentation Standard

**Status:** DEFINITIVE  
**Version:** 1.2  
**Last Updated:** 2026-10-03

---

## Purpose

Define shared standards for drafting and presenting project documentation so workflow phase instructions can stay focused on phase-specific content and decisions.

## Prerequisites

Read these first:
1. Read the current workflow phase instructions from get_work_context.
2. Read the phase-specific standards referenced by the current phase, especially ARCHITECTURE_PRINCIPLES.md when design or implementation choices are in scope.
---

## Summary

This document defines the shared documentation rules for pre-implementation and other governed project documents. It explains when standards apply, how to draft before scaffolding, how to present information clearly, and how documentation standards interact with phase-specific instructions and templates.





---

## When To Read

- Read this before drafting or scaffolding research, design, planning, or other governed project documents.
- Use this as the shared documentation baseline; phase instructions still define what belongs in the current phase.
- Re-read this when a document starts to drift into long prose, weak evidence, or phase mixing.

## Core Rules

- Apply the content boundaries of the current phase before scaffolding, not after.
- Treat scaffolding as a writing accelerator, not as a discovery tool for what belongs in the document.
- Carry the same standards from the draft nucleus into the final scaffolded document.
- If phase-specific instructions and this document differ, follow the phase-specific instructions for phase content and this document for documentation quality.

## Presentation Rules

- Prefer tables when comparing options, risks, dependencies, boundaries, interfaces, stakeholders, or expected versus actual behavior.
- Use Mermaid diagrams when they materially clarify flows, boundaries, dependencies, or system relationships.
- Do not use ASCII diagrams in Markdown documents.
- Avoid long unstructured prose when a table, short list, or Mermaid diagram communicates the same information more clearly.
- Prefer concise evidence-backed statements over broad narrative summaries.

## Scaffolded Document Metadata And Whitespace

Full-document packages require one shared `document_metadata` input with an explicit
status and a nonempty ordered revision list. Each revision supplies version, date, author
and change. The visible header takes current version/date from the final supplied
revision; the terminal Version History table preserves the caller's sequence and facts.
Do not fabricate approval, authorship, dates or revisions, and do not sort the history.
Metadata remains mandatory for minimal full-document contexts. Technical first-line
provenance identifies the template/package/suite; it is separate from authored document
facts and does not replace the visible header or history.

Issue, PR and Commit packages follow their own body/message contracts. They do not
inherit the full-document header/history. Publication title, labels and other envelope
fields belong to the publication tool. Retain technical provenance in the saved local
artifact; exclude that single recognized first-line marker from a published body.

Templates own section/list joins and one terminal LF. Boundary-only normalization of
chosen prose/code fragments removes blank edge lines while preserving internal blank
lines, line endings, Markdown hard-break spaces, fence indentation and literal data.
Omitted optional content and defined empty content have distinct meanings; preserve
explicit empty carriers where the package contract admits them. Scaffolded structure is
a valid starting point, requiring authored content review rather than declaring a finished
or approved document. Native syntax/style acceptance does not prove semantic quality.

## Evidence And Traceability

- Prefer concrete evidence over general statements: cite specific files, symbols, behaviors, interfaces, flows, logs, or references where possible.
- For tool-run claims in committed documents and hand-overs, record the relevant invocation/scope and observed outcome, or link to durable evidence containing those facts. Transient cache URIs and run IDs may supplement that evidence, but must not be its sole basis.
- Treat external findings as evidence, not as decisions.
- Separate observed facts, assumptions, open questions, and chosen decisions clearly.
- If an external claim cannot be traced to a source, do not present it as established fact.

## Phase Ownership

- Research documents investigate the problem space, constraints, prior art, and unknowns; they do not choose design or implementation. They must define the Approved Strategy (compatibility and migration policy per boundary, with rationale) and the Expected Results (behavioral success criteria) before the phase transitions to Design.
- Design documents compare options, justify a chosen direction, and define interfaces and trade-offs; they do not become implementation plans. To prevent divergent or creative implementations, design documents should define concrete interface contracts (such as Pydantic models, configuration schemas, and method signatures without bodies). They must avoid "implementation bleed", meaning they do not contain concrete method bodies (the logic under the def statement), helper-level variable mappings, or patch sequences.
- Planning documents define slices, cycles, dependencies, and stop-go criteria; they do not repeat research or redesign the solution.
- Implementation details, patch plans, and execution sequencing belong in implementation work, not in pre-implementation documentation unless explicitly required by the current phase.

## Drafting Workflow

- Form a stable nucleus before scaffolding so the first scaffolded draft is directionally correct.
- Use the scaffolded template structure deliberately; fill optional sections when they materially improve understanding.
- If a section starts mixing phases, move that content to the appropriate phase artifact instead of stretching the current document.
- Before finalizing, check whether a table or Mermaid diagram would communicate the core information better than prose.

## Related Documentation
- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md][related-1]**
- **[docs/coding_standards/CODE_STYLE.md][related-2]**
- **[docs/coding_standards/TYPE_CHECKING_PLAYBOOK.md][related-3]**
- **[docs/coding_standards/QUALITY_GATES.md][related-4]**

<!-- Link definitions -->

[related-1]: ARCHITECTURE_PRINCIPLES.md
[related-2]: CODE_STYLE.md
[related-3]: TYPE_CHECKING_PLAYBOOK.md
[related-4]: QUALITY_GATES.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 |  | Agent | Initial draft |
| 1.1 | 2026-06-17 | Agent | Clarify distinction between interface contracts and implementation bleed |
| 1.2 | 2026-10-03 | @imp implementer | Align required full-document metadata/history, tracking publication boundaries and whitespace ownership with the approved template contracts; correct local related links. |
