<!-- pgmcp:v1 id=pr pv=1.0.0 pf=hG0a9tLUxIzayxH4 sf=FAN5Vr-4vcbMMjZ2 -->

## Summary

Correct the first output of all nineteen shipped concrete template packages. Generated layout, explicit prose inputs and required full-document metadata/history now follow the approved clean-break strategy; caller-authored interiors and values remain preserved. Closes the concrete first-call quality scope of #473; epic #72 is administrative only, and integration is into main.

## Changes

- Centralize generated spacing and full-document header/history in the tiered shared Jinja templates. Use one pure text_block filter in the existing engine for boundary-only blank-line normalization, registered by real bootstrap, CLI and existing renderer consumers.
- Correct Python import/layout/composed expressions, TypeScript presentation, and document/tracking structure. Require explicit module/class prose and caller-authored document_metadata with ordered revisions; preserve absent versus explicitly empty input and meaningful literal/interior whitespace.
- Migrate affected existing tests and concrete consumers, including the missed header-reader renderer. Add no new automated content/regression suite or permanent context harness.
- Reconcile coding/documentation standards, live scaffold references, distributed and active create-issue instructions, and Unreleased notes. Persist the long-run client-budget rationale and concise cache/hash guidance in tracked instructions/setup.
- Preserve exact requests and pristine outputs for nineteen families, manual boundary findings and independent review provenance in issue473 artifacts. The large branch diff is predominantly the intentionally retained research/output archive; temporary working scaffolds under .pgmcp/temp are not part of the tracked deliverable.

## Testing

- Independent configured full suite, no target/argument partition: 2775 passed, 1 skipped, 1 XPASS, 229 warnings; 2777 items, eight workers, native exit 0 (316.20 s, timeout_seconds=1200). Producer also obtained the same totals.
- All 25 changed Python files covered by fresh format/lint/Pyright evidence; strict Mypy on the three changed production files. Missed header-reader consumer module: 68 passed, with existing frame/provenance/length/round-trip coverage retained.
- Actual manual inspection of 38 pristine minimal/filled outputs across nineteen families, six final document boundaries and separate code boundaries. All sixteen clean Python examples pass Ruff format/lint. Twenty-six document/boundary replays reproduce the reviewed output. Arbitrary caller code, semantics and dependencies remain caller responsibilities.
- Accepted issue-specific Markdown route: QA checked the 24-file Validation selection (563 successful links, 48 exclusions, zero errors/time-outs). Four AGENTS source/runtime copies retain the recorded 41 directory-relative failures; their nine root-relative targets exist and source/runtime parity is verified. This is an explicit deployment-context exception, not a blanket passing branch gate.
- Documentation QA: all eleven changed documents/instructions, 80 successful links, 16 existing HTTPS/pgmcp exclusions, zero errors/time-outs; four source/runtime pairs equal. Final verdict-index refinement separately passed its focused link check.
- Independent Implementation repair GO on b3e3719f, Validation GO on 2756f8dd and Documentation GO on 620fdd53; final Documentation closure indexed at 3215946d. Ready changes only this PR narrative and workflow state, so existing behavioral evidence is reused.

## Checklist

- [x] Completed phase artifacts and independent QA closures are linked; fresh required evidence is reused.
- [x] Deferred work retains reproduction/impact/uncertainty and coordination ownership.
- [x] No branch-selection adapter repair, generic #476 enforcement, new content-test harness or package deployment is claimed.

## Breaking Changes

Approved clean break: removed root description/status aliases are rejected instead of bridged. Use scaffold_schema for the selected package: applicable Python families separate module_description and class_description; full-document families require document_metadata with status and a nonempty ordered revisions list. Issue/PR/Commit retain their separate body/message contracts. Scaffolds are valid starting points, not complete caller-specific products. Main receives tracked setup/instruction guidance, but ignored .codex/config.toml client windows still require explicit host rollout/activation as documented; this PR does not deploy a package.

## Deferred Work

### F6: invalid-template bootstrap/proxy diagnostics and recovery.

Confirmed invalid Jinja admission led to process exit, lost startup diagnostics and false ready state. The template correction restores admission but does not repair lifecycle behavior. Highest-priority separately scoped coordination repair; preserve rejection and provide actionable diagnostics/recovery.

**References:**

- [F6 reproduction, impact and triage](<https://github.com/MikeyVK/phase-gate-mcp/blob/bug/473-first-call-template-quality/docs/development/issue473/tool-practice-findings.md>)

### Branch-wide check applicability and native-config selection.

Owner deferred adapter/wire/resolver production changes to a separate issue. Mixed branch targets cause irrelevant native checks or oversized results. Preserve selection_intent proposal, native config reuse, meaningful files/folders and unresolved feasibility/migration decisions; review the nine-package audit and four packages requiring behavior changes.

**References:**

- [Deferred branch-wide check solution](<https://github.com/MikeyVK/phase-gate-mcp/blob/bug/473-first-call-template-quality/docs/development/issue473/tool-practice-findings.md#deferred-branch-wide-check-solution--owner-disposition-2026-10-04>)

### Generic schema/template consumption remains issue \#476.

Concrete nineteen-family output correction does not establish generic consumption of every admitted field. Keep existing #476 separate; no automatic scope absorption.

**References:**

- [Issue #476](<https://github.com/MikeyVK/phase-gate-mcp/issues/476>)
- [Approved strategy and scope decisions](<https://github.com/MikeyVK/phase-gate-mcp/blob/bug/473-first-call-template-quality/docs/development/issue473/research.md>)

### F1: Markdown angle-destination parsing.

A bounded valid-link false positive is documented. Investigate native parsing separately rather than rewrite legitimate destinations or weaken the concrete-output contract.

**References:**

- [F1 reproduction](<https://github.com/MikeyVK/phase-gate-mcp/blob/bug/473-first-call-template-quality/docs/development/issue473/tool-practice-findings.md>)

### F2/V-F10 cache-window usability and excessive producer reads.

Current AGENTS provides bounded selective-read/hash instructions. Further diagnostic/export usability needs coordination triage; historical producer inefficiency is not a reason for routine full downloads.

**References:**

- [Cache practice and producer finding](<https://github.com/MikeyVK/phase-gate-mcp/blob/bug/473-first-call-template-quality/docs/development/issue473/tool-practice-findings.md>)

### F3: verbose native negative-result response bounds.

Existing RED output hit operational response limits. Triage negative-result usability separately; unavailable/incomplete evidence must not be represented as RED or pass.

**References:**

- [F3 reproduction](<https://github.com/MikeyVK/phase-gate-mcp/blob/bug/473-first-call-template-quality/docs/development/issue473/tool-practice-findings.md>)

### F4/F7 restart sequencing and per-client catalog refresh.

Separate expected client lifecycle constraints from confirmed defects before scheduling repairs. No universal automatic refresh/restart behavior is claimed.

**References:**

- [Restart/client reproduction](<https://github.com/MikeyVK/phase-gate-mcp/blob/bug/473-first-call-template-quality/docs/development/issue473/tool-practice-findings.md>)

### F5: schema-source authoring friction.

Direct schema-authoring support is absent. Triage separately; this correction adds no new schema pipeline or public artifact type.

**References:**

- [F5 evidence](<https://github.com/MikeyVK/phase-gate-mcp/blob/bug/473-first-call-template-quality/docs/development/issue473/tool-practice-findings.md>)

### Cross-session receipt accessibility.

Producer passing receipts were inaccessible to the independent QA session, requiring necessary independent reruns. Storage/expiry/transport root cause is not established. Investigate durable hand-off/access separately.

**References:**

- [Observed receipt-access case](<https://github.com/MikeyVK/phase-gate-mcp/blob/bug/473-first-call-template-quality/docs/development/issue473/tool-practice-findings.md#documentation-closure-and-coordination-triage--2026-10-04>)

### Four AGENTS source/deployment-relative link locations.

Original 41 native directory-relative failures remain disclosed under the independently accepted issue-specific gate route. Preserve active deployment conventions; coordination may triage a future solution without blanket exclusions.

**References:**

- [Accepted Validation boundary](<https://github.com/MikeyVK/phase-gate-mcp/blob/bug/473-first-call-template-quality/docs/development/issue473/validation.md>)

## Closes

Closes #473

## Related Documents

- [research.md][related-1]
- [design.md][related-2]
- [planning.md][related-3]
- [implementation.md][related-4]
- [validation.md][related-5]
- [documentation.md][related-6]
- [manual-inspection.md][related-7]
- [first-output-evidence.md][related-8]
- [tool-practice-findings.md][related-9]

[related-1]: <https://github.com/MikeyVK/phase-gate-mcp/blob/bug/473-first-call-template-quality/docs/development/issue473/research.md>
[related-2]: <https://github.com/MikeyVK/phase-gate-mcp/blob/bug/473-first-call-template-quality/docs/development/issue473/design.md>
[related-3]: <https://github.com/MikeyVK/phase-gate-mcp/blob/bug/473-first-call-template-quality/docs/development/issue473/planning.md>
[related-4]: <https://github.com/MikeyVK/phase-gate-mcp/blob/bug/473-first-call-template-quality/docs/development/issue473/implementation.md>
[related-5]: <https://github.com/MikeyVK/phase-gate-mcp/blob/bug/473-first-call-template-quality/docs/development/issue473/validation.md>
[related-6]: <https://github.com/MikeyVK/phase-gate-mcp/blob/bug/473-first-call-template-quality/docs/development/issue473/documentation.md>
[related-7]: <https://github.com/MikeyVK/phase-gate-mcp/blob/bug/473-first-call-template-quality/docs/development/issue473/manual-inspection.md>
[related-8]: <https://github.com/MikeyVK/phase-gate-mcp/blob/bug/473-first-call-template-quality/docs/development/issue473/first-output-evidence.md>
[related-9]: <https://github.com/MikeyVK/phase-gate-mcp/blob/bug/473-first-call-template-quality/docs/development/issue473/tool-practice-findings.md>
