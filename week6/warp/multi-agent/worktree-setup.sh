#!/usr/bin/env bash
# Create two git worktrees for concurrent Warp agents working on week6 tasks.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
PARENT="$(dirname "$ROOT")"
BASE_BRANCH="${BASE_BRANCH:-HEAD}"

WT_A="${PARENT}/modern-ai-wt-task-a"
WT_B="${PARENT}/modern-ai-wt-task-b"

echo "Repo root: $ROOT"
echo "Creating worktrees (idempotent if already present)..."

if [[ ! -d "$WT_A" ]]; then
  git -C "$ROOT" worktree add -b week6/agent-a "$WT_A" "$BASE_BRANCH"
else
  echo "Already exists: $WT_A"
fi

if [[ ! -d "$WT_B" ]]; then
  git -C "$ROOT" worktree add -b week6/agent-b "$WT_B" "$BASE_BRANCH"
else
  echo "Already exists: $WT_B"
fi

echo
echo "Open Warp tabs with cwd:"
echo "  A) $WT_A/week6   → paste warp/prompts/week6-test-agent.md"
echo "  B) $WT_B/week6   → paste warp/prompts/week6-code-agent.md"
echo
echo "Cleanup later:"
echo "  git -C \"$ROOT\" worktree remove \"$WT_A\""
echo "  git -C \"$ROOT\" worktree remove \"$WT_B\""
