<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=QEtFztWtFehT8R5U sf=9PfER5JkyAoFQLRi -->

# Issue 473 — Python Class v2/v3 Comparison

**Status:** RESEARCH DISCUSSION — no strategy selected  
**Version:** 0.1  
**Last updated:** 2026-10-02

## Purpose and boundary

Compare one plain Python class before discussing other template families. The examples use the same class name and description. This document records observed output, recorded #460 decisions, current standards, and possible objectives for discussion. It neither restores old behavior nor chooses new policy.

The [Research](research.md) remains open. Issue #473 integrates into main; epic #72 is administrative. Generic schema/template-consumption analysis belongs to [issue #476](https://github.com/MikeyVK/phase-gate-mcp/issues/476).

## Artifact locations and reproduction limits

The original 38 accepted first outputs are in `C:/temp/pgmcp/.pgmcp/temp/issue473-survey/`. Their exact contexts, measurements, native evidence and digests are preserved in [first-output-survey.md](first-output-survey.md). These scratch files have not been repaired.

This comparison is in `C:/temp/pgmcp/.pgmcp/temp/issue473-comparison-01/`:

| File | What was executed | Limit |
| --- | --- | --- |
| [artifact_path_resolver.v2-render.py](../../../.pgmcp/temp/issue473-comparison-01/artifact_path_resolver.v2-render.py) | Unmodified legacy public `TemplateEngine.render` using its shipped Generic template and tiered dependencies | Renderer evidence from another checkout; not a full v2 public MCP scaffold |
| [artifact_path_resolver.v3-minimal.py](../../../.pgmcp/temp/issue473-comparison-01/artifact_path_resolver.v3-minimal.py) | Current public `scaffold_artifact(python_class)`, required-only context | Real current schema, preflight, persistence and provenance |
| [artifact_path_resolver.v3.py](../../../.pgmcp/temp/issue473-comparison-01/artifact_path_resolver.v3.py) | Current public scaffold with an import and typed method signature | Representative v3 capability; not an identical legacy payload |

The user identified `C:/Users/miche/.codex/worktrees/issue460-validation-baseline` as the intended old worktree. Inspection finds only the zero-byte `.codex-worktree-name` marker, with no checkout, engine or template files. The intended issue460 pipeline therefore remains unreproduced.

On 2026-10-02, the user explicitly authorized continued use of the located v2 renderer for future work within branch `bug/473-first-call-template-quality`. This resolves source selection for further comparisons on this branch. It does not establish equivalence to the missing issue460 checkout, approve a compatibility strategy, or change the observed scope of renderer-only evidence.

A separate checkout contains the legacy PGMCP engine and templates:

- Source root: `C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a`.
- Engine: `mcp_server/services/template_engine.py`.
- Suite: `mcp_server/scaffolding/templates/`.
- Concrete root: `concrete/generic.py.jinja2`, version 1.2.0.
- Inherited root/code/Python tiers: versions 2.4.0 / 1.4.0 / 1.2.0.

The renderer was explicitly imported from that path and called without source modification. Its result was first captured in memory, then persisted through MCP: scaffold a scratch Python file, then `safe_edit_file` rewrite the exact legacy bytes with enforced Python syntax validation. This persistence bootstrap is not evidence of the legacy schema, routing, metadata-generation or public MCP pipeline.

The old engine selects `trim_blocks=True`, `lstrip_blocks=True`, and `keep_trailing_newline=True`. The current production composition uses a plain Jinja environment without those overrides. This is a relevant layout difference, not proof that changing environment flags is the desired correction.

## Exact inputs and untouched outputs

The minimal contexts share the intended class name and description, but schemas and operation envelopes differ. The legacy raw-render context includes metadata variables normally supplied by the old pipeline; those extra keys are not claimed to be valid old public caller fields.

### Legacy renderer input

```json
{
  "name": "ArtifactPathResolver",
  "description": "Resolves an artifact path within an explicit workspace.",
  "artifact_type": "generic",
  "version_hash": "comparison-only",
  "timestamp": "2026-10-02",
  "format": "python",
  "output_path": "",
  "title": "ArtifactPathResolver"
}
```

The literal `comparison-only` is a probe marker, not a computed v2 version hash or verified provenance identity.

```python
# template=generic version=comparison-only
"""ArtifactPathResolver module.

Resolves an artifact path within an explicit workspace.

@layer: Backend (Generic)
@dependencies: [None]
@responsibilities:
    - [To be defined]
"""

# Standard library
import logging

# Third-party

# Project modules


logger = logging.getLogger(__name__)

class ArtifactPathResolver:
    """Resolves an artifact path within an explicit workspace."""

    def placeholder(self):
        """Placeholder method."""
        pass
```

### Current required-only context

```json
{
  "class_name": "ArtifactPathResolver",
  "description": "Resolves an artifact path within an explicit workspace."
}
```

```python
# pgmcp:v1 id=python_class pv=1.0.0 pf=hy3SAizDAZ8yUHLN sf=9PfER5JkyAoFQLRi

"Resolves an artifact path within an explicit workspace."


class ArtifactPathResolver:
    "Resolves an artifact path within an explicit workspace."

    pass


```

### Current representative filled context

```json
{
  "class_name": "ArtifactPathResolver",
  "description": "Resolves an artifact path within an explicit workspace.",
  "module_description": "Artifact path resolution.",
  "imports": {
    "stdlib": [
      {
        "kind": "from",
        "module": "pathlib",
        "names": [
          {
            "name": "Path"
          }
        ]
      }
    ]
  },
  "methods": [
    {
      "name": "resolve",
      "description": "Return the resolved artifact path.",
      "async": false,
      "parameters": [
        {
          "name": "relative_path",
          "type": "Path"
        }
      ],
      "return_type": "Path"
    }
  ]
}
```

```python
# pgmcp:v1 id=python_class pv=1.0.0 pf=hy3SAizDAZ8yUHLN sf=9PfER5JkyAoFQLRi

"Artifact path resolution."

# Standard library
from pathlib import Path


class ArtifactPathResolver:
    "Resolves an artifact path within an explicit workspace."

    def resolve(self, relative_path: Path) -> Path:
        "Return the resolved artifact path."
        raise NotImplementedError


```

The terminal blank lines are part of the generated files. SHA-256 digests below, rather than Markdown fence rendering, define the exact byte evidence.

## Visible differences and #460 traceability

[The canonical #460 strategy register](../issue460/research.md#approved-strategy-and-decision-status) records the Generic Python responsibility as approved on 2026-08-24. Its F-14 portability row is dated 2026-08-23. [Supporting Generic analysis](../issue460/research-findings.md) describes the old renderer and the approved responsibility at lines 671–704; the primary register governs if wording differs.

| Familiar v2 feature | Observed v3 result | Recorded disposition / confidence |
| --- | --- | --- |
| `@layer: Backend (Generic)`, dependency and responsibility placeholders | Absent | Generic explicitly stops inventing project architecture metadata. Research findings 687, 694, 698; F-14 and Generic register rows. Recorded as approved; original human message not independently retrieved |
| Forced `import logging` and module logger | Absent | Generic no longer forces logging. Same Research boundary; specialized adapter/worker opt-in logging is described separately in [Design §7.6](../issue460/design-code-test-artifacts.md) |
| Fabricated `placeholder(self)` | Minimal class contains `pass` | Research findings 694 explicitly specifies a valid empty class, without fabricated methods |
| Optional supplied methods | v3 admits structured typed signatures and explicit `NotImplementedError` stubs | Research findings 696–697 retain signatures and exclude caller bodies from Generic only; exact schema and initial method kinds are Design-owned |
| Triple-quoted module and class documentation | Short safely quoted Python docstrings | Research requires module/class documentation, not an exact quote dialect. Design §7.3 specifies escaping and multiline preservation; exact quote presentation is not a separate recorded Research approval |
| Three import-group headings, even when groups are empty | No headings for omitted groups; filled example shows supplied standard-library group | Grouped import capability remains in Design §7.3. Empty-heading omission is an observed presentation difference, not proof of a separately approved removal |
| Legacy template/version header | Real v3 package/version/fingerprint and suite fingerprint header | Provenance was deliberately redesigned in #460; this comparison's legacy marker is only a probe and cannot validate old provenance computation |
| Implicit constructor/dunder machinery in shared bases | Generic exposes ordinary methods; specialized packages may retain richer constructs | Design §7.5 and preservation table distinguish package-local Generic restrictions from specialized capabilities. Presence in a legacy base does not prove the old concrete Generic override exposed every capability |

The #460 baseline [probe evidence](../issue460/probe-evidence.yaml) independently records successful minimal Generic rendering and a failed schema-valid filled context: the old schema admitted method strings while the renderer expected structured members. This supports the historical mismatch, but it does not turn this renderer-only comparison into a full old MCP reproduction.

Recorded approval in an artifact and verified original human approval are different evidence levels. The original approval conversations and the missing issue460 checkout remain open provenance questions. This document does not tell the user that every visible presentation change was explicitly approved.

## Current standards assessment

The current [Code Style Guide](../../coding_standards/CODE_STYLE.md) delegates executable whitespace, import and line-length policy to configured tools. It asks for purpose/contract docstrings and explicit public types. It says to add headers only when the relevant source/template contract requires them.

An older Code Style snapshot in the same legacy checkout required standard architecture headers and all three import-group sections. That historical guidance helps explain the familiar v2 appearance; it is not the current repository rule. This pass has not established the exact commit or original human approval that changed the style guide.

| Requirement or question | Current class evidence | Assessment / ownership |
| --- | --- | --- |
| Configured Python formatting | Both v3 samples fail Ruff format only because two terminal blank lines must be removed | Concrete template-owned gap against current style; not a caller-text defect |
| Configured Python lint | Both v3 samples pass selected Ruff lint | Positive evidence for these contexts only; not a universal lint-clean objective |
| Module, class and method purpose docstrings | Generated as valid first-statement string literals; supplied concise descriptions retained | Meets the demonstrated structural requirement. Richer contract explanations remain caller-owned |
| Explicit public types | Filled method has typed argument and return; minimal class has no public method to annotate | Demonstrated compliance; legacy placeholder fails current ANN201 |
| Structured imports and group ownership | Filled sample preserves `from pathlib import Path`; minimal sample invents no imports | Current style supports imports according to native configuration. Full mixed-import compliance requires the broader survey evidence |
| Architecture headers / default logger | Not generated in Generic | No conflict with current Code Style. Restoring a blanket requirement would change the current contract and should be discussed explicitly |
| Single versus triple quotation | Short strings are valid docstrings; current style does not require triple quotation | Presentation preference to discuss; no proven current policy violation |
| Class usefulness | Minimal class is intentionally empty; filled method raises `NotImplementedError` | Matches the bounded Generic responsibility. Application behavior and descriptive completeness are supplied or edited by the caller |

The [Documentation Standard](../../coding_standards/DOCUMENTATION_STANDARD.md) principally governs project documents such as Research, Design and Planning. It does not directly mandate Python docstring quoting or a logger. Its relevant duties here are concrete evidence, traceability, clearly separated questions/decisions, readable comparisons and phase ownership.

| Documentation requirement / maintenance question | Evidence | Assessment |
| --- | --- | --- |
| Evidence distinct from chosen decisions | Contexts, source limits, exact outputs and recorded #460 decisions are separated above | Applied to this Research; possible objectives are not Approved Strategy |
| Phase-specific completeness | Required input fields can produce a structurally valid first draft, not a complete approved phase artifact | #460 workflow alignment explicitly preserves this distinction; generic preflight does not certify substantive completeness |
| Readable presentation | Original survey reports generated blank runs of 4–21 in Markdown and some mechanical carrier labels | Spacing is observed; label redundancy is an editorial question. The standard gives no numeric blank-line limit |
| Document metadata consistency | Standard header says version 1.0 / 2026-05-21; history includes version 1.1 / 2026-06-17 | Concrete documentation maintenance defect |
| Related-document links | Offline Lychee reports four missing local targets in the standard's reference definitions | Concrete defect: repository-root-looking relative paths resolve beneath `docs/coding_standards/docs/coding_standards/` |
| Architecture terminology dependency | [Architecture Principles §16](../../coding_standards/ARCHITECTURE_PRINCIPLES.md) describes bundled `templates/` and artifact-config YAML, while current packages use `template_suite/` and JSON context schemas | Candidate stale implementation terminology; the binding cohesion/configuration principles still apply. Wording and intended scope need reconciliation |

The standards link check inspected both current Code Style and Documentation Standard: 12 total links, eight successful checks and four errors, all attributed to Documentation Standard. No template source, standard, quality configuration or runtime enforcement was changed.

There is a demonstrated formatting gap and documentation maintenance debt. There is no demonstrated current rule requiring the removed Generic architecture metadata or logger. A preference to restore richer first drafts must therefore be discussed alongside the recorded portability boundary, rather than silently enforced through an engine change.

## Verification and exact evidence

Python samples were validated and checked using the current workspace baseline: Python 3.13.7, Ruff 0.15.6. Applying today's configuration to v2 is a comparative observation, not a historical claim about old release gates.

| Check | v2 renderer output | v3 minimal | v3 filled |
| --- | --- | --- | --- |
| Python syntax | Passed on exact-byte MCP persistence | Passed public scaffold preflight | Passed public scaffold preflight |
| Ruff format | Failed; missing blank line before class | Failed; two terminal blank lines | Failed; two terminal blank lines |
| Ruff lint | Failed; ANN201 on `placeholder` return type | Passed | Passed |

| Evidence | Cached run |
| --- | --- |
| Live current Python context schema | `e4ef20c417f64b0b922c1eb6704538bf` |
| v3 minimal scaffold | `0795884e0fab4cc5b5ac17b6b31540f4` |
| v3 filled scaffold | `69674afa05c94d1eb4b1d46d7ca8a826` |
| Exact v2-render persistence rewrite | `5db00a0fc4ca43c685aac5132f96afeb` |
| v2 and v3 minimal native checks | `faff33ed46634161b8271b2aee0613bf` |
| v3 filled native checks | `1d383c19a50944629867afbfc9b7cf00` |
| Current standards native link check | `a6ad5ea07c8b49059b3daefb4eecd56e` |

Complete structured receipts were read from their cached resources, with pagination and length/hash verification. Scratch output SHA-256:

| File | SHA-256 |
| --- | --- |
| v2-render | `56c25e7a4fa4015d390bcfb8107150273d6ae8d17085bdb9e9ce644846e2d95a` |
| v3-minimal | `90d3c82ba6b6fd80d375eeaa4388ebdfadeb15c5bb646193d5c249fea0b977fa` |
| v3-filled | `43c76d99792ee52d0233669705dad1bd0fd935357f981a43ff0895425027629b` |

Legacy engine source SHA-256: `ea6024a1612795b07161b50a6416ad40259757229c7a3885ed891f085d0eb382`.
Legacy Generic template SHA-256: `88438500e84ddd1c0b10eb9f2174508997a97fabed64f09ce3143feeb10666b4`.

## Possible objectives and open discussion

These are questions and candidate objectives, not guarantees or an approval request:

- Make template-owned Python layout pass the configured formatter on the first call for an explicitly bounded context set.
- Decide whether more familiar module documentation, multiline presentation or empty import headings materially improve the plain-class scaffold.
- Distinguish portable defaults from useful workspace-specific architecture conventions; discuss any requested reversal of #460 at the affected boundary.
- Reconcile current standard wording and references with the engine contract so documentation and executable configuration express the same policy.
- Locate or recover the actual issue460 checkout before claiming a complete v2 pipeline comparison or historical provenance equivalence.
- Retrieve original human decisions if recorded artifact status is insufficient to resolve uncertainty about a particular removal.

Automatic test generation is absent from the bounded Generic contract. A separate test-template comparison may be useful later; it is not performed ahead of the requested one-at-a-time Python code comparison. Full Validation, template repairs, standards edits, and #476 consumption analysis remain outside this Research pass.
