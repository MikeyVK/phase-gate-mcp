---
name: resume-work
description: Rebuild implementation context after compaction without relying on hidden workflow state.
agent: imp
argument-hint: Optionally add the exact task or file set you want to resume.
---

# Resume Work

Reconstruct the active implementation context before making changes.

## Recovery Protocol

1. Read [AGENTS.md](../../AGENTS.md).
2. Read [.github/copilot-instructions.md](../copilot-instructions.md).
3. Read [docs/coding_standards/ARCHITECTURE_PRINCIPLES.md](../../docs/coding_standards/ARCHITECTURE_PRINCIPLES.md).
4. Inspect the current worktree before editing anything.
5. Reconstruct scope from the latest user request, the current conversation, visible files in scope, and any explicit plan or handover.

## Required Output

Respond with these sections before you continue implementation:
1. Recovered goal
2. Active sub-role
3. Files in scope
4. Verification state
5. Next concrete step
6. Missing context or blockers
