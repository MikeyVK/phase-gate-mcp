<!-- docs\development\issue429\safe_edit_tool_finding.md -->
<!-- template=generic_doc version=43c84181 created=2026-07-18T17:07Z updated= -->
# Safe Edit Tool UX Finding (Deferred Work)

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-07-18

---

When faced with this rejection during Issue #429, the agent erroneously fell back to using `line_edits` with a `start_line` and `end_line`, which explicitly *replaced* the end of the file rather than appending to it. This led to unintentional data loss (document corruption).

Furthermore, even if an `append: true` mode existed, simply appending to the absolute end of a document is often structurally incorrect. For example, appending content *after* a `## Related Documentation` or `## Version History` table instead of inserting it before these footers. This highlights a secondary risk: agents lack structural awareness when blindly appending.

Furthermore, even if an `append: true` mode existed, simply appending to the absolute end of a document is often structurally incorrect (e.g., appending content *after* a `## Version History` table instead of inserting it before the footer). This highlights a secondary risk: agents lack structural awareness when blindly appending.

Document a UX/design flaw in the safe_edit_file tool and propose an append-mode for deferred work.

---

## Summary

The safe_edit_file tool requires exact file line counts to append, leading to fragile agent edits. We propose adding an explicit append mode or relative index support.





---

## 

## 

## Related Documentation
None
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-18 | Agent | Initial draft |