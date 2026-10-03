<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=QEtFztWtFehT8R5U sf=9PfER5JkyAoFQLRi -->

# Issue 473 — Untouched First-output Evidence

**Status:** Implementation in progress
**Version:** 0.1
**Last Updated:** 2026-10-03

These actual C_SHARED outputs are characterization and shared-boundary evidence. Concrete code/document corrections remain later cycles. They are not the final 38 pairs. Every file was created through the public tool after catalog restart; no fix/edit touched the output. SHA-256 and literal contexts permit replay in a fresh directory. Fence display does not certify physical newline bytes; measured facts below do.

## c1.commit.representative.txt

Observed 2026-10-03. UTF-8 309 bytes; SHA-256 `84d5c600530b412503318c3f228f18658a417c78975e4e213728e73ab2933061`. EOF: one LF; CRLF pairs: 0. Complete operation receipt: `pgmcp://cache/runs/98279dd6c5e442058c05d5919d0b392d`; read via contiguous cache windows with verified SHA-256.

Request:

```json
{
  "artifact_type": "commit",
  "file_name": "c1.commit.representative.txt",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "type": "feat",
    "scope": "templates",
    "subject": "Preserve authored commit framing",
    "body": "Keep the supplied message text intact.\n\nRetain paragraph boundaries.",
    "breaking_change": true,
    "breaking_description": "Consumers must supply explicit commit fields.",
    "refs": [
      473,
      460
    ],
    "footer": "Reviewed-by: Template Maintainers"
  },
  "validation": "enforce"
}
```

Operation and native rows:

```json
{
  "success": true,
  "written": true,
  "validation_status": "passed",
  "profile_id": "commit_preflight",
  "package_version": "1.0.0",
  "package_fingerprint": "3TpXe6SmgbR9G_PI",
  "checks": [
    {
      "check_id": "commit_message",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": {
        "format": "text",
        "data": "checked message view (first valid provenance line removed):\n\nfeat(templates)!: Preserve authored commit framing\n\nKeep the supplied message text intact.\n\nRetain paragraph boundaries.\n\nBREAKING CHANGE: Consumers must supply explicit commit fields.\n\nRefs: #473, #460\n\nReviewed-by: Template Maintainers\n\nnative exit code: 0\nstdout:\n\nstderr:\n"
      },
      "invocation": {
        "adapter": {
          "adapter_id": "commitlint",
          "version": "1.0.0",
          "fingerprint": "33ygyZvwX7L9eAnv",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 490,
            "head": null,
            "tail": null,
            "truncated": false
          },
          "stderr": {
            "observed_bytes": 225,
            "head": "C:\\Users\\miche\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\pydantic\\_internal\\_fields.py:198: UserWarning: Field name \"schema\" in \"SchemaAttachment\" shadows an attribute in parent \"BaseModel\"\r\n  warnings.warn(\r\n",
            "tail": "",
            "truncated": false
          }
        },
        "external_tools": [
          {
            "tool_id": "commitlint",
            "version": "21.2.2"
          }
        ]
      },
      "args_source": "configured",
      "effective_args": []
    }
  ]
}
```

Untouched output (literal content):

~~~~
# pgmcp:v1 id=commit pv=1.0.0 pf=3TpXe6SmgbR9G_PI sf=EtVV09H1wi7LX7HU

feat(templates)!: Preserve authored commit framing

Keep the supplied message text intact.

Retain paragraph boundaries.

BREAKING CHANGE: Consumers must supply explicit commit fields.

Refs: #473, #460

Reviewed-by: Template Maintainers
~~~~

## c1.generic_doc.padding.md

Observed 2026-10-03. UTF-8 306 bytes; SHA-256 `48f0b1567e9dfeec2c2e481511a3d5b75e7f391742d12ec3e48c5c8df458560a`. EOF: one LF; CRLF pairs: 9. Complete operation receipt: `pgmcp://cache/runs/29b1620f0a7947249d5a47a00b8ee657`; read via contiguous cache windows with verified SHA-256.

Request:

```json
{
  "artifact_type": "generic_doc",
  "file_name": "c1.generic_doc.padding.md",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "title": "Boundary preservation",
    "purpose": "\n \t\nPurpose retains a hard break.  \r\nNext line.\r\n\t \n",
    "summary": " \t\r\nA paragraph.\r\n\r\n    indented detail\r\n\r\n```text\r\nfence interior\r\n\r\nend\r\n```\r\n \t\r\n",
    "sections": [
      {
        "heading": "Explicit empty",
        "content": " \t\n \n"
      }
    ]
  },
  "validation": "enforce"
}
```

Operation and native rows:

```json
{
  "success": true,
  "written": true,
  "validation_status": "passed",
  "profile_id": "markdown_document",
  "package_version": "1.0.0",
  "package_fingerprint": "rhyxnjcE-yt08Bsz",
  "checks": [
    {
      "check_id": "markdown_document",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "invocation": {
        "adapter": {
          "adapter_id": "markdown_preflight",
          "version": "1.0.0",
          "fingerprint": "v0NjYjqP55u7eH7r",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "args_source": "configured",
      "effective_args": []
    }
  ]
}
```

Untouched output (literal content):

~~~~
<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=rhyxnjcE-yt08Bsz sf=EtVV09H1wi7LX7HU -->

# Boundary preservation

## Purpose

Purpose retains a hard break.  
Next line.

## Summary

A paragraph.

    indented detail

```text
fence interior

end
```






## Sections


### Explicit empty


**Content:**
~~~~

## c1.generic_doc.representative.md

Observed 2026-10-03. UTF-8 1028 bytes; SHA-256 `408c45260ce0b511e90efdd1655006f554b5e3773731c79420030ba6f74567f9`. EOF: one LF; CRLF pairs: 0. Complete operation receipt: `pgmcp://cache/runs/1ec9780261aa4ee5ab5ba2ed733b41ab`; read via contiguous cache windows with verified SHA-256.

Request:

```json
{
  "artifact_type": "generic_doc",
  "file_name": "c1.generic_doc.representative.md",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "title": "Template Output Review",
    "status": "Research",
    "version": "1.0",
    "last_updated": "2026-10-02",
    "purpose": "Record observations from representative first-call rendering.",
    "scope_in": "Six shipped concrete template packages.",
    "scope_out": "Template implementation choices.",
    "prerequisites": [
      "Use contexts valid against each package schema."
    ],
    "related_docs": [
      {
        "label": "Template suite",
        "target": "../../../.pgmcp/template_suite/README.md"
      }
    ],
    "summary": "Generated formatting and Markdown presentation are assessed separately from caller-owned values.",
    "key_changes": [
      "Compare minimal and populated output.",
      "Record defects by ownership boundary."
    ],
    "migration_steps": [],
    "validation_checklist": [
      {
        "text": "Check output using representative contexts.",
        "checked": false
      }
    ],
    "faq": [
      {
        "question": "Does a valid context guarantee polished output?",
        "answer": "That guarantee remains a research decision."
      }
    ],
    "sections": [
      {
        "heading": "Evidence",
        "content": "Compare generated structure with the supplied values."
      }
    ]
  },
  "validation": "enforce"
}
```

Operation and native rows:

```json
{
  "success": true,
  "written": true,
  "validation_status": "passed",
  "profile_id": "markdown_document",
  "package_version": "1.0.0",
  "package_fingerprint": "rhyxnjcE-yt08Bsz",
  "checks": [
    {
      "check_id": "markdown_document",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": {
        "format": "json",
        "data": {
          "issues": [
            {
              "severity": "warning",
              "message": "Broken link: '<../../../.pgmcp/template_suite/README.md>' not found at C:\\temp\\pgmcp\\.pgmcp\\temp\\.pgmcp\\template_suite\\README.md>",
              "line": 71
            }
          ]
        }
      },
      "invocation": {
        "adapter": {
          "adapter_id": "markdown_preflight",
          "version": "1.0.0",
          "fingerprint": "v0NjYjqP55u7eH7r",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 323,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "args_source": "configured",
      "effective_args": []
    }
  ]
}
```

Untouched output (literal content):

~~~~
<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=rhyxnjcE-yt08Bsz sf=EtVV09H1wi7LX7HU -->

# Template Output Review

**Status:** Research
**Version:** 1.0
**Last Updated:** 2026-10-02

## Purpose

Record observations from representative first-call rendering.

## Scope In

Six shipped concrete template packages.

## Scope Out

Template implementation choices.

## Prerequisites

- Use contexts valid against each package schema.

## Summary

Generated formatting and Markdown presentation are assessed separately from caller-owned values.


## Key Changes

- Compare minimal and populated output.
- Record defects by ownership boundary.



## Migration Steps





## Validation Checklist

- [ ] Check output using representative contexts.



## FAQ


### Does a valid context guarantee polished output?

That guarantee remains a research decision.




## Sections


### Evidence


**Content:**

Compare generated structure with the supplied values.

## Related Documents

- [Template suite](<../../../.pgmcp/template_suite/README.md>)
~~~~

## c1.issue.representative.md

Observed 2026-10-03. UTF-8 662 bytes; SHA-256 `5364ed9c9012e5bfec643278e223d9bfb58c93f731829052ac5fbf3316bd8c42`. EOF: one LF; CRLF pairs: 0. Complete operation receipt: `pgmcp://cache/runs/30eef81218fc484ca7e3f15064353b84`; read via contiguous cache windows with verified SHA-256.

Request:

```json
{
  "artifact_type": "issue",
  "file_name": "c1.issue.representative.md",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "problem": "The generated Markdown contains extra blank lines.",
    "summary": "The defect appears with valid issue content.",
    "expected": "Headings and paragraphs have consistent spacing.",
    "actual": "The rendered body has excessive vertical whitespace.",
    "context": "Exercise the shipped issue template with valid content.",
    "reproduction_steps": [
      "Render the issue package with this context.",
      "Inspect whitespace between sections."
    ],
    "related_docs": [
      {
        "label": "Template contract",
        "target": "../../../.pgmcp/template_suite/issue/context.schema.json"
      }
    ]
  },
  "validation": "enforce"
}
```

Operation and native rows:

```json
{
  "success": true,
  "written": true,
  "validation_status": "passed",
  "profile_id": "markdown_body",
  "package_version": "1.0.0",
  "package_fingerprint": "jm4QBysArXjknPkj",
  "checks": [
    {
      "check_id": "markdown_body",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "invocation": {
        "adapter": {
          "adapter_id": "markdown_preflight",
          "version": "1.0.0",
          "fingerprint": "v0NjYjqP55u7eH7r",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "args_source": "configured",
      "effective_args": []
    }
  ]
}
```

Untouched output (literal content):

~~~~
<!-- pgmcp:v1 id=issue pv=1.0.0 pf=jm4QBysArXjknPkj sf=EtVV09H1wi7LX7HU -->

## Problem

The generated Markdown contains extra blank lines.


## Summary

The defect appears with valid issue content.



## Expected Behavior

Headings and paragraphs have consistent spacing.



## Actual Behavior

The rendered body has excessive vertical whitespace.



## Context

Exercise the shipped issue template with valid content.



## Reproduction Steps

1. Render the issue package with this context.
2. Inspect whitespace between sections.

## Related Documents

- [Template contract][related-1]

[related-1]: <../../../.pgmcp/template_suite/issue/context.schema.json>
~~~~

## c1.pr.representative.md

Observed 2026-10-03. UTF-8 673 bytes; SHA-256 `0a171d7cd906b9f4691a99dc2e788a2bb82d4db0de68431d45ef2fe6a73d97f9`. EOF: one LF; CRLF pairs: 0. Complete operation receipt: `pgmcp://cache/runs/69e13f68228e437f902b70173ffea75e`; read via contiguous cache windows with verified SHA-256.

Request:

```json
{
  "artifact_type": "pr",
  "file_name": "c1.pr.representative.md",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "summary": "First-call template output is easier to review.",
    "changes": "Render each shipped concrete package with minimal and populated valid contexts.",
    "testing": "Inspect both generated forms for Python formatting and Markdown presentation.",
    "checklist": [
      {
        "text": "Confirm supplied values are preserved.",
        "checked": true
      },
      {
        "text": "Review rendered whitespace.",
        "checked": false
      }
    ],
    "breaking_changes": "None.",
    "deferred_work": [
      {
        "description": "Review markdown layout",
        "rationale": "The generated body should be readable in a pull request.",
        "references": [
          {
            "label": "PR template schema",
            "target": "../../../.pgmcp/template_suite/pr/context.schema.json"
          }
        ]
      }
    ],
    "closes": [
      473
    ]
  },
  "validation": "enforce"
}
```

Operation and native rows:

```json
{
  "success": true,
  "written": true,
  "validation_status": "passed",
  "profile_id": "markdown_body",
  "package_version": "1.0.0",
  "package_fingerprint": "p7sHZu8BNPzEY0Ow",
  "checks": [
    {
      "check_id": "markdown_body",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": {
        "format": "json",
        "data": {
          "issues": [
            {
              "severity": "warning",
              "message": "Broken link: '<../../../.pgmcp/template_suite/pr/context.schema.json>' not found at C:\\temp\\pgmcp\\.pgmcp\\temp\\.pgmcp\\template_suite\\pr\\context.schema.json>",
              "line": 42
            }
          ]
        }
      },
      "invocation": {
        "adapter": {
          "adapter_id": "markdown_preflight",
          "version": "1.0.0",
          "fingerprint": "v0NjYjqP55u7eH7r",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 350,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "args_source": "configured",
      "effective_args": []
    }
  ]
}
```

Untouched output (literal content):

~~~~
<!-- pgmcp:v1 id=pr pv=1.0.0 pf=p7sHZu8BNPzEY0Ow sf=EtVV09H1wi7LX7HU -->

## Summary

First-call template output is easier to review.


## Changes

Render each shipped concrete package with minimal and populated valid contexts.


## Testing

Inspect both generated forms for Python formatting and Markdown presentation.



## Checklist

- [x] Confirm supplied values are preserved.
- [ ] Review rendered whitespace.



## Breaking Changes

None.


## Deferred Work



### Review markdown layout

The generated body should be readable in a pull request.


**References:**

- [PR template schema](<../../../.pgmcp/template_suite/pr/context.schema.json>)





## Closes

#473
~~~~

## c1.python_adapter.representative.py

Observed 2026-10-03. UTF-8 497 bytes; SHA-256 `29fd77a97aa2bacf4a7bbede63547a4fc42a4c2501f0c4a733760f4086e71a9b`. EOF: one LF; CRLF pairs: 0. Complete operation receipt: `pgmcp://cache/runs/8af2b18843514c829d52e562ad69feb5`; read via contiguous cache windows with verified SHA-256.

Request:

```json
{
  "artifact_type": "python_adapter",
  "file_name": "c1.python_adapter.representative.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "PriceAdapter",
    "description": "Adapts a price source.",
    "module_description": "Market data adapter.",
    "imports": {
      "project": [
        {
          "kind": "from",
          "module": "market_ports",
          "names": [
            {
              "name": "PriceClient"
            }
          ]
        }
      ]
    },
    "logging": {
      "name": "market.adapter"
    },
    "constructor": {
      "parameters": [
        {
          "name": "client",
          "type": "PriceClient"
        }
      ],
      "body": "self._client = client"
    },
    "methods": [
      {
        "name": "read_price",
        "description": "Return the latest price.",
        "async": false,
        "parameters": [
          {
            "name": "symbol",
            "type": "str"
          }
        ],
        "return_type": "int",
        "body": "return self._client.read_price(symbol)"
      }
    ]
  },
  "validation": "enforce"
}
```

Operation and native rows:

```json
{
  "success": true,
  "written": true,
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "package_version": "1.0.0",
  "package_fingerprint": "HgDV2o_dmkAr6N14",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "args_source": "configured",
      "effective_args": []
    }
  ]
}
```

Untouched output (literal content):

~~~~
# pgmcp:v1 id=python_adapter pv=1.0.0 pf=HgDV2o_dmkAr6N14 sf=EtVV09H1wi7LX7HU

"Market data adapter."

# Standard library
import logging

# Project
from market_ports import PriceClient


logger = logging.getLogger("market.adapter")


class PriceAdapter:
    "Adapts a price source."

    def __init__(self, client: PriceClient) -> None:
        self._client = client


    def read_price(self, symbol: str) -> int:
        "Return the latest price."
        return self._client.read_price(symbol)
~~~~

## c1.python_class.padding.py

Observed 2026-10-03. UTF-8 296 bytes; SHA-256 `871a6deecd77596a1899e1ed4b2e53f8d0e3e20df7be442f1cf56b417db6f58f`. EOF: one LF; CRLF pairs: 0. Complete operation receipt: `pgmcp://cache/runs/7ee42e3147a04a23a2cd156863ff94d2`; read via contiguous cache windows with verified SHA-256.

Request:

```json
{
  "artifact_type": "python_class",
  "file_name": "c1.python_class.padding.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "BoundaryClass",
    "description": "\n \t\nClass interior.\r\n\r\n  Indented.\r\n \t\n",
    "module_description": " \t\n",
    "methods": [
      {
        "name": "sample",
        "description": "\n  Method text.\n\t\n",
        "async": false,
        "parameters": [
          {
            "name": "value",
            "type": "str",
            "default": " \t\nliteral interior\r\n \t"
          }
        ],
        "return_type": "str"
      }
    ]
  },
  "validation": "enforce"
}
```

Operation and native rows:

```json
{
  "success": true,
  "written": true,
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "package_version": "1.0.0",
  "package_fingerprint": "GRzDnCXYeq-Ux0vH",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "args_source": "configured",
      "effective_args": []
    }
  ]
}
```

Untouched output (literal content):

~~~~
# pgmcp:v1 id=python_class pv=1.0.0 pf=GRzDnCXYeq-Ux0vH sf=EtVV09H1wi7LX7HU

""


class BoundaryClass:
    "Class interior.\x0d\x0a\x0d\x0a  Indented."

    def sample(self, value: str = " \x09\x0aliteral interior\x0d\x0a \x09") -> str:
        "  Method text."
        raise NotImplementedError
~~~~

## c1.python_class.representative.py

Observed 2026-10-03. UTF-8 369 bytes; SHA-256 `2e25327e20575c8e42ffd3bfa98b1c65b0fa21f19cd7ce5f2b1dfb0d3399f90e`. EOF: one LF; CRLF pairs: 0. Complete operation receipt: `pgmcp://cache/runs/fb8dcc20163c4753801638cbc126d15c`; read via contiguous cache windows with verified SHA-256.

Request:

```json
{
  "artifact_type": "python_class",
  "file_name": "c1.python_class.representative.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "PriceCalculator",
    "description": "Calculates a notional value.",
    "imports": {
      "stdlib": [
        {
          "kind": "from",
          "module": "decimal",
          "names": [
            {
              "name": "Decimal"
            }
          ]
        }
      ]
    },
    "methods": [
      {
        "name": "notional",
        "description": "Multiply quantity by unit price.",
        "async": false,
        "parameters": [
          {
            "name": "quantity",
            "type": "Decimal"
          },
          {
            "name": "unit_price",
            "type": "Decimal"
          }
        ],
        "return_type": "Decimal"
      }
    ]
  },
  "validation": "enforce"
}
```

Operation and native rows:

```json
{
  "success": true,
  "written": true,
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "package_version": "1.0.0",
  "package_fingerprint": "GRzDnCXYeq-Ux0vH",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "args_source": "configured",
      "effective_args": []
    }
  ]
}
```

Untouched output (literal content):

~~~~
# pgmcp:v1 id=python_class pv=1.0.0 pf=GRzDnCXYeq-Ux0vH sf=EtVV09H1wi7LX7HU

"Calculates a notional value."

# Standard library
from decimal import Decimal


class PriceCalculator:
    "Calculates a notional value."

    def notional(self, quantity: Decimal, unit_price: Decimal) -> Decimal:
        "Multiply quantity by unit price."
        raise NotImplementedError
~~~~

## c1.python_pydantic_dto.representative.py

Observed 2026-10-03. UTF-8 649 bytes; SHA-256 `af0d68a79a9e195a33c4fa6360ccaf39a977882c4ecb3df08399a0126064fb28`. EOF: one LF; CRLF pairs: 0. Complete operation receipt: `pgmcp://cache/runs/b18af35bfc4249bb9970ecfdbdcd2e78`; read via contiguous cache windows with verified SHA-256.

Request:

```json
{
  "artifact_type": "python_pydantic_dto",
  "file_name": "c1.python_pydantic_dto.representative.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "PriceSnapshot",
    "description": "A price snapshot.",
    "module_description": "Validated market data.",
    "imports": {
      "stdlib": [
        {
          "kind": "import",
          "module": "datetime"
        }
      ]
    },
    "fields": [
      {
        "name": "symbol",
        "type": "str",
        "description": "Instrument identifier.",
        "min_length": 1
      },
      {
        "name": "mid",
        "type": "float",
        "description": "Mid-market price.",
        "gt": 0
      },
      {
        "name": "observed_at",
        "type": "datetime.datetime",
        "description": "Observation time.",
        "default_factory": "datetime.datetime.now"
      }
    ],
    "examples": [
      {
        "symbol": "ABC",
        "mid": 101.25
      }
    ]
  },
  "validation": "enforce"
}
```

Operation and native rows:

```json
{
  "success": true,
  "written": true,
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "package_version": "1.0.0",
  "package_fingerprint": "fd6PPe2Rx3NX6gPJ",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "args_source": "configured",
      "effective_args": []
    }
  ]
}
```

Untouched output (literal content):

~~~~
# pgmcp:v1 id=python_pydantic_dto pv=1.0.0 pf=fd6PPe2Rx3NX6gPJ sf=EtVV09H1wi7LX7HU

"Validated market data."

# Standard library
import datetime

# Third party
from pydantic import BaseModel, ConfigDict, Field


class PriceSnapshot(BaseModel):
    "A price snapshot."

    model_config = ConfigDict(extra="forbid", frozen=True, json_schema_extra={"examples": [{"symbol": "ABC", "mid": 101.25}]})
    symbol: str = Field(description="Instrument identifier.", min_length=1)
    mid: float = Field(description="Mid-market price.", gt=0)
    observed_at: datetime.datetime = Field(default_factory=datetime.datetime.now, description="Observation time.")
~~~~

## c1.typescript_dto.representative.ts

Observed 2026-10-03. UTF-8 723 bytes; SHA-256 `3a379b32c2ce9a70abb0928f52a5cb33f88052a44c7b11847cb1b49b6d284590`. EOF: one LF; CRLF pairs: 0. Complete operation receipt: `pgmcp://cache/runs/82e6168e0ae741abb93d2191c336a064`; read via contiguous cache windows with verified SHA-256.

Request:

```json
{
  "artifact_type": "typescript_dto",
  "file_name": "c1.typescript_dto.representative.ts",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "PriceSnapshot",
    "description": "A price snapshot.",
    "module_description": "A normalized market price.",
    "imports": [
      "import type { Currency } from './money';"
    ],
    "implements": [
      "PriceRecordContract"
    ],
    "fields": [
      {
        "name": "instrument",
        "type": "string",
        "readonly": true,
        "optional": false,
        "description": "Instrument identifier."
      },
      {
        "name": "currency",
        "type": "Currency",
        "readonly": true,
        "optional": false
      },
      {
        "name": "mid",
        "type": "number",
        "readonly": false,
        "optional": false
      },
      {
        "name": "note",
        "type": "string | null",
        "readonly": false,
        "optional": true
      }
    ]
  },
  "validation": "enforce"
}
```

Operation and native rows:

```json
{
  "success": true,
  "written": true,
  "validation_status": "passed",
  "profile_id": "typescript_preflight",
  "package_version": "1.0.0",
  "package_fingerprint": "tPhFPn9jTxd48ECA",
  "checks": [
    {
      "check_id": "typescript_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "invocation": {
        "adapter": {
          "adapter_id": "typescript_syntax",
          "version": "1.0.0",
          "fingerprint": "asfu0uAAuaq6247x",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 95,
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
        "external_tools": [
          {
            "tool_id": "typescript",
            "version": "6.0.3"
          }
        ]
      },
      "args_source": "configured",
      "effective_args": []
    }
  ]
}
```

Untouched output (literal content):

~~~~
// pgmcp:v1 id=typescript_dto pv=1.0.0 pf=tPhFPn9jTxd48ECA sf=EtVV09H1wi7LX7HU

/**
 * A normalized market price.
 */

import type { Currency } from './money';

/**
 * A price snapshot.
 */
export class PriceSnapshot implements PriceRecordContract {

  /**
   * Instrument identifier.
   */
  public readonly instrument: string;

  public readonly currency: Currency;

  public mid: number;

  public declare note?: string | null;


  constructor(data: {
    instrument: string;
    currency: Currency;
    mid: number;
    note?: string | null;
  }) {

    this.instrument = data.instrument;

    this.currency = data.currency;

    this.mid = data.mid;

    if ("note" in data) {
      this.note = data.note;
    }
  }
}
~~~~

## c1.typescript_dto.absent.ts

Observed 2026-10-03. UTF-8 202 bytes; SHA-256 `fae75c58b92a3211911c39f47d6c777300ed1724105f802a22d83d310b99f634`; one terminal LF. The two outputs distinguish absent/explicit empty input; C_CODE removes the current implicit absent-module fallback. Receipt: `pgmcp://cache/runs/2dd42e746374489bb443d75b5b95af99`.

```json
{
  "request": {
    "artifact_type": "typescript_dto",
    "file_name": "c1.typescript_dto.absent.ts",
    "target_path": ".pgmcp/temp/issue473",
    "force_target": true,
    "context": {
      "class_name": "PriceSnapshot",
      "description": "A price snapshot."
    },
    "validation": "enforce"
  },
  "operation": {
    "success": true,
    "written": true,
    "validation_policy": "enforce",
    "validation_status": "passed",
    "profile_id": "typescript_preflight",
    "checks": [
      {
        "check_id": "typescript_syntax",
        "status": "passed",
        "reason": null,
        "message": null,
        "evidence": null,
        "request_rejection": null,
        "invocation": {
          "adapter": {
            "adapter_id": "typescript_syntax",
            "version": "1.0.0",
            "fingerprint": "asfu0uAAuaq6247x",
            "contract_version": 1
          },
          "capture": {
            "exit_code": 0,
            "stdout": {
              "observed_bytes": 95,
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
          "external_tools": [
            {
              "tool_id": "typescript",
              "version": "6.0.3"
            }
          ]
        },
        "termination_problem": null,
        "housekeeping": [],
        "args_source": "configured",
        "effective_args": []
      }
    ],
    "error_code": null,
    "error_details": null,
    "housekeeping": [],
    "output_path": ".pgmcp/temp/issue473/c1.typescript_dto.absent.ts",
    "template_id": "typescript_dto",
    "package_version": "1.0.0",
    "package_fingerprint": "tPhFPn9jTxd48ECA"
  }
}
```

~~~~
// pgmcp:v1 id=typescript_dto pv=1.0.0 pf=tPhFPn9jTxd48ECA sf=EtVV09H1wi7LX7HU

/**
 * A price snapshot.
 */

/**
 * A price snapshot.
 */
export class PriceSnapshot {


  constructor(data: {}) {
  }
}
~~~~

## c1.typescript_dto.empty.ts

Observed 2026-10-03. UTF-8 185 bytes; SHA-256 `b8f3a0a92d38193cb3eaf80db1ed61cb0f8eabefce18d1d3d1dc027020a6f247`; one terminal LF. The two outputs distinguish absent/explicit empty input; C_CODE removes the current implicit absent-module fallback. Receipt: `pgmcp://cache/runs/875d1becd596496ca4c836adec3b2d01`.

```json
{
  "request": {
    "artifact_type": "typescript_dto",
    "file_name": "c1.typescript_dto.empty.ts",
    "target_path": ".pgmcp/temp/issue473",
    "force_target": true,
    "context": {
      "class_name": "PriceSnapshot",
      "description": "A price snapshot.",
      "module_description": ""
    },
    "validation": "enforce"
  },
  "operation": {
    "success": true,
    "written": true,
    "validation_policy": "enforce",
    "validation_status": "passed",
    "profile_id": "typescript_preflight",
    "checks": [
      {
        "check_id": "typescript_syntax",
        "status": "passed",
        "reason": null,
        "message": null,
        "evidence": null,
        "request_rejection": null,
        "invocation": {
          "adapter": {
            "adapter_id": "typescript_syntax",
            "version": "1.0.0",
            "fingerprint": "asfu0uAAuaq6247x",
            "contract_version": 1
          },
          "capture": {
            "exit_code": 0,
            "stdout": {
              "observed_bytes": 95,
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
          "external_tools": [
            {
              "tool_id": "typescript",
              "version": "6.0.3"
            }
          ]
        },
        "termination_problem": null,
        "housekeeping": [],
        "args_source": "configured",
        "effective_args": []
      }
    ],
    "error_code": null,
    "error_details": null,
    "housekeeping": [],
    "output_path": ".pgmcp/temp/issue473/c1.typescript_dto.empty.ts",
    "template_id": "typescript_dto",
    "package_version": "1.0.0",
    "package_fingerprint": "tPhFPn9jTxd48ECA"
  }
}
```

~~~~
// pgmcp:v1 id=typescript_dto pv=1.0.0 pf=tPhFPn9jTxd48ECA sf=EtVV09H1wi7LX7HU

/**
 * 
 */

/**
 * A price snapshot.
 */
export class PriceSnapshot {


  constructor(data: {}) {
  }
}
~~~~

## C_CODE intermediate native findings

These 18 outputs preceded the final spacing/import/preservation corrections and are not counted as current final pairs. All contents remain untouched. Native syntax passed, while Ruff identified missing class-doc/pass gaps and excessive import-to-variable gaps; later isolated fix instances do not certify these originals.

### C2 intermediate pytest_integration_test minimal

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `1e29a32b4c8a8f86b9cf13d6da8d9d229d46ab7381f0c3a0547642506c9cf4d5`; 225 bytes; terminal sequence "\\n". Receipt `pgmcp://cache/runs/89cd97da07e741a38e8aa966844abb6e`; package 1.0.0, fingerprint `nJmcwvyzZEEA1jnp`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "pytest_integration_test",
  "file_name": "c2_final_pytest_integration_test_minimal.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "description": "Check a rendered integration result.",
    "cases": [
      {
        "name": "test_total",
        "description": "Add two values.",
        "async": false,
        "parameters": [],
        "body": "result = sum([2, 3])\nassert result == 5"
      }
    ]
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=pytest_integration_test pv=1.0.0 pf=nJmcwvyzZEEA1jnp sf=hL6nSzijRu9etOsX

"Check a rendered integration result."


def test_total() -> None:
    "Add two values."
    result = sum([2, 3])
    assert result == 5
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_final_pytest_integration_test_minimal.py",
  "template_id": "pytest_integration_test",
  "package_version": "1.0.0",
  "package_fingerprint": "nJmcwvyzZEEA1jnp"
}
```

### C2 intermediate pytest_integration_test filled

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `e755f3a4baa065439f482c45022ea1ed75f6ccb319ce6555013e7714e1533976`; 407 bytes; terminal sequence "\\n". Receipt `pgmcp://cache/runs/2ccfffe49f054143a2647fe7e2dd0360`; package 1.0.0, fingerprint `nJmcwvyzZEEA1jnp`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "pytest_integration_test",
  "file_name": "c2_final_pytest_integration_test_filled.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "description": "Check a temporary file round trip.",
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
    "cases": [
      {
        "name": "test_file_round_trip",
        "description": "Write and read a temporary file.",
        "async": false,
        "parameters": [
          {
            "name": "tmp_path",
            "type": "Path"
          }
        ],
        "body": "source = tmp_path / \"input.txt\"\nsource.write_text(\"payload\", encoding=\"utf-8\")\nassert source.read_text(encoding=\"utf-8\") == \"payload\""
      }
    ]
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=pytest_integration_test pv=1.0.0 pf=nJmcwvyzZEEA1jnp sf=hL6nSzijRu9etOsX

"Check a temporary file round trip."

# Standard library
from pathlib import Path


def test_file_round_trip(tmp_path: Path) -> None:
    "Write and read a temporary file."
    source = tmp_path / "input.txt"
    source.write_text("payload", encoding="utf-8")
    assert source.read_text(encoding="utf-8") == "payload"
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_final_pytest_integration_test_filled.py",
  "template_id": "pytest_integration_test",
  "package_version": "1.0.0",
  "package_fingerprint": "nJmcwvyzZEEA1jnp"
}
```

### C2 intermediate pytest_unit_test minimal

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `cf78336d26e2294a1f5b27f89e36ddc36406bf52702a29c399b3f700b9ea3c73`; 212 bytes; terminal sequence "\\n". Receipt `pgmcp://cache/runs/8ef1804b47b24494bc6376fb41a8f5da`; package 1.0.0, fingerprint `hLMMuu-e7C4inaNK`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "pytest_unit_test",
  "file_name": "c2_final_pytest_unit_test_minimal.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "description": "Check a small arithmetic result.",
    "cases": [
      {
        "name": "test_sum",
        "description": "Add two values.",
        "async": false,
        "parameters": [],
        "body": "result = sum([2, 3])\nassert result == 5"
      }
    ]
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=pytest_unit_test pv=1.0.0 pf=hLMMuu-e7C4inaNK sf=hL6nSzijRu9etOsX

"Check a small arithmetic result."


def test_sum() -> None:
    "Add two values."
    result = sum([2, 3])
    assert result == 5
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_final_pytest_unit_test_minimal.py",
  "template_id": "pytest_unit_test",
  "package_version": "1.0.0",
  "package_fingerprint": "hLMMuu-e7C4inaNK"
}
```

### C2 intermediate pytest_unit_test filled

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `19555110c724268840723e486aa036b0e30f735357ea4db79aa244cebd9881c8`; 617 bytes; terminal sequence "\\n". Receipt `pgmcp://cache/runs/f1ed183d7359404ca06ed09012bdc1d1`; package 1.0.0, fingerprint `hLMMuu-e7C4inaNK`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "pytest_unit_test",
  "file_name": "c2_final_pytest_unit_test_filled.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "description": "Check serialized fixture content.",
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
      ],
      "third_party": [
        {
          "kind": "import",
          "module": "pytest"
        }
      ]
    },
    "markers": [
      "pytest.mark.usefixtures(\"sample_path\")"
    ],
    "fixtures": [
      {
        "name": "sample_path",
        "description": "Write a temporary text file.",
        "async": false,
        "parameters": [
          {
            "name": "tmp_path",
            "type": "Path"
          }
        ],
        "return_type": "Path",
        "body": "path = tmp_path / \"sample.txt\"\npath.write_text(\"ready\", encoding=\"utf-8\")\nreturn path",
        "decorator": "pytest.fixture",
        "scope": "function",
        "autouse": false
      }
    ],
    "cases": [
      {
        "name": "test_sample_content",
        "description": "Read the fixture file.",
        "async": false,
        "parameters": [
          {
            "name": "sample_path",
            "type": "Path"
          }
        ],
        "body": "assert sample_path.read_text(encoding=\"utf-8\") == \"ready\""
      }
    ]
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=pytest_unit_test pv=1.0.0 pf=hLMMuu-e7C4inaNK sf=hL6nSzijRu9etOsX

"Check serialized fixture content."

# Standard library
from pathlib import Path

# Third party
import pytest


pytestmark = [pytest.mark.usefixtures("sample_path")]


@pytest.fixture(scope="function", autouse=False)
def sample_path(tmp_path: Path) -> Path:
    "Write a temporary text file."
    path = tmp_path / "sample.txt"
    path.write_text("ready", encoding="utf-8")
    return path


def test_sample_content(sample_path: Path) -> None:
    "Read the fixture file."
    assert sample_path.read_text(encoding="utf-8") == "ready"
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_final_pytest_unit_test_filled.py",
  "template_id": "pytest_unit_test",
  "package_version": "1.0.0",
  "package_fingerprint": "hLMMuu-e7C4inaNK"
}
```

### C2 intermediate python_adapter minimal

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `684fe1548b4d1fdca142e91aead2ea9b8acf856f8bbe76882c76914500d51a99`; 164 bytes; terminal sequence "\\n". Receipt `pgmcp://cache/runs/d5c152c92c254197887a7b3e5bbeba5f`; package 1.0.0, fingerprint `slMZZBRxum8KQuGv`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "python_adapter",
  "file_name": "c2_final_python_adapter_minimal.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "PriceAdapter",
    "class_description": "Adapts a price source.",
    "module_description": "Adapts a price source."
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=python_adapter pv=1.0.0 pf=slMZZBRxum8KQuGv sf=hL6nSzijRu9etOsX

"Adapts a price source."


class PriceAdapter:
    "Adapts a price source."
    pass
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_final_python_adapter_minimal.py",
  "template_id": "python_adapter",
  "package_version": "1.0.0",
  "package_fingerprint": "slMZZBRxum8KQuGv"
}
```

### C2 intermediate python_adapter filled

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `e9d85bb1cf32ab19fbf37d925cdde6fa4d8c76fb3fcbd0363b986d98529adcf3`; 496 bytes; terminal sequence "\\n". Receipt `pgmcp://cache/runs/3a8b2a19d5004873848bbc42a1dd1e6f`; package 1.0.0, fingerprint `slMZZBRxum8KQuGv`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "python_adapter",
  "file_name": "c2_final_python_adapter_filled.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "PriceAdapter",
    "module_description": "Market data adapter.",
    "imports": {
      "project": [
        {
          "kind": "from",
          "module": "market_ports",
          "names": [
            {
              "name": "PriceClient"
            }
          ]
        }
      ]
    },
    "logging": {
      "name": "market.adapter"
    },
    "constructor": {
      "parameters": [
        {
          "name": "client",
          "type": "PriceClient"
        }
      ],
      "body": "self._client = client"
    },
    "methods": [
      {
        "name": "read_price",
        "description": "Return the latest price.",
        "async": false,
        "parameters": [
          {
            "name": "symbol",
            "type": "str"
          }
        ],
        "return_type": "int",
        "body": "return self._client.read_price(symbol)"
      }
    ],
    "class_description": "Adapts a price source."
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=python_adapter pv=1.0.0 pf=slMZZBRxum8KQuGv sf=hL6nSzijRu9etOsX

"Market data adapter."

# Standard library
import logging

# Project
from market_ports import PriceClient


logger = logging.getLogger("market.adapter")


class PriceAdapter:
    "Adapts a price source."

    def __init__(self, client: PriceClient) -> None:
        self._client = client

    def read_price(self, symbol: str) -> int:
        "Return the latest price."
        return self._client.read_price(symbol)
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_final_python_adapter_filled.py",
  "template_id": "python_adapter",
  "package_version": "1.0.0",
  "package_fingerprint": "slMZZBRxum8KQuGv"
}
```

### C2 intermediate python_class minimal

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `07bac573452e552349772925f2d62c906d527c25c0ec4f25f79cc9604a713bf5`; 177 bytes; terminal sequence "\\n". Receipt `pgmcp://cache/runs/dbedc0aae38e483dba0b33e532a5edc7`; package 1.0.0, fingerprint `nGD0mdL5prLJnb14`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "python_class",
  "file_name": "c2_final_python_class_minimal.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "PriceCalculator",
    "class_description": "Calculates a notional value.",
    "module_description": "Calculates a notional value."
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=python_class pv=1.0.0 pf=nGD0mdL5prLJnb14 sf=hL6nSzijRu9etOsX

"Calculates a notional value."


class PriceCalculator:
    "Calculates a notional value."
    pass
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_final_python_class_minimal.py",
  "template_id": "python_class",
  "package_version": "1.0.0",
  "package_fingerprint": "nGD0mdL5prLJnb14"
}
```

### C2 intermediate python_class filled

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `a7eb964cfe8612a763fc394d4d6120b237f2d48b7fd37b56e73cfaecb156f277`; 368 bytes; terminal sequence "\\n". Receipt `pgmcp://cache/runs/368cb5439de64dfcb43ccdef08543e0f`; package 1.0.0, fingerprint `nGD0mdL5prLJnb14`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "python_class",
  "file_name": "c2_final_python_class_filled.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "PriceCalculator",
    "imports": {
      "stdlib": [
        {
          "kind": "from",
          "module": "decimal",
          "names": [
            {
              "name": "Decimal"
            }
          ]
        }
      ]
    },
    "methods": [
      {
        "name": "notional",
        "description": "Multiply quantity by unit price.",
        "async": false,
        "parameters": [
          {
            "name": "quantity",
            "type": "Decimal"
          },
          {
            "name": "unit_price",
            "type": "Decimal"
          }
        ],
        "return_type": "Decimal"
      }
    ],
    "class_description": "Calculates a notional value.",
    "module_description": "Module for PriceCalculator."
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=python_class pv=1.0.0 pf=nGD0mdL5prLJnb14 sf=hL6nSzijRu9etOsX

"Module for PriceCalculator."

# Standard library
from decimal import Decimal


class PriceCalculator:
    "Calculates a notional value."

    def notional(self, quantity: Decimal, unit_price: Decimal) -> Decimal:
        "Multiply quantity by unit price."
        raise NotImplementedError
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_final_python_class_filled.py",
  "template_id": "python_class",
  "package_version": "1.0.0",
  "package_fingerprint": "nGD0mdL5prLJnb14"
}
```

### C2 intermediate python_protocol minimal

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `5b3d16de944e2259ea1c623e5c2a8514907d6ca95f01045aebe5ab1739bb20ee`; 218 bytes; terminal sequence "\\n". Receipt `pgmcp://cache/runs/ca72a49d8d9b4455abbe390aeea6e964`; package 1.0.0, fingerprint `kmziv072QAqqNTzE`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "python_protocol",
  "file_name": "c2_final_python_protocol_minimal.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "PriceSource",
    "class_description": "Provides price data.",
    "module_description": "Provides price data."
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=python_protocol pv=1.0.0 pf=kmziv072QAqqNTzE sf=hL6nSzijRu9etOsX

"Provides price data."

# Standard library
from typing import Protocol


class PriceSource(Protocol):
    "Provides price data."
    pass
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_final_python_protocol_minimal.py",
  "template_id": "python_protocol",
  "package_version": "1.0.0",
  "package_fingerprint": "kmziv072QAqqNTzE"
}
```

### C2 intermediate python_protocol filled

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `6b3e9a73c2ec8b71c0b9aaed8ae43e6df0c1073e353c71ce4dbc644fd73b7bfe`; 406 bytes; terminal sequence "\\n". Receipt `pgmcp://cache/runs/4a564bd88acf4f0ea9f1b7b0a0b6a279`; package 1.0.0, fingerprint `kmziv072QAqqNTzE`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "python_protocol",
  "file_name": "c2_final_python_protocol_filled.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "PriceSource",
    "module_description": "Contract for reading market prices.",
    "methods": [
      {
        "name": "read_price",
        "description": "Return a price for one symbol.",
        "async": false,
        "parameters": [
          {
            "name": "symbol",
            "type": "str"
          }
        ],
        "return_type": "int"
      },
      {
        "name": "close",
        "description": "Release the source resources.",
        "async": false,
        "parameters": [],
        "return_type": "None"
      }
    ],
    "class_description": "Provides price data."
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=python_protocol pv=1.0.0 pf=kmziv072QAqqNTzE sf=hL6nSzijRu9etOsX

"Contract for reading market prices."

# Standard library
from typing import Protocol


class PriceSource(Protocol):
    "Provides price data."

    def read_price(self, symbol: str) -> int:
        "Return a price for one symbol."
        ...

    def close(self) -> None:
        "Release the source resources."
        ...
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_final_python_protocol_filled.py",
  "template_id": "python_protocol",
  "package_version": "1.0.0",
  "package_fingerprint": "kmziv072QAqqNTzE"
}
```

### C2 intermediate python_pydantic_config minimal

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `f14ea0ea3aee5def1798099f39cc6570b29e2cd3e0b5423c54ac1838e806dde5`; 299 bytes; terminal sequence "\\n". Receipt `pgmcp://cache/runs/914a6a0fc4834964bae14a3767008d3c`; package 1.0.0, fingerprint `66WD53voKDEd3NUl`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "python_pydantic_config",
  "file_name": "c2_final_python_pydantic_config_minimal.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "RiskSettings",
    "frozen": true,
    "class_description": "Risk settings.",
    "module_description": "Risk settings."
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=python_pydantic_config pv=1.0.0 pf=66WD53voKDEd3NUl sf=hL6nSzijRu9etOsX

"Risk settings."

# Third party
from pydantic import BaseModel, ConfigDict


class RiskSettings(BaseModel):
    "Risk settings."

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_final_python_pydantic_config_minimal.py",
  "template_id": "python_pydantic_config",
  "package_version": "1.0.0",
  "package_fingerprint": "66WD53voKDEd3NUl"
}
```

### C2 intermediate python_pydantic_config filled

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `3bc458fa56af3655f48bdb0b51f717ac5fc2a55ec819e5c169fbcd1677af99c0`; 909 bytes; terminal sequence "\\n". Receipt `pgmcp://cache/runs/4f1b81119222422e93f7fa567ef67ada`; package 1.0.0, fingerprint `66WD53voKDEd3NUl`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "python_pydantic_config",
  "file_name": "c2_final_python_pydantic_config_filled.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "RiskSettings",
    "module_description": "Risk controls for one strategy.",
    "frozen": false,
    "fields": [
      {
        "name": "enabled",
        "type": "bool",
        "description": "Enable order submission.",
        "default": false
      },
      {
        "name": "max_order_size",
        "type": "int",
        "description": "Maximum permitted order size.",
        "default": 0,
        "ge": 0
      },
      {
        "name": "label",
        "type": "str",
        "description": "Optional operator label.",
        "default": "",
        "min_length": 0
      }
    ],
    "examples": [
      {
        "enabled": true,
        "max_order_size": 5,
        "label": "primary"
      }
    ],
    "class_description": "Risk settings."
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=python_pydantic_config pv=1.0.0 pf=66WD53voKDEd3NUl sf=hL6nSzijRu9etOsX

"Risk controls for one strategy."

# Third party
from pydantic import BaseModel, ConfigDict, Field


class RiskSettings(BaseModel):
    "Risk settings."

    model_config = ConfigDict(
        extra="forbid",
        frozen=False,
        json_schema_extra={
            "examples": [
                {
                    "enabled": True,
                    "max_order_size": 5,
                    "label": "primary",
                },
            ],
        },
    )

    enabled: bool = Field(
        default=False,
        description="Enable order submission.",
    )
    max_order_size: int = Field(
        default=0,
        description="Maximum permitted order size.",
        ge=0,
    )
    label: str = Field(
        default="",
        description="Optional operator label.",
        min_length=0,
    )
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_final_python_pydantic_config_filled.py",
  "template_id": "python_pydantic_config",
  "package_version": "1.0.0",
  "package_fingerprint": "66WD53voKDEd3NUl"
}
```

### C2 intermediate python_pydantic_dto minimal

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `aaa79efad919173be7e04f9fd9b7e669075a6747278f4e1468de8a71abcf75d5`; 303 bytes; terminal sequence "\\n". Receipt `pgmcp://cache/runs/d88dcdacf93a47b08452ea057a7a7662`; package 1.0.0, fingerprint `mE-YLzlLSrIvdRtV`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "python_pydantic_dto",
  "file_name": "c2_final_python_pydantic_dto_minimal.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "PriceSnapshot",
    "class_description": "A price snapshot.",
    "module_description": "A price snapshot."
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=python_pydantic_dto pv=1.0.0 pf=mE-YLzlLSrIvdRtV sf=hL6nSzijRu9etOsX

"A price snapshot."

# Third party
from pydantic import BaseModel, ConfigDict


class PriceSnapshot(BaseModel):
    "A price snapshot."

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_final_python_pydantic_dto_minimal.py",
  "template_id": "python_pydantic_dto",
  "package_version": "1.0.0",
  "package_fingerprint": "mE-YLzlLSrIvdRtV"
}
```

### C2 intermediate python_pydantic_dto filled

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `1f73e8be5d0abc79dea97ea08caa6a09e14e818297edcde9adc76c7b7f2445a6`; 863 bytes; terminal sequence "\\n". Receipt `pgmcp://cache/runs/5c8c6cfea49a4298b013b4cb395ea473`; package 1.0.0, fingerprint `mE-YLzlLSrIvdRtV`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "python_pydantic_dto",
  "file_name": "c2_final_python_pydantic_dto_filled.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "PriceSnapshot",
    "module_description": "Validated market data.",
    "imports": {
      "stdlib": [
        {
          "kind": "import",
          "module": "datetime"
        }
      ]
    },
    "fields": [
      {
        "name": "symbol",
        "type": "str",
        "description": "Instrument identifier.",
        "min_length": 1
      },
      {
        "name": "mid",
        "type": "float",
        "description": "Mid-market price.",
        "gt": 0
      },
      {
        "name": "observed_at",
        "type": "datetime.datetime",
        "description": "Observation time.",
        "default_factory": "datetime.datetime.now"
      }
    ],
    "examples": [
      {
        "symbol": "ABC",
        "mid": 101.25
      }
    ],
    "class_description": "A price snapshot."
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=python_pydantic_dto pv=1.0.0 pf=mE-YLzlLSrIvdRtV sf=hL6nSzijRu9etOsX

"Validated market data."

# Standard library
import datetime

# Third party
from pydantic import BaseModel, ConfigDict, Field


class PriceSnapshot(BaseModel):
    "A price snapshot."

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        json_schema_extra={
            "examples": [
                {
                    "symbol": "ABC",
                    "mid": 101.25,
                },
            ],
        },
    )

    symbol: str = Field(
        description="Instrument identifier.",
        min_length=1,
    )
    mid: float = Field(
        description="Mid-market price.",
        gt=0,
    )
    observed_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now,
        description="Observation time.",
    )
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_final_python_pydantic_dto_filled.py",
  "template_id": "python_pydantic_dto",
  "package_version": "1.0.0",
  "package_fingerprint": "mE-YLzlLSrIvdRtV"
}
```

### C2 intermediate python_worker minimal

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `3d2e4b08a26a55a6bf0483411a7590d1b82be8cc5caa6ed7d784dba6f2609dc1`; 260 bytes; terminal sequence "\\n". Receipt `pgmcp://cache/runs/eea00e255ae546409c68d03bda6a1cb5`; package 1.0.0, fingerprint `wnNlUY0mPabVRsbu`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "python_worker",
  "file_name": "c2_final_python_worker_minimal.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "PriceWorker",
    "operation": {
      "name": "process",
      "description": "Return one accepted value.",
      "async": false,
      "parameters": [
        {
          "name": "value",
          "type": "int"
        }
      ],
      "return_type": "int",
      "body": "return value"
    },
    "class_description": "Processes a price update.",
    "module_description": "Processes a price update."
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=python_worker pv=1.0.0 pf=wnNlUY0mPabVRsbu sf=hL6nSzijRu9etOsX

"Processes a price update."


class PriceWorker:
    "Processes a price update."

    def process(self, value: int) -> int:
        "Return one accepted value."
        return value
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_final_python_worker_minimal.py",
  "template_id": "python_worker",
  "package_version": "1.0.0",
  "package_fingerprint": "wnNlUY0mPabVRsbu"
}
```

### C2 intermediate python_worker filled

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `9d5dee43014ff3644300a01b6c34fa5103672609b7c68d9249b2002bdb186819`; 516 bytes; terminal sequence "\\n". Receipt `pgmcp://cache/runs/e0c0e1b80e71442691a65cbe18b150db`; package 1.0.0, fingerprint `wnNlUY0mPabVRsbu`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "python_worker",
  "file_name": "c2_final_python_worker_filled.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "PriceWorker",
    "imports": {
      "project": [
        {
          "kind": "from",
          "module": "market_ports",
          "names": [
            {
              "name": "PriceClient"
            }
          ]
        }
      ]
    },
    "logging": {
      "name": "market.worker"
    },
    "constructor": {
      "parameters": [
        {
          "name": "client",
          "type": "PriceClient"
        }
      ],
      "body": "self._client = client"
    },
    "operation": {
      "name": "process",
      "description": "Publish the accepted price update.",
      "async": false,
      "parameters": [
        {
          "name": "symbol",
          "type": "str"
        },
        {
          "name": "value",
          "type": "int"
        }
      ],
      "return_type": "None",
      "body": "self._client.publish(symbol, value)"
    },
    "class_description": "Publishes a price update.",
    "module_description": "Module for PriceWorker."
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=python_worker pv=1.0.0 pf=wnNlUY0mPabVRsbu sf=hL6nSzijRu9etOsX

"Module for PriceWorker."

# Standard library
import logging

# Project
from market_ports import PriceClient


logger = logging.getLogger("market.worker")


class PriceWorker:
    "Publishes a price update."

    def __init__(self, client: PriceClient) -> None:
        self._client = client

    def process(self, symbol: str, value: int) -> None:
        "Publish the accepted price update."
        self._client.publish(symbol, value)
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_final_python_worker_filled.py",
  "template_id": "python_worker",
  "package_version": "1.0.0",
  "package_fingerprint": "wnNlUY0mPabVRsbu"
}
```

### C2 intermediate typescript_dto minimal

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `2d40b42df5c9d93bb532abc56db06ff859e27531d8b9a742cd316cee01d1ecab`; 167 bytes; terminal sequence "\\n". Receipt `pgmcp://cache/runs/1df130d0ab524852b22f69d7ec1d5ffc`; package 1.0.0, fingerprint `EniV0La_ffqYvp3y`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "typescript_dto",
  "file_name": "c2_final_typescript_dto_minimal.ts",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "PriceSnapshot",
    "class_description": "A price snapshot."
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
// pgmcp:v1 id=typescript_dto pv=1.0.0 pf=EniV0La_ffqYvp3y sf=hL6nSzijRu9etOsX

/**
 * A price snapshot.
 */
export class PriceSnapshot {
  constructor(data: {}) {}
}
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "typescript_preflight",
  "checks": [
    {
      "check_id": "typescript_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "typescript_syntax",
          "version": "1.0.0",
          "fingerprint": "asfu0uAAuaq6247x",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 95,
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
        "external_tools": [
          {
            "tool_id": "typescript",
            "version": "6.0.3"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_final_typescript_dto_minimal.ts",
  "template_id": "typescript_dto",
  "package_version": "1.0.0",
  "package_fingerprint": "EniV0La_ffqYvp3y"
}
```

### C2 intermediate typescript_dto filled

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `67e3e2bb7d4b42fd5638e98ed9462d9d2f43b80f2e387bc102fe384b7d6bdd4c`; 715 bytes; terminal sequence "\\n". Receipt `pgmcp://cache/runs/acc7a1297f8c441191d75a2761de5aae`; package 1.0.0, fingerprint `EniV0La_ffqYvp3y`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "typescript_dto",
  "file_name": "c2_final_typescript_dto_filled.ts",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "PriceSnapshot",
    "module_description": "A normalized market price.",
    "imports": [
      "import type { Currency } from './money';"
    ],
    "implements": [
      "PriceRecordContract"
    ],
    "fields": [
      {
        "name": "instrument",
        "type": "string",
        "readonly": true,
        "optional": false,
        "description": "Instrument identifier."
      },
      {
        "name": "currency",
        "type": "Currency",
        "readonly": true,
        "optional": false
      },
      {
        "name": "mid",
        "type": "number",
        "readonly": false,
        "optional": false
      },
      {
        "name": "note",
        "type": "string | null",
        "readonly": false,
        "optional": true
      }
    ],
    "class_description": "A price snapshot."
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
// pgmcp:v1 id=typescript_dto pv=1.0.0 pf=EniV0La_ffqYvp3y sf=hL6nSzijRu9etOsX

/**
 * A normalized market price.
 */

import type { Currency } from './money';

/**
 * A price snapshot.
 */
export class PriceSnapshot implements PriceRecordContract {
  /**
   * Instrument identifier.
   */
  public readonly instrument: string;
  public readonly currency: Currency;
  public mid: number;
  public declare note?: string | null;

  constructor(data: {
    instrument: string;
    currency: Currency;
    mid: number;
    note?: string | null;
  }) {
    this.instrument = data.instrument;
    this.currency = data.currency;
    this.mid = data.mid;

    if ("note" in data) {
      this.note = data.note;
    }
  }
}
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "typescript_preflight",
  "checks": [
    {
      "check_id": "typescript_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "typescript_syntax",
          "version": "1.0.0",
          "fingerprint": "asfu0uAAuaq6247x",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 95,
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
        "external_tools": [
          {
            "tool_id": "typescript",
            "version": "6.0.3"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_final_typescript_dto_filled.ts",
  "template_id": "typescript_dto",
  "package_version": "1.0.0",
  "package_fingerprint": "EniV0La_ffqYvp3y"
}
```

### Physical CRLF before indentation correction

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `080aa89e86b070896f3a9fd953143648fd548100998562c9c152ad1bb7ba2ddd`; 287 bytes; terminal sequence "\\n". Receipt `pgmcp://cache/runs/d12e4cf135b545838339b2c8abd4e050`; package 1.0.0, fingerprint `Dy1ZHMQjAFdDnt0J`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "python_worker",
  "file_name": "c2_crlf_before.py",
  "target_path": ".pgmcp/temp/issue473/c2_crlf_before.py",
  "force_target": true,
  "context": {
    "class_name": "PriceWorker",
    "operation": {
      "name": "process",
      "description": "Return one accepted value.",
      "async": false,
      "parameters": [
        {
          "name": "value",
          "type": "int"
        }
      ],
      "return_type": "int",
      "body": "\r\n \t\r\nvalue = value + 1\r\n\r\nreturn value\r\n \t\r\n"
    },
    "class_description": "Processes a price update.",
    "module_description": "Processes a price update."
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=python_worker pv=1.0.0 pf=Dy1ZHMQjAFdDnt0J sf=bAu8oCTjP5d0qCGs

"Processes a price update."


class PriceWorker:
    "Processes a price update."

    def process(self, value: int) -> int:
        "Return one accepted value."
        value = value + 1

        return value
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_crlf_before.py/c2_crlf_before.py",
  "template_id": "python_worker",
  "package_version": "1.0.0",
  "package_fingerprint": "Dy1ZHMQjAFdDnt0J"
}
```

### Physical CRLF after first indentation correction

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `b7a1c03b890831b863f160dd29cf5148920c0c838e22fcccb5312086013ef188`; 289 bytes; terminal sequence "\\n". Receipt `pgmcp://cache/runs/9470787ce4ba4d2588c26343465eb8a0`; package 1.0.0, fingerprint `wnNlUY0mPabVRsbu`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "python_worker",
  "file_name": "c2_crlf_after.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "PriceWorker",
    "operation": {
      "name": "process",
      "description": "Return one accepted value.",
      "async": false,
      "parameters": [
        {
          "name": "value",
          "type": "int"
        }
      ],
      "return_type": "int",
      "body": "\r\n \t\r\nvalue = value + 1\r\n\r\nreturn value\r\n \t\r\n"
    },
    "class_description": "Processes a price update.",
    "module_description": "Processes a price update."
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=python_worker pv=1.0.0 pf=wnNlUY0mPabVRsbu sf=hL6nSzijRu9etOsX

"Processes a price update."


class PriceWorker:
    "Processes a price update."

    def process(self, value: int) -> int:
        "Return one accepted value."
        value = value + 1

        return value
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_crlf_after.py",
  "template_id": "python_worker",
  "package_version": "1.0.0",
  "package_fingerprint": "wnNlUY0mPabVRsbu"
}
```

For the two physical-ending cases, literal encoded outputs also expose retained versus lost endings independently of Markdown rendering:

```json
{
  "before": "# pgmcp:v1 id=python_worker pv=1.0.0 pf=Dy1ZHMQjAFdDnt0J sf=bAu8oCTjP5d0qCGs\n\n\"Processes a price update.\"\n\n\nclass PriceWorker:\n    \"Processes a price update.\"\n\n    def process(self, value: int) -> int:\n        \"Return one accepted value.\"\n        value = value + 1\n\n        return value\n",
  "after": "# pgmcp:v1 id=python_worker pv=1.0.0 pf=wnNlUY0mPabVRsbu sf=hL6nSzijRu9etOsX\n\n\"Processes a price update.\"\n\n\nclass PriceWorker:\n    \"Processes a price update.\"\n\n    def process(self, value: int) -> int:\n        \"Return one accepted value.\"\n        value = value + 1\r\n\r\n        return value\n"
}
```

Native intermediate checks:

```json
{
  "success": true,
  "run_status": "failed",
  "requested_scope": "targets",
  "requested_targets": [
    ".pgmcp/temp/issue473/c2_final_pytest_integration_test_minimal.py",
    ".pgmcp/temp/issue473/c2_final_pytest_integration_test_filled.py",
    ".pgmcp/temp/issue473/c2_final_pytest_unit_test_minimal.py",
    ".pgmcp/temp/issue473/c2_final_pytest_unit_test_filled.py",
    ".pgmcp/temp/issue473/c2_final_python_adapter_minimal.py",
    ".pgmcp/temp/issue473/c2_final_python_adapter_filled.py",
    ".pgmcp/temp/issue473/c2_final_python_class_minimal.py",
    ".pgmcp/temp/issue473/c2_final_python_class_filled.py",
    ".pgmcp/temp/issue473/c2_final_python_protocol_minimal.py",
    ".pgmcp/temp/issue473/c2_final_python_protocol_filled.py",
    ".pgmcp/temp/issue473/c2_final_python_pydantic_config_minimal.py",
    ".pgmcp/temp/issue473/c2_final_python_pydantic_config_filled.py",
    ".pgmcp/temp/issue473/c2_final_python_pydantic_dto_minimal.py",
    ".pgmcp/temp/issue473/c2_final_python_pydantic_dto_filled.py",
    ".pgmcp/temp/issue473/c2_final_python_worker_minimal.py",
    ".pgmcp/temp/issue473/c2_final_python_worker_filled.py"
  ],
  "selected_profile": null,
  "removed_targets": [],
  "results": [
    {
      "check_id": "python_format",
      "status": "failed",
      "reason": null,
      "message": "3 files would be reformatted, 13 files already formatted",
      "evidence": {
        "format": "text",
        "data": "stdout:\n--- .pgmcp\\temp\\issue473\\c2_final_python_adapter_minimal.py\n+++ .pgmcp\\temp\\issue473\\c2_final_python_adapter_minimal.py\n@@ -5,4 +5,5 @@\n \n class PriceAdapter:\n     \"Adapts a price source.\"\n+\n     pass\n\n--- .pgmcp\\temp\\issue473\\c2_final_python_class_minimal.py\n+++ .pgmcp\\temp\\issue473\\c2_final_python_class_minimal.py\n@@ -5,4 +5,5 @@\n \n class PriceCalculator:\n     \"Calculates a notional value.\"\n+\n     pass\n\n--- .pgmcp\\temp\\issue473\\c2_final_python_protocol_minimal.py\n+++ .pgmcp\\temp\\issue473\\c2_final_python_protocol_minimal.py\n@@ -8,4 +8,5 @@\n \n class PriceSource(Protocol):\n     \"Provides price data.\"\n+\n     pass\n\n\nstderr:\n3 files would be reformatted, 13 files already formatted\n"
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
        "fingerprint": "sFWzvJZBN26YRZqa",
        "contract_version": 1
      },
      "capture": {
        "exit_code": 1,
        "stdout": {
          "observed_bytes": 985,
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
      "message": "I001 [*] Import block is un-sorted or un-formatted",
      "evidence": {
        "format": "text",
        "data": "stdout:\nI001 [*] Import block is un-sorted or un-formatted\n --> .pgmcp\\temp\\issue473\\c2_final_pytest_unit_test_filled.py:6:1\n  |\n5 |   # Standard library\n6 | / from pathlib import Path\n7 | |\n8 | | # Third party\n9 | | import pytest\n  | |_____________^\n  |\nhelp: Organize imports\n\nI001 [*] Import block is un-sorted or un-formatted\n --> .pgmcp\\temp\\issue473\\c2_final_python_adapter_filled.py:6:1\n  |\n5 |   # Standard library\n6 | / import logging\n7 | |\n8 | | # Project\n9 | | from market_ports import PriceClient\n  | |____________________________________^\n  |\nhelp: Organize imports\n\nI001 [*] Import block is un-sorted or un-formatted\n --> .pgmcp\\temp\\issue473\\c2_final_python_worker_filled.py:6:1\n  |\n5 |   # Standard library\n6 | / import logging\n7 | |\n8 | | # Project\n9 | | from market_ports import PriceClient\n  | |____________________________________^\n  |\nhelp: Organize imports\n\nFound 3 errors.\n[*] 3 fixable with the `--fix` option.\n"
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
        "fingerprint": "sFWzvJZBN26YRZqa",
        "contract_version": 1
      },
      "capture": {
        "exit_code": 1,
        "stdout": {
          "observed_bytes": 1213,
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

Isolated same-context fix probes (pristine pairs untouched):

```json
{
  "probes": [
    {
      "request": {
        "artifact_type": "python_class",
        "file_name": "c2_fix_probe_format.py",
        "target_path": ".pgmcp/temp/issue473",
        "force_target": true,
        "context": {
          "class_name": "PriceCalculator",
          "class_description": "Calculates a notional value.",
          "module_description": "Calculates a notional value."
        },
        "validation": "enforce"
      },
      "uri": "pgmcp://cache/runs/8147aca4857d49b3a89daef1dedf4f8c",
      "dto": {
        "success": true,
        "written": true,
        "validation_policy": "enforce",
        "validation_status": "passed",
        "profile_id": "python_preflight",
        "checks": [
          {
            "check_id": "python_syntax",
            "status": "passed",
            "reason": null,
            "message": null,
            "evidence": null,
            "request_rejection": null,
            "invocation": {
              "adapter": {
                "adapter_id": "python_syntax",
                "version": "1.0.0",
                "fingerprint": "T9Nk9E_T6kGuq0ed",
                "contract_version": 1
              },
              "capture": {
                "exit_code": 0,
                "stdout": {
                  "observed_bytes": 92,
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
              "external_tools": [
                {
                  "tool_id": "python",
                  "version": "3.13.7"
                }
              ]
            },
            "termination_problem": null,
            "housekeeping": [],
            "args_source": "configured",
            "effective_args": []
          }
        ],
        "error_code": null,
        "error_details": null,
        "housekeeping": [],
        "output_path": ".pgmcp/temp/issue473/c2_fix_probe_format.py",
        "template_id": "python_class",
        "package_version": "1.0.0",
        "package_fingerprint": "nGD0mdL5prLJnb14"
      }
    },
    {
      "request": {
        "artifact_type": "pytest_unit_test",
        "file_name": "c2_fix_probe_lint.py",
        "target_path": ".pgmcp/temp/issue473",
        "force_target": true,
        "context": {
          "description": "Check serialized fixture content.",
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
            ],
            "third_party": [
              {
                "kind": "import",
                "module": "pytest"
              }
            ]
          },
          "markers": [
            "pytest.mark.usefixtures(\"sample_path\")"
          ],
          "fixtures": [
            {
              "name": "sample_path",
              "description": "Write a temporary text file.",
              "async": false,
              "parameters": [
                {
                  "name": "tmp_path",
                  "type": "Path"
                }
              ],
              "return_type": "Path",
              "body": "path = tmp_path / \"sample.txt\"\npath.write_text(\"ready\", encoding=\"utf-8\")\nreturn path",
              "decorator": "pytest.fixture",
              "scope": "function",
              "autouse": false
            }
          ],
          "cases": [
            {
              "name": "test_sample_content",
              "description": "Read the fixture file.",
              "async": false,
              "parameters": [
                {
                  "name": "sample_path",
                  "type": "Path"
                }
              ],
              "body": "assert sample_path.read_text(encoding=\"utf-8\") == \"ready\""
            }
          ]
        },
        "validation": "enforce"
      },
      "uri": "pgmcp://cache/runs/621a03db373d4518a38696c0ed93ac56",
      "dto": {
        "success": true,
        "written": true,
        "validation_policy": "enforce",
        "validation_status": "passed",
        "profile_id": "python_preflight",
        "checks": [
          {
            "check_id": "python_syntax",
            "status": "passed",
            "reason": null,
            "message": null,
            "evidence": null,
            "request_rejection": null,
            "invocation": {
              "adapter": {
                "adapter_id": "python_syntax",
                "version": "1.0.0",
                "fingerprint": "T9Nk9E_T6kGuq0ed",
                "contract_version": 1
              },
              "capture": {
                "exit_code": 0,
                "stdout": {
                  "observed_bytes": 92,
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
              "external_tools": [
                {
                  "tool_id": "python",
                  "version": "3.13.7"
                }
              ]
            },
            "termination_problem": null,
            "housekeeping": [],
            "args_source": "configured",
            "effective_args": []
          }
        ],
        "error_code": null,
        "error_details": null,
        "housekeeping": [],
        "output_path": ".pgmcp/temp/issue473/c2_fix_probe_lint.py",
        "template_id": "pytest_unit_test",
        "package_version": "1.0.0",
        "package_fingerprint": "hLMMuu-e7C4inaNK"
      }
    }
  ],
  "result": {
    "success": true,
    "requested_scope": "targets",
    "requested_targets": [
      ".pgmcp/temp/issue473/c2_fix_probe_format.py",
      ".pgmcp/temp/issue473/c2_fix_probe_lint.py"
    ],
    "selected_fixes": [
      "python_lint",
      "python_format"
    ],
    "results": [
      {
        "fix_id": "python_lint",
        "status": "passed",
        "reason": null,
        "message": null,
        "evidence": {
          "format": "text",
          "data": "Found 1 error (1 fixed, 0 remaining).\n"
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
          "fingerprint": "sFWzvJZBN26YRZqa",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 180,
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
        "effective_args": []
      },
      {
        "fix_id": "python_format",
        "status": "passed",
        "reason": null,
        "message": null,
        "evidence": {
          "format": "text",
          "data": "1 file reformatted, 1 file left unchanged\n"
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
          "fingerprint": "sFWzvJZBN26YRZqa",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 184,
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
        "effective_args": []
      }
    ],
    "error_code": null,
    "error_details": null
  },
  "readback": [
    {
      "content": "# pgmcp:v1 id=python_class pv=1.0.0 pf=nGD0mdL5prLJnb14 sf=hL6nSzijRu9etOsX\n\n\"Calculates a notional value.\"\n\n\nclass PriceCalculator:\n    \"Calculates a notional value.\"\n\n    pass\n",
      "path": ".pgmcp/temp/issue473/c2_fix_probe_format.py"
    },
    {
      "content": "# pgmcp:v1 id=pytest_unit_test pv=1.0.0 pf=hLMMuu-e7C4inaNK sf=hL6nSzijRu9etOsX\n\n\"Check serialized fixture content.\"\n\n# Standard library\nfrom pathlib import Path\n\n# Third party\nimport pytest\n\npytestmark = [pytest.mark.usefixtures(\"sample_path\")]\n\n\n@pytest.fixture(scope=\"function\", autouse=False)\ndef sample_path(tmp_path: Path) -> Path:\n    \"Write a temporary text file.\"\n    path = tmp_path / \"sample.txt\"\n    path.write_text(\"ready\", encoding=\"utf-8\")\n    return path\n\n\ndef test_sample_content(sample_path: Path) -> None:\n    \"Read the fixture file.\"\n    assert sample_path.read_text(encoding=\"utf-8\") == \"ready\"\n",
      "path": ".pgmcp/temp/issue473/c2_fix_probe_lint.py"
    }
  ],
  "recheck": {
    "success": true,
    "run_status": "failed",
    "requested_scope": "targets",
    "requested_targets": [
      ".pgmcp/temp/issue473/c2_mixed_imports.py",
      ".pgmcp/temp/issue473/c2_fix_probe_format.py",
      ".pgmcp/temp/issue473/c2_fix_probe_lint.py"
    ],
    "selected_profile": null,
    "removed_targets": [],
    "results": [
      {
        "check_id": "python_format",
        "status": "passed",
        "reason": null,
        "message": null,
        "evidence": {
          "format": "text",
          "data": "stderr:\n3 files already formatted\n"
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
          "fingerprint": "sFWzvJZBN26YRZqa",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 203,
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
        "message": "I001 [*] Import block is un-sorted or un-formatted",
        "evidence": {
          "format": "text",
          "data": "stdout:\nI001 [*] Import block is un-sorted or un-formatted\n --> .pgmcp\\temp\\issue473\\c2_mixed_imports.py:6:1\n  |\n5 |   # Standard library\n6 | / from enum import Enum\n7 | | import logging\n  | |______________^\n8 |\n9 |   logger = logging.getLogger(__name__)\n  |\nhelp: Organize imports\n\nFound 1 error.\n[*] 1 fixable with the `--fix` option.\n"
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
          "fingerprint": "sFWzvJZBN26YRZqa",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 1,
          "stdout": {
            "observed_bytes": 585,
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
}
```

## C_CODE final first-output pairs

These 18 pristine outputs were scaffolded after all evidenced code corrections. Source-suite identity is `miQevm1LFgWRuTJ9`; package identities below cover their actual reachable templates/schema. Manual findings and limitations are indexed in manual-inspection.md. None was rewritten/fixed after generation.

### C2 final pytest_integration_test minimal

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `6ff4a444e5fce535a04bc3791c647c238f8b1de49b415be52d9445fe53194c89`; 225 bytes; terminal sequence "\n". Receipt `pgmcp://cache/runs/70cd4b38423e41d48a25e45c46640c8e`; package 1.0.0, fingerprint `uPJ3pSfUHtVF7jFS`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "pytest_integration_test",
  "file_name": "c2_verified_pytest_integration_test_minimal.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "description": "Check a rendered integration result.",
    "cases": [
      {
        "name": "test_total",
        "description": "Add two values.",
        "async": false,
        "parameters": [],
        "body": "result = sum([2, 3])\nassert result == 5"
      }
    ]
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=pytest_integration_test pv=1.0.0 pf=uPJ3pSfUHtVF7jFS sf=miQevm1LFgWRuTJ9

"Check a rendered integration result."


def test_total() -> None:
    "Add two values."
    result = sum([2, 3])
    assert result == 5
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_verified_pytest_integration_test_minimal.py",
  "template_id": "pytest_integration_test",
  "package_version": "1.0.0",
  "package_fingerprint": "uPJ3pSfUHtVF7jFS"
}
```

### C2 final pytest_integration_test filled

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `21bf4522663a8184c51e761023f48e55282516c6ae30fb472ca22bd2dd51a56f`; 407 bytes; terminal sequence "\n". Receipt `pgmcp://cache/runs/b6f4320d18574420ab175b07ca3031b5`; package 1.0.0, fingerprint `uPJ3pSfUHtVF7jFS`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "pytest_integration_test",
  "file_name": "c2_verified_pytest_integration_test_filled.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "description": "Check a temporary file round trip.",
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
    "cases": [
      {
        "name": "test_file_round_trip",
        "description": "Write and read a temporary file.",
        "async": false,
        "parameters": [
          {
            "name": "tmp_path",
            "type": "Path"
          }
        ],
        "body": "source = tmp_path / \"input.txt\"\nsource.write_text(\"payload\", encoding=\"utf-8\")\nassert source.read_text(encoding=\"utf-8\") == \"payload\""
      }
    ]
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=pytest_integration_test pv=1.0.0 pf=uPJ3pSfUHtVF7jFS sf=miQevm1LFgWRuTJ9

"Check a temporary file round trip."

# Standard library
from pathlib import Path


def test_file_round_trip(tmp_path: Path) -> None:
    "Write and read a temporary file."
    source = tmp_path / "input.txt"
    source.write_text("payload", encoding="utf-8")
    assert source.read_text(encoding="utf-8") == "payload"
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_verified_pytest_integration_test_filled.py",
  "template_id": "pytest_integration_test",
  "package_version": "1.0.0",
  "package_fingerprint": "uPJ3pSfUHtVF7jFS"
}
```

### C2 final pytest_unit_test minimal

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `c621ab456ecf7ead3996a8a90f4d80f2233f87f7cd5085bfc41a3729ac22462e`; 212 bytes; terminal sequence "\n". Receipt `pgmcp://cache/runs/fc9b54426c9c4603903edb15e1424c27`; package 1.0.0, fingerprint `11emgLdo_Hku-aIQ`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "pytest_unit_test",
  "file_name": "c2_verified_pytest_unit_test_minimal.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "description": "Check a small arithmetic result.",
    "cases": [
      {
        "name": "test_sum",
        "description": "Add two values.",
        "async": false,
        "parameters": [],
        "body": "result = sum([2, 3])\nassert result == 5"
      }
    ]
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=pytest_unit_test pv=1.0.0 pf=11emgLdo_Hku-aIQ sf=miQevm1LFgWRuTJ9

"Check a small arithmetic result."


def test_sum() -> None:
    "Add two values."
    result = sum([2, 3])
    assert result == 5
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_verified_pytest_unit_test_minimal.py",
  "template_id": "pytest_unit_test",
  "package_version": "1.0.0",
  "package_fingerprint": "11emgLdo_Hku-aIQ"
}
```

### C2 final pytest_unit_test filled

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `bbbce5726cbf889abc197adca5b306033dd693ee5b233412da08170253be6a06`; 616 bytes; terminal sequence "\n". Receipt `pgmcp://cache/runs/e6be30dd8d224abfb26657854a073891`; package 1.0.0, fingerprint `11emgLdo_Hku-aIQ`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "pytest_unit_test",
  "file_name": "c2_verified_pytest_unit_test_filled.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "description": "Check serialized fixture content.",
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
      ],
      "third_party": [
        {
          "kind": "import",
          "module": "pytest"
        }
      ]
    },
    "markers": [
      "pytest.mark.usefixtures(\"sample_path\")"
    ],
    "fixtures": [
      {
        "name": "sample_path",
        "description": "Write a temporary text file.",
        "async": false,
        "parameters": [
          {
            "name": "tmp_path",
            "type": "Path"
          }
        ],
        "return_type": "Path",
        "body": "path = tmp_path / \"sample.txt\"\npath.write_text(\"ready\", encoding=\"utf-8\")\nreturn path",
        "decorator": "pytest.fixture",
        "scope": "function",
        "autouse": false
      }
    ],
    "cases": [
      {
        "name": "test_sample_content",
        "description": "Read the fixture file.",
        "async": false,
        "parameters": [
          {
            "name": "sample_path",
            "type": "Path"
          }
        ],
        "body": "assert sample_path.read_text(encoding=\"utf-8\") == \"ready\""
      }
    ]
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=pytest_unit_test pv=1.0.0 pf=11emgLdo_Hku-aIQ sf=miQevm1LFgWRuTJ9

"Check serialized fixture content."

# Standard library
from pathlib import Path

# Third party
import pytest

pytestmark = [pytest.mark.usefixtures("sample_path")]


@pytest.fixture(scope="function", autouse=False)
def sample_path(tmp_path: Path) -> Path:
    "Write a temporary text file."
    path = tmp_path / "sample.txt"
    path.write_text("ready", encoding="utf-8")
    return path


def test_sample_content(sample_path: Path) -> None:
    "Read the fixture file."
    assert sample_path.read_text(encoding="utf-8") == "ready"
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_verified_pytest_unit_test_filled.py",
  "template_id": "pytest_unit_test",
  "package_version": "1.0.0",
  "package_fingerprint": "11emgLdo_Hku-aIQ"
}
```

### C2 final python_adapter minimal

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `60e7051eefd323cecddc437c96121aad2b0eb932774f0876bacb9b885d93621b`; 165 bytes; terminal sequence "\n". Receipt `pgmcp://cache/runs/1c9896e5453d43c1a8f70d559a9437b7`; package 1.0.0, fingerprint `6N8mGmWdBDN9kiMt`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "python_adapter",
  "file_name": "c2_verified_python_adapter_minimal.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "PriceAdapter",
    "class_description": "Adapts a price source.",
    "module_description": "Adapts a price source."
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=python_adapter pv=1.0.0 pf=6N8mGmWdBDN9kiMt sf=miQevm1LFgWRuTJ9

"Adapts a price source."


class PriceAdapter:
    "Adapts a price source."

    pass
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_verified_python_adapter_minimal.py",
  "template_id": "python_adapter",
  "package_version": "1.0.0",
  "package_fingerprint": "6N8mGmWdBDN9kiMt"
}
```

### C2 final python_adapter filled

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `baba17764ebccff4ba56a175b2c00ac3f3878a4bef2567457fe7c87e1f75109a`; 495 bytes; terminal sequence "\n". Receipt `pgmcp://cache/runs/c3d537d88fc64ae6bcc567777ed5580b`; package 1.0.0, fingerprint `6N8mGmWdBDN9kiMt`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "python_adapter",
  "file_name": "c2_verified_python_adapter_filled.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "PriceAdapter",
    "module_description": "Market data adapter.",
    "imports": {
      "project": [
        {
          "kind": "from",
          "module": "market_ports",
          "names": [
            {
              "name": "PriceClient"
            }
          ]
        }
      ]
    },
    "logging": {
      "name": "market.adapter"
    },
    "constructor": {
      "parameters": [
        {
          "name": "client",
          "type": "PriceClient"
        }
      ],
      "body": "self._client = client"
    },
    "methods": [
      {
        "name": "read_price",
        "description": "Return the latest price.",
        "async": false,
        "parameters": [
          {
            "name": "symbol",
            "type": "str"
          }
        ],
        "return_type": "int",
        "body": "return self._client.read_price(symbol)"
      }
    ],
    "class_description": "Adapts a price source."
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=python_adapter pv=1.0.0 pf=6N8mGmWdBDN9kiMt sf=miQevm1LFgWRuTJ9

"Market data adapter."

# Standard library
import logging

# Project
from market_ports import PriceClient

logger = logging.getLogger("market.adapter")


class PriceAdapter:
    "Adapts a price source."

    def __init__(self, client: PriceClient) -> None:
        self._client = client

    def read_price(self, symbol: str) -> int:
        "Return the latest price."
        return self._client.read_price(symbol)
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_verified_python_adapter_filled.py",
  "template_id": "python_adapter",
  "package_version": "1.0.0",
  "package_fingerprint": "6N8mGmWdBDN9kiMt"
}
```

### C2 final python_class minimal

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `6fdada655732a25f7a24b546a82ff19ca1ffe3a9a91abcfff1e6846cf1a971c0`; 178 bytes; terminal sequence "\n". Receipt `pgmcp://cache/runs/5f3fb35e39ba4005b1d10392a1a1945b`; package 1.0.0, fingerprint `L31zRqmDoswXaVMQ`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "python_class",
  "file_name": "c2_verified_python_class_minimal.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "PriceCalculator",
    "class_description": "Calculates a notional value.",
    "module_description": "Calculates a notional value."
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=python_class pv=1.0.0 pf=L31zRqmDoswXaVMQ sf=miQevm1LFgWRuTJ9

"Calculates a notional value."


class PriceCalculator:
    "Calculates a notional value."

    pass
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_verified_python_class_minimal.py",
  "template_id": "python_class",
  "package_version": "1.0.0",
  "package_fingerprint": "L31zRqmDoswXaVMQ"
}
```

### C2 final python_class filled

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `19682d70bcbcd7dc9dcabf764c79f2ad3c21b7f316f18d094c7d66d0a52ea609`; 368 bytes; terminal sequence "\n". Receipt `pgmcp://cache/runs/0e35559140da4ea1a836616ea6f84c35`; package 1.0.0, fingerprint `L31zRqmDoswXaVMQ`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "python_class",
  "file_name": "c2_verified_python_class_filled.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "PriceCalculator",
    "imports": {
      "stdlib": [
        {
          "kind": "from",
          "module": "decimal",
          "names": [
            {
              "name": "Decimal"
            }
          ]
        }
      ]
    },
    "methods": [
      {
        "name": "notional",
        "description": "Multiply quantity by unit price.",
        "async": false,
        "parameters": [
          {
            "name": "quantity",
            "type": "Decimal"
          },
          {
            "name": "unit_price",
            "type": "Decimal"
          }
        ],
        "return_type": "Decimal"
      }
    ],
    "class_description": "Calculates a notional value.",
    "module_description": "Module for PriceCalculator."
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=python_class pv=1.0.0 pf=L31zRqmDoswXaVMQ sf=miQevm1LFgWRuTJ9

"Module for PriceCalculator."

# Standard library
from decimal import Decimal


class PriceCalculator:
    "Calculates a notional value."

    def notional(self, quantity: Decimal, unit_price: Decimal) -> Decimal:
        "Multiply quantity by unit price."
        raise NotImplementedError
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_verified_python_class_filled.py",
  "template_id": "python_class",
  "package_version": "1.0.0",
  "package_fingerprint": "L31zRqmDoswXaVMQ"
}
```

### C2 final python_protocol minimal

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `5ce10e1ff3a87944e5c53b7529e2601fc03532e6895efd7a66cddecccc54674d`; 219 bytes; terminal sequence "\n". Receipt `pgmcp://cache/runs/41abb44a8c6640b3a11d742f10fb7d44`; package 1.0.0, fingerprint `MpC6qp0nvDBiTlPI`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "python_protocol",
  "file_name": "c2_verified_python_protocol_minimal.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "PriceSource",
    "class_description": "Provides price data.",
    "module_description": "Provides price data."
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=python_protocol pv=1.0.0 pf=MpC6qp0nvDBiTlPI sf=miQevm1LFgWRuTJ9

"Provides price data."

# Standard library
from typing import Protocol


class PriceSource(Protocol):
    "Provides price data."

    pass
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_verified_python_protocol_minimal.py",
  "template_id": "python_protocol",
  "package_version": "1.0.0",
  "package_fingerprint": "MpC6qp0nvDBiTlPI"
}
```

### C2 final python_protocol filled

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `11dcf9bf133f9c90af7a8eabdbd8bdd6cfd2a695d3902f1af2fc67852d92b33c`; 406 bytes; terminal sequence "\n". Receipt `pgmcp://cache/runs/5ca307ef0ceb41ee9b1b46b34e4cdc69`; package 1.0.0, fingerprint `MpC6qp0nvDBiTlPI`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "python_protocol",
  "file_name": "c2_verified_python_protocol_filled.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "PriceSource",
    "module_description": "Contract for reading market prices.",
    "methods": [
      {
        "name": "read_price",
        "description": "Return a price for one symbol.",
        "async": false,
        "parameters": [
          {
            "name": "symbol",
            "type": "str"
          }
        ],
        "return_type": "int"
      },
      {
        "name": "close",
        "description": "Release the source resources.",
        "async": false,
        "parameters": [],
        "return_type": "None"
      }
    ],
    "class_description": "Provides price data."
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=python_protocol pv=1.0.0 pf=MpC6qp0nvDBiTlPI sf=miQevm1LFgWRuTJ9

"Contract for reading market prices."

# Standard library
from typing import Protocol


class PriceSource(Protocol):
    "Provides price data."

    def read_price(self, symbol: str) -> int:
        "Return a price for one symbol."
        ...

    def close(self) -> None:
        "Release the source resources."
        ...
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_verified_python_protocol_filled.py",
  "template_id": "python_protocol",
  "package_version": "1.0.0",
  "package_fingerprint": "MpC6qp0nvDBiTlPI"
}
```

### C2 final python_pydantic_config minimal

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `5729d8273ed36f4e3c22d71f5c619cc4b1f1dfc986ae0b1a9088ddb7ce4585f7`; 299 bytes; terminal sequence "\n". Receipt `pgmcp://cache/runs/bfdd300897d74c2a898c1ee583dbce8f`; package 1.0.0, fingerprint `a4L8t8DsfHodDFUk`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "python_pydantic_config",
  "file_name": "c2_verified_python_pydantic_config_minimal.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "RiskSettings",
    "frozen": true,
    "class_description": "Risk settings.",
    "module_description": "Risk settings."
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=python_pydantic_config pv=1.0.0 pf=a4L8t8DsfHodDFUk sf=miQevm1LFgWRuTJ9

"Risk settings."

# Third party
from pydantic import BaseModel, ConfigDict


class RiskSettings(BaseModel):
    "Risk settings."

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_verified_python_pydantic_config_minimal.py",
  "template_id": "python_pydantic_config",
  "package_version": "1.0.0",
  "package_fingerprint": "a4L8t8DsfHodDFUk"
}
```

### C2 final python_pydantic_config filled

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `d804d4ad4a3bb5abbe9068f6b8385f4a0b0216ab0b420229eae7ac1cde8000bf`; 909 bytes; terminal sequence "\n". Receipt `pgmcp://cache/runs/270b7ed221414f09805e4fb2f6835b57`; package 1.0.0, fingerprint `a4L8t8DsfHodDFUk`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "python_pydantic_config",
  "file_name": "c2_verified_python_pydantic_config_filled.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "RiskSettings",
    "module_description": "Risk controls for one strategy.",
    "frozen": false,
    "fields": [
      {
        "name": "enabled",
        "type": "bool",
        "description": "Enable order submission.",
        "default": false
      },
      {
        "name": "max_order_size",
        "type": "int",
        "description": "Maximum permitted order size.",
        "default": 0,
        "ge": 0
      },
      {
        "name": "label",
        "type": "str",
        "description": "Optional operator label.",
        "default": "",
        "min_length": 0
      }
    ],
    "examples": [
      {
        "enabled": true,
        "max_order_size": 5,
        "label": "primary"
      }
    ],
    "class_description": "Risk settings."
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=python_pydantic_config pv=1.0.0 pf=a4L8t8DsfHodDFUk sf=miQevm1LFgWRuTJ9

"Risk controls for one strategy."

# Third party
from pydantic import BaseModel, ConfigDict, Field


class RiskSettings(BaseModel):
    "Risk settings."

    model_config = ConfigDict(
        extra="forbid",
        frozen=False,
        json_schema_extra={
            "examples": [
                {
                    "enabled": True,
                    "max_order_size": 5,
                    "label": "primary",
                },
            ],
        },
    )

    enabled: bool = Field(
        default=False,
        description="Enable order submission.",
    )
    max_order_size: int = Field(
        default=0,
        description="Maximum permitted order size.",
        ge=0,
    )
    label: str = Field(
        default="",
        description="Optional operator label.",
        min_length=0,
    )
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_verified_python_pydantic_config_filled.py",
  "template_id": "python_pydantic_config",
  "package_version": "1.0.0",
  "package_fingerprint": "a4L8t8DsfHodDFUk"
}
```

### C2 final python_pydantic_dto minimal

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `0d52212529bb5c5d8986e329ea74cc3adf97cb430f7fe55852b38cd87b60c5bf`; 303 bytes; terminal sequence "\n". Receipt `pgmcp://cache/runs/7278fb5cf9314db284f5132a1e124ca3`; package 1.0.0, fingerprint `j0XU3OMmFDRe3K-S`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "python_pydantic_dto",
  "file_name": "c2_verified_python_pydantic_dto_minimal.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "PriceSnapshot",
    "class_description": "A price snapshot.",
    "module_description": "A price snapshot."
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=python_pydantic_dto pv=1.0.0 pf=j0XU3OMmFDRe3K-S sf=miQevm1LFgWRuTJ9

"A price snapshot."

# Third party
from pydantic import BaseModel, ConfigDict


class PriceSnapshot(BaseModel):
    "A price snapshot."

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_verified_python_pydantic_dto_minimal.py",
  "template_id": "python_pydantic_dto",
  "package_version": "1.0.0",
  "package_fingerprint": "j0XU3OMmFDRe3K-S"
}
```

### C2 final python_pydantic_dto filled

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `3cf8aefca35aee450fec9cdbbb5cd8b910db36a5f736c4ed1daa6fb198bb0b88`; 863 bytes; terminal sequence "\n". Receipt `pgmcp://cache/runs/db058612ebe04a6895756c0fc3a8456a`; package 1.0.0, fingerprint `j0XU3OMmFDRe3K-S`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "python_pydantic_dto",
  "file_name": "c2_verified_python_pydantic_dto_filled.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "PriceSnapshot",
    "module_description": "Validated market data.",
    "imports": {
      "stdlib": [
        {
          "kind": "import",
          "module": "datetime"
        }
      ]
    },
    "fields": [
      {
        "name": "symbol",
        "type": "str",
        "description": "Instrument identifier.",
        "min_length": 1
      },
      {
        "name": "mid",
        "type": "float",
        "description": "Mid-market price.",
        "gt": 0
      },
      {
        "name": "observed_at",
        "type": "datetime.datetime",
        "description": "Observation time.",
        "default_factory": "datetime.datetime.now"
      }
    ],
    "examples": [
      {
        "symbol": "ABC",
        "mid": 101.25
      }
    ],
    "class_description": "A price snapshot."
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=python_pydantic_dto pv=1.0.0 pf=j0XU3OMmFDRe3K-S sf=miQevm1LFgWRuTJ9

"Validated market data."

# Standard library
import datetime

# Third party
from pydantic import BaseModel, ConfigDict, Field


class PriceSnapshot(BaseModel):
    "A price snapshot."

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        json_schema_extra={
            "examples": [
                {
                    "symbol": "ABC",
                    "mid": 101.25,
                },
            ],
        },
    )

    symbol: str = Field(
        description="Instrument identifier.",
        min_length=1,
    )
    mid: float = Field(
        description="Mid-market price.",
        gt=0,
    )
    observed_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now,
        description="Observation time.",
    )
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_verified_python_pydantic_dto_filled.py",
  "template_id": "python_pydantic_dto",
  "package_version": "1.0.0",
  "package_fingerprint": "j0XU3OMmFDRe3K-S"
}
```

### C2 final python_worker minimal

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `cad40fee56b9289e345d623caeecd4365553c339e45dc024954e49f56862b3ca`; 260 bytes; terminal sequence "\n". Receipt `pgmcp://cache/runs/16a1585ca3c3425588a9c9a5344de521`; package 1.0.0, fingerprint `WNw6udi_l_fdddh8`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "python_worker",
  "file_name": "c2_verified_python_worker_minimal.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "PriceWorker",
    "operation": {
      "name": "process",
      "description": "Return one accepted value.",
      "async": false,
      "parameters": [
        {
          "name": "value",
          "type": "int"
        }
      ],
      "return_type": "int",
      "body": "return value"
    },
    "class_description": "Processes a price update.",
    "module_description": "Processes a price update."
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=python_worker pv=1.0.0 pf=WNw6udi_l_fdddh8 sf=miQevm1LFgWRuTJ9

"Processes a price update."


class PriceWorker:
    "Processes a price update."

    def process(self, value: int) -> int:
        "Return one accepted value."
        return value
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_verified_python_worker_minimal.py",
  "template_id": "python_worker",
  "package_version": "1.0.0",
  "package_fingerprint": "WNw6udi_l_fdddh8"
}
```

### C2 final python_worker filled

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `b1c56d6dacb1b3e542ec842cb12bca9a4f42868621489abc1e328bf2b1b0a9c5`; 515 bytes; terminal sequence "\n". Receipt `pgmcp://cache/runs/377d076bf4e044e18153cf0fa2e5871f`; package 1.0.0, fingerprint `WNw6udi_l_fdddh8`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "python_worker",
  "file_name": "c2_verified_python_worker_filled.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "PriceWorker",
    "imports": {
      "project": [
        {
          "kind": "from",
          "module": "market_ports",
          "names": [
            {
              "name": "PriceClient"
            }
          ]
        }
      ]
    },
    "logging": {
      "name": "market.worker"
    },
    "constructor": {
      "parameters": [
        {
          "name": "client",
          "type": "PriceClient"
        }
      ],
      "body": "self._client = client"
    },
    "operation": {
      "name": "process",
      "description": "Publish the accepted price update.",
      "async": false,
      "parameters": [
        {
          "name": "symbol",
          "type": "str"
        },
        {
          "name": "value",
          "type": "int"
        }
      ],
      "return_type": "None",
      "body": "self._client.publish(symbol, value)"
    },
    "class_description": "Publishes a price update.",
    "module_description": "Module for PriceWorker."
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=python_worker pv=1.0.0 pf=WNw6udi_l_fdddh8 sf=miQevm1LFgWRuTJ9

"Module for PriceWorker."

# Standard library
import logging

# Project
from market_ports import PriceClient

logger = logging.getLogger("market.worker")


class PriceWorker:
    "Publishes a price update."

    def __init__(self, client: PriceClient) -> None:
        self._client = client

    def process(self, symbol: str, value: int) -> None:
        "Publish the accepted price update."
        self._client.publish(symbol, value)
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_verified_python_worker_filled.py",
  "template_id": "python_worker",
  "package_version": "1.0.0",
  "package_fingerprint": "WNw6udi_l_fdddh8"
}
```

### C2 final typescript_dto minimal

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `d83f7a57195f77c44c8772f399299c5fb1ea46d20e3df876978898dcade9d375`; 167 bytes; terminal sequence "\n". Receipt `pgmcp://cache/runs/d1af0b782fe4415598143e43b2dafa5f`; package 1.0.0, fingerprint `EniV0La_ffqYvp3y`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "typescript_dto",
  "file_name": "c2_verified_typescript_dto_minimal.ts",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "PriceSnapshot",
    "class_description": "A price snapshot."
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
// pgmcp:v1 id=typescript_dto pv=1.0.0 pf=EniV0La_ffqYvp3y sf=miQevm1LFgWRuTJ9

/**
 * A price snapshot.
 */
export class PriceSnapshot {
  constructor(data: {}) {}
}
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "typescript_preflight",
  "checks": [
    {
      "check_id": "typescript_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "typescript_syntax",
          "version": "1.0.0",
          "fingerprint": "asfu0uAAuaq6247x",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 95,
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
        "external_tools": [
          {
            "tool_id": "typescript",
            "version": "6.0.3"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_verified_typescript_dto_minimal.ts",
  "template_id": "typescript_dto",
  "package_version": "1.0.0",
  "package_fingerprint": "EniV0La_ffqYvp3y"
}
```

### C2 final typescript_dto filled

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `4edfa54668286761b92057fa2b990219758cdd5a66fb8d101e200df9f2850c26`; 715 bytes; terminal sequence "\n". Receipt `pgmcp://cache/runs/bb901a5be10945dda4cfa7bc3acfa39c`; package 1.0.0, fingerprint `EniV0La_ffqYvp3y`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "typescript_dto",
  "file_name": "c2_verified_typescript_dto_filled.ts",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "context": {
    "class_name": "PriceSnapshot",
    "module_description": "A normalized market price.",
    "imports": [
      "import type { Currency } from './money';"
    ],
    "implements": [
      "PriceRecordContract"
    ],
    "fields": [
      {
        "name": "instrument",
        "type": "string",
        "readonly": true,
        "optional": false,
        "description": "Instrument identifier."
      },
      {
        "name": "currency",
        "type": "Currency",
        "readonly": true,
        "optional": false
      },
      {
        "name": "mid",
        "type": "number",
        "readonly": false,
        "optional": false
      },
      {
        "name": "note",
        "type": "string | null",
        "readonly": false,
        "optional": true
      }
    ],
    "class_description": "A price snapshot."
  },
  "validation": "enforce"
}
```

Complete untouched output:

`````text
// pgmcp:v1 id=typescript_dto pv=1.0.0 pf=EniV0La_ffqYvp3y sf=miQevm1LFgWRuTJ9

/**
 * A normalized market price.
 */

import type { Currency } from './money';

/**
 * A price snapshot.
 */
export class PriceSnapshot implements PriceRecordContract {
  /**
   * Instrument identifier.
   */
  public readonly instrument: string;
  public readonly currency: Currency;
  public mid: number;
  public declare note?: string | null;

  constructor(data: {
    instrument: string;
    currency: Currency;
    mid: number;
    note?: string | null;
  }) {
    this.instrument = data.instrument;
    this.currency = data.currency;
    this.mid = data.mid;

    if ("note" in data) {
      this.note = data.note;
    }
  }
}
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "typescript_preflight",
  "checks": [
    {
      "check_id": "typescript_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "typescript_syntax",
          "version": "1.0.0",
          "fingerprint": "asfu0uAAuaq6247x",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 95,
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
        "external_tools": [
          {
            "tool_id": "typescript",
            "version": "6.0.3"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_verified_typescript_dto_filled.ts",
  "template_id": "typescript_dto",
  "package_version": "1.0.0",
  "package_fingerprint": "EniV0La_ffqYvp3y"
}
```

### C2 boundary ts_empty

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `7214e14fc8f4b911bc296774e7a230b3b26f4c9f62c111b85cb2f7a49a628e97`; 176 bytes; terminal sequence "\n". Receipt `pgmcp://cache/runs/d802a002271b4fd99cd15346248105da`; package 1.0.0, fingerprint `EniV0La_ffqYvp3y`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "typescript_dto",
  "context": {
    "class_name": "PriceSnapshot",
    "class_description": "A price snapshot.",
    "module_description": ""
  },
  "file_name": "c2_boundary_ts_empty.ts",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "validation": "enforce"
}
```

Complete untouched output:

`````text
// pgmcp:v1 id=typescript_dto pv=1.0.0 pf=EniV0La_ffqYvp3y sf=miQevm1LFgWRuTJ9

/**
 */

/**
 * A price snapshot.
 */
export class PriceSnapshot {
  constructor(data: {}) {}
}
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "typescript_preflight",
  "checks": [
    {
      "check_id": "typescript_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "typescript_syntax",
          "version": "1.0.0",
          "fingerprint": "asfu0uAAuaq6247x",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 95,
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
        "external_tools": [
          {
            "tool_id": "typescript",
            "version": "6.0.3"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_boundary_ts_empty.ts",
  "template_id": "typescript_dto",
  "package_version": "1.0.0",
  "package_fingerprint": "EniV0La_ffqYvp3y"
}
```

### C2 boundary ts_whitespace

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `7214e14fc8f4b911bc296774e7a230b3b26f4c9f62c111b85cb2f7a49a628e97`; 176 bytes; terminal sequence "\n". Receipt `pgmcp://cache/runs/454d04cacf1e4039a1041346c7c63d44`; package 1.0.0, fingerprint `EniV0La_ffqYvp3y`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "typescript_dto",
  "context": {
    "class_name": "PriceSnapshot",
    "class_description": "A price snapshot.",
    "module_description": " \t\r\n\t"
  },
  "file_name": "c2_boundary_ts_whitespace.ts",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "validation": "enforce"
}
```

Complete untouched output:

`````text
// pgmcp:v1 id=typescript_dto pv=1.0.0 pf=EniV0La_ffqYvp3y sf=miQevm1LFgWRuTJ9

/**
 */

/**
 * A price snapshot.
 */
export class PriceSnapshot {
  constructor(data: {}) {}
}
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "typescript_preflight",
  "checks": [
    {
      "check_id": "typescript_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "typescript_syntax",
          "version": "1.0.0",
          "fingerprint": "asfu0uAAuaq6247x",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 95,
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
        "external_tools": [
          {
            "tool_id": "typescript",
            "version": "6.0.3"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_boundary_ts_whitespace.ts",
  "template_id": "typescript_dto",
  "package_version": "1.0.0",
  "package_fingerprint": "EniV0La_ffqYvp3y"
}
```

### C2 boundary python_empty

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `ea0734d96d191da1d2097e5614708123a7d754c52617e531d7cc2e257fcea564`; 160 bytes; terminal sequence "\n". Receipt `pgmcp://cache/runs/8b656fc0e0c74090a260e91362f14998`; package 1.0.0, fingerprint `6N8mGmWdBDN9kiMt`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "python_adapter",
  "context": {
    "class_name": "PriceAdapter",
    "class_description": "\r\n  Class text with significant spaces.  \r\n \t\n",
    "module_description": ""
  },
  "file_name": "c2_boundary_python_empty.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=python_adapter pv=1.0.0 pf=6N8mGmWdBDN9kiMt sf=miQevm1LFgWRuTJ9

""


class PriceAdapter:
    "  Class text with significant spaces.  "

    pass
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_boundary_python_empty.py",
  "template_id": "python_adapter",
  "package_version": "1.0.0",
  "package_fingerprint": "6N8mGmWdBDN9kiMt"
}
```

### C2 boundary physical_unicode

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `d9199fef3267b61b69abaf0ccb3a9c32fd3350f7dd4f9f7360917fe49c138b2f`; 293 bytes; terminal sequence "\n". Receipt `pgmcp://cache/runs/4a10e74a969349d5a22b80411858d055`; package 1.0.0, fingerprint `WNw6udi_l_fdddh8`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "python_worker",
  "context": {
    "class_name": "PriceWorker",
    "operation": {
      "name": "process",
      "description": "Return one accepted value.",
      "async": false,
      "parameters": [
        {
          "name": "value",
          "type": "int"
        }
      ],
      "return_type": "int",
      "body": "\r\n\t\r\ntext = \"left right\"\r\n\r\nreturn value\r\n \t\r\n"
    },
    "class_description": "Processes a price update.",
    "module_description": "Processes a price update."
  },
  "file_name": "c2_boundary_physical_unicode.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=python_worker pv=1.0.0 pf=WNw6udi_l_fdddh8 sf=miQevm1LFgWRuTJ9

"Processes a price update."


class PriceWorker:
    "Processes a price update."

    def process(self, value: int) -> int:
        "Return one accepted value."
        text = "left right"

        return value
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_boundary_physical_unicode.py",
  "template_id": "python_worker",
  "package_version": "1.0.0",
  "package_fingerprint": "WNw6udi_l_fdddh8"
}
```

### C2 boundary literals

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `916d2cfac42113b3cb427e232ed9383022842b9284b0c9b34ac0c38bec2c4cfb`; 677 bytes; terminal sequence "\n". Receipt `pgmcp://cache/runs/75f458116eff4e93a1c6e2fc7cf251df`; package 1.0.0, fingerprint `a4L8t8DsfHodDFUk`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "python_pydantic_config",
  "context": {
    "class_name": "RiskSettings",
    "frozen": true,
    "class_description": "Risk settings.",
    "module_description": "Risk settings.",
    "fields": [
      {
        "name": "label",
        "type": "str",
        "description": "Literal label.",
        "default": " \r\nleft right\n "
      },
      {
        "name": "nothing",
        "type": "str | None",
        "description": "None.",
        "default": null
      },
      {
        "name": "enabled",
        "type": "bool",
        "description": "Disabled.",
        "default": false
      },
      {
        "name": "zero",
        "type": "int",
        "description": "Zero.",
        "default": 0
      }
    ]
  },
  "file_name": "c2_boundary_literals.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=python_pydantic_config pv=1.0.0 pf=a4L8t8DsfHodDFUk sf=miQevm1LFgWRuTJ9

"Risk settings."

# Third party
from pydantic import BaseModel, ConfigDict, Field


class RiskSettings(BaseModel):
    "Risk settings."

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    label: str = Field(
        default=" \x0d\x0aleft right\x0a ",
        description="Literal label.",
    )
    nothing: str | None = Field(
        default=None,
        description="None.",
    )
    enabled: bool = Field(
        default=False,
        description="Disabled.",
    )
    zero: int = Field(
        default=0,
        description="Zero.",
    )
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_boundary_literals.py",
  "template_id": "python_pydantic_config",
  "package_version": "1.0.0",
  "package_fingerprint": "a4L8t8DsfHodDFUk"
}
```

### C2 boundary mixed_after

Observation: 2026-10-03; pristine actual output retained. UTF-8 SHA256 `195d5114bf99f047d1e97541407aa1c76e70a99fbdc31be9c76aa44e316aead7`; 263 bytes; terminal sequence "\n". Receipt `pgmcp://cache/runs/921d4c91aecf4346b4446b8d506cb303`; package 1.0.0, fingerprint `6N8mGmWdBDN9kiMt`. First physical line preserves suite identity. Context and file effects below are exact; detailed native rows are included.

Request:

```json
{
  "artifact_type": "python_adapter",
  "context": {
    "class_name": "EnumAdapter",
    "class_description": "Adapts an enumeration.",
    "module_description": "Enumeration adapter.",
    "logging": {},
    "imports": {
      "stdlib": [
        {
          "kind": "from",
          "module": "enum",
          "names": [
            {
              "name": "Enum"
            }
          ]
        }
      ]
    },
    "bases": [
      "Enum"
    ]
  },
  "file_name": "c2_boundary_mixed_after.py",
  "target_path": ".pgmcp/temp/issue473",
  "force_target": true,
  "validation": "enforce"
}
```

Complete untouched output:

`````text
# pgmcp:v1 id=python_adapter pv=1.0.0 pf=6N8mGmWdBDN9kiMt sf=miQevm1LFgWRuTJ9

"Enumeration adapter."

# Standard library
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class EnumAdapter(Enum):
    "Adapts an enumeration."

    pass
`````

Preflight DTO:

```json
{
  "success": true,
  "written": true,
  "validation_policy": "enforce",
  "validation_status": "passed",
  "profile_id": "python_preflight",
  "checks": [
    {
      "check_id": "python_syntax",
      "status": "passed",
      "reason": null,
      "message": null,
      "evidence": null,
      "request_rejection": null,
      "invocation": {
        "adapter": {
          "adapter_id": "python_syntax",
          "version": "1.0.0",
          "fingerprint": "T9Nk9E_T6kGuq0ed",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 92,
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
        "external_tools": [
          {
            "tool_id": "python",
            "version": "3.13.7"
          }
        ]
      },
      "termination_problem": null,
      "housekeeping": [],
      "args_source": "configured",
      "effective_args": []
    }
  ],
  "error_code": null,
  "error_details": null,
  "housekeeping": [],
  "output_path": ".pgmcp/temp/issue473/c2_boundary_mixed_after.py",
  "template_id": "python_adapter",
  "package_version": "1.0.0",
  "package_fingerprint": "6N8mGmWdBDN9kiMt"
}
```

### C2 rejected legacy_rejected

No output written. This proves public clean-break admission at the selected boundary.

```json
{
  "type": "python_class",
  "label": "legacy_rejected",
  "request": {
    "artifact_type": "python_class",
    "context": {
      "class_name": "Legacy",
      "description": "Former ambiguous prose."
    },
    "file_name": "c2_boundary_legacy_rejected.py",
    "target_path": ".pgmcp/temp/issue473",
    "force_target": true,
    "validation": "enforce"
  },
  "uri": "pgmcp://cache/runs/695aba0ae1c44956a9a1c39181258f72",
  "dto": {
    "success": false,
    "written": false,
    "validation_policy": "enforce",
    "validation_status": "not_executed",
    "profile_id": "python_preflight",
    "checks": [],
    "error_code": "context_invalid",
    "error_details": {
      "issues": [
        {
          "pointer": "",
          "keyword": "additionalProperties",
          "message": "Additional properties are not allowed ('description' was unexpected)"
        }
      ]
    },
    "housekeeping": [],
    "output_path": ".pgmcp/temp/issue473/c2_boundary_legacy_rejected.py",
    "template_id": "python_class",
    "package_version": "1.0.0",
    "package_fingerprint": "L31zRqmDoswXaVMQ"
  }
}
```

### C2 rejected module_missing

No output written. This proves public clean-break admission at the selected boundary.

```json
{
  "type": "python_class",
  "label": "module_missing",
  "request": {
    "artifact_type": "python_class",
    "context": {
      "class_name": "MissingModule",
      "class_description": "Class only."
    },
    "file_name": "c2_boundary_module_missing.py",
    "target_path": ".pgmcp/temp/issue473",
    "force_target": true,
    "validation": "enforce"
  },
  "uri": "pgmcp://cache/runs/aa6b8db7d1ca4d21ae543c5ec8aa4c81",
  "dto": {
    "success": false,
    "written": false,
    "validation_policy": "enforce",
    "validation_status": "not_executed",
    "profile_id": "python_preflight",
    "checks": [],
    "error_code": "context_invalid",
    "error_details": {
      "issues": [
        {
          "pointer": "",
          "keyword": "required",
          "message": "'module_description' is a required property"
        }
      ]
    },
    "housekeeping": [],
    "output_path": ".pgmcp/temp/issue473/c2_boundary_module_missing.py",
    "template_id": "python_class",
    "package_version": "1.0.0",
    "package_fingerprint": "L31zRqmDoswXaVMQ"
  }
}
```

Complete final native gate/test DTOs:

```json
{
  "pristine": {
    "request": {
      "scope": "targets",
      "targets": [
        ".pgmcp/temp/issue473/c2_verified_pytest_integration_test_minimal.py",
        ".pgmcp/temp/issue473/c2_verified_pytest_integration_test_filled.py",
        ".pgmcp/temp/issue473/c2_verified_pytest_unit_test_minimal.py",
        ".pgmcp/temp/issue473/c2_verified_pytest_unit_test_filled.py",
        ".pgmcp/temp/issue473/c2_verified_python_adapter_minimal.py",
        ".pgmcp/temp/issue473/c2_verified_python_adapter_filled.py",
        ".pgmcp/temp/issue473/c2_verified_python_class_minimal.py",
        ".pgmcp/temp/issue473/c2_verified_python_class_filled.py",
        ".pgmcp/temp/issue473/c2_verified_python_protocol_minimal.py",
        ".pgmcp/temp/issue473/c2_verified_python_protocol_filled.py",
        ".pgmcp/temp/issue473/c2_verified_python_pydantic_config_minimal.py",
        ".pgmcp/temp/issue473/c2_verified_python_pydantic_config_filled.py",
        ".pgmcp/temp/issue473/c2_verified_python_pydantic_dto_minimal.py",
        ".pgmcp/temp/issue473/c2_verified_python_pydantic_dto_filled.py",
        ".pgmcp/temp/issue473/c2_verified_python_worker_minimal.py",
        ".pgmcp/temp/issue473/c2_verified_python_worker_filled.py",
        ".pgmcp/temp/issue473/c2_boundary_mixed_after.py"
      ],
      "checks": [
        "python_format",
        "python_lint"
      ]
    },
    "uri": "pgmcp://cache/runs/347c4a8c62c34230b4515b363cd09c9d",
    "dto": {
      "success": true,
      "run_status": "passed",
      "requested_scope": "targets",
      "requested_targets": [
        ".pgmcp/temp/issue473/c2_verified_pytest_integration_test_minimal.py",
        ".pgmcp/temp/issue473/c2_verified_pytest_integration_test_filled.py",
        ".pgmcp/temp/issue473/c2_verified_pytest_unit_test_minimal.py",
        ".pgmcp/temp/issue473/c2_verified_pytest_unit_test_filled.py",
        ".pgmcp/temp/issue473/c2_verified_python_adapter_minimal.py",
        ".pgmcp/temp/issue473/c2_verified_python_adapter_filled.py",
        ".pgmcp/temp/issue473/c2_verified_python_class_minimal.py",
        ".pgmcp/temp/issue473/c2_verified_python_class_filled.py",
        ".pgmcp/temp/issue473/c2_verified_python_protocol_minimal.py",
        ".pgmcp/temp/issue473/c2_verified_python_protocol_filled.py",
        ".pgmcp/temp/issue473/c2_verified_python_pydantic_config_minimal.py",
        ".pgmcp/temp/issue473/c2_verified_python_pydantic_config_filled.py",
        ".pgmcp/temp/issue473/c2_verified_python_pydantic_dto_minimal.py",
        ".pgmcp/temp/issue473/c2_verified_python_pydantic_dto_filled.py",
        ".pgmcp/temp/issue473/c2_verified_python_worker_minimal.py",
        ".pgmcp/temp/issue473/c2_verified_python_worker_filled.py",
        ".pgmcp/temp/issue473/c2_boundary_mixed_after.py"
      ],
      "selected_profile": null,
      "removed_targets": [],
      "results": [
        {
          "check_id": "python_format",
          "status": "passed",
          "reason": null,
          "message": null,
          "evidence": {
            "format": "text",
            "data": "stderr:\n17 files already formatted\n"
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
            "fingerprint": "sFWzvJZBN26YRZqa",
            "contract_version": 1
          },
          "capture": {
            "exit_code": 0,
            "stdout": {
              "observed_bytes": 204,
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
          "status": "passed",
          "reason": null,
          "message": null,
          "evidence": {
            "format": "text",
            "data": "stdout:\nAll checks passed!\n"
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
            "fingerprint": "sFWzvJZBN26YRZqa",
            "contract_version": 1
          },
          "capture": {
            "exit_code": 0,
            "stdout": {
              "observed_bytes": 196,
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
  },
  "testSet": {
    "uri": "pgmcp://cache/runs/197fb04a662940c8bd50ba2c6ccd3f8b",
    "request": {
      "scope": "targets",
      "targets": [
        "tests/mcp_server/integration/templates/test_python_class.py",
        "tests/mcp_server/integration/templates/test_python_protocol.py",
        "tests/mcp_server/integration/templates/test_python_pydantic_config.py",
        "tests/mcp_server/integration/templates/test_python_pydantic_dto.py",
        "tests/mcp_server/integration/templates/test_python_adapter.py",
        "tests/mcp_server/integration/templates/test_python_worker.py",
        "tests/mcp_server/integration/templates/test_pytest_unit_test.py",
        "tests/mcp_server/integration/templates/test_pytest_integration_test.py",
        "tests/mcp_server/integration/templates/test_typescript_artifact.py",
        "tests/mcp_server/integration/templates/test_shared_python.py"
      ],
      "tests": [
        "python_tests"
      ],
      "args": {
        "python_tests": [
          "-q",
          "-n",
          "0",
          "--tb=no",
          "-rN"
        ]
      },
      "timeout_seconds": 120
    },
    "dto": {
      "success": true,
      "requested_scope": "targets",
      "requested_targets": [
        "tests/mcp_server/integration/templates/test_python_class.py",
        "tests/mcp_server/integration/templates/test_python_protocol.py",
        "tests/mcp_server/integration/templates/test_python_pydantic_config.py",
        "tests/mcp_server/integration/templates/test_python_pydantic_dto.py",
        "tests/mcp_server/integration/templates/test_python_adapter.py",
        "tests/mcp_server/integration/templates/test_python_worker.py",
        "tests/mcp_server/integration/templates/test_pytest_unit_test.py",
        "tests/mcp_server/integration/templates/test_pytest_integration_test.py",
        "tests/mcp_server/integration/templates/test_typescript_artifact.py",
        "tests/mcp_server/integration/templates/test_shared_python.py"
      ],
      "selected_tests": [
        "python_tests"
      ],
      "results": [
        {
          "test_id": "python_tests",
          "status": "failed",
          "reason": null,
          "message": "Pytest reported a negative native result (exit 1).",
          "evidence": {
            "format": "text",
            "data": "============================= test session starts =============================\r\nplatform win32 -- Python 3.13.7, pytest-9.0.2, pluggy-1.6.0\r\nrootdir: C:\\temp\\pgmcp\r\nconfigfile: pyproject.toml\r\nplugins: anyio-4.12.1, asyncio-1.3.0, cov-7.0.0, xdist-3.8.0\r\nasyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function\r\ncollected 53 items\r\n\r\ntests\\mcp_server\\integration\\templates\\test_python_class.py ....         [  7%]\r\ntests\\mcp_server\\integration\\templates\\test_python_protocol.py ....      [ 15%]\r\ntests\\mcp_server\\integration\\templates\\test_python_pydantic_config.py .. [ 18%]\r\n....                                                                     [ 26%]\r\ntests\\mcp_server\\integration\\templates\\test_python_pydantic_dto.py ..... [ 35%]\r\n.                                                                        [ 37%]\r\ntests\\mcp_server\\integration\\templates\\test_python_adapter.py .....      [ 47%]\r\ntests\\mcp_server\\integration\\templates\\test_python_worker.py .....       [ 56%]\r\ntests\\mcp_server\\integration\\templates\\test_pytest_unit_test.py .....    [ 66%]\r\ntests\\mcp_server\\integration\\templates\\test_pytest_integration_test.py . [ 67%]\r\nF...                                                                     [ 75%]\r\ntests\\mcp_server\\integration\\templates\\test_typescript_artifact.py ....  [ 83%]\r\ntests\\mcp_server\\integration\\templates\\test_shared_python.py .........   [100%]\r\n\r\n============================== warnings summary ===============================\r\n..\\..\\Users\\miche\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\pydantic\\_internal\\_fields.py:198\r\n  C:\\Users\\miche\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\pydantic\\_internal\\_fields.py:198: UserWarning: Field name \"schema\" in \"SchemaAttachment\" shadows an attribute in parent \"BaseModel\"\r\n    warnings.warn(\r\n\r\n-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html\r\n================== 1 failed, 52 passed, 1 warning in 33.72s ===================\r\n"
          },
          "external_tools": [
            {
              "tool_id": "pytest",
              "version": "9.0.2"
            }
          ],
          "adapter": {
            "adapter_id": "pytest",
            "version": "1.0.0",
            "fingerprint": "m2Mk3Lc50xWA3fi5",
            "contract_version": 1
          },
          "capture": {
            "exit_code": 1,
            "stdout": {
              "observed_bytes": 2371,
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
          "args_source": "caller",
          "effective_args": [
            "-q",
            "-n",
            "0",
            "--tb=no",
            "-rN"
          ]
        }
      ],
      "error_code": null,
      "error_details": null
    }
  },
  "integrationClosure": {
    "request": {
      "scope": "targets",
      "targets": [
        "tests/mcp_server/integration/templates/test_pytest_integration_test.py"
      ],
      "tests": [
        "python_tests"
      ],
      "args": {
        "python_tests": [
          "-q",
          "-n",
          "0",
          "--tb=short",
          "-rN"
        ]
      },
      "timeout_seconds": 90
    },
    "uri": "pgmcp://cache/runs/dc4b351972b4429ca5824d8341e6955d",
    "dto": {
      "success": true,
      "requested_scope": "targets",
      "requested_targets": [
        "tests/mcp_server/integration/templates/test_pytest_integration_test.py"
      ],
      "selected_tests": [
        "python_tests"
      ],
      "results": [
        {
          "test_id": "python_tests",
          "status": "passed",
          "reason": null,
          "message": "Pytest completed the requested native operation (exit 0).",
          "evidence": {
            "format": "text",
            "data": "============================= test session starts =============================\r\nplatform win32 -- Python 3.13.7, pytest-9.0.2, pluggy-1.6.0\r\nrootdir: C:\\temp\\pgmcp\r\nconfigfile: pyproject.toml\r\nplugins: anyio-4.12.1, asyncio-1.3.0, cov-7.0.0, xdist-3.8.0\r\nasyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function\r\ncollected 5 items\r\n\r\ntests\\mcp_server\\integration\\templates\\test_pytest_integration_test.py . [ 20%]\r\n....                                                                     [100%]\r\n\r\n============================== warnings summary ===============================\r\n..\\..\\Users\\miche\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\pydantic\\_internal\\_fields.py:198\r\n  C:\\Users\\miche\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\pydantic\\_internal\\_fields.py:198: UserWarning: Field name \"schema\" in \"SchemaAttachment\" shadows an attribute in parent \"BaseModel\"\r\n    warnings.warn(\r\n\r\n-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html\r\n======================== 5 passed, 1 warning in 4.27s =========================\r\n"
          },
          "external_tools": [
            {
              "tool_id": "pytest",
              "version": "9.0.2"
            }
          ],
          "adapter": {
            "adapter_id": "pytest",
            "version": "1.0.0",
            "fingerprint": "m2Mk3Lc50xWA3fi5",
            "contract_version": 1
          },
          "capture": {
            "exit_code": 0,
            "stdout": {
              "observed_bytes": 1428,
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
          "args_source": "caller",
          "effective_args": [
            "-q",
            "-n",
            "0",
            "--tb=short",
            "-rN"
          ]
        }
      ],
      "error_code": null,
      "error_details": null
    }
  },
  "integrationGate": {
    "uri": "pgmcp://cache/runs/54de446a941043779391899059e8b62a",
    "dto": {
      "success": true,
      "run_status": "passed",
      "requested_scope": "targets",
      "requested_targets": [
        "tests/mcp_server/integration/templates/test_pytest_integration_test.py"
      ],
      "selected_profile": null,
      "removed_targets": [],
      "results": [
        {
          "check_id": "python_format",
          "status": "passed",
          "reason": null,
          "message": null,
          "evidence": {
            "format": "text",
            "data": "stderr:\n1 file already formatted\n"
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
            "fingerprint": "sFWzvJZBN26YRZqa",
            "contract_version": 1
          },
          "capture": {
            "exit_code": 0,
            "stdout": {
              "observed_bytes": 202,
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
          "status": "passed",
          "reason": null,
          "message": null,
          "evidence": {
            "format": "text",
            "data": "stdout:\nAll checks passed!\n"
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
            "fingerprint": "sFWzvJZBN26YRZqa",
            "contract_version": 1
          },
          "capture": {
            "exit_code": 0,
            "stdout": {
              "observed_bytes": 196,
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
          "check_id": "python_pyright",
          "status": "passed",
          "reason": null,
          "message": null,
          "evidence": {
            "format": "text",
            "data": "stdout:\n{\n    \"version\": \"1.1.408\",\n    \"time\": \"1791053308481\",\n    \"generalDiagnostics\": [],\n    \"summary\": {\n        \"filesAnalyzed\": 1,\n        \"errorCount\": 0,\n        \"warningCount\": 0,\n        \"informationCount\": 0,\n        \"timeInSec\": 1.326\n    }\n}\n\n"
          },
          "external_tools": [
            {
              "tool_id": "pyright",
              "version": "1.1.408"
            }
          ],
          "adapter": {
            "adapter_id": "pyright",
            "version": "1.0.0",
            "fingerprint": "GfhwbqXxleu1yBzE",
            "contract_version": 1
          },
          "capture": {
            "exit_code": 0,
            "stdout": {
              "observed_bytes": 466,
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
          "effective_args": [
            "--level",
            "warning",
            "--warnings"
          ],
          "coverage": null,
          "required_targets": []
        }
      ],
      "error_code": null,
      "error_details": null
    }
  },
  "sharedFixtureGate": {
    "success": true,
    "run_status": "passed",
    "requested_scope": "targets",
    "requested_targets": [
      "tests/mcp_server/integration/templates/test_shared_python.py"
    ],
    "selected_profile": null,
    "removed_targets": [],
    "results": [
      {
        "check_id": "python_format",
        "status": "passed",
        "reason": null,
        "message": null,
        "evidence": {
          "format": "text",
          "data": "stderr:\n1 file already formatted\n"
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
          "fingerprint": "sFWzvJZBN26YRZqa",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 202,
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
        "status": "passed",
        "reason": null,
        "message": null,
        "evidence": {
          "format": "text",
          "data": "stdout:\nAll checks passed!\n"
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
          "fingerprint": "sFWzvJZBN26YRZqa",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 196,
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
        "check_id": "python_pyright",
        "status": "passed",
        "reason": null,
        "message": null,
        "evidence": {
          "format": "text",
          "data": "stdout:\n{\n    \"version\": \"1.1.408\",\n    \"time\": \"1791052845758\",\n    \"generalDiagnostics\": [],\n    \"summary\": {\n        \"filesAnalyzed\": 1,\n        \"errorCount\": 0,\n        \"warningCount\": 0,\n        \"informationCount\": 0,\n        \"timeInSec\": 1.759\n    }\n}\n\n"
        },
        "external_tools": [
          {
            "tool_id": "pyright",
            "version": "1.1.408"
          }
        ],
        "adapter": {
          "adapter_id": "pyright",
          "version": "1.0.0",
          "fingerprint": "GfhwbqXxleu1yBzE",
          "contract_version": 1
        },
        "capture": {
          "exit_code": 0,
          "stdout": {
            "observed_bytes": 466,
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
        "effective_args": [
          "--level",
          "warning",
          "--warnings"
        ],
        "coverage": null,
        "required_targets": []
      }
    ],
    "error_code": null,
    "error_details": null
  }
}
```
