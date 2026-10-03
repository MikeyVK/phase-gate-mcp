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

