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


## C_CODE closure

D2_DOC_INPUTS, D2_PY_LAYOUT, D2_TS_LAYOUT and D2_CODE_EVIDENCE are fulfilled for the nine code families. The final inventory is 18 untouched `c2_verified_*` minimal/filled files, with complete contexts/outputs, UTF-8 hashes, preflight rows and identities in first-output-evidence.md. Suite identity at observation: `miQevm1LFgWRuTJ9`; each reachable package fingerprint is recorded there. Earlier `c2_*` and `c2_final_*` examples remain intermediate characterization, not final proof.

| Family | Manual observations across minimal/filled |
| --- | --- |
| Class | Explicit module/class prose, one main class, valid empty pass gap, two-blank module join, one-blank member joins, typed stub retained. |
| Protocol | Distinct prose, native Protocol import/base, intentional ellipsis methods, same valid empty-class gap and supplied method order. |
| Pydantic Config | Required caller frozen choice, multiline ConfigDict/Field calls, fields/examples order and False/0/empty string values retained; ge/min_length constraints attached to actual fields. |
| Pydantic DTO | Frozen default retained, fields carry their descriptions without automatic duplicated Fields summary, default_factory/min_length/gt and example facts retained. |
| Adapter | Empty/filled valid class, explicit logger/constructor presence, constructor-before-method order and body preserved; imports-to-logger gap corrected separately from class joins. |
| Worker | Explicit single operation, optional injected constructor/logger, one main class, no automatic __all__, preserved operation body. |
| Pytest Unit | Retained module description input, marker variable separated correctly from imports, supplied fixture/decorator/case order and bodies retained, valid empty optional arrays. |
| Pytest Integration | Retained module description, meaningful temporary-file case, top-level function spacing; existing native Pytest test proves real generated filesystem/JSON collaboration. |
| TypeScript | Absent module comment stays absent, required class comment, direct class-comment join, empty constructor, readonly/type/implements facts and optional property presence assignments retained. |

All 18 outputs have first-line provenance and exactly one terminal LF. Every public content-preflight row passed: Python 3.13.7 or TypeScript 6.0.3 syntax. Configured Ruff 0.15.6 format/lint passed for all 16 pristine Python pairs and the mixed fixed/caller import reproduction: 17 already formatted and all lint checks passed, receipt `pgmcp://cache/runs/347c4a8c62c34230b4515b363cd09c9d`. This does not promise arbitrary caller expressions/imports/dependencies meet Ruff or type checking.

Additional actual boundary cases prove required module_description rejection and removed root description rejection before persistence; explicitly empty Python module prose remains a documentation literal; identical supplied module/class prose is not deduplicated. TypeScript explicit empty and whitespace-only module descriptions both preserve the defined empty comment, while minimal absence does not produce it. A Worker body preserves two internal CRLFs, internal blank line and Unicode U+2028 inside a quoted value; Pydantic defaults retain significant whitespace, CRLF, Unicode, False, 0 and None without generic trimming. Safe Python escaping represents control characters in literals. The preservation-only Worker case intentionally has a caller-authored unused local; it is syntax/preservation evidence, not a clean lint example.

Native review found real generated gaps before pass and imports-to-variables, then a same-group import ordering error. Those originals are preserved. Two separately scaffolded fix probes received ordered lint then format operations: one lint correction, one formatted file; inspected changes are precisely the spacing findings. An explicit recheck confirms those probes pass (format row: three already formatted in the combined probe/import run; its sole lint finding belongs to the unrepaired mixed-import reproduction, subsequently corrected in templates). Pristine evidence was not fixed.

The initial meaningful contract RED is 32 failed / 2 passed, bounded native receipt `pgmcp://cache/runs/c3f79f7a494a4ee39f4418fc712f1e3e`; commit `deb5a2ccfaa3481f631c1bd2475e120d9ebd032a`. New required explicit descriptions were rejected by old schemas. Intermediate native tests caught lost Pydantic constraint arguments; namespace accumulation corrected that defect. Final ten-file subset reports 52 passed / 1 failed / 1 existing warning / 33.72s (`pgmcp://cache/runs/197fb04a662940c8bd50ba2c6ccd3f8b`); the sole failure was the existing expected obsolete from-before-import ordering. After adapting that expectation, the affected existing integration file reports 5 passed / 1 existing warning / 4.27s (`pgmcp://cache/runs/dc4b351972b4429ca5824d8341e6955d`). Reuse the fresh other 52 rows plus this exact closure; no broad suite was run.

Changed eight family/shared test files passed format/lint/Pyright, with refreshed gates for the subsequently changed shared Python fixture (`pgmcp://cache/runs/c3749daff9824bd6a716676f6a870020`) and integration expectation (`pgmcp://cache/runs/54de446a941043779391899059e8b62a`). No new content tests/assertions or permanent harness were added. Existing typing/native/semantic coverage remains valuable. Scope/Approved Strategy are unchanged.

Remaining work: C_DOCS and C_RECONCILE, independent Implementation review, then separately owned full Validation.
