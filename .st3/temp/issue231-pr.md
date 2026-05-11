<!-- c:\temp\st3\.st3\temp\issue231-pr.md -->
<!-- template=pr version=93bb9b4e created=2026-04-28T13:48Z updated= -->
# Close out issue #231; sequence runtime-contract follow-ups

Finalizes the issue #231 documentation close-out and records the required follow-up ordering: first close the runtime contract boundary, then make state.json authoritative.
## Changes
- Finalized the issue #231 research close-out in documentation phase
- Reclassified issue #231 as a documentation boundary clarification, not an implementation completion
- Recorded the required follow-up sequence: reuse issue #271 for runtime contract closure, then use issue #298 for state.json authority after contract closure
- Updated the GitHub issue body for #231 with the close-out note and follow-up chain

## Testing
No code tests were run. Verification for this change set consisted of issue-overlap analysis, MCP workflow phase transition to documentation, issue update through GitHub tools, and document readback validation.
## Checklist

- [ ] Issue #231 body updated with follow-up sequencing
- [ ] Research document finalized in docs/development/issue231
- [ ] Follow-up issue #298 created
- [ ] Branch transitioned to documentation phase
- [ ] Ready-phase transition completed before submit_pr

## Related Documentation
- **[docs/development/issue231/research-state-json-absolute-ssot-impact.md][related-1]**

---

Closes: #231