"""Shared test fixtures and configuration."""

from __future__ import annotations

import pytest


@pytest.fixture
def sample_html() -> str:
    """Sample HTML for testing conversion."""
    return """<!DOCTYPE html>
<html>
<head><title>Test Page</title></head>
<body>
<h1>Main Heading</h1>
<p>This is a paragraph.</p>
<ul>
<li>Item one</li>
<li>Item two</li>
</ul>
</body>
</html>"""


@pytest.fixture
def sample_html_with_code() -> str:
    """Sample HTML with code blocks for testing."""
    return """<!DOCTYPE html>
<html>
<body>
<h2>Code Example</h2>
<pre><code class="language-python">def hello():
    print("world")</code></pre>
<blockquote>
<p>Important note:</p>
<pre><code>some code</code></pre>
</blockquote>
</body>
</html>"""


@pytest.fixture
def sample_html_with_table() -> str:
    """Sample HTML with a table."""
    return """<!DOCTYPE html>
<html>
<body>
<table>
<thead>
<tr><th>Name</th><th>Value</th></tr>
</thead>
<tbody>
<tr><td>Foo</td><td>1</td></tr>
<tr><td>Bar</td><td>2</td></tr>
</tbody>
</table>
</body>
</html>"""


@pytest.fixture
def sample_html_with_details() -> str:
    """Sample HTML with details/summary."""
    return """<!DOCTYPE html>
<html>
<body>
<details>
<summary>Click me</summary>
<p>This is hidden content.</p>
</details>
</body>
</html>"""


@pytest.fixture
def sample_html_with_links() -> str:
    """Sample HTML with links."""
    return """<!DOCTYPE html>
<html>
<body>
<a href="https://example.com">Example Link</a>
<a href="/relative">Relative Link</a>
</body>
</html>"""


@pytest.fixture
def sample_html_with_abbr() -> str:
    """Sample HTML with abbreviations."""
    return """<!DOCTYPE html>
<html>
<body>
<p>The <abbr title="HyperText Markup Language">HTML</abbr> specification.</p>
</body>
</html>"""


@pytest.fixture
def sample_html_with_blockquote() -> str:
    """Sample HTML with blockquote."""
    return """<!DOCTYPE html>
<html>
<body>
<blockquote>
<p>This is a blockquote.</p>
</blockquote>
</body>
</html>"""


@pytest.fixture
def sample_html_with_hr() -> str:
    """Sample HTML with horizontal rule."""
    return """<!DOCTYPE html>
<html>
<body>
<p>Before</p>
<hr>
<p>After</p>
</body>
</html>"""


@pytest.fixture
def sample_html_with_bold_italic() -> str:
    """Sample HTML with bold and italic."""
    return """<!DOCTYPE html>
<html>
<body>
<p><strong>Bold text</strong> and <em>italic text</em>.</p>
</body>
</html>"""


@pytest.fixture
def sample_html_with_inline_code() -> str:
    """Sample HTML with inline code."""
    return """<!DOCTYPE html>
<html>
<body>
<p>Use the <code>print()</code> function.</p>
</body>
</html>"""


@pytest.fixture
def sample_html_with_nested_lists() -> str:
    """Sample HTML with nested lists."""
    return """<!DOCTYPE html>
<html>
<body>
<ul>
<li>Parent 1
<ul>
<li>Child 1.1</li>
<li>Child 1.2</li>
</ul>
</li>
<li>Parent 2</li>
</ul>
</body>
</html>"""


@pytest.fixture
def httpbin_url() -> str:
    """Base URL for httpbin.org integration tests."""
    return "https://httpbin.org"
