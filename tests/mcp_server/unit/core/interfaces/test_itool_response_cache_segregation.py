# c:\temp\pgmcp\tests\mcp_server\unit\core\interfaces\test_itool_response_cache_segregation.py
# template=unit_test version=3d15d309 created=2026-06-19T22:20Z updated=
"""Verify CQRS cache segregation interfaces.

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.core.interfaces]
"""

# Third-party
from pydantic import BaseModel

# Project modules
from mcp_server.core.interfaces import IToolResponsePublisher, IToolResponseReader
from mcp_server.schemas.cache_publication import CachePublication


class DummyModel(BaseModel):
    value: int


class DummyPublisher:
    def put(self, tool_name: str, output: BaseModel) -> CachePublication:
        return CachePublication(run_id="run-123", success=True)


class DummyReader:
    def get(self, run_id: str, response_model: type[BaseModel]) -> BaseModel | None:
        return DummyModel(value=42)

    def exists(self, run_id: str) -> bool:
        return True


class TestIToolResponseCacheSegregation:
    """Test suite for CQRS cache segregation protocols."""

    def test_publisher_protocol(self) -> None:
        """Verify that IToolResponsePublisher is runtime-checkable and matches implementation."""
        publisher = DummyPublisher()
        assert isinstance(publisher, IToolResponsePublisher)

    def test_reader_protocol(self) -> None:
        """Verify that IToolResponseReader is runtime-checkable and matches implementation."""
        reader = DummyReader()
        assert isinstance(reader, IToolResponseReader)
