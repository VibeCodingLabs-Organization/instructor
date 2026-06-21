#!/bin/bash
set -e
echo "Running pytest for agent_ecosystem..."
uv run pytest agent_ecosystem/tests/
echo "Tests passed."
