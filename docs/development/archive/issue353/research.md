<!-- docs\development\issue353\research.md -->
<!-- template=research version=8b7bb3ab created=2026-05-25T19:23Z updated=2026-05-25 -->
# create_branch: remove implicit auto-checkout (SRP violation)

**Status:** COMPLETE
**Version:** 1.0
**Last Updated:** 2026-05-25

---

## Problem Statement

`GitAdapter.create_branch()` calls `new_branch.checkout()` as an undeclared side effect,
causing the tool to switch the active branch without the caller requesting it.
This violates SRP (ARCHITECTURE_PRINCIPLES §1.1): branch creation and branch switching are
two distinct responsibilities.
The tool return text compounds the violation by explicitly advertising the side effect:
`"✅ Created and switched to branch: {name}"`.
As a direct consequence, step 3 of `start-issue.prompt.md` (`git_checkout`) is currently
a no-op — the caller is already on the new branch before it is explicitly asked to switch.

## Research Goals

- Confirm the root cause and exact affected code paths
- Identify all callers and tests that rely on the defect behavior
- Determine the corrected behavior and capture the Approved Strategy

## Related Documentation

- [docs/coding_standards/ARCHITECTURE_PRINCIPLES.md](../../coding_standards/ARCHITECTURE_PRINCIPLES.md)
- [docs/coding_standards/DOCUMENTATION_STANDARD.md](../../coding_standards/DOCUMENTATION_STANDARD.md)
- [.github/prompts/start-issue.prompt.md](../../../.github/prompts/start-issue.prompt.md)

---

## Observed vs Expected Behavior

| Dimension | Observed (defect) | Expected (corrected) |
|-----------|-------------------|----------------------|
| Postcondition | branch created **and** active branch switched | branch created; active branch **unchanged** |
| Tool return text | `✅ Created and switched to branch: {name}` | `✅ Created branch: {name}` |
| Adapter log message | `"Created and checked out branch"` | `"Created branch"` |
| `start-issue.prompt.md` step 3 | `git_checkout(branch=...)` is a no-op | `git_checkout(branch=...)` is a meaningful, intentional switch |
| SRP compliance | ❌ one method does create **and** switch | ✅ one method does create only |

---

## Root Cause

The root cause is a single unconditional call to `new_branch.checkout()` inside
`GitAdapter.create_branch()`, immediately after the branch is created via
`self.repo.create_head(branch_name, base_ref)`.

**`mcp_server/adapters/git_adapter.py` (lines ~115–131):**

```python
new_branch = self.repo.create_head(branch_name, base_ref)
new_branch.checkout()          # ← defect: auto-checkout embedded in creation

logger.info(
    "Created and checked out branch",   # ← defect: log echoes the side effect
    extra={"props": {"branch_name": branch_name, "base": resolved_base}},
)
```

The `GitManager.create_branch()` is a passthrough with no checkout logic of its own:
it validates inputs, runs a pre-flight clean-check, then delegates to
`self.adapter.create_branch(full_name, base=base_branch)`.

The tool layer (`CreateBranchTool.execute()` in `mcp_server/tools/git_tools.py`, line 167)
explicitly documents the side effect in its return value:

```python
return ToolResult.text(f"\u2705 Created and switched to branch: {branch_name}")
```

No `IGitAdapter` Protocol exists in the codebase — only `IGitContextReader` covers the
read-only git surface — so no interface definition requires updating.

---

## Affected Surface

### Production

| File | Location | Defect artifact |
|------|----------|-----------------|
| `mcp_server/adapters/git_adapter.py` | `GitAdapter.create_branch()`, line ~119 | `new_branch.checkout()` |
| `mcp_server/adapters/git_adapter.py` | `GitAdapter.create_branch()`, line ~126 | log: `"Created and checked out branch"` |
| `mcp_server/tools/git_tools.py` | `CreateBranchTool.execute()`, line 167 | return text: `"Created and switched to branch: {name}"` |

### Tests asserting defect behavior (must change)

| File | Test name | Defect assertion |
|------|-----------|-----------------|
| `tests/mcp_server/unit/adapters/test_git_adapter.py` | `test_create_branch_with_head` | `mock_new_branch.checkout.assert_called_once()` |
| `tests/mcp_server/unit/adapters/test_git_adapter.py` | `test_create_branch_with_branch_name` | `mock_new_branch.checkout.assert_called_once()` |
| `tests/mcp_server/unit/adapters/test_git_adapter.py` | `test_create_branch_with_commit_hash` | `mock_new_branch.checkout.assert_called_once()` |
| `tests/mcp_server/unit/tools/test_git_tools.py` | `test_create_branch_tool_calls_manager_with_explicit_base` | `"Created and switched to branch: feature/test-branch"` |

### Prompts (no content change needed)

| File | Current status | Post-fix status |
|------|----------------|-----------------|
| `.github/prompts/start-issue.prompt.md` step 3 | `git_checkout` is a no-op (branch already active) | `git_checkout` becomes a meaningful, intentional switch |

The prompt already has the structurally correct sequence (`create_branch` → `git_checkout`).
No content change is required; the fix restores the intended semantics of the existing step.

### Tests NOT affected

Tests in `tests/mcp_server/managers/test_git_manager_config.py` mock the adapter
(`mock_adapter.create_branch.assert_called_once_with(...)`) and do not assert checkout behavior.
Tests in `tests/mcp_server/integration/test_pr_status_lockdown.py` import `CreateBranchTool`
for tool-registry checks only, not for execution behavior.

---

## Architectural Constraints

- **SRP (ARCHITECTURE_PRINCIPLES §1.1):** Branch creation and branch switching are distinct
  responsibilities. Embedding checkout in create violates the rule "a class has exactly one
  reason to change." The test: can `create_branch` be described in one sentence without "and"?
  No — it currently does "create **and** switch."
- **No backward-compat shim warranted:** The auto-checkout is a defect, not a supported
  contract. The `start-issue.prompt.md` already calls `git_checkout` explicitly after
  `create_branch`, which is the intended postcondition.
- **No optional flag allowed:** Introducing a `checkout: bool = False` parameter would
  preserve the defect path and create a permanent code smell. Design must not propose it.

---

## Supported Contract vs Defect Dependence

The `git_checkout(branch=...)` call in `start-issue.prompt.md` step 3 is the **supported
contract** — it was always intended to be a meaningful, intentional operation.
The auto-checkout inside `GitAdapter.create_branch()` is the **defect**: no production
caller outside the tool-chain itself was found to rely on the auto-checkout as an
explicit postcondition.
Later phases must preserve the explicit `git_checkout` call in the start-issue flow
and must not introduce any caller that depends on `create_branch` having switched the
active branch.

---

## Corrected Behavior

- `GitAdapter.create_branch()` creates the local branch without calling `checkout()`.
- Active branch is unchanged after `create_branch` returns.
- Tool return text: `"✅ Created branch: {name}"`.
- Adapter log: `"Created branch"`.
- `start-issue.prompt.md` step 3 (`git_checkout`) is a real, intentional switch.

---

## Regression Risks

- Any code path that calls `create_branch` and then immediately acts on the repository
  as if on the new branch — without an explicit `git_checkout` — would silently operate
  on the wrong branch. No such production path was found in `mcp_server/`.
- Tests that remove `checkout.assert_called_once()` must add a complementary assertion
  confirming that `checkout` is **not** called, to prevent the defect from being
  re-introduced silently.

---

## Assumptions

- `GitManager.create_branch()` contains no checkout logic of its own (confirmed: delegated
  entirely to adapter).
- No other production caller of `GitAdapter.create_branch()` or `GitManager.create_branch()`
  relies on the auto-checkout as a postcondition (confirmed by code inspection).
- `IGitAdapter` Protocol does not exist and is not required for this fix (confirmed).

---

## Open Questions

None. All decision points are resolved by the research evidence and the Approved Strategy below.

---

## Approved Strategy

| Dimension | Decision |
|-----------|----------|
| Affected boundary | `GitAdapter.create_branch()` and `CreateBranchTool.execute()` return contract |
| Selected strategy | **Clean break** — remove auto-checkout from adapter, correct return text, update 4 affected tests |
| Supported contract | Explicit `git_checkout` call in `start-issue.prompt.md` step 3 |
| Defect to remove | `new_branch.checkout()` call and "Created and switched" return text |
| Backward compat shim | None — no production caller depends on auto-checkout as a supported contract |
| Optional `checkout` flag | Forbidden — preserves the defect path |
| Prompt changes | None — `start-issue.prompt.md` is already structurally correct |
| Constraints for design/planning | Design must not reintroduce auto-checkout via flag, default, or shim |

**Human approval captured:** user confirmed "Mee eens ga verder" on 2026-05-25.

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-25 | Agent | Initial draft — root cause, affected surface, approved strategy |
