<!-- docs\development\issue289\epic_scope_analysis.md -->
<!-- template=research version=8b7bb3ab created=2026-06-28T16:20Z updated= -->
# Refactoring Epic Scope and Child Issues Analysis

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-06-28

---

## Purpose

Define the execution scope and child issues for Epic #289 to enable step-by-step TDD refactoring.

## Scope

**In Scope:**
Refactoring of exceptions, decorators, schemas, managers, presenters, and 20 tool files.

**Out of Scope:**
New feature development, installable wheel/CLI implementation (which has been moved to Epic #416), and ST3 backend migrations.

## Prerequisites

Read these first:
1. docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
2. docs/development/issue289/tools_error_mapping_research.md
3. docs/development/issue289/presentation_error_codes_design.md
4. docs/development/issue289/implementation_plan.md
---

## Problem Statement

Determine the correct, structured scope for Epic #289 (MCP Server Structural Refactoring & DTO/Exception Segregation) and outline a series of cleanly decoupled child issues based on the findings in the gearchiveerde issue289 docs.

## Research Goals

- Identify the architectural gaps in the current codebase concerning decorators, exceptions, DTOs, and tools.
- Formulate a strategy aligned with ARCHITECTURE_PRINCIPLES.md (SOLID, Presentation Boundary, DIP, etc.).
- Define a clear roadmap of child issues with strict scope boundaries to avoid the chaotic development history of the previous attempt.

---

## Background

The previous attempt under issue #413 suffered from scope creep, repetitive workflow loops, and tool workarounds. By separating the 'Installable Wheel' epic from the 'Structural Refactoring' epic, we have isolated the technical debt. This document maps out the specific refactoring path for the technical debt.

---

## Findings

Based on our analysis of the files in docs/development/issue289/, the core refactoring consists of:
1. **Base Infrastructure (Exception/DTO/Decorator Alignment)**: Removing message: str from custom exception constructors, defining NoteDTO, updating BaseToolOutput with passed and notes, deleting NoteContext and operation_notes.py, and updating server.py/text_presenter.py.
2. **Managers Clean-up**: Eliminating hardcoded strings and note_context parameters from git_manager.py, enforcement_runner.py, artifact_manager.py, and phase_state_engine.py.
3. **51 Core Tool Refactoring Paths**: Batched refactoring of 20 tool files applying the Category A, B, C, D, E recipes.
4. **Test Suite Alignment**: Refactoring 250+ assertions in the test suite to test behavior (class, error codes, parameters) rather than checking exception message strings.

We propose dividing this work into 4 clean child issues under Epic #289:
1. **Child Issue A (Base Infrastructure & Decorators)**: Corresponds to Cycle 6 (tool_outputs, exceptions, decorators, presenter updates, deletion of operation_notes.py).
2. **Child Issue B (Managers Refactoring)**: Corresponds to Cycle 7 (updating git_manager, enforcement_runner, artifact_manager, phase_state_engine).
3. **Child Issue C (Core Tools Refactoring - Batched)**: Corresponds to Cycle 8 (updating all 51 tool path violations in clean batches).
4. **Child Issue D (Test Suite Modernization)**: Standardizing all tests to test behavior (verify exc.code, exc.error_code, exc.params) rather than message strings, eliminating all brittle regex-matching assertions.

---

## Approved Strategy

We will execute a clean-break strategy. No backward compatibility shims or message-based assertions will be maintained. Step proposals will cite ARCHITECTURE_PRINCIPLES.md and undergo strict Go/No-go human gatekeeping.

---

## Expected Results

A robust, highly typed codebase adhering 100% to ARCHITECTURE_PRINCIPLES.md. Core tools will not have try-except blocks or import error DTOs. Exception presentation will be declarative, defined entirely in presentation.yaml. Pyright and all quality gates pass at 10.00/10.

## Related Documentation
None
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-28 | Agent | Initial draft |