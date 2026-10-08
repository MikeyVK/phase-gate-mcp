<!-- pgmcp:v1 id=research pv=1.0.0 pf=lgBwxWMfTAmNNg_O sf=5--KpGf2wHUv2qAj -->

# Issue 121 — Minimal structure-preserving artifact edit review

**Status:** Draft — tool-enforced strategy pending  
**Version:** 0.9  
**Last Updated:** 2026-10-08

## Purpose

Present the least heavy architecturally clean response to the structure-preservation finding consolidated from issue483.

## Scope In

Current edit/profile/provenance boundaries, all template-generated artifact formats, original Jinja source association, existing checker feasibility, package-owned preservation requirements, options and strategy decisions.

## Scope Out

Implementing safeguards before approval, new editing APIs, designing a universal Jinja/AST output-contract framework, generic undo, universal rewrite restrictions, text/newline policy changes, implementation sequencing and a new architecture.

## Problem Statement

A native-passed edit and retained template provenance do not establish that required artifact structure and information remain usable. The owner wants the lightest architecturally clean option, not a new editing architecture.

## Goals

- Separate demonstrated structural damage from valid refinement.
- Identify authoritative requirements without freezing generated text or moving package knowledge into generic server code.
- Recommend a minimal solution and make its review-versus-runtime guarantee explicit before strategy approval.

## Background

Issue121 now consolidates the deferred finding from #483. The historical revision-table repair removed two blank lines between the 0.3/0.4/0.5 rows; it is a bounded example, not a measured incident rate. The active issue permits an instruction-based conclusion, but the owner has now rejected that as sufficient and requires protection through pgmcp tooling. Historical introspection/API sketches remain unapproved design assumptions.

## Findings

### Existing tooling boundary

| Surface | Current facts | Reuse or limitation |
| --- | --- | --- |
| EditOperation / ScaffoldOperation | Construct proposed content, run a configured profile before persistence, interpret factual results, and block negative required results under enforce. | Existing no-write behavior can enforce an additional contentcheck. No new editing engine or operation mode is required for this route. |
| CheckService / adapter wire | A profile can contain multiple checks. Each receives proposed content or its owned scratch file, target_path, configured args and execution context. | A final-content contract check fits. The original snapshot is not part of this wire contract: before/after comparisons are not a free existing capability. |
| Profile selection | Explicit package ID overrides original recognized metadata, then extension fallback. Package policy chooses output_profile. | Associate the selected package with the configured structural obligation; do not let rewritten provenance choose a weaker contract. .md alone does not identify a template contract. |
| EnforcementDecorator | Pre/post actions receive tool parameters; they do not share the operation's constructed proposal and checked original snapshot. | A decorator would duplicate proposal construction/reads or need another integration boundary. Post-write checks cannot provide the requested pre-write protection. |
| TemplatePolicy / suite identity | Strict policy currently admits only output_profile and persistence. Extra private generation sources must be reachable from the admitted generation graph. policy.yaml is excluded from generation identity but included in operational component state. | Adding an arbitrary rules file is not automatically safe/admitted. A small generic policy extension carrying opaque native checkconfig is a candidate; do not smuggle output rules into the input context schema or whitelist a tool-specific filename in generic code. |

### Cross-format requirement and original Jinja source

The owner explicitly requires tooling for all template-generated content, including code, rather than a Markdown-only safeguard. The previous Markdownlint recommendation is therefore insufficient as the issue-wide solution. Existing pre-write contentcheck execution is reusable; the missing capability is a checker that distinguishes permitted development from loss of required template structure.

Jinja renders text from source, environment and caller context. Its documented Meta API exposes referenced variables/templates, not a post-generation preservation contract; dynamic references can be unresolved statically. Inspection of the installed python_class template gives a concrete counterexample to exact equality: methods are generated with raise NotImplementedError and an empty class can contain pass. Replacing these with working implementation is expected development, although the placeholder is literal template output. The TypeScript DTO also builds conditional declarations and assignments through macros, loops and filters. The original renderer alone does not declare which emitted elements must remain invariant after generation.

There are three distinct guarantees:

| Check | Required information | Limit |
| --- | --- | --- |
| Exact regenerated output comparison | Original source graph, renderer environment/custom filters, original context and reproducible generation | Rejects legitimate changes to generated placeholders and authored content. It is suitable only for intentionally immutable outputs. |
| Match some possible render of the original template | A supported inverse/render-language analysis and suitable context constraints | Does not establish required post-edit semantics. Flexible content slots admit many outputs; literal generated placeholders can still be intended to change. |
| Preserve declared artifact obligations | Explicit required/optional/conditional/editable semantics associated with the source package | Can admit development and reject structural damage, but these semantics must be supplied rather than inferred as a universal Jinja guarantee. |

Canonical id/pv/pf/sf metadata is generation provenance. It does not store the original context or provide an archived source registry. Selecting the current installed package by ID does not prove that its graph is the original graph. Source mismatch or unavailability must remain visible; a current-contract policy and historical-source conformance are separate choices.

### Existing tool investigation

This is a documentation/source feasibility assessment, not a native execution witness. No drop-in checker for the complete installed Jinja suite and permitted post-generation edits has been established. That is a bounded research finding, not proof that no such tool exists anywhere.

| Tool / API | Verified purpose | Fit for the requested check |
| --- | --- | --- |
| Jinja Meta API | Inspect variables and referenced templates in the source AST. | No documented output-conformance or editable-region semantics. Reusing this alone would reopen the earlier introspection problem. |
| jinja2schema | Infer expected input-context types and a JSON Schema for input. | Validates a different boundary; does not validate edited emitted artifacts. |
| TTP | Extract structured data from text using authored parsing templates and matching expressions. | Cross-format text parsing is possible, but its templates are a separate matching language. Existing Jinja inheritance/macros/filters are not directly a TTP validation contract. Extraction success alone is not full-content acceptance. |
| jinja-reverse | Build derived templates by extracting block contents from samples. Source uses regex for simple block syntax and treats surrounding text literally. | Does not execute the installed Jinja graph or return a complete conformance verdict. No-match samples can still produce an extends-only output; loops/expressions/filters and edited code semantics are not covered. |
| Copier | Regenerate versioned Jinja projects from stored answers and merge template updates with user changes. | Useful for update management, not a pre-write structural acceptance check. Requires source/answer lifecycle absent from current provenance. |
| Markdownlint custom rules | Apply owned predicates to parsed Markdown. | Possible format-specific implementation component only. Neither all-artifact coverage nor direct original-Jinja validation. |

Genji was also checked: it extends Jinja rendering with LLM generation calls and format escaping, rather than checking an independently edited artifact against its source. It is not a solution to this acceptance boundary.

### Language- and artifact-type-agnostic boundary

The owner requires the checker to work entirely at the text/Jinja level, without Markdown/Python/TypeScript parsers or artifact-specific semantic node types. The earlier format-parser candidate is superseded. The candidate scope remains unconditional required main structure, not all emitted text or conditional generation behavior. Whether any implementation is worth its cost remains undecided.

The checker may understand generic text relationships: required fragments, their relative order, line/start/end boundaries, contiguous regions and explicitly editable gaps. It must obtain concrete text and obligations from parsed schema/template data, never from built-in template names, headings, class conventions or revision-history rules. Relative placement is meaningful; absolute line numbers would shift during ordinary authored edits. This is a text-preservation guarantee, not language syntax or semantic correctness.

The current context schema describes generation input. It does not define mandatory output fragments or post-generation editable regions. Jinja required blocks require template overrides during rendering, not immutable output. The installed renderer returns only a string; it does not return a map distinguishing mandatory scaffolding from editable emitted content. Shared document/code bases compose captured blocks through text_block/select/join, and macro output is further transformed. Simply excluding conditionals therefore does not make source-to-output ownership or permanent-literal selection automatic.

A generic matcher for a known sequence of required fragments with editable gaps is the lower-cost component. Producing a reliable source-bound matching specification is the uncertain/high-cost component. Viable bounded research candidates are a minimal explicit text-level declaration in the template/schema, or narrowly supported extraction from actual Jinja definitions. Neither a new annotation dialect nor a generation-tracing/inverse-rendering framework is approved. Any derivation must state its supported subset and report unsupported or ambiguous definitions explicitly.

### Effort versus demonstrated reward

| Candidate | Potential reward | Cost and material limit |
| --- | --- | --- |
| Required text fragments and relative order | Detect broad removal/reordering of deliberately required scaffolding while permitting edits in gaps. | Comparatively small matching logic once obligations exist. A duplicate fragment in free text can create ambiguity; presence/order alone can still admit the demonstrated split revision table. |
| Declared text regions and boundary/continuity obligations | May protect a specific relation that simple anchors miss, without knowing the artifact language. | More precise declarations and template maintenance; effectiveness against the actual example must be demonstrated without introducing artifact-specific rules. |
| Automatic mandatory/editable output derivation across general Jinja | Potentially avoid manual mapping for many templates. | Inheritance, macros, string construction, filters and transformations increase proof and maintenance burden. No existing renderer capability supplies this guarantee; least-heavy feasibility is unproven. |

Do not equate a language-agnostic matcher with a low-effort end-to-end solution. The demonstrated benefit is one structural defect plus qualitative reports of template-discarding rewrites; no failure-rate or time-saving estimate is established.

A further feasibility investigation should be bounded to one small text model and representative existing document/code source graphs. It must distinguish loss/reordering of required text from permitted authored development, disclose whether it actually catches the historical split-table example, and identify the required package annotations/source association work. Stop if useful coverage requires format parsers, template-specific checker predicates, general Jinja introspection/trace infrastructure, or a large second specification of the templates. Deferring runtime protection remains a valid outcome if the useful subset does not justify its lifecycle cost.

### Owner-proposed LLM score gate

The owner proposes a single inexpensive LLM assessment of template compliance, a configured threshold that rejects low-scoring writes, and a generic instruction for the calling agent to review the edit against scaffold_schema for the selected template. Precise comparison and pinpoint findings are intentionally unnecessary. This is a new probabilistic candidate, not approval to implement or contact a provider.

The candidate judge consumes proposed complete text, the selected resolved input schema, relevant admitted Jinja source graph and one generic rubric for preservation of mandatory main structure while permitting authored edits. Template-specific knowledge remains supplied reference data; no format parser or package-specific predicate is required. Model scores are judgments, not measured compliance percentages or calibrated probabilities.

Promptfoo already documents llm-rubric grading, configurable providers, numeric scores, threshold decisions and standalone evaluation of supplied outputs. Its explicit pass field also affects acceptance when present; a score-only policy must be configured deliberately. This is a credible existing native-tool candidate for a thin adapter, not an installed/proven pgmcp route. Compare pinned runtime/adapter overhead with a small provider-backed runner before choosing; there is no existing LLM provider integration in the inspected mcp_server, workspace config or project dependencies.

Existing contentcheck decisions and NativeEvidence can carry failed/passed/unavailable, a generic failure message and native JSON score/model/threshold facts. Existing enforce blocks failed checks before writing; extending the common check DTO merely to add a first-class score is not established as necessary. Sources must be bound to the selected package rather than inferred from proposed provenance. Configured source references may use the existing args boundary, but coherent graph/schema association remains unresolved.

The smallest useful assessment is one model request per applicable edit with bounded output and no agent tools or self-repair loop. Threshold comparison is deterministic code over a validated numeric result. Artifact/template contents are assessment data, not instructions; the rubric must not accept instructions embedded in them. Missing source, malformed result, context overflow and provider timeout are unavailable assessment, not invented high scores. If all such writes must block even report, existing mutation policy needs an explicit strategy change; enforce-only integration reuses current behavior.

ScaffoldSchemaTool currently returns purpose, identity and the complete resolved input schema. It does not expose the full Jinja graph or an output-preservation contract. A generic repair instruction can require scaffold_schema plus inspection of the matching template sources; schema-only remediation must not be advertised as complete. A minimal source attachment or schema-description improvement is an alternative to assess, not a preselected API addition.

The effort/reward advantage is avoiding exact inverse rendering and a new output-contract dialect. Remaining costs are the native runtime/provider setup, reference-context transport, per-edit latency/input tokens and a tiny calibration exercise. The cheapest model cannot be assumed adequate: use a few known good/damaged text examples, permitted code implementation and repeated judgments to check useful separation before selecting model/threshold. Reuse existing probes rather than creating a broad regression matrix. No model, provider, threshold or live judging outcome has been selected. The Jev candidate below adds published pricing and independent latency evidence.

### Jev feasibility candidate

Jev from TypeSafe AI is a typed decision model rather than a generative chat judge. Its Score primitive accepts an ordered rubric of 2–10 described levels and returns a typed score, probabilities and confidence. The raw score ranges from zero to the last level index; normalize in code if using a 0–1 threshold. Confidence describes the answer distribution and is not the structural-compliance score or a correctness guarantee.

As checked on 2026-10-08, jev-1.13.0 costs USD 0.042 per million input tokens; output is free. Calculated request costs at 5k/10k/20k total input tokens are USD 0.00021/0.00042/0.00084, respectively. These are pricing scenarios, not measured pgmcp payload sizes. For a single question, the applicable limit is 32k tokens for state plus that question, despite the separate 64k aggregate request limit. Pin the version rather than jev-latest when calibrating a threshold.

A September 2026 independent evaluation measured mean client-side latency of 0.36 seconds across 346,009 requests at 32-way concurrency, averaging 630 input tokens. Its rubric-scoring requests averaged 727 tokens. This supports investigating a fast route, not promising that latency for complete artifact/schema/Jinja inputs. The study found weaker results for generated-text quality judgments and application-dependent binary thresholds; neither an arbitrary threshold nor general benchmark success proves our preservation criterion.

The vendor documents weaker results with multiple reasoning hops, distracting long input and adversarial instructions inside state. Inferring output obligations through schema, inheritance, macros and filters is the principal feasibility risk. Supply only the relevant admitted source graph as reference data without silently discarding dependencies or artifact text; do not solve a weak result by introducing a template-specific parser or predicate.

The official Python SDK provides typed synchronous/asynchronous API calls. DeepEval already offers JevEval with one request, normalized scores and threshold handling, so an existing evaluator route must be compared with the dependency weight of direct SDK use. Neither is installed or integrated here. A direct SDK route still needs a native checker entry point and a thin pgmcp adapter; placing provider or template logic in generic server orchestration is not justified. Original-source association and enforce/report decisions remain the existing unresolved boundaries.

The owner challenges whole-artifact feasibility using issue460. Local read-only measurements on 2026-10-08 establish:

| Existing artifact | Characters | Whitespace-separated words | Illustrative tokens at 4 / 3 characters per token |
| --- | ---: | ---: | ---: |
| [Issue460 Research](<../issue460/research.md>) | 102,674 | 13,240 | 25,669 / 34,225 |
| [Issue460 detailed findings](<../issue460/research-findings.md>) | 254,283 | 32,464 | 63,571 / 84,761 |

These are measured character/word counts and illustrative token conversions, not Jev token counts or statistically established bounds. No local Jev tokenizer is available. Count reproduction: read the complete UTF-8 file; count characters and whitespace-separated words; divide characters by four or three only for the stated estimates. The six reachable literal-import/extends Jinja sources in the current Research package total 12,079 characters; its root schema adds 2,741 before external schema definitions, rubric and request framing. These current sources illustrate additional input volume and are not claimed to be the exact historical generation graph of issue460.

Even the optimistic four-character estimate puts primary Research plus those source inputs at approximately 29,374 tokens before the remaining input. The detailed findings alone plausibly exceed Jev's 32k state-plus-question limit by a wide margin. The primary document is therefore borderline rather than proven to fit or exceed; the larger artifact demonstrates a material size constraint for a general whole-artifact route.

Recommendation revised: Jev is a bounded-input candidate, not the proposed default for every template-generated artifact. Establish supported payload size before score calibration. A judge with a sufficiently larger context window may preserve the one-call/full-text approach with less integration complexity than chunking or compression, but no provider/model is selected. Silent truncation, checking only the edit diff, or combining independent chunk scores does not establish preservation across the complete artifact. Summarization introduces another model/selection step whose structure-loss risk must be assessed; format-specific extraction would violate the required agnosticism.

If a bounded Jev probe is still useful, reuse existing damaged/allowed examples and one permitted/damaged code pair. Record actual input tokens, repeated score separation and client-side latency. Do not build a broad regression suite or complicated preprocessing to force the candidate to fit. No live Jev call, dependency installation, provider selection or implementation approval is recorded.

### Local model and harness-backed judging routes

Local inference is feasible without a remote judging provider. Ollama supports JSON-schema-constrained responses, and Qwen's official Qwen3.5-4B card declares a native 262,144-token context. Ollama distributes a 4B variant with a 256K model window. This makes the issue460 text volumes plausible input candidates, not proven fast or reliable judgments. Model window, allocated runtime context, hardware memory, input processing time and long-context judgment quality are separate constraints. Ollama's default allocation can be far below the model window and increasing context requires additional memory. Pin model/runtime and reject incomplete input rather than accepting truncation.

| Route | Existing support | Integration boundary and limitation |
| --- | --- | --- |
| Local model service | Ollama structured output; published small long-context model | External native checker calls a configured local service. Additional runtime/model installation and hardware measurement; no per-request remote token charge, but computation has cost. |
| Headless harness session | Codex exec accepts piped input, final JSON Schema, model override and saved CLI authentication; Antigravity SDK documents typed output | External native checker invokes the selected existing harness interface. Separate bounded session, not a callback to this chat; startup, subscription/API usage and input processing must be measured. |
| Active client's model via MCP sampling | MCP sampling standard; VS Code documents model/subscription access | Requires client capability, permission and a request-scoped callback from server to client. Model preferences are hints; client selects the model. This is not supported by the current adapter wire. |
| Producer asks a subagent before editing | Harness delegation can provide a review | Advisory unless the actual write tool enforces a result for the exact proposal. A prompt alone does not establish a no-write guarantee. |

Read-only discovery found codex.exe on PATH; neither ollama nor lms was found there. No runtime was installed, model downloaded or judging session started. Current pgmcp server dispatch has no sampling callback; content requests contain text/file, target_path, args and scratch execution context. The adapter process receives one request over stdin, then stdin closes; it returns the check response on stdout. Calling the active client's model therefore needs an explicit new callback boundary, not adapter access to an existing session API.

Codex and Antigravity document MCP integration, but the inspected pages do not establish MCP sampling support in those clients. Antigravity's SDK route documents API-key setup, so it must not be advertised as reusing IDE subscription access. Codex exec documents saved-auth reuse; that does not guarantee free, inexpensive or low-latency execution. Host delegation tools available to the producer are not automatically exposed to an external checker.

Least-heavy investigation for this workspace: a single external checker using an existing headless Codex session, returning a bounded typed judgment through a thin adapter and existing enforce policy. Keep the judge isolated from mutation tools and recursive pgmcp calls; a read-only filesystem sandbox alone does not establish tool isolation. Judge the complete proposal against coherent schema/source references, with no inherited producer conversation or repair loop. Local inference remains an alternative if on-device operation or measured recurring cost warrants runtime setup. Do not implement a cross-harness orchestrator or sampling bridge before a small large-artifact feasibility witness justifies that cost. Source association, model/threshold adequacy and report policy remain unresolved; no strategy is approved.

### Existing enforcement boundary

Under enforce, a selected required contentcheck failure prevents persistence. Existing report permits failed checks to be written while retaining failure facts; making structural failure block report is a separate owner decision. Missing association, unavailable source/config and unavailable execution cannot be presented as successful template conformance.

The current check transport contains proposed content/its scratch file, target_path, configured args and execution context. It does not carry original text, historical source graph or original render context. Fixed source/config references can potentially be supplied through existing configured args; automatic source-bound resolution needs an explicit ownership and identity decision. Preserve factual guarantees rather than claiming all required inputs already exist.

### Blast radius and evidence

No implementation strategy is approved. The existing pre-write executor offers a small integration boundary, but cross-format checker selection, preservation semantics and source association remain open. Any package metadata extension must stay generic/opaque to server orchestration; no package names, language predicates or native-specific rule schemas belong in generic Python.

Behavioral evidence should distinguish permitted edits from structural damage and verify actual persistence/results. Reuse meaningful existing consumer/enforcement tests and add only missing coverage for the selected behavior; no full-text snapshots, wording inventories or retired checker regressions. The Markdown probes below establish a real gap but cannot establish cross-format coverage or candidate-checker success.

#483's link checker replacement, #476's package release review, #470's text/newline/span/race work and #491's planning-data contracts remain separate.

## Questions

- Can a small schema/Jinja-derived text specification deliver useful protection at acceptable authoring and maintenance cost? Compare known text matching with the cost of deriving mandatory/editable boundaries; do not use format parsers.
- Should checks enforce a selected current package contract or require availability of the exact generation source? How should missing/mismatching source be handled?
- Does report retain its existing semantics or must structural failure also block report writes?
- Compare the owner-proposed single-call LLM score gate with exact text-contract work: reference context, native tool overhead, model/threshold calibration, latency/input-token cost and schema-plus-source remediation. Establish only a small feasibility witness before recommending Design.

## References

- [Editing execution and persistence](<../../../mcp_server/services/edit_operation.py>)
- [Original-source profile selection](<../../../mcp_server/services/edit_construction.py>)
- [Provenance recognition](<../../../mcp_server/services/artifact_header_reader.py>)
- [Package identity and limitations](<../../reference/template_metadata_format.md>)
- [Normal template use](<../../reference/TEMPLATE_LIBRARY_USAGE.md>)
- [Package review procedure](<../schema-template-maintenance.md#develop-and-release-a-package>)
- [Documentation requirements](<../../coding_standards/DOCUMENTATION_STANDARD.md>)
- [Architecture contract](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)
- [Research template](<../../../.pgmcp/template_suite/research/template.jinja2>)
- [Shared document structure](<../../../.pgmcp/template_suite/shared/templates/bases/tier2_markdown_document.jinja2>)
- [Existing original/profile behavior tests](<../../../tests/mcp_server/unit/services/test_edit_construction.py>)
- [Existing public edit behavior tests](<../../../tests/mcp_server/integration/test_edit_public_v3.py>)
- [Current validation bindings](<../../../.pgmcp/config/checks.yaml>)
- [Authoritative instruction model](<../../reference/copilot-agent-instructions-model.md>)

- [Existing contentcheck executor](<../../../mcp_server/execution/check_service.py>)
- [Existing proposed-content wire](<../../../mcp_server/execution/content_input.py>)
- [Tool-level enforcement boundary](<../../../mcp_server/core/decorators/enforcement_decorator.py>)
- [Strict current package policy](<../../../mcp_server/config/schemas/template_suite.py>)
- [Generation-source admission and closure](<../../../mcp_server/services/artifact_identity.py>)
- [Operational package component identity](<../../../mcp_server/services/template_components.py>)
- [Markdownlint custom rule contract](<https://github.com/DavidAnson/markdownlint/blob/main/doc/CustomRules.md>)
- [Markdownlint CLI2 configuration and input](<https://github.com/DavidAnson/markdownlint-cli2>)
- [Built-in Markdownlint rules](<https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md>)
- [Observed CLI2 main metadata, not a selected release](<https://raw.githubusercontent.com/DavidAnson/markdownlint-cli2/main/package.json>)
- [Jinja Meta API and renderer context](<https://jinja.palletsprojects.com/en/stable/api/#the-meta-api>)
- [jinja2schema input-context purpose](<https://jinja2schema.readthedocs.io/en/latest/>)
- [TTP matching-template language](<https://ttp.readthedocs.io/en/latest/Writing%20templates/>)
- [jinja-reverse extraction implementation](<https://github.com/gabihodoroaga/jinja-reverse/blob/master/reverse.py>)
- [Copier update and stored-answer lifecycle](<https://copier.readthedocs.io/en/stable/updating/>)
- [Genji generation and escaping](<https://pypi.org/project/genji/>)
- [Promptfoo LLM rubric and threshold semantics](<https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/llm-rubric/>)
- [Promptfoo evaluation of supplied outputs](<https://www.promptfoo.dev/docs/configuration/expected-outputs/#running-assertions-directly-on-outputs>)
- [Existing factual check decisions and native JSON evidence](<../../../mcp_server/execution/models.py>)
- [Current scaffold_schema output](<../../../mcp_server/tools/template_schema_tool.py>)
- [TypeSafe model versions, pricing and context limits](<https://docs.typesafe.ai/models>)
- [Jev Score rubric and response semantics](<https://docs.typesafe.ai/primitives/score>)
- [Jev documented limitations](<https://docs.typesafe.ai/model-jaggedness/jev-1.13>)
- [Official TypeSafe Python SDK](<https://docs.typesafe.ai/sdk/python>)
- [Existing DeepEval Jev evaluator](<https://deepeval.com/docs/metrics-jev-eval>)
- [Independent Jev evaluation, rubric results and measured latency](<https://arxiv.org/html/2609.37647v1>)
- [Ollama structured outputs](<https://docs.ollama.com/capabilities/structured-outputs>)
- [Ollama runtime context and memory](<https://docs.ollama.com/context-length>)
- [Official Qwen3.5-4B model card](<https://huggingface.co/Qwen/Qwen3.5-4B>)
- [Ollama Qwen3.5 distribution](<https://ollama.com/library/qwen3.5>)
- [Codex non-interactive structured judging and saved authentication](<https://learn.chatgpt.com/docs/non-interactive-mode>)
- [MCP sampling and capability/model selection](<https://modelcontextprotocol.io/specification/2025-11-25/client/sampling>)
- [VS Code documented sampling support](<https://code.visualstudio.com/blogs/2025/06/12/full-mcp-spec-support>)
- [Antigravity SDK authentication and harness support](<https://www.antigravity.google/docs/sdk/overview/>)
- [Antigravity typed output](<https://www.antigravity.google/docs/sdk/structured-output>)
- [Existing server dispatch](<../../../mcp_server/server.py>)
- [Current adapter process transport](<../../../mcp_server/execution/process_runtime.py>)
- [Current adapter wire](<../../../mcp_server/execution/protocol.py>)
- [JSON Schema required properties](<https://json-schema.org/understanding-json-schema/reference/object#required-properties>)
- [Jinja required blocks mean rendering overrides](<https://jinja.palletsprojects.com/en/stable/templates/#required-blocks>)
- [Current Research input schema](<../../../.pgmcp/template_suite/research/context.schema.json>)
- [Python class scaffold and intentional stubs](<../../../.pgmcp/template_suite/python_class/template.jinja2>)
- [TypeScript DTO scaffold and conditional structure](<../../../.pgmcp/template_suite/typescript_dto/template.jinja2>)

## Approved Strategy

Pending owner decision. The owner requires a tooling solution covering all template-generated artifact formats and rejects instruction-only review or Markdown-only coverage as sufficient. The least-heavy/no-new-architecture constraint remains binding.

| Boundary | Candidate to assess | Approval state |
| --- | --- | --- |
| Public edit/scaffold and validation policies | Reuse existing contentcheck/no-write machinery; stronger report protection requires an explicit decision. | Pending |
| Native checker and adapter ownership | Entirely language/type-agnostic text checking from schema/Jinja-derived requirements; no format parsers or template-specific predicates. Only unconditional mandatory main structure is in the candidate scope. | Constraints specified by owner; implementation investment and concrete mechanism/strategy pending |
| Package preservation semantics | Explicit source-associated requirements versus contextual interpretation of original Jinja; do not silently infer permanent structure from generated literals. | Pending |
| Source identity and older/manual artifacts | Decide current-contract versus exact original-source acceptance and unavailable/mismatching source behavior. No guessed association, automatic restamping or compatibility emulation. | Pending |
| Behavioral proof | Small cross-format permitted/damaged edit and persistence coverage; reuse useful tests, avoid full-text/wording matrices. | Pending |

## Expected Results

A selected checker must permit intended code/document development and identify loss of required structure across the applicable template-generated formats. Exact regeneration, source compatibility and preservation of declared obligations must not be conflated. Evidence must identify the actual source/contract association, check scope and native outcome. Enforcement/report semantics and missing-source behavior remain pending; no new tool postconditions are implemented here.

## Evidence

### Historical table damage was a small edit-level defect

Commit ab189a83fb1511c02f73c93a442d4d1f257345c5 removed exactly two blank lines between existing revision rows. The facts remained present while table continuity was lost. Current #483 Research is corrected; no historical document was edited here.

- [Exact revision-table correction](<https://github.com/MikeyVK/phase-gate-mcp/commit/ab189a83fb1511c02f73c93a442d4d1f257345c5>)

**Invocation:** Read-only git show --format= --unified=3 ab189a83fb1511c02f73c93a442d4d1f257345c5 -- docs/development/issue483/research.md

**Observed Result:** Two deleted blank lines, no revision fact changes.

### Current enforce validation admits damaged and valid structural variants alike

Scaffold one disposable research artifact; retain its original text BASE. Each of the three public edits uses operation={op:'rewrite',content:<BASE with the stated change>}, validation='enforce', no explicit template_id. A: insert one blank line immediately before '| 0.2 |' in Version History. B: remove the visible Status/Version/Last Updated block, retaining first-line provenance. C: remove the optional Findings heading/prose and replace the Problem Statement with 'Link acceptance and reviewed artifact conformance are distinct claims.', retaining valid metadata/history. Reconstruct every variant from BASE rather than carrying damage into later cases. The final on-disk file is C.

- [Editing execution and persistence](<../../../mcp_server/services/edit_operation.py>)
- [Original-source profile selection](<../../../mcp_server/services/edit_construction.py>)
- [Research template](<../../../.pgmcp/template_suite/research/template.jinja2>)
- [Shared document structure](<../../../.pgmcp/template_suite/shared/templates/bases/tier2_markdown_document.jinja2>)
- [Current validation bindings](<../../../.pgmcp/config/checks.yaml>)

**Invocation:** scaffold_artifact(artifact_type="research", file_name="edit-proof.md", target_path=".pgmcp/temp/issue121-research", force_target=true, validation="enforce", context={"title":"Issue 121 structural edit probe","problem_statement":"Native link acceptance does not establish artifact conformance.","goals":["Compare structural damage with intentional valid refinement."],"findings":"Optional findings prose can be removed when not needed.","document_metadata":{"status":"Research probe","revisions":[{"version":"0.1","date":"2026-10-08","author":"@imp researcher","change":"Initial disposable probe."},{"version":"0.2","date":"2026-10-08","author":"@imp researcher","change":"Second row for the table boundary probe."}]}}); safe_edit_file(path=".pgmcp/temp/issue121-research/edit-proof.md", operation={"op":"rewrite","content":<variant>}, validation="enforce")

**Observed Result:** All three: success=true, written=true, content_changed=true, validation_status=passed, selected_source=metadata, template_id=research, profile_id=markdown_link_review. Lychee 0.24.2 / adapter 2.0.0 returned native exit 0, zero links and zero errors, configured args --offline --cache=false --include-fragments. Correct link acceptance is not structural approval. Supplemental receipts A a946a9b38c2d4228b03be91ad3aa11de, B 2389d554caaa40f7a4ef20cb37849132, C 2d15d206f2f443c2b25b2453a673ed86. Probes are ignored temporary artifacts, not new test code.

## Risks

### Review wording is mistaken for runtime enforcement

State the accepted guarantee boundary explicitly; do not promise a no-write result from unchanged tools.

**Consequence:** False assurance when an agent omits or misjudges a review.

### Latest or guessed template shape becomes an implicit migration

Use source-bound identity and explicit requirements; disclose mismatches/missing source and resolve material uncertainty.

**Consequence:** Valid manual/older artifacts may be incorrectly rewritten.

### Instruction duplication or frozen content expands the work

Keep one shared procedure, reference it minimally, and distinguish required, optional, conditional and freely authored content.

**Consequence:** Maintenance ballast and false positives against valid refinement.

## Related Documents

- [Issue #121](<https://github.com/MikeyVK/phase-gate-mcp/issues/121>)
- [#483 deferred finding](<../issue483/research.md#deferred-finding--preserve-template-structure-during-artifact-edits>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-08 | @imp researcher | Establish current edit boundaries, reproduce structural gaps and compare minimal source-aware review with runtime alternatives. |
| 0.2 | 2026-10-08 | @imp researcher | Replace the rejected instruction-only recommendation with a bounded contentcheck candidate; expose native-rule, policy/admission and enforce/report decisions. |
| 0.3 | 2026-10-08 | @imp researcher | Require all generated artifact formats; assess existing Jinja-related tools and distinguish exact rendering, source matching and permitted-edit obligations. |
| 0.4 | 2026-10-08 | @imp researcher | Limit the candidate to required main structure and require an agnostic checker consuming schema/template requirements as data; identify the missing input-to-output mapping. |
| 0.5 | 2026-10-08 | @imp researcher | Require text-level language/type agnosticism; supersede format-parser proposals and separate matching cost from Jinja mapping cost with explicit reward and stop criteria. |
| 0.6 | 2026-10-08 | @imp researcher | Assess the owner-proposed single-call LLM score gate, existing grader tooling/check reuse and the limits of schema-only remediation. |
| 0.7 | 2026-10-08 | @imp researcher | Assess Jev pricing, measured latency, typed scoring, input limits and existing evaluator options; recommend a bounded feasibility witness. |
| 0.8 | 2026-10-08 | @imp researcher | Measure issue460 artifact sizes and narrow the Jev recommendation to bounded inputs; keep full-text size and preprocessing costs explicit. |
| 0.9 | 2026-10-08 | @imp researcher | Compare local long-context inference, headless harness judging and MCP sampling; distinguish existing checker reuse from a new client callback boundary. |
