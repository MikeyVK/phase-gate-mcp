# S1mpleTrader V3 - Agent Cooperation Protocol

**Auto-loaded by VS Code** via `chat.useAgentsMdFile: true` — this is the always-on multi-agent
protocol file for the S1mpleTrader V3 workspace.
**Status:** Active | **Type:** Bootloader | **Context:** High-Frequency Trading Platform

> **🛑 STOP & READ:** You are an autonomous developer agent. Your goal is precision and efficiency. **DO NOT ask the user for context we already have.** Follow this protocol to orient yourself and begin work.

---

## 🚀 Phase 1: Orientation Protocol

If you need the big-picture MCP server context (vision, architecture, roadmap), read:
- [docs/reference/mcp/mcp_vision_reference.md](docs/reference/mcp/mcp_vision_reference.md)

**Running this protocol allows you to "download" the current project state into your context.**

### 1.1 Tool Activation (Execute FIRST)

> **⚡ CRITICAL:** VS Code Copilot uses lazy loading for MCP tools. Tools appear "disabled" until activated.

**Activate all tool categories before proceeding:**

```
activate_file_editing_tools              → create_file, safe_edit_file, scaffold_artifact (unified tool for code+docs)
activate_git_workflow_management_tools   → 15 git/PR tools (create_branch, git_status, etc.)
activate_branch_phase_management_tools   → phase transition tools
activate_issue_management_tools          → 6 issue tools (create_issue, list_issues, etc.)
activate_label_management_tools          → 5 label tools
activate_milestone_and_pr_management_tools → milestone + PR list tools
activate_project_initialization_tools    → initialize_project, get_project_plan
activate_code_validation_tools           → 4 validation tools
```

**Why:** Tools are dynamically loaded by VS Code based on semantic name analysis. Without activation, they appear as "disabled by user" (misleading error message). This is a VS Code 1.108+ feature (Dec 2025), not part of MCP specification.

### 1.2 State Synchronization (Execute Immediately)

Don't guess the phase or status. **Query the system:**

1.  **Read Coding Standards:**
    *   `pgmcp://rules/coding_standards` → *Loads TDD rules, Style, Quality Gates.*
    *   Also follow [docs/coding_standards/TYPE_CHECKING_PLAYBOOK.md](docs/coding_standards/TYPE_CHECKING_PLAYBOOK.md) for typing-issue resolution consistency (no global disables; targeted ignores only as last resort).
2.  **Check Development Phase:**
    *   `pgmcp://status/phase` → *Tells you current_phase, active_branch, is_clean.*
3.  **Check Work Context:**
    *   `get_work_context` → *Retrieves active issue, blockers, and recent changes.*

---

## 🔄 Phase 2: Issue-First Development Workflow

**GOLDEN RULE:** Never commit directly to `main`. All work starts with an issue.

### 2.1 Starting New Work

**Workflow Sequence:**
```
1. create_issue(issue_type, title, priority, scope, body) → Create GitHub issue (labels assembled from config, body rendered via Jinja2)
2. create_branch         → Create feature/bug/docs/refactor/hotfix branch
3. git_checkout          → Switch to new branch
4. initialize_project    → Set up workflow, phase state, parent tracking
5. get_project_plan      → Verify workflow phases loaded
```

**Example `create_issue` call (all required fields):**
```python
create_issue(
    issue_type="feature",
    title="Add Redis caching to strategy loader",
    priority="high",
    scope="mcp-server",
    body={
        "problem": "Strategy loader re-reads YAML on every call, causing latency spikes.",
        "expected": "Cached reads with TTL, invalidated on file change.",
        "context": "Observed on high-frequency backtests (>500 calls/s)."
    }
    # Optional: is_epic=False, parent_issue=76, milestone="v1.0.0", assignees=["alice"]
)
# → Creates issue with labels: type:feature, priority:high, scope:mcp-server
# → Returns: issue #47: Add Redis caching to strategy loader
```

**Workflow Types (from `.phase-gate/config/workflows.yaml`):**

| **feature** | 7 phases: research → design → planning → implementation → validation → documentation → ready | New functionality |
| **bug** | 7 phases: research → design → planning → implementation → validation → documentation → ready | Bug fixes |
| **docs** | 3 phases: planning → documentation → ready | Documentation work |
| **refactor** | 6 phases: research → planning → implementation → validation → documentation → ready | Code improvements |
| **hotfix** | 4 phases: implementation → validation → documentation → ready | Urgent fixes |
| **epic** | 6 phases: research → design → planning → coordination → documentation → ready | Large multi-issue initiatives |

**Epic Support:**
- Large issues use `type:epic` label
- Research phase identifies child issues
- Child issues reference parent epic (parent branch tracking)
- Epic hierarchy: `main → epic/76 → feature/77, feature/78`

### 2.2 Phase Progression

**Sequential Transitions (Strict Enforcement):**
```python
transition_phase(branch="feature/42-name", to_phase="design")
# Validates against workflow definition in .phase-gate/config/workflows.yaml
# Must follow sequential order defined in workflow
```

**Forced Transitions (Requires Human Approval):**
```python
force_phase_transition(
    branch="feature/42-name",
    to_phase="ready",
    skip_reason="Skipping validation - already covered by epic-level tests",
    human_approval="User: John approved on 2026-01-09"
)
# Creates audit trail in .phase-gate/state.json
# Only use when documented reason exists
```

### 2.3 Implementation Cycle Within Phase

**RED → GREEN → REFACTOR loop, each cycle numbered. Subphases (red/green/refactor) apply only to phases with `cycle_based: true` in `contracts.yaml` (default: `implementation`).**

| Sub-phase | Commit | Scope format |
|-----------|--------|--------------|
| red | `test(P_IMPLEMENTATION_SP_C1_RED): ...` | `git_add_or_commit(workflow_phase="implementation", sub_phase="red", cycle_number=1, message="...")` |
| green | `feat(P_IMPLEMENTATION_SP_C1_GREEN): ...` | `git_add_or_commit(workflow_phase="implementation", sub_phase="green", cycle_number=1, message="...")` |
| refactor | `refactor(P_IMPLEMENTATION_SP_C1_REFACTOR): ...` | `git_add_or_commit(workflow_phase="implementation", sub_phase="refactor", cycle_number=1, message="...")` |

> `cycle_number` is required for `cycle_based` phases (see `contracts.yaml`). Next cycle: `transition_cycle(to_cycle=2)`.
> `workflow_phase` may be omitted — auto-detect via `state.json`.

**Other phases (no subphases unless optional):**
- `git_add_or_commit(workflow_phase="research", message="...")` → `docs(P_RESEARCH): ...`
- `git_add_or_commit(workflow_phase="documentation", message="...")` → `docs(P_DOCUMENTATION): ...`

**Quality control (REFACTOR sub-phase):**
- `run_quality_gates(scope="files", files=["path/to/file.py"])` — targeted check
- `run_quality_gates(scope="branch")` — branch-wide

**Test execution:**
- Targeted: `run_tests(path="tests/specific_test.py")`
- End of phase: `run_tests(path="tests/")`

**Phase transition after all TDD cycles:**
```python
transition_phase(to_phase="validation")
```

### 2.4 Documentation Phases

**Pre-Development Documentation (research/planning/design phases):**
- Output location: `docs/development/issueXX/` (XX = active issue number)
- Tool: `scaffold_artifact(artifact_type="design|architecture|tracking", name="...", context={...})`
  - Unified tool for ALL artifacts (code + docs)
  - Auto-resolves paths from artifacts.yaml registry

**Documentation Phase (after validation):**
- Focus: Reference docs, project documentation updates
- Tasks: Update issue content, generate PR description, finalize docs
- Quality gate: `validate_architecture(scope="all")`

### 2.5 Work Completion

**PR Creation & Merge:**
```
1. transition_phase(to_phase="ready")
2. submit_pr(head="feature/42", base="main", title="...", body="...")
   ← atomic: neutralizes branch-local artifacts → commits → pushes → creates GitHub PR → sets PRStatus.OPEN
   ← blocked by enforcement unless current_phase == "ready"
   ← also blocked if the branch already has an open PR (check_pr_status)
3. Wait for human approval (ALWAYS REQUIRED)
4. merge_pr(pr_number=X) - only after human approval
5. Branch cleanup - discuss with human (context-dependent)
   - State cleanup (.phase-gate/state.json) is automatic on git_checkout
```

---

## 🛠️ Phase 3: Execution Protocols

**Use the specific protocol for your assigned task. DO NOT perform manual file operations where a tool exists.**

### A. "Implement a New Component" (DTO, Worker, Adapter)
1.  **Scaffold Code:**
    *   `scaffold_artifact(artifact_type="dto|worker|adapter", name="ComponentName", context={...})`
    *   Unified tool for generating code and documentation artifacts
    *   Auto-resolves paths from artifacts.yaml registry
    *   *Result:* Creates impl file with proper structure.
2.  **TDD Loop (Strict):**
    *   Follow Section 2.3 RED → GREEN → REFACTOR cycle
3.  **Phase Transition:**
    *   `transition_phase(to_phase="validation")` after implementation cycles complete

### B. "Create Documentation" (Architecture, Design, Plan)
1.  **Scaffold Document:**
    *   `scaffold_artifact(artifact_type="design|architecture|tracking", name="document-name", context={...})`
    *   Same unified tool as code artifacts
    *   Auto-resolves `docs/development/issueXX/` from artifacts.yaml
    *   *Result:* Creates perfectly structured markdown file.
2.  **Validate:**
    *   `validate_architecture(scope="all")` — verifies doc structure against schema
    *   Manual review: check all required sections are filled in

### C. "Manage Labels & Milestones"
1.  **Create Label:**
    *   `create_label(name="type:feature", color="0e8a16", description="...")`
    *   Labels validated against `.phase-gate/config/labels.yaml`
2.  **Detect Drift:**
    *   `list_labels()` → compare against `.phase-gate/config/labels.yaml`
    *   Missing labels: `create_label(...)` per entry
    *   Obsolete labels: `delete_label(name)` after confirming no active issues use it

---

## ⚠️ Phase 4: Critical Directives (The "Prime Directives")

1.  **Issue-First Development:** Never work directly on `main`. Always start with `create_issue`.
2.  **Workflow Enforcement:** Always `initialize_project` before work. Use `transition_phase` for progression.
3.  **TDD is Non-Negotiable:** If you write code without a test, you are violating protocol.
4.  **Tools > Manual:** Never manually create a file if `scaffold_*` exists. Never manually parse status if `pgmcp://status/*` exists.
5.  **English Artifacts, Dutch Chat:**
    *   Write Code/Docs/Commits in **English**.
    *   Talk to the User in **Dutch** (Nederlands).
6.  **Human-in-the-Loop:** PR merge ALWAYS requires human approval. `force_phase_transition` requires approval + reason.
7.  **Quality Gates:** Run before phase transitions and before PR creation.

---

## 🤝 Three-Agent Model

This project uses three specialized agents. Each runs in a separate VS Code chat session
to prevent role contamination and context pollution.

### Roles

| Agent | Role | Allowed operations |
|-------|------|--------------------|
| `@co` | Coordination authority | Read all; create/update issues, labels, milestones; produce implementation briefs |
| `@imp` | Implementation executor | All PhaseGate MCP tools; file edits; commits; phase transitions |
| `@qa` | QA authority — read-only | Read files; run tests; run quality gates. **No edits, no commits** |

### Sub-roles

**`@co` sub-roles:** `triager` (default), `backlog-reviewer`, `tracker`, `issue-author`  
**`@imp` sub-roles:** `researcher` (default), `planner`, `designer`, `implementer`, `validator`, `documenter`  
**`@qa` sub-roles:** `design-reviewer` (default), `plan-verifier`, `verifier`, `validation-reviewer`, `doc-reviewer`

Declare your active sub-role in the invocation text.  
Example: `@imp implementer: start cycle C_LOADER.5 for issue 257`

### Two-Chat Model

- **Coordination** → use `@co`. When output is actionable (priority changes, new issues, implementation directives), produce a Co → Imp hand-over.
- **Implementation** → use `@imp`. Execute the current cycle. When complete, produce an Imp → QA hand-over.
- **Review** → use `@qa`. Provide findings and a verdict in-chat. If corrections are needed, the user starts a new `@imp` session.

Never mix roles in one session. Fresh context prevents scope contamination and authority confusion.

### Startup Protocol (all roles)

After context compaction or a new session, always rebuild state from scratch:
1. Read this file (AGENTS.md) and `.github/copilot-instructions.md`
2. Call `get_work_context` — active branch, phase, issue
3. Call `get_project_plan(issue_number)` if phase-specific exit criteria are relevant
4. Read the active planning document for the issue

`@imp` additionally reads: `docs/coding_standards/ARCHITECTURE_PRINCIPLES.md` and `docs/coding_standards/TYPE_CHECKING_PLAYBOOK.md` when typing concerns are relevant.

`@qa` additionally reads: same architecture and type-checking docs; plus the latest implementation hand-over.

### Hand-Over Contract

**Co → Imp hand-over:**
```text
## Co → Imp Hand-over

**Directive**: [what to do]
**Issues in scope**: [#N, #M]
**Priority changes applied**: [yes/no, which labels]
**Next @imp sub-role**: [researcher | planner | implementer | ...]
**Out of scope**: [what not to touch]
```

**Imp → QA hand-over:**
```text
### Scope
- what cycle or task was executed
- what was intentionally kept out of scope

### Files
- changed files grouped by role

### Deliverables
- which authoritative deliverables are now satisfied

### Stop-Go Proof
- exact tests run
- exact gate commands or MCP checks run
- exact outcome
```

---

## 🔧 Phase 5: Tool Priority Matrix (MANDATORY)

> **🛑 CRITICAL RULE:** Use PhaseGate MCP tools for ALL operations. NEVER use terminal/CLI or create_file where an MCP tool exists.

### Project Initialization & Planning
| Action | ✅ USE THIS | ❌ NEVER USE |
|--------|-------------|------------|
| Initialize project | `initialize_project(issue_number, workflow_name)` | Manual branch setup |
| Get workflow phases | `get_project_plan(issue_number)` | Read workflows.yaml manually |
| Detect parent branch | `get_parent_branch(branch)` | Manual git reflog parsing |

### Phase Management
| Action | ✅ USE THIS | ❌ NEVER USE |
|--------|-------------|------------|
| Sequential transition | `transition_phase(branch, to_phase)` | Manual state update |
| Forced transition | `force_phase_transition(branch, to_phase, skip_reason, human_approval)` | Skip validation |

### Git Operations
| Action | ✅ USE THIS | ❌ NEVER USE |
|--------|-------------|------------|
| Create branch | `create_branch(branch_type, name, base_branch)` | `run_in_terminal("git checkout -b")` |
| Switch branch | `git_checkout(branch)` | `run_in_terminal("git checkout")` |
| Check status | `git_status()` | `run_in_terminal("git status")` |
| Stage & Commit | `git_add_or_commit(message, workflow_phase?, sub_phase?, commit_type?)` | `run_in_terminal("git add/commit")` |
| List branches | `git_list_branches(verbose, remote)` | `run_in_terminal("git branch")` |
| Push to remote | `git_push(set_upstream)` | `run_in_terminal("git push")` |
| Pull from remote | `git_pull(rebase)` | `run_in_terminal("git pull")` |
| Fetch from remote | `git_fetch(remote, prune)` | `run_in_terminal("git fetch")` |
| Merge branches | `git_merge(branch)` | `run_in_terminal("git merge")` |
| Delete branch | `git_delete_branch(branch, force)` | `run_in_terminal("git branch -d")` |
| Stash changes | `git_stash(action, message, include_untracked)` | `run_in_terminal("git stash")` |
| Restore files | `git_restore(files, source)` | `run_in_terminal("git restore")` |
| Diff statistics | `git_diff_stat(source_branch, target_branch)` | `run_in_terminal("git diff --stat")` |

**`git_add_or_commit` required parameters:** `workflow_phase` (auto-detect via state.json if omitted), `cycle_number` (required in `cycle_based` phases), `sub_phase` (optional). Use `commit_type` only as override. The `phase` parameter does **not** exist — crashes with `extra='forbid'`.

### GitHub Issues
| Action | ✅ USE THIS | ❌ NEVER USE |
|--------|-------------|------------|
| Create issue | `create_issue(issue_type, title, priority, scope, body, is_epic?, parent_issue?, milestone?, assignees?)` | GitHub CLI / manual |
| List issues | `list_issues(state, labels)` | `run_in_terminal("gh issue list")` |
| Get issue details | `get_issue(issue_number)` | `run_in_terminal("gh issue view")` |
| Update issue | `update_issue(issue_number, title, body, state, labels)` | GitHub CLI / manual |
| Close issue | `close_issue(issue_number, comment)` | `run_in_terminal("gh issue close")` |

### GitHub Labels
| Action | ✅ USE THIS | ❌ NEVER USE |
|--------|-------------|------------|
| Create label | `create_label(name, color, description)` | GitHub CLI / manual |
| Delete label | `delete_label(name)` | GitHub CLI / manual |
| List labels | `list_labels()` | `run_in_terminal("gh label list")` |
| Add labels to issue/PR | `add_labels(issue_number, labels)` | GitHub CLI / manual |
| Remove labels | `remove_labels(issue_number, labels)` | GitHub CLI / manual |

### GitHub Milestones
| Action | ✅ USE THIS | ❌ NEVER USE |
|--------|-------------|------------|
| Create milestone | `create_milestone(title, description, due_on)` | GitHub CLI / manual |
| List milestones | `list_milestones(state)` | `run_in_terminal("gh milestone list")` |
| Close milestone | `close_milestone(milestone_number)` | GitHub CLI / manual |

### Pull Requests
| Action | ✅ USE THIS | ❌ NEVER USE |
|--------|-------------|------------|
| Create PR (atomic) | `submit_pr(title, body, head, base, draft)` | `create_pr(...)` (internal, deleted as public tool) |
| List PRs | `list_prs(state, base, head)` | `run_in_terminal("gh pr list")` |
| Merge PR | `merge_pr(pr_number, commit_message, merge_method)` | `run_in_terminal("gh pr merge")` |

### Code Scaffolding (Jinja2 Templates)
| Action | ✅ USE THIS | ❌ NEVER USE |
|--------|-------------|------------|
| Any artifact (code or doc) | `scaffold_artifact(artifact_type="dto|worker|adapter|design|...", name="...", output_path="...", context={...})` | `create_file` with manual code |

**Common artifact types:**
- **Code:** dto, worker, adapter, interface, tool, resource, schema, service
- **Docs:** design, architecture, tracking, generic, research, planning

**Registry:** `.phase-gate/config/artifacts.yaml`

**Template System (Issue #72 - 5-tier Jinja2):**
- Tier 0 (SCAFFOLD) → Tier 1 (CODE/DOC/CONFIG) → Tier 2 (Python/Markdown/YAML) → Tier 3 (component type) → Concrete template
- `output_path` is **optional** — auto-resolved by ArtifactManager via `project_structure.yaml`. Provide only as override.
- `generate_test` is a registry-flag per artifact type (`true` for code, `false` for docs) — test generation not yet implemented in ArtifactManager.

### Quality & Testing
| Action | ✅ USE THIS | ❌ NEVER USE |
|--------|-------------|------------|
| Run tests | `run_tests(path, markers, last_failed_only, scope, timeout, coverage)` | `run_in_terminal("pytest")` |
| Quality gates | `run_quality_gates(scope, files?)` | `run_in_terminal("ruff/mypy/pylint")` |
| Validate template | `validate_template(path, template_type)` | Manual validation |
| Validate architecture | `validate_architecture(scope)` | Manual review |

### Discovery & Context
| Action | ✅ USE THIS | ❌ NEVER USE |
|--------|-------------|------------|
| Get work context | `get_work_context(include_closed_recent)` | Manual file reading |
| Search docs | `search_documentation(query, scope)` | `grep_search` on docs/ |
| Health check | `health_check()` | N/A |

### MCP Server Management
| Action | ✅ USE THIS | ❌ NEVER USE | Notes |
|--------|-------------|------------|-------|
| Hot-reload server | `restart_server()` | Manual process kill | **Use after code changes to MCP tools/server. ⏳ WAIT 3 SECONDS after restart before calling next tool.** Zero client downtime. |

### File Editing
| Action | ✅ USE THIS | ❌ NEVER USE |
|--------|-------------|------------|
| Edit file (multi-mode) | `safe_edit_file(path, content/line_edits/insert_lines/search+replace, mode)` | Manual file editing |
| Create generic file | `create_file(path, content)` | VS Code create_file (deprecated) |

---

### Ready-Phase Enforcement (Issue #283)

`submit_pr` is blocked outside the `ready` phase. All `branch_mutating` tools are blocked while an open PR exists on the current branch.

**Branch-local artifacts** are automatically neutralized by `submit_pr` itself:

| Artifact | Path | Reason |
|----------|------|--------|
| Workflow state | `.phase-gate/state.json` | Branch-local — must never reach main |
| Deliverables | `.phase-gate/deliverables.json` | Branch-local — must never reach main |

Configuration: `.phase-gate/config/enforcement.yaml` + `.phase-gate/config/contracts.yaml`

```
submit_pr          → pre: check_phase_readiness(policy=ready)   → blocked if phase != "ready"
branch_mutating    → pre: check_pr_status                       → blocked if open PR exists
create_branch      → pre: check_branch_policy                   → blocked for invalid base
```

**`submit_pr` atomic flow (self-contained, via `GitManager.prepare_submission`):**
1. Preflight: clean working tree + upstream present (`PreflightError` if not)
2. Filter: detect branch-local artifacts with net diff vs base
3. Conditional: neutralize + commit (skipped if no diffs)
4. Push (always) — internal rollback + RecoveryNote on failure
5. `GitHubManager.create_pr(...)` → GitHub API  
   → on failure + commit made: automatic `rollback_push(context)` + RecoveryNote
6. Write `PRStatus.OPEN` to cache

**`MergePRTool` is intentionally excluded from `BranchMutatingTool`** — it is the escape hatch that clears `PRStatus.OPEN`. Including it would create a deadlock.

---

## 🚫 run_in_terminal Restrictions (CRITICAL)

**`run_in_terminal` is ONLY allowed for:**

✅ **Permitted (rare cases):**
- Development servers where no MCP tool exists (e.g., `npm run dev`, `python -m http.server`)
- Build commands explicitly requested by user
- Smoke tests / exploratory commands approved by user
- Python package installations via pip (when not using install_python_packages tool)

❌ **FORBIDDEN (use MCP tool instead):**
- **File operations** → use `create_file` / `safe_edit_file`
- **Git operations** → use `git_*` tools (see matrix above)
- **Test execution** → use `run_tests` tool
- **File copy/move/delete** → use file editing tools or ask user
- **Quality gates** → use `run_quality_gates` tool
- **Python execution** → use appropriate MCP tool or ask user

**Default rule: If unsure, ask yourself "Is there an MCP tool for this?" If yes → use it. If no → ask user permission first.**

**Restriction prevents bypassing template validation, quality gates, audit trail, and provenance tracking.**

---

## 🏁 Ready State

**If you have run Phase 1: Orientation, you are now READY.**
*   "What is my next task?" → Check `get_work_context`.
*   "How do I build X?" → Check `pgmcp://rules/coding_standards`.
*   "What phase am I in?" → Check `pgmcp://status/phase`.
*   "Which tool should I use?" → **Consult Phase 5: Tool Priority Matrix.**
*   "How do I start work?" → **Follow Phase 2: Issue-First Development Workflow.**
*   "Which agent am I?" → **Consult the Three-Agent Model section above.**

> **Start now by running Phase 1.**
CRITICAL: Read AGENTS.md before any work. Follow Tool Priority Matrix strictly. NEVER use run_in_terminal for file/git/test operations.
