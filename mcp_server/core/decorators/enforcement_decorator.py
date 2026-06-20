# c:\temp\pgmcp\mcp_server\core\decorators\enforcement_decorator.py
# template=generic version=f35abd82 created=2026-06-19T22:04Z updated=
"""EnforcementDecorator module.

Decorator that executes policy preflights and rules checks (both pre and post execution).

@layer: Backend (Decorators)
@dependencies: [icore_tool, enforcement_runner, pydantic]
@responsibilities:
    - Run pre-execution policy checks
    - Run post-execution policy checks
    - Return EnforcementErrorOutput DTO on enforcement failure
"""

# Standard library
from pathlib import Path
from typing import TypeVar

# Third-party
from pydantic import BaseModel

# Project modules
from mcp_server.core.exceptions import ValidationError
from mcp_server.core.interfaces.icore_tool import ICoreTool
from mcp_server.core.operation_notes import NoteContext
from mcp_server.managers.enforcement_runner import EnforcementContext, EnforcementRunner
from mcp_server.schemas.error_outputs import EnforcementErrorOutput, ToolErrorOutput

TInput = TypeVar("TInput", bound=BaseModel)
TOutput = TypeVar("TOutput", bound=BaseModel)


class EnforcementDecorator(ICoreTool[TInput, TOutput]):
    """Inner decorator that runs policies before/after execution and traps enforcement errors."""

    def __init__(
        self,
        inner_tool: ICoreTool[TInput, TOutput],
        enforcement_runner: EnforcementRunner,
        workspace_root: Path,
    ) -> None:
        self._inner_tool = inner_tool
        self._enforcement_runner = enforcement_runner
        self._workspace_root = workspace_root

    @property
    def name(self) -> str:
        return self._inner_tool.name

    @property
    def description(self) -> str:
        return self._inner_tool.description

    @property
    def args_model(self) -> type[BaseModel] | None:
        return self._inner_tool.args_model

    @property
    def tool_category(self) -> str | None:
        return getattr(self._inner_tool, "tool_category", None)

    async def execute(self, params: TInput, context: NoteContext) -> TOutput:
        # 1. Run "pre" execution policy checks
        try:
            self._enforcement_runner.run(
                event=self.name,
                timing="pre",
                tool_category=self.tool_category,
                enforcement_ctx=EnforcementContext(
                    workspace_root=self._workspace_root,
                    tool_name=self.name,
                    params=params,
                ),
                note_context=context,
            )
        except ValidationError as exc:
            return EnforcementErrorOutput(
                error_message=exc.message,
                error_code=exc.code,
                params=exc.params or {},
            )  # type: ignore[return-value]

        # 2. Execute target tool
        result = await self._inner_tool.execute(params, context)

        # Skip "post" checks if tool execution returned a validation or other error DTO
        if isinstance(result, ToolErrorOutput):
            return result

        # 3. Run "post" execution policy checks
        try:
            self._enforcement_runner.run(
                event=self.name,
                timing="post",
                tool_category=self.tool_category,
                enforcement_ctx=EnforcementContext(
                    workspace_root=self._workspace_root,
                    tool_name=self.name,
                    params=params,
                ),
                note_context=context,
            )
        except ValidationError as exc:
            return EnforcementErrorOutput(
                error_message=exc.message,
                error_code=exc.code,
                params=exc.params or {},
            )  # type: ignore[return-value]

        return result
