# mcp_server/config/schemas/template_suite.py
# template=schema version=74378193 created=2026-09-13T15:00Z updated=
"""Pure package admission values; loading and cross-package coherence belong to the loader.

@layer: Config
@dependencies: pydantic, shared template identity values
"""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, StringConstraints

from mcp_server.schemas.template_identity import TemplateId, TemplatePackageVersion

__all__ = [
    "TemplateId",
    "TemplatePackageVersion",
    "PackageText",
    "TemplateManifest",
    "TemplatePolicy",
]

PackageText = Annotated[str, StringConstraints(strict=True, strip_whitespace=True, min_length=1)]


class TemplateManifest(BaseModel):
    """The two authored generation facts of one template package."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    template_id: TemplateId
    purpose: PackageText


class TemplatePolicy(BaseModel):
    """Authored evidence selection and target lifetime, separate from generation identity."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    output_profile: PackageText
    persistence: Literal["workspace", "temporary"]
