#!/usr/bin/env python3
"""Run Ren'Py acceptance tests under the shared v2.1 GUI lock.

Every GUI/native-interface run in the v2.1 effort must serialize through the
main repository's ``.work/v21/gui.lock``. This wrapper:

  * acquires that lock exclusively (fcntl.flock) for the whole run,
  * points RENPY_PATH_TO_SAVES at an isolated saves root,
  * optionally enables the QA trace overlay (V21_QA_TRACE),
  * tees the full Ren'Py output to a log file,
  * prints a compact PASSED/FAILED summary and returns a nonzero exit code
    when the run did not pass.

Usage:
    python3 tools/v21_run_tests.py --case global --log .work/qa/logs/full.log
    python3 tools/v21_run_tests.py --case save_load_smoke --trace .work/qa/logs/trace.jsonl

Exit codes: 0 = passed, 1 = failed tests, 2 = configuration error,
40 = could not acquire GUI lock.
"""

from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
from pathlib import Path

DEFAULT_LOCK = "/Users/ik/Desktop/02_学习与资料/game/my-renpy-game/.work/v21/gui.lock"
DEFAULT_SDK = (
    "/Users/ik/Desktop/02_学习与资料/game/my-renpy-game/.work/renpy-sdk/renpy-8.5.3-sdk/renpy.sh"
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default=".work/qa/project")
    parser.add_argument("--saves", default=".work/qa/saves")
    parser.add_argument("--case", default="global", help="testcase or testsuite name")
    parser.add_argument("--log", default="", help="tee output to this log file")
    parser.add_argument("--trace", default="", help="enable QA trace overlay, write JSONL here")
    parser.add_argument(
        "--focus-chaos",
        action="store_true",
        help="only with --trace: simulate periodic host-window focus loss",
    )
    parser.add_argument("--state-file", default="", help="fixture capture: V21_QA_STATE_FILE target")
    parser.add_argument("--label-file", default="", help="record dynamically reached v21_* labels here")
    parser.add_argument("--lock", default=DEFAULT_LOCK)
    parser.add_argument("--sdk", default=DEFAULT_SDK)
    parser.add_argument("--timeout", type=float, default=3600.0, help="GUI lock wait timeout")
    parser.add_argument(
        "--max-runtime",
        type=float,
        default=300.0,
        help="positive maximum runtime in seconds (default 300)",
    )
    parser.add_argument("--label", default="", help="diagnostic label recorded in the lock file")
    parser.add_argument("--detailed", action="store_true", default=True)
    args = parser.parse_args()

    project = Path(args.project).resolve()
    saves = Path(args.saves).resolve()
    sdk = Path(args.sdk)

    for path, what in ((project, "project"), (sdk, "SDK")):
        if not path.exists():
            print(f"error: {what} not found: {path}", file=sys.stderr)
            return 2

    if args.max_runtime <= 0:
        parser.error("--max-runtime must be positive")
    pause_file = Path(args.lock).resolve().parent / "TESTS_PAUSED_BY_USER"
    if pause_file.exists():
        print("tests paused by user", file=sys.stderr)
        return 42
    saves.mkdir(parents=True, exist_ok=True)
    lock_helper = Path(__file__).with_name("v21_gui_lock_exec.py")

    env = dict(os.environ)
    env["RENPY_PATH_TO_SAVES"] = str(saves)
    if args.trace:
        trace_path = Path(args.trace).resolve()
        trace_path.parent.mkdir(parents=True, exist_ok=True)
        if trace_path.exists():
            trace_path.unlink()
        env["V21_QA_TRACE"] = str(trace_path)
        if args.focus_chaos:
            env["V21_QA_FOCUS_CHAOS"] = "1"
    if args.state_file:
        state_path = Path(args.state_file).resolve()
        state_path.parent.mkdir(parents=True, exist_ok=True)
        if state_path.exists():
            state_path.unlink()
        env["V21_QA_STATE_FILE"] = str(state_path)
    if args.label_file:
        label_path = Path(args.label_file).resolve()
        label_path.parent.mkdir(parents=True, exist_ok=True)
        if label_path.exists():
            label_path.unlink()
        env["V21_QA_LABEL_FILE"] = str(label_path)

    cmd = [
        sys.executable,
        str(lock_helper),
        "--lock",
        args.lock,
        "--timeout",
        str(args.timeout),
        "--label",
        args.label or f"v21-qa:{args.case}",
        "--max-runtime",
        str(args.max_runtime),
        "--",
        str(sdk),
        str(project),
        "test",
        args.case,
        "--report-detailed",
    ]

    log_file = None
    if args.log:
        log_path = Path(args.log).resolve()
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_file = open(log_path, "w", encoding="utf-8")
        print(f"log: {log_path}")

    lines: list[str] = []
    # The lock holder owns the deadline and the Ren'Py process group. It also
    # observes this wrapper's PID, so killing the wrapper cannot orphan a game.
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            env=env, text=True, bufsize=1)
    interrupted = [None]
    def forward_signal(signum, frame):
        interrupted[0] = signum
        if proc.poll() is None:
            proc.send_signal(signum)
    signal.signal(signal.SIGINT, forward_signal)
    signal.signal(signal.SIGTERM, forward_signal)
    try:
        assert proc.stdout is not None
        for line in proc.stdout:
            lines.append(line)
            sys.stdout.write(line)
            sys.stdout.flush()
            if log_file is not None:
                log_file.write(line)
                log_file.flush()
        rc = proc.wait()
    finally:
        if proc.poll() is None:
            proc.terminate()
            proc.wait(timeout=10)
        if log_file is not None:
            log_file.close()
    if interrupted[0]:
        return 128 + interrupted[0]
    if rc in (40, 41, 42, 43):
        return rc

    joined = "".join(lines)
    failed = "Status: FAILED" in joined
    passed = "Status: PASSED" in joined

    print("\n=== v21_run_tests summary ===")
    for line in lines:
        if line.startswith("[rpytest]   FAILED") or line.startswith("[rpytest]   PASSED"):
            print(line.rstrip())
        elif line.startswith("[rpytest] Status:"):
            print(line.rstrip())

    if rc == 40:
        print("lock not acquired", file=sys.stderr)
        return 40
    if rc != 0 or failed or not passed:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
