# mcp_server\presenters\schema_resource_presenter.py
# template=service version=5d5b489a created=2026-09-13T18:22Z updated=
"""Serialize supplied schema attachments according to their identity.

@layer: Presentation
@dependencies: tool_execution, presentation_output
"""

import json
from urllib.parse import quote

from mcp_server.core.interfaces.ipresenter import IResourcePresenter
from mcp_server.core.interfaces.template_catalog import thaw_json
from mcp_server.core.tool_execution import SchemaAttachment
from mcp_server.schemas.presentation_output import PresentationResource


class SchemaResourcePresenter(IResourcePresenter):
    """Format attachments without inspecting operation DTOs or resolving schemas."""

    def present_resources(
        self, attachments: tuple[SchemaAttachment, ...]
    ) -> tuple[PresentationResource, ...]:
        resources: list[PresentationResource] = []
        for attachment in attachments:
            identity = attachment.identity
            if identity.kind == "whole_tool":
                uri = "schema://validation"
                mime_type = "application/json"
            else:
                uri = f"schema://template/{quote(identity.template_id, safe='')}/context"
                mime_type = "application/schema+json"
            resources.append(
                PresentationResource(
                    uri=uri,
                    mime_type=mime_type,
                    content=json.dumps(thaw_json(attachment.schema), ensure_ascii=False),
                )
            )
        return tuple(resources)
