<!-- docs\development\issue330\planning.md -->
<!-- template=planning version=130ac5ea created=2026-05-20T09:30Z updated= -->
# GitHubAdapter.list_prs head filter - planning

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-05-20

---

## Scope

**In Scope:**
GitHubAdapter.list_prs() head parameter transform and test_list_prs_filter_head assertion update.

**Out of Scope:**
Other GitHub API methods, PRStatusCache, enforcement logic.

---

## Summary

Single-cycle fix: add owner:branch transform in GitHubAdapter.list_prs() when head is provided. One production file, one test file, one assertion update.

---

## TDD Cycles


### Cycle 1: C1 - owner:branch transform in list_prs

**Goal:** Add owner:branch prefix to the head parameter in GitHubAdapter.list_prs() so GitHub API returns only exact-match PRs.

**Tests:**
- tests/mcp_server/unit/adapters/test_github_adapter.py::test_list_prs_filter_head

**Success Criteria:**
- test_list_prs_filter_head passes asserting get_pulls called with head=test-owner:feature
- Full test suite green


## Related Documentation
- **[docs/development/issue330/research.md][related-1]**
- **[docs/development/issue330/design.md][related-2]**

<!-- Link definitions -->

[related-1]: docs/development/issue330/research.md
[related-2]: docs/development/issue330/design.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 |  | Agent | Initial draft |