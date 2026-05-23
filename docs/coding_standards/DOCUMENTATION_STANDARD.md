<!-- docs/coding_standards/DOCUMENTATION_STANDARD.md -->
<!-- template=generic_doc version=43c84181 created=2026-05-21T00:00:00Z updated= -->
# Documentation Standard

**Status:** DEFINITIVE  
**Version:** 1.0  
**Last Updated:** 2026-05-21

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

## Evidence And Traceability

- Prefer concrete evidence over general statements: cite specific files, symbols, behaviors, interfaces, flows, logs, or references where possible.
- Treat external findings as evidence, not as decisions.
- Separate observed facts, assumptions, open questions, and chosen decisions clearly.
- If an external claim cannot be traced to a source, do not present it as established fact.

## Phase Ownership

- Research documents investigate the problem space, constraints, prior art, and unknowns; they do not choose design or implementation.
- Design documents compare options, justify a chosen direction, and define interfaces and trade-offs; they do not become implementation plans.
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

[related-1]: docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
[related-2]: docs/coding_standards/CODE_STYLE.md
[related-3]: docs/coding_standards/TYPE_CHECKING_PLAYBOOK.md
[related-4]: docs/coding_standards/QUALITY_GATES.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 |  | Agent | Initial draft |