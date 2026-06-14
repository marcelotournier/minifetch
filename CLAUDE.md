# Minifetch

Minifetch is a python library with no dependencies that creates a API to fetching URLs and convert them to Markdown.

This repo installs the minifetch lib and also the minifetch CLI and the minifetch MCP that serves for agents.

There should be an option for enabling ips (eg folks who want localhost vs 0.0.0.0)

Development of this library follows TDD Red Green development.

The web server for the MCP service should be uvicorn compatible.

Logs should go to stdout/stderr and be compatible with gunicorn logging as well (Case we want to save as files in the future)

Create a python .gitignore, a virtualenv .venv (.venv should be ignored)

Create an integration test suite with real urls to verify the workings.

Make sure the MCP contains enough instructions for the agent to use it.
