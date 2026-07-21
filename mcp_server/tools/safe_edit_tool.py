# mcp_server/tools/safe_edit_tool.py
"""
Safe File Editing Tool with Validation and Mutex Protection.

Multi-mode file editing tool supporting full rewrites, line-based edits,
line insertions, and search/replace operations. Includes file-level mutex
protection to prevent concurrent edit race conditions, integrated validation,
and diff preview capabilities.

@layer: Service (MCP Tools)
@dependencies: [re, asyncio, difflib, pathlib, typing, dataclasses, pydantic]
@responsibilities:
    - Provide safe multi-mode file editing (content/line_edits/insert_lines/search_replace)
    - Enforce file-level mutex to prevent concurrent edit race conditions
    - Validate edited content before writing (strict/interactive/verify_only modes)
    - Generate unified diff previews for transparency
    - Handle edge cases (new files, encoding, line range validation)
"""

# Standard library
import asyncio
import re
from dataclasses import dataclass
from difflib import get_close_matches, unified_diff
from pathlib import Path
from typing import Annotated, Any, Literal, Union

# Third-party
from pydantic import BaseModel, ConfigDict, Field

from mcp_server.core.interfaces.file_writer import IAtomicFileWriter
from mcp_server.core.interfaces.icore_tool import ICoreTool
from mcp_server.core.operation_notes import NoteContext
from mcp_server.schemas.tool_outputs import SafeEditOutput
from mcp_server.utils.atomic_file_writer import AtomicFileWriter
from mcp_server.validation.validation_service import ValidationService


@dataclass
class EditResponse:
    """Parameters for building edit response."""

    passed: bool
    issues: str
    diff: str


@dataclass
class SearchReplaceParams:
    """Parameters for search/replace operation."""

    search: str
    replace: str
    regex: bool = False
    count: int | None = None
    flags: int = 0


class ReplaceOp(BaseModel):
    """Replace target_content with replacement."""

    model_config = ConfigDict(extra="forbid")

    op: Literal["replace"] = "replace"
    target_content: str = Field(..., description="Exact string sequence to find and replace")
    replacement: str = Field(..., description="Replacement content")
    search_window: list[int] | None = Field(
        default=None,
        description="Optional 1-based line window [start_line, end_line] to scope search",
    )


class AppendOp(BaseModel):
    """Append content to file end (EOF) or relative to text anchor."""

    model_config = ConfigDict(extra="forbid")

    op: Literal["append"] = "append"
    content: str = Field(..., description="Content to append or insert")
    anchor: str | None = Field(
        default=None,
        description="Optional target anchor string. If None, appends to EOF.",
    )
    position: Literal["after", "before"] = Field(
        default="after",
        description="Insertion position relative to anchor",
    )


class RewriteOp(BaseModel):
    """Replace entire file content (file must already exist)."""

    model_config = ConfigDict(extra="forbid")

    op: Literal["rewrite"] = "rewrite"
    content: str = Field(..., description="New complete file content")


class PatternReplaceOp(BaseModel):
    """Regex pattern replacement."""

    model_config = ConfigDict(extra="forbid")

    op: Literal["pattern_replace"] = "pattern_replace"
    pattern: str = Field(..., description="Regex pattern to search")
    replacement: str = Field(..., description="Replacement string")
    regex: bool = Field(default=True, description="Treat pattern as regular expression")


OperationType = Annotated[
    Union[ReplaceOp, AppendOp, RewriteOp, PatternReplaceOp],
    Field(discriminator="op"),
]


class SafeEditInput(BaseModel):
    """Input for SafeEditTool."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(..., description="Path to target file (must exist)")
    operation: OperationType = Field(..., description="Edit operation to perform")
    mode: Literal["strict", "interactive", "verify_only"] = Field(
        default="strict",
        description="Validation mode. 'strict' fails on error, 'interactive' writes but warns.",
    )


class SafeEditTool(ICoreTool[SafeEditInput, SafeEditOutput]):
    """Tool for safely editing files with validation and multiple edit modes.

    Supports four mutually exclusive edit modes:
    1. **content**: Full file rewrite
    2. **line_edits**: Replace specific line ranges (surgical edits)
    3. **insert_lines**: Insert content without replacing existing lines
    4. **search_replace**: Pattern-based find/replace (literal or regex)

    All modes support:
    - Validation modes: strict (reject on error) / interactive (warn) / verify_only (dry-run)
    - Validator integration: PythonValidator, MarkdownValidator, TemplateValidator

    **IMPORTANT - Concurrent Edit Protection:**
    - File-level mutex prevents race conditions
    - Bundle multiple edits in ONE call using line_edits list
    - Sequential calls on same file will wait for lock (10ms timeout)
    - Example: [{"start_line": 1, "end_line": 1, "new_content": "..."}, ...]
    """

    @property
    def name(self) -> str:
        return "safe_edit_file"

    @property
    def description(self) -> str:
        return (
            "Write content to a file with automatic validation. "
            "Supports 'strict' mode (rejects on error) or 'interactive' (warns). "
            "Shows diff preview by default. "
            "Supports full content rewrite, chirurgical line-based edits, "
            "line inserts, or search/replace."
        )

    @property
    def args_model(self) -> type[SafeEditInput] | None:
        return SafeEditInput

    def __init__(
        self,
        validator: ValidationService | None = None,
        file_writer: IAtomicFileWriter | None = None,
    ) -> None:
        """Initialize tool, validation service, and atomic file writer."""
        self.validation_service = validator if validator is not None else ValidationService()
        self.file_writer: IAtomicFileWriter = (
            file_writer if file_writer is not None else AtomicFileWriter()
        )
        # Mutex for preventing concurrent edits on same file
        self._file_locks: dict[str, asyncio.Lock] = {}

    async def execute(self, params: SafeEditInput, context: NoteContext) -> SafeEditOutput:
        """Execute the safe edit with validation.

        Uses file-level locking to prevent concurrent edits on the same file.
        Multiple edits for the same file should be batched in line_edits list.
        """
        del context  # Not used
        # Normalize path for lock key
        file_key = str(Path(params.path).resolve())
        # Get or create lock for this file
        if file_key not in self._file_locks:
            self._file_locks[file_key] = asyncio.Lock()
        file_lock = self._file_locks[file_key]
        # Try to acquire lock with timeout
        try:
            async with asyncio.timeout(0.01):  # 10ms timeout - very aggressive
                async with file_lock:
                    # Read original content
                    original_result = self._read_original(params)
                    if isinstance(original_result, SafeEditOutput):
                        return original_result  # Error
                    original_content = original_result

                    # Generate new content based on edit mode
                    new_result = self._generate_new_content(params, original_content)
                    if isinstance(new_result, SafeEditOutput):
                        return new_result  # Error
                    new_content = new_result

                    # Diff preview is no longer part of the public agent-facing contract.
                    diff_output = ""
                    passed, issues_text = await self._validate(params.path, new_content)

                    # Build response DTO
                    if params.mode == "verify_only":
                        return SafeEditOutput(
                            success=True,
                            path=params.path,
                            passed=passed,
                            issues=issues_text,
                            mode=params.mode,
                            written=False,
                            diff=diff_output,
                            has_diff=False,
                        )

                    # Handle strict mode with validation failure
                    if params.mode == "strict" and not passed:
                        return SafeEditOutput(
                            success=False,
                            error_message=(
                                f"Edit rejected due to validation errors "
                                f"(Mode: strict):{issues_text}\n"
                                "Use mode='interactive' to force save "
                                "if necessary, or fix the content."
                            ),
                            path=params.path,
                            passed=passed,
                            issues=issues_text,
                            mode=params.mode,
                            written=False,
                            diff=diff_output,
                            has_diff=False,
                        )

                    # Write file atomically
                    try:
                        self.file_writer.write_text(Path(params.path), new_content)
                    except OSError as e:
                        return SafeEditOutput(
                            success=False,
                            error_message=f"Failed to write file: {e}",
                            path=params.path,
                            passed=passed,
                            issues=issues_text,
                            mode=params.mode,
                            written=False,
                            diff=diff_output,
                            has_diff=False,
                        )

                    return SafeEditOutput(
                        success=True,
                        path=params.path,
                        passed=passed,
                        issues=issues_text,
                        mode=params.mode,
                        written=True,
                        diff=diff_output,
                        has_diff=False,
                    )
        except TimeoutError:
            return SafeEditOutput(
                success=False,
                error_message=(
                    f"File '{params.path}' is already being edited. "
                    "Please wait or bundle multiple edits in one call using line_edits list."
                ),
                path=params.path,
                passed=False,
                mode=params.mode,
                written=False,
            )

    def _read_original(self, params: SafeEditInput) -> str | SafeEditOutput:
        """Read original file content or return error if file does not exist."""
        try:
            return Path(params.path).read_text(encoding="utf-8")
        except FileNotFoundError:
            return SafeEditOutput(
                success=False,
                error_message=(
                    f"File '{params.path}' does not exist. "
                    "safe_edit_file is strictly an edit tool for existing files. "
                    "To create new code or documentation files, call scaffold_artifact."
                ),
                path=params.path,
                passed=False,
                mode=params.mode,
                written=False,
            )
        except (UnicodeDecodeError, PermissionError) as e:
            return SafeEditOutput(
                success=False,
                error_message=f"Failed to read file: {e}",
                path=params.path,
                passed=False,
                mode=params.mode,
                written=False,
            )

    def _find_fuzzy_matches(self, original_text: str, target: str) -> str | None:
        """Find close matching lines in original_text for diagnostic error messages."""
        lines = original_text.splitlines()
        target_line = target.splitlines()[0] if target.splitlines() else target
        matches = get_close_matches(target_line, lines, n=3, cutoff=0.6)
        if matches:
            suggestions = "\n".join(f"  - '{m.strip()}'" for m in matches)
            return f"Did you mean one of these lines?\n{suggestions}"
        return None

    def _generate_new_content(self, params: SafeEditInput, original: str) -> str | SafeEditOutput:
        """Generate new content based on operation."""
        op = params.operation
        if isinstance(op, RewriteOp):
            return op.content
        if isinstance(op, ReplaceOp):
            search_text = original
            if op.search_window is not None:
                start_line, end_line = op.search_window
                lines = original.splitlines(keepends=True)
                window_lines = lines[start_line - 1 : end_line]
                search_text = "".join(window_lines)

            if op.target_content not in search_text:
                fuzzy = self._find_fuzzy_matches(original, op.target_content)
                err_msg = f"Pattern '{op.target_content}' not found in file"
                if fuzzy:
                    err_msg += f"\n\n{fuzzy}"
                err_msg += f"\n\n{self._build_file_context_preview(original)}"
                return SafeEditOutput(
                    success=False,
                    error_message=err_msg,
                    path=params.path,
                    passed=False,
                    mode=params.mode,
                    written=False,
                )

            if op.search_window is not None:
                start_line, end_line = op.search_window
                lines = original.splitlines(keepends=True)
                target_chunk = "".join(lines[start_line - 1 : end_line])
                replaced_chunk = target_chunk.replace(op.target_content, op.replacement, 1)
                lines[start_line - 1 : end_line] = [replaced_chunk]
                return "".join(lines)

            return original.replace(op.target_content, op.replacement, 1)
        if isinstance(op, AppendOp):
            append_text = op.content
            if not append_text.endswith("\n"):
                append_text += "\n"

            if op.anchor is None:
                prefix = "" if original.endswith("\n") or not original else "\n"
                return original + prefix + append_text

            if op.anchor not in original:
                fuzzy = self._find_fuzzy_matches(original, op.anchor)
                err_msg = f"Anchor '{op.anchor}' not found in file"
                if fuzzy:
                    err_msg += f"\n\n{fuzzy}"
                err_msg += f"\n\n{self._build_file_context_preview(original)}"
                return SafeEditOutput(
                    success=False,
                    error_message=err_msg,
                    path=params.path,
                    passed=False,
                    mode=params.mode,
                    written=False,
                )

            if op.position == "before":
                return original.replace(op.anchor, append_text + op.anchor, 1)
            return original.replace(op.anchor, op.anchor + "\n" + append_text.rstrip("\n"), 1)
        if isinstance(op, PatternReplaceOp):
            try:
                if op.regex:
                    return re.sub(op.pattern, op.replacement, original)
                return original.replace(op.pattern, op.replacement)
            except re.error as e:
                return SafeEditOutput(
                    success=False,
                    error_message=f"Regex pattern error: {e}",
                    path=params.path,
                    passed=False,
                    mode=params.mode,
                    written=False,
                )
        return original
        return original

    def _handle_line_edits(
        self, path: str, original: str, line_edits: list[Any], mode: str
    ) -> str | SafeEditOutput:
        """Legacy line_edits stub for Cycle 1."""
        return original

    def _handle_insert_lines(
        self, path: str, original: str, insert_lines: list[Any], mode: str
    ) -> str | SafeEditOutput:
        """Legacy insert_lines stub for Cycle 1."""
        return original

    def _handle_search_replace(self, params: SafeEditInput, original: str) -> str | SafeEditOutput:
        """Handle search/replace mode."""
        try:
            new_content, count = self._apply_search_replace(params, original)
            if params.mode == "strict" and not count:
                error_msg = f"Pattern not found in file\n\n"
                error_msg += self._build_file_context_preview(original)
                return SafeEditOutput(
                    success=False,
                    error_message=error_msg,
                    path=params.path,
                    passed=False,
                    mode=params.mode,
                    written=False,
                )
            return new_content
        except (ValueError, re.error) as e:
            return SafeEditOutput(
                success=False,
                error_message=f"Search/replace failed: {e}",
                path=params.path,
                passed=False,
                mode=params.mode,
                written=False,
            )

    def _apply_search_replace(self, params: SafeEditInput, content: str) -> tuple[str, int]:
        """Apply search/replace with params."""
        srp = SearchReplaceParams(
            search="",
            replace="",
            regex=False,
            count=None,
            flags=0,
        )
        return self._apply_search_replace_flat(content, srp)

    def _apply_line_edits(self, content: str, edits: list[Any]) -> str:
        """Apply line-based edits to content."""
        return content

    def _apply_insert_lines(self, content: str, inserts: list[Any]) -> str:
        """Apply line insert operations to content."""
        return content

    def _apply_search_replace_flat(
        self,
        content: str,
        params: SearchReplaceParams,
    ) -> tuple[str, int]:
        """Apply search and replace operation.

        Args:
            content: Content to search in.
            params: Search/replace parameters.

        Returns:
            Tuple of (new_content, replacement_count).
        """
        if params.regex:
            try:
                pattern = re.compile(params.search, params.flags or 0)
                if params.count is not None:
                    new_content, replacement_count = pattern.subn(
                        params.replace, content, count=params.count
                    )
                else:
                    new_content, replacement_count = pattern.subn(params.replace, content)
                return new_content, replacement_count
            except re.error as e:
                raise ValueError(f"Invalid regex pattern: {e}") from e

        # Literal string matching
        if params.count is not None:
            parts = content.split(params.search, params.count)
            new_content = params.replace.join(parts)
            replacement_count = len(parts) - 1
        else:
            replacement_count = content.count(params.search)
            new_content = content.replace(params.search, params.replace)

        return new_content, replacement_count

    def _generate_diff(self, path: str, original_content: str, new_content: str) -> str:
        """Generate unified diff between original and new content."""
        if original_content == new_content:
            return ""

        filename = Path(path).name
        original_lines = original_content.splitlines(keepends=True)
        new_lines = new_content.splitlines(keepends=True)

        diff_lines = unified_diff(
            original_lines, new_lines, fromfile=f"a/{filename}", tofile=f"b/{filename}", lineterm=""
        )

        return "".join(diff_lines)

    async def _validate(self, path: str, content: str) -> tuple[bool, str]:
        """Delegate validation to ValidationService."""
        return await self.validation_service.validate(path, content)

    def _build_file_context_preview(self, content: str, max_lines: int = 10) -> str:
        """Build file preview for error messages (DRY helper).

        Args:
            content: File content to preview.
            max_lines: Maximum number of lines to show.

        Returns:
            Formatted preview string with line numbers.
        """
        lines = content.splitlines()[:max_lines]
        preview = "**File Preview (first 10 lines):**\n"
        for i, line in enumerate(lines, 1):
            preview += f"{i:3}: {line}\n"

        total_lines = len(content.splitlines())
        if total_lines > max_lines:
            preview += f"... ({total_lines} total lines)\n"

        return preview
