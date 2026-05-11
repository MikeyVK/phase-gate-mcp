<!-- .st3\temp\issue_render.md -->
<!-- template=issue version=8dd42510 created=2026-04-15T05:35Z updated= -->
# Remove state.json/deliverables.json from git tracking; ready-phase enforcement

## Problem
state.json and deliverables.json kept contaminating main despite the merge=ours .gitattributes strategy. Root cause analysis revealed three compounding issues: (1) .gitattributes was introduced on a feature branch instead of main first — so the merge that introduced it was unprotected (chicken-and-egg). (2) merge=ours only protects against overwrites of existing files, not fresh additions (deleted-on-main, added-on-branch). (3) GitHub server-side merges do not reliably respect .gitattributes merge drivers. Additionally, ad-hoc debug scripts (check_yaml.py, fix_yaml.py, etc.) were committed to the feature branch and landed on main. A deeper structural problem existed: there was no automated guard preventing branch-local runtime artifacts from entering commits or PRs in the first place.

## Expected Behavior

state.json and deliverables.json are listed in .gitignore so they can never be committed. Main is clean. Debug scripts are removed and a pattern-based .gitignore entry prevents ad-hoc *.py scripts in the root from being committed. Additionally, create_pr is blocked unless the workflow phase is ready, preventing premature PRs. git_add_or_commit in the ready phase automatically unstages branch-local artifacts before committing, making contamination structurally impossible.
## Context

The merge=ours approach in .gitattributes was removed (misleading, unreliable with GitHub server-side merges). The .gitignore approach is the correct mechanism — state.json is a local MCP runtime artifact; it does not need git tracking. The MCP server manages state via automatic cleanup on git_checkout. A new enforcement system was added: enforcement.yaml defines pre/post hooks for tools; phase_contracts.yaml defines per-phase constraints. The workphases.yaml was extended with a ready phase as the final pre-PR gate. The EnforcementRunner now executes these hooks as part of normal tool invocation. The implementation required a non-trivial refactor of git_tools, pr_tools, and the enforcement_runner to wire up the pre-hook dispatch.
## Related Documentation
- **[docs/reference/mcp/tools/git.md][related-1]**
- **[docs/reference/mcp/tools/github.md][related-2]**
- **[.st3/config/enforcement.yaml][related-3]**
- **[.st3/config/phase_contracts.yaml][related-4]**
- **[docs/development/issue283/design-ready-phase-enforcement.md][related-5]**
