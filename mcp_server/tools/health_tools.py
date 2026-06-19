"""Health check tools."""

import os
import sys
import time
from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict

from mcp_server.config.settings import Settings
from mcp_server.core.operation_notes import NoteContext
from mcp_server.schemas.tool_outputs import HealthCheckOutput, HealthStatus
from mcp_server.tools.base import ILegacyTool

START_TIME = time.time()


class HealthCheckInput(BaseModel):
    """Input for HealthCheckTool."""

    model_config = ConfigDict(extra="forbid")


class HealthCheckTool(ILegacyTool):
    """Tool to check server health."""

    output_model: ClassVar[type[BaseModel]] = HealthCheckOutput
    presentation_category = "query"

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
        settings = Settings.from_env()
        return HealthCheckOutput(
            status=HealthStatus.HEALTHY,
            version=settings.server.version,
            pid=os.getpid(),
            platform=sys.platform,
            uptime_seconds=time.time() - START_TIME,
        )
