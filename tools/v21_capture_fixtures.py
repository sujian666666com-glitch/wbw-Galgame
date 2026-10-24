#!/usr/bin/env python3
"""Capture 2.0 compatibility fixtures for the v2.1 verification.

Runs the `fixtures` testsuite from game/testcases.rpy against the frozen 2.0
baseline. Each capture testcase reaches its menu through the real main-menu
entry and real choices, saves page-1 slot 1, and dumps the live store state.

Every GUI run serializes on the shared v2.1 GUI lock and uses its own isolated
saves root (RENPY_PATH_TO_SAVES), so neither the user's save directory nor
another agent's run is touched.

Output (main repository):
    .work/v21/compat-v20/<fixture-id>/saves/three-months-to-stay-1/1-1-LT1.save
    .work/v21/compat-v20/<fixture-id>/saves/three-months-to-stay-1/persistent
    .work/v21/compat-v20/<fixture-id>/state.json
    .work/v21/compat-v20/manifest.json
    .work/v21/compat-v20/README.md

Usage:
    python3 tools/v21_capture_fixtures.py            # capture everything
    python3 tools/v21_capture_fixtures.py --only v20_old_chapter01_menu
    python3 tools/v21_capture_fixtures.py --check    # verify manifest hashes
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

WORKTREE = Path(__file__).resolve().parents[1]


def _find_main_repo(start: Path) -> Path:
    """Repository root whose .work/v21 holds the shared fixtures.

    Works in a worktree and in the integrated main repository; does not count
    parent directories.
    """

    for candidate in (start, *start.parents):
        if (candidate / ".work/v21").is_dir() and (candidate / "game").is_dir():
            return candidate
    return start


MAIN_REPO = _find_main_repo(WORKTREE)
COMPAT_ROOT = MAIN_REPO / ".work/v21/compat-v20"
QA_ROOT = WORKTREE / ".work/qa"

SAVE_DIRECTORY = "three-months-to-stay-1"
SLOT_FILE = "1-1-LT1.save"

FIXTURES = [
    {
        "id": "v20_old_chapter01_menu",
        "case": "capture_v20_old_chapter01_menu",
        "arc": "old",
        "description": "旧篇：主菜单→旧篇→序章选择后自然到达第一章菜单（ability=3，未做第一章选择）",
        "purpose": "2.1 在旧篇第一章前后插入片段时的早期菜单兼容性；验证 from 2.0 存档读入后数值与进度不变",
    },
    {
        "id": "v20_old_chapter06_menu",
        "case": "capture_v20_old_chapter06_menu",
        "arc": "old",
        "description": "旧篇：自然走完序章至第五章（理想数值路线），停在第六章三选项菜单",
        "purpose": "旧篇结局前插入（persistent 写入之前）与第六章菜单的兼容性；同时覆盖三结局选择入口",
    },
    {
        "id": "v20_sequel_first_menu",
        "case": "capture_v20_sequel_first_menu",
        "arc": "sequel",
        "description": "续篇：主菜单→新篇→序章自然到达第一个菜单，未做任何续篇选择",
        "purpose": "续篇序章/第一章新增片段的早期兼容性；验证 story_arc/续篇变量初始值",
    },
    {
        "id": "v20_sequel_finale_menu",
        "case": "capture_v20_sequel_finale_menu",
        "arc": "sequel",
        "description": "续篇：自然走完四季章节（全信任/高洞察路线），停在终章六选项菜单之前",
        "purpose": "终章最终 menu 之前插入与真结局前置的兼容性；核对四碎片、insight/resolve、四人信任",
    },
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def save_metadata(save_path: Path) -> dict:
    """Read the small json member of a Ren'Py save (version/ctime)."""
    try:
        with zipfile.ZipFile(save_path) as zf:
            raw = zf.read("json")
        return json.loads(raw.decode("utf-8"))
    except Exception as exc:  # pragma: no cover - diagnostic only
        return {"error": repr(exc)}


def load_states(state_path: Path) -> list[dict]:
    records = []
    if not state_path.is_file():
        return records
    for line in state_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            records.append(json.loads(line))
    return records


def run_capture(fixture: dict, project: Path) -> int:
    fixture_id = fixture["id"]
    work = QA_ROOT / "fixtures" / fixture_id
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    saves = work / "saves"
    state_path = work / "state.jsonl"
    log_path = QA_ROOT / "logs" / f"fixture-{fixture_id}.log"

    cmd = [
        sys.executable,
        str(WORKTREE / "tools/v21_run_tests.py"),
        "--project",
        str(project),
        "--saves",
        str(saves),
        "--case",
        f"fixtures::{fixture['case']}",
        "--log",
        str(log_path),
        "--state-file",
        str(state_path),
        "--label",
        f"fixture:{fixture_id}",
    ]
    print(f"\n=== capturing {fixture_id} ===")
    print(" ".join(cmd))
    proc = subprocess.run(cmd, cwd=str(WORKTREE))
    if proc.returncode != 0:
        print(f"capture failed: {fixture_id} (exit {proc.returncode})", file=sys.stderr)
        return proc.returncode

    save = saves / SAVE_DIRECTORY / SLOT_FILE
    if not save.is_file():
        print(f"save missing: {save}", file=sys.stderr)
        return 3

    fixture_dir = COMPAT_ROOT / fixture_id
    if fixture_dir.exists():
        shutil.rmtree(fixture_dir)
    target_saves = fixture_dir / "saves" / SAVE_DIRECTORY
    target_saves.mkdir(parents=True)
    shutil.copy2(save, target_saves / SLOT_FILE)

    persistent = saves / SAVE_DIRECTORY / "persistent"
    if persistent.is_file():
        shutil.copy2(persistent, target_saves / "persistent")

    records = load_states(state_path)
    if not records:
        print(f"state record missing: {state_path}", file=sys.stderr)
        return 4
    (fixture_dir / "state.json").write_text(
        json.dumps(records[-1], ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    meta = save_metadata(target_saves / SLOT_FILE)
    files = []
    for path in sorted(target_saves.iterdir()):
        if path.is_file():
            files.append(
                {
                    "path": str(path.relative_to(fixture_dir)),
                    "size": path.stat().st_size,
                    "sha256": sha256(path),
                }
            )

    return {
        "id": fixture_id,
        "arc": fixture["arc"],
        "description": fixture["description"],
        "purpose": fixture["purpose"],
        "capture_testcase": fixture["case"],
        "captured_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "game_version": meta.get("_version"),
        "renpy_version": meta.get("_renpy_version"),
        "save_directory": SAVE_DIRECTORY,
        "slot": "page 1 / slot 1",
        "files": files,
        "state": records[-1],
    }


def write_readme(manifest: dict) -> None:
    lines = [
        "# 2.0 兼容存档夹具（v2.1 验收用）",
        "",
        "由 `tools/v21_capture_fixtures.py` 在冻结的 2.0 基线上真实游玩生成：",
        "每个夹具都从主菜单进入对应篇章，按真实选项走到目标 menu 后用存档 UI 的",
        "page 1 / slot 1 保存，并同步记录当时的 store 状态。生成过程持有",
        "`.work/v21/gui.lock` 独占锁，使用独立 `RENPY_PATH_TO_SAVES` 与隔离 persistent，",
        "不读写用户存档。",
        "",
        "## 目录",
        "",
        "```text",
        "compat-v20/",
        "├── manifest.json                  # 夹具清单、状态记录、文件 SHA-256",
        "├── README.md",
    ]
    for fixture in manifest["fixtures"]:
        lines.append(f"├── {fixture['id']}/")
        lines.append("│   ├── state.json                 # 存档时刻的 store/persistent 状态")
        lines.append(f"│   └── saves/{SAVE_DIRECTORY}/1-1-LT1.save")
    lines += [
        "```",
        "",
        "## 用法（2.1 验证时）",
        "",
        "```bash",
        "# 1. 准备隔离存档根目录，把夹具拷进去（不要指向用户存档）",
        "mkdir -p .work/qa/saves-2.1",
        f"cp -R .work/v21/compat-v20/<fixture>/saves/{SAVE_DIRECTORY} .work/qa/saves-2.1/",
        "",
        "# 2. 用 2.1 项目副本跑 GUI（必须持 gui.lock）",
        "python3 tools/v21_run_tests.py --project .work/qa/project --saves .work/qa/saves-2.1 \\",
        "    --case <compat testcase>",
        "```",
        "",
        "`state.json` 给出读档后应立即成立的数值；2.1 读入后应保持旧篇数值与进度，",
        "新增变量使用 `default` 的初值（例如 `sequel_luna_observation_outcome = \"unknown\"`）。",
        "",
        "## 夹具一览",
        "",
    ]
    for fixture in manifest["fixtures"]:
        state = fixture["state"]["state"]
        lines.append(f"### {fixture['id']}")
        lines.append("")
        lines.append(f"- 篇：{fixture['arc']}")
        lines.append(f"- 说明：{fixture['description']}")
        lines.append(f"- 用途：{fixture['purpose']}")
        lines.append(f"- 游戏版本：{fixture['game_version']} / Ren'Py {fixture['renpy_version']}")
        lines.append(f"- 存档时刻语句：`{fixture['state']['current']}`")
        lines.append(
            "- 关键数值："
            + ", ".join(
                f"{key}={state[key]}"
                for key in (
                    "ability",
                    "affection",
                    "money",
                    "chapter_progress",
                    "story_arc",
                    "sequel_chapter_progress",
                    "sequel_insight",
                    "sequel_resolve",
                    "dana_affection",
                    "luna_affection",
                    "irene_affection",
                    "ruby_affection",
                )
                if key in state
            )
        )
        lines.append("")
    (COMPAT_ROOT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default=str(QA_ROOT / "project-fixtures"))
    parser.add_argument("--only", action="append", default=[], help="fixture id (repeatable)")
    parser.add_argument("--check", action="store_true", help="verify existing manifest hashes")
    parser.add_argument("--no-build", action="store_true", help="reuse an existing project copy")
    args = parser.parse_args()

    COMPAT_ROOT.mkdir(parents=True, exist_ok=True)

    if args.check:
        manifest_path = COMPAT_ROOT / "manifest.json"
        if not manifest_path.is_file():
            print(f"missing manifest: {manifest_path}", file=sys.stderr)
            return 2
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        bad = 0
        for fixture in manifest["fixtures"]:
            for entry in fixture["files"]:
                path = COMPAT_ROOT / fixture["id"] / entry["path"]
                if not path.is_file():
                    print(f"MISSING {path}")
                    bad += 1
                    continue
                if sha256(path) != entry["sha256"]:
                    print(f"HASH MISMATCH {path}")
                    bad += 1
        print(f"checked {len(manifest['fixtures'])} fixtures: {'ok' if not bad else f'{bad} problem(s)'}")
        return 0 if not bad else 1

    project = Path(args.project).resolve()
    print(f"main repo: {MAIN_REPO}")
    print(f"compat dir: {COMPAT_ROOT}")
    if not args.no_build:
        subprocess.run(
            [
                sys.executable,
                str(WORKTREE / "tools/v21_qa_project.py"),
                "--source",
                str(WORKTREE),
                "--dest",
                str(project),
                "--saves",
                str(QA_ROOT / "fixtures/saves-unused"),
                "--clean",
            ],
            check=True,
            cwd=str(WORKTREE),
        )

    wanted = set(args.only)
    results = []
    for fixture in FIXTURES:
        if wanted and fixture["id"] not in wanted:
            continue
        result = run_capture(fixture, project)
        if isinstance(result, int):
            return result
        results.append(result)

    manifest_path = COMPAT_ROOT / "manifest.json"
    previous = {}
    if manifest_path.is_file():
        try:
            old = json.loads(manifest_path.read_text(encoding="utf-8"))
            previous = {f["id"]: f for f in old.get("fixtures", [])}
        except Exception:
            previous = {}
    merged = dict(previous)
    for result in results:
        merged[result["id"]] = result

    manifest = {
        "purpose": "Ren'Py 2.0 -> 2.1 save compatibility fixtures (v2.1 acceptance)",
        "created_by": "tools/v21_capture_fixtures.py (Pi QA)",
        "save_directory": SAVE_DIRECTORY,
        "fixtures": [merged[key] for key in sorted(merged)],
    }
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_readme(manifest)
    print(f"\nwrote {manifest_path}")
    print(f"wrote {COMPAT_ROOT / 'README.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
