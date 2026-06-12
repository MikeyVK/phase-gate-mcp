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

    def _get_json_reference(self) -> str:
        """Get the global JSON reference string."""
        if isinstance(self.global_config, dict):
            return str(self.global_config.get("json_reference", ""))
        return self.global_config.json_reference

    def _get_default_failure_template(self) -> str:
        """Get the default failure template."""
        if isinstance(self.global_config, dict):
            return str(
                self.global_config.get("default_failure_template", "Failed: {error_message}")
            )
        return self.global_config.default_failure_template

    def _get_advisories(self) -> dict[str, str]:
        """Get the advisories lookup dictionary."""
        if isinstance(self.global_config, dict):
            return cast(dict[str, str], self.global_config.get("advisories", {}))
        return self.global_config.advisories

    def _is_complex(self, val: object) -> bool:
        """Check if a value represents complex structured data."""
        if isinstance(val, (list, dict, set, tuple)):
            return len(val) > 0
        return (
            isinstance(val, str)
            and "\n" in val
            and (val.startswith("diff ") or "@@ " in val or "\n+" in val or "\n-" in val)
        )

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
        advisory_key = None
        append_json_ref = False

        if tool_cfg is not None:
            # Support both Pydantic model and raw dict for tool config
            if isinstance(tool_cfg, ToolPresentationConfig):
                template = tool_cfg.template_success if success else tool_cfg.template_failure
                advisory_key = tool_cfg.advisory
                append_json_ref = tool_cfg.append_json_reference
            else:
                template = (
                    tool_cfg.get("template_success")
                    if success
                    else tool_cfg.get("template_failure")
                )
                advisory_key = tool_cfg.get("advisory")
                append_json_ref = tool_cfg.get("append_json_reference", False)

        # Fallback for failure template
        if not success and not template:
            template = self._get_default_failure_template()

        # Format template if we have one, otherwise dump/default representation
        if template:
            try:
                # Fill missing keys in data_dict with empty string to avoid KeyError
                # Parse all placeholders in the template
                placeholders = []
                for _, field_name, _, _ in string.Formatter().parse(template):
                    if field_name is not None:
                        placeholders.append(field_name.split(".")[0].split("[")[0])

                format_dict = {}
                for key in placeholders:
                    format_dict[key] = data_dict.get(key, "")

                text = template.format(**format_dict)
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

        # 4. Resolve and append advisories
        if advisory_key:
            advisories = self._get_advisories()
            advisory_text = advisories.get(advisory_key, "")
            if advisory_text:
                text = f"{text}{advisory_text}"

        # 5. Appending json reference conditionally
        # Check if DTO has any complex data
        has_complex_data = any(
            self._is_complex(v)
            for k, v in data_dict.items()
            if k not in ("success", "error_message", "post_tool_instruction")
        )

        if append_json_ref or has_complex_data:
            json_ref = self._get_json_reference()
            if json_ref:
                text = f"{text}\n\n{json_ref}"

        return text


def validate_presentation_alignment(presenter: TextPresenter, tools: list[Any]) -> None:
    """Verifies that templates in presentation.yaml align with DTO models to prevent drift."""
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
        else:
            val_success = tool_cfg.get("template_success")
            if isinstance(val_success, str):
                templates.append(val_success)
            val_failure = tool_cfg.get("template_failure")
            if isinstance(val_failure, str):
                templates.append(val_failure)

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
