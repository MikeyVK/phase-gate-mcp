<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=QEtFztWtFehT8R5U sf=9PfER5JkyAoFQLRi -->

# Issue 473 — Manual Inspection

**Status:** Implementation in progress
**Version:** 0.1
**Last Updated:** 2026-10-03

Authority: [Design](design.md), [Planning](planning.md) and [Research approved strategy](research.md#approved-strategy). No additional automated content tests were added. Actual outputs and exact requests are preserved in [first-output evidence](first-output-evidence.md).

## C_SHARED inspection

Ten actual untouched scaffolds: Python class, populated Pydantic DTO, populated adapter, full Markdown document, Issue, PR, Commit, TypeScript and two padding/interior cases. All selected preflight rows passed: Python 3.13.7 syntax, TypeScript 6.0.3 syntax, Markdown document/body and commitlint 21.2.2. Native warning evidence remains visible, not treated as a clean-link proof.

Every file has provenance on its first line and exactly one terminal LF. The shared code boundary places one blank line between documentation/imports and two before top-level code. Shared document/tracking fragments have explicit single-blank joins; concrete body-internal gaps remain C_DOCS work.

The Python padding case retains an explicitly empty module-docstring, strips only blank class/method edges, preserves CRLF and indentation inside class documentation and retains a string default with leading/trailing whitespace and mixed internal endings. The Markdown padding case retains the two spaces creating a hard break, internal CRLF, indented text and fenced-code interiors. Its explicit empty supplied content remains present in the old concrete carrier; its mechanical wrapper is C_DOCS work.

Remaining concrete findings in these intermediate outputs are expected cycle dependencies: adapter constructor/method gap, model composed-call length, TypeScript assignment/brace-edge gaps and document/tracking body gaps. They are not final corrected examples.

## Existing-test evidence and freshness

Before edits: C_SHARED planned seven-path subset, 183 passed / 19 warnings / 128.04s; receipt `pgmcp://cache/runs/eab74e0e702f42ceb4b798143b2a437f`. Configured pytest arguments were retained. Existing warning families: Pydantic SchemaAttachment.schema shadowing and PurePath.is_reserved deprecation.

After shared edits: same subset, 182 passed / 1 failed / 19 warnings / 66.42s; receipt `pgmcp://cache/runs/be2b312c3035498d8be5688f7815b34b`. Installed CLI failed admission with “No filter named 'text_block'”. Real CLI composition now uses the same registration. Its narrow retest passed that installed-handshake case, but newly included renewal coverage exposed the same omission in the existing shared admission fixture (22 passed / 1 failed / 9 warnings / 107.95s; `pgmcp://cache/runs/56abe3577903429f87b01a7cd32b75ac`). That fixture now also registers the real filters. Follow-up evidence is pending.

Generic engine preservation tests still cover raw rendering and explicit False/0 values without artifact EOF rewriting. Tests characterize production behavior through public seams; no helper-only test was introduced.

## Open work

Finish C_SHARED gates, then C_CODE, C_DOCS and C_RECONCILE. Independent Implementation review and Validation remain outstanding.

## C_SHARED closure

The admission-helper consumers' narrow existing subset (renewal CLI, template activation, template proposal) now reports **27 passed, 9 existing warnings, 18.76s**; receipt `pgmcp://cache/runs/c5e6893461874529b30410e1c2bae1c4`. Exact request:

```json
{
  "scope": "targets",
  "targets": [
    "tests/mcp_server/integration/test_renewal_cli.py",
    "tests/mcp_server/integration/test_template_activation.py",
    "tests/mcp_server/integration/test_template_proposal.py"
  ],
  "tests": [
    "python_tests"
  ]
}
```

Reuse the 182 passing rows from the full C_SHARED subset together with the successful installed-handshake row in the 22-passing-row retest; the helper-only failing recovery is now closed by this 27-pass run. No broad/full-suite rerun was introduced. Final changes after these native behavior checks are Python-only formatting with no template/content semantics change.

Production format/lint/Mypy/Pyright evidence: lint/types/Pyright passed for all three changed production files (`pgmcp://cache/runs/f52bf613062e46da9b7dd731825b99a2`), with only function-spacing format failure. The actual Ruff fix reports one file reformatted (`pgmcp://cache/runs/8b561fce0fdd4ffb845809bb15459256`); explicit recheck passed (`pgmcp://cache/runs/5d1937705c8c42cba5918db3bbb463a3`). Earlier production format passed for bootstrap/CLI, still fresh.

Changed delivered/installed/shared-Python fixtures passed format/lint/Pyright (`pgmcp://cache/runs/e3281d24983446458d1ca56af61ecbc8`); changed shared admission support separately passed those three checks (`pgmcp://cache/runs/de4695039315468e8cb550db278a7e56`). Evidence document links passed markdown_link_review: 5 successes, 0 errors (`pgmcp://cache/runs/28367da6b3d64ce3bb7ae25840c7ab43`). Complete DTOs were read; the rows above preserve their relevant facts and exact target sets are stored in each DTO and planning.

Two more actual TypeScript inputs demonstrate absent versus explicit empty module context: both syntax rows passed, both one terminal LF; absent currently uses the old concrete fallback, explicit empty produces an empty module comment. This is characterized without approving fallback: C_CODE owns its removal. Thus 12 shared-stage outputs are preserved, separate from the final 38 pairs.

D1_ENV, D1_LAYOUT and D1_EVIDENCE are fulfilled for their shared-boundary scope. Remaining concrete imperfections are explicitly allocated to C_CODE/C_DOCS and do not alter Approved Strategy. Independent Implementation verdict remains unrequested until all cycles complete.
