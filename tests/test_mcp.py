"""Tests for MCP server."""

from __future__ import annotations

import pytest


class TestMCPServer:
    """Tests for the MCP server."""

    def test_create_mcp_server(self) -> None:
        """MCP server can be created with a Minifetch instance."""
        raise NotImplementedError

    def test_mcp_tool_fetch_to_markdown(self) -> None:
        """MCP tool fetch_to_markdown works."""
        raise NotImplementedError

    def test_mcp_tool_fetch_raw(self) -> None:
        """MCP tool fetch_raw works."""
        raise NotImplementedError

    def test_mcp_response_format(self) -> None:
        """MCP tool responses have correct JSON format."""
        raise NotImplementedError

    def test_mcp_error_response(self) -> None:
        """MCP tool returns error on failure."""
        raise NotImplementedError


class TestMCPTransport:
    """Tests for MCP transport."""

    def test_streamable_http_endpoint(self) -> None:
        """MCP server exposes streamable HTTP endpoint."""
        raise NotImplementedError

    def test_mcp_server_starts(self) -> None:
        """MCP server starts and listens."""
        raise NotImplementedError
