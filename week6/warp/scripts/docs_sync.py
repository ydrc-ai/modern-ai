#!/usr/bin/env python3
"""Regenerate week6/docs/API.md from a running FastAPI /openapi.json."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path


def fetch_openapi(base_url: str) -> dict:
    url = base_url.rstrip("/") + "/openapi.json"
    with urllib.request.urlopen(url, timeout=10) as resp:
        return json.load(resp)


def route_rows(spec: dict) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for path, methods in sorted(spec.get("paths", {}).items()):
        for method, meta in sorted(methods.items()):
            if method.startswith("x-"):
                continue
            summary = (meta or {}).get("summary") or (meta or {}).get("operationId") or ""
            rows.append((method.upper(), path, summary))
    return rows


def parse_existing_routes(text: str) -> set[tuple[str, str]]:
    found: set[tuple[str, str]] = set()
    for match in re.finditer(r"\|\s*`?([A-Z]+)`?\s*\|\s*`([^`]+)`", text):
        found.add((match.group(1), match.group(2)))
    return found


def render(spec: dict, previous: str) -> str:
    title = spec.get("info", {}).get("title", "Week 6 API")
    version = spec.get("info", {}).get("version", "")
    rows = route_rows(spec)
    old = parse_existing_routes(previous) if previous else set()
    new = {(m, p) for m, p, _ in rows}

    added = sorted(new - old)
    removed = sorted(old - new)

    lines = [
        f"# {title}",
        "",
        f"Generated from `/openapi.json` (OpenAPI {spec.get('openapi', '')}, app version {version}).",
        "",
        "## Endpoints",
        "",
        "| Method | Path | Summary |",
        "|--------|------|---------|",
    ]
    for method, path, summary in rows:
        lines.append(f"| `{method}` | `{path}` | {summary} |")

    lines += ["", "## Delta vs previous API.md", ""]
    if not previous.strip():
        lines.append("_No previous file — full inventory written._")
    else:
        if not added and not removed:
            lines.append("No route additions or removals detected.")
        if added:
            lines.append("**Added:**")
            for m, p in added:
                lines.append(f"- `{m} {p}`")
        if removed:
            lines.append("**Removed:**")
            for m, p in removed:
                lines.append(f"- `{m} {p}`")

    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument(
        "--out",
        default=str(Path(__file__).resolve().parents[2] / "docs" / "API.md"),
    )
    args = parser.parse_args()
    out_path = Path(args.out)

    try:
        spec = fetch_openapi(args.base_url)
    except urllib.error.URLError as exc:
        print(f"Failed to fetch OpenAPI from {args.base_url}: {exc}", file=sys.stderr)
        print("Start the app with `make run` first.", file=sys.stderr)
        return 1

    previous = out_path.read_text() if out_path.exists() else ""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render(spec, previous))
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
