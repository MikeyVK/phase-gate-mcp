<!-- docs\development\issue341\research.md -->
<!-- template=research version=8b7bb3ab created=2026-05-23T09:33Z updated= -->
# Research: @co as end-to-end epic workflow owner

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-05-23

---

## Purpose

Capture the pre-research nucleus for issue #341 and preserve the analysis discovered during issue #268 before any implementation work is considered.

## Scope

**In Scope:**
Epic workflow ownership, role authority, allowed tool sets, epic phase instructions, hand-over paths, documentation authority, and any minimal runtime implications needed to make the model coherent.

**Out of Scope:**
Implementing the redesign, reopening issue #268 C1-C8 implementation code, introducing a generic phase-ownership system, or redesigning non-epic workflows.

## Prerequisites

Read these first:
1. Read `AGENTS.md` role and workflow definitions
2. Read `.github/agents/co.agent.md` and `.github/agents/imp.agent.md`
3. Read `docs/development/issue268/research.md` findings around lifecycle coordination
4. Read `.phase-gate/config/contracts.yaml` epic phase instructions
---

## Problem Statement

The current workflow model shows a semantic mismatch around epic execution. The repository treats `epic` as a large multi-issue coordination workflow, but the active execution rails still lean on `@imp`, which is primarily the implementation executor. This creates friction in epic-specific phases, especially `coordination`, where the semantics point toward `@co` while the mechanics still depend on `@imp`.

The resulting ambiguity makes it hard to answer simple questions cleanly:
- who actually owns an epic branch
- who is allowed to mutate epic workflow state and artifacts
- who hands over to QA from epic phases
- whether epic work is coordination/governance work or implementation work

## Research Goals

- Determine whether `@co` should own epic branches from research through ready
- Identify the smallest coherent change set needed in role definitions, phase contracts, and related docs
- Determine whether workflow-level ownership is sufficient without introducing generic phase ownership
- Define the revised hand-over paths if `@co` becomes the producer for epic phases
- Identify which existing documentation is authoritative versus stale and needs reconciliation

---

## Background

This follow-up was discovered during issue #268 while reconciling workflow-phase instructions in `contracts.yaml`, role definitions in `AGENTS.md`, the role boundaries in `co.agent.md` and `imp.agent.md`, and the semantics of the epic `coordination` phase. The immediate trigger was the observation that epic coordination semantics do not fit naturally inside the current `@imp` sub-role model, even though broader epic ownership already points toward `@co`.

---

## Findings

Working hypothesis: `@co` already fits the semantic role of epic owner better than `@imp`. The shortest high-value redesign is likely a workflow-level rule: `@co` owns the `epic` workflow end-to-end, while `@imp` executes only child issues delegated from the epic.

Evidence already identified:
- `AGENTS.md` defines `epic` as a large multi-issue workflow and `@co` as coordination authority.
- `.github/agents/co.agent.md` already aligns with backlog, issue, and prioritization authority, but currently lacks the mutation tools needed to carry epic phases end-to-end.
- `.github/agents/imp.agent.md` is broad enough to execute artifact-producing phases today, but semantically fits child-issue execution better than epic governance.
- `docs/development/issue268/research.md` already argues for `@co` as lifecycle coordinator and places lifecycle-boundary writes with `@co`.
- `.phase-gate/config/contracts.yaml` shows the current epic phase instructions and where the semantic mismatch is currently expressed.
- `docs/architecture/VSCODE_AGENT_ORCHESTRATION.md` likely contains drift and should be treated as evidence to reconcile, not as current authority.

## Open Questions

- ❓ Should `@co` own epic branches from research through ready?
- ❓ If yes, which mutation tools must be added to `@co`, and which must remain forbidden?
- ❓ Should epic QA reviews hand back to `@co` by default instead of `@imp`?
- ❓ Is a workflow-level ownership rule enough, or is some smaller runtime hint still required?
- ❓ Which existing documentation becomes stale immediately if this direction is adopted?
- ❓ What is the smallest migration path that preserves current workflow correctness while clarifying ownership?


## Related Documentation
- **[AGENTS.md][related-1]**
- **[.github/agents/co.agent.md][related-2]**
- **[.github/agents/imp.agent.md][related-3]**
- **[.github/agents/qa.agent.md][related-4]**
- **[.phase-gate/config/contracts.yaml][related-5]**
- **[.phase-gate/config/workflows.yaml][related-6]**
- **[docs/development/issue268/research.md][related-7]**
- **[docs/architecture/VSCODE_AGENT_ORCHESTRATION.md][related-8]**

<!-- Link definitions -->

[related-1]: AGENTS.md
[related-2]: .github/agents/co.agent.md
[related-3]: .github/agents/imp.agent.md
[related-4]: .github/agents/qa.agent.md
[related-5]: .phase-gate/config/contracts.yaml
[related-6]: .phase-gate/config/workflows.yaml
[related-7]: docs/development/issue268/research.md
[related-8]: docs/architecture/VSCODE_AGENT_ORCHESTRATION.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 |  | Agent | Initial draft |