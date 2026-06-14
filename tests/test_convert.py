"""Tests for HTML to Markdown conversion."""

from __future__ import annotations

import pytest


class TestConvertHeadings:
    """Tests for heading conversion."""

    def test_h1(self) -> None:
        """H1 converts to # heading."""
        raise NotImplementedError

    def test_h2(self) -> None:
        """H2 converts to ## heading."""
        raise NotImplementedError

    def test_h3(self) -> None:
        """H3 converts to ### heading."""
        raise NotImplementedError

    def test_h6(self) -> None:
        """H6 converts to ###### heading."""
        raise NotImplementedError

    def test_nested_headings(self) -> None:
        """Multiple headings convert correctly."""
        raise NotImplementedError


class TestConvertParagraphs:
    """Tests for paragraph conversion."""

    def test_simple_paragraph(self) -> None:
        """Simple paragraph converts."""
        raise NotImplementedError

    def test_multiple_paragraphs(self) -> None:
        """Multiple paragraphs have blank lines between."""
        raise NotImplementedError


class TestConvertBoldItalic:
    """Tests for bold and italic conversion."""

    def test_strong(self) -> None:
        """Strong converts to bold."""
        raise NotImplementedError

    def test_em(self) -> None:
        """Em converts to italic."""
        raise NotImplementedError

    def test_nested_bold_italic(self) -> None:
        """Nested bold/italic converts."""
        raise NotImplementedError


class TestConvertLinks:
    """Tests for link conversion."""

    def test_simple_link(self) -> None:
        """Simple link converts to markdown link."""
        raise NotImplementedError

    def test_relative_url_resolved(self) -> None:
        """Relative URLs are resolved to absolute."""
        raise NotImplementedError


class TestConvertLists:
    """Tests for list conversion."""

    def test_unordered_list(self) -> None:
        """Unordered list converts."""
        raise NotImplementedError

    def test_ordered_list(self) -> None:
        """Ordered list converts."""
        raise NotImplementedError

    def test_nested_lists(self) -> None:
        """Nested lists convert with proper indentation."""
        raise NotImplementedError


class TestConvertCode:
    """Tests for code block conversion."""

    def test_inline_code(self) -> None:
        """Inline code converts with single backticks."""
        raise NotImplementedError

    def test_fenced_code_block(self) -> None:
        """Fenced code block converts with triple backticks."""
        raise NotImplementedError

    def test_fenced_code_with_language(self) -> None:
        """Fenced code block with language attribute."""
        raise NotImplementedError

    def test_pre_code_without_language(self) -> None:
        """Pre/code without language attribute."""
        raise NotImplementedError


class TestConvertBlockquote:
    """Tests for blockquote conversion."""

    def test_simple_blockquote(self) -> None:
        """Simple blockquote converts."""
        raise NotImplementedError

    def test_blockquote_with_code(self) -> None:
        """Blockquote containing code converts."""
        raise NotImplementedError


class TestConvertTable:
    """Tests for table conversion."""

    def test_simple_table(self) -> None:
        """Simple table converts to pipe syntax."""
        raise NotImplementedError

    def test_table_with_colspan_fallback(self) -> None:
        """Tables with colspans fall back to bullet list."""
        raise NotImplementedError


class TestConvertDetails:
    """Tests for details/summary conversion."""

    def test_details_always_expanded(self) -> None:
        """Details content is always shown (not collapsed)."""
        raise NotImplementedError


class TestConvertHR:
    """Tests for horizontal rule conversion."""

    def test_hr(self) -> None:
        """HR converts to ---."""
        raise NotImplementedError


class TestConvertStripping:
    """Tests for style/script stripping."""

    def test_style_stripped(self) -> None:
        """Style content is stripped from output."""
        raise NotImplementedError

    def test_script_stripped(self) -> None:
        """Script content is stripped from output."""
        raise NotImplementedError

    def test_comments_stripped(self) -> None:
        """HTML comments are stripped."""
        raise NotImplementedError


class TestConvertAbbr:
    """Tests for abbreviation conversion."""

    def test_abbr_inline_parentheses(self) -> None:
        """Abbreviations render as Term (full form)."""
        raise NotImplementedError
