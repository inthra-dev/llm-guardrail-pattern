#!/usr/bin/env python3
"""
gate.py — minimal preflight validator for LLM execution plans.

Usage:
  ./gate.py plan.json --allow-path nginx/nginx.conf --allow-path docker-compose.yml
  ./gate.py plan.json --allow-op read_file --allow-op edit_file

Exit codes:
  0 = PASS
  2 = FAIL (contract/scope violation)
  3 = FAIL (invalid input)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any


DEFAULT_ALLOWED_OPS = {"read_file", "edit_file"}


def eprint(*args: Any) -> None:
    print(*args, file=sys.stderr)


def fail(msg: str, code: int = 2) -> None:
    eprint(f"FAIL: {msg}")
    sys.exit(code)


def is_safe_relative_path(p: str) -> bool:
    # Must be a clean relative path without traversal or absolute prefixes.
    if not isinstance(p, str) or not p.strip():
        return False
    if os.path.isabs(p):
        return False
    # Normalize and ensure it doesn't escape.
    norm = os.path.normpath(p)
    if norm.startswith("..") or "/../" in norm.replace("\\", "/") or norm == "..":
        return False
    # Prevent weird edge cases
    if norm.startswith("~"):
        return False
    return True


def load_json(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        fail(f"Plan file not found: {path}", code=3)
    except json.JSONDecodeError as e:
        fail(f"Invalid JSON: {e}", code=3)
    except Exception as e:
        fail(f"Cannot read plan: {e}", code=3)

    if not isinstance(data, dict):
        fail("Top-level JSON must be an object", code=3)
    return data


def validate_plan(plan: dict, allowed_ops: set[str], allowed_paths: set[str]) -> None:
    ops = plan.get("operations")
    if not isinstance(ops, list) or not ops:
        fail("Missing or empty 'operations' array", code=3)

    for i, item in enumerate(ops):
        if not isinstance(item, dict):
            fail(f"operations[{i}] must be an object", code=3)

        op_type = item.get("op")
        path = item.get("path")
        reason = item.get("reason")

        if op_type not in allowed_ops:
            fail(
                f"operations[{i}].op '{op_type}' not allowed. "
                f"Allowed ops: {sorted(allowed_ops)}"
            )

        if not isinstance(path, str):
            fail(f"operations[{i}].path must be a string", code=3)

        if not is_safe_relative_path(path):
            fail(f"operations[{i}].path '{path}' is not a safe relative path")

        # Enforce exact allowlist match (tightest control).
        if path not in allowed_paths:
            fail(
                f"operations[{i}].path '{path}' not allowed. "
                f"Allowed paths: {sorted(allowed_paths)}"
            )

        if not isinstance(reason, str) or not reason.strip():
            fail(f"operations[{i}].reason must be a non-empty string", code=3)

    # Optional: enforce presence of task for auditability
    task = plan.get("task")
    if task is not None and (not isinstance(task, str) or not task.strip()):
        fail("'task' must be a non-empty string if present", code=3)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate an LLM execution plan against an allowlist.")
    parser.add_argument("plan_json", help="Path to plan.json")
    parser.add_argument(
        "--allow-op",
        action="append",
        default=[],
        help="Allowed operation (repeatable). Default: read_file, edit_file",
    )
    parser.add_argument(
        "--allow-path",
        action="append",
        default=[],
        help="Allowed file path (repeatable), relative to repo root.",
    )

    args = parser.parse_args()

    allowed_ops = set(args.allow_op) if args.allow_op else set(DEFAULT_ALLOWED_OPS)
    allowed_paths = set(args.allow_path)

    if not allowed_paths:
        fail("No allowed paths provided. Use --allow-path <path> ...", code=3)

    # Validate allowlist entries themselves
    for p in allowed_paths:
        if not is_safe_relative_path(p):
            fail(f"Allowlisted path '{p}' is not a safe relative path", code=3)

    plan = load_json(args.plan_json)
    validate_plan(plan, allowed_ops, allowed_paths)

    print("PASS: plan within declared scope")
    sys.exit(0)


if __name__ == "__main__":
    main()

