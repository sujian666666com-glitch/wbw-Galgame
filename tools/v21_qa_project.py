#!/usr/bin/env python3
"""Build an isolated Ren'Py project copy for v2.1 QA runs.

The checkout (this worktree, or the main repository once the tools are
integrated there) is never used directly for GUI tests: every run gets its own
project copy and its own saves root, so that no save/persistent data leaks into
the user's real save directory and concurrent runs cannot interleave.

The copy contains:

  * ``game/``            source files; compiled ``.rpyc`` and caches are NOT
                         copied, so the build always reflects the sources;
  * ``old-game/``        the frozen 2.0 compiled tree, copied *including*
                         ``.rpyc``. Ren'Py uses it to keep the 2.0 statement
                         identities stable, which is what makes 2.0 saves
                         resume at the right statement instead of falling back
                         to ``start``;
  * ``game/qa_trace.rpy`` only with ``--trace``, from
                         ``tools/v21_qa_trace.rpy.txt``.

Usage:
    python3 tools/v21_qa_project.py \
        --source . \
        [--dest .work/qa/project] \
        [--saves .work/qa/saves] \
        [--trace] [--clean]

Options:
    --source DIR   checkout to copy (default: repo root containing this tool)
    --dest DIR     destination project (default: <repo>/.work/qa/project)
    --saves DIR    saves root for RENPY_PATH_TO_SAVES (default: <repo>/.work/qa/saves)
    --trace        add game/qa_trace.rpy instrumentation overlay
    --clean        delete --dest and --saves first (only inside an isolated
                   .work/qa directory; never the source tree or a real save dir)
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

# <repo>/tools/v21_qa_project.py -> <repo>. Works both in a worktree and in the
# integrated main repository, without counting parent directories.
REPO_ROOT = Path(__file__).resolve().parents[1]

SKIP_DIRS = {"cache", "saves", "__pycache__"}
SKIP_SUFFIXES = (".rpyc", ".rpymc")
SKIP_FILES = {".DS_Store", "log.txt", "errors.txt", "traceback.txt", "files.txt"}


def copytree(src: Path, dst: Path, *, keep_compiled: bool) -> int:
    """Copy a tree; compiled bytecode only when keep_compiled is true."""

    count = 0
    for root, dirs, files in os.walk(src):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        target_dir = dst / Path(root).relative_to(src)
        target_dir.mkdir(parents=True, exist_ok=True)
        for name in sorted(files):
            if name in SKIP_FILES:
                continue
            if not keep_compiled and name.endswith(SKIP_SUFFIXES):
                continue
            shutil.copy2(Path(root) / name, target_dir / name)
            count += 1
    return count


def is_isolated(path: Path) -> bool:
    """True when path is a disposable QA destination.

    A destination is only safe to delete when it lives under a directory named
    ``.work`` (the isolated scratch root of this project) and is not a home
    directory, a Ren'Py save directory, or a filesystem root. This is a
    positive allow-list, not a blocklist: an unexpected path is refused.
    """

    resolved = path.resolve()
    parts = resolved.parts
    if ".work" not in parts:
        return False
    if len(parts) < parts.index(".work") + 2:
        return False  # neither .work itself nor anything above it
    if resolved == Path.home().resolve() or resolved == Path("/"):
        return False
    lowered = str(resolved).lower()
    if "renpy_saves" in lowered or "/library/renpy" in lowered:
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=str(REPO_ROOT))
    parser.add_argument("--dest", default=str(REPO_ROOT / ".work/qa/project"))
    parser.add_argument("--saves", default=str(REPO_ROOT / ".work/qa/saves"))
    parser.add_argument("--trace", action="store_true")
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()

    source = Path(args.source).resolve()
    dest = Path(args.dest).resolve()
    saves = Path(args.saves).resolve()

    src_game = source / "game"
    if not (src_game / "script.rpy").is_file():
        print(f"error: {src_game}/script.rpy not found", file=sys.stderr)
        return 2

    for label, target in (("dest", dest), ("saves", saves)):
        # Deleting a destination that is the source or an ancestor of it would
        # destroy the checkout; descendants are the normal, isolated case and
        # are covered by is_isolated() below.
        if target == source or target in source.parents:
            print(f"error: --{label} {target} is the source tree or its ancestor {source}", file=sys.stderr)
            return 2
        if not is_isolated(target):
            print(
                f"error: --{label} {target} is not an isolated .work/... destination; "
                "refusing to write or clean there",
                file=sys.stderr,
            )
            return 2

    if args.clean:
        shutil.rmtree(dest, ignore_errors=True)
        shutil.rmtree(saves, ignore_errors=True)

    dest.mkdir(parents=True, exist_ok=True)
    saves.mkdir(parents=True, exist_ok=True)

    game_count = copytree(src_game, dest / "game", keep_compiled=False)

    old_game_count = 0
    src_old_game = source / "old-game"
    if src_old_game.is_dir():
        # Includes .rpyc: these carry the 2.0 statement identities.
        old_game_count = copytree(src_old_game, dest / "old-game", keep_compiled=True)

    if args.trace:
        template = REPO_ROOT / "tools/v21_qa_trace.rpy.txt"
        if not template.is_file():
            print(f"error: trace template missing: {template}", file=sys.stderr)
            return 2
        shutil.copy2(template, dest / "game/qa_trace.rpy")

    print(f"project: {dest}")
    print(f"  game files copied: {game_count}")
    print(f"  old-game files copied: {old_game_count} (compiled .rpyc kept)")
    print(f"  saves root: {saves}")
    print(f"  trace overlay: {'yes' if args.trace else 'no'}")
    return 0 if old_game_count else 0


if __name__ == "__main__":
    sys.exit(main())
