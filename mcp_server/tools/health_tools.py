"""Health check tools."""

import os
import sys
import time
from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict

from mcp_server.config.settings import Settings
from mcp_server.core.interfaces import ICoreTool
from mcp_server.core.operation_notes import NoteContext
from mcp_server.schemas.startup_diagnostic import StartupDiagnostic
from mcp_server.schemas.tool_outputs import HealthCheckOutput, HealthStatus

START_TIME = time.time()


class HealthCheckInput(BaseModel):
    """Input for HealthCheckTool."""

    model_config = ConfigDict(extra="forbid")


class HealthCheckTool(ICoreTool[HealthCheckInput, HealthCheckOutput]):
    """Tool to check server health."""

    output_model: ClassVar[type[BaseModel]] = HealthCheckOutput

    def __init__(
        self,
        settings: Settings,
        startup_diagnostic: StartupDiagnostic | None = None,
    ) -> None:
        """Receive the resolved settings and optional immutable startup failure."""
        super().__init__()
        self._settings = settings
        self._startup_diagnostic = startup_diagnostic

    @property
    def name(self) -> str:
        return "health_check"

    @property
    def description(self) -> str:
        return "Check server health status"

    @property
    def args_model(self) -> type[BaseModel] | None:
        return HealthCheckInput

    @property
    def input_schema(self) -> dict[str, Any]:
        assert self.args_model is not None
        return self.args_model.model_json_schema()

    async def execute(self, params: HealthCheckInput, context: NoteContext) -> HealthCheckOutput:
        del params, context  # Not used
        status = (
            HealthStatus.UNHEALTHY if self._startup_diagnostic is not None else HealthStatus.HEALTHY
        )
        return HealthCheckOutput(
            status=status,
            startup_diagnostic=self._startup_diagnostic,
            version=self._settings.server.version,
            pid=os.getpid(),
            platform=sys.platform,
            uptime_seconds=time.time() - START_TIME,
        )
