#!/usr/bin/env python3
"""Serialize a bounded GUI run and reap its whole process group before unlocking."""
from __future__ import annotations
import argparse
import fcntl
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
from datetime import datetime


def log(message):
    try:
        print(f"[v21-lock {datetime.now().strftime('%H:%M:%S')}] {message}", file=sys.stderr, flush=True)
    except (BrokenPipeError, OSError):
        pass


def alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def group_alive(pgid):
    try:
        os.killpg(pgid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        # Darwin can briefly report EPERM for a group whose last members have
        # died. Inspect only pid-group/status, never command lines or secrets.
        states = subprocess.check_output(['ps', '-axo', 'pgid=,stat='], text=True)
        return any(int(parts[0]) == pgid and not parts[1].startswith('Z')
                   for row in states.splitlines() if len(parts := row.split()) == 2)


def reap_group(child, grace=2.0):
    # A wrapper can exit before its descendants. Never use child.wait() alone
    # to decide whether escalation is needed: that caused the October 24 leak.
    pgid = child.pid
    if group_alive(pgid):
        try:
            os.killpg(pgid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        until = time.monotonic() + grace
        while group_alive(pgid) and time.monotonic() < until:
            child.poll()
            time.sleep(0.05)
        if group_alive(pgid):
            try:
                os.killpg(pgid, signal.SIGKILL)
            except ProcessLookupError:
                pass
    child.wait(timeout=5)
    # SIGKILL delivery is asynchronous. Keep the GUI lock until the kernel
    # has removed the remaining group, including orphaned grandchildren.
    until = time.monotonic() + 5.0
    while group_alive(pgid) and time.monotonic() < until:
        time.sleep(0.02)
    if group_alive(pgid):
        raise RuntimeError(f"process group {pgid} survived SIGKILL; manual inspection required")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lock', required=True)
    parser.add_argument('--timeout', type=float, default=3600.0, help='lock acquisition deadline')
    parser.add_argument('--max-runtime', type=float, default=300.0, help='positive child runtime limit')
    parser.add_argument('--label', default='')
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    if not command or args.max_runtime <= 0 or args.timeout <= 0:
        parser.error('a command and positive time limits are required')
    lock_path = Path(args.lock).resolve()
    pause_file = lock_path.parent / 'TESTS_PAUSED_BY_USER'
    parent_pid = os.getppid()
    owner_pid = int(os.environ.get('V21_TEST_OWNER_PID', parent_pid))
    interrupted = [None]
    def signal_handler(signum, frame):
        interrupted[0] = signum
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    def stop_reason():
        if interrupted[0]:
            return 128 + interrupted[0], 'interrupted'
        if pause_file.exists():
            return 42, 'tests paused by user'
        if os.getppid() != parent_pid or not alive(owner_pid):
            return 43, 'test supervisor exited'
        return None
    if reason := stop_reason():
        log(reason[1]);return reason[0]
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open('a+') as lock:
        until = time.monotonic() + args.timeout
        while True:
            if reason := stop_reason():
                log(reason[1]);return reason[0]
            try:
                fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= until:
                    return 40
                time.sleep(0.1)
        child = None
        rc = 1
        try:
            if reason := stop_reason():
                return reason[0]
            child = subprocess.Popen(command, start_new_session=True)
            lock.seek(0);lock.truncate()
            lock.write(f'pid={os.getpid()} child_pgid={child.pid} owner={owner_pid} label={args.label!r}\n')
            lock.flush()
            log(f'lock acquired; child group {child.pid}; limit {args.max_runtime:g}s')
            until = time.monotonic() + args.max_runtime
            while True:
                if reason := stop_reason():
                    rc = reason[0];log(reason[1]);break
                if child.poll() is not None:
                    rc = child.returncode;break
                if time.monotonic() >= until:
                    rc = 41;log('runtime deadline reached');break
                time.sleep(0.1)
        finally:
            if child is not None:
                reap_group(child)
            lock.seek(0);lock.truncate()
            lock.write(f'released pid={os.getpid()} exit={rc} label={args.label!r}\n')
            lock.flush()
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)
            log('child group reaped; lock released')
        return rc


if __name__ == '__main__':
    sys.exit(main())
