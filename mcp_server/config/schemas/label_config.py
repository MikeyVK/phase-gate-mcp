# mcp_server/config/schemas/label_config.py
"""
Label configuration schema value objects.

Defines typed label and pattern metadata loaded by the configuration layer.

@layer: Backend (Config)
@dependencies: [re, typing, pydantic]
@responsibilities:
    - Define label and label-pattern schema contracts
    - Validate label color and duplicate-name invariants
    - Provide lookup helpers used by label-aware tooling
"""

import re
from dataclasses import FrozenInstanceError
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from mcp_server.config.schemas.workphases import WorkphasesConfig

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, field_validator


class Label(BaseModel):
    """Immutable label definition from labels.yaml."""

    model_config = ConfigDict(frozen=True)

    name: str
    color: str
    description: str = ""

    def __setattr__(self, name: str, value: object) -> None:
        if name in type(self).model_fields and name in self.__dict__:
            raise FrozenInstanceError(f"cannot assign to field '{name}'")
        super().__setattr__(name, value)

    @field_validator("color")
    @classmethod
    def validate_color(cls, color: str) -> str:
        if not re.match(r"^[0-9a-fA-F]{6}$", color):
            raise ValueError(
                f"Invalid color format '{color}'. Expected 6-character hex WITHOUT # prefix"
            )
        return color

    def to_github_dict(self) -> dict[str, str]:
        return {"name": self.name, "color": self.color, "description": self.description}


class LabelPattern(BaseModel):
    """Dynamic label pattern definition."""

    pattern: str
    description: str
    color: str
    example: str = ""

    def matches(self, label_name: str) -> bool:
        return bool(re.match(self.pattern, label_name))


class LabelConfig(BaseModel):
    """Label configuration value object."""

    version: str = Field(..., description="Schema version")
    labels: list[Label] = Field(..., description="Label definitions")
    freeform_exceptions: list[str] = Field(default_factory=list)
    label_patterns: list[LabelPattern] = Field(default_factory=list)

    _labels_by_name: dict[str, Label] = PrivateAttr(default_factory=dict)
    _labels_by_category: dict[str, list[Label]] = PrivateAttr(default_factory=dict)

    def model_post_init(self, __context: Any) -> None:  # noqa: ANN401
        self._build_caches()

    def _build_caches(self) -> None:
        self._labels_by_name = {label.name: label for label in self.labels}
        self._labels_by_category = {}
        for label in self.labels:
            if ":" in label.name:
                category = label.name.split(":", 1)[0]
                self._labels_by_category.setdefault(category, []).append(label)

    def validate_label_name(self, name: str) -> tuple[bool, str]:
        if name in self.freeform_exceptions:
            return (True, "")
        if name in self._labels_by_name:
            return (True, "")
        for pattern in self.label_patterns:
            if pattern.matches(name):
                return (True, "")

        pattern_examples = [pattern.example for pattern in self.label_patterns if pattern.example]
        examples_str = (
            f" Dynamic patterns: {', '.join(pattern_examples)}." if pattern_examples else ""
        )
        return (
            False,
            f"Label '{name}' does not match any configured static label, "
            f"dynamic pattern,{examples_str} or freeform exception.",
        )

    def label_exists(self, name: str) -> bool:
        return name in self._labels_by_name

    def get_label(self, name: str) -> Label | None:
        return self._labels_by_name.get(name)

    def get_labels_by_category(self, category: str) -> list[Label]:
        return self._labels_by_category.get(category, [])

    def sync_to_github(self, github_adapter: Any, dry_run: bool = False) -> dict[str, list[str]]:  # noqa: ANN401
        result: dict[str, list[str]] = {"created": [], "updated": [], "skipped": [], "errors": []}

        try:
            existing = github_adapter.list_labels()
            existing_by_name = {label["name"]: label for label in existing}
        except Exception as exc:
            result["errors"].append(f"Failed to fetch labels: {exc}")
            return result

        for label in self.labels:
            try:
                if label.name not in existing_by_name:
                    if not dry_run:
                        github_adapter.create_label(
                            name=label.name,
                            color=label.color,
                            description=label.description,
                        )
                    result["created"].append(label.name)
                else:
                    existing_label = existing_by_name[label.name]
                    if self._needs_update(label, existing_label):
                        if not dry_run:
                            github_adapter.update_label(
                                name=label.name,
                                color=label.color,
                                description=label.description,
                            )
                        result["updated"].append(label.name)
                    else:
                        result["skipped"].append(label.name)
            except Exception as exc:
                result["errors"].append(f"{label.name}: {exc}")

        return result

    def _needs_update(self, yaml_label: Label, github_label: dict[str, Any]) -> bool:
        return bool(
            yaml_label.color != github_label["color"]
            or yaml_label.description != github_label.get("description", "")
        )

    @field_validator("labels")
    @classmethod
    def validate_no_duplicates(cls, labels: list[Label]) -> list[Label]:
        names = [label.name for label in labels]
        duplicates = [name for name in names if names.count(name) > 1]
        if duplicates:
            raise ValueError(f"Duplicate label names: {set(duplicates)}")
        return labels


def validate_phase_label(
    label_name: str,
    workphases_config: "WorkphasesConfig",
) -> tuple[bool, str]:
    """Validate a label against known workflow phases.

    Returns (True, "") if the label is not a phase:* label, or if it names a
    known non-terminal phase.  Returns (False, <reason>) otherwise.
    """
    if not label_name.startswith("phase:"):
        return (True, "")

    phase_slug = label_name.removeprefix("phase:")
    known_phases = set(workphases_config.phases.keys())
    if phase_slug in known_phases:
        return (True, "")

    valid_list = ", ".join(sorted(known_phases))
    return (
        False,
        f"phase label 'phase:{phase_slug}' names an unknown workphase '{phase_slug}'. "
        f"Valid phases: {valid_list}.",
    )
