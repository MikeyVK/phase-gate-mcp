<!-- .st3\temp\issue_render.md -->
<!-- template=issue version=8dd42510 created=2026-04-24T12:57Z updated= -->
# Phase F: Extend SafeEdit validators (YAML/JSON/TOML)

## Problem
safe_edit_file valideert markdown en Python na edits, maar YAML/JSON/TOML-bestanden (waaronder alle .st3/ configuratiebestanden) worden niet gevalideerd. Een syntax-fout in phase_contracts.yaml of enforcement.yaml wordt niet gedetecteerd bij de edit.

## Expected Behavior

YAMLValidator, JSONValidator en TOMLValidator naast de bestaande MarkdownValidator en PythonValidator, zodat safe_edit_file alle relevante bestandstypes kan valideren na een edit.
## Actual Behavior

Gedeeltelijk gerealiseerd: MarkdownValidator en PythonValidator zijn aanwezig in mcp_server/validation/. YAMLValidator, JSONValidator en TOMLValidator zijn niet geïmplementeerd. De validators zijn low priority t.o.v. deployment-blockers (#260, Focus A, Focus B). Concrete behoefte kan als apart issue worden heropend wanneer SafeEdit uitbreiding op de roadmap staat.
## Context

Child van #18 (Epic: Enforce TDD & Coverage via Hard Tooling). SafeEdit validators zijn onderdeel van de bredere safe_edit_file-tool kwaliteitsverbetering.
## Related Documentation
- **[mcp_server/validation/][related-1]**
