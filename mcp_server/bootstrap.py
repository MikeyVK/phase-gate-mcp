# mcp_server\bootstrap.py
# template=generic version=f35abd82 created=2026-06-09T09:48Z updated=
"""Bootstrap module.

Dependency injection and bootstrap orchestration layer.

@layer: MCP Server
@dependencies: [
    pathlib,
    dataclasses,
    mcp_server.config.loader,
    mcp_server.config.schemas,
    mcp_server.config.settings,
    mcp_server.config.validator,
    mcp_server.core.*,
    mcp_server.managers.*,
    mcp_server.state.*
]
@responsibilities:
    - Define immutable dataclasses for config models and managers.
    - Orchestrate composition root build phase.
"""

from __future__ import annotations

import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast, get_args, get_origin
from uuid import uuid4

from jinja2 import DictLoader, Environment
from pydantic import BaseModel

from mcp_server.adapters.git_adapter import GitAdapter
from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas import (
    ContractsConfig,
    ContributorConfig,
    EnforcementConfig,
    GitConfig,
    IssueConfig,
    LabelConfig,
    MilestoneConfig,
    OperationPoliciesConfig,
    PresentationConfig,
    QualityConfig,
    ScopeConfig,
    WorkflowConfig,
    WorkphasesConfig,
)
from mcp_server.config.settings import Settings
from mcp_server.config.validator import ConfigValidator
from mcp_server.core.commit_phase_detector import CommitPhaseDetector
from mcp_server.core.exceptions import ConfigError, MCPError
from mcp_server.core.interfaces import (
    ICoreTool,
    IToolResponsePublisher,
    IToolResponseReader,
)
from mcp_server.core.interfaces.template_catalog import FrozenJsonObject, freeze_json
from mcp_server.core.logging import get_logger, setup_logging
from mcp_server.core.phase_detection import ScopeDecoder
from mcp_server.core.tool_execution import operation_output_model
from mcp_server.core.tool_factory import ToolFactory as CoreToolFactory
from mcp_server.execution.catalog import AdapterCatalogLoader, FileAdapterPackageReader
from mcp_server.execution.check_selection import CheckSelector, FileScopePaths, ScopeResolver
from mcp_server.execution.check_service import CheckService, ContentInputPreparer
from mcp_server.execution.content_input import FileContentScratch
from mcp_server.execution.fix_service import FileFixScopePaths, FixManager
from mcp_server.execution.process_runtime import AdapterProcessRuntime, AsyncioProcessBackend
from mcp_server.execution.test_service import TestRunManager
from mcp_server.managers.branch_parent_reader import BranchStateParentReader
from mcp_server.managers.deliverable_checker import DeliverableChecker
from mcp_server.managers.enforcement_runner import EnforcementRunner
from mcp_server.managers.git_manager import GitManager
from mcp_server.managers.github_manager import GitHubManager
from mcp_server.managers.phase_contract_resolver import (
    MergeReadinessContext,
    PhaseConfigContext,
    PhaseContractResolver,
)
from mcp_server.managers.phase_state_engine import PhaseStateEngine
from mcp_server.managers.project_manager import ProjectManager
from mcp_server.managers.pytest_runner import PytestRunner
from mcp_server.managers.qa_manager import QAManager
from mcp_server.managers.quality_state_repository import FileQualityStateRepository
from mcp_server.managers.state_repository import BranchValidatedStateReader, FileStateRepository
from mcp_server.managers.workflow_gate_runner import WorkflowGateRunner
from mcp_server.managers.workflow_state_mutator import WorkflowStateMutator
from mcp_server.managers.workflow_status_resolver import WorkflowStatusResolver
from mcp_server.managers.workspace_version_validator import WorkspaceVersionValidator
from mcp_server.presenters.collection_text_renderer import CollectionTextRenderer
from mcp_server.presenters.response_presenter import ResponsePresenter
from mcp_server.presenters.schema_resource_presenter import (
    SchemaResourcePresenter,
)
from mcp_server.presenters.text_budget_limiter import TextBudgetLimiter
from mcp_server.presenters.text_presenter import (
    TextPresenter,
    validate_presentation_alignment,
)
from mcp_server.resources.base import BaseResource
from mcp_server.resources.cache import CachedResponseResource, CacheReadGuideResource
from mcp_server.resources.github import GitHubIssuesResource
from mcp_server.resources.standards import StandardsResource
from mcp_server.resources.status import StatusResource
from mcp_server.server import MCPServer
from mcp_server.services.artifact_header_reader import ArtifactHeaderReader
from mcp_server.services.artifact_identity import (
    ArtifactIdentity,
    GenerationEdge,
    derive_artifact_identities,
)
from mcp_server.services.artifact_target_resolver import ArtifactTargetResolver
from mcp_server.services.check_operation import CheckOperation
from mcp_server.services.edit_construction import (
    EditProfileSelection,
    construct_edit,
    select_profile,
)
from mcp_server.services.edit_operation import EditOperation
from mcp_server.services.installation_state import read_installation_state
from mcp_server.services.scaffold_operation import ScaffoldOperation
from mcp_server.services.template_activation import UpgradeLock
from mcp_server.services.template_catalog import (
    TemplateCatalogLoader,
    TemplateCatalogRenderer,
    TemplateInputValidator,
)
from mcp_server.services.template_contract_loader import TemplateContractLoader
from mcp_server.services.template_engine import TemplateEngine
from mcp_server.services.template_graph import TemplateGraphResolver
from mcp_server.services.template_proposal import admit_template_suite
from mcp_server.state.context_loaded_cache import ContextLoadedCache
from mcp_server.state.pr_status_cache import PRStatusCache
from mcp_server.state.response_cache import ResponseCacheManager
from mcp_server.tools.admin_tools import RestartServerTool

# Target V3 tool implementations
from mcp_server.tools.check_tools import RunChecksTool as TargetRunChecksTool
from mcp_server.tools.cycle_tools import ForceCycleTransitionTool, TransitionCycleTool
from mcp_server.tools.discovery_tools import GetWorkContextTool
from mcp_server.tools.edit_tool import SafeEditTool as TargetSafeEditTool
from mcp_server.tools.fix_tools import ApplyFixesTool as TargetApplyFixesTool
from mcp_server.tools.git_analysis_tools import GitDiffTool, GitListBranchesTool
from mcp_server.tools.git_fetch_tool import GitFetchTool
from mcp_server.tools.git_pull_tool import GitPullTool
from mcp_server.tools.git_tools import (
    CheckMergeTool,
    CreateBranchTool,
    GetParentBranchTool,
    GitCheckoutTool,
    GitCommitTool,
    GitDeleteBranchTool,
    GitMergeTool,
    GitPushTool,
    GitRestoreTool,
    GitStashTool,
    GitStatusTool,
    build_commit_type_resolver,
    build_phase_guard,
)
from mcp_server.tools.health_tools import HealthCheckTool
from mcp_server.tools.issue_tools import (
    CloseIssueTool,
    CreateIssueTool,
    GetIssueTool,
    ListIssuesTool,
    UpdateIssueTool,
)
from mcp_server.tools.label_tools import (
    AddLabelsTool,
    CreateLabelTool,
    DeleteLabelTool,
    ListLabelsTool,
    RemoveLabelsTool,
)
from mcp_server.tools.milestone_tools import (
    CloseMilestoneTool,
    CreateMilestoneTool,
    ListMilestonesTool,
)
from mcp_server.tools.phase_tools import ForcePhaseTransitionTool, TransitionPhaseTool
from mcp_server.tools.pr_tools import GetPRTool, ListPRsTool, MergePRTool, SubmitPRTool
from mcp_server.tools.project_tools import (
    GetProjectPlanTool,
    InitializeProjectTool,
    SavePlanningDeliverablesTool,
    UpdatePlanningDeliverablesTool,
)
from mcp_server.tools.quality_tools import AutoFixTool, RunQualityGatesTool
from mcp_server.tools.run_tests_tool import RunTestsTool as TargetRunTestsTool
from mcp_server.tools.scaffold_tool import ScaffoldArtifactTool as TargetScaffoldArtifactTool
from mcp_server.tools.template_schema_tool import ScaffoldSchemaTool as TargetScaffoldSchemaTool
from mcp_server.tools.test_tools import RunTestsTool
from mcp_server.utils.atomic_file_writer import (
    CheckedFileWriter,
    CreateOnlyFileWriter,
    OriginalFileReader,
)
from mcp_server.utils.path_resolver import FileArtifactTargetPaths, resolve_temporary_paths

if TYPE_CHECKING:
    from mcp_server.server import MCPServer
logger = get_logger("bootstrap")
lifecycle_logger = get_logger("server_lifecycle")


@dataclass(frozen=True)
class ConfigLayer:
    """Immutable layer containing all validated configurations."""

    git_config: GitConfig
    workflow_config: WorkflowConfig
    workphases_config: WorkphasesConfig
    quality_config: QualityConfig | None
    label_config: LabelConfig
    issue_config: IssueConfig
    scope_config: ScopeConfig
    milestone_config: MilestoneConfig
    contributor_config: ContributorConfig
    operation_policies_config: OperationPoliciesConfig
    enforcement_config: EnforcementConfig
    contracts_config: ContractsConfig
    presentation_config: PresentationConfig


@dataclass(frozen=True)
class ManagerGraph:
    """Immutable graph of instantiated managers and services."""

    git_manager: GitManager
    state_repository: FileStateRepository
    workflow_status_resolver: WorkflowStatusResolver
    project_manager: ProjectManager
    phase_contract_resolver: PhaseContractResolver
    workflow_gate_runner: WorkflowGateRunner
    workflow_state_mutator: WorkflowStateMutator
    context_loaded_cache: ContextLoadedCache
    phase_state_engine: PhaseStateEngine
    quality_state_repository: FileQualityStateRepository
    qa_manager: QAManager | None
    github_manager: GitHubManager
    pr_status_cache: PRStatusCache
    enforcement_runner: EnforcementRunner
    response_cache: IToolResponsePublisher | IToolResponseReader


@dataclass(frozen=True)
class SupportedToolContract:
    """Minimal presentation-validation contract derived from a core tool."""

    name: str
    output_model: type[BaseModel]


def _resolve_generic_output_models(tool_type: type[Any]) -> tuple[type[BaseModel], ...]:
    """Resolve concrete ICoreTool output arguments across generic base classes."""
    resolved: list[type[BaseModel]] = []

    def resolve_binding(value: object, bindings: dict[object, object]) -> object:
        seen: set[object] = set()
        current = value
        while current in bindings and current not in seen:
            seen.add(current)
            current = bindings[current]
        return current

    def visit(current: type[Any], bindings: dict[object, object]) -> None:
        original_bases = current.__dict__.get("__orig_bases__")
        bases = original_bases if original_bases is not None else current.__bases__
        for generic_base in bases:
            origin = get_origin(generic_base) or generic_base
            arguments = tuple(
                resolve_binding(argument, bindings) for argument in get_args(generic_base)
            )
            if origin is ICoreTool:
                if len(arguments) != 2:
                    continue
                output_candidate = arguments[1]
                if isinstance(output_candidate, type) and issubclass(output_candidate, BaseModel):
                    operation_model = operation_output_model(output_candidate)
                    if operation_model not in resolved:
                        resolved.append(operation_model)
                continue
            if not isinstance(origin, type) or origin is object:
                continue
            parameters = getattr(origin, "__parameters__", ())
            child_bindings = dict(zip(parameters, arguments, strict=False))
            visit(origin, child_bindings)

    visit(tool_type, {})
    return tuple(resolved)


def _resolve_supported_tool_contract(tool: object) -> SupportedToolContract:
    """Derive and validate the minimal contract for one supported core tool."""
    name = getattr(tool, "name", None)
    if not isinstance(name, str) or not name.strip():
        raise ConfigError("Supported tool name must be a non-empty string")

    explicit_model = getattr(tool, "output_model", None)
    if explicit_model is not None and (
        not isinstance(explicit_model, type) or not issubclass(explicit_model, BaseModel)
    ):
        raise ConfigError(f"Invalid explicit output model for supported tool '{name}'")

    if explicit_model is not None:
        explicit_model = operation_output_model(explicit_model)

    generic_models = _resolve_generic_output_models(type(tool))
    if len(generic_models) > 1:
        model_names = ", ".join(model.__name__ for model in generic_models)
        raise ConfigError(
            f"Conflicting generic output models for supported tool '{name}': {model_names}"
        )

    generic_model = generic_models[0] if generic_models else None
    if (
        explicit_model is not None
        and generic_model is not None
        and explicit_model is not generic_model
    ):
        raise ConfigError(
            f"Conflicting explicit and generic output models for supported tool '{name}'"
        )

    output_model = explicit_model or generic_model
    if output_model is None:
        raise ConfigError(f"Unable to resolve output model for supported tool '{name}'")
    return SupportedToolContract(name=name, output_model=output_model)


@dataclass(frozen=True)
class ToolAssembly:
    """Complete supported core tools plus the settings-dependent active subset."""

    supported_tools: tuple[ICoreTool[Any, Any], ...]
    active_tools: tuple[ICoreTool[Any, Any], ...]
    supported_contracts: tuple[SupportedToolContract, ...] = field(init=False)

    def __post_init__(self) -> None:
        contracts = tuple(_resolve_supported_tool_contract(tool) for tool in self.supported_tools)
        names = [contract.name for contract in contracts]
        duplicate_names = sorted({name for name in names if names.count(name) > 1})
        if duplicate_names:
            raise ConfigError("Duplicate supported tool names: " + ", ".join(duplicate_names))

        supported_ids = {id(tool) for tool in self.supported_tools}
        if any(id(tool) not in supported_ids for tool in self.active_tools):
            raise ConfigError("Every active tool must be an object from supported_tools")

        object.__setattr__(self, "supported_contracts", contracts)

    @classmethod
    def create(
        cls,
        supported_tools: tuple[Any, ...],
        active_tools: tuple[Any, ...],
    ) -> ToolAssembly:
        """Validate and freeze supported and active core-tool tuples."""
        return cls(
            supported_tools=cast(tuple[ICoreTool[Any, Any], ...], supported_tools),
            active_tools=cast(tuple[ICoreTool[Any, Any], ...], active_tools),
        )


class ServerBootstrapper:
    """Orchestrates configuration loading and manager graph instantiation."""

    def __init__(self, settings: Settings | None = None) -> None:
        """Initialize bootstrapper with settings."""
        self._settings = settings or Settings.from_env()

    def bootstrap(self) -> MCPServer:
        """Bootstrap logging, config, registry, and managers, and return MCPServer."""
        settings = self._settings

        # Configure logging
        _server_root_early = settings.server.resolved_server_root
        _logs_dir_early = _server_root_early / settings.server.logs_dir
        _audit_log = settings.logging.audit_log or str(_logs_dir_early / "mcp_audit.log")
        setup_logging(settings.logging.level, _audit_log)

        lifecycle_logger.info("MCP server starting via bootstrapper")

        # Validate workspace version
        self._validate_version()

        # Build ConfigLayer
        configs = self._build_config_layer()

        # Build ManagerGraph
        managers = self._build_manager_graph(configs)

        # Build Tools and Resources
        tool_assembly = self._build_tool_assembly(configs, managers)
        resources = self._build_resources(configs, managers)

        presentation_config = configs.presentation_config
        text_presenter = TextPresenter(
            config=presentation_config,
            collection_renderer=CollectionTextRenderer(
                presentation_config.global_settings.formatting
            ),
            budget_limiter=TextBudgetLimiter(
                max_text_response_bytes=(
                    presentation_config.global_settings.max_text_response_bytes
                ),
                formatting=presentation_config.global_settings.formatting,
            ),
        )
        validate_presentation_alignment(
            text_presenter,
            tool_assembly.supported_contracts,
        )
        resource_presenter = SchemaResourcePresenter()
        presenter = ResponsePresenter(
            text_presenter=text_presenter,
            resource_presenter=resource_presenter,
        )

        # Decorate core tools using ToolFactory composition root
        factory = CoreToolFactory(
            enforcement_runner=managers.enforcement_runner,
            workspace_root=Path(settings.server.workspace_root),
        )
        tools = [factory.create_tool(tool) for tool in tool_assembly.active_tools]

        return MCPServer(
            settings=settings,
            tools=tools,
            resources=resources,
            presenter=presenter,
            publisher=managers.response_cache,
        )

    def bootstrap_target(self) -> MCPServer:
        """Compose and return the target V3 MCPServer under the DI-06 startup lock."""
        settings = self._settings
        server_root = settings.server.resolved_server_root
        config_root = settings.server.resolved_config_root
        template_root = (
            Path(settings.server.template_root)
            if settings.server.template_root is not None
            else server_root / "template_suite"
        )
        workspace_root = Path(settings.server.workspace_root)

        # 1. DI-06 Startup Lock Check and Acquisition
        lock_path = server_root / "template_upgrade.lock"
        upgrade_lock = UpgradeLock(lock_path)
        upgrade_lock.acquire()

        try:
            # 2. Check for unresolved recovery record
            recovery_record_path = server_root / "template_upgrade.json"
            if recovery_record_path.exists():
                raise MCPError("template_recovery_unknown", code="ERR_CONFIG")

            installation_path = server_root / "installation.json"
            installation = read_installation_state(installation_path)
            if not settings.server.bypass_version_check:
                if installation is None:
                    raise ConfigError(
                        f"Workspace installation state is missing: '{installation_path}'. "
                        "Please run with '--init' to initialize the workspace.",
                        file_path=installation_path.as_posix(),
                    )
                if installation.pgmcp_version != settings.server.version:
                    raise ConfigError(
                        f"Workspace version mismatch. Workspace version: "
                        f"{installation.pgmcp_version}, server version: "
                        f"{settings.server.version}. Please run 'pgmcp --upgrade'.",
                        file_path=installation_path.as_posix(),
                    )

            # 3. Load configurations via ConfigLoader
            contracts_loader = TemplateContractLoader(template_root)
            config_loader = ConfigLoader(
                config_root=config_root,
                template_root=template_root,
                context_schema_reader=contracts_loader.load_context_schema,
            )

            # Load V2/V3 configurations
            git_config = config_loader.load_git_config()
            workflow_config = config_loader.load_workflow_config()
            workphases_config = config_loader.load_workphases_config()
            label_config = config_loader.load_label_config()
            issue_config = config_loader.load_issue_config()
            scope_config = config_loader.load_scope_config()
            milestone_config = config_loader.load_milestone_config()
            contributor_config = config_loader.load_contributor_config()
            checks_config = config_loader.load_checks_config()
            tests_config = config_loader.load_tests_config()
            fixes_config = config_loader.load_fixes_config()
            locations_config = config_loader.load_artifact_locations_config()
            operation_policies_config = config_loader.load_operation_policies_config()
            enforcement_config = config_loader.load_enforcement_config()
            contracts_config = config_loader.load_contracts_config()
            presentation_config = config_loader.load_presentation_config()

            validator = ConfigValidator()

            # Admit one complete source snapshot before constructing runtime consumers.
            parser = Environment()
            provenance_schema = freeze_json(ArtifactIdentity.model_json_schema())
            assert isinstance(provenance_schema, FrozenJsonObject)
            package_root = Path(__file__).resolve().parent

            def create_config(effective_root: Path, suite_root: Path) -> ConfigLoader:
                return ConfigLoader(
                    effective_root,
                    suite_root,
                    context_schema_reader=contracts_loader.load_context_schema,
                )

            def create_catalog(
                suite_root: Path, config: ConfigLoader, profiles: frozenset[str]
            ) -> TemplateCatalogLoader:
                return TemplateCatalogLoader(
                    suite_root,
                    read_manifest=config.load_template_manifest,
                    read_version=config.load_template_version,
                    read_policy=config.load_template_policy,
                    read_schema=config.load_template_context_schema,
                    validate_policy=lambda policy: validator.validate_template_policy(
                        policy, profiles
                    ),
                    resolve_graph=TemplateGraphResolver(suite_root, parser.parse).resolve,
                    validate_inputs=TemplateInputValidator(
                        parser.parse, provenance_schema
                    ).validate,
                )

            def create_adapters(config: ConfigLoader) -> AdapterCatalogLoader:
                return AdapterCatalogLoader(
                    package_root / "bundled_adapters",
                    server_root / "workspace_adapters",
                    config.load_adapter_trust(),
                    read_manifest=config.load_adapter_manifest,
                    files=FileAdapterPackageReader(),
                    resolve_program=lambda name: (
                        Path(found).resolve() if (found := shutil.which(name)) else None
                    ),
                    windows=sys.platform == "win32",
                )

            snapshot = admit_template_suite(
                template_root,
                config_root,
                create_config=create_config,
                create_catalog=create_catalog,
                create_adapters=create_adapters,
                validator=validator,
            )
            template_catalog = snapshot.catalog

            # Validate artifact locations against loaded catalog IDs
            known_ids = frozenset(p.manifest.template_id for p in template_catalog.packages)
            validator.validate_artifact_locations(locations_config, known_ids)

            # Preserve the shared workflow validation without legacy artifact inputs.
            validator.validate_startup(
                policies=operation_policies_config,
                workflow=workflow_config,
                contracts=contracts_config,
                workphases=workphases_config,
            )

            identities = derive_artifact_identities(
                snapshot.packages,
                snapshot.sources,
                (
                    *(
                        GenerationEdge(
                            source=edge.source,
                            target=edge.target,
                            kind=edge.kind,
                            position=str(edge.line),
                        )
                        for edge in template_catalog.graph.edges
                    ),
                    *(
                        GenerationEdge(
                            source=source,
                            target=target,
                            kind="schema_ref",
                            position=reference,
                        )
                        for source, target, reference in contracts_loader.reference_edges
                    ),
                ),
            )

            # 5. Build the unrelated workflow, Git, GitHub, and enforcement managers.
            configs = ConfigLayer(
                git_config=git_config,
                workflow_config=workflow_config,
                workphases_config=workphases_config,
                quality_config=None,
                label_config=label_config,
                issue_config=issue_config,
                scope_config=scope_config,
                milestone_config=milestone_config,
                contributor_config=contributor_config,
                operation_policies_config=operation_policies_config,
                enforcement_config=enforcement_config,
                contracts_config=contracts_config,
                presentation_config=presentation_config,
            )
            managers = self._build_manager_graph(configs)

            # Target V3 service engines
            target_resolver = ArtifactTargetResolver(
                paths=FileArtifactTargetPaths(workspace_root),
                temporary_artifacts_root=resolve_temporary_paths(server_root).artifacts_root,
                locations=locations_config,
            )

            render_environment = Environment(
                loader=DictLoader(
                    {
                        source.name: source.content.decode("utf-8-sig")
                        for source in template_catalog.graph.sources
                    }
                )
            )
            engine = TemplateEngine(environment=render_environment)
            renderer = TemplateCatalogRenderer(
                template_catalog,
                validate_context=validator.validate_template_context,
                render_context=engine.render_context,
            )

            adapter_catalog = create_adapters(config_loader).load()
            validator.validate_checks_config(
                checks_config,
                adapter_catalog,
                template_profiles=frozenset(
                    p.policy.output_profile for p in template_catalog.packages
                ),
            )
            validator.validate_tests_config(tests_config, adapter_catalog)
            validator.validate_fixes_config(fixes_config, adapter_catalog)
            process_runtime = AdapterProcessRuntime(AsyncioProcessBackend())
            scratch = FileContentScratch(
                resolve_temporary_paths(server_root).validation_root,
                fresh_id=lambda: uuid4().hex,
            )
            check_service = CheckService(
                config=checks_config,
                catalog=adapter_catalog,
                runtime=process_runtime,
                content=ContentInputPreparer(scratch),
                workspace_root=workspace_root,
            )
            scope_resolver = ScopeResolver(
                paths=FileScopePaths(workspace_root),
                git=GitAdapter(repo_path=str(workspace_root)),
                parents=BranchStateParentReader(
                    state_reader=managers.state_repository,
                    git_config=git_config,
                ),
            )
            check_selector = CheckSelector(
                config=checks_config,
                catalog=adapter_catalog,
                scopes=scope_resolver,
            )
            check_operation = CheckOperation(selector=check_selector, executor=check_service)

            scaffold_op = ScaffoldOperation(
                catalog=template_catalog,
                identities=identities,
                targets=target_resolver,
                render=renderer.render,
                checks=check_service,
                creator=CreateOnlyFileWriter(),
                workspace_root=workspace_root,
            )
            template_profiles = {
                package.manifest.template_id: package.policy.output_profile
                for package in template_catalog.packages
            }
            header_reader = ArtifactHeaderReader()

            def choose_edit_profile(
                original: str, filename: str, explicit_template_id: str | None
            ) -> EditProfileSelection:
                return select_profile(
                    original,
                    filename,
                    explicit_template_id=explicit_template_id,
                    header_reader=header_reader,
                    template_profiles=template_profiles,
                    extension_profile_for_filename=checks_config.match_for_filename,
                )

            edit_op = EditOperation(
                paths=FileArtifactTargetPaths(workspace_root),
                reader=OriginalFileReader(),
                writer=CheckedFileWriter(),
                select=choose_edit_profile,
                construct=construct_edit,
                checks=check_service,
            )
            test_run_manager = TestRunManager(
                config=tests_config,
                catalog=adapter_catalog,
                runtime=process_runtime,
                paths=FileScopePaths(workspace_root),
            )
            fix_manager = FixManager(
                config=fixes_config,
                catalog=adapter_catalog,
                runtime=process_runtime,
                paths=FileFixScopePaths(workspace_root),
            )

            # 6. Compose the 6 Target V3 Tools
            target_tools = (
                TargetScaffoldArtifactTool(catalog=template_catalog, operation=scaffold_op),
                TargetScaffoldSchemaTool(catalog=template_catalog, identities=identities),
                TargetSafeEditTool(catalog=template_catalog, operation=edit_op),
                TargetRunChecksTool(operation=check_operation, config=checks_config),
                TargetRunTestsTool(manager=test_run_manager, config=tests_config),
                TargetApplyFixesTool(manager=fix_manager, config=fixes_config),
            )

            tool_assembly = self._build_target_tool_assembly(
                configs=configs,
                managers=managers,
                target_v3_tools=target_tools,
            )
            resources = self._build_resources(
                configs,
                managers,
                standards=StandardsResource(
                    checks=checks_config,
                    tests=tests_config,
                    fixes=fixes_config,
                ),
            )

            # 7. Presentation & Alignment
            text_presenter = TextPresenter(
                config=presentation_config,
                collection_renderer=CollectionTextRenderer(
                    presentation_config.global_settings.formatting
                ),
                budget_limiter=TextBudgetLimiter(
                    max_text_response_bytes=(
                        presentation_config.global_settings.max_text_response_bytes
                    ),
                    formatting=presentation_config.global_settings.formatting,
                ),
            )
            validate_presentation_alignment(
                text_presenter,
                tool_assembly.supported_contracts,
            )
            resource_presenter = SchemaResourcePresenter()
            presenter = ResponsePresenter(
                text_presenter=text_presenter,
                resource_presenter=resource_presenter,
            )

            factory = CoreToolFactory(
                enforcement_runner=managers.enforcement_runner,
                workspace_root=workspace_root,
            )
            tools = [factory.create_tool(tool) for tool in tool_assembly.active_tools]

            return MCPServer(
                settings=settings,
                tools=tools,
                resources=resources,
                presenter=presenter,
                publisher=managers.response_cache,
            )
        finally:
            upgrade_lock.release()

    def _validate_version(self) -> None:
        """Validate that the workspace version matches the running server version."""
        validator = WorkspaceVersionValidator()
        validator.validate(
            server_root=self._settings.server.resolved_server_root,
            expected_version=self._settings.server.version,
            bypass_version_check=self._settings.server.bypass_version_check,
        )

    def _build_config_layer(self) -> ConfigLayer:
        """Load and validate all configurations."""
        config_root = self._settings.server.resolved_config_root

        config_loader = ConfigLoader(
            config_root=config_root,
            template_root=self._settings.server.resolved_template_root,
        )
        git_config = config_loader.load_git_config()
        workflow_config = config_loader.load_workflow_config()
        workphases_config = config_loader.load_workphases_config()
        quality_config = config_loader.load_quality_config()
        label_config = config_loader.load_label_config()
        issue_config = config_loader.load_issue_config()
        scope_config = config_loader.load_scope_config()
        milestone_config = config_loader.load_milestone_config()
        contributor_config = config_loader.load_contributor_config()
        operation_policies_config = config_loader.load_operation_policies_config()
        enforcement_config = config_loader.load_enforcement_config()
        contracts_config = config_loader.load_contracts_config()
        presentation_config = config_loader.load_presentation_config()

        ConfigValidator().validate_startup(
            policies=operation_policies_config,
            workflow=workflow_config,
            contracts=contracts_config,
            workphases=workphases_config,
        )

        return ConfigLayer(
            git_config=git_config,
            workflow_config=workflow_config,
            workphases_config=workphases_config,
            quality_config=quality_config,
            label_config=label_config,
            issue_config=issue_config,
            scope_config=scope_config,
            milestone_config=milestone_config,
            contributor_config=contributor_config,
            operation_policies_config=operation_policies_config,
            enforcement_config=enforcement_config,
            contracts_config=contracts_config,
            presentation_config=presentation_config,
        )

    def _build_manager_graph(self, configs: ConfigLayer) -> ManagerGraph:
        """Instantiate all managers and services."""
        workspace_root = Path(self._settings.server.workspace_root)
        server_root = workspace_root / self._settings.server.server_root_dir
        logs_dir = server_root / self._settings.server.logs_dir

        git_manager = GitManager(
            git_config=configs.git_config,
            workphases_config=configs.workphases_config,
        )
        state_repository = FileStateRepository(state_file=server_root / "state.json")
        branch_validated_reader = BranchValidatedStateReader(inner=state_repository)
        commit_phase_detector = CommitPhaseDetector(
            workphases_config=configs.workphases_config,
        )
        workflow_status_resolver = WorkflowStatusResolver(
            git_context_reader=git_manager,
            state_reader=branch_validated_reader,
            commit_phase_detector=commit_phase_detector,
        )
        project_manager = ProjectManager(
            workspace_root=workspace_root,
            contracts_config=configs.contracts_config,
            git_manager=git_manager,
            workphases_config=configs.workphases_config,
            workflow_status_resolver=workflow_status_resolver,
            server_root=server_root,
        )
        phase_contract_resolver = PhaseContractResolver(
            PhaseConfigContext(
                workphases=configs.workphases_config,
                contracts=configs.contracts_config,
            )
        )
        workflow_gate_runner = WorkflowGateRunner(
            deliverable_checker=DeliverableChecker(workspace_root),
            phase_contract_resolver=phase_contract_resolver,
        )
        workflow_state_mutator = WorkflowStateMutator(
            state_repository=state_repository,
        )
        context_loaded_cache = ContextLoadedCache()
        phase_state_engine = PhaseStateEngine(
            workspace_root=workspace_root,
            project_manager=project_manager,
            git_config=configs.git_config,
            contracts_config=configs.contracts_config,
            state_repository=state_repository,
            scope_decoder=ScopeDecoder(
                workphases_config=configs.workphases_config,
            ),
            workflow_gate_runner=workflow_gate_runner,
            context_loaded_writer=context_loaded_cache,
            server_root=server_root,
        )
        quality_state_repository = FileQualityStateRepository(
            backing_file=server_root / "quality_state.json"
        )
        qa_manager = (
            QAManager(
                workspace_root=workspace_root,
                quality_config=configs.quality_config,
                logs_dir=logs_dir,
                quality_state_repository=quality_state_repository,
                git_context_reader=git_manager,
                state_reader=branch_validated_reader,
            )
            if configs.quality_config is not None
            else None
        )
        github_manager = GitHubManager(
            issue_config=configs.issue_config,
            label_config=configs.label_config,
            scope_config=configs.scope_config,
            milestone_config=configs.milestone_config,
            contributor_config=configs.contributor_config,
            git_config=configs.git_config,
        )
        pr_status_cache = PRStatusCache(github_manager=github_manager)
        enforcement_runner = EnforcementRunner(
            workspace_root=workspace_root,
            config=configs.enforcement_config,
            git_config=configs.git_config,
            state_reader=state_repository,
            pr_status_reader=pr_status_cache,
            server_root=server_root,
            context_loaded_reader=context_loaded_cache,
        )
        response_cache = ResponseCacheManager(max_size=50)
        return ManagerGraph(
            git_manager=git_manager,
            state_repository=state_repository,
            workflow_status_resolver=workflow_status_resolver,
            project_manager=project_manager,
            phase_contract_resolver=phase_contract_resolver,
            workflow_gate_runner=workflow_gate_runner,
            workflow_state_mutator=workflow_state_mutator,
            context_loaded_cache=context_loaded_cache,
            phase_state_engine=phase_state_engine,
            quality_state_repository=quality_state_repository,
            qa_manager=qa_manager,
            github_manager=github_manager,
            pr_status_cache=pr_status_cache,
            enforcement_runner=enforcement_runner,
            response_cache=response_cache,
        )

    def _build_tool_assembly(
        self,
        configs: ConfigLayer,
        managers: ManagerGraph,
    ) -> ToolAssembly:
        """Compose all supported tools and select the settings-dependent active subset."""
        settings = self._settings
        qa_manager = managers.qa_manager
        if qa_manager is None:
            raise ConfigError("Legacy tool assembly requires legacy quality manager")
        branch_validated_reader = BranchValidatedStateReader(inner=managers.state_repository)
        merge_readiness_context = MergeReadinessContext(
            terminal_phase=configs.workphases_config.get_terminal_phase(),
            pr_allowed_phase=configs.contracts_config.get_pr_allowed_phase(),
            branch_local_artifacts=tuple(
                configs.contracts_config.merge_policy.branch_local_artifacts
            ),
        )

        base_tools: list[ICoreTool[Any, Any]] = [
            CreateBranchTool(manager=managers.git_manager),
            GitStatusTool(manager=managers.git_manager),
            GitCommitTool(
                manager=managers.git_manager,
                phase_guard=build_phase_guard(
                    state_reader=branch_validated_reader,
                    phase_contract_resolver=managers.phase_contract_resolver,
                ),
                commit_type_resolver=build_commit_type_resolver(
                    managers.phase_state_engine,
                    managers.phase_contract_resolver,
                ),
                state_engine=managers.phase_state_engine,
                phase_contract_resolver=managers.phase_contract_resolver,
            ),
            GitCheckoutTool(
                manager=managers.git_manager,
                state_engine=managers.phase_state_engine,
                context_loaded_writer=managers.context_loaded_cache,
            ),
            GitFetchTool(manager=managers.git_manager),
            GitPullTool(
                manager=managers.git_manager,
                state_engine=managers.phase_state_engine,
                context_loaded_writer=managers.context_loaded_cache,
            ),
            GitPushTool(manager=managers.git_manager),
            GitMergeTool(manager=managers.git_manager),
            GitDeleteBranchTool(manager=managers.git_manager),
            GitStashTool(manager=managers.git_manager),
            GitRestoreTool(manager=managers.git_manager),
            GitListBranchesTool(manager=managers.git_manager),
            GitDiffTool(manager=managers.git_manager),
            GetParentBranchTool(
                manager=managers.git_manager,
                state_engine=managers.phase_state_engine,
            ),
            CheckMergeTool(manager=managers.git_manager),
            RunQualityGatesTool(manager=qa_manager),
            HealthCheckTool(),
            RestartServerTool(
                server_root=(Path(settings.server.workspace_root) / settings.server.server_root_dir)
            ),
            RunTestsTool(runner=PytestRunner(), settings=settings),
            InitializeProjectTool(
                workspace_root=Path(settings.server.workspace_root),
                manager=managers.project_manager,
                git_manager=managers.git_manager,
                state_engine=managers.phase_state_engine,
                contracts_config=configs.contracts_config,
            ),
            GetProjectPlanTool(manager=managers.project_manager),
            SavePlanningDeliverablesTool(manager=managers.project_manager),
            UpdatePlanningDeliverablesTool(manager=managers.project_manager),
            TransitionPhaseTool(
                workspace_root=Path(settings.server.workspace_root),
                project_manager=managers.project_manager,
                state_engine=managers.phase_state_engine,
                server_root=(
                    Path(settings.server.workspace_root) / settings.server.server_root_dir
                ),
                workphases_config=configs.workphases_config,
            ),
            ForcePhaseTransitionTool(
                workspace_root=Path(settings.server.workspace_root),
                project_manager=managers.project_manager,
                state_engine=managers.phase_state_engine,
                server_root=(
                    Path(settings.server.workspace_root) / settings.server.server_root_dir
                ),
                workphases_config=configs.workphases_config,
            ),
            TransitionCycleTool(
                workspace_root=Path(settings.server.workspace_root),
                project_manager=managers.project_manager,
                state_engine=managers.phase_state_engine,
                git_manager=managers.git_manager,
                gate_runner=managers.workflow_gate_runner,
                server_root=(
                    Path(settings.server.workspace_root) / settings.server.server_root_dir
                ),
            ),
            ForceCycleTransitionTool(
                workspace_root=Path(settings.server.workspace_root),
                project_manager=managers.project_manager,
                state_engine=managers.phase_state_engine,
                git_manager=managers.git_manager,
                gate_runner=managers.workflow_gate_runner,
                server_root=(
                    Path(settings.server.workspace_root) / settings.server.server_root_dir
                ),
            ),
            GetWorkContextTool(
                settings=settings,
                git_manager=managers.git_manager,
                project_manager=managers.project_manager,
                state_engine=managers.phase_state_engine,
                github_manager=managers.github_manager,
                workphases_config=configs.workphases_config,
                workflow_status_resolver=managers.workflow_status_resolver,
                contracts_config=configs.contracts_config,
                context_loaded_writer=managers.context_loaded_cache,
            ),
        ]

        issue_tools: list[ICoreTool[Any, Any]] = [
            CreateIssueTool(
                manager=managers.github_manager,
                issue_config=configs.issue_config,
                milestone_config=configs.milestone_config,
                contracts_config=configs.contracts_config,
                label_config=configs.label_config,
                scope_config=configs.scope_config,
                git_config=configs.git_config,
            ),
            ListIssuesTool(manager=managers.github_manager),
            GetIssueTool(manager=managers.github_manager),
            CloseIssueTool(manager=managers.github_manager),
            UpdateIssueTool(manager=managers.github_manager),
        ]

        credential_tools: list[ICoreTool[Any, Any]] = [
            ListPRsTool(
                manager=managers.github_manager,
                git_config=configs.git_config,
            ),
            GetPRTool(manager=managers.github_manager),
            MergePRTool(
                manager=managers.github_manager,
                git_config=configs.git_config,
                pr_status_writer=managers.pr_status_cache,
            ),
            SubmitPRTool(
                git_manager=managers.git_manager,
                github_manager=managers.github_manager,
                pr_status_writer=managers.pr_status_cache,
                merge_readiness_context=merge_readiness_context,
                branch_parent_reader=BranchStateParentReader(
                    state_reader=managers.state_repository,
                    git_config=configs.git_config,
                ),
            ),
            AddLabelsTool(
                manager=managers.github_manager,
                label_config=configs.label_config,
                workphases_config=configs.workphases_config,
            ),
            ListLabelsTool(
                manager=managers.github_manager,
                label_config=configs.label_config,
            ),
            CreateLabelTool(
                manager=managers.github_manager,
                label_config=configs.label_config,
                workphases_config=configs.workphases_config,
            ),
            DeleteLabelTool(
                manager=managers.github_manager,
                label_config=configs.label_config,
            ),
            RemoveLabelsTool(
                manager=managers.github_manager,
                label_config=configs.label_config,
            ),
            ListMilestonesTool(manager=managers.github_manager),
            CreateMilestoneTool(manager=managers.github_manager),
            CloseMilestoneTool(manager=managers.github_manager),
        ]

        auto_fix_tool = AutoFixTool(qa_manager=qa_manager)
        supported_tools = (*base_tools, *issue_tools, *credential_tools, auto_fix_tool)
        active_tools = (
            supported_tools if settings.github.token else (*base_tools, *issue_tools, auto_fix_tool)
        )
        return ToolAssembly.create(
            supported_tools=supported_tools,
            active_tools=active_tools,
        )

    def _build_target_tool_assembly(
        self,
        configs: ConfigLayer,
        managers: ManagerGraph,
        target_v3_tools: tuple[ICoreTool[Any, Any], ...],
    ) -> ToolAssembly:
        """Compose the target V3 runtime ToolAssembly without legacy V2 tools."""
        settings = self._settings
        branch_validated_reader = BranchValidatedStateReader(inner=managers.state_repository)
        merge_readiness_context = MergeReadinessContext(
            terminal_phase=configs.workphases_config.get_terminal_phase(),
            pr_allowed_phase=configs.contracts_config.get_pr_allowed_phase(),
            branch_local_artifacts=tuple(
                configs.contracts_config.merge_policy.branch_local_artifacts
            ),
        )

        unchanged_base_tools: list[ICoreTool[Any, Any]] = [
            CreateBranchTool(manager=managers.git_manager),
            GitStatusTool(manager=managers.git_manager),
            GitCommitTool(
                manager=managers.git_manager,
                phase_guard=build_phase_guard(
                    state_reader=branch_validated_reader,
                    phase_contract_resolver=managers.phase_contract_resolver,
                ),
                commit_type_resolver=build_commit_type_resolver(
                    managers.phase_state_engine,
                    managers.phase_contract_resolver,
                ),
                state_engine=managers.phase_state_engine,
                phase_contract_resolver=managers.phase_contract_resolver,
            ),
            GitCheckoutTool(
                manager=managers.git_manager,
                state_engine=managers.phase_state_engine,
                context_loaded_writer=managers.context_loaded_cache,
            ),
            GitFetchTool(manager=managers.git_manager),
            GitPullTool(
                manager=managers.git_manager,
                state_engine=managers.phase_state_engine,
                context_loaded_writer=managers.context_loaded_cache,
            ),
            GitPushTool(manager=managers.git_manager),
            GitMergeTool(manager=managers.git_manager),
            GitDeleteBranchTool(manager=managers.git_manager),
            GitStashTool(manager=managers.git_manager),
            GitRestoreTool(manager=managers.git_manager),
            GitListBranchesTool(manager=managers.git_manager),
            GitDiffTool(manager=managers.git_manager),
            GetParentBranchTool(
                manager=managers.git_manager,
                state_engine=managers.phase_state_engine,
            ),
            CheckMergeTool(manager=managers.git_manager),
            HealthCheckTool(),
            RestartServerTool(
                server_root=(Path(settings.server.workspace_root) / settings.server.server_root_dir)
            ),
            InitializeProjectTool(
                workspace_root=Path(settings.server.workspace_root),
                manager=managers.project_manager,
                git_manager=managers.git_manager,
                state_engine=managers.phase_state_engine,
                contracts_config=configs.contracts_config,
            ),
            GetProjectPlanTool(manager=managers.project_manager),
            SavePlanningDeliverablesTool(manager=managers.project_manager),
            UpdatePlanningDeliverablesTool(manager=managers.project_manager),
            TransitionPhaseTool(
                workspace_root=Path(settings.server.workspace_root),
                project_manager=managers.project_manager,
                state_engine=managers.phase_state_engine,
                server_root=(
                    Path(settings.server.workspace_root) / settings.server.server_root_dir
                ),
                workphases_config=configs.workphases_config,
            ),
            ForcePhaseTransitionTool(
                workspace_root=Path(settings.server.workspace_root),
                project_manager=managers.project_manager,
                state_engine=managers.phase_state_engine,
                server_root=(
                    Path(settings.server.workspace_root) / settings.server.server_root_dir
                ),
                workphases_config=configs.workphases_config,
            ),
            TransitionCycleTool(
                workspace_root=Path(settings.server.workspace_root),
                project_manager=managers.project_manager,
                state_engine=managers.phase_state_engine,
                git_manager=managers.git_manager,
                gate_runner=managers.workflow_gate_runner,
                server_root=(
                    Path(settings.server.workspace_root) / settings.server.server_root_dir
                ),
            ),
            ForceCycleTransitionTool(
                workspace_root=Path(settings.server.workspace_root),
                project_manager=managers.project_manager,
                state_engine=managers.phase_state_engine,
                git_manager=managers.git_manager,
                gate_runner=managers.workflow_gate_runner,
                server_root=(
                    Path(settings.server.workspace_root) / settings.server.server_root_dir
                ),
            ),
            GetWorkContextTool(
                settings=settings,
                git_manager=managers.git_manager,
                project_manager=managers.project_manager,
                state_engine=managers.phase_state_engine,
                github_manager=managers.github_manager,
                workphases_config=configs.workphases_config,
                workflow_status_resolver=managers.workflow_status_resolver,
                contracts_config=configs.contracts_config,
                context_loaded_writer=managers.context_loaded_cache,
            ),
        ]

        issue_tools: list[ICoreTool[Any, Any]] = [
            CreateIssueTool(
                manager=managers.github_manager,
                issue_config=configs.issue_config,
                milestone_config=configs.milestone_config,
                contracts_config=configs.contracts_config,
                label_config=configs.label_config,
                scope_config=configs.scope_config,
                git_config=configs.git_config,
            ),
            ListIssuesTool(manager=managers.github_manager),
            GetIssueTool(manager=managers.github_manager),
            CloseIssueTool(manager=managers.github_manager),
            UpdateIssueTool(manager=managers.github_manager),
        ]

        credential_tools: list[ICoreTool[Any, Any]] = [
            ListPRsTool(
                manager=managers.github_manager,
                git_config=configs.git_config,
            ),
            GetPRTool(manager=managers.github_manager),
            MergePRTool(
                manager=managers.github_manager,
                git_config=configs.git_config,
                pr_status_writer=managers.pr_status_cache,
            ),
            SubmitPRTool(
                git_manager=managers.git_manager,
                github_manager=managers.github_manager,
                pr_status_writer=managers.pr_status_cache,
                merge_readiness_context=merge_readiness_context,
                branch_parent_reader=BranchStateParentReader(
                    state_reader=managers.state_repository,
                    git_config=configs.git_config,
                ),
            ),
            AddLabelsTool(
                manager=managers.github_manager,
                label_config=configs.label_config,
                workphases_config=configs.workphases_config,
            ),
            ListLabelsTool(
                manager=managers.github_manager,
                label_config=configs.label_config,
            ),
            CreateLabelTool(
                manager=managers.github_manager,
                label_config=configs.label_config,
                workphases_config=configs.workphases_config,
            ),
            DeleteLabelTool(
                manager=managers.github_manager,
                label_config=configs.label_config,
            ),
            RemoveLabelsTool(
                manager=managers.github_manager,
                label_config=configs.label_config,
            ),
            ListMilestonesTool(manager=managers.github_manager),
            CreateMilestoneTool(manager=managers.github_manager),
            CloseMilestoneTool(manager=managers.github_manager),
        ]

        all_base = (*unchanged_base_tools, *target_v3_tools)
        supported_tools = (*all_base, *issue_tools, *credential_tools)
        active_tools = supported_tools if settings.github.token else (*all_base, *issue_tools)
        return ToolAssembly.create(
            supported_tools=supported_tools,
            active_tools=active_tools,
        )

    def _build_resources(
        self,
        configs: ConfigLayer,  # noqa: ARG002
        managers: ManagerGraph,
        *,
        standards: StandardsResource | None = None,
    ) -> list[BaseResource]:
        """Compose the list of available resources."""
        resources: list[BaseResource] = []
        if standards is not None:
            resources.append(standards)
        resources.append(StatusResource())
        resources.append(CachedResponseResource(cache=managers.response_cache))
        resources.append(CacheReadGuideResource())

        if self._settings.github.token:
            resources.append(GitHubIssuesResource())

        return resources
