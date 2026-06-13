"""Quality tools."""

import uuid
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from mcp_server.core.interfaces import IToolResponseCache
from mcp_server.core.operation_notes import NoteContext, RecoveryNote
from mcp_server.managers.qa_manager import QAManager
from mcp_server.managers.quality_state_repository import QualityStateMutationConflictError
from mcp_server.schemas.tool_outputs import AutoFixOutput
from mcp_server.tools.base import BaseTool, StructuredTool
from mcp_server.tools.tool_result import ToolResult


class RunQualityGatesInput(BaseModel):
    """Input for RunQualityGatesTool."""

    model_config = ConfigDict(extra="forbid")

    scope: Literal["auto", "branch", "project", "files"] = Field(
        default="auto",
        description=(
            "Scope of the quality gate run. "
            "'auto' = union of changed files and previously failed files; "
            "'branch' = files changed on this branch vs parent; "
            "'project' = all files matching project_scope.include_globs; "
            "'files' = explicit list supplied via the 'files' field."
        ),
    )
    files: list[str] | None = Field(
        default=None,
        description=(
            "Explicit list of files to check. "
            "Required (and non-empty) when scope='files'. "
            "Must be omitted (or null) for all other scope values."
        ),
    )

    @model_validator(mode="after")
    def _validate_files_scope_contract(self) -> "RunQualityGatesInput":
        """Enforce the two-rule validator contract (design.md §4.6a).

        Rule 1 – files required:  scope='files' and files is None or []  → ValidationError
        Rule 2 – files forbidden: scope != 'files' and files is not None → ValidationError
        """
        if self.scope == "files":
            if not self.files:
                raise ValueError("files must be a non-empty list when scope='files'")
        else:
            if self.files is not None:
                raise ValueError(
                    f"files must be omitted when scope='{self.scope}' "
                    "(only allowed with scope='files')"
                )
        return self


class RunQualityGatesTool(BaseTool):
    """Tool to run quality gates."""

    name = "run_quality_gates"
    description = (
        "Run quality gates. "
        "scope='auto' (default): union of changed + previously failed files; "
        "scope='branch': files changed on this branch; "
        "scope='project': all project files; "
        "scope='files': explicit file list supplied via the 'files' field."
    )
    args_model = RunQualityGatesInput

    @staticmethod
    def _effective_scope(params: RunQualityGatesInput) -> str:
        """Return authoritative scope value for the current tool execution."""
        return params.scope

    def __init__(self, manager: QAManager) -> None:
        self.manager = manager

    @property
    def input_schema(self) -> dict[str, Any]:
        """Get input schema for the tool."""
        if self.args_model is None:
            return {}
        return self.args_model.model_json_schema()

    async def execute(self, params: RunQualityGatesInput, context: NoteContext) -> ToolResult:
        """Execute quality gates and return contract-compliant response.

        Returns exactly two content items (design.md §4.8, planning.md C27):
        1. ``{"type": "text", "text": <summary_line>}`` — one-line human-readable status
        2. ``{"type": "json", "json": <compact_payload>}`` — structured gate results

        Args:
            params: Tool input parameters.

        Returns:
            ToolResult with content[0]=text summary, content[1]=compact JSON payload.
        """
        effective_scope = self._effective_scope(params)
        resolved_files = self.manager._resolve_scope(effective_scope, files=params.files)  # pyright: ignore[reportPrivateUsage]

        try:
            result = self.manager.run_quality_gates(
                resolved_files,
                effective_scope=effective_scope,
            )
        except QualityStateMutationConflictError as e:
            context.produce(RecoveryNote(message=e.recovery))
            return ToolResult.error(e.diagnostic)
        except OSError as e:
            context.produce(
                RecoveryNote(
                    message=f"Quality state write failed — retry the quality gates run: {e}"
                )
            )
            return ToolResult.error(str(e))

        summary_line = QAManager._format_summary_line(  # pyright: ignore[reportPrivateUsage]
            result,
            scope=effective_scope,
            file_count=len(resolved_files),
        )
        compact_payload = self.manager._build_compact_result(result)  # pyright: ignore[reportPrivateUsage]
        return ToolResult.json_data(compact_payload, text=summary_line)


class AutoFixInput(BaseModel):
    """Input for AutoFixTool."""

    model_config = ConfigDict(extra="forbid")

    scope: Literal["auto", "branch", "project", "files"] = Field(
        default="auto",
        description=(
            "Scope of the auto fix run. "
            "'auto' = union of changed files and previously failed files; "
            "'branch' = files changed on this branch vs parent; "
            "'project' = all files matching project_scope.include_globs; "
            "'files' = explicit list supplied via the 'files' field."
        ),
    )
    files: list[str] | None = Field(
        default=None,
        description=(
            "Explicit list of files to check. "
            "Required (and non-empty) when scope='files'. "
            "Must be omitted (or null) for all other scope values."
        ),
    )

    @model_validator(mode="after")
    def _validate_files_scope_contract(self) -> "AutoFixInput":
        if self.scope == "files":
            if not self.files:
                raise ValueError("files must be a non-empty list when scope='files'")
        else:
            if self.files is not None:
                raise ValueError(
                    f"files must be omitted when scope='{self.scope}' "
                    "(only allowed with scope='files')"
                )
        return self


class AutoFixTool(StructuredTool):
    """Tool to run auto fixes."""

    name = "auto_fix"
    description = (
        "Execute configured fixer commands on matching files. "
        "scope='auto' (default): union of changed + failed files; "
        "scope='branch': files changed on this branch; "
        "scope='project': all project files; "
        "scope='files': explicit file list supplied via the 'files' field."
    )
    args_model = AutoFixInput
    output_model = AutoFixOutput
    presentation_category = "mutation"

    def __init__(self, qa_manager: QAManager, cache: IToolResponseCache) -> None:
        self.qa_manager = qa_manager
        self.cache = cache

    async def execute_structured(self, params: AutoFixInput, context: NoteContext) -> AutoFixOutput:
        """Execute the auto fixes and cache the result."""
        _ = context
        # 1. Run the auto fix logic via QAManager
        output = self.qa_manager.run_auto_fix(scope=params.scope, files=params.files)

        # 2. Generate run_id and copy output with the run_id
        run_id = uuid.uuid4().hex
        uri = f"pgmcp://cache/runs/{run_id}"

        # 3. Cache the original output (so cached_dto == expected_output matches)
        self.cache.put(uri, output)

        # 4. Return the output DTO containing run_id
        return output.model_copy(update={"run_id": run_id})
