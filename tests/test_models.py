"""Tests for the Result model."""

from __future__ import annotations

import pytest

from minifetch.models import Result


class TestResultSuccess:
    """Tests for successful Result construction."""

    def test_result_success_default(self) -> None:
        """Result can be constructed with just success and url."""
        result = Result(success=True, url="https://example.com")
        assert result.success is True
        assert result.url == "https://example.com"
        assert result.status_code is None
        assert result.fetch_time_ms is None
        assert result.redirect_chain == []
        assert result.markdown is None
        assert result.raw is None
        assert result.error is None

    def test_result_full_success(self) -> None:
        """Result can be constructed with all success fields."""
        result = Result(
            success=True,
            url="https://example.com",
            status_code=200,
            fetch_time_ms=150.5,
            redirect_chain=["https://example.com", "https://www.example.com"],
            markdown="# Hello",
        )
        assert result.success is True
        assert result.status_code == 200
        assert result.fetch_time_ms == 150.5
        assert result.redirect_chain == ["https://example.com", "https://www.example.com"]
        assert result.markdown == "# Hello"
        assert result.error is None


class TestResultFailure:
    """Tests for failed Result construction."""

    def test_result_failure(self) -> None:
        """Result represents failure correctly."""
        result = Result(success=False, url="https://bad.com", error="Connection refused")
        assert result.success is False
        assert result.url == "https://bad.com"
        assert result.error == "Connection refused"

    def test_result_failure_without_error(self) -> None:
        """Result can be failed without an error message."""
        result = Result(success=False, url="https://bad.com")
        assert result.success is False
        assert result.error is None
