"""Prepared template renewal CLI composition."""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Sequence
from contextlib import redirect_stderr
from datetime import UTC, datetime
from pathlib import Path
from typing import TextIO

from jinja2 import Environment

from mcp_server.config.loader import ConfigLoader
from mcp_server.config.settings import Settings
from mcp_server.config.validator import ConfigValidator
from mcp_server.core.exceptions import MCPError
from mcp_server.core.interfaces.template_catalog import FrozenJsonObject, freeze_json
from mcp_server.execution.catalog import AdapterCatalogLoader, FileAdapterPackageReader
from mcp_server.presenters.renewal_presenter import RenewalPresenter
from mcp_server.services.artifact_identity import ArtifactIdentity
from mcp_server.services.installation_state import InstallationStateRepository
from mcp_server.services.template_activation import (
    ActivationFiles,
    TemplateActivationService,
    UpgradeLock,
)
from mcp_server.services.template_catalog import TemplateCatalogLoader, TemplateInputValidator
from mcp_server.services.template_contract_loader import TemplateContractLoader
from mcp_server.services.template_graph import TemplateGraphResolver
from mcp_server.services.template_proposal import (
    SuiteSnapshot,
    TemplateProposalService,
    admit_template_suite,
)
from mcp_server.services.template_renewal import TemplateRenewalService
from mcp_server.utils.atomic_json_writer import AtomicJsonWriter


def build_parser() -> argparse.ArgumentParser:
    """Build the isolated renewal parser and its explicit owner modifiers."""

    parser = argparse.ArgumentParser(description="PGMCP template renewal")
    parser.add_argument("--upgrade", action="store_true", help="Renew the managed template suite")
    modifiers = parser.add_mutually_exclusive_group()
    modifiers.add_argument(
        "--accept-template-baseline",
        action="store_true",
        help="Accept a complete staged suite as the adopted baseline",
    )
    modifiers.add_argument(
        "--resolve-template",
        nargs="+",
        metavar="COMPONENT_ID",
        help="Advance named reconciled component checkpoint entries",
    )
    modifiers.add_argument(
        "--force-template-upgrade",
        action="store_true",
        help="Replace the complete managed suite after a verified backup",
    )
    return parser


def build_default_operation(
    settings: Settings, *, supplied_candidate_root: Path | None = None
) -> TemplateRenewalService:
    """Compose the real renewal boundary for an installed server root."""

    server_root = Path(settings.server.resolved_server_root).resolve()
    managed_root = server_root / "template_suite"
    actual_root = (
        Path(settings.server.resolved_template_root).resolve()
        if settings.server.template_root is not None
        else managed_root
    )
    legacy_root = server_root / "templates" if actual_root == managed_root else None
    legacy_version_path = server_root / ".version" if actual_root == managed_root else None
    candidate_root = server_root / "upgrade"
    proposal_root = server_root / "proposal"
    config_root = Path(settings.server.resolved_config_root).resolve()
    package_root = Path(__file__).resolve().parent
    official_adapters = package_root / "bundled_adapters"
    workspace_adapters = server_root / "workspace_adapters"
    validator = ConfigValidator()
    environment = Environment()
    provenance = freeze_json(ArtifactIdentity.model_json_schema())
    assert isinstance(provenance, FrozenJsonObject)

    def create_config(effective_config_root: Path, suite_root: Path) -> ConfigLoader:
        contracts = TemplateContractLoader(suite_root)
        return ConfigLoader(
            effective_config_root,
            suite_root,
            context_schema_reader=contracts.load_context_schema,
        )

    def create_catalog(
        suite_root: Path,
        config: ConfigLoader,
        profiles: frozenset[str],
    ) -> TemplateCatalogLoader:
        return TemplateCatalogLoader(
            suite_root,
            read_manifest=config.load_template_manifest,
            read_version=config.load_template_version,
            read_policy=config.load_template_policy,
            read_schema=config.load_template_context_schema,
            validate_policy=lambda policy: validator.validate_template_policy(policy, profiles),
            resolve_graph=TemplateGraphResolver(suite_root, environment.parse).resolve,
            validate_inputs=TemplateInputValidator(environment.parse, provenance).validate,
        )

    def create_adapters(config: ConfigLoader) -> AdapterCatalogLoader:
        return AdapterCatalogLoader(
            official_adapters,
            workspace_adapters,
            config.load_adapter_trust(),
            read_manifest=config.load_adapter_manifest,
            files=FileAdapterPackageReader(),
            resolve_program=lambda _adapter_id: None,
            windows=os.name == "nt",
        )

    def admit(root: Path) -> SuiteSnapshot:
        return admit_template_suite(
            root,
            config_root,
            create_config=create_config,
            create_catalog=create_catalog,
            create_adapters=create_adapters,
            validator=validator,
        )

    writer = AtomicJsonWriter().write_json
    repository = InstallationStateRepository(server_root / "installation.json", writer=writer)
    files = ActivationFiles(
        server_root,
        json_writer=writer,
        move=os.replace,
        read_installation=repository.read,
        legacy_root=legacy_root,
        legacy_version_path=legacy_version_path,
    )
    proposal = TemplateProposalService(
        actual_root=actual_root,
        candidate_root=candidate_root,
        proposal_root=proposal_root,
        effective_config_root=config_root,
        admit=lambda root, effective_config: admit_template_suite(
            root,
            effective_config,
            create_config=create_config,
            create_catalog=create_catalog,
            create_adapters=create_adapters,
            validator=validator,
        ),
    )
    lock = UpgradeLock(files.paths.lock)
    activation = TemplateActivationService(
        files,
        lock,
        admit=admit,
        clock=lambda: datetime.now(UTC),
    )

    def activate(root: Path, version: str, fresh: bool, force: bool) -> None:
        activation.activate(root, pgmcp_version=version, fresh=fresh, force=force)

    return TemplateRenewalService(
        actual_root=actual_root,
        candidate_root=candidate_root,
        proposal_root=proposal_root,
        pgmcp_version=settings.server.version,
        managed=actual_root == managed_root,
        legacy_root=legacy_root,
        legacy_version_path=legacy_version_path,
        supplied_candidate_root=(
            supplied_candidate_root.resolve()
            if supplied_candidate_root is not None
            else package_root / "assets" / "template_suite"
        ),
        stage_candidate=proposal.stage_candidate,
        hold_lock=lock.hold,
        recovery_pending=lambda: files.record() is not None,
        read_installation=repository.read,
        publish_installation=repository.publish,
        admit=proposal.admit,
        materialize_proposal=proposal.materialize_proposal,
        activate=activate,
        recover=activation.recover,
        read_activation_result=lambda: activation.last_result,
        discard_candidate=files.discard,
    )


class RenewalCli:
    """Run a prepared renewal operation and present its immutable result."""

    def __init__(
        self,
        *,
        operation: TemplateRenewalService,
        presenter: RenewalPresenter | None = None,
        stdout: TextIO | None = None,
        stderr: TextIO | None = None,
    ) -> None:
        self._operation = operation
        self._presenter = presenter or RenewalPresenter()
        self._stdout = stdout or sys.stdout
        self._stderr = stderr or sys.stderr

    def run(self, argv: Sequence[str] | None = None) -> int:
        """Parse one renewal command, execute it, and return its exit code."""

        parser = build_parser()
        try:
            with redirect_stderr(self._stderr):
                args, unknown = parser.parse_known_args(argv)
                if unknown:
                    parser.error(f"unrecognized arguments: {' '.join(unknown)}")
                if not args.upgrade:
                    parser.error("--upgrade is required for template renewal")
        except SystemExit as error:
            return int(error.code) if isinstance(error.code, int) else 2

        try:
            self._operation.execute(
                accept_baseline=bool(args.accept_template_baseline),
                force=bool(args.force_template_upgrade),
                resolve_components=tuple(args.resolve_template or ()),
            )
        except MCPError as error:
            print(f"Template upgrade failed: {error.message}", file=self._stderr)
            return 1
        except (OSError, ValueError, TypeError) as error:
            print(f"Template upgrade failed: {error}", file=self._stderr)
            return 1

        result = self._operation.last_result
        assert result is not None
        self._stdout.write(self._presenter.present(result))
        self._stdout.flush()
        return result.exit_code


def main(
    argv: Sequence[str] | None = None,
    *,
    operation: TemplateRenewalService | None = None,
    presenter: RenewalPresenter | None = None,
    settings: Settings | None = None,
) -> int:
    """Public entry point for the prepared renewal command."""

    resolved_settings = settings or Settings.from_env()
    resolved_operation = operation or build_default_operation(resolved_settings)
    return RenewalCli(operation=resolved_operation, presenter=presenter).run(argv)


__all__ = [
    "RenewalCli",
    "build_default_operation",
    "build_parser",
    "main",
]
