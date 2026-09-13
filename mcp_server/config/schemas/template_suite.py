# mcp_server/config/schemas/template_suite.py
# template=schema version=74378193 created=2026-09-13T15:00Z updated=
"""Pure package admission values; loading and cross-package coherence belong to the loader.

@layer: Config
@dependencies: pydantic
"""

import re
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, StringConstraints

TemplateId = Annotated[
    str,
    StringConstraints(
        strict=True,
        min_length=1,
        max_length=24,
        pattern=re.compile(r"^(?!.*(?:<!--|-->|/\*|\*/|//|#))[^\s=\x00-\x1f\x7f-\x9f]+$(?![\s\S])"),
    ),
]

_NUMERIC_IDENTIFIER = r"(?:0|[1-9][0-9]*)"
_PRERELEASE_IDENTIFIER = r"(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)"

TemplatePackageVersion = Annotated[
    str,
    StringConstraints(
        strict=True,
        max_length=11,
        pattern=re.compile(
            rf"^{_NUMERIC_IDENTIFIER}\.{_NUMERIC_IDENTIFIER}\.{_NUMERIC_IDENTIFIER}"
            rf"(?:-{_PRERELEASE_IDENTIFIER}(?:\.{_PRERELEASE_IDENTIFIER})*)?"
            r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$(?![\s\S])"
        ),
    ),
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
