#!/usr/bin/env python3
"""Machine-readable v2.1 acceptance coverage matrix (QA-owned, read-only).

Static evidence:
  * every menu option in game/story/*.rpy and the testcases that click it,
  * every v2.1 insert label and its product call site.

Runtime evidence (when the files exist):
  * labels dynamically reached during `tools/v21_run_tests.py --case global
    --label-file ...`,
  * the four 2.0 save compatibility results from v21_compat_check.py.

Usage:
    python3 tools/v21_coverage_report.py \
        --labels .work/qa/logs/global-labels.txt \
        --compat .work/qa/logs/compat-report.json \
        --output .work/qa/logs/coverage-matrix.json
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
STORY = REPO_ROOT / "game/story"
TESTCASES = REPO_ROOT / "game/testcases.rpy"
EXPECTED_OPTIONS = 61
EXPECTED_LABELS = 23

MENU_RE = re.compile(r'^(\s*)menu(?:\s+\w+)?\s*:\s*$')
OPTION_RE = re.compile(r'^(\s*)"((?:[^"\\]|\\.)+)"(?:\s+if\s+.+)?\s*:\s*$')
CLICK_RE = re.compile(r'^\s*click\s+"((?:[^"\\]|\\.)+)"')
TESTCASE_RE = re.compile(r'^(\s*)testcase\s+(\w+)')
LABEL_RE = re.compile(r'^label\s+(v21_\w+)\s*:', re.M)
CALL_RE = re.compile(r'^\s*(?:call|jump)\s+(v21_\w+)', re.M)


def scan_options():
    menus, options = [], []
    for path in sorted(STORY.glob("*.rpy")):
        lines = path.read_text(encoding="utf-8").splitlines()
        i = 0
        while i < len(lines):
            m = MENU_RE.match(lines[i])
            if not m:
                i += 1
                continue
            indent = len(m.group(1))
            menu = {"file": str(path.relative_to(REPO_ROOT)), "line": i + 1, "options": []}
            i += 1
            while i < len(lines):
                line = lines[i]
                if not line.strip():
                    i += 1
                    continue
                cur = len(line) - len(line.lstrip())
                if cur <= indent:
                    break
                om = OPTION_RE.match(line)
                if om:
                    caption = om.group(2)
                    menu["options"].append(caption)
                    options.append(
                        {"caption": caption, "file": menu["file"], "line": i + 1}
                    )
                i += 1
            menus.append(menu)
    return menus, options


def scan_clicks():
    clicks = []
    for number, line in enumerate(TESTCASES.read_text(encoding="utf-8").splitlines(), 1):
        m = CLICK_RE.match(line)
        if m:
            clicks.append({"text": m.group(1), "line": number})
    return clicks


def scan_testcases():
    """Count top-level (global) and nested (fixture/compat) testcases."""

    global_cases, nested_cases = [], []
    for line in TESTCASES.read_text(encoding="utf-8").splitlines():
        m = TESTCASE_RE.match(line)
        if not m:
            continue
        (global_cases if len(m.group(1)) == 0 else nested_cases).append(m.group(2))
    return {
        "global": len(global_cases),
        "nested_fixture_compat": len(nested_cases),
        "total": len(global_cases) + len(nested_cases),
        "settings_smoke_present": "settings_smoke_main_menu_and_in_game" in global_cases,
        "global_names": global_cases,
    }


def scan_labels():
    expected, calls = {}, []
    for path in sorted(STORY.glob("*.rpy")):
        text = path.read_text(encoding="utf-8")
        for name in LABEL_RE.findall(text):
            expected[name] = str(path.relative_to(REPO_ROOT))
        for name in CALL_RE.findall(text):
            calls.append({"label": name, "file": str(path.relative_to(REPO_ROOT))})
    return expected, calls


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels", default=str(REPO_ROOT / ".work/qa/logs/global-labels.txt"))
    ap.add_argument("--compat", default=str(REPO_ROOT / ".work/qa/logs/compat-report.json"))
    ap.add_argument("--output", default=str(REPO_ROOT / ".work/qa/logs/coverage-matrix.json"))
    args = ap.parse_args()

    menus, options = scan_options()
    clicks = scan_clicks()
    testcases = scan_testcases()
    expected_labels, calls = scan_labels()

    for option in options:
        option["clicked_by"] = [
            c for c in clicks if c["text"] in option["caption"]
        ]
        option["covered"] = bool(option["clicked_by"])

    label_path = Path(args.labels)
    reached = set()
    if label_path.is_file():
        reached = {l.strip() for l in label_path.read_text(encoding="utf-8").splitlines() if l.strip()}

    compat = {}
    compat_path = Path(args.compat)
    if compat_path.is_file():
        report = json.loads(compat_path.read_text(encoding="utf-8"))
        compat = {
            item["fixture"]: {
                "status": item["status"],
                "exit": item.get("exit"),
                "resumed": item.get("loaded_current"),
                "choice_captions": item.get("choice_captions"),
                "trusted_key_fingerprints": item.get("trusted_key_fingerprints"),
            }
            for item in report.get("results", [])
        }

    covered = [o for o in options if o["covered"]]
    missing = [o for o in options if not o["covered"]]
    labels_reached = sorted(set(expected_labels) & reached)
    labels_missing = sorted(set(expected_labels) - reached)

    matrix = {
        "generated_from": {
            "story": str(STORY.relative_to(REPO_ROOT)),
            "testcases": str(TESTCASES.relative_to(REPO_ROOT)),
            "labels_file": str(label_path),
            "compat_report": str(compat_path),
        },
        "options": {
            "menus": len(menus),
            "total": len(options),
            "expected": EXPECTED_OPTIONS,
            "covered": len(covered),
            "missing": len(missing),
            "ok": len(options) == EXPECTED_OPTIONS and not missing,
            "items": [
                {
                    "caption": o["caption"],
                    "file": o["file"],
                    "line": o["line"],
                    "covered": o["covered"],
                    "clicked_by_lines": [c["line"] for c in o["clicked_by"]],
                }
                for o in options
            ],
        },
        "testcases": testcases,
        "v21_labels": {
            "expected": len(expected_labels),
            "dynamically_reached": len(labels_reached),
            "missing": labels_missing,
            "ok": len(expected_labels) == EXPECTED_LABELS and not labels_missing,
            "items": [
                {
                    "label": name,
                    "defined_in": expected_labels[name],
                    "call_sites": [c["file"] for c in calls if c["label"] == name],
                    "reached_in_run": name in reached,
                }
                for name in sorted(expected_labels)
            ],
        },
        "summer_m05": {
            "values": ["unknown", "paper_tape", "aborted", "evacuated"],
            "evidence": {
                "unknown": "compat::compat_v20_sequel_* (2.0 default after load)",
                "paper_tape": "sequel_full_flow_true_ending",
                "aborted": "sequel_low_trust_flow",
                "evacuated": "sequel_partial_trust_flow",
            },
        },
        "low_trust_heroines": {
            "values": {"dana": 0, "luna": 0, "irene": 0, "ruby": 0},
            "evidence": "sequel_low_trust_flow",
        },
        "true_ending": {
            "met": "sequel_full_flow_true_ending / compat_v20_sequel_finale_menu (6 offered)",
            "not_met": ["sequel_true_gate_insight_short", "sequel_true_gate_missing_fragment"],
        },
        "compat": compat,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(matrix, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"options: {len(options)} (expected {EXPECTED_OPTIONS}), covered {len(covered)}, missing {len(missing)}")
    for item in missing:
        print(f"  UNCOVERED {item['caption']} ({item['file']}:{item['line']})")
    print(f"v21 labels: {len(expected_labels)} (expected {EXPECTED_LABELS}), reached {len(labels_reached)}, missing {len(labels_missing)}")
    print(f"testcases: {testcases['total']} total, {testcases['global']} global, {testcases['nested_fixture_compat']} fixture/compat")
    for name in labels_missing:
        print(f"  NOT REACHED {name}")
    print(f"compat results: {len(compat)}")
    print(f"report: {output}")
    return 0 if matrix["options"]["ok"] and matrix["v21_labels"]["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
