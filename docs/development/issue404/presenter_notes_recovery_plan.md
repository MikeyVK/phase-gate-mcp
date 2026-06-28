<!-- docs\development\issue404\presenter_notes_recovery_plan.md -->
<!-- template=generic_doc version=43c84181 created=2026-06-17T21:35Z updated= -->
# Presenter Notes Recovery Plan

This document outlines the detailed technical recovery plan for the presenter-driven notes redesign (Topic 1) and exception mapping under Issue #404.

---

## 1. Pydantic Config Schema Extensions (`presentation_config.py`)

To prevent server startup crashes due to `extra="forbid"`, we will extend the configuration schemas in `mcp_server/config/schemas/presentation_config.py`:

```python
class FormattingConfig(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    none_value: str = "-"

class NoteGroupConfig(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    emoji: str
    header: str

class GlobalNotesConfig(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    groups: dict[str, NoteGroupConfig] = Field(default_factory=dict)
    templates: dict[str, dict[str, str]] = Field(default_factory=dict)

class GlobalPresentationConfig(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    emojis: EmojisConfig = Field(default_factory=EmojisConfig)
    default_failure_template: str = "Failed: {error_message}"
    next_instruction_texts: dict[str, str] = Field(default_factory=dict)
    
    # New configurations
    formatting: FormattingConfig = Field(default_factory=FormattingConfig)
    notes: GlobalNotesConfig = Field(default_factory=GlobalNotesConfig)
    failures: dict[str, str] = Field(default_factory=dict)

class ToolPresentationConfig(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    template_success: str | None = None
    template_failure: str | None = None
    next_instructions: list[str] = Field(default_factory=list)
    
    # Allowed note groups for tool-local templates
    exclusions: dict[str, str] = Field(default_factory=dict)
    suggestions: dict[str, str] = Field(default_factory=dict)
    recoveries: dict[str, str] = Field(default_factory=dict)
    info: dict[str, str] = Field(default_factory=dict)
```

---

## 2. Note Rendering Loop & Multiplicity

`TextPresenter` will implement a new public method `present_notes(tool_name: str, notes: list[NoteEntry]) -> str | None` to format and group notes:

1. Retrieve the tool configuration `tool_cfg = self.tools_config.get(tool_name)`.
2. Retrieve the global note groups configuration `groups_cfg = self.global_config.notes.groups`.
3. Initialize an empty dictionary of grouped rendered notes: `grouped_texts = {group_name: [] for group_name in groups_cfg}`.
4. For each note in `notes`:
   - Obtain its `key` and `params` (either natively or via the translation mapper).
   - Look up the template template string:
     - **First path (local):** Check `tool_cfg.<group_name>.<key>`.
     - **Second path (global fallback):** Check `global.notes.templates.<group_name>.<key>`.
   - Resolve the template placeholders using `params` (applying the `none_value` fallback filter).
   - Append the rendered string to `grouped_texts[group_name]`.
5. Format the markdown output:
   - For each group with items (in order: `exclusions`, `suggestions`, `recoveries`, `info`):
     - Append the group's emoji and header (e.g. `🚫 Excluded files:`).
     - Append each note as an indented bullet point (`  - {note_text}`).
6. Return the joined string block.

---

## 3. Backward Compatibility Mapper (Phase 1 Bridge)

To allow incremental migration of the 368 missing notes across the manager and adapter layers, we retain the typed note classes as pure metadata dataclasses and implement a translation mapper:

```python
def map_legacy_note_to_event(note: NoteEntry) -> tuple[str, dict[str, Any]]:
    """Maps legacy typed notes to generic key-parameter tuples for the presenter."""
    if isinstance(note, ExclusionNote):
        return "file_excluded", {"file_path": note.file_path}
    elif isinstance(note, SuggestionNote):
        return "suggestion_message", {"message": note.message, "subject": note.subject}
    elif isinstance(note, BlockerNote):
        return "blocker_message", {"message": note.message}
    elif isinstance(note, RecoveryNote):
        return "recovery_message", {"message": note.message}
    elif isinstance(note, InfoNote):
        return "info_message", {"message": note.message}
    elif hasattr(note, "key"):
        return note.key, getattr(note, "params", {})
    return "unknown_note", {"message": str(note)}
```

During Phase 1, `NoteContext.render_to_response` will route formatting requests through `TextPresenter.present_notes`. The legacy `to_message()` methods are kept temporarily for unit test backward compatibility but will be completely removed by the end of the issue (Clean Break).

---

## 4. Architectural Rules & Design Refinements

### 4.1. Global Note Templates Fallback (DRY & SSOT)
To prevent duplicating shared note templates (e.g., manager-produced warnings like `"Working directory is not clean"`) across every tool namespace, the presenter will fallback to `global.notes.templates.<group_name>.<key>` in `presentation.yaml` when a tool-local template is missing.

### 4.2. Error Code Mapping for Custom Exceptions
To comply with the Config-First principle, custom exceptions raised by our code (e.g., `PreflightError`, `ValidationError`, `DeliverableCheckError`) must carry an `error_code` and semantic parameters instead of hardcoded strings:
- **Exception Structure:** `raise PreflightError(error_code="dirty_workdir", params={"branch": branch})`
- **YAML Config:** `global.failures.dirty_workdir: "Branch '{branch}' is not in a clean state -- commit or stash changes."`
- **Presenter Resolution:** The presenter catches the custom exception, looks up `global.failures.<error_code>`, resolves placeholders, and presents the text. Raw/unexpected external exceptions (e.g., subprocess crashes) fallback to `default_failure_template` using the raw exception message.

### 4.3. Strict "No-Message-Backdoor" Rule
To prevent developers from bypassing the configuration-driven design by passing hardcoded strings in Python:
1. **No `{message}` or `{error_message}` parameters:** The `params` of any note or custom exception must contain ONLY raw semantic data (file paths, counts, branch names), **never** user-facing sentences, phrases, or pre-formatted strings.
2. **Validator Enforcement:** The drift validator (`validate_presentation_alignment`) will scan all templates in `presentation.yaml`. If it detects `{message}` or `{error_message}` within any custom note or failure template, it will raise a startup `ConfigError`, failing boot. (Note: `{error_message}` is permitted only in `global.default_failure_template` for raw external exceptions).

### 4.4. Drift Validator Extension (`validate_presentation_alignment`)
We extend the drift validator to verify that:
1. All placeholders inside `global.failures.<error_type>` exist as fields in the corresponding `ToolErrorOutput` DTO class.
2. Placeholders in tool-local and global note templates correspond to the constructor parameters of the mapped note classes.
