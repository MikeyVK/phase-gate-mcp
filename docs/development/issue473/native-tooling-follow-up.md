<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=QEtFztWtFehT8R5U sf=9PfER5JkyAoFQLRi -->

# Issue 473 — Native Tooling Follow-up

**Status:** RESEARCH EVIDENCE — native prerequisites installed
**Version:** 0.1
**Last Updated:** 2026-10-03

## Purpose and authorization

The human authorized installation of the missing tools to support an honest, substantive comparison. This follow-up resolves the TypeScript and Commit dependency gaps recorded in the [final family comparison](tracking-typescript-comparison.md). Historical pre-installation receipts remain unchanged; they describe the environment at that time.

The workspace now has the project-pinned packages below, installed locally under node_modules. Node 24.14.0 satisfies the Commit adapter's Node >=22.12 prerequisite.

| Package | Installed version | Project authority |
| --- | --- | --- |
| typescript | 6.0.3 | [TypeScript adapter package](../../../mcp_server/bundled_adapters/typescript_syntax/package.json) |
| @commitlint/cli | 21.2.2 | [Commit adapter package](../../../mcp_server/bundled_adapters/commitlint/package.json) |
| conventional-changelog-conventionalcommits | 10.4.0 | [Commit adapter package](../../../mcp_server/bundled_adapters/commitlint/package.json) |
| pyright | 1.1.408 | [Pyright adapter package](../../../mcp_server/bundled_adapters/pyright/package.json) |

The first successful npm installation pruned the existing Pyright package because the workspace has no root package manifest. Pyright was restored at its project-pinned version while explicitly retaining all four packages. Final manifest reads confirm all four versions. The final installation command was:

```text
npm.cmd install --no-save --package-lock=false --ignore-scripts --no-audit --no-fund --cache .pgmcp/temp/npm-cache --fetch-retries=0 --fetch-timeout=20000 typescript@6.0.3 @commitlint/cli@21.2.2 conventional-changelog-conventionalcommits@10.4.0 pyright@1.1.408
```

Installation used the existing Node/npm runtime and an ignored workspace cache. No root package.json or package-lock.json was created; lifecycle scripts were disabled. No tracked dependency manifest, adapter, template, schema or public gate configuration was edited. Installation authorizes these research prerequisites, not automatic installation by the engine or a new enforcement policy.

## Native checks on unchanged comparison outputs

Twelve stored raw comparison files were submitted through safe_edit_file with identical content, report validation and explicit TypeScript/Commit identity. This invokes each package's configured content preflight without a repair. Every receipt reports content_changed=false. SHA-256 values before and after all checks match for all twelve files.

| Surface | Result | Interpretation |
| --- | --- | --- |
| Current TypeScript: minimal, filled, empty-fields and colon-type | 4 passed | Native syntax preflight now runs with TypeScript 6.0.3. |
| Old TypeScript minimal | 1 passed | The minimal old render has no native syntax error. |
| Old TypeScript filled | Failed: TS1109 at 24:16 and 24:28 | The generated `this.note? = data.note?;` assignment is invalid native syntax. |
| Old TypeScript colon-type | Failed: TS1005 at 9:34 and 11:20 | The old renderer truncates native type text on colons; the current probe passes. |
| Current Commit: minimal, filled and authored-empty | 3 passed | Native commitlint 21.2.2 accepts the checked message views. |
| Two complete saved old Commit files | Both failed: type-empty and subject-empty | The old comparison-only provenance line remains in the checked input. This is a stored-artifact framing boundary, not evidence that the authored commit messages are invalid. |
| Two separately derived old Commit message views | Both passed | Excluding only the first provenance line leaves the exact remainder, including its initial newline, accepted by native commitlint. |

The twelve raw checks comprise eight passes and four failures, with no dependency-unavailable result. Two additional message-view checks pass. The old source and renderer limits in the family comparison still apply; installing native tools does not establish an exact historical #460 public-pipeline baseline.

## Commit framing isolation

Each derived view excludes exactly the first line of its old saved artifact and preserves the remaining characters. The raw saved files remain unchanged. The views are separate ignored research probes:

| Source | Derived view | SHA-256 |
| --- | --- | --- |
| [commit.v2-minimal-render.txt](../../../.pgmcp/temp/issue473-comparison-05/commit.v2-minimal-render.txt) | [commit.v2-minimal-message-view.txt](../../../.pgmcp/temp/issue473-native-tooling/commit.v2-minimal-message-view.txt) | `b25a219608db0a5e10e7cdd99ef268c3f73e281a718cddad6d6ebe348b43c75e` |
| [commit.v2-filled-render.txt](../../../.pgmcp/temp/issue473-comparison-05/commit.v2-filled-render.txt) | [commit.v2-filled-message-view.txt](../../../.pgmcp/temp/issue473-native-tooling/commit.v2-filled-message-view.txt) | `746be32e2775b3deba61f4a370c1b8e8951060aa2f329edf152f68688249fe8b` |

These probes isolate message validity from storage framing. They do not add legacy-header acceptance or a production header-stripping path. The approved clean break remains binding.

## Existing native contract tests

The following narrow MCP run_tests request re-executed the existing TypeScript and Commit integration tests:

```json
{
  "scope": "targets",
  "targets": [
    "tests/mcp_server/integration/templates/test_typescript_artifact.py",
    "tests/mcp_server/integration/templates/test_commit_artifact.py"
  ],
  "tests": ["python_tests"],
  "args": {"python_tests": ["-q", "-n", "0"]},
  "timeout_seconds": 180
}
```

Result: **8 passed, 1 existing warning**, in 29.85 seconds. The warning concerns SchemaAttachment.schema shadowing a Pydantic BaseModel attribute. The complete cached DTO was read and is retained below.

The [TypeScript tests](../../../tests/mcp_server/integration/templates/test_typescript_artifact.py) provide strict compilation and executable fixture evidence for optional property presence, readonly behavior, object/function types and safe comment encoding. The [Commit tests](../../../tests/mcp_server/integration/templates/test_commit_artifact.py) provide message framing, multiline and schema-boundary evidence. No tests were added or changed, and no broad Validation suite was run.

## Evidence boundaries and remaining decisions

The raw TypeScript content preflight establishes native syntax, not semantic correctness against arbitrary external dependencies. The filled PriceSnapshot example still depends on caller-owned Currency and PriceRecordContract support. The existing fixture tests provision their own dependencies and prove their specific contracts; their success is not semantic certification of every raw survey file.

Commitlint acceptance establishes the configured message contract. It does not establish an agreed generated blank-line/EOF objective. No TypeScript formatter/linter or additional Markdown formatter was selected or installed. Independent whitespace assessment remains necessary for Python, documents and the final tracking/TypeScript batch.

The native dependency gap is resolved for these research checks. Remaining numerical whitespace, presentation and enforcement decisions in [Research](research.md) remain open. Installation does not turn possible objectives into universal guarantees, change caller-content ownership, widen #476 or authorize workflow progression.

## Appendix — raw hashes and native receipts

| Raw file | Unchanged SHA-256 | Result | Cache receipt |
| --- | --- | --- | --- |
| [commit.v2-filled-render.txt](../../../.pgmcp/temp/issue473-comparison-05/commit.v2-filled-render.txt) | `d9cbfbd265d6bdd50268ba898d28d7e0b18a8358b6db26f752a395d7872bacfb` | failed | `pgmcp://cache/runs/dbdb5d468c23415da903512fc1d06482` |
| [commit.v2-minimal-render.txt](../../../.pgmcp/temp/issue473-comparison-05/commit.v2-minimal-render.txt) | `d83b271a968fd7903a73a683bd302e980fdeac35a7bddf4a285d7ff15cc1415a` | failed | `pgmcp://cache/runs/9c502e4c6d4d4ef4bf1ca8103fac5257` |
| [commit.v3-authored-empty.txt](../../../.pgmcp/temp/issue473-comparison-05/commit.v3-authored-empty.txt) | `446e142b23fcc311ee332907d90f9744c327f0cacfada6a3bc1c57c7229e7c51` | passed | `pgmcp://cache/runs/1a6440d83a944ed2a16ea6180bbacd10` |
| [commit.v3-filled.txt](../../../.pgmcp/temp/issue473-comparison-05/commit.v3-filled.txt) | `68a77cd959414766cee1d942491afdb1a890601e233b41bb0f296b26bb6b7ccc` | passed | `pgmcp://cache/runs/47cf94594c304a238c54f030e6debe3c` |
| [commit.v3-minimal.txt](../../../.pgmcp/temp/issue473-comparison-05/commit.v3-minimal.txt) | `55f1761d484042c7176109d0214e6756c49fae050d5755e841d3926069988910` | passed | `pgmcp://cache/runs/2718005b87f0429c89734dc29aee130c` |
| [typescript_dto.v2-colon-type-render.ts](../../../.pgmcp/temp/issue473-comparison-05/typescript_dto.v2-colon-type-render.ts) | `b9f23918a8985b4e1a12fb0b94f1082ab9dab5c13166bbdc45ebca929a70fd7d` | failed | `pgmcp://cache/runs/818b8345e4764347bd5d01861c782b28` |
| [typescript_dto.v2-filled-render.ts](../../../.pgmcp/temp/issue473-comparison-05/typescript_dto.v2-filled-render.ts) | `78223c27b7af07aaf91955be3ff2ccb437beba695b23d7aa90fa0260b09a9771` | failed | `pgmcp://cache/runs/c29390d3e0314feaae42d4516c3e1a35` |
| [typescript_dto.v2-minimal-render.ts](../../../.pgmcp/temp/issue473-comparison-05/typescript_dto.v2-minimal-render.ts) | `a373b0a9b2418ec0e64612abf20acc6d249808f775a483f5f627440c1b102022` | passed | `pgmcp://cache/runs/a06d846f52fb42ff9eda4bb949d1bd58` |
| [typescript_dto.v3-colon-type.ts](../../../.pgmcp/temp/issue473-comparison-05/typescript_dto.v3-colon-type.ts) | `a8d691c220e7e60cebe040a03a309ad118bbf1f63624abb653eedde5ba1c393e` | passed | `pgmcp://cache/runs/e24538e238c140648020753e11eedc7c` |
| [typescript_dto.v3-empty-fields.ts](../../../.pgmcp/temp/issue473-comparison-05/typescript_dto.v3-empty-fields.ts) | `1b6c2b3c9242615d061acace7777a122c2a406a36b089f9854523df65d170721` | passed | `pgmcp://cache/runs/06413030404a40d58139ad776b43fa12` |
| [typescript_dto.v3-filled.ts](../../../.pgmcp/temp/issue473-comparison-05/typescript_dto.v3-filled.ts) | `09e3d178fa9e001a601d461a8f497507a0ff8e0fcdc0c0ecc717be03be6db8e6` | passed | `pgmcp://cache/runs/f41c698f2ce2443993ca0090f7a31978` |
| [typescript_dto.v3-minimal.ts](../../../.pgmcp/temp/issue473-comparison-05/typescript_dto.v3-minimal.ts) | `1b6c2b3c9242615d061acace7777a122c2a406a36b089f9854523df65d170721` | passed | `pgmcp://cache/runs/daf3336368334548a383aef935cbf262` |

Complete structured DTOs from the fourteen content-preflight checks and the native contract-test run follow. They retain native diagnostics, tool versions and original request provenance.

```json
{
  "raw_checks": [
    {
      "file": "commit.v2-filled-render.txt",
      "uri": "pgmcp://cache/runs/dbdb5d468c23415da903512fc1d06482",
      "result": {
        "success": true,
        "written": true,
        "validation_policy": "report",
        "validation_status": "failed",
        "profile_id": "commit_preflight",
        "checks": [
          {
            "check_id": "commit_message",
            "status": "failed",
            "reason": null,
            "message": "Commitlint rejected the checked message.",
            "evidence": {
              "format": "text",
              "data": "checked message view (original supplied content):\n# template=commit version=comparison-only\n\nfeat(templates)!: Preserve authored commit framing\n\nKeep the supplied message text intact.\n\nRetain paragraph boundaries.\nBREAKING CHANGE: Consumers must supply explicit commit fields.\nRefs: #473, #460\nReviewed-by: Template Maintainers\nnative exit code: 1\nstdout:\n\u001b[90m⧗\u001b[39m   --- input ---\n\u001b[1m# template=commit version=comparison-only\n\nfeat(templates)!: Preserve authored commit framing\n\nKeep the supplied message text intact.\n\nRetain paragraph boundaries.\n\nBREAKING CHANGE: Consumers must supply explicit commit fields.\nRefs: #473, #460\nReviewed-by: Template Maintainers\u001b[22m\n\u001b[31m✖\u001b[39m   type may not be empty \u001b[90m[type-empty]\u001b[39m\n\u001b[31m✖\u001b[39m   subject may not be empty \u001b[90m[subject-empty]\u001b[39m\n\n\u001b[1m\u001b[31m✖\u001b[39m   found 2 problems, 0 warnings\u001b[22m\nⓘ   Get help: https://github.com/conventional-changelog/commitlint/#what-is-commitlint\n\n\nstderr:\n"
            },
            "request_rejection": null,
            "invocation": {
              "adapter": {
                "adapter_id": "commitlint",
                "version": "1.0.0",
                "fingerprint": "33ygyZvwX7L9eAnv",
                "contract_version": 1
              },
              "capture": {
                "exit_code": 1,
                "stdout": {
                  "observed_bytes": 1257,
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
            "termination_problem": null,
            "housekeeping": [],
            "args_source": "configured",
            "effective_args": []
          }
        ],
        "error_code": null,
        "error_details": null,
        "housekeeping": [],
        "path": ".pgmcp/temp/issue473-comparison-05/commit.v2-filled-render.txt",
        "content_changed": false,
        "selected_source": "input",
        "template_id": "commit",
        "extension": null,
        "selection_reason": null
      }
    },
    {
      "file": "commit.v2-minimal-render.txt",
      "uri": "pgmcp://cache/runs/9c502e4c6d4d4ef4bf1ca8103fac5257",
      "result": {
        "success": true,
        "written": true,
        "validation_policy": "report",
        "validation_status": "failed",
        "profile_id": "commit_preflight",
        "checks": [
          {
            "check_id": "commit_message",
            "status": "failed",
            "reason": null,
            "message": "Commitlint rejected the checked message.",
            "evidence": {
              "format": "text",
              "data": "checked message view (original supplied content):\n# template=commit version=comparison-only\n\nfix: Keep caller intent\n\nnative exit code: 1\nstdout:\n\u001b[90m⧗\u001b[39m   --- input ---\n\u001b[1m# template=commit version=comparison-only\n\nfix: Keep caller intent\u001b[22m\n\u001b[31m✖\u001b[39m   type may not be empty \u001b[90m[type-empty]\u001b[39m\n\u001b[31m✖\u001b[39m   subject may not be empty \u001b[90m[subject-empty]\u001b[39m\n\n\u001b[1m\u001b[31m✖\u001b[39m   found 2 problems, 0 warnings\u001b[22m\nⓘ   Get help: https://github.com/conventional-changelog/commitlint/#what-is-commitlint\n\n\nstderr:\n"
            },
            "request_rejection": null,
            "invocation": {
              "adapter": {
                "adapter_id": "commitlint",
                "version": "1.0.0",
                "fingerprint": "33ygyZvwX7L9eAnv",
                "contract_version": 1
              },
              "capture": {
                "exit_code": 1,
                "stdout": {
                  "observed_bytes": 821,
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
            "termination_problem": null,
            "housekeeping": [],
            "args_source": "configured",
            "effective_args": []
          }
        ],
        "error_code": null,
        "error_details": null,
        "housekeeping": [],
        "path": ".pgmcp/temp/issue473-comparison-05/commit.v2-minimal-render.txt",
        "content_changed": false,
        "selected_source": "input",
        "template_id": "commit",
        "extension": null,
        "selection_reason": null
      }
    },
    {
      "file": "commit.v3-authored-empty.txt",
      "uri": "pgmcp://cache/runs/1a6440d83a944ed2a16ea6180bbacd10",
      "result": {
        "success": true,
        "written": true,
        "validation_policy": "report",
        "validation_status": "passed",
        "profile_id": "commit_preflight",
        "checks": [
          {
            "check_id": "commit_message",
            "status": "passed",
            "reason": null,
            "message": null,
            "evidence": {
              "format": "text",
              "data": "checked message view (first valid provenance line removed):\n\nfix!: Preserve body spacing\n\nAUTHORED_START\n\n\n\nAUTHORED_END\n\nRefs: \n\n\n\n\n\nnative exit code: 0\nstdout:\n\nstderr:\n"
            },
            "request_rejection": null,
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
                  "observed_bytes": 326,
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
            "termination_problem": null,
            "housekeeping": [],
            "args_source": "configured",
            "effective_args": []
          }
        ],
        "error_code": null,
        "error_details": null,
        "housekeeping": [],
        "path": ".pgmcp/temp/issue473-comparison-05/commit.v3-authored-empty.txt",
        "content_changed": false,
        "selected_source": "input",
        "template_id": "commit",
        "extension": null,
        "selection_reason": null
      }
    },
    {
      "file": "commit.v3-filled.txt",
      "uri": "pgmcp://cache/runs/47cf94594c304a238c54f030e6debe3c",
      "result": {
        "success": true,
        "written": true,
        "validation_policy": "report",
        "validation_status": "passed",
        "profile_id": "commit_preflight",
        "checks": [
          {
            "check_id": "commit_message",
            "status": "passed",
            "reason": null,
            "message": null,
            "evidence": {
              "format": "text",
              "data": "checked message view (first valid provenance line removed):\n\nfeat(templates)!: Preserve authored commit framing\n\nKeep the supplied message text intact.\n\nRetain paragraph boundaries.\n\nBREAKING CHANGE: Consumers must supply explicit commit fields.\n\nRefs: #473, #460\n\nReviewed-by: Template Maintainers\n\n\n\nnative exit code: 0\nstdout:\n\nstderr:\n"
            },
            "request_rejection": null,
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
                  "observed_bytes": 494,
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
            "termination_problem": null,
            "housekeeping": [],
            "args_source": "configured",
            "effective_args": []
          }
        ],
        "error_code": null,
        "error_details": null,
        "housekeeping": [],
        "path": ".pgmcp/temp/issue473-comparison-05/commit.v3-filled.txt",
        "content_changed": false,
        "selected_source": "input",
        "template_id": "commit",
        "extension": null,
        "selection_reason": null
      }
    },
    {
      "file": "commit.v3-minimal.txt",
      "uri": "pgmcp://cache/runs/2718005b87f0429c89734dc29aee130c",
      "result": {
        "success": true,
        "written": true,
        "validation_policy": "report",
        "validation_status": "passed",
        "profile_id": "commit_preflight",
        "checks": [
          {
            "check_id": "commit_message",
            "status": "passed",
            "reason": null,
            "message": null,
            "evidence": {
              "format": "text",
              "data": "checked message view (first valid provenance line removed):\n\nfix: Keep caller intent\n\n\n\nnative exit code: 0\nstdout:\n\nstderr:\n"
            },
            "request_rejection": null,
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
                  "observed_bytes": 270,
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
            "termination_problem": null,
            "housekeeping": [],
            "args_source": "configured",
            "effective_args": []
          }
        ],
        "error_code": null,
        "error_details": null,
        "housekeeping": [],
        "path": ".pgmcp/temp/issue473-comparison-05/commit.v3-minimal.txt",
        "content_changed": false,
        "selected_source": "input",
        "template_id": "commit",
        "extension": null,
        "selection_reason": null
      }
    },
    {
      "file": "typescript_dto.v2-colon-type-render.ts",
      "uri": "pgmcp://cache/runs/818b8345e4764347bd5d01861c782b28",
      "result": {
        "success": true,
        "written": true,
        "validation_policy": "report",
        "validation_status": "failed",
        "profile_id": "typescript_preflight",
        "checks": [
          {
            "check_id": "typescript_syntax",
            "status": "failed",
            "reason": null,
            "message": "')' expected.",
            "evidence": {
              "format": "text",
              "data": ".pgmcp/temp/issue473-comparison-05/typescript_dto.v2-colon-type-render.ts(9,34): error TS1005: ')' expected.\r\n.pgmcp/temp/issue473-comparison-05/typescript_dto.v2-colon-type-render.ts(11,20): error TS1005: ')' expected.\r\n"
            },
            "request_rejection": null,
            "invocation": {
              "adapter": {
                "adapter_id": "typescript_syntax",
                "version": "1.0.0",
                "fingerprint": "asfu0uAAuaq6247x",
                "contract_version": 1
              },
              "capture": {
                "exit_code": 1,
                "stdout": {
                  "observed_bytes": 385,
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
        "path": ".pgmcp/temp/issue473-comparison-05/typescript_dto.v2-colon-type-render.ts",
        "content_changed": false,
        "selected_source": "input",
        "template_id": "typescript_dto",
        "extension": null,
        "selection_reason": null
      }
    },
    {
      "file": "typescript_dto.v2-filled-render.ts",
      "uri": "pgmcp://cache/runs/c29390d3e0314feaae42d4516c3e1a35",
      "result": {
        "success": true,
        "written": true,
        "validation_policy": "report",
        "validation_status": "failed",
        "profile_id": "typescript_preflight",
        "checks": [
          {
            "check_id": "typescript_syntax",
            "status": "failed",
            "reason": null,
            "message": "Expression expected.",
            "evidence": {
              "format": "text",
              "data": ".pgmcp/temp/issue473-comparison-05/typescript_dto.v2-filled-render.ts(24,16): error TS1109: Expression expected.\r\n.pgmcp/temp/issue473-comparison-05/typescript_dto.v2-filled-render.ts(24,28): error TS1109: Expression expected.\r\n"
            },
            "request_rejection": null,
            "invocation": {
              "adapter": {
                "adapter_id": "typescript_syntax",
                "version": "1.0.0",
                "fingerprint": "asfu0uAAuaq6247x",
                "contract_version": 1
              },
              "capture": {
                "exit_code": 1,
                "stdout": {
                  "observed_bytes": 399,
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
        "path": ".pgmcp/temp/issue473-comparison-05/typescript_dto.v2-filled-render.ts",
        "content_changed": false,
        "selected_source": "input",
        "template_id": "typescript_dto",
        "extension": null,
        "selection_reason": null
      }
    },
    {
      "file": "typescript_dto.v2-minimal-render.ts",
      "uri": "pgmcp://cache/runs/a06d846f52fb42ff9eda4bb949d1bd58",
      "result": {
        "success": true,
        "written": true,
        "validation_policy": "report",
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
        "path": ".pgmcp/temp/issue473-comparison-05/typescript_dto.v2-minimal-render.ts",
        "content_changed": false,
        "selected_source": "input",
        "template_id": "typescript_dto",
        "extension": null,
        "selection_reason": null
      }
    },
    {
      "file": "typescript_dto.v3-colon-type.ts",
      "uri": "pgmcp://cache/runs/e24538e238c140648020753e11eedc7c",
      "result": {
        "success": true,
        "written": true,
        "validation_policy": "report",
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
        "path": ".pgmcp/temp/issue473-comparison-05/typescript_dto.v3-colon-type.ts",
        "content_changed": false,
        "selected_source": "input",
        "template_id": "typescript_dto",
        "extension": null,
        "selection_reason": null
      }
    },
    {
      "file": "typescript_dto.v3-empty-fields.ts",
      "uri": "pgmcp://cache/runs/06413030404a40d58139ad776b43fa12",
      "result": {
        "success": true,
        "written": true,
        "validation_policy": "report",
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
        "path": ".pgmcp/temp/issue473-comparison-05/typescript_dto.v3-empty-fields.ts",
        "content_changed": false,
        "selected_source": "input",
        "template_id": "typescript_dto",
        "extension": null,
        "selection_reason": null
      }
    },
    {
      "file": "typescript_dto.v3-filled.ts",
      "uri": "pgmcp://cache/runs/f41c698f2ce2443993ca0090f7a31978",
      "result": {
        "success": true,
        "written": true,
        "validation_policy": "report",
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
        "path": ".pgmcp/temp/issue473-comparison-05/typescript_dto.v3-filled.ts",
        "content_changed": false,
        "selected_source": "input",
        "template_id": "typescript_dto",
        "extension": null,
        "selection_reason": null
      }
    },
    {
      "file": "typescript_dto.v3-minimal.ts",
      "uri": "pgmcp://cache/runs/daf3336368334548a383aef935cbf262",
      "result": {
        "success": true,
        "written": true,
        "validation_policy": "report",
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
        "path": ".pgmcp/temp/issue473-comparison-05/typescript_dto.v3-minimal.ts",
        "content_changed": false,
        "selected_source": "input",
        "template_id": "typescript_dto",
        "extension": null,
        "selection_reason": null
      }
    }
  ],
  "message_view_checks": [
    {
      "source": "commit.v2-minimal-render.txt",
      "file": "commit.v2-minimal-message-view.txt",
      "uri": "pgmcp://cache/runs/b435c0d649ce40dca9b79dbc734c5523",
      "result": {
        "success": true,
        "written": true,
        "validation_policy": "report",
        "validation_status": "passed",
        "profile_id": "commit_preflight",
        "checks": [
          {
            "check_id": "commit_message",
            "status": "passed",
            "reason": null,
            "message": null,
            "evidence": {
              "format": "text",
              "data": "checked message view (original supplied content):\n\nfix: Keep caller intent\n\nnative exit code: 0\nstdout:\n\nstderr:\n"
            },
            "request_rejection": null,
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
                  "observed_bytes": 256,
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
            "termination_problem": null,
            "housekeeping": [],
            "args_source": "configured",
            "effective_args": []
          }
        ],
        "error_code": null,
        "error_details": null,
        "housekeeping": [],
        "path": ".pgmcp/temp/issue473-native-tooling/commit.v2-minimal-message-view.txt",
        "content_changed": true,
        "selected_source": "input",
        "template_id": "commit",
        "extension": null,
        "selection_reason": null
      }
    },
    {
      "source": "commit.v2-filled-render.txt",
      "file": "commit.v2-filled-message-view.txt",
      "uri": "pgmcp://cache/runs/f6e159a7d6ca4de087b397aff043d300",
      "result": {
        "success": true,
        "written": true,
        "validation_policy": "report",
        "validation_status": "passed",
        "profile_id": "commit_preflight",
        "checks": [
          {
            "check_id": "commit_message",
            "status": "passed",
            "reason": null,
            "message": null,
            "evidence": {
              "format": "text",
              "data": "checked message view (original supplied content):\n\nfeat(templates)!: Preserve authored commit framing\n\nKeep the supplied message text intact.\n\nRetain paragraph boundaries.\nBREAKING CHANGE: Consumers must supply explicit commit fields.\nRefs: #473, #460\nReviewed-by: Template Maintainers\nnative exit code: 0\nstdout:\n\nstderr:\n"
            },
            "request_rejection": null,
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
                  "observed_bytes": 472,
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
            "termination_problem": null,
            "housekeeping": [],
            "args_source": "configured",
            "effective_args": []
          }
        ],
        "error_code": null,
        "error_details": null,
        "housekeeping": [],
        "path": ".pgmcp/temp/issue473-native-tooling/commit.v2-filled-message-view.txt",
        "content_changed": true,
        "selected_source": "input",
        "template_id": "commit",
        "extension": null,
        "selection_reason": null
      }
    }
  ],
  "contract_tests": {
    "uri": "pgmcp://cache/runs/b0f17617cd4244aab1ffb87cb9bf376d",
    "result": {
      "success": true,
      "requested_scope": "targets",
      "requested_targets": [
        "tests/mcp_server/integration/templates/test_typescript_artifact.py",
        "tests/mcp_server/integration/templates/test_commit_artifact.py"
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
            "data": "============================= test session starts =============================\r\nplatform win32 -- Python 3.13.7, pytest-9.0.2, pluggy-1.6.0\r\nrootdir: C:\\temp\\pgmcp\r\nconfigfile: pyproject.toml\r\nplugins: anyio-4.12.1, asyncio-1.3.0, cov-7.0.0, xdist-3.8.0\r\nasyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function\r\ncollected 8 items\r\n\r\ntests\\mcp_server\\integration\\templates\\test_typescript_artifact.py ....  [ 50%]\r\ntests\\mcp_server\\integration\\templates\\test_commit_artifact.py ....      [100%]\r\n\r\n============================== warnings summary ===============================\r\n..\\..\\Users\\miche\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\pydantic\\_internal\\_fields.py:198\r\n  C:\\Users\\miche\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\pydantic\\_internal\\_fields.py:198: UserWarning: Field name \"schema\" in \"SchemaAttachment\" shadows an attribute in parent \"BaseModel\"\r\n    warnings.warn(\r\n\r\n-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html\r\n======================== 8 passed, 1 warning in 29.85s ========================\r\n"
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
              "observed_bytes": 1432,
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
            "0"
          ]
        }
      ],
      "error_code": null,
      "error_details": null
    }
  }
}
```

## Version History

| Version | Date | Author | Change |
| --- | --- | --- | --- |
| 0.1 | 2026-10-03 | @imp researcher | Install authorized project-pinned native prerequisites; rerun unchanged TypeScript/Commit outputs, isolate old message framing and re-execute eight existing native contract tests. |
