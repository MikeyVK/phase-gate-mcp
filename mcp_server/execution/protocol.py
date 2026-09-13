"""Generic adapter JSON transport and bounded stream capture."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Generic, TypeVar

from pydantic import BaseModel

from mcp_server.execution.models import (
    AdapterExitCode,
    InvocationCompleted,
    ProcessCapture,
    StreamCapture,
)

STDOUT_LIMIT = 8 * 1024 * 1024
STDERR_LIMIT = 256 * 1024
READ_CHUNK_SIZE = 64 * 1024


class InvalidAdapterResponseError(ValueError):
    """The adapter response is valid JSON but mismatches its exit contract."""


@dataclass
class StdoutBuffer:
    """Retain bounded stdout bytes while counting all observed bytes."""

    _retained: bytearray = field(default_factory=bytearray)
    _observed_bytes: int = 0
    _oversized: bool = False

    def feed(self, chunk: bytes) -> None:
        """Consume one raw byte chunk without line-oriented parsing."""
        self._observed_bytes += len(chunk)
        remaining = STDOUT_LIMIT - len(self._retained)
        if remaining > 0:
            self._retained.extend(chunk[:remaining])
        if self._observed_bytes > STDOUT_LIMIT:
            self._oversized = True

    @property
    def oversized(self) -> bool:
        """Whether observed stdout exceeded the formal response limit."""
        return self._oversized

    @property
    def data(self) -> bytes:
        """Return the retained stdout prefix."""
        return bytes(self._retained)

    def capture(self, *, accepted: bool = False) -> StreamCapture:
        """Create capture facts, omitting accepted formal stdout bytes."""
        if accepted:
            head: str | None = None
            tail: str | None = None
            truncated = False
        else:
            head = self.data.decode("utf-8", errors="replace")
            tail = ""
            truncated = self.oversized
        return StreamCapture(
            observed_bytes=self._observed_bytes,
            head=head,
            tail=tail,
            truncated=truncated,
        )


@dataclass
class StderrBuffer:
    """Retain bounded stderr head/tail bytes while counting all output."""

    _head: bytearray = field(default_factory=bytearray, init=False)
    _tail: bytearray = field(default_factory=bytearray, init=False)
    _observed_bytes: int = field(default=0, init=False)

    def feed(self, chunk: bytes) -> None:
        """Consume one raw byte chunk without line-oriented parsing."""
        self._observed_bytes += len(chunk)
        half = STDERR_LIMIT // 2
        head_room = half - len(self._head)
        if head_room > 0:
            self._head.extend(chunk[:head_room])
            chunk = chunk[head_room:]
        if chunk:
            self._tail.extend(chunk)
            if len(self._tail) > half:
                del self._tail[:-half]

    def capture(self) -> StreamCapture:
        """Create bounded, replacement-decoded stderr capture facts."""
        truncated = self._observed_bytes > STDERR_LIMIT
        if not truncated:
            # Before the limit, _tail contains the bytes after the head split.
            data = bytes(self._head) + bytes(self._tail)
            return StreamCapture(
                observed_bytes=self._observed_bytes,
                head=data.decode("utf-8", errors="replace"),
                tail="",
                truncated=False,
            )
        return StreamCapture(
            observed_bytes=self._observed_bytes,
            head=bytes(self._head).decode("utf-8", errors="replace"),
            tail=bytes(self._tail).decode("utf-8", errors="replace"),
            truncated=True,
        )


TResponse = TypeVar("TResponse", bound=BaseModel)


@dataclass(frozen=True)
class AdapterResponseContract(Generic[TResponse]):
    """Injected role response model and exit-code expectation."""

    response_type: type[TResponse]
    completed_type: type[InvocationCompleted[TResponse]]
    expected_exit: Callable[[TResponse], AdapterExitCode]

    def decode(
        self,
        raw: bytes,
        exit_code: int,
        capture: ProcessCapture,
    ) -> InvocationCompleted[TResponse]:
        """Decode one strict role response and enforce its exit mapping."""
        response = self.response_type.model_validate_json(raw, strict=True)
        expected = self.expected_exit(response)
        if exit_code != int(expected):
            raise InvalidAdapterResponseError(
                f"exit_code_mismatch: observed={exit_code}, expected={int(expected)}"
            )
        return self.completed_type(
            outcome="completed",
            response=response,
            capture=capture,
        )
