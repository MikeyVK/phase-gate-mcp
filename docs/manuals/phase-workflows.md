# Workflow Guide

## Purpose

Workflows organize project work into configured phases and contracts. This page is an
orientation guide; it does not define a universal phase sequence, GitHub-label lifecycle,
or mandatory TDD ceremony. The selected workflow configuration, active project plan, and
host instructions determine the actual phases, deliverables, checks, and transition rules.

## Find the active workflow

Use `get_work_context` to inspect the current project and phase context, and consult the
project plan and configured workflow contracts for the work item. Workflow types include
feature, bug, refactor, docs, hotfix, chore, and epic; their phase sequences can differ.
For example, a documentation workflow may use a shorter path than a feature workflow.
The configuration and project plan, not a fixed table in this guide, resolve the current
sequence.

## Work within the active phase

Use the project’s current tool references and configured contracts for the task at hand.
Common capabilities include project planning and phase/cycle transitions, Git and GitHub
operations, artifact scaffolding and safe editing, and configured checks, tests, and fixes.
The current check/test/fix MCP operations are `run_checks`, `run_tests`, and
`apply_fixes`; use the [tool reference index](../reference/tools/README.md) and
[quality tool reference](../reference/tools/quality.md) for their live contracts.

Apply strict RED → GREEN → REFACTOR only when the active workflow contract and approved
plan require it. Otherwise use the test strategy appropriate to the change, preserve the
required deliverables, and satisfy the configured transition contract. Domain findings,
operational failures, and partial native fixes retain the meanings defined by their
owning tool and result contracts.

## Related documentation

- [AGENTS.md](../../AGENTS.md) — active agent protocol and tool priorities.
- [Workflow and phase configuration](../reference/config-loading-architecture.md) —
  configuration-loading boundaries.
- [Tool reference index](../reference/tools/README.md) — current MCP tool contracts.
- [Quality gates](../coding_standards/QUALITY_GATES.md) — validation standards.
- [Architecture manual](architecture.md) — current runtime orientation.
