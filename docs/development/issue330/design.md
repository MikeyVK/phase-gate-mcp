<!-- docs\development\issue330\design.md -->
<!-- template=design version=5827e841 created=2026-05-20T09:29Z updated= -->
# GitHubAdapter.list_prs head filter - owner:branch transformation

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-05-20

---

## 1. Context & Requirements

### 1.1. Problem Statement

GitHubAdapter.list_prs() passes bare head branch names to GitHub API get_pulls(), but GitHub requires owner:branch format for exact head matching. Without the prefix, unrelated open PRs are returned.

### 1.2. Requirements

**Functional:**
- [ ] list_prs(head='branch-name') must pass 'owner:branch-name' to GitHub API get_pulls()
- [ ] list_prs(head=None) behavior must remain unchanged
- [ ] Owner must be derived from the adapter's own _repo_name attribute

**Non-Functional:**
- [ ] Minimal change: one-line transform inside list_prs()
- [ ] No new dependencies or imports required
- [ ] Test update limited to test_list_prs_filter_head in test_github_adapter.py

### 1.3. Constraints

['GitHubAdapter is the API boundary; protocol-level details must not leak to the manager layer', 'No interface or method signature changes', 'owner is always available from self._repo_name (set in __init__)']
---

## 2. Design Options
---

## 3. Chosen Design

**Decision:** Fix in GitHubAdapter.list_prs(): when head is not None, extract owner from self._repo_name and pass head as owner:branch to get_pulls().

**Rationale:** The adapter is the correct boundary between domain (bare branch names) and GitHub API protocol (owner:branch format). Fixing in the adapter ensures all current and future callers get correct behavior without leaking API knowledge upward.

### 3.1. Key Design Decisions

| Decision | Rationale |
|----------|-----------|

## Related Documentation
- **[docs/development/issue330/research.md][related-1]**
- **[mcp_server/adapters/github_adapter.py][related-2]**
- **[mcp_server/managers/github_manager.py][related-3]**

<!-- Link definitions -->

[related-1]: docs/development/issue330/research.md
[related-2]: mcp_server/adapters/github_adapter.py
[related-3]: mcp_server/managers/github_manager.py

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 |  | Agent | Initial draft |