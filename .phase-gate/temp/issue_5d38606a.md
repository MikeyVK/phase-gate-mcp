<!-- .st3\temp\issue_render.md -->
<!-- template=issue version=8dd42510 created=2026-04-24T12:58Z updated= -->
# [Tooling Debt] Missing Git operations in ST3 workflow tools

## Problem
Diverse Git-operaties ontbraken in de ST3 workflow tools, waardoor de agent buiten de MCP-toolset om git moest uitvoeren. Dit verstoort de enforceability van de workflow.

## Expected Behavior

Volledige dekking van essentiële Git-operaties als MCP tools: fetch, pull, push, status, stash, diff, branch management.
## Actual Behavior

Grotendeels gerealiseerd via meerdere issues: #56 (git_add_or_commit, git_fetch, git_pull, git_push, git_status, git_stash), #229 (git_diff_stat, git_list_branches, git_merge), #283 (BranchMutatingTool ABC, submit_pr). Resterende gaps worden bijgehouden in specifieke open issues: #46 (pre-push/post-pull validation), #116 (create_branch accepteert issue_number parameter). Dit overkoepelende tooling-debt issue is inhoudelijk afgerond.
## Context

Geen parent issue. Aangemaakt vroeg in het project als overkoepelende inventaris van ontbrekende Git-operaties.
## Related Documentation
- **[mcp_server/tools/git_tools.py][related-1]**
- **[mcp_server/tools/pr_tools.py][related-2]**
