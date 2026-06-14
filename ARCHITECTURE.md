# Minifetch — Architecture Decision Records (ADRs)

This document is the **source of truth** for all architectural decisions in the minifetch project. Refer to it whenever making changes to the project.

---

## ADR-01: Project Structure — Single Package with Entry Points

**Status:** Accepted  
**Date:** 2026-06-14

### Context

Minifetch delivers three things: a Python library (URL → Markdown), a CLI tool, and an MCP service. All three need to share code (the core fetching and conversion logic). The project must have zero external dependencies for the library itself.

### Decision

**Option C — Single package with entry points.** One `minifetch/` Python package. CLI and MCP are defined as `console_scripts` / `entry_points` in one `pyproject.toml`. Shared code easily accessible across all three delivery modes.

### Consequences

- One package, one dependency graph for users
- Easy to share code between CLI, MCP, and library
- Users install once: `pip install minifetch` (library + CLI), `pip install minifetch[mcp]` (adds uvicorn)

---

## ADR-02: HTML → Markdown Conversion — `html.parser.HTMLParser`

**Status:** Accepted  
**Date:** 2026-06-14

### Context

The library has **zero dependencies**. We must build HTML→Markdown conversion using only Python stdlib. Options range from fragile regex extraction to building a full DOM tree.

### Decision

**Option B — `html.parser.HTMLParser` (stdlib).** Use Python's built-in SAX-style parser to walk the DOM tree, rendering markdown as we traverse events. More robust than regex, no need to build a full DOM tree.

### Consequences

- Handles nested elements correctly
- Event-driven traversal without heavy memory overhead
- Standard library only — no extra dependencies
- Well-understood, testable

---

## ADR-03: HTML-to-Markdown Scope — Comprehensive (Except Images)

**Status:** Accepted  
**Date:** 2026-06-14

### Context

Real-world HTML contains many elements. We need to decide how comprehensive the converter should be. Blockquotes are explicitly required as they commonly contain code examples for agentic programming.

### Decision

**Comprehensive scope (Option C) minus images.**

Supported elements:
- Headings (`<h1>`–`<h6>`)
- Paragraphs (`<p>`)
- Links (`<a href>`)
- Bold/Italic (`<strong>`, `<em>`)
- Inline code (`<code>`)
- Fenced code blocks (`<pre><code>`)
- Lists (ordered, unordered, nested)
- **Blockquotes** (`<blockquote>`) — critical for code examples in agentic workflows
- Horizontal rules (`<hr>`)
- Pre/code blocks
- Tables (pipe syntax)
- Nested lists
- `<details>`/`<summary>` — always expanded (markdown can't represent collapsibility)
- `<abbr>` — rendered as `Term (full form)`
- Raw HTML fallback for unsupported tags
- **Images excluded** — not required for the use case

### Consequences

- Covers the vast majority of real-world HTML encountered in agentic programming
- Simpler than trying to support images (which would require URL resolution, alt text, etc.)
- Tables rendered as pipe syntax; complex tables with colspans/rowspans fall back to bullet-point lists
- `<details>` content always shown; no false promises of collapsibility
- `<abbr>` rendered inline as `Abbreviation (full form)`

---

## ADR-04: Fetching URLs — Configurable Fetcher with Retries

**Status:** Accepted  
**Date:** 2026-06-14

### Context

Real-world HTTP is flaky. A simple `urllib.request.urlopen()` call is insufficient for robust fetching. We need resilience without adding dependencies.

### Decision

**Option B — Configurable fetcher using `urllib.request`.** Features:
- Configurable timeout
- Retry logic with exponential backoff
- Max redirects control
- Configurable user-agent

### Consequences

- Handles transient failures gracefully
- User can tune timeout/retries to their needs
- Pure stdlib — no requests/httpx dependency
- Predictable behavior

---

## ADR-05: Library API Design — Class-Based

**Status:** Accepted  
**Date:** 2026-06-14

### Context

The library needs a clean API. The CLI, MCP, and tests all need to instantiate and use the fetcher/converter. A class-based approach provides the most reusable pattern.

### Decision

**Option C — Class-based API.** `Minifetch` class with configurable parameters (timeout, retries, user-agent, etc.). The CLI instantiates it with CLI defaults, the MCP instantiates it with MCP defaults, tests inject mock configs.

### Consequences

- Single source of truth for fetch+convert logic
- Easy to configure per-instance
- Testable with dependency injection
- Clean separation between config and execution

---

## ADR-06: Browser Spoofing / Fingerprint Evasion — Full Header Sets

**Status:** Accepted  
**Date:** 2026-06-14

### Context

Many sites block requests with default Python user-agents or detect non-browser fingerprints. We need to mimic real browsers without external dependencies.

### Decision

**Option B — Full header spoofing with multiple stored header sets.** Store complete, realistic browser header blocks for different browsers/OS combinations (Chrome on Windows, Firefox on macOS, Safari on iPhone, etc.). Each retry uses a different header set, making successive attempts appear as different browsers hitting the server.

### Consequences

- Mimics real Chrome/Firefox/Safari header blocks — goes far with anti-bot systems
- Multiple header sets = efficient retries (each looks like a different client)
- Covers common browser/OS combinations
- No external dependencies needed

---

## ADR-07: MCP Service Design — Two Tools

**Status:** Accepted  
**Date:** 2026-06-14

### Context

The MCP service needs to expose minifetch's capabilities to AI agents. We need to decide which tools to expose.

### Decision

**Option B — Two tools:** `fetch_to_markdown` (URL → markdown) + `fetch_raw` (URL → raw HTML/text).

### Consequences

- Agents get markdown for reading and raw HTML for debugging
- Simple tool surface — easy to document and implement
- Save/load is a file-system concern the agent already handles

---

## ADR-08: MCP Transport Layer — Streamable HTTP

**Status:** Accepted  
**Date:** 2026-06-14

### Context

The MCP protocol needs a transport layer. It must work with uvicorn's ASGI model.

### Decision

**Option A — MCP over HTTP (Streamable HTTP).** Single HTTP endpoint handling JSON-RPC messages. The new MCP transport standard. Works natively with uvicorn/ASGI.

### Consequences

- Modern MCP standard
- Single endpoint, simpler than SSE
- Works great with uvicorn
- Clean handshake and request handling

---

## ADR-09: CLI Design — Flag-Rich with argparse

**Status:** Accepted  
**Date:** 2026-06-14

### Context

Users need to fetch URLs and get markdown from the terminal. The CLI should be configurable without being complex.

### Decision

**Option B — Flag-rich CLI using `argparse`.** Supports `--timeout`, `--retries`, `--user-agent`, `--output`, and all configurable parameters. No subcommands for the fetch path. `minifetch mcp` starts the MCP server as a subcommand.

### Consequences

- Clean, discoverable flags
- All parameters configurable from CLI
- Two clear modes: fetch directly or start MCP server

---

## ADR-10: Logging — JSON to stderr, Optional File Flag

**Status:** Accepted  
**Date:** 2026-06-14

### Context

Logs must go to stdout/stderr, be compatible with gunicorn, and **not bloat the system needlessly**. Console-only unless explicitly requested to write to files.

### Decision

**Option B — JSON logging to stderr by default.** Custom `JSONFormatter` (no extra deps — ~20 lines). Every log line is a JSON object. Optional `--log-file` flag for file output. No log rotation, no auto-bloating of disk.

### Consequences

- Machine-parseable logs for aggregation
- Gunicorn-friendly
- Zero disk impact unless user explicitly enables file logging
- Easy debugging of MCP requests and fetch retries

---

## ADR-11: Python Version — Cross-Compatible 3.9–3.14

**Status:** Accepted  
**Date:** 2026-06-14

### Context

The library targets broad compatibility. We must avoid features introduced after Python 3.9.

### Decision

**Target Python 3.9 through 3.14.** No `match`/`case` (use `if-elif`), no `typing.TypeAlias` (use inline types), no `functools.cached_property` (use plain `@property`). Use `from __future__ import annotations` for forward reference support.

### Consequences

- Broadest possible user base
- Slightly more code for type annotations and control flow
- `from __future__ import annotations` at top of every file
- Compatible with most production environments

---

## ADR-12: .gitignore — Comprehensive

**Status:** Accepted  
**Date:** 2026-06-14

### Context

Python projects generate many artifacts. The `.gitignore` should cover all of them.

### Decision

**Comprehensive `.gitignore`** covering:
- `.venv/`, `venv/`, `env/`, `pyvenv.cfg`
- `__pycache__/`, `*.pyc`, `*.pyo`
- `.python-version`
- `.mypy_cache/`, `.ruff_cache/`
- `dist/`, `build/`, `*.egg-info/`
- `.pytest_cache/`, `coverage.xml`, `.coverage`, `htmlcov/`
- `*.log`, `*.sqlite`
- `.env`, `*.env.*`
- `.DS_Store`, `Thumbs.db`

### Consequences

- No accidental commits of generated artifacts
- Clean repo for contributors
- Covers all Python tooling outputs

---

## ADR-13: Testing Strategy — Hybrid (Mocked + Optional Integration)

**Status:** Accepted  
**Date:** 2026-06-14

### Context

Real URL integration tests are useful but introduce internet dependency and flakiness.

### Decision

**Option B — Hybrid testing.** Unit tests with mocked HTTP calls for parser logic (fast, deterministic, run in CI). Integration tests hitting stable real URLs (httpbin.org, Wikipedia, GitHub) gated behind `--integration` flag (local-only, optional).

### Consequences

- Fast CI feedback from mocked tests
- Real-URL sanity checks when run locally
- httpbin.org for deterministic HTML regression
- Wikipedia/GitHub for complex HTML regression
- No flaky CI from real URL failures

---

## ADR-14: Dependency Management — Extras for uvicorn

**Status:** Accepted  
**Date:** 2026-06-14

### Context

The library has zero dependencies, but the MCP needs `uvicorn`. We need clean separation.

### Decision

**Option B — Extras.** `uvicorn` in `[extras]`. `pip install minifetch` for library + CLI. `pip install minifetch[mcp]` for MCP.

### Consequences

- Library installable without uvicorn
- MCP requires explicit opt-in
- Clean dependency boundaries

---

## ADR-15: MCP Tool Response Format — Structured JSON

**Status:** Accepted  
**Date:** 2026-06-14

### Context

MCP tools return results to agents. The format should provide both content and useful metadata.

### Decision

**Option B — Structured JSON with markdown field.** Response includes:
```json
{
  "markdown": "...",
  "url": "https://example.com",
  "status": "success",
  "fetch_time_ms": 234
}
```
(Also `redirect_chain` for multi-redirect responses.)

### Consequences

- Agent gets markdown as a field plus metadata
- `fetch_time_ms` useful for retry decisions
- `redirect_chain` shows the full redirect path
- Clean MCP tool result structure

---

## ADR-16: HTML Encoding & Content Stripping — Detection + Strip Style/Script

**Status:** Accepted  
**Date:** 2026-06-14

### Context

HTML pages come in all encodings and may contain CSS/JS that bloats markdown output.

### Decision

**Option C — Encoding detection + script/style stripping + comment removal.** 
- Detect encoding from HTTP `Content-Type` header (highest precedence), then `<meta charset>`, then `<meta http-equiv>`, then BOM check, then UTF-8 fallback
- Strip `<style>` and `<script>` content entirely (not just hide — remove)
- Strip HTML comments
- Normalize whitespace

### Consequences

- Clean markdown output, no CSS/JS bloat
- Handles international encodings correctly
- UTF-8 fallback covers 99% of modern web
- Fail cleanly on undecodable pages rather than producing garbled output

---

## ADR-17: Error Handling — Exceptions Internally, Result Objects Externally

**Status:** Accepted  
**Date:** 2026-06-14

### Context

The API needs to handle failures gracefully while keeping internal code strict.

### Decision

**Option C — Hybrid.** Internal methods raise exceptions for unexpected bugs and config errors. Public API (`fetch_to_markdown`, `fetch_raw`) returns a `Result` object with `success: bool`, `data` or `error` field, and metadata (HTTP status, timing, redirect chain).

### Consequences

- MCP checks `success` without try/except
- Internal development stays strict (exceptions bubble up)
- Clean error reporting to agents
- Testable error paths

---

## ADR-18: Markdown Table Generation — Simple Pipe Tables + Fallback

**Status:** Accepted  
**Date:** 2026-06-14

### Context

Tables are complex in HTML (colspans, rowspans). Markdown pipe tables are simple but limited.

### Decision

**Option A — Simple pipe tables for the common case.** First row = header, second row = separator (`|---|---|`), rest = data. For tables with colspans/rowspans that can't be represented, fall back to bullet-point list representation.

### Consequences

- Covers 90%+ of real-world tables
- Clean pipe syntax output
- Graceful fallback for complex tables
- No over-engineering on edge cases

---

## ADR-19: `<details>`/`<summary>` — Always Expanded

**Status:** Accepted  
**Date:** 2026-06-14

### Context

Markdown can't represent collapsibility. `<details>` content must be shown or hidden.

### Decision

**Option B — Always show all content.** Summary as heading, content as normal text. No false promises of collapsibility. All content is visible in the output.

### Consequences

- No loss of information
- No confusing ASCII indicators
- Simple, correct behavior
- Markdown is static — it can't be collapsible anyway

---

## ADR-20: CLI User-Agent Selection — Presets + Custom Override

**Status:** Accepted  
**Date:** 2026-06-14

### Context

Users need to specify a user-agent via CLI. Presets are convenient, custom strings are flexible.

### Decision

**Option C — Hybrid.** `--ua chrome-windows` picks from stored presets (each expands to a full header set: UA + Accept headers + Sec-Fetch headers). `--ua "custom string"` also works as a raw override.

### Consequences

- Most users get presets (convenient)
- Power users get custom strings (flexible)
- Presets map to full header sets, not just the user-agent string
- Consistent with the retry header rotation strategy

---

## ADR-21: Redirect Handling — Follow + Log Chain

**Status:** Accepted  
**Date:** 2026-06-14

### Context

Browsers follow redirects by default. Agents need to know where they landed.

### Decision

**Option C — Follow redirects by default, log the redirect chain.** Include full redirect chain in response metadata (final URL + intermediate URLs). Fail when exceeding the redirect limit.

### Consequences

- Browsers follow redirects — we should too
- Agents see the full redirect path
- Response metadata includes `redirect_chain`
- Configurable redirect limit

---

## ADR-22: Security / SSRF Protection — DNS Resolution Before Connect

**Status:** Accepted  
**Date:** 2026-06-14

### Context

The MCP server receives URLs from AI agents. SSRF attacks (e.g., `http://169.254.169.254/` for cloud metadata, `http://localhost:6379/` for Redis) must be prevented.

### Decision

**DNS resolution before connect.** Resolve the hostname first (not via OS resolver which could be hijacked), check the resolved IP against private/reserved ranges (10.x.x.x, 172.16-31.x.x, 192.168.x.x, 127.x.x.x, 169.254.x.x, ::1, etc.), then connect. Prevents DNS rebinding attacks.

### Consequences

- Non-negotiable for network-facing tools
- DNS rebinding attacks mitigated
- Private/reserved IPs blocked at resolution time
- Clear error message when blocked

---

## ADR-23: Server Bind Address — Localhost Default, Explicit Override

**Status:** Accepted  
**Date:** 2026-06-14

### Context

Users may want localhost (secure) or 0.0.0.0 (external access). The default should be safe.

### Decision

**Option A — Localhost default with explicit flags.** MCP server binds to `127.0.0.1:8000` by default. Override with `--host 0.0.0.0 --port 8080`.

### Consequences

- Secure by default (localhost only)
- Explicit opt-in for external access
- No config files needed
- `--host` handles localhost vs 0.0.0.0 cleanly

---

## ADR-24: Encoding Detection — Most Thorough Stdlib Approach

**Status:** Accepted  
**Date:** 2026-06-14

### Context

We can't use `charset-normalizer` (dependency). We need the best possible encoding detection with stdlib only.

### Decision

**Option C — Most thorough stdlib approach.** HTTP `Content-Type` header first (highest precedence) → `<meta charset>` → `<meta http-equiv>` → BOM detection (`\xef\xbb\xbf`) → UTF-8 fallback. Clean failure rather than garbled output.

### Consequences

- Follows web standards (HTTP header > meta > UTF-8)
- BOM detection for files that declare UTF-8 via BOM
- No guessing, no fragile heuristics
- Fail cleanly on truly ambiguous pages

---

## ADR-25: `<abbr>` Handling — Inline Parentheses

**Status:** Accepted  
**Date:** 2026-06-14

### Context

`<abbr title="...">` elements carry semantic meaning. Markdown has no native tooltip syntax.

### Decision

**Option B — Full form in parentheses.** Render as `Markdown (full form of M)`. Inline, readable, gives the agent the full form.

### Consequences

- Captures semantic meaning inline
- No clutter from footnotes
- Useful for agents understanding technical terms
- Simple to implement

---

## ADR-26: Horizontal Rule — Standard `---`

**Status:** Accepted  
**Date:** 2026-06-14

### Context

`<hr>` must map to a markdown horizontal rule.

### Decision

**Option A — Three dashes `---`.** The universal standard in CommonMark/GFM.

### Consequences

- Every renderer supports it
- De facto standard
- No ambiguity

---

## ADR-27: URL Resolution — Absolute URLs

**Status:** Accepted  
**Date:** 2026-06-14

### Context

Markdown output is often extracted from its HTML context. Relative URLs would break.

### Decision

**Option A — Resolve all URLs to absolute.** Use `urllib.parse.urljoin(base_url, relative_url)`. Links in the output are fully self-contained.

### Consequences

- Portable markdown output
- Works in any context
- URLs are verbose but correct
- Agents get fully functional links

---

## ADR-28: Code Block Detection — Parent Check + Language Attribute

**Status:** Accepted  
**Date:** 2026-06-14

### Context

Distinguish `<code>` (inline) from `<pre><code>` (fenced block). Also capture syntax language for better agent handling.

### Decision

**Parent check + language attribute.** If `<code>` is inside `<pre>`, it's a fenced code block (triple-backtick). If inside `<p>`, `<li>`, or inline text, it's inline code (single backtick). If it's a fenced block and has `class="language-*"` or `lang="*"`, include the syntax tag.

### Consequences

- Correct for 99% of real HTML
- Syntax-aware code blocks help agents
- Inline code uses single backticks
- Language tags enable syntax highlighting in agents

---

## ADR-29: Concurrent Fetching — Gunicorn Worker Count = Concurrency

**Status:** Accepted  
**Date:** 2026-06-14

### Context

The MCP server may handle multiple fetch requests. Nested concurrency (gunicorn workers × thread pools) is confusing and can overwhelm targets.

### Decision

**Gunicorn worker count = max concurrent fetches.** No nested thread pools. User runs `gunicorn -w N -k uvicorn.workers.UvicornWorker minifetch.mcp:app` and knows exactly how many concurrent fetches they have. The thread pool from the Python API stays separate — for programmatic use, not the HTTP server. Clean separation of concerns.

### Consequences

- Predictable concurrency: worker count = concurrent fetches
- No nested concurrency to reason about
- Simple `gunicorn` command
- Programmatic API keeps its own thread pool for non-server use

---

## ADR-29b: MCP Entry Points — Factory Pattern

**Status:** Accepted  
**Date:** 2026-06-14

### Context

The MCP module needs clean entry points for gunicorn and programmatic use.

### Decision

**Factory pattern.** `create_mcp_server(minifetch_instance)` factory builds the MCP instance with an injected `Minifetch` config. `serve()` creates and runs it. Module exposes `app` (for gunicorn) and `serve()` (for programmatic use).

### Consequences

- CLI passes its own configured `Minifetch` object
- Testable factory pattern
- Clean separation between building and running
- Standard pattern for ASGI apps

---

## ADR-30: CLI-to-MCP Bridge — Two Separate Modes

**Status:** Accepted  
**Date:** 2026-06-14

### Context

Should the CLI talk to an MCP server, or call the library directly?

### Decision

**Option B — Two separate modes.** `minifetch https://example.com` calls the library directly. `minifetch mcp` starts the MCP server. Most users use direct mode, agents use MCP.

### Consequences

- Simple CLI: one command, direct result
- MCP mode is explicitly `minifetch mcp`
- No confusion about which path is taken
- Agents use MCP, humans use CLI

---

## ADR-31: Build System — setuptools

**Status:** Accepted  
**Date:** 2026-06-14

### Context

We need a `pyproject.toml` build backend. Standard, reliable, handles extras and entry points.

### Decision

**Option A — `setuptools` (pyproject.toml format).** `build-backend = "setuptools"`. Standard, universally supported, handles extras and console_scripts entry points cleanly.

### Consequences

- Every Python tool supports it
- Handles extras cleanly (`minifetch[mcp]`)
- Well-understood, no surprises
- No exotic build features needed

---

## ADR-32: Type Hints — Full Everywhere with `__future__` Annotations

**Status:** Accepted  
**Date:** 2026-06-14

### Context

Type hints improve code quality, IDE support, and self-documentation. Python 3.9+ limits some typing features.

### Decision

**Full type hints everywhere.** `from __future__ import annotations` at the top of every file for forward reference support. Every function, every method, every attribute typed. Makes the public API self-documenting.

### Consequences

- Professional, IDE-friendly codebase
- mypy can check everything
- Public API is self-documenting
- `from __future__ import annotations` handles forward references cleanly

---

## ADR-33: Code Quality Tooling — ruff + mypy

**Status:** Accepted  
**Date:** 2026-06-14

### Context

We want a clean codebase with automated quality checks.

### Decision

**ruff for linting/formatting + mypy for strict type checking.** `ruff check` + `ruff format` replace flake8 + black + isort. `mypy --strict` for type checking. Complementary tools.

### Consequences

- Fast CI (both tools are fast)
- Current Python best practice
- Style + logic checks via ruff
- Type checks via mypy
- One config file (`pyproject.toml`)

---

## ADR-34: CI/CD — GitHub Actions (ruff + mypy + pytest)

**Status:** Accepted  
**Date:** 2026-06-14

### Context

We need automated checks on every push/PR.

### Decision

**Simple GitHub Actions workflow.** Runs `ruff check`, `ruff format --check`, `mypy`, and `pytest` on every push/PR.

### Consequences

- Automated quality enforcement
- Fast CI (mocked tests are instant)
- Integration tests excluded from CI (run locally with `--integration`)
- Standard GitHub Actions setup

---

## ADR-34b: Pre-commit Hooks — Full Suite

**Status:** Accepted  
**Date:** 2026-06-14

### Context

Pre-commit hooks catch issues before they reach the repository. Should be fast enough that developers actually use them.

### Decision

**Full suite on pre-commit.** `ruff format` + `ruff check --fix` + `mypy` + `pytest` (full suite, changed-files-only for pytest). Integration tests excluded via `@pytest.mark.integration` (skipped by default).

### Consequences

- Issues caught before push
- Full test suite runs locally
- Fast enough with mocked tests
- Integration tests gated behind flag

---

## ADR-35: README — Comprehensive Reference

**Status:** Accepted  
**Date:** 2026-06-14

### Context

The README is the first thing users see. It should be self-contained.

### Decision

**Comprehensive README.** Full reference: install instructions, library API with examples, CLI flags, MCP setup with gunicorn, encoding support, error handling, security considerations. Self-contained, not a quick-start skim.

### Consequences

- Users don't need to look elsewhere for basic info
- More upfront reading for new users
- Complete reference in one place
- Reduces support questions

---

## ADR-36: License — MIT

**Status:** Accepted  
**Date:** 2026-06-14

### Context

We need a license. Minifetch is a utility library, not patent-prone.

### Decision

**Option A — MIT.** Permissive, short, lets users do anything. Industry standard for utility libraries.

### Consequences

- No restrictions on commercial use
- Short and simple
- Widely understood
- No patent grant needed

---

## ADR-37: Architecture — Modular Package

**Status:** Accepted  
**Date:** 2026-06-14

### Context

How should the `minifetch/` package be structured internally?

### Decision

**Option B — Modular package.** Separate submodules:
- `minifetch/__init__.py` — public API exports (`Minifetch`, `Result`)
- `minifetch/fetch.py` — HTTP fetching logic (retry, redirect, SSRF protection, header rotation)
- `minifetch/convert.py` — HTML to Markdown conversion (`HTMLParser`-based)
- `minifetch/cli.py` — CLI entry point (`argparse` + `Minifetch` instantiation)
- `minifetch/mcp.py` — MCP server (`create_mcp_server` factory, `serve()` function, tool definitions)
- `minifetch/models.py` — Data models (`Result`, header presets)
- `minifetch/utils.py` — Shared utilities (JSON formatter, encoding detection)

### Consequences

- Clear separation of concerns
- Each module independently testable
- Easy to find and modify code
- Thin entry points (CLI/MCP) over core logic

---

*Last updated: 2026-06-14*
