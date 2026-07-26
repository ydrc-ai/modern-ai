#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
TEST_PATH="${1:-backend/tests}"
PYTHONPATH=. pytest -q "$TEST_PATH" --maxfail="${MAXFAIL:-1}"
echo "OK: week6 tests passed"
