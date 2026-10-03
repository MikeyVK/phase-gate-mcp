<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=QEtFztWtFehT8R5U sf=9PfER5JkyAoFQLRi -->

# Issue 473 First-output Survey Evidence

**Status:** RESEARCH — strategy approval pending  
**Version:** 0.1  
**Last updated:** 2026-10-02

Preserve exact replay inputs, source identities, first-output measurements and decisive native observations.

All 19 shipped concrete packages were exercised with minimal and representative filled context. This evidence index records observations without approving a correction strategy.

[Research and strategy decision](research.md)

## Survey protocol

Observed on 2026-10-02 in initialized Research branch `bug/473-first-call-template-quality`; source suite `.pgmcp/template_suite/`. Every accepted context was rendered once through `scaffold_artifact`, with no subsequent source edits or `apply_fixes`. Source suite identity in the generated headers: `sf=9PfER5JkyAoFQLRi`.

There are 19 direct concrete packages and 38 accepted first outputs. The shared support directory is not a concrete artifact. The [release manifest](../../../.pgmcp/config/release_manifest.yaml) copies the complete source suite into shipped assets; this survey exercises the live source catalog, not an assembled release wheel.

Use each `minimal` or `filled` object below as `context`. Call:

```json
{
  "artifact_type": "<package>",
  "file_name": "<package>.<minimal-or-filled>.<extension>",
  "context": "<the corresponding object below, not this placeholder string>",
  "target_path": ".pgmcp/temp/issue473-survey",
  "force_target": true,
  "validation": "report"
}
```

Extension: `py` for the eight Python packages, `ts` for TypeScript, `txt` for commit, and `md` for the nine Markdown packages. Choose a fresh survey directory for replay because scaffold is create-only. Relative document links in these inputs assume a directory three levels below the workspace root; adjust caller paths if replaying at another depth. Report mode is an observation policy for this investigation: it preserves native failed/unavailable facts, and was not a change to product enforcement.

One rejected preparation call preceded the accepted TypeScript filled render: the supplied field name `symbol` is excluded by the current schema's contextual-keyword list. Receipt `pgmcp://cache/runs/ae3023466faf45dd91cf7754d51f5345` returned `context_invalid`, `written=false`. The valid sample uses `instrument`. This was a caller-context mistake, not a generated-output defect; it is excluded from the 38 outputs.

Counts below include a whitespace-only line as blank and exclude the final zero-length split element caused by the terminal LF. Maximum run includes trailing blank lines; trailing blank lines are reported separately. These measures are observations, not the proposed acceptance contract.

| Package | Variant | Preflight | Lines | Maximum blank run | Trailing blank lines | SHA-256 |
| --- | --- | --- | ---: | ---: | ---: | --- |
| architecture | minimal | passed | 24 | 8 | 8 | `c397da5adc15400389c3ac17a0f6b20d84370dc7049ff198f6c8da85c1d44ecd` |
| architecture | filled | passed | 76 | 5 | 1 | `df46ccf8012f4397d669f57e9dfc08aaa56a80451b61fd417676b3a6e794437f` |
| commit | minimal | unavailable | 5 | 2 | 2 | `55f1761d484042c7176109d0214e6756c49fae050d5755e841d3926069988910` |
| commit | filled | unavailable | 15 | 2 | 2 | `68a77cd959414766cee1d942491afdb1a890601e233b41bb0f296b26bb6b7ccc` |
| design | minimal | passed | 39 | 20 | 20 | `b66139975fa1547744aa97c1c99eab211b5889373bd969b379f92fc1db56d31c` |
| design | filled | passed | 114 | 11 | 8 | `c2be4a7f91273d80019127f1c17a3a8cfa3eaee8220ec0a26ea47bc0ce6321ef` |
| generic_doc | minimal | passed | 23 | 8 | 8 | `a30b90120872743b8a60b76a87de7732153680f89ffd9fb53ef7e0e996733e95` |
| generic_doc | filled | passed | 81 | 7 | 1 | `bd9b9de85f092047e2e2e4f0e50de8e7545e092713a413c52d601475007c538e` |
| issue | minimal | passed | 14 | 8 | 8 | `984e6c0edeed40b3a9cef85c3716641c6c9c45c8fef4927dc7af4bbda9540c9f` |
| issue | filled | passed | 46 | 4 | 1 | `f4c1a6256a90fd318145a38c227c25bdf9ca49906675b1e960f15b2dd89817b0` |
| planning | minimal | passed | 46 | 10 | 10 | `427f3b9f8a1ceba3e62f51835fa50c8365558ee1da9b99cfab4e4e58d557a949` |
| planning | filled | passed | 127 | 13 | 13 | `52d2d2f9a91471ecfab92d4867cbdfa50a713d33810fc1f422627368772b2c12` |
| pr | minimal | passed | 20 | 5 | 5 | `a9a8d000fd397e472088b3fed0a7d2221e6d1ab96fa82f99145c622176f654f3` |
| pr | filled | passed | 56 | 5 | 4 | `3f72b5819a96af436fdfe0cb673c2e78dbae5fe7dcecc84ef0651f199ae10fb3` |
| pytest_integration_test | minimal | passed | 15 | 5 | 3 | `4a424715f8cefe8f0b16c90628eccfacd3a5c016c4d3c3d615da24bd6c16e5e4` |
| pytest_integration_test | filled | passed | 19 | 5 | 3 | `b9695e5d94812327baa9453133630ed45854ba1af1f37effd5b5d051ff4d1adc` |
| pytest_unit_test | minimal | passed | 15 | 5 | 3 | `7c88e587df1bdeb914a02257f41a4923e3a792e4f925f1837b5e47b13be7bfb4` |
| pytest_unit_test | filled | passed | 28 | 3 | 3 | `2219a7ceb1435ed9313a1dffe8986fb66079071ccb992760209a311f38e37227` |
| python_adapter | minimal | passed | 16 | 5 | 2 | `8b9e724fe4571c037457e9f6838b0d363ae8efabfe8a4a1123f806d7152401d9` |
| python_adapter | filled | passed | 30 | 4 | 3 | `9e9c1002268d8280433ae210285e8249eb0a7f5404b1d61e95089b130e672e6e` |
| python_class | minimal | passed | 11 | 2 | 2 | `e73e164041ba637b66dbe6ae48517e6370f9ed866c1505fefaf57f30b194c0f3` |
| python_class | filled | passed | 16 | 2 | 2 | `4cf11dafbc36292b1dafeb43e903cd04b97b2c9588ce5ff8f5aaa9c6a12be551` |
| python_protocol | minimal | passed | 16 | 3 | 2 | `cfa3a7443a096ca9e7bf231b7869813fa98715eea36b6a031f8b1de760f4ac4b` |
| python_protocol | filled | passed | 22 | 3 | 2 | `4b3a9256073a93cc41dc7f5c260652f64a67b5d32d18ff57ba83f09e01db7983` |
| python_pydantic_config | minimal | passed | 18 | 4 | 2 | `4c16609539b813e6ab583c40e108c7c26cdc539e46cf3a4d431b1c78965ee21f` |
| python_pydantic_config | filled | passed | 21 | 4 | 2 | `f501b7eda3e79fcad545bb65476cf0fb4f21a38df44e5bad826d629ecef61aab` |
| python_pydantic_dto | minimal | passed | 18 | 4 | 2 | `4caafa43388bd02a622927bb5e9ea7f6e93cef600fb9a880df9a42fe651e06c7` |
| python_pydantic_dto | filled | passed | 24 | 4 | 2 | `d59202a33d7ae2ca91f13ae2b9f7665a29b1455a5f6ee06d2a135a1afe8445ef` |
| python_worker | minimal | passed | 15 | 5 | 1 | `bfe07c8a73bdbb11fc1052a5d53fba59f7ecedd0ea4f8ffce664c81dfc020a5f` |
| python_worker | filled | passed | 27 | 4 | 1 | `63ba23aea0003bae0b1abbef2491c9936b48665ee14fc824090627e353f76d1f` |
| reference | minimal | passed | 21 | 5 | 5 | `4d9b3a6db0c3374540a743b6ad732083752e736fb1e2d1056c1bbfd184d8f956` |
| reference | filled | passed | 82 | 6 | 5 | `7af78ebb8bb07aef52b3ccac7f7920dbc4fc7d8f78c1927972cf4f8a947f63cd` |
| research | minimal | passed | 29 | 14 | 14 | `09d949ef324097e3613fd7bc9ad2b63a52c18ef5638b355a83c7235eeeff6e3e` |
| research | filled | passed | 104 | 5 | 4 | `e368ee845068e4525fa1bccdb27a6c6451a967b49d9591cdd78960252a0d0d6c` |
| typescript_dto | minimal | unavailable | 17 | 2 | 1 | `1b6c2b3c9242615d061acace7777a122c2a406a36b089f9854523df65d170721` |
| typescript_dto | filled | unavailable | 45 | 2 | 1 | `09e3d178fa9e001a601d461a8f497507a0ff8e0fcdc0c0ecc717be03be6db8e6` |
| validation_report | minimal | passed | 24 | 21 | 21 | `0b6e98ddd6e637c961134cf29fd2b6ed4d483dff9200c917455e87c3ad84e029` |
| validation_report | filled | passed | 93 | 8 | 6 | `64b0ae6b95fcdf3f0dba5066cf08a34051751525cbc1303b59cea7a60fecd9f0` |

## Exact inputs and source identities

Minimal uses only required properties, including required nested properties. Filled exercises optional/nested carriers with modest descriptions and normally formatted bodies; it is representative, not exhaustive. Research/validation status and evidence in the illustrative contexts are caller-authored samples and do not assert an actual workflow result. Python adapter/worker imports and TypeScript interfaces are illustrative dependencies, so syntax checks cannot prove import resolution or execution.

### architecture

Version: 1.0.0; package fingerprint: `hlDXMID07Yn0gQ03`.

```json
{
  "minimal": {
    "title": "Execution Architecture",
    "concepts": [
      {
        "name": "Event stream",
        "description": "Events move from intake to persistence."
      }
    ]
  },
  "filled": {
    "title": "Execution Architecture",
    "status": "DRAFT — review pending",
    "version": "1.0",
    "last_updated": "2026-10-02",
    "purpose": "Describe the order-preserving event path.",
    "related_docs": [
      {
        "label": "Design",
        "target": "../../../docs/coding_standards/DOCUMENTATION_STANDARD.md"
      }
    ],
    "concepts": [
      {
        "name": "Event stream",
        "description": "Events move from intake to persistence.",
        "diagram": "flowchart LR\n  Intake --> Journal\n  Journal --> Store",
        "subsections": [
          {
            "name": "Ordering",
            "description": "Each partition preserves append order."
          }
        ]
      }
    ],
    "constraints": [
      "Never acknowledge before durable append."
    ],
    "decisions": [
      {
        "decision": "Use a durable journal",
        "rationale": "Recovery needs an authoritative append order.",
        "alternatives": [
          "In-memory queue"
        ]
      }
    ],
    "sources": [
      {
        "label": "Journal contract",
        "target": "../../../docs/coding_standards/ARCHITECTURE_PRINCIPLES.md"
      }
    ]
  }
}
```

Scaffold receipts: minimal: `pgmcp://cache/runs/4fe3eb7e99ad4f949d0baa8dc095d324`; filled: `pgmcp://cache/runs/0ae98baeb67d4fc994671a68c3249003`.

### commit

Version: 1.0.0; package fingerprint: `_Yga89XCROsHUBlO`.

```json
{
  "minimal": {
    "type": "fix",
    "subject": "Keep caller intent"
  },
  "filled": {
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
  }
}
```

Scaffold receipts: minimal: `pgmcp://cache/runs/cc6ca692e6f642849e16c604eeabfbbe`; filled: `pgmcp://cache/runs/536498e6b2d8468b9680015890181d58`.

### design

Version: 1.0.0; package fingerprint: `WCiT2npbapCBexKy`.

```json
{
  "minimal": {
    "title": "Event Path Design",
    "problem_statement": "The consumer can acknowledge an event before its journal append is durable.",
    "requirements_functional": [
      "Acknowledge only after durable append."
    ],
    "requirements_nonfunctional": [
      "Preserve per-partition order."
    ]
  },
  "filled": {
    "title": "Event Path Design",
    "status": "DRAFT — review pending",
    "problem_statement": "The consumer can acknowledge an event before its journal append is durable.",
    "requirements_functional": [
      "Acknowledge only after durable append."
    ],
    "requirements_nonfunctional": [
      "Preserve per-partition order."
    ],
    "options": [
      {
        "name": "Append then acknowledge",
        "description": "Commit to the journal before replying.",
        "pros": [
          "Crash recovery has a durable source."
        ],
        "cons": [
          "Adds append latency."
        ]
      }
    ],
    "decision": "Append before acknowledgement.",
    "rationale": "The durability requirement determines the ordering.",
    "contracts": [
      {
        "heading": "Append result",
        "content": "Returns an explicit durable position."
      }
    ],
    "validation": [
      {
        "obligation": "A failed append is not acknowledged",
        "method": "Inject journal failure",
        "expected_result": "The call fails and no acknowledgement is sent.",
        "references": [
          {
            "label": "Journal contract",
            "target": "../../../docs/coding_standards/ARCHITECTURE_PRINCIPLES.md"
          }
        ]
      }
    ],
    "risks": [
      {
        "description": "Append latency increases.",
        "mitigation": "Measure the journal path.",
        "consequence": "Higher tail latency."
      }
    ]
  }
}
```

Scaffold receipts: minimal: `pgmcp://cache/runs/b48ae4150c424b698ae152afbe4a5967`; filled: `pgmcp://cache/runs/a6e5911bae0b4aa7ba45c45ffda81aa7`.

### generic_doc

Version: 1.0.0; package fingerprint: `QEtFztWtFehT8R5U`.

```json
{
  "minimal": {
    "title": "Template Output Review",
    "purpose": "Record first-call output observations.",
    "summary": "Review representative generated artifacts for formatting and presentation."
  },
  "filled": {
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
  }
}
```

Scaffold receipts: minimal: `pgmcp://cache/runs/dca46d4b3a444c4da577cb44397d2a9d`; filled: `pgmcp://cache/runs/9a299153c37144f99cca16980e3ccc64`.

### issue

Version: 1.0.0; package fingerprint: `O3lr-JfD_5Kv7Cfx`.

```json
{
  "minimal": {
    "problem": "A valid issue body renders without caller-supplied publication metadata."
  },
  "filled": {
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
  }
}
```

Scaffold receipts: minimal: `pgmcp://cache/runs/b31277947b014a4eb155f8de52a4f569`; filled: `pgmcp://cache/runs/c5e98d57f2c04be194747ff30db43841`.

### planning

Version: 1.0.0; package fingerprint: `E5cXGU37lhDmDnjF`.

```json
{
  "minimal": {
    "title": "Event Path Plan",
    "summary": "Make acknowledgement follow a durable append.",
    "work_units": [
      {
        "id": "U1",
        "name": "Append ordering",
        "goal": "Enforce durable append before acknowledgement.",
        "deliverables": [
          {
            "id": "code",
            "description": "Updated consumer path."
          }
        ],
        "exit_criteria": "Failure injection proves no early acknowledgement."
      }
    ]
  },
  "filled": {
    "title": "Event Path Plan",
    "summary": "Make acknowledgement follow a durable append.",
    "dependencies": [
      "Approved interface contract"
    ],
    "work_units": [
      {
        "id": "U1",
        "name": "Append ordering",
        "goal": "Enforce durable append before acknowledgement.",
        "owner": "@imp",
        "deliverables": [
          {
            "id": "code",
            "description": "Updated consumer path.",
            "owner": "@imp",
            "validates": {
              "type": "contains_text",
              "file": "mcp_server/consumer.py",
              "text": "append"
            }
          }
        ],
        "exit_criteria": "Failure injection proves no early acknowledgement.",
        "verification": [
          {
            "obligation": "Failed append does not acknowledge",
            "method": "Run focused failure-path test",
            "expected_result": "No acknowledgement is observed."
          }
        ],
        "risks": [
          {
            "description": "Retry may duplicate an append.",
            "mitigation": "Use the durable event key.",
            "consequence": "Duplicate journal entries."
          }
        ],
        "stop_conditions": [
          "Stop if the approved call contract cannot be preserved."
        ]
      }
    ],
    "phase_deliverables": {
      "validation": [
        {
          "id": "report",
          "description": "Validation evidence report.",
          "validates": {
            "type": "file_exists",
            "file": "docs/development/issue473/validation.md"
          }
        }
      ]
    }
  }
}
```

Scaffold receipts: minimal: `pgmcp://cache/runs/730f01d21410426b90a7b5a5b24ba692`; filled: `pgmcp://cache/runs/345b7c0ecddc4589bef6f0b919461748`.

### pr

Version: 1.0.0; package fingerprint: `XKvE7Nls1VlJQIPF`.

```json
{
  "minimal": {
    "changes": "Describe the change.",
    "deferred_work": []
  },
  "filled": {
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
  }
}
```

Scaffold receipts: minimal: `pgmcp://cache/runs/63bf9fcb1f1346a2a436a00268929cae`; filled: `pgmcp://cache/runs/b24a36800aa94091b9703cccaf323fcb`.

### pytest_integration_test

Version: 1.0.0; package fingerprint: `J4-Led_kGRhKPVHQ`.

```json
{
  "minimal": {
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
  "filled": {
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
  }
}
```

Scaffold receipts: minimal: `pgmcp://cache/runs/12f677977ac84d87887960a58fd7fd77`; filled: `pgmcp://cache/runs/2f9e663a51854427b322086fcfcde2d6`.

### pytest_unit_test

Version: 1.0.0; package fingerprint: `KPwraD7t-PPta2Q0`.

```json
{
  "minimal": {
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
  "filled": {
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
  }
}
```

Scaffold receipts: minimal: `pgmcp://cache/runs/0c72160e821f41c3a723e6a8586c9e5e`; filled: `pgmcp://cache/runs/4a48025b483f45fdaa1ca793f2b9c971`.

### python_adapter

Version: 1.0.0; package fingerprint: `6_4LR53QIIsijfkP`.

```json
{
  "minimal": {
    "class_name": "PriceAdapter",
    "description": "Adapts a price source."
  },
  "filled": {
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
  }
}
```

Scaffold receipts: minimal: `pgmcp://cache/runs/034af4ba6a0e4e4bbce9cb7b5f879030`; filled: `pgmcp://cache/runs/dca0a4b3068b48d189c66279614336ab`.

### python_class

Version: 1.0.0; package fingerprint: `hy3SAizDAZ8yUHLN`.

```json
{
  "minimal": {
    "class_name": "PriceCalculator",
    "description": "Calculates a notional value."
  },
  "filled": {
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
  }
}
```

Scaffold receipts: minimal: `pgmcp://cache/runs/722a393c10bd42509ae35777f26a8fa6`; filled: `pgmcp://cache/runs/9af12dcd1c444c6b9add8b23808e946a`.

### python_protocol

Version: 1.0.0; package fingerprint: `0pdQ_BkqDPKZxHss`.

```json
{
  "minimal": {
    "class_name": "PriceSource",
    "description": "Provides price data."
  },
  "filled": {
    "class_name": "PriceSource",
    "description": "Provides price data.",
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
    ]
  }
}
```

Scaffold receipts: minimal: `pgmcp://cache/runs/3960868e39284e0b83d3bd8a2a3beb8c`; filled: `pgmcp://cache/runs/a2ee58d729ae44cc8503b12362578f37`.

### python_pydantic_config

Version: 1.0.0; package fingerprint: `KjQnWprHR3MCCNwv`.

```json
{
  "minimal": {
    "class_name": "RiskSettings",
    "description": "Risk settings.",
    "frozen": true
  },
  "filled": {
    "class_name": "RiskSettings",
    "description": "Risk settings.",
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
    ]
  }
}
```

Scaffold receipts: minimal: `pgmcp://cache/runs/2fb1deb6652b4bc4a94942a0eed41a4f`; filled: `pgmcp://cache/runs/1bc2141a6c57449caf3808a2ec283699`.

### python_pydantic_dto

Version: 1.0.0; package fingerprint: `ZaJvTOvENaaS4lHn`.

```json
{
  "minimal": {
    "class_name": "PriceSnapshot",
    "description": "A price snapshot."
  },
  "filled": {
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
  }
}
```

Scaffold receipts: minimal: `pgmcp://cache/runs/33d914380d3d43ddaa8887e6774f94d0`; filled: `pgmcp://cache/runs/11de08cb102a4984b364515091abe759`.

### python_worker

Version: 1.0.0; package fingerprint: `XLHdkTeXyRZ14HBB`.

```json
{
  "minimal": {
    "class_name": "PriceWorker",
    "description": "Processes a price update.",
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
    }
  },
  "filled": {
    "class_name": "PriceWorker",
    "description": "Publishes a price update.",
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
    }
  }
}
```

Scaffold receipts: minimal: `pgmcp://cache/runs/a7c47dfb74f24a3b87d35a95e20bfafb`; filled: `pgmcp://cache/runs/4d320ba2b9b148d78cc5432ad12cddb4`.

### reference

Version: 1.0.0; package fingerprint: `6p2eztqyHAFsTyHx`.

```json
{
  "minimal": {
    "title": "Event API",
    "sources": [
      {
        "label": "API source",
        "target": "../../../README.md"
      }
    ],
    "api_reference": []
  },
  "filled": {
    "title": "Event API",
    "status": "DRAFT — review pending",
    "sources": [
      {
        "label": "API source",
        "target": "../../../README.md"
      }
    ],
    "api_reference": [
      {
        "name": "EventReader",
        "description": "Reads events in partition order.",
        "sources": [
          {
            "label": "Reader source",
            "target": "../../../README.md"
          }
        ],
        "methods": [
          {
            "signature": "read(partition: str)",
            "parameters": "partition identifier",
            "returns": "Event | None",
            "description": "Returns the next event.",
            "errors": "Raises JournalUnavailable when storage cannot be read.",
            "sources": [
              {
                "label": "Method source",
                "target": "../../../README.md"
              }
            ]
          }
        ]
      }
    ],
    "test_evidence": [
      {
        "label": "Reader tests",
        "target": "../../../tests/mcp_server/integration/templates/test_reference.py"
      }
    ],
    "usage_examples": [
      {
        "description": "Python reader use",
        "language": "python",
        "code": "event = reader.read(partition)"
      }
    ]
  }
}
```

Scaffold receipts: minimal: `pgmcp://cache/runs/972a1574059c4302b12ccfd26122dc5e`; filled: `pgmcp://cache/runs/4e91aab024274206b3a6054aa290a77e`.

### research

Version: 1.0.0; package fingerprint: `i6OWAIfugGkQJPIz`.

```json
{
  "minimal": {
    "title": "First-call template quality research",
    "problem_statement": "Some shipped templates produce first outputs with formatting defects.",
    "goals": [
      "Locate generated presentation defects."
    ]
  },
  "filled": {
    "title": "First-call template quality research",
    "problem_statement": "Some shipped templates produce first outputs with formatting defects.",
    "goals": [
      "Locate generated presentation defects.",
      "Separate template text from caller-authored strings."
    ],
    "background": "Issue 473 reports excess Markdown spacing and mechanical labels.",
    "findings": "The six Markdown templates extend the same document base and section/link macros.",
    "questions": [
      "Which boundaries need an explicit compatibility decision?"
    ],
    "references": [
      {
        "label": "Documentation Standard",
        "target": "../../../docs/coding_standards/DOCUMENTATION_STANDARD.md"
      }
    ],
    "evidence": [
      {
        "claim": "The document base emits metadata and related-document blocks.",
        "observation": "The base has explicit conditional blocks for status, version, date, and related docs.",
        "sources": [
          {
            "label": "Markdown document base",
            "target": "../../../.pgmcp/template_suite/shared/templates/bases/tier2_markdown_document.jinja2"
          }
        ],
        "invocation": "Render one populated document context",
        "observed_result": "Authored sample evidence; actual rendering is measured separately.",
        "observed_at": "2026-10-02T12:00:00Z"
      }
    ],
    "consumers": [
      {
        "name": "First-time scaffold caller",
        "responsibility": "Supplies artifact context.",
        "impact": "Reads generated Markdown before editing."
      }
    ],
    "risks": [
      {
        "description": "A template defect can be misattributed to a user string.",
        "mitigation": "Use marker strings and compare the raw template path.",
        "consequence": "A fix could alter valid authored content."
      }
    ],
    "assumptions": [
      "The supplied context strings are representative."
    ]
  }
}
```

Scaffold receipts: minimal: `pgmcp://cache/runs/86b965da485f465794143a9052eeb9bd`; filled: `pgmcp://cache/runs/b9cce7424c214d55b52e8fc063b86584`.

### typescript_dto

Version: 1.0.0; package fingerprint: `nrJatmiH7RAfWNzm`.

```json
{
  "minimal": {
    "class_name": "PriceSnapshot",
    "description": "A price snapshot."
  },
  "filled": {
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
  }
}
```

Scaffold receipts: minimal: `pgmcp://cache/runs/6c5806241a3141f99ba67c17e8f841ba`; filled: `pgmcp://cache/runs/0376fc83fd3441309086e501ef796590`.

### validation_report

Version: 1.0.0; package fingerprint: `3zJkRylM4sIT4HzD`.

```json
{
  "minimal": {
    "title": "Event path validation"
  },
  "filled": {
    "title": "Event path validation",
    "issue_number": 473,
    "cycle": "C1",
    "validation_status": "PARTIAL",
    "scope": "Durable append ordering.",
    "obligations": [
      {
        "obligation": "Failed append is not acknowledged",
        "evidence": [
          {
            "label": "Failure-path test",
            "target": "../../../tests/mcp_server/integration/templates/test_validation_artifact.py"
          }
        ],
        "outcome": "Authored sample outcome; not independent validation."
      }
    ],
    "evidence": [
      {
        "claim": "The focused failure case preserves ordering.",
        "observation": "Authored sample observation, supplied to exercise the evidence carrier.",
        "sources": [
          {
            "label": "Sample source",
            "target": "../../../README.md"
          }
        ],
        "invocation": "Authored example invocation",
        "observed_result": "Authored example result; not a measured test outcome.",
        "observed_at": "2026-10-02T12:00:00Z"
      }
    ],
    "failures": [],
    "caveats": [
      "PARTIAL is authored sample content, not independent QA status."
    ]
  }
}
```

Scaffold receipts: minimal: `pgmcp://cache/runs/931214ef5630438cada6200590710518`; filled: `pgmcp://cache/runs/d4c5d178a05249a6adb1a0c59e332c74`.

## Quality invocations and factual results

`run_checks(scope="targets", targets=<all 16 .py outputs>, checks=["python_format","python_lint"], timeout_seconds=120)`: receipt `pgmcp://cache/runs/8f29b7b33e584a53be0097d1b6f0d1f8`; both selected checks failed. Ruff uses [workspace configuration](../../../pyproject.toml): line length 100, target Python 3.11 and the configured lint rule selection. The temporary survey paths do not match the test-only ANN/ARG exclusions. No authored body finding occurred in this survey.

### python_format

Status: failed; native Ruff 0.15.6. Configured arguments: `[]` (the adapter adds operation controls, including non-mutating format check/diff).

```text
stdout:
--- .pgmcp\temp\issue473-survey\pytest_integration_test.filled.py
+++ .pgmcp\temp\issue473-survey\pytest_integration_test.filled.py
@@ -6,14 +6,8 @@
 from pathlib import Path
 
 
-
-
-
 def test_file_round_trip(tmp_path: Path) -> None:
     "Write and read a temporary file."
     source = tmp_path / "input.txt"
     source.write_text("payload", encoding="utf-8")
     assert source.read_text(encoding="utf-8") == "payload"
-
-
-

--- .pgmcp\temp\issue473-survey\pytest_integration_test.minimal.py
+++ .pgmcp\temp\issue473-survey\pytest_integration_test.minimal.py
@@ -3,13 +3,7 @@
 "Check a rendered integration result."
 
 
-
-
-
 def test_total() -> None:
     "Add two values."
     result = sum([2, 3])
     assert result == 5
-
-
-

--- .pgmcp\temp\issue473-survey\pytest_unit_test.filled.py
+++ .pgmcp\temp\issue473-survey\pytest_unit_test.filled.py
@@ -11,18 +11,15 @@
 
 pytestmark = [pytest.mark.usefixtures("sample_path")]
 
+
 @pytest.fixture(scope="function", autouse=False)
 def sample_path(tmp_path: Path) -> Path:
     "Write a temporary text file."
     path = tmp_path / "sample.txt"
     path.write_text("ready", encoding="utf-8")
     return path
-
 
 
 def test_sample_content(sample_path: Path) -> None:
     "Read the fixture file."
     assert sample_path.read_text(encoding="utf-8") == "ready"
-
-
-

--- .pgmcp\temp\issue473-survey\pytest_unit_test.minimal.py
+++ .pgmcp\temp\issue473-survey\pytest_unit_test.minimal.py
@@ -3,13 +3,7 @@
 "Check a small arithmetic result."
 
 
-
-
-
 def test_sum() -> None:
     "Add two values."
     result = sum([2, 3])
     assert result == 5
-
-
-

--- .pgmcp\temp\issue473-survey\python_adapter.filled.py
+++ .pgmcp\temp\issue473-survey\python_adapter.filled.py
@@ -2,16 +2,13 @@
 
 "Market data adapter."
 
-
 # Standard library
 import logging
 
 # Project
 from market_ports import PriceClient
-
 
 
-
 logger = logging.getLogger("market.adapter")
 
 
@@ -20,11 +17,7 @@
 
     def __init__(self, client: PriceClient) -> None:
         self._client = client
-
 
     def read_price(self, symbol: str) -> int:
         "Return the latest price."
         return self._client.read_price(symbol)
-
-
-

--- .pgmcp\temp\issue473-survey\python_adapter.minimal.py
+++ .pgmcp\temp\issue473-survey\python_adapter.minimal.py
@@ -3,14 +3,7 @@
 "Adapts a price source."
 
 
-
-
-
 class PriceAdapter:
     "Adapts a price source."
-
 
-
     pass
-
-

--- .pgmcp\temp\issue473-survey\python_class.filled.py
+++ .pgmcp\temp\issue473-survey\python_class.filled.py
@@ -12,5 +12,3 @@
     def notional(self, quantity: Decimal, unit_price: Decimal) -> Decimal:
         "Multiply quantity by unit price."
         raise NotImplementedError
-
-

--- .pgmcp\temp\issue473-survey\python_class.minimal.py
+++ .pgmcp\temp\issue473-survey\python_class.minimal.py
@@ -7,5 +7,3 @@
     "Calculates a notional value."
 
     pass
-
-

--- .pgmcp\temp\issue473-survey\python_protocol.filled.py
+++ .pgmcp\temp\issue473-survey\python_protocol.filled.py
@@ -2,10 +2,8 @@
 
 "Contract for reading market prices."
 
-
 # Standard library
 from typing import Protocol
-
 
 
 class PriceSource(Protocol):
@@ -18,5 +16,3 @@
     def close(self) -> None:
         "Release the source resources."
         ...
-
-

--- .pgmcp\temp\issue473-survey\python_protocol.minimal.py
+++ .pgmcp\temp\issue473-survey\python_protocol.minimal.py
@@ -2,15 +2,11 @@
 
 "Provides price data."
 
-
 # Standard library
 from typing import Protocol
-
 
 
 class PriceSource(Protocol):
     "Provides price data."
 
     pass
-
-

--- .pgmcp\temp\issue473-survey\python_pydantic_config.filled.py
+++ .pgmcp\temp\issue473-survey\python_pydantic_config.filled.py
@@ -2,20 +2,20 @@
 
 "Risk controls for one strategy."
 
-
-
-
 # Third party
 from pydantic import BaseModel, ConfigDict, Field
-
 
 
 class RiskSettings(BaseModel):
     "Risk settings."
 
-    model_config = ConfigDict(extra="forbid", frozen=False, json_schema_extra={"examples": [{"enabled": True, "max_order_size": 5, "label": "primary"}]})
+    model_config = ConfigDict(
+        extra="forbid",
+        frozen=False,
+        json_schema_extra={
+            "examples": [{"enabled": True, "max_order_size": 5, "label": "primary"}]
+        },
+    )
     enabled: bool = Field(default=False, description="Enable order submission.")
     max_order_size: int = Field(default=0, description="Maximum permitted order size.", ge=0)
     label: str = Field(default="", description="Optional operator label.", min_length=0)
-
-

--- .pgmcp\temp\issue473-survey\python_pydantic_config.minimal.py
+++ .pgmcp\temp\issue473-survey\python_pydantic_config.minimal.py
@@ -2,17 +2,11 @@
 
 "Risk settings."
 
-
-
-
 # Third party
 from pydantic import BaseModel, ConfigDict
 
 
-
 class RiskSettings(BaseModel):
     "Risk settings."
 
     model_config = ConfigDict(extra="forbid", frozen=True)
-    
-

--- .pgmcp\temp\issue473-survey\python_pydantic_dto.filled.py
+++ .pgmcp\temp\issue473-survey\python_pydantic_dto.filled.py
@@ -2,23 +2,23 @@
 
 "Validated market data."
 
-
-
-
 # Standard library
 import datetime
 
 # Third party
 from pydantic import BaseModel, ConfigDict, Field
-
 
 
 class PriceSnapshot(BaseModel):
     "A price snapshot."
 
-    model_config = ConfigDict(extra="forbid", frozen=True, json_schema_extra={"examples": [{"symbol": "ABC", "mid": 101.25}]})
+    model_config = ConfigDict(
+        extra="forbid",
+        frozen=True,
+        json_schema_extra={"examples": [{"symbol": "ABC", "mid": 101.25}]},
+    )
     symbol: str = Field(description="Instrument identifier.", min_length=1)
     mid: float = Field(description="Mid-market price.", gt=0)
-    observed_at: datetime.datetime = Field(default_factory=datetime.datetime.now, description="Observation time.")
-
-
+    observed_at: datetime.datetime = Field(
+        default_factory=datetime.datetime.now, description="Observation time."
+    )

--- .pgmcp\temp\issue473-survey\python_pydantic_dto.minimal.py
+++ .pgmcp\temp\issue473-survey\python_pydantic_dto.minimal.py
@@ -2,17 +2,11 @@
 
 "A price snapshot."
 
-
-
-
 # Third party
 from pydantic import BaseModel, ConfigDict
 
 
-
 class PriceSnapshot(BaseModel):
     "A price snapshot."
 
     model_config = ConfigDict(extra="forbid", frozen=True)
-    
-

--- .pgmcp\temp\issue473-survey\python_worker.filled.py
+++ .pgmcp\temp\issue473-survey\python_worker.filled.py
@@ -2,16 +2,13 @@
 
 "Publishes a price update."
 
-
 # Standard library
 import logging
 
 # Project
 from market_ports import PriceClient
-
 
 
-
 logger = logging.getLogger("market.worker")
 
 
@@ -24,4 +21,3 @@
     def process(self, symbol: str, value: int) -> None:
         "Publish the accepted price update."
         self._client.publish(symbol, value)
-

--- .pgmcp\temp\issue473-survey\python_worker.minimal.py
+++ .pgmcp\temp\issue473-survey\python_worker.minimal.py
@@ -3,13 +3,9 @@
 "Processes a price update."
 
 
-
-
-
 class PriceWorker:
     "Processes a price update."
 
     def process(self, value: int) -> int:
         "Return one accepted value."
         return value
-


stderr:
16 files would be reformatted

```

### python_lint

Status: failed; native Ruff 0.15.6. Configured arguments: `[]` (the adapter adds operation controls, including non-mutating format check/diff).

```text
stdout:
I001 [*] Import block is un-sorted or un-formatted
 --> .pgmcp\temp\issue473-survey\pytest_integration_test.filled.py:6:1
  |
5 | # Standard library
6 | from pathlib import Path
  | ^^^^^^^^^^^^^^^^^^^^^^^^
  |
help: Organize imports

I001 [*] Import block is un-sorted or un-formatted
 --> .pgmcp\temp\issue473-survey\pytest_unit_test.filled.py:6:1
  |
5 |   # Standard library
6 | / from pathlib import Path
7 | |
8 | | # Third party
9 | | import pytest
  | |_____________^
  |
help: Organize imports

I001 [*] Import block is un-sorted or un-formatted
  --> .pgmcp\temp\issue473-survey\python_adapter.filled.py:7:1
   |
 6 |   # Standard library
 7 | / import logging
 8 | |
 9 | | # Project
10 | | from market_ports import PriceClient
   | |____________________________________^
   |
help: Organize imports

I001 [*] Import block is un-sorted or un-formatted
 --> .pgmcp\temp\issue473-survey\python_protocol.filled.py:7:1
  |
6 | # Standard library
7 | from typing import Protocol
  | ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  |
help: Organize imports

I001 [*] Import block is un-sorted or un-formatted
 --> .pgmcp\temp\issue473-survey\python_protocol.minimal.py:7:1
  |
6 | # Standard library
7 | from typing import Protocol
  | ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  |
help: Organize imports

I001 [*] Import block is un-sorted or un-formatted
 --> .pgmcp\temp\issue473-survey\python_pydantic_config.filled.py:9:1
  |
8 | # Third party
9 | from pydantic import BaseModel, ConfigDict, Field
  | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  |
help: Organize imports

E501 Line too long (153 > 100)
  --> .pgmcp\temp\issue473-survey\python_pydantic_config.filled.py:16:101
   |
14 | …
15 | …
16 | …json_schema_extra={"examples": [{"enabled": True, "max_order_size": 5, "label": "primary"}]})
   |                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
17 | … order submission.")
18 | …mum permitted order size.", ge=0)
   |

I001 [*] Import block is un-sorted or un-formatted
 --> .pgmcp\temp\issue473-survey\python_pydantic_config.minimal.py:9:1
  |
8 | # Third party
9 | from pydantic import BaseModel, ConfigDict
  | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  |
help: Organize imports

W293 [*] Blank line contains whitespace
  --> .pgmcp\temp\issue473-survey\python_pydantic_config.minimal.py:17:1
   |
16 |     model_config = ConfigDict(extra="forbid", frozen=True)
17 |     
   | ^^^^
   |
help: Remove whitespace from blank line

I001 [*] Import block is un-sorted or un-formatted
  --> .pgmcp\temp\issue473-survey\python_pydantic_dto.filled.py:9:1
   |
 8 |   # Standard library
 9 | / import datetime
10 | |
11 | | # Third party
12 | | from pydantic import BaseModel, ConfigDict, Field
   | |_________________________________________________^
   |
help: Organize imports

E501 Line too long (126 > 100)
  --> .pgmcp\temp\issue473-survey\python_pydantic_dto.filled.py:19:101
   |
17 |     "A price snapshot."
18 |
19 |     model_config = ConfigDict(extra="forbid", frozen=True, json_schema_extra={"examples": [{"symbol": "ABC", "mid": 101.25}]})
   |                                                                                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^
20 |     symbol: str = Field(description="Instrument identifier.", min_length=1)
21 |     mid: float = Field(description="Mid-market price.", gt=0)
   |

E501 Line too long (114 > 100)
  --> .pgmcp\temp\issue473-survey\python_pydantic_dto.filled.py:22:101
   |
20 |     symbol: str = Field(description="Instrument identifier.", min_length=1)
21 |     mid: float = Field(description="Mid-market price.", gt=0)
22 |     observed_at: datetime.datetime = Field(default_factory=datetime.datetime.now, description="Observation time.")
   |                                                                                                     ^^^^^^^^^^^^^^
   |

I001 [*] Import block is un-sorted or un-formatted
 --> .pgmcp\temp\issue473-survey\python_pydantic_dto.minimal.py:9:1
  |
8 | # Third party
9 | from pydantic import BaseModel, ConfigDict
  | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  |
help: Organize imports

W293 [*] Blank line contains whitespace
  --> .pgmcp\temp\issue473-survey\python_pydantic_dto.minimal.py:17:1
   |
16 |     model_config = ConfigDict(extra="forbid", frozen=True)
17 |     
   | ^^^^
   |
help: Remove whitespace from blank line

I001 [*] Import block is un-sorted or un-formatted
  --> .pgmcp\temp\issue473-survey\python_worker.filled.py:7:1
   |
 6 |   # Standard library
 7 | / import logging
 8 | |
 9 | | # Project
10 | | from market_ports import PriceClient
   | |____________________________________^
   |
help: Organize imports

Found 15 errors.
[*] 12 fixable with the `--fix` option.

```

`run_checks(scope="targets", targets=<all 18 .md outputs>, profile="markdown_link_review", timeout_seconds=120)`: receipt `pgmcp://cache/runs/35bad7031e77439db4e03ec2aef7d900`. Lychee 0.24.2, offline/cache-disabled/include-fragments, inspected 15 links (9 unique); 14 successful, one missing file. The failing target `../../../.pgmcp/template_suite/README.md` was supplied by the researcher in `generic_doc.filled`; that file does not exist. The template preserves the supplied target. The failed invocation is retained unchanged; it is caller-authored counterevidence, not proof of a template link defect.

Scaffold preflights: 16 Python syntax passes (Python 3.13.7), 18 Markdown passes, two TypeScript unavailabilities (`Cannot find module 'typescript'` from the active workspace), and two commitlint unavailabilities (`Cannot find module '@commitlint/cli/package.json'`). The four unavailable observations are not passes.

`run_tests(scope="targets", targets=<the 19 corresponding concrete-package integration test files>, tests=["python_tests"], args={"python_tests":["-q","-n","0"]}, timeout_seconds=120)`: receipt `pgmcp://cache/runs/6db8054b319647679b0346a58a727d32`; **85 passed, one existing Pydantic schema-shadowing warning, 83.31 s**. Exact selected paths:

```json
[
  "tests/mcp_server/integration/templates/test_architecture.py",
  "tests/mcp_server/integration/templates/test_commit_artifact.py",
  "tests/mcp_server/integration/templates/test_design_artifact.py",
  "tests/mcp_server/integration/templates/test_generic_document.py",
  "tests/mcp_server/integration/templates/test_issue.py",
  "tests/mcp_server/integration/templates/test_planning_artifact.py",
  "tests/mcp_server/integration/templates/test_pr.py",
  "tests/mcp_server/integration/templates/test_pytest_integration_test.py",
  "tests/mcp_server/integration/templates/test_pytest_unit_test.py",
  "tests/mcp_server/integration/templates/test_python_adapter.py",
  "tests/mcp_server/integration/templates/test_python_class.py",
  "tests/mcp_server/integration/templates/test_python_protocol.py",
  "tests/mcp_server/integration/templates/test_python_pydantic_config.py",
  "tests/mcp_server/integration/templates/test_python_pydantic_dto.py",
  "tests/mcp_server/integration/templates/test_python_worker.py",
  "tests/mcp_server/integration/templates/test_reference.py",
  "tests/mcp_server/integration/templates/test_research_artifact.py",
  "tests/mcp_server/integration/templates/test_typescript_artifact.py",
  "tests/mcp_server/integration/templates/test_validation_artifact.py"
]
```

These tests exercise separate copied package fixtures with native test dependencies and strict TypeScript compilation/commit fixtures. Their renderer uses `StrictUndefined` and `keep_trailing_newline=True`; production composition uses a plain Jinja environment with its prepared loader. Their success proves existing semantic contracts under those fixtures; it does not convert the two current workspace dependencies into available tools or prove live first-output Ruff/presentation cleanliness.

Cached structured receipts were read in full with contiguous pagination and verified length/SHA-256 before interpretation. The context, measured output digests, decisive native diagnostic text, and selected unchanged outputs are preserved here because runtime cache resources and ignored survey files are not durable branch artifacts.

## Selected unchanged outputs

### python_adapter.minimal.py

Unchanged first output; SHA-256 `8b9e724fe4571c037457e9f6838b0d363ae8efabfe8a4a1123f806d7152401d9`.

````python
# pgmcp:v1 id=python_adapter pv=1.0.0 pf=6_4LR53QIIsijfkP sf=9PfER5JkyAoFQLRi

"Adapts a price source."





class PriceAdapter:
    "Adapts a price source."



    pass


````

### python_pydantic_config.filled.py

Unchanged first output; SHA-256 `f501b7eda3e79fcad545bb65476cf0fb4f21a38df44e5bad826d629ecef61aab`.

````python
# pgmcp:v1 id=python_pydantic_config pv=1.0.0 pf=KjQnWprHR3MCCNwv sf=9PfER5JkyAoFQLRi

"Risk controls for one strategy."




# Third party
from pydantic import BaseModel, ConfigDict, Field



class RiskSettings(BaseModel):
    "Risk settings."

    model_config = ConfigDict(extra="forbid", frozen=False, json_schema_extra={"examples": [{"enabled": True, "max_order_size": 5, "label": "primary"}]})
    enabled: bool = Field(default=False, description="Enable order submission.")
    max_order_size: int = Field(default=0, description="Maximum permitted order size.", ge=0)
    label: str = Field(default="", description="Optional operator label.", min_length=0)


````

### python_pydantic_dto.minimal.py

Unchanged first output; SHA-256 `4caafa43388bd02a622927bb5e9ea7f6e93cef600fb9a880df9a42fe651e06c7`.

````python
# pgmcp:v1 id=python_pydantic_dto pv=1.0.0 pf=ZaJvTOvENaaS4lHn sf=9PfER5JkyAoFQLRi

"A price snapshot."




# Third party
from pydantic import BaseModel, ConfigDict



class PriceSnapshot(BaseModel):
    "A price snapshot."

    model_config = ConfigDict(extra="forbid", frozen=True)
    

````

### planning.filled.md

Unchanged first output; SHA-256 `52d2d2f9a91471ecfab92d4867cbdfa50a713d33810fc1f422627368772b2c12`.

````markdown
<!-- pgmcp:v1 id=planning pv=1.0.0 pf=E5cXGU37lhDmDnjF sf=9PfER5JkyAoFQLRi -->

# Event Path Plan





## Summary

Make acknowledgement follow a durable append.


## Dependencies

- Approved interface contract




## Work Units


### U1 — Append ordering

**Goal:** Enforce durable append before acknowledgement.



**Owner:** @imp



#### Deliverables

##### code

Updated consumer path.


**Owner:** @imp



**Validates:**
**Type:** contains_text

**File:** mcp_server/consumer.py

**Text:** append





#### Exit Criteria

Failure injection proves no early acknowledgement.




#### Verification


##### Failed append does not acknowledge

**Method:** Run focused failure-path test

**Expected Result:** No acknowledgement is observed.





#### Risks


##### Retry may duplicate an append.

Use the durable event key.


**Consequence:** Duplicate journal entries.





#### Stop Conditions

- Stop if the approved call contract cannot be preserved.




## Phase Deliverables





### Validation

#### report

Validation evidence report.



**Validates:**
**Type:** file_exists

**File:** docs/development/issue473/validation.md













````

### generic_doc.filled.md

Unchanged first output; SHA-256 `bd9b9de85f092047e2e2e4f0e50de8e7545e092713a413c52d601475007c538e`.

````markdown
<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=QEtFztWtFehT8R5U sf=9PfER5JkyAoFQLRi -->

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

````

### validation_report.minimal.md

Unchanged first output; SHA-256 `0b6e98ddd6e637c961134cf29fd2b6ed4d483dff9200c917455e87c3ad84e029`.

````markdown
<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=3zJkRylM4sIT4HzD sf=9PfER5JkyAoFQLRi -->

# Event path validation





















````

### commit.filled.txt

Unchanged first output; SHA-256 `68a77cd959414766cee1d942491afdb1a890601e233b41bb0f296b26bb6b7ccc`.

````text
# pgmcp:v1 id=commit pv=1.0.0 pf=_Yga89XCROsHUBlO sf=9PfER5JkyAoFQLRi

feat(templates)!: Preserve authored commit framing

Keep the supplied message text intact.

Retain paragraph boundaries.

BREAKING CHANGE: Consumers must supply explicit commit fields.

Refs: #473, #460

Reviewed-by: Template Maintainers


````

### typescript_dto.filled.ts

Unchanged first output; SHA-256 `09e3d178fa9e001a601d461a8f497507a0ff8e0fcdc0c0ecc717be03be6db8e6`.

````typescript
// pgmcp:v1 id=typescript_dto pv=1.0.0 pf=nrJatmiH7RAfWNzm sf=9PfER5JkyAoFQLRi

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

````

