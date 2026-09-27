# pgmcp:v1 id=python_pydantic_dto pv=1.0.0 pf=ZaJvTOvENaaS4lHn sf=9PfER5JkyAoFQLRi

"""Pure shared template-package identity and provenance values."""

from __future__ import annotations

import re
from typing import Annotated, Literal, TypeAlias

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

CompactFingerprint = Annotated[
    str,
    StringConstraints(
        strict=True,
        min_length=16,
        max_length=16,
        pattern=re.compile(r"^[A-Za-z0-9_-]{16}$(?![\s\S])"),
    ),
]

EdgeKind: TypeAlias = Literal["extends", "include", "import", "from_import"]


class ArtifactIdentity(BaseModel):
    """The four canonical generation facts consumed by artifact provenance."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    id: TemplateId
    pv: TemplatePackageVersion
    pf: CompactFingerprint
    sf: CompactFingerprint
