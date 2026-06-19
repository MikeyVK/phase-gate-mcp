# mcp_server/core/tool_factory.py
# template=generic version=f35abd82 created=2026-06-19T22:39Z updated=
"""ToolFactory module.

Composition root for wrapping business logic tools into decorators.

@layer: Core
"""

# Standard library
from pathlib import Path

# Third-party
from pydantic import BaseModel

# Project modules
from mcp_server.core.decorators.enforcement_decorator import EnforcementDecorator
from mcp_server.core.decorators.input_validation_decorator import InputValidationDecorator
from mcp_server.core.decorators.tool_error_handler_decorator import ToolErrorHandlerDecorator
from mcp_server.core.interfaces.icore_tool import ICoreTool
from mcp_server.core.interfaces.itool import ITool
from mcp_server.managers.enforcement_runner import EnforcementRunner


class ToolFactory:
    """Composition root for wrapping business logic tools into decorators."""

    def __init__(self, enforcement_runner: EnforcementRunner, workspace_root: Path) -> None:
        """Initialize the ToolFactory with runner and workspace root."""
        self._enforcement_runner = enforcement_runner
        self._workspace_root = workspace_root

    def create_tool(self, core_tool: ICoreTool[BaseModel, BaseModel]) -> ITool:
        """Compose the Russian Doll decorator stack for a core tool."""
        # 1. Wrap the core tool with Enforcement policy checking
        enforcement_stacked = EnforcementDecorator(
            core_tool, self._enforcement_runner, self._workspace_root
        )

        # 2. Wrap with validation checking (Bridges ICoreTool to ITool)
        validated_stacked = InputValidationDecorator(enforcement_stacked)

        # 3. Wrap with catch-all error handling
        return ToolErrorHandlerDecorator(validated_stacked)
