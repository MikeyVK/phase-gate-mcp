<!-- pgmcp:v1 id=design pv=1.0.0 pf=Uk1D2XWpiag1c6nn sf=WI5iXHBKVOU91bYE -->

# Issue \#524 — Cache/text availability notice correction

**Status:** Design completed; independent review requested  
**Version:** 1.0  
**Last Updated:** 2026-10-19

## Purpose

Use existing presentation ownership to correct availability statements without changing transport or cache contracts.

## Problem Statement

Both the configured no-cache truncation notice and ordinary failure warning overstate what failed cache publication proves. The optional-key presenter fallback repeats the full-inline claim.

## Functional Requirements

- Cache failure remains visible with and without text truncation; a failed publication supplies no usable cache URI.
- Notices state text/cached-access facts without asserting loss of complete operation data or client/model access.
- Existing actual operation DTO, outcomes, structured diagnostics and no-operation error behavior remain intact.

## Nonfunctional Requirements

- No new public fields, schemas, service, configuration path, tool-specific branch or presentation capability.
- Preserve existing byte ceiling, inline fallback and traceback policy; no legacy/compatibility layer.
- Use existing behavior tests and injected markers rather than exact-prose snapshots or tests rejecting historic wording.

## Options

### 1. Correct existing notice values and existing generic literal fallback

Keep the current config keys and generic optional-key fallback path; correct their factual content only.

**Pros:**

- Removes all inventoried false claims without new control flow or config admission changes.
- No consumer migration or new source of wording ownership.

**Cons:**

- Existing generic fallback remains in the presenter; review its factual scope alongside shipped config.

### 2. Require a new formatting field or make the generic instruction key mandatory

Move the failure warning into newly mandatory schema configuration.

**Pros:**

- Would make every warning value externally required.

**Cons:**

- Changes config admission and fixtures/consumers to solve a wording bug; disproportional and outside correction strategy.

### 3. Add structured-channel awareness to the limiter or presenter

Feed transport/client capabilities into presentation.

**Cons:**

- Violates existing separation and can create an unproved client-access promise; rejected.

## Decision

Correct the two shipped notice strings and the one existing generic presenter fallback literal. No functions, signatures, schemas, branches or channel selection change.

## Rationale

The fault is the claim, not publication, projection or operation serialization. Architecture §15 permits generic text at the existing presentation boundary; this adds no new wording owner or fallback mechanism. Keeping the optional key behavior avoids turning this defect into a configuration-contract migration. Policy/recovery explanations and operation facts remain in their existing owners.

## Production Design

Only notice-value corrections in shipped presentation.yaml and the existing TextPresenter generic fallback literal. TextBudgetLimiter, ResponsePresenter, server serialization, cache publication, operation/attachment ownership and public schemas remain untouched. Existing fallback JSON may omit traceback in text; structured operation keeps all fields. Documentation clarifies this distinction without changing the traceback policy.

## Test Design

Adapt the existing shipped-cache guidance test in [execution presentation integration](../../../tests/mcp_server/integration/test_execution_presentation_v3.py), reusing its frozen DTO/core/config/client fixture and real success cache. Failed publication uses a controlled existing publisher interface, not a new production abstraction.

| Case | Evidence |
|---|---|
| Successful cache, small and large DTO | Real cache URI/readback and paging guidance preserved; structured operation exact. |
| Failed cache, small DTO | Configured ordinary failure notice selected, bounded text, no cache URI, structured operation exact. |
| Failed cache, large DTO | Configured no-cache truncation tail reserved within byte limit, no fabricated URI, complete structured operation. |
| Failed cache with error operation | isError reflects original outcome and structured diagnostic fields remain intact. |
| No structured operation | Reuse existing processing-failure and unknown-tool transport cases; no new promise or cache URI. |

Adapt existing presenter unit assertions to injected configured marker values and fallback JSON semantics, rather than old wording. Exercise omitted optional warning key without a wording snapshot. Retain limiter marker/byte tests and no-operation controls; no new test module or framework. Review the three authored notice values directly for semantic truth. Automated behavior tests deliberately do not classify natural-language meaning.

## Contracts

### Notice values and selection

| Existing source | Corrected value | Known selection facts |
|---|---|---|
| global.next_instruction_texts.cache_publication_failed | *(Cache publication failed; cached access is unavailable.)* | TextPresenter has a failed CachePublication. |
| Existing generic fallback for the absent instruction key | Same neutral cache-failure value | Existing optional-key behavior only; not a new fallback route. |
| global.formatting.cache_unavailable_truncation_notice | Text output truncated; no cached result is available. | TextBudgetLimiter has overflow and no usable cache reference. |

The limiter knows absence of a reference, not why publication was absent; its notice therefore does not invent a failure cause. A real cache failure remains visible as unavailable cached access in that mandatory tail. Ordinary failure text explicitly identifies failed publication. Neither notice claims operation data loss, inline completeness or client/model access.

### Unchanged interfaces

FormattingConfig.cache_unavailable_truncation_notice: str; GlobalPresentationConfig.next_instruction_texts: dict[str, str]; TextPresenter.present_text(..., cache_pub: CachePublication | None, ...) -> str; TextBudgetLimiter.limit(body: str, cache_reference: str | None) -> str. MCPServer continues to serialize the actual operation in JSON mode with aliases. No interface or model shape changes.

## Preservation

No schema exposure, DTO migration, response-channel removal, cache redesign, conditional-reference proposal, client-specific routing, dependency upgrade, new exception handling or suppression. The server cannot promise what clients forward to a model. #523 follow-up decisions remain separate.

## Validation

### Behavior and preservation

**Method:** Focused existing integration/presenter/limiter/transport cases plus changed-file checks; one required native configured suite and relevant branch/configured gates in Validation.

**Expected Result:** Real publication controls, failed publication under both text sizes, exact structured DTO/outcome and no-operation controls pass; native configurations and evidence retained.

## Planning Consequences

One compact non-redesign cycle. Treat literal/config corrections and test maintenance as mechanical: no artificial failing prose test or RED commit. New transport scenarios prove missing preservation evidence rather than a new algorithm; full suite and broad gates belong only to Validation. Stop for owner if new delivery/config admission policy becomes necessary.

## Related Documents

- [Approved Research](<research.md>)
- [Architecture principles](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-19 | @imp designer | Specify existing notice-value correction, neutral fallback and proportional transport evidence. |
