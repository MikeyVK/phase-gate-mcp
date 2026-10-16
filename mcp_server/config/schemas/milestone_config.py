# mcp_server/config/schemas/milestone_config.py
"""
Milestone configuration schema definitions.

Defines typed value objects for milestone metadata loaded by the config layer.

@layer: Backend (Config)
@dependencies: [pydantic]
@responsibilities:
    - Define milestone entry and root config schema contracts
    - Validate milestone metadata loaded from YAML
    - Provide milestone lookup helpers for issue workflows
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from mcp_server.config.ordering import ConfigId


class MilestoneEntry(BaseModel):
    """Single milestone entry from milestones.yaml."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    number: int
    title: str
    state: str = "open"


class MilestoneConfig(BaseModel):
    """Milestone validation configuration value object."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    version: Literal["1.0.0"] = Field("1.0.0", description="Schema version")
    milestones: dict[ConfigId, MilestoneEntry] = Field(default_factory=dict)

    def validate_milestone(self, title: str) -> bool:
        if not self.milestones:
            return True
        return any(milestone.title == title for milestone in self.milestones.values())
