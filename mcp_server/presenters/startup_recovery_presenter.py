# pgmcp:v1 id=python_class pv=1.0.0 pf=u_KOYBekCfsMbBaW sf=5--KpGf2wHUv2qAj

"""Present recovery results without loading rejected template or presentation configuration."""

import json
from collections.abc import Mapping
from typing import Any

from pydantic import BaseModel

from mcp_server.core.interfaces.ipresenter import IPresenter, IResourcePresenter
from mcp_server.core.operation_notes import NoteEntry
from mcp_server.core.tool_execution import SchemaAttachment
from mcp_server.schemas.cache_publication import CachePublication
from mcp_server.schemas.presentation_output import PresentedOutput
from mcp_server.schemas.tool_outputs import HealthCheckOutput, RestartServerOutput


def present_proxy_event(event_type: str, parameters: Mapping[str, object]) -> str:
    """Render transport facts at the presentation boundary."""
    if event_type == "server_stderr":
        return (
            f"[SERVER pid={parameters.get('server_pid')} "
            f"generation={parameters.get('generation')}] {parameters.get('raw_stderr', '')}"
        )
    if event_type == "server_unavailable":
        return (
            f"Server transport is unavailable ({parameters.get('state')}). "
            "Inspect the startup stderr/audit log; correct the source or launch failure "
            "and retry through the recovery server or reconnect the launcher."
        )
    if event_type == "message_encoding_failed":
        return f"Message must contain valid UTF-8 text: {parameters.get('error')}"
    return f"[PROXY] {event_type}: {json.dumps(dict(parameters), ensure_ascii=False, default=str)}"


class StartupRecoveryPresenter(IPresenter):
    """Render the complete recovery operation without configuration or cache access."""

    def __init__(self, resource_presenter: IResourcePresenter) -> None:
        self._resource_presenter = resource_presenter

    def present(
        self,
        tool_name: str,
        data: BaseModel | dict[str, Any],
        notes: list[NoteEntry] | None = None,
        cache_pub: CachePublication | None = None,
        success: bool | None = None,
        *,
        attachments: tuple[SchemaAttachment, ...] = (),
    ) -> PresentedOutput:
        """Include diagnostic and decorator errors verbatim in the public result."""
        del cache_pub, success
        payload = data.model_dump(mode="json") if isinstance(data, BaseModel) else data
        if isinstance(data, HealthCheckOutput):
            heading = (
                "Server admission failed. Correct the source externally, then call restart_server."
                if data.startup_diagnostic is not None
                else "Server health"
            )
        elif isinstance(data, RestartServerOutput):
            heading = (
                "Restart requested. This receipt does not confirm admission success. "
                "Check health after replacement and refresh tools/list."
            )
        else:
            heading = f"Recovery operation result: {tool_name}"
        text = heading + "\n\n" + json.dumps(payload, ensure_ascii=False, indent=2)
        if notes:
            text += "\n\n" + json.dumps(
                [{"key": note.key, "params": note.params} for note in notes],
                ensure_ascii=False,
                indent=2,
            )
        return PresentedOutput(
            text=text,
            resources=list(self._resource_presenter.present_resources(attachments)),
        )
