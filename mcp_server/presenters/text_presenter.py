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
                for key in placeholders:
                    format_dict[key] = data_dict.get(key, None)

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
        if next_instructions:
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
    """Verifies that templates align with DTO models to prevent drift."""
    for tool in tools:
        tool_name = getattr(tool, "name", None)
        if not tool_name:
            continue

        output_model = getattr(tool, "output_model", None)
        if (
            output_model is None
            or not isinstance(output_model, type)
            or not issubclass(output_model, BaseModel)
        ):
            # Graceful fallback: ignore tools without an output_model ClassVar
            # during migration phase
            continue

        # Get templates for this tool
        tool_cfg = presenter.tools_config.get(tool_name)
        if not tool_cfg:
            continue

        templates = []
        if isinstance(tool_cfg, ToolPresentationConfig):
            if tool_cfg.template_success is not None:
                templates.append(tool_cfg.template_success)
            if tool_cfg.template_failure is not None:
                templates.append(tool_cfg.template_failure)
            next_inst_keys = tool_cfg.next_instructions
        else:
            val_success = tool_cfg.get("template_success")
            if isinstance(val_success, str):
                templates.append(val_success)
            val_failure = tool_cfg.get("template_failure")
            if isinstance(val_failure, str):
                templates.append(val_failure)
            next_inst_keys = tool_cfg.get("next_instructions") or []

        instruction_texts = presenter.get_next_instruction_texts()
        for key in next_inst_keys:
            raw_text = instruction_texts.get(key)
            if isinstance(raw_text, str):
                templates.append(raw_text)

        # Check fields in output_model (Pydantic model)
        allowed_fields = set(output_model.model_fields.keys())
        # Also allow standard BaseToolOutput fields
        allowed_fields.update({"success", "error_message", "post_tool_instruction"})

        for template in templates:
            try:
                for _, field_name, _, _ in string.Formatter().parse(template):
                    if field_name is not None:
                        base_field = field_name.split(".")[0].split("[")[0]
                        if base_field.startswith("emoji_"):
                            continue
                        if base_field not in allowed_fields:
                            raise ConfigError(
                                f"Template placeholder '{base_field}' not found in DTO "
                                f"'{output_model.__name__}' for tool '{tool_name}'"
                            )
            except ConfigError:
                raise
            except Exception as exc:
                raise ConfigError(f"Invalid template format for tool '{tool_name}': {exc}") from exc
