# mcp_server/config/schemas/presentation_config.py
# template=schema version=74378193 created=2026-06-12T20:49Z updated=2026-06-12T21:00Z
"""PresentationConfig schema.

@layer: Config
"""

from pydantic import BaseModel, ConfigDict, Field


class EmojisConfig(BaseModel):
    """Global emojis settings."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    success: str = "✅"
    failure: str = "❌"
    warning: str = "⚠️"
    query: str = "📋"
    bootstrap: str = "🚀"


class GlobalPresentationConfig(BaseModel):
    """Global presentation settings."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    emojis: EmojisConfig = Field(default_factory=EmojisConfig)
    default_failure_template: str = "Failed: {error_message}"
    next_instruction_texts: dict[str, str] = Field(default_factory=dict)


class ToolPresentationConfig(BaseModel):
    """Presentation settings for a specific tool."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    template_success: str | None = None
    template_failure: str | None = None
    next_instructions: list[str] = Field(default_factory=list)


class PresentationConfig(BaseModel):
    """Unified configuration for declarative text presentation."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    global_settings: GlobalPresentationConfig = Field(alias="global")
    tools: dict[str, ToolPresentationConfig] = Field(default_factory=dict)
