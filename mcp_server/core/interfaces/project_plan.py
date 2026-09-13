# mcp_server/core/interfaces/project_plan.py
# template=interface version=3fb28c28 created=2026-09-13T12:25Z updated=
"""Read-only project plan contract.

@layer: Backend (Contracts)
"""

from collections.abc import Mapping
from typing import Any, Protocol


class IProjectPlanReader(Protocol):
    """Expose stored project planning without project mutation commands."""

    def get_project_plan(self, issue_number: int) -> Mapping[str, Any] | None:
        """Return the stored plan and current workflow status, when available."""
        ...
