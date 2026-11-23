#!/usr/bin/env python3
"""Check installed Trellis hook output without touching task/session data.

Task discovery and configuration are stubbed; the installed hook's main routing,
workflow loader, state rendering, and host response encoding run unchanged.
"""

from __future__ import annotations

import argparse
import ast
import contextlib
import io
import json
import os
from pathlib import Path
import re
import runpy
from types import SimpleNamespace
from unittest.mock import patch


def check_hook(root: Path, hook: Path, platform: str) -> list[dict]:
    ast.parse(hook.read_text(encoding="utf-8"), filename=str(hook))
    module = runpy.run_path(str(hook))
    main = module["main"]
    namespace = main.__globals__
    results = []
    cases = [
        ("no_task", None, "检查当前白屏问题"),
        ("explicit_creation_request", None, "请创建一个 Trellis 任务"),
        ("planning", ("policy-check-task", "planning", "session:test"), "继续"),
        ("in_progress", ("policy-check-task", "in_progress", "session:test"), "继续"),
        ("completed", ("policy-check-task", "completed", "session:test"), "继续"),
        ("stale", ("policy-check-task", "stale_session", "session:test"), "继续"),
    ]
    for state, task, prompt in cases:
        data = {"cwd": str(root), "prompt": prompt, "session_id": "policy-check"}
        stdout = io.StringIO()
        replacements = {
            "_load_hook_input": lambda: data,
            "_detect_platform": lambda _: platform,
            "get_active_task": lambda *_: task,
            "_read_trellis_config": lambda _: {"codex": {"dispatch_mode": "inline"}},
        }
        with patch.dict(namespace, replacements), patch.dict(os.environ, {}, clear=True):
            with contextlib.redirect_stdout(stdout):
                code = main()
        output = stdout.getvalue()
        passed = code == 0
        if task is None:
            passed = passed and output == ""
        else:
            try:
                body = json.loads(output)["hookSpecificOutput"]["additionalContext"]
            except (ValueError, KeyError, TypeError):
                body = ""
            passed = passed and "policy-check-task" in body and task[1] in body
        results.append({"hook": str(hook), "state": state, "passed": passed, "output": output})
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("projects", type=Path, nargs="+")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    results = []
    for root in args.projects:
        for folder, platform in [(".codex", "codex"), (".claude", "claude"), (".cursor", "cursor")]:
            hook = root / folder / "hooks" / "inject-workflow-state.py"
            if hook.is_file():
                results.extend(check_hook(root, hook, platform))
            session_hook = root / folder / "hooks" / "session-start.py"
            if session_hook.is_file():
                ast.parse(session_hook.read_text(encoding="utf-8"), filename=str(session_hook))
                module = runpy.run_path(str(session_hook))
                status = module.get("_get_task_status")
                if status is not None:
                    with patch.dict(status.__globals__, {
                        "_resolve_active_task": lambda *_: SimpleNamespace(task_path=None),
                    }):
                        output = status(root / ".trellis", {})
                    asks_creation = re.search(
                        r"\basks?\s+(?:only\s+)?(?:whether|for task-creation consent)",
                        output, re.IGNORECASE,
                    )
                    results.append({
                        "hook": str(session_hook), "state": "session_start_no_task",
                        "passed": "NO ACTIVE TASK" in output and not asks_creation,
                        "output": output,
                    })
    if not results:
        parser.error("No installed Trellis hooks found")
    failures = [r for r in results if not r["passed"]]
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for r in failures:
            print(f"FAIL {r['hook']} {r['state']}")
        print(f"Hook checks: {len(results) - len(failures)}/{len(results)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
