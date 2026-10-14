# pgmcp:v1 id=pytest_integration_test pv=1.0.0 pf=70EjvGU6LK1YPSz3 sf=zJbLuUrs_I33kpX4

"""Native data artifact persistence using real configured checks and public operations."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from shutil import copytree
from typing import Literal

import pytest
from pydantic import JsonValue

from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.adapter_manifest import AdapterTrustConfig
from mcp_server.config.schemas.artifact_locations import ArtifactLocationsConfig
from mcp_server.core.interfaces.template_catalog import thaw_json
from mcp_server.execution.catalog import AdapterCatalogLoader, FileAdapterPackageReader
from mcp_server.execution.check_service import CheckService
from mcp_server.execution.content_input import ContentInputPreparer, FileContentScratch
from mcp_server.execution.invocation_scratch import FileInvocationScratch
from mcp_server.execution.process_runtime import AdapterProcessRuntime, AsyncioProcessBackend
from mcp_server.schemas.template_identity import ArtifactIdentity
from mcp_server.services.artifact_header_reader import ArtifactHeaderReader
from mcp_server.services.artifact_target_resolver import ArtifactTargetResolver
from mcp_server.services.edit_construction import RewriteOperation, construct_edit, select_profile
from mcp_server.services.edit_operation import EditOperation
from mcp_server.services.scaffold_operation import ScaffoldOperation
from mcp_server.utils.atomic_file_writer import (
    CheckedFileWriter,
    CreateOnlyFileWriter,
    OriginalFileReader,
)
from mcp_server.utils.path_resolver import FileArtifactTargetPaths, resolve_temporary_paths
from tests.mcp_server.fixtures.delivered_templates import DeliveredTemplate, load_delivered_template


@pytest.fixture(params=["yaml_configuration", "json_schema"])
def data_environment(
    request: pytest.FixtureRequest,
    tmp_path: Path,
    pytestconfig: pytest.Config,
) -> tuple[Path, CheckService, DeliveredTemplate, dict[str, JsonValue], str]:
    """Keep native schema files, proposal scratch and all mutations in tmp_path."""
    template_id = str(request.param)
    root = tmp_path / "workspace"
    root.mkdir()
    copytree(
        pytestconfig.rootpath / ".pgmcp/config/check_schemas",
        root / ".pgmcp/config/check_schemas",
    )
    source_suite = pytestconfig.rootpath / ".pgmcp/template_suite"
    delivered = load_delivered_template(
        source_suite=source_suite,
        source_package=source_suite / template_id,
        config_root=pytestconfig.rootpath / ".pgmcp/config",
        destination=tmp_path / "suite",
        template_id=template_id,
    )
    loader = ConfigLoader(
        pytestconfig.rootpath / ".pgmcp/config",
    )
    catalog = AdapterCatalogLoader(
        pytestconfig.rootpath / "mcp_server/bundled_adapters",
        tmp_path / "workspace adapters",
        AdapterTrustConfig(trusted_adapter_ids=()),
        read_manifest=loader.load_adapter_manifest,
        files=FileAdapterPackageReader(),
        resolve_program=lambda name: Path(sys.executable) if name == "python" else None,
        windows=os.name == "nt",
    ).load()
    checks = CheckService(
        delivered.checks,
        catalog,
        AdapterProcessRuntime(AsyncioProcessBackend(), FileInvocationScratch(root / "invocations")),
        ContentInputPreparer(FileContentScratch(root / "snapshots", fresh_id=lambda: "proposal")),
        root,
    )
    (root / "artifacts").mkdir()
    (root / "artifacts/neighbor.txt").write_text("Untouched neighbor.\n", encoding="utf-8")
    context: dict[str, JsonValue] = (
        {"data": {"enabled": False, "count": 0, "caption": "yes"}}
        if template_id == "yaml_configuration"
        else {
            "schema": {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object"}
        }
    )
    # Ordinary .json has no extension profile: the original provenance must select it.
    filename = "settings.yaml" if template_id == "yaml_configuration" else "contract.json"
    return root, checks, delivered, context, filename


@pytest.mark.asyncio
async def test_data_scaffold_native_persistence(
    data_environment: tuple[Path, CheckService, DeliveredTemplate, dict[str, JsonValue], str],
) -> None:
    """Create valid native artifacts, retaining exact rendered bytes and native evidence."""
    root, checks, delivered, context, filename = data_environment
    identity = ArtifactIdentity.model_validate(thaw_json(delivered.provenance))
    locations = ArtifactLocationsConfig.model_validate(
        {"version": "2.0.0", "artifacts": {identity.id: {"default_root": "artifacts"}}}
    )
    operation = ScaffoldOperation(
        catalog=delivered.catalog,
        identities=(identity,),
        targets=ArtifactTargetResolver(
            paths=FileArtifactTargetPaths(root),
            temporary_artifacts_root=resolve_temporary_paths(root / "server").artifacts_root,
            locations=locations,
        ),
        render=delivered.renderer.render,
        checks=checks,
        creator=CreateOnlyFileWriter(),
        workspace_root=root,
    )
    result = await operation.execute(
        artifact_type=identity.id,
        file_name=filename,
        context=context,
        validation="enforce",
    )
    assert result.success and result.written and result.validation_status == "passed"
    assert result.checks and all(item.status == "passed" for item in result.checks)
    assert all(
        item.evidence is not None and item.evidence.format == "json" for item in result.checks
    )
    assert (root / "artifacts" / filename).read_bytes() == delivered.renderer.render(
        identity.id, context, delivered.provenance
    ).encode("utf-8")
    assert (root / "artifacts/neighbor.txt").read_text(encoding="utf-8") == "Untouched neighbor.\n"
    assert not list((root / "snapshots").iterdir())
    assert not list((root / "invocations").iterdir())


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("broken", "policy"),
    [(False, "enforce"), (True, "enforce"), (True, "report")],
)
async def test_data_edit_native_persistence(
    data_environment: tuple[Path, CheckService, DeliveredTemplate, dict[str, JsonValue], str],
    broken: bool,
    policy: Literal["enforce", "report"],
) -> None:
    """Select by original identity and prove native enforce/report persistence."""
    root, checks, delivered, context, filename = data_environment
    identity = ArtifactIdentity.model_validate(thaw_json(delivered.provenance))
    target = root / "artifacts" / filename
    original = delivered.renderer.render(identity.id, context, delivered.provenance)
    target.write_text(original, encoding="utf-8", newline="")
    if identity.id == "yaml_configuration":
        header = original.splitlines()[0]
        proposal = header + ("\n[]\n" if broken else '\n"changed": true\n')
    else:
        document = json.loads(original)
        document["type"] = 7 if broken else "array"
        proposal = json.dumps(document, ensure_ascii=False, indent=2) + "\n"
    profiles = {
        package.manifest.template_id: package.policy.output_profile
        for package in delivered.catalog.packages
    }
    operation = EditOperation(
        paths=FileArtifactTargetPaths(root),
        reader=OriginalFileReader(),
        writer=CheckedFileWriter(),
        select=lambda content, name, explicit: select_profile(
            content,
            name,
            explicit_template_id=explicit,
            header_reader=ArtifactHeaderReader(),
            template_profiles=profiles,
            extension_profile_for_filename=delivered.checks.match_for_filename,
        ),
        construct=construct_edit,
        checks=checks,
    )
    result = await operation.execute(
        path=f"artifacts/{filename}",
        operation=RewriteOperation(content=proposal),
        validation=policy,
    )
    expected_status = "failed" if broken else "passed"
    expected_write = not broken or policy == "report"
    assert result.selected_source == "metadata"
    assert result.validation_status == expected_status
    assert result.written is expected_write and result.success is expected_write
    assert result.checks and any(item.status == expected_status for item in result.checks)
    assert all(
        item.evidence is not None and item.evidence.format == "json" for item in result.checks
    )
    assert target.read_bytes() == (proposal if expected_write else original).encode("utf-8")
    if not expected_write:
        assert result.error_code == "validation_blocked"
    assert (root / "artifacts/neighbor.txt").read_text(encoding="utf-8") == "Untouched neighbor.\n"
    assert not list((root / "snapshots").iterdir())
    assert not list((root / "invocations").iterdir())
