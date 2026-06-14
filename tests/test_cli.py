"""Tests for CLI."""

from __future__ import annotations

import pytest


class TestCLI:
    """Tests for the CLI."""

    def test_cli_main_exists(self) -> None:
        """CLI has a main function."""
        raise NotImplementedError

    def test_cli_url_argument(self) -> None:
        """CLI accepts a URL argument."""
        raise NotImplementedError

    def test_cli_timeout_flag(self) -> None:
        """CLI --timeout flag works."""
        raise NotImplementedError

    def test_cli_retries_flag(self) -> None:
        """CLI --retries flag works."""
        raise NotImplementedError

    def test_cli_user_agent_flag(self) -> None:
        """CLI --user-agent flag works."""
        raise NotImplementedError

    def test_cli_output_flag(self) -> None:
        """CLI --output flag writes to file."""
        raise NotImplementedError

    def test_cli_mcp_subcommand(self) -> None:
        """CLI 'mcp' subcommand starts the MCP server."""
        raise NotImplementedError
