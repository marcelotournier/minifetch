"""Data models for minifetch."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Result:
    """Result of a fetch operation.

    Attributes:
        success: Whether the operation succeeded.
        url: The URL that was fetched.
        status_code: HTTP status code, if available.
        fetch_time_ms: Time taken in milliseconds, if available.
        redirect_chain: List of URLs followed during redirects.
        markdown: Converted Markdown content, if successful.
        raw: Raw content (HTML/text), if available.
        error: Error message, if failed.
    """

    success: bool
    url: str
    status_code: int | None = None
    fetch_time_ms: float | None = None
    redirect_chain: list[str] = field(default_factory=list)
    markdown: str | None = None
    raw: str | None = None
    error: str | None = None
