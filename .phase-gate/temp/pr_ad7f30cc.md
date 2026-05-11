<!-- .st3\temp\pr_render.md -->
<!-- template=pr version=93bb9b4e created=2026-05-06T12:42Z updated= -->
# fix(#295): submit_pr atomicity — upstream preflight, dirty-tree guard, rollback on API failure

Hardent submit_pr met drie atomiciteitsgaranties: upstream-check en dirty-tree guard blokkeren vóór elke mutatie; bij GitHub API-fout na push wordt de neutralization-commit automatisch teruggedraaid (hard_reset + force-push). De branch is na elke faalfase clean en direct retryable.
## Changes
- `GitAdapter.hard_reset(ref)` + `force_push_with_lease()` toegevoegd (C1)
- `GitManager.prepare_submission(artifact_paths, base, note_context) -> bool`: upstream-preflight, dirty-tree preflight, conditionele neutralize+commit, altijd push — interne rollback bij fout (C2/C3)
- `GitManager.rollback_push(note_context)`: hard_reset HEAD~1 + force-push (C4)
- `SubmitPRTool.execute()` herschreven naar 3 high-level calls — Law of Demeter afgedwongen, geen directe git-internals (C5)

## Testing
26 nieuwe tests over 4 bestanden (5 adapter + 11 manager + 8 integration + 2 LoD-structureel). Volledige suite: 2580 passed, 6/6 quality gates groen. Smoke test op live branch: alle 4 faalopaden geverifieerd.
## Checklist

- [ ] Code follows project standards
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Quality gates passing
## Related Documentation
- **[docs/development/issue295/design.md][related-1]**
- **[docs/development/issue295/planning.md][related-2]**
- **[docs/development/issue295/SESSIE_OVERDRACHT_295.md][related-3]**
- **[docs/reference/mcp/tools/github.md][related-4]**

---

Closes: #295, #304