<!-- docs\development\issue404\pr.md -->
<!-- template=pr version=93bb9b4e created=2026-06-18T10:46Z updated= -->
# Resolve TextPresenter formatting gaps (#404)

This PR resolves the formatting gaps in TextPresenter and establishes a taxonomical error propagation bridge. Hardcoded visual emojis, failure templates, and note group configurations are removed from Python and fully schema-driven via presentation.yaml. None values format safely to '-' without standard library crashes. Legacy note subclasses and Python to_message methods are completely removed (Clean Break).
## Changes
Extends presentation_config.py with Pydantic configuration schemas. Defines base ToolErrorOutput and error DTO subclasses in error_outputs.py. Implements Note(key, params) generic dataclass and SafeNoneFormatter. Decouples NoteContext from rendering and routes notes to TextPresenter.present_notes in server.py. Extends validate_presentation_alignment with parameter blacklist. Migrates note production in all managers/adapters/tools and cleans up dead code.

## Testing
2873 passed tests in pytest. Quality gates passed on branch scope.
## Checklist

- [ ] Run full test suite
- [ ] Verify quality gates
- [ ] Verify template validation alignment
- [ ] Verify None-formatting behavior

## Related Documentation
- **[docs/development/issue404/design.md][related-1]**
- **[docs/development/issue404/validation.md][related-2]**

---

Closes: #404