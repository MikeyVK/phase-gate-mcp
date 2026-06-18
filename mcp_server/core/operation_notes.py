# mcp_server/core/operation_notes.py
"""
NoteEntry typed notes protocol and NoteContext.

Defines the generic Note dataclass and NoteContext — the per-call notes bus.

@layer: Core
@dependencies: [collections.abc, dataclasses, typing, mcp_server.tools.tool_result]
@responsibilities:
    - Define the generic Note dataclass for declarative presentation
    - Implement NoteContext: per-call notes bus with produce, of_type,
      render_to_response
"""

from __future__ import annotations

# Standard library
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, TypeVar

# Project modules
from mcp_server.tools.tool_result import ToolResult

T = TypeVar("T")


@dataclass(frozen=True)
class Note:
    """Generic presentation-driven metadata note.

    All layout, text formatting, and emojis are configured declaratively
    in presentation.yaml under the corresponding key.
    """

    key: str
    params: dict[str, Any] = field(default_factory=dict)


NoteEntry = Note


@dataclass
class NoteContext:
    """Bidirectional per-call notes bus.

    Lifetime: exactly one tool invocation. Constructed as a local variable
    in handle_call_tool. Never stored as server instance state.

    Producers call produce(). Consumers call of_type(). The server calls
    render_to_response() once, unconditionally, after execution completes.
    """

    presenter: Any | None = None
    tool_name: str | None = None
    _entries: list[NoteEntry] = field(default_factory=list, init=False)

    def produce(self, note: NoteEntry) -> None:
        """Write a note. Preserves insertion order."""
        self._entries.append(note)

    @property
    def entries(self) -> list[NoteEntry]:
        """Return all collected note entries."""
        return self._entries

    def of_type(self, t: type[T]) -> Sequence[T]:
        """Return all notes of the given type, in insertion order.

        Type-safe: pyright infers the return element type from the argument.
        Example: context.of_type(Note) -> Sequence[Note]
        """
        return [n for n in self._entries if isinstance(n, t)]

    def render_to_response(self, base: ToolResult) -> ToolResult:
        """Append all notes as an additional TextContent block using the presenter.

        Called once by the server after tool execution, on both success and
        error paths. Returns base unchanged when no presenter or entries exist.
        Insertion order is preserved.
        """
        if self.presenter is not None and self.tool_name is not None:
            notes_text = self.presenter.present_notes(self.tool_name, self._entries)
            if not notes_text:
                return base
            augmented = list(base.content) + [{"type": "text", "text": notes_text}]
            return base.model_copy(update={"content": augmented})

        return base
