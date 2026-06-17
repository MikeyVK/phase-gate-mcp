# mcp_server/presenters/text_presenter.py
# template=service version=5d5b489a created=2026-06-12T20:49Z updated=2026-06-12T21:00Z
"""Text presenter service.

@layer: Presenters
"""

import string
from typing import Any, cast

from pydantic import BaseModel

from mcp_server.config.schemas.presentation_config import (
    EmojisConfig,
    GlobalPresentationConfig,
    PresentationConfig,
    ToolPresentationConfig,
)
from mcp_server.core.exceptions import ConfigError
from mcp_server.core.operation_notes import (
    BlockerNote,
    ExclusionNote,
    InfoNote,
    Note,
    NoteEntry,
    RecoveryNote,
    SuggestionNote,
)


class SafeNoneFormatter(string.Formatter):
    """Subclass of string.Formatter that formats None values without errors."""

    def __init__(self, none_value: str = "-") -> None:
        super().__init__()
        self.none_value = none_value

    def format_field(self, value: Any, format_spec: str) -> str:
        if value is None:
            return self.none_value
        try:
            return str(super().format_field(value, format_spec))
        except (ValueError, TypeError):
            return str(value)


def map_legacy_note_to_event(note: NoteEntry) -> tuple[str, dict[str, Any]]:
    """Maps legacy typed notes to generic key-parameter tuples for the presenter.

    # TODO: Remove in Cycle 6 (Clean Break)
    """
    if isinstance(note, Note):
        return note.key, note.params
    elif isinstance(note, ExclusionNote):
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
        return getattr(note, "key"), getattr(note, "params", {})
    return "unknown_note", {"message": str(note)}


class TextPresenter:
    """Formats structured tool outputs into markdown text fallbacks using templates."""

    global_config: GlobalPresentationConfig | dict[str, Any]
    tools_config: dict[str, ToolPresentationConfig | dict[str, Any]]

    def __init__(
        self,
        config_data: dict[str, Any] | None = None,
        config: PresentationConfig | None = None,
    ) -> None:
        """Initialize presenter with config data or PresentationConfig object."""
        if config is not None:
            # Extract from PresentationConfig object
            self.global_config = config.global_settings
            self.tools_config = cast(
                dict[str, ToolPresentationConfig | dict[str, Any]], config.tools
            )
        elif config_data is not None:
            # Extract from raw dictionary (tests)
            self.global_config = config_data.get("global", {})
            self.tools_config = config_data.get("tools", {})
        else:
            self.global_config = {}
            self.tools_config = {}

    def _get_emoji_config(self) -> EmojisConfig | dict[str, str]:
        """Get the emoji configuration dictionary or model."""
        if isinstance(self.global_config, dict):
            return cast(dict[str, str], self.global_config.get("emojis", {}))
        return self.global_config.emojis

    def get_next_instruction_texts(self) -> dict[str, str]:
        """Get the next instruction texts lookup dictionary."""
        if isinstance(self.global_config, dict):
            return cast(dict[str, str], self.global_config.get("next_instruction_texts", {}))
        return self.global_config.next_instruction_texts

    def _get_default_failure_template(self) -> str:
        """Get the default failure template."""
        if isinstance(self.global_config, dict):
            return str(
                self.global_config.get("default_failure_template", "Failed: {error_message}")
            )
        return self.global_config.default_failure_template

    def _is_complex(self, val: object) -> bool:
        """Check if a value represents complex structured data."""
        if isinstance(val, (list, dict, set, tuple)):
            return len(val) > 0
        return (
            isinstance(val, str)
            and "\n" in val
            and (val.startswith("diff ") or "@@ " in val or "\n+" in val or "\n-" in val)
        )

    def _get_none_value(self) -> str:
        """Get the placeholder string for None values."""
        if isinstance(self.global_config, dict):
            formatting = self.global_config.get("formatting", {})
            if isinstance(formatting, dict):
                return str(formatting.get("none_value", "-"))
            return getattr(formatting, "none_value", "-")
        formatting = getattr(self.global_config, "formatting", None)
        if formatting is not None:
            return getattr(formatting, "none_value", "-")
        return "-"

    def present(
        self,
        tool_name: str,
        success: bool,
        presentation_category: str,
        data: BaseModel | dict[str, Any],
    ) -> str:
        """Present the DTO or dict as a formatted string."""
        # 1. Convert DTO/dict to a flat dictionary for formatting
        data_dict = data.model_dump() if isinstance(data, BaseModel) else dict(data)

        # 2. Bepaal template op basis van success
        tool_cfg = self.tools_config.get(tool_name)
        template = None
        next_instructions = []

        if tool_cfg is not None:
            # Support both Pydantic model and raw dict for tool config
            if isinstance(tool_cfg, ToolPresentationConfig):
                template = tool_cfg.template_success if success else tool_cfg.template_failure
                next_instructions = tool_cfg.next_instructions
            else:
                template = (
                    tool_cfg.get("template_success")
                    if success
                    else tool_cfg.get("template_failure")
                )
                next_instructions = tool_cfg.get("next_instructions") or []

        # Fallback for failure template
        if not success and not template:
            # Try to resolve template via error_code if present
            error_code = None
            if isinstance(data, BaseModel):
                error_code = getattr(data, "error_code", None)
                if not error_code and hasattr(data, "params") and isinstance(data.params, dict):
                    error_code = data.params.get("error_code")
            elif isinstance(data, dict):
                error_code = data.get("error_code")
                if not error_code and isinstance(data.get("params"), dict):
                    error_code = data.get("params", {}).get("error_code")

            failures = {}
            if isinstance(self.global_config, dict):
                failures = self.global_config.get("failures", {})
            else:
                failures = getattr(self.global_config, "failures", {})

            if error_code and error_code in failures:
                template = failures[error_code]
            else:
                template = self._get_default_failure_template()

        # Format template if we have one, otherwise dump/default representation
        if template:
            try:
                # Fill missing keys in data_dict with None to trigger SafeNoneFormatter
                # Parse all placeholders in the template
                placeholders = []
                none_val = self._get_none_value()
                formatter = SafeNoneFormatter(none_val)
                for _, field_name, _, _ in formatter.parse(template):
                    if field_name is not None:
                        placeholders.append(field_name.split(".")[0].split("[")[0])

                format_dict = {}
                params_dict = data_dict.get("params", {}) or {}
                for key in placeholders:
                    val = None
                    if key in data_dict:
                        val = data_dict[key]
                    elif isinstance(params_dict, dict) and key in params_dict:
                        val = params_dict[key]
                    elif key == "error_message" and "message" in data_dict:
                        val = data_dict["message"]
                    elif key == "message" and "error_message" in data_dict:
                        val = data_dict["error_message"]
                    format_dict[key] = val

                text = formatter.format(template, **format_dict)
            except Exception as exc:
                text = f"Format error: {exc}"
        else:
            # If no template is found, use a fallback text or DTO string
            text = data_dict.get("message") or data_dict.get("error_message") or str(data_dict)
        # 3. Prepend emoji prefix
        emojis = self._get_emoji_config()
        emoji = ""
        if not success:
            if isinstance(emojis, dict):
                emoji = emojis.get("failure", "❌")
            else:
                emoji = getattr(emojis, "failure", "❌")
        else:
            # Map presentation_category to emoji
            cat = presentation_category.lower()
            if cat in ("mutation", "admin"):
                key = "success"
            elif cat in ("query", "testing"):
                key = "query"
            elif cat in ("bootstrap",):
                key = "bootstrap"
            else:
                key = "success"

            if isinstance(emojis, dict):
                emoji = emojis.get(key, "✅")
            else:
                emoji = getattr(emojis, key, "✅")

        if emoji:
            text = f"{emoji} {text}"

        # 4. Resolve and append next instructions
        if success and next_instructions:
            instruction_texts = self.get_next_instruction_texts()
            for key in next_instructions:
                raw_text = instruction_texts.get(key, "")
                if raw_text:
                    # Parse placeholders in the next instruction template
                    try:
                        placeholders = []
                        none_val = self._get_none_value()
                        formatter = SafeNoneFormatter(none_val)
                        for _, field_name, _, _ in formatter.parse(raw_text):
                            if field_name is not None:
                                placeholders.append(field_name.split(".")[0].split("[")[0])

                        format_dict = {}
                        for k in placeholders:
                            format_dict[k] = data_dict.get(k, None)

                        formatted_instruction = formatter.format(raw_text, **format_dict)
                        text = f"{text}\n\n{formatted_instruction}"
                    except Exception as exc:
                        text = f"{text}\n\nFormat error in instruction '{key}': {exc}"

        return text

    def present_notes(self, tool_name: str, notes: list[NoteEntry]) -> str | None:
        """Format notes into markdown text blocks using templates."""
        group_names = ["exclusions", "suggestions", "recoveries", "info"]
        grouped_texts: dict[str, list[str]] = {g: [] for g in group_names}

        none_val = self._get_none_value()
        formatter = SafeNoneFormatter(none_val)

        # Retrieve group configuration
        # global.notes.groups
        global_notes = None
        if isinstance(self.global_config, dict):
            global_notes = self.global_config.get("notes")
        else:
            global_notes = getattr(self.global_config, "notes", None)

        group_configs: dict[str, Any] = {}
        if global_notes is not None:
            if isinstance(global_notes, dict):
                group_configs = global_notes.get("groups") or {}
            else:
                group_configs = getattr(global_notes, "groups", {})

        for note in notes:
            key, params = map_legacy_note_to_event(note)

            # Search for template and group
            found_template = None
            found_group = None

            for group in group_names:
                # 1. Local tool config lookup
                tool_cfg = self.tools_config.get(tool_name)
                local_tmpl = None
                if tool_cfg is not None:
                    if isinstance(tool_cfg, dict):
                        group_dict = tool_cfg.get(group)
                        if isinstance(group_dict, dict):
                            local_tmpl = group_dict.get(key)
                    else:
                        group_dict = getattr(tool_cfg, group, None)
                        if isinstance(group_dict, dict):
                            local_tmpl = group_dict.get(key)

                if isinstance(local_tmpl, str):
                    found_template = local_tmpl
                    found_group = group
                    break

                # 2. Global notes config fallback lookup
                global_tmpl = None
                if global_notes is not None:
                    templates = None
                    if isinstance(global_notes, dict):
                        templates = global_notes.get("templates")
                    else:
                        templates = getattr(global_notes, "templates", None)

                    if templates is not None and isinstance(templates, dict):
                        group_templates = templates.get(group)
                        if isinstance(group_templates, dict):
                            global_tmpl = group_templates.get(key)

                if isinstance(global_tmpl, str):
                    found_template = global_tmpl
                    found_group = group
                    break

            if found_template is not None and found_group is not None:
                # Fill missing keys in params with None to trigger SafeNoneFormatter
                placeholders = []
                try:
                    for _, field_name, _, _ in formatter.parse(found_template):
                        if field_name is not None:
                            placeholders.append(field_name.split(".")[0].split("[")[0])
                except Exception:
                    pass

                format_dict = {}
                for p_key in placeholders:
                    format_dict[p_key] = params.get(p_key, None)

                try:
                    formatted_text = formatter.format(found_template, **format_dict)
                    grouped_texts[found_group].append(formatted_text)
                except Exception as exc:
                    grouped_texts[found_group].append(f"Format error: {exc}")
            else:
                # Fallback: if it's a legacy note, render it using to_message()
                if hasattr(note, "to_message") and callable(note.to_message):
                    msg = note.to_message()
                    if isinstance(note, ExclusionNote):
                        grouped_texts["exclusions"].append(msg)
                    elif isinstance(note, SuggestionNote):
                        grouped_texts["suggestions"].append(msg)
                    elif isinstance(note, RecoveryNote):
                        cleaned = (
                            msg.lstrip()
                            .removeprefix("🩹")
                            .lstrip()
                            .removeprefix("Recovery:")
                            .lstrip()
                        )
                        grouped_texts["recoveries"].append(cleaned)
                    elif isinstance(note, InfoNote):
                        grouped_texts["info"].append(msg)
                    else:
                        grouped_texts["info"].append(msg)

        lines = []
        for group in group_names:
            items = grouped_texts[group]
            if not items:
                continue

            # Get emoji and header
            emoji = ""
            header = ""
            cfg = None
            if isinstance(group_configs, dict):
                cfg = group_configs.get(group)
            else:
                cfg = getattr(group_configs, "get", lambda k: None)(group)

            if cfg is not None:
                if isinstance(cfg, dict):
                    emoji = cfg.get("emoji", "")
                    header = cfg.get("header", "")
                else:
                    emoji = getattr(cfg, "emoji", "")
                    header = getattr(cfg, "header", "")
            else:
                fallbacks = {
                    "exclusions": ("🩹", "Exclusions"),
                    "suggestions": ("💡", "Suggestions"),
                    "recoveries": ("🩹", "Recoveries"),
                    "info": ("📋", "Information"),
                }
                emoji, header = fallbacks[group]

            group_header = f"{emoji} {header}".strip()
            lines.append(group_header)
            for item in items:
                lines.append(f"  - {item}")
            lines.append("")

        if not lines:
            return None
        return "\n".join(lines).strip()


def validate_presentation_alignment(presenter: TextPresenter, tools: list[Any]) -> None:
    """Verifies that templates align with DTO models, note classes, and errors to prevent drift."""
    import string  # noqa: PLC0415

    # ConfigError imported on module level
    pass
    blacklist = {"message", "msg", "text", "txt", "error_message", "error", "err"}
    blacklist = {"message", "msg", "text", "txt", "error_message", "error", "err"}

    # Mapping for system-level errors
    error_class_fields = {
        "ERR_CONFIG": {"message", "file_path", "code"},
        "config": {"message", "file_path", "code"},
        "ERR_VALIDATION": {
            "message",
            "validation_errors",
            "input_schema",
            "params",
            "success",
            "error_type",
            "traceback",
        },
        "validation": {
            "message",
            "validation_errors",
            "input_schema",
            "params",
            "success",
            "error_type",
            "traceback",
        },
        "ERR_EXECUTION": {"message", "params", "success", "error_type", "traceback"},
        "execution": {"message", "params", "success", "error_type", "traceback"},
        "ERR_SYSTEM": {"message", "fallback", "code"},
        "system": {"message", "fallback", "code"},
        "ERR_CACHE": {"message", "params", "success", "error_type", "traceback"},
        "cache": {"message", "params", "success", "error_type", "traceback"},
    }

    # Mapping for legacy notes
    legacy_note_fields = {
        "file_excluded": {"file_path"},
        "suggestion_message": {"message", "subject"},
        "blocker_message": {"message"},
        "recovery_message": {"message"},
        "info_message": {"message"},
    }

    def get_placeholders(tmpl: str) -> list[str]:
        p_list = []
        try:
            for _, field_name, _, _ in string.Formatter().parse(tmpl):
                if field_name is not None:
                    base_field = field_name.split(".")[0].split("[")[0]
                    p_list.append(base_field)
        except Exception as exc:
            raise ConfigError(f"Invalid template format: {exc}") from exc
        return p_list

    def check_blacklist(tmpl: str, template_key: str, is_default_fail: bool = False) -> None:
        placeholders = get_placeholders(tmpl)
        for p in placeholders:
            if p in blacklist:
                # Exceptions
                if is_default_fail and p == "error_message":
                    continue
                if template_key in legacy_note_fields and p == "message":
                    continue
                raise ConfigError(
                    f"Template for '{template_key}' uses blacklisted generic parameter '{p}'"
                )

    # 1. Global settings validation
    global_note_templates: dict[str, Any] = {}
    global_cfg = presenter.global_config
    if isinstance(global_cfg, dict):
        default_fail = global_cfg.get("default_failure_template")
        failures = global_cfg.get("failures") or {}
        global_notes = global_cfg.get("notes") or {}
        global_note_templates = {}
        if isinstance(global_notes, dict):
            global_note_templates = global_notes.get("templates") or {}
    else:
        default_fail = getattr(global_cfg, "default_failure_template", None)
        failures = getattr(global_cfg, "failures", {}) or {}
        global_notes = getattr(global_cfg, "notes", None)
        global_note_templates = {}
        if global_notes is not None:
            global_note_templates = getattr(global_notes, "templates", {}) or {}

    # Validate default failure template
    if default_fail:
        check_blacklist(default_fail, "default_failure_template", is_default_fail=True)

    # Validate global failures
    for err_code, template in failures.items():
        check_blacklist(template, err_code)
        placeholders = get_placeholders(template)
        # Verify placeholders against system error fields if it is a known code
        if err_code in error_class_fields:
            allowed = error_class_fields[err_code]
            for p in placeholders:
                if p not in allowed:
                    raise ConfigError(
                        f"Failure placeholder '{p}' not found in DTO fields for '{err_code}'"
                    )

    # Validate global note templates
    for _, group_templates in global_note_templates.items():
        if not isinstance(group_templates, dict):
            continue
        for key, template in group_templates.items():
            check_blacklist(template, key)
            placeholders = get_placeholders(template)
            if key in legacy_note_fields:
                allowed = legacy_note_fields[key]
                for p in placeholders:
                    if p not in allowed:
                        raise ConfigError(
                            f"Note template placeholder '{p}' not found in fields for note '{key}'"
                        )

    # 2. Tool-specific validation
    for tool in tools:
        tool_name = getattr(tool, "name", None)
        if not tool_name:
            continue

        output_model = getattr(tool, "output_model", None)
        tool_cfg = presenter.tools_config.get(tool_name)
        if not tool_cfg:
            continue

        # Get templates for this tool
        templates_to_check = []
        next_inst_keys = []

        if isinstance(tool_cfg, ToolPresentationConfig):
            if tool_cfg.template_success is not None:
                templates_to_check.append(("template_success", tool_cfg.template_success))
            if tool_cfg.template_failure is not None:
                templates_to_check.append(("template_failure", tool_cfg.template_failure))
            next_inst_keys = tool_cfg.next_instructions

            # Local notes
            local_notes = {
                "exclusions": tool_cfg.exclusions,
                "suggestions": tool_cfg.suggestions,
                "recoveries": tool_cfg.recoveries,
                "info": tool_cfg.info,
            }
        else:
            val_success = tool_cfg.get("template_success")
            if isinstance(val_success, str):
                templates_to_check.append(("template_success", val_success))
            val_failure = tool_cfg.get("template_failure")
            if isinstance(val_failure, str):
                templates_to_check.append(("template_failure", val_failure))
            next_inst_keys = tool_cfg.get("next_instructions") or []

            # Local notes
            local_notes = {
                "exclusions": tool_cfg.get("exclusions") or {},
                "suggestions": tool_cfg.get("suggestions") or {},
                "recoveries": tool_cfg.get("recoveries") or {},
                "info": tool_cfg.get("info") or {},
            }

        instruction_texts = presenter.get_next_instruction_texts()
        for key in next_inst_keys:
            raw_text = instruction_texts.get(key)
            if isinstance(raw_text, str):
                templates_to_check.append((f"instruction_{key}", raw_text))

        # Check local notes
        for _, notes_dict in local_notes.items():
            if not isinstance(notes_dict, dict):
                continue
            for key, template in notes_dict.items():
                check_blacklist(template, key)
                placeholders = get_placeholders(template)
                if key in legacy_note_fields:
                    allowed = legacy_note_fields[key]
                    for p in placeholders:
                        if p not in allowed:
                            raise ConfigError(
                                f"Note placeholder '{p}' not found in fields for '{key}'"
                            )

        # Skip output model validation if model is not defined (or None during migration)
        if (
            output_model is None
            or not isinstance(output_model, type)
            or not issubclass(output_model, BaseModel)
        ):
            continue

        allowed_fields = set(output_model.model_fields.keys())
        allowed_fields.update({"success", "error_message", "post_tool_instruction"})

        for _, template in templates_to_check:
            placeholders = get_placeholders(template)
            for base_field in placeholders:
                if base_field.startswith("emoji_"):
                    continue
                if base_field not in allowed_fields:
                    raise ConfigError(
                        f"Template placeholder '{base_field}' not found in DTO "
                        f"'{output_model.__name__}' for tool '{tool_name}'"
                    )
