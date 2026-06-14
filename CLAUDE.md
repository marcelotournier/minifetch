# Minifetch

Minifetch is a python library with no dependencies that creates a API to fetching URLs and convert them to Markdown.

This repo installs the minifetch lib and also the minifetch CLI and the minifetch MCP that serves for agents.

**ARCHITECTURE.md is the source of truth for all project decisions.** All architectural decisions are recorded there as ADRs. Follow them when making changes to this project.

## Development Workflow

### TDD Red-Green Development
- **Red:** Write the failing test first (assertion fails)
- **Green:** Write minimum code to make the test pass
- **Refactor:** Clean up without breaking the test
- One test at a time. No implementation without a failing test.

### Tracer Bullet Approach
- Start with a single end-to-end path that validates the whole architecture
- The tracer bullet goes through: `Result` model → `Minifetch` class → fetch → convert → CLI output
- Build incrementally, commit after each Green

### Local Testing
- Always use `pip install -e .` for editable local installs
- For MCP testing: `pip install -e ".[mcp]"`
- Never use plain `pip install .` — always editable mode

### Pre-commit Hooks
- Install: `pre-commit install` (in .venv)
- Runs: `ruff format`, `ruff check --fix`, `mypy`, `pytest` (full suite, no integration)
- Integration tests excluded by default (run with `--integration` flag)

### Cross-Platform Compatibility
- Python 3.9–3.14 on Linux, macOS, Windows
- No platform-specific stdlib features
- All paths use `pathlib`
- No shell commands in tests
- Windows line endings handled by `ruff format --check`

### Commit Discipline
- Commit after each Green (each passing test)
- Push after each commit
- Atomic commits: one logical change per commit

### Testing Strategy
- Unit tests: mocked HTTP, fast, run on every pre-commit
- Integration tests: real URLs (httpbin.org, Wikipedia), gated behind `--integration`
- Never commit without all tests passing

## Requirements

- There should be an option for enabling IPs (eg folks who want localhost vs 0.0.0.0)
- Development follows TDD Red Green development
- The MCP web server is uvicorn-compatible, served behind gunicorn
- Logs go to stdout/stderr in JSON format, compatible with gunicorn. Console-only unless `--log-file` flag is set.
- Create a python `.gitignore`, a virtualenv `.venv` (ignored)
- Integration test suite with real URLs (gated behind `--integration` flag)
- MCP contains enough instructions for agents to use it

## Key Decisions (See ARCHITECTURE.md for Full Details)

- Single package with entry points (ADR-01)
- `html.parser.HTMLParser` for HTML→Markdown conversion (ADR-02)
- Comprehensive scope minus images (ADR-03)
- Configurable fetcher with retries, exponential backoff (ADR-04)
- Class-based `Minifetch` API (ADR-05)
- Full browser header sets stored for retry rotation (ADR-06)
- Two MCP tools: `fetch_to_markdown` + `fetch_raw` (ADR-07)
- Streamable HTTP transport for MCP (ADR-08)
- `argparse` CLI with full config flags (ADR-09)
- JSON logging to stderr, optional file output (ADR-10)
- Python 3.9–3.14 cross-compatible (ADR-11)
- Comprehensive `.gitignore` (ADR-12)
- Hybrid testing: mocked unit tests + optional integration tests (ADR-13)
- Extras dependency: `uvicorn` in `[extras]` (ADR-14)
- Structured JSON MCP tool responses (ADR-15)
- Encoding detection + strip style/script (ADR-16)
- Hybrid error handling: exceptions internally, `Result` objects externally (ADR-17)
- Simple pipe tables with bullet fallback (ADR-18)
- `<details>` always expanded (ADR-19)
- Preset + custom user-agent CLI (ADR-20)
- Follow redirects, log chain (ADR-21)
- DNS resolution before connect for SSRF protection (ADR-22)
- Localhost default for MCP server (ADR-23)
- Thorough stdlib encoding detection (ADR-24)
- `<abbr>` as inline parentheses (ADR-25)
- Standard `---` horizontal rule (ADR-26)
- Absolute URL resolution (ADR-27)
- Parent check + language attribute for code blocks (ADR-28)
- Gunicorn worker count = concurrency (ADR-29)
- Factory pattern for MCP entry points (ADR-29b)
- Two separate CLI modes (ADR-30)
- setuptools build backend (ADR-31)
- Full type hints with `from __future__ import annotations` (ADR-32)
- ruff + mypy tooling (ADR-33)
- GitHub Actions: ruff + mypy + pytest (ADR-34)
- Pre-commit: full suite (ADR-34b)
- Comprehensive README (ADR-35)
- MIT license (ADR-36)
- Modular package: fetch.py, convert.py, cli.py, mcp.py (ADR-37)
