# Quality and Evidence Standards

## Purpose and authority

This page describes how to select and interpret implementation evidence. It does not
define a numbered runtime gate catalog. Workflow contracts and phase instructions own
when checks, tests, fixes, reviews, and handovers are required. Architectural principles
remain binding even when tooling succeeds.

The workspace declarations under `.pgmcp/config/` own check profiles and bindings
(`checks.yaml`), test bindings and activation (`tests.yaml`), and fix bindings
(`fixes.yaml`). Adapter package contracts own supported capabilities and invocation
protocols. Native tool installations and settings belong to the environment owner.
These declarations select admitted work; they do not install tools or reinterpret native
command-line options. See [server configuration](../reference/server-configuration.md)
and [the execution tool reference](../reference/tools/quality.md).

## Selecting evidence

Use the narrowest selection that supports the claim being made:

- `run_checks` selects configured, workspace, branch, or explicit target scope, and
  optionally a configured profile or explicit check IDs.
- `run_tests` selects configured, workspace, or explicit target scope and configured
  test IDs.
- `apply_fixes` requires explicit workspace-relative file targets and selected fix IDs.

Inspect current tool schemas for admitted IDs and defaults. Native arguments keep their
adapter-defined meanings. Before calling a selection a required gate, identify the active
workflow or phase contract, the relevant workspace configuration, and the exact tool call:
scope, targets or profile, selected check or test IDs, and any caller arguments. A wider
explicit-target call is diagnostic unless that authority requires it. Its findings still
need investigation when they reveal a concrete violation of another binding contract;
the diagnostic count alone is not a gate failure. An unavailable required selection is
missing evidence, not a pass.

The current strict Mypy gate is configured for production sources: `pyproject.toml`
sets `files = ["mcp_server"]`. The issue-72 hybrid policy deliberately excluded tests
from strict Mypy because dynamic `Mock` and `AsyncMock` usage produced noisy or false
positives. `run_checks` can still request native Mypy on explicit test targets for
diagnosis; that capability does not make test Mypy mandatory. Making it a required
gate needs an owner-approved scope, baseline and remediation plan, followed by an
explicit workflow/configuration change. Do not use global disables to suppress
individual findings. A fix is a mutation, not evidence that the resulting files
satisfy checks; review its results and affected files, then choose a suitable recheck.

## Interpreting outcomes

Operation success and substantive result are separate facts. Read operation `success`
and any `error_code` together with per-check, per-test, or per-fix results. A completed
check or test may report `failed` without becoming a protocol failure. Unavailable
dependencies, invalid selections, request rejection, interruption, and unconfirmed
process termination are distinct operational outcomes. Do not call an unavailable or
incomplete run a pass.

For fixes, earlier steps can have changed files before a later step fails or cannot run.
The tool reports ordered rows and stops; it does not promise rollback or automatically
start checks. Inspect actual file changes and perform only an authorized narrow recovery
or recheck. Native output is reported as evidence, not normalized into a generic score.

“Quality gate” remains valid as a workflow-policy phrase when a contract requires
evidence before a phase transition. This document defines no numbered gates, universal
test count, coverage threshold, or separate CI command authority.

## Architecture review

Tool output is one part of review. Check the change against
[ARCHITECTURE_PRINCIPLES.md](ARCHITECTURE_PRINCIPLES.md), including responsibility,
configuration-first behavior, constructor injection, narrow read interfaces, CQS,
immutable value objects, import safety, and public-boundary testing. Consult the full
principles for the binding requirements; this list is a review aid, not a replacement.

## Integration test boundary

Integration tests in `tests/mcp_server/integration/` run in the default suite and
exercise multiple real internal layers while isolating external effects:

| Boundary | Rule |
|---|---|
| External API or process adapter | Replace with a controlled test double where the test contract requires isolation. |
| Filesystem writes | Confine to `tmp_path` or another explicitly isolated temporary workspace. |
| Network calls | Do not issue live external requests. |
| Shared mutable state | Keep tests safe under parallel execution. |
| Environment guards | Use the adapter boundary and explicit fixtures rather than environment-dependent skip rules. |

Follow the current pytest configuration and test architecture when adding coverage.

## Review expectations

Reject changes with failing required checks or tests, missing required evidence, unresolved
architecture violations, unsafe external side effects, or claims that overstate native
execution. Confirm that reports distinguish a negative domain result from an operational
failure and that recovery reflects actual mutations.

## Editor assistance

Editor formatting and analysis settings may improve local feedback, but they do not
replace the configured check/test/fix contracts, workflow requirements, or architecture
review.

## Related documentation

- [Execution tools](../reference/tools/quality.md)
- [Architecture principles](ARCHITECTURE_PRINCIPLES.md)
- [Type checking playbook](TYPE_CHECKING_PLAYBOOK.md)
