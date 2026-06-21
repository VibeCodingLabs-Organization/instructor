#!/bin/bash
set -e
echo "Running Ruff linter..."
uv run ruff check agent_ecosystem/
echo "Running Ruff formatter check..."
uv run ruff format --check agent_ecosystem/
echo "Linting passed."
