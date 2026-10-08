# docs/reference/MAINTENANCE_SCRIPTS.md

**Status:** APPROVED  
**Version:** 1.1  
**Last Updated:** 2026-10-08

---

## Purpose

Ready-to-use PowerShell scripts for documentation maintenance tasks. Run these during weekly, monthly, or emergency maintenance cycles.

## Scope

**In scope:** PowerShell scripts for doc auditing, duplicate detection, orphan finding  
**Out of scope:** Content authoring and general modernization of historical maintenance examples.

---

## File Size Audit

Find documents exceeding their size limits:

```powershell
# List all docs by size (descending)
Get-ChildItem docs -Recurse -Filter "*.md" | 
    Select-Object FullName, @{
        Name="Lines"
        Expression={(Get-Content $_.FullName | Measure-Object -Line).Lines}
    } |
    Sort-Object Lines -Descending

# Find oversized docs (respects architecture/ 1000-line limit)
Get-ChildItem docs -Recurse -Filter "*.md" | 
    Where-Object {
        $lines = (Get-Content $_.FullName | Measure-Object -Line).Lines
        $limit = if ($_.FullName -match "\\architecture\\") { 1000 } else { 300 }
        $lines -gt $limit
    } | 
    Select-Object @{
        Name="File"; Expression={$_.Name}
    }, @{
        Name="Lines"; Expression={(Get-Content $_.FullName | Measure-Object -Line).Lines}
    }, @{
        Name="Limit"; Expression={if ($_.FullName -match "\\architecture\\") { 1000 } else { 300 }}
    }
```

---

## Duplication Check

Search for repeated patterns that should be consolidated:

```powershell
# Search for pattern in all docs (adjust keywords as needed)
Get-ChildItem docs -Recurse -Filter "*.md" | 
    Select-String -Pattern "TDD workflow" | 
    Group-Object Path | 
    Select-Object Count, Name

# Other common patterns to check:
# "quality gates", "Point-in-Time", "frozen=True"

# If count > 3, consolidate to single source with links
```

---

## Orphan Detection

Find .md files not linked from any README.md:

```powershell
# Step 1: Get all .md files (excluding READMEs)
$allDocs = Get-ChildItem docs -Recurse -Filter "*.md" | 
    Where-Object { $_.Name -ne "README.md" } | 
    Select-Object -ExpandProperty Name

# Step 2: Get all links from README files
$linkedDocs = Get-ChildItem docs -Recurse -Filter "README.md" | 
    ForEach-Object { Get-Content $_.FullName } | 
    Select-String -Pattern "\[.*\]\((.*\.md)" -AllMatches | 
    ForEach-Object { $_.Matches.Groups[1].Value } | 
    ForEach-Object { Split-Path $_ -Leaf } | 
    Sort-Object -Unique

# Step 3: Find orphans
$allDocs | Where-Object { $_ -notin $linkedDocs }
```

---

## Broken Link Check

Use PGMCP's native `markdown_link_review` profile for the selected active documentation. Lychee 0.24.2 (adapter 2.0.0) checks local destinations and fragments with `--offline --cache=false --include-fragments`. Offline success does not certify external HTTP availability.

### Inventory and reading bases

Run this read-only selection from the workspace root; normalize separators before grouping. Pass the resulting arrays as explicit tool targets.

```powershell
$normal = @('README.md', 'CHANGELOG.md', 'AGENTS.md',
    'docs/development/schema-template-maintenance.md',
    'docs/development/MAINTENANCE_SCRIPTS.md',
    'docs/development/issue460/deferred-work.md',
    'mcp_server/resources/cache_reading.md') + @(
    rg --files docs/setup docs/reference docs/manuals docs/coding_standards -g '*.md'
)
$normal = @($normal -replace '\\', '/' |
    Where-Object { $_ -ne 'docs/reference/migration_v2.0.md' } | Sort-Object -Unique)
$instructions = @(rg --files --hidden docs/agents .agents .github -g '*.md' -g '!**/archive/**')
$instructions = @($instructions -replace '\\', '/' | Sort-Object -Unique)
$rootCopies = @($instructions | Where-Object {
    $_ -match '^(docs/agents/(codex|antigravity|vscode/copilot)|\.agents)/AGENTS\.md$'
})
$roles = @($instructions | Where-Object { $_ -match '^docs/agents/(codex|antigravity)/rules/' })
$workflows = @($instructions | Where-Object { $_ -match '^docs/agents/(codex|antigravity)/workflows/' })
$vscodeAgents = @($instructions | Where-Object { $_ -match '^docs/agents/vscode/copilot/\.github/agents/' })
$contextual = @($rootCopies) + @($roles) + @($workflows) + @($vscodeAgents)
$natural = @($instructions | Where-Object { $_ -notin $contextual })
# Build each table entry's file URI from the actual workspace root:
$rootBase = ([uri](Join-Path (Get-Location).Path 'AGENTS.md')).AbsoluteUri
```

| Targets | Files at the 2026-10-08 baseline | Reading base |
|---|---:|---|
| `$normal` | 56 | Each document's own path |
| `$natural` | 31 | Each source/runtime file's own path |
| `$rootCopies` | 4 | Workspace-root `AGENTS.md` |
| `$roles` | 7 | Workspace `.agents/rules/imp.agent.md` |
| `$workflows` | 11 | Workspace `.agents/workflows/go.md` |
| `$vscodeAgents` | 3 | Workspace `.github/agents/imp.agent.md` |

These are 112 distinct input files. Sources stored under `docs/agents` can contain paths intended for their deployment location; the existing native selection-check `--base-url` supplies that reading base. Its filename anchors the containing directory for these references. The [release procedure](../reference/release-assets-procedure.md) and [bootstrap layout](../setup/agentic-bootstrap.md) own deployment. This does not change mutation preflight behavior or certify a separately installed Antigravity host.

Historical issue artifacts, `docs/development/archive`, archived prompts, the explicitly HISTORICAL `migration_v2.0.md`, implementation-adjacent legacy notes, generated assets, caches and temporary files are outside the input inventory. Archived files remain valid destinations. The active #460 deferred register is explicitly included. Check new issue-local artifacts separately; do not blanket-exclude an instruction family.

### Native calls and observed outcome

For `$normal` and `$natural`, call:

```python
run_checks(scope="targets", targets=<selected array>,
           profile="markdown_link_review", timeout_seconds=120)
```

For each of the other four arrays, call the same native check with its table entry converted to a workspace-root-derived file URI:

```python
run_checks(scope="targets", targets=<selected array>, checks=["markdown_links"],
           args={"markdown_links": ["--offline", "--cache=false",
                 "--include-fragments", "--base-url", <reading-base file URI>]},
           timeout_seconds=120)
```

The 2026-10-08 survey found 21 missing local link occurrences in six documents: nine ordinary path errors, three obsolete maintenance references and nine historical source citations. #471 repairs the paths, removes the unsupported references and pins the historical citations to verified commit `79759183272e28ddbc68b9b1023168a63bd79cbb`. No fragment failures were observed. The pinned source paths were verified in the local Git tree; HTTP reachability is outside the offline claim.

| Group | Successful occurrences | Excluded occurrences | Errors / timeouts | Native exit |
|---|---:|---:|---|---:|
| Normal documentation | 525 | 16 | 0 / 0 | 0 |
| Natural instruction bases | 45 | 0 | 0 / 0 | 0 |
| Root-base AGENTS copies | 44 | 0 | 0 / 0 | 0 |
| Role sources | 25 | 0 | 0 / 0 | 0 |
| Workflow sources | 17 | 0 | 0 / 0 | 0 |
| VS Code agent sources | 12 | 0 | 0 / 0 | 0 |

The final normal-group check and reused, unchanged instruction checks all completed without capture truncation: 668 successful occurrences, 16 exclusions and zero errors/timeouts across 112 files. The 16 offline exclusions are external URLs: nine historical source citations, the #471 issue link, two specification links and four CHANGELOG links. All 24 Codex/VS Code source/runtime pairs were byte-equivalent. Run IDs may supplement these recorded invocations and outcomes, not replace them. This baseline adds no CI obligation, test coverage claim or new gate.

---

## Emergency Cleanup Procedure

When documentation becomes chaotic (multiple files >400 lines, conflicting info, outdated indices):

```powershell
# 1. Create emergency branch
git checkout -b docs/emergency-cleanup

# 2. Triage - list all docs by size
Get-ChildItem docs -Recurse -Filter "*.md" | 
    Select-Object FullName, @{
        Name="Lines"
        Expression={(Get-Content $_.FullName | Measure-Object -Line).Lines}
    } |
    Sort-Object Lines -Descending |
    Format-Table -AutoSize

# 3. Find repeated content
Get-ChildItem docs -Recurse -Filter "*.md" | 
    Select-String -Pattern "specific phrase from duplicated content" |
    Format-Table Path, LineNumber, Line -AutoSize

# 4. After fixes, commit with clear message
git add docs/
git commit -m "docs: emergency cleanup - restore modular structure

Problem: Documentation grew to unmanageable state
- X files exceeded 400 lines (split into focused docs)
- Found Y concept duplicated in Z places (consolidated)
- Updated all README indices with current structure

Result: Back to <300 lines per doc, single source of truth"

# 5. Merge
git checkout main
git merge --no-ff docs/emergency-cleanup
```

---

## Related Documentation

- [Quality tool reference](../reference/tools/quality.md) - Native check selection and invocation
- [Documentation Standard](../coding_standards/DOCUMENTATION_STANDARD.md) - Documentation and durable evidence rules

---

## Version History

| Version | Date | Changes |
|---------|------|---------|  
| 1.0 | 2025-11-27 | Initial creation, extracted from DOCUMENTATION_MAINTENANCE.md |
| 1.1 | 2026-10-08 | Replace regex link example with the native active-documentation baseline and remove unavailable references (#471). |

<!-- ═══════════════════════════════════════════════════════════════════════════
     LINK DEFINITIONS
     ═══════════════════════════════════════════════════════════════════════════ -->