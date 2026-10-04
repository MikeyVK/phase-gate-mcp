<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=QEtFztWtFehT8R5U sf=9PfER5JkyAoFQLRi -->

# Issue 473 — Independent Whitespace Examples

**Status:** RESEARCH — generated whitespace/EOF and text-block boundary normalization approved  
**Version:** 0.3  
**Last Updated:** 2026-10-03

## Purpose and decision boundary

On 2026-10-03 the human agreed to the proposed bounded Python native format/lint objective, while explicitly qualifying that Ruff conformance alone may not establish tidy whitespace. The human requested targeted examples for Python and the document batch and kept whitespace an important independent concern. [Research](research.md#human-approved-python-quality-and-independent-whitespace-objective--2026-10-03) records this decision.

The initial approval established whitespace assessment separately from native conformance. In the subsequent sequential discussion, the human explicitly accepted four generated-spacing/EOF criteria, recorded below and authoritatively in Research. Caller-content ownership is now approved: blank boundary lines of inserted text blocks are normalized, while internal content, meaningful spaces and literal/data values remain preserved. Remaining presentation/enforcement choices are pending. No whole-output formatter, context-wide trimming, runtime preflight change or new schema restriction was selected. The existing clean-break strategy remains binding.

## Method and ownership

Eight probes were generated through public scaffold_artifact with validation=report into the ignored scratch directory. Four Python and four Generic Doc cases deliberately exercise omitted, explicitly empty and populated carriers. All eight native structural preflights passed. Files were neither repaired nor formatted; their hashes remained unchanged after run_checks.

Generic Doc stands for targeted Markdown seams, not exhaustive proof across all seven full-document families. The [document-family comparison](document-family-comparison.md) already measures all seven; Design and later regression evidence must cover family-specific joins too. Legacy output remains comparison evidence, not a whitespace standard.

Measurements use actual source lines, not rendered Markdown. Each terminating newline closes a line; the split sentinel after a final newline is excluded. “Trailing blank lines” counts source lines after the final nonblank line, including whitespace-only lines. An eight-blank-line suffix therefore has nine newline characters after the final text. Raw outputs and line annotations below keep this distinction inspectable.

Template ownership includes provenance/module framing, optional-block joins, indentation supplied by structural macros, separators between generated declarations, and generated EOF spacing. Caller ownership includes the internal blank lines of supplied method bodies and Markdown prose/fences. A generated seam rule cannot be implemented by collapsing every blank run in the complete output.

## Concrete observations

| Probe | Observed source layout | Attribution |
| --- | --- | --- |
| [Empty class](../../../.pgmcp/temp/issue473-whitespace-probes/class_absent.py) | Two blank lines between module description and class; two extra blank lines after pass. | The declaration separator is accepted by this native formatter; EOF surplus is template-generated. |
| [Empty config fields](../../../.pgmcp/temp/issue473-whitespace-probes/config_empty.py) | Four blank lines before imports, three before the class, an indented empty line with four spaces at EOF. | Generated optional/import/field joins; W293 confirms the whitespace-only line. |
| [Two methods with authored spacing](../../../.pgmcp/temp/issue473-whitespace-probes/adapter_authored.py) | Five blank lines before class, two before first method, one between methods, three at EOF; two authored blanks inside first body. | Outer joins are generated; the internal two-line body separator belongs to the caller. |
| [Fixture and two cases](../../../.pgmcp/temp/issue473-whitespace-probes/test_boundaries.py) | Four blank lines before decorator, three between fixture and first case, two between cases, three at EOF. | Generated joins; decorator remains directly attached to its function. |
| [Omitted document carriers](../../../.pgmcp/temp/issue473-whitespace-probes/doc_absent.md) | Two blanks after metadata, three between Purpose prose and Summary, eight at EOF. | All these runs are generated. |
| [Explicitly empty document carriers](../../../.pgmcp/temp/issue473-whitespace-probes/doc_empty.md) | Empty headings are emitted; five/six blanks between them, five at EOF. | Preserve the intentional absent-versus-empty distinction while separately considering spacing. |
| [Authored Markdown](../../../.pgmcp/temp/issue473-whitespace-probes/doc_authored.md) | Three authored blanks in prose, two inside a fence, an authored two-space hard break; five generated blanks between custom sections and eight at EOF. | Caller content is preserved exactly; outer generated joins remain independently measurable. |
| [Multiple section carriers](../../../.pgmcp/temp/issue473-whitespace-probes/doc_carriers.md) | Three generated blanks before Bullets, before Checklist and before the next section; eight at EOF. | Generated joins; labels/headings also relate to the earlier approved Generic Doc presentation change. |

The full contexts and every numbered source line appear in the appendices. The earlier reference Python Class finding was EOF surplus; the other families demonstrate additional joins and an empty-block indentation defect.

## Native evidence and limits

Public run_checks used only these four Python targets with python_format/python_lint, timeout_seconds=120, configured arguments. The complete cached DTO was read from `pgmcp://cache/runs/232619e40b0842f1a4cdb35c64c1194f` and retained below.

Ruff 0.15.6 would reformat all four. Lint reports generated I001 for config/test import framing and W293 for the config's empty field line. RET504 in the adapter is caused by the authored assignment/return body; it is not a template-generated defect. The class has no lint finding, but its formatter diff removes the two trailing blank lines. Thus lint success alone does not prove whitespace quality.

The formatter diff also removes one of the two authored blank lines in the adapter body. A whole-output formatter would therefore change that supplied content. This is evidence for keeping the generated-structure objective distinct from an unrestricted complete-output promise; it does not authorize formatting that caller body.

All four Markdown preflights passed despite the observed runs. Structural Markdown validity consequently does not prove the intended source presentation. This pass makes no claim about complete rendered layout, dependency resolution, runtime execution, typing, every accepted context or future unavailable tools.

## Human-approved generated whitespace and EOF criteria

The human explicitly agreed ("Ja mee eens") to the four criteria below after the researcher presented their scope and limits. These replace the earlier numerical proposals; measured raw probe outputs and native DTOs remain unchanged.

| Surface | Approved criterion | Evidence / boundary |
| --- | --- | --- |
| Python generated declarations | Follow the configured Ruff formatter's syntax-aware spacing, with appropriate treatment of top-level declarations, methods, decorators and docstrings. | A global one-blank rule would damage correct top-level layout. This does not authorize arbitrary caller-body formatting. |
| Markdown generated block joins | One empty separator between independent generated headings, paragraphs, lists, tables and fences; no unnecessary empty lines within a list/table. | Applies to all seven full-document families and Issue/PR bodies. Caller-owned prose/fence spacing and hard breaks are outside this decision. |
| Generated absent/empty parts | No blank-line residue from omitted parts and no generated indentation-only source lines. | Explicitly empty containers retain their defined meaning; surrounding joins are corrected independently. |
| Generated EOF | One terminal newline and no additional template-generated blank lines in every family. | Includes Commit and TypeScript; the approved point 2 trims only blank boundary lines of inserted text blocks, preserving meaningful content/data whitespace. |

TypeScript/Commit have an approved EOF criterion, not a complete new formatter style. TypeScript assignment spacing and other remaining presentation choices belong to point 3. The subsequent point 2 decision explicitly permits text-block boundary trimming as recorded below; it does not authorize whole-output normalization.

[CODE_STYLE.md](../../coding_standards/CODE_STYLE.md#formatting-and-readability) delegates Python whitespace/imports/line length to the configured native tools. [DOCUMENTATION_STANDARD.md](../../coding_standards/DOCUMENTATION_STANDARD.md) must be reconciled with the explicitly agreed generated Markdown objective; the decision is human input rather than a claimed pre-existing universal rule.

The authoritative decision and sequential status are in [Research](research.md). Macro composition, algorithms, exact schemas and verification/enforcement remain Design or later decision work. Independent QA is requested only after all remaining boundary decisions are complete.

## Human-approved text-block boundary treatment

The human explicitly agreed to normalizing empty or space/tab-only lines before/after inserted code/document text blocks. The renderer supplies surrounding separators and EOF. Internal blanks, comments, meaningful spaces on substantive lines, structural code content and fence/literal content remain preserved. Required structural indentation and safe encoding remain rendering responsibilities.

This is one shared render contract under DRY, not a general .strip() on arbitrary context values. Exact literal/data values such as "  value  " are retained. A supplied whitespace-only block becomes empty for composition; the declared absent-versus-supplied-empty container behavior and existing input validation still apply. Routine padding needs no extra caller instructions or new padding-specific errors.

The decision explicitly changes preservation at text-block edges under the approved clean break. No legacy mode or implementation algorithm is selected. [Research](research.md) owns the authoritative boundary; Design must distinguish inserted text from data and preserve meaningful fence/literal lines. Targeted future regression evidence must compare padded/unpadded blocks and prove internal/data preservation. Original probes, hashes and native logs below remain historical, untouched evidence.

## Preservation observations

```json
{
  "adapter_body_preserved": true,
  "markdown_content_preserved": [
    {
      "heading": "Authored prose",
      "exact": true
    },
    {
      "heading": "Authored code",
      "exact": true
    }
  ]
}
```

## Probe contexts, hashes and line views

`<blank>` denotes an empty source line; `<4 spaces>` denotes indentation with no text; `<two trailing spaces>` displays the deliberately authored Markdown hard break. These markers belong to the annotation only and were not inserted into the actual files.

### class_absent.py

Package: `python_class`; SHA-256: `33b86ac8d16e9d5d1d931d16f887d463b026925f0f63bf7c98a24eb128337ca8`. Structural preflight: passed. Receipt: `pgmcp://cache/runs/08787e79fab14f8abc62b663a29d7099`.

```json
{
  "class_name": "WhitespaceExample",
  "description": "Observe an empty class."
}
```

```text
  1 | # pgmcp:v1 id=python_class pv=1.0.0 pf=hy3SAizDAZ8yUHLN sf=9PfER5JkyAoFQLRi
  2 | <blank>
  3 | "Observe an empty class."
  4 | <blank>
  5 | <blank>
  6 | class WhitespaceExample:
  7 |     "Observe an empty class."
  8 | <blank>
  9 |     pass
 10 | <blank>
 11 | <blank>
```

### config_empty.py

Package: `python_pydantic_config`; SHA-256: `8a04d80eb5736a52cda4e9a162eaadfe7b894d65f3476b267716a84dde086d12`. Structural preflight: passed. Receipt: `pgmcp://cache/runs/bdbce06c1cb54238876518282966d6ed`.

```json
{
  "class_name": "WhitespaceSettings",
  "description": "Observe empty fields.",
  "frozen": true,
  "fields": []
}
```

```text
  1 | # pgmcp:v1 id=python_pydantic_config pv=1.0.0 pf=KjQnWprHR3MCCNwv sf=9PfER5JkyAoFQLRi
  2 | <blank>
  3 | "Observe empty fields."
  4 | <blank>
  5 | <blank>
  6 | <blank>
  7 | <blank>
  8 | # Third party
  9 | from pydantic import BaseModel, ConfigDict
 10 | <blank>
 11 | <blank>
 12 | <blank>
 13 | class WhitespaceSettings(BaseModel):
 14 |     "Observe empty fields."
 15 | <blank>
 16 |     model_config = ConfigDict(extra="forbid", frozen=True)
 17 | <4 spaces>
 18 | <blank>
```

### adapter_authored.py

Package: `python_adapter`; SHA-256: `f0d2cd1ff3d09e68a9cbbf39cb6e155d172ffae8184439b6c2f6730899a56943`. Structural preflight: passed. Receipt: `pgmcp://cache/runs/06de81fc2d4d459c8063bb23f5f80738`.

```json
{
  "class_name": "WhitespaceAdapter",
  "description": "Observe method boundaries.",
  "methods": [
    {
      "name": "first",
      "description": "Return authored text.",
      "async": false,
      "parameters": [],
      "return_type": "str",
      "body": "value = \"FIRST\"\n\n\n# AUTHORED_BOUNDARY\nreturn value"
    },
    {
      "name": "second",
      "description": "Return a second value.",
      "async": false,
      "parameters": [],
      "return_type": "str",
      "body": "return \"SECOND\""
    }
  ]
}
```

```text
  1 | # pgmcp:v1 id=python_adapter pv=1.0.0 pf=6_4LR53QIIsijfkP sf=9PfER5JkyAoFQLRi
  2 | <blank>
  3 | "Observe method boundaries."
  4 | <blank>
  5 | <blank>
  6 | <blank>
  7 | <blank>
  8 | <blank>
  9 | class WhitespaceAdapter:
 10 |     "Observe method boundaries."
 11 | <blank>
 12 | <blank>
 13 |     def first(self) -> str:
 14 |         "Return authored text."
 15 |         value = "FIRST"
 16 | <blank>
 17 | <blank>
 18 |         # AUTHORED_BOUNDARY
 19 |         return value
 20 | <blank>
 21 |     def second(self) -> str:
 22 |         "Return a second value."
 23 |         return "SECOND"
 24 | <blank>
 25 | <blank>
 26 | <blank>
```

### test_boundaries.py

Package: `pytest_unit_test`; SHA-256: `8c0e25e8a353f9140ba1c6f50e172b29975f4569d833cdacf806e260f9aa295e`. Structural preflight: passed. Receipt: `pgmcp://cache/runs/cb543a0e1332473e9d6c4dcc639ff820`.

```json
{
  "description": "Observe fixture and case boundaries.",
  "imports": {
    "third_party": [
      {
        "kind": "import",
        "module": "pytest"
      }
    ]
  },
  "fixtures": [
    {
      "name": "sample_value",
      "description": "Provide a value.",
      "async": false,
      "parameters": [],
      "return_type": "int",
      "body": "return 1",
      "decorator": "pytest.fixture"
    }
  ],
  "cases": [
    {
      "name": "test_first",
      "description": "Check the first value.",
      "async": false,
      "parameters": [
        {
          "name": "sample_value",
          "type": "int"
        }
      ],
      "body": "assert sample_value == 1"
    },
    {
      "name": "test_second",
      "description": "Check a literal value.",
      "async": false,
      "parameters": [],
      "body": "assert 2 > 1"
    }
  ]
}
```

```text
  1 | # pgmcp:v1 id=pytest_unit_test pv=1.0.0 pf=KPwraD7t-PPta2Q0 sf=9PfER5JkyAoFQLRi
  2 | <blank>
  3 | "Observe fixture and case boundaries."
  4 | <blank>
  5 | # Third party
  6 | import pytest
  7 | <blank>
  8 | <blank>
  9 | <blank>
 10 | <blank>
 11 | @pytest.fixture
 12 | def sample_value() -> int:
 13 |     "Provide a value."
 14 |     return 1
 15 | <blank>
 16 | <blank>
 17 | <blank>
 18 | def test_first(sample_value: int) -> None:
 19 |     "Check the first value."
 20 |     assert sample_value == 1
 21 | <blank>
 22 | <blank>
 23 | def test_second() -> None:
 24 |     "Check a literal value."
 25 |     assert 2 > 1
 26 | <blank>
 27 | <blank>
 28 | <blank>
```

### doc_absent.md

Package: `generic_doc`; SHA-256: `54b02d2e54c457739df9f21904bce807b6325a6728d2a7e5c40e17b1c49f272d`. Structural preflight: passed. Receipt: `pgmcp://cache/runs/74a155683cee46d8a1c01082f1bade0f`.

```json
{
  "title": "Whitespace probe",
  "purpose": "Observe generated spacing.",
  "summary": "Raw output for issue 473.",
  "status": "Research sample",
  "version": "0.1",
  "last_updated": "2026-10-03"
}
```

```text
  1 | <!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=QEtFztWtFehT8R5U sf=9PfER5JkyAoFQLRi -->
  2 | <blank>
  3 | # Whitespace probe
  4 | <blank>
  5 | **Status:** Research sample
  6 | **Version:** 0.1
  7 | **Last Updated:** 2026-10-03
  8 | <blank>
  9 | <blank>
 10 | ## Purpose
 11 | <blank>
 12 | Observe generated spacing.
 13 | <blank>
 14 | <blank>
 15 | <blank>
 16 | ## Summary
 17 | <blank>
 18 | Raw output for issue 473.
 19 | <blank>
 20 | <blank>
 21 | <blank>
 22 | <blank>
 23 | <blank>
 24 | <blank>
 25 | <blank>
 26 | <blank>
```

### doc_empty.md

Package: `generic_doc`; SHA-256: `76956d608dbf851f7fd599270474258fcc968b44d2ba99a95e9563c122a14ef7`. Structural preflight: passed. Receipt: `pgmcp://cache/runs/b198891a195e47a7a6ccfa7b15459c77`.

```json
{
  "title": "Whitespace probe",
  "purpose": "Observe generated spacing.",
  "summary": "Raw output for issue 473.",
  "status": "Research sample",
  "version": "0.1",
  "last_updated": "2026-10-03",
  "key_changes": [],
  "migration_steps": [],
  "validation_checklist": [],
  "sections": []
}
```

```text
  1 | <!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=QEtFztWtFehT8R5U sf=9PfER5JkyAoFQLRi -->
  2 | <blank>
  3 | # Whitespace probe
  4 | <blank>
  5 | **Status:** Research sample
  6 | **Version:** 0.1
  7 | **Last Updated:** 2026-10-03
  8 | <blank>
  9 | <blank>
 10 | ## Purpose
 11 | <blank>
 12 | Observe generated spacing.
 13 | <blank>
 14 | <blank>
 15 | <blank>
 16 | ## Summary
 17 | <blank>
 18 | Raw output for issue 473.
 19 | <blank>
 20 | <blank>
 21 | ## Key Changes
 22 | <blank>
 23 | <blank>
 24 | <blank>
 25 | <blank>
 26 | <blank>
 27 | ## Migration Steps
 28 | <blank>
 29 | <blank>
 30 | <blank>
 31 | <blank>
 32 | <blank>
 33 | ## Validation Checklist
 34 | <blank>
 35 | <blank>
 36 | <blank>
 37 | <blank>
 38 | <blank>
 39 | <blank>
 40 | ## Sections
 41 | <blank>
 42 | <blank>
 43 | <blank>
 44 | <blank>
 45 | <blank>
```

### doc_authored.md

Package: `generic_doc`; SHA-256: `fcbc82dc1ef9c388c8dc1d876b1e3808cda55723d78a59f1c01eeb02b7653be7`. Structural preflight: passed. Receipt: `pgmcp://cache/runs/77b890c4301041ed87e07790868bbbb7`.

```json
{
  "title": "Whitespace probe",
  "purpose": "Observe generated spacing.",
  "summary": "Raw output for issue 473.",
  "status": "Research sample",
  "version": "0.1",
  "last_updated": "2026-10-03",
  "sections": [
    {
      "heading": "Authored prose",
      "content": "AUTHORED_START\n\n\n\nAUTHORED_END  \nHard break follows two spaces."
    },
    {
      "heading": "Authored code",
      "content": "```python\nvalue = 1\n\n\n# AUTHORED_CODE_BOUNDARY\nprint(value)\n```"
    }
  ]
}
```

```text
  1 | <!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=QEtFztWtFehT8R5U sf=9PfER5JkyAoFQLRi -->
  2 | <blank>
  3 | # Whitespace probe
  4 | <blank>
  5 | **Status:** Research sample
  6 | **Version:** 0.1
  7 | **Last Updated:** 2026-10-03
  8 | <blank>
  9 | <blank>
 10 | ## Purpose
 11 | <blank>
 12 | Observe generated spacing.
 13 | <blank>
 14 | <blank>
 15 | <blank>
 16 | ## Summary
 17 | <blank>
 18 | Raw output for issue 473.
 19 | <blank>
 20 | <blank>
 21 | <blank>
 22 | <blank>
 23 | <blank>
 24 | <blank>
 25 | ## Sections
 26 | <blank>
 27 | <blank>
 28 | ### Authored prose
 29 | <blank>
 30 | <blank>
 31 | **Content:**
 32 | <blank>
 33 | AUTHORED_START
 34 | <blank>
 35 | <blank>
 36 | <blank>
 37 | AUTHORED_END<two trailing spaces>
 38 | Hard break follows two spaces.
 39 | <blank>
 40 | <blank>
 41 | <blank>
 42 | <blank>
 43 | <blank>
 44 | ### Authored code
 45 | <blank>
 46 | <blank>
 47 | **Content:**
 48 | <blank>
 49 | ```python
 50 | value = 1
 51 | <blank>
 52 | <blank>
 53 | # AUTHORED_CODE_BOUNDARY
 54 | print(value)
 55 | ```
 56 | <blank>
 57 | <blank>
 58 | <blank>
 59 | <blank>
 60 | <blank>
 61 | <blank>
 62 | <blank>
 63 | <blank>
```

### doc_carriers.md

Package: `generic_doc`; SHA-256: `4795f276b1493463177f38faa7e9d8d084bc646adbb116fe0d55192ca1ab36b4`. Structural preflight: passed. Receipt: `pgmcp://cache/runs/4fd5bd4b79f94ad18d55e7e59d3cbc03`.

```json
{
  "title": "Whitespace probe",
  "purpose": "Observe generated spacing.",
  "summary": "Raw output for issue 473.",
  "status": "Research sample",
  "version": "0.1",
  "last_updated": "2026-10-03",
  "sections": [
    {
      "heading": "One section",
      "content": "Generated carrier transitions follow.",
      "bullets": [
        "First item.",
        "Second item."
      ],
      "checklist": [
        {
          "text": "Done item.",
          "checked": true
        },
        {
          "text": "Open item.",
          "checked": false
        }
      ]
    },
    {
      "heading": "Next section",
      "content": "Final paragraph."
    }
  ]
}
```

```text
  1 | <!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=QEtFztWtFehT8R5U sf=9PfER5JkyAoFQLRi -->
  2 | <blank>
  3 | # Whitespace probe
  4 | <blank>
  5 | **Status:** Research sample
  6 | **Version:** 0.1
  7 | **Last Updated:** 2026-10-03
  8 | <blank>
  9 | <blank>
 10 | ## Purpose
 11 | <blank>
 12 | Observe generated spacing.
 13 | <blank>
 14 | <blank>
 15 | <blank>
 16 | ## Summary
 17 | <blank>
 18 | Raw output for issue 473.
 19 | <blank>
 20 | <blank>
 21 | <blank>
 22 | <blank>
 23 | <blank>
 24 | <blank>
 25 | ## Sections
 26 | <blank>
 27 | <blank>
 28 | ### One section
 29 | <blank>
 30 | <blank>
 31 | **Content:**
 32 | <blank>
 33 | Generated carrier transitions follow.
 34 | <blank>
 35 | <blank>
 36 | <blank>
 37 | **Bullets:**
 38 | <blank>
 39 | - First item.
 40 | - Second item.
 41 | <blank>
 42 | <blank>
 43 | <blank>
 44 | **Checklist:**
 45 | <blank>
 46 | - [x] Done item.
 47 | - [ ] Open item.
 48 | <blank>
 49 | <blank>
 50 | <blank>
 51 | ### Next section
 52 | <blank>
 53 | <blank>
 54 | **Content:**
 55 | <blank>
 56 | Final paragraph.
 57 | <blank>
 58 | <blank>
 59 | <blank>
 60 | <blank>
 61 | <blank>
 62 | <blank>
 63 | <blank>
 64 | <blank>
```

## Native check DTO

```json
{
  "success": true,
  "run_status": "failed",
  "requested_scope": "targets",
  "requested_targets": [
    ".pgmcp/temp/issue473-whitespace-probes/class_absent.py",
    ".pgmcp/temp/issue473-whitespace-probes/config_empty.py",
    ".pgmcp/temp/issue473-whitespace-probes/adapter_authored.py",
    ".pgmcp/temp/issue473-whitespace-probes/test_boundaries.py"
  ],
  "selected_profile": null,
  "removed_targets": [],
  "results": [
    {
      "check_id": "python_format",
      "status": "failed",
      "reason": null,
      "message": "4 files would be reformatted",
      "evidence": {
        "format": "text",
        "data": "stdout:\n--- .pgmcp\\temp\\issue473-whitespace-probes\\adapter_authored.py\n+++ .pgmcp\\temp\\issue473-whitespace-probes\\adapter_authored.py\n@@ -3,24 +3,16 @@\n \"Observe method boundaries.\"\n \n \n-\n-\n-\n class WhitespaceAdapter:\n     \"Observe method boundaries.\"\n-\n \n     def first(self) -> str:\n         \"Return authored text.\"\n         value = \"FIRST\"\n \n-\n         # AUTHORED_BOUNDARY\n         return value\n \n     def second(self) -> str:\n         \"Return a second value.\"\n         return \"SECOND\"\n-\n-\n-\n\n--- .pgmcp\\temp\\issue473-whitespace-probes\\class_absent.py\n+++ .pgmcp\\temp\\issue473-whitespace-probes\\class_absent.py\n@@ -7,5 +7,3 @@\n     \"Observe an empty class.\"\n \n     pass\n-\n-\n\n--- .pgmcp\\temp\\issue473-whitespace-probes\\config_empty.py\n+++ .pgmcp\\temp\\issue473-whitespace-probes\\config_empty.py\n@@ -2,17 +2,11 @@\n \n \"Observe empty fields.\"\n \n-\n-\n-\n # Third party\n from pydantic import BaseModel, ConfigDict\n \n \n-\n class WhitespaceSettings(BaseModel):\n     \"Observe empty fields.\"\n \n     model_config = ConfigDict(extra=\"forbid\", frozen=True)\n-    \n-\n\n--- .pgmcp\\temp\\issue473-whitespace-probes\\test_boundaries.py\n+++ .pgmcp\\temp\\issue473-whitespace-probes\\test_boundaries.py\n@@ -6,13 +6,10 @@\n import pytest\n \n \n-\n-\n @pytest.fixture\n def sample_value() -> int:\n     \"Provide a value.\"\n     return 1\n-\n \n \n def test_first(sample_value: int) -> None:\n@@ -23,6 +20,3 @@\n def test_second() -> None:\n     \"Check a literal value.\"\n     assert 2 > 1\n-\n-\n-\n\n\nstderr:\n4 files would be reformatted\n"
      },
      "external_tools": [
        {
          "tool_id": "ruff",
          "version": "0.15.6"
        }
      ],
      "adapter": {
        "adapter_id": "ruff",
        "version": "1.0.0",
        "fingerprint": "Y2FKuZ8LbIQH27t4",
        "contract_version": 1
      },
      "capture": {
        "exit_code": 1,
        "stdout": {
          "observed_bytes": 1831,
          "head": null,
          "tail": null,
          "truncated": false
        },
        "stderr": {
          "observed_bytes": 0,
          "head": "",
          "tail": "",
          "truncated": false
        }
      },
      "termination_problem": null,
      "request_rejection": null,
      "args_source": "configured",
      "effective_args": [],
      "coverage": null,
      "required_targets": []
    },
    {
      "check_id": "python_lint",
      "status": "failed",
      "reason": null,
      "message": "RET504 Unnecessary assignment to `value` before `return` statement",
      "evidence": {
        "format": "text",
        "data": "stdout:\nRET504 Unnecessary assignment to `value` before `return` statement\n  --> .pgmcp\\temp\\issue473-whitespace-probes\\adapter_authored.py:19:16\n   |\n18 |         # AUTHORED_BOUNDARY\n19 |         return value\n   |                ^^^^^\n20 |\n21 |     def second(self) -> str:\n   |\nhelp: Remove unnecessary assignment\n\nI001 [*] Import block is un-sorted or un-formatted\n --> .pgmcp\\temp\\issue473-whitespace-probes\\config_empty.py:9:1\n  |\n8 | # Third party\n9 | from pydantic import BaseModel, ConfigDict\n  | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  |\nhelp: Organize imports\n\nW293 [*] Blank line contains whitespace\n  --> .pgmcp\\temp\\issue473-whitespace-probes\\config_empty.py:17:1\n   |\n16 |     model_config = ConfigDict(extra=\"forbid\", frozen=True)\n17 |     \n   | ^^^^\n   |\nhelp: Remove whitespace from blank line\n\nI001 [*] Import block is un-sorted or un-formatted\n --> .pgmcp\\temp\\issue473-whitespace-probes\\test_boundaries.py:6:1\n  |\n5 | # Third party\n6 | import pytest\n  | ^^^^^^^^^^^^^\n  |\nhelp: Organize imports\n\nFound 4 errors.\n[*] 3 fixable with the `--fix` option (1 hidden fix can be enabled with the `--unsafe-fixes` option).\n"
      },
      "external_tools": [
        {
          "tool_id": "ruff",
          "version": "0.15.6"
        }
      ],
      "adapter": {
        "adapter_id": "ruff",
        "version": "1.0.0",
        "fingerprint": "Y2FKuZ8LbIQH27t4",
        "contract_version": 1
      },
      "capture": {
        "exit_code": 1,
        "stdout": {
          "observed_bytes": 1440,
          "head": null,
          "tail": null,
          "truncated": false
        },
        "stderr": {
          "observed_bytes": 0,
          "head": "",
          "tail": "",
          "truncated": false
        }
      },
      "termination_problem": null,
      "request_rejection": null,
      "args_source": "configured",
      "effective_args": [],
      "coverage": null,
      "required_targets": []
    }
  ],
  "error_code": null,
  "error_details": null
}
```

## Version History

| Version | Date | Author | Change |
| --- | --- | --- | --- |
| 0.1 | 2026-10-03 | @imp researcher | Record the qualified quality approval, eight untouched whitespace probes, generated/authored attribution and unapproved numerical criteria. |
| 0.2 | 2026-10-03 | @imp researcher | Record approved generated Python/Markdown spacing, absent-block cleanup and all-family EOF criteria; keep caller-content and enforcement decisions separate. |
| 0.3 | 2026-10-03 | @imp researcher | Record approved trimming of blank text-block boundary lines, preserved internal/data content and renderer-owned joins/EOF. |
