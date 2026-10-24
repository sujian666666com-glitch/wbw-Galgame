#!/usr/bin/env python3
"""Load the 2.0 compatibility fixtures into a build and verify the state.

For every fixture in ``<fixtures>/manifest.json``:

  1. copy its save + persistent into a fresh isolated saves root,
  2. run the matching `compat_*` testcase from game/testcases.rpy (which loads
     page-1 slot 1, re-enters the saved menu and asserts the values),
  3. compare the live store state after the load with the state recorded when
     the fixture was captured.

A fixture only passes when, after loading the save:

  * the run itself succeeded,
  * the game resumed at the *saved statement* (same file as at capture time)
    and is showing an actual choice menu - falling back to ``start`` / the main
    menu is a failure, not a pass,
  * every recorded store value is unchanged,
  * ``persistent`` is byte-for-byte equivalent to the captured one,
  * new 2.1 variables that did not exist in 2.0 still hold their ``default``
    (``sequel_luna_observation_outcome == "unknown"``).

All Ren'Py runs serialize on the shared v2.1 GUI lock (via v21_run_tests.py)
and never touch the user's save directory.

Usage:
    python3 tools/v21_compat_check.py                  # all fixtures
    python3 tools/v21_compat_check.py --only v20_old_chapter01_menu
    python3 tools/v21_compat_check.py --project .work/qa/project-2.1
    python3 tools/v21_compat_check.py --fixtures /path/to/compat-v20 \
        --output .work/qa/logs/compat-report.json
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import shutil
import subprocess
import sys
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path

# <repo>/tools/v21_compat_check.py -> <repo>. Works in a worktree and in the
# integrated main repository alike; no fixed number of parent directories.
REPO_ROOT = Path(__file__).resolve().parents[1]
QA_ROOT = REPO_ROOT / ".work/qa"
SAVE_DIRECTORY = "three-months-to-stay-1"
DEFAULT_MAX_RUNTIME = 90.0

# Keys where a 2.1 build must keep the 2.0 value exactly.
EXACT_KEYS = [
    "ability",
    "affection",
    "money",
    "chapter_progress",
    "ending_route",
    "evidence_ready",
    "side_project_ready",
    "story_arc",
    "sequel_chapter_progress",
    "sequel_route",
    "sequel_insight",
    "sequel_resolve",
    "dana_affection",
    "luna_affection",
    "irene_affection",
    "ruby_affection",
    "spring_fragment",
    "summer_fragment",
    "autumn_fragment",
    "winter_fragment",
]

# Variables introduced in 2.1: a 2.0 save has no value for them, so the
# `default` statement must supply exactly this and nothing else.
DEFAULT_SENTINELS = {"sequel_luna_observation_outcome": "unknown"}

# A resumed statement from these files means the save fell back instead of
# restoring the saved position.
START_FALLBACK_FILES = {"game/script.rpy"}

# The only fixtures whose public verification key may be trusted, after their
# files have been checked against tools/v21_capture_fixtures.py's manifest.
APPROVED_FIXTURES = {
    "v20_old_chapter01_menu",
    "v20_old_chapter06_menu",
    "v20_sequel_first_menu",
    "v20_sequel_finale_menu",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _decode_line(line: str):
    parts = line.strip().split(None, 2)
    if len(parts) < 2:
        return "", b""
    try:
        return parts[0], base64.b64decode(parts[1])
    except Exception:
        return "", b""


def save_verification_keys(save_path: Path) -> list[bytes]:
    """Public verification keys from the signatures member of a save file.

    Only the DER public key is read. No private key exists in a save file, and
    this function never opens a token/key store outside the isolated saves
    root.
    """

    keys = []
    with zipfile.ZipFile(save_path) as zf:
        if "signatures" not in zf.namelist():
            return keys
        signatures = zf.read("signatures").decode("utf-8")
    for line in signatures.splitlines():
        kind, key = _decode_line(line)
        if kind == "signature" and key:
            keys.append(key)
    return keys


def persistent_verification_keys(persistent_path: Path) -> list[bytes]:
    """Public verification keys appended after the zlib stream of persistent."""

    if not persistent_path.is_file():
        return []
    do = zlib.decompressobj()
    do.decompress(persistent_path.read_bytes())
    tail = do.unused_data.decode("utf-8")
    keys = []
    for line in tail.splitlines():
        kind, key = _decode_line(line)
        if kind == "signature" and key:
            keys.append(key)
    return keys


def trust_fixture_public_keys(
    fixture_id: str, saves_root: Path, copied_save: Path, copied_persistent: Path
) -> list[str]:
    """Add this fixture's own public verification keys to its isolated token dir.

    Ren'Py's renpy/savetoken.py:check_load() prompts UNKNOWN_TOKEN/TRUST_TOKEN
    for a save whose signature key is not in the save-directory token store.
    FileLoad(confirm=False) does not bypass that prompt. A save that was moved
    from another machine (here: from the frozen 2.0 capture project) therefore
    has to have its public key trusted explicitly.

    Security boundary: only the four approved, hash-fixed, self-generated
    fixtures are trusted; only the public key embedded in the signature of
    that fixture's own save/persistent is written; no private key is read or
    written, and no global/user token store is touched. The SDK still creates
    and uses its own private key for this isolated saves root.
    """

    if fixture_id not in APPROVED_FIXTURES:
        raise SystemExit(f"refusing to trust unapproved fixture {fixture_id!r}")

    keys = save_verification_keys(copied_save)
    if not keys:
        raise SystemExit(f"fixture {fixture_id!r}: save has no signature verification key")

    persistent_keys = persistent_verification_keys(copied_persistent)
    unknown = [key for key in persistent_keys if key not in keys]
    if unknown:
        raise SystemExit(f"fixture {fixture_id!r}: persistent is signed by a key absent from the save")

    token_dir = saves_root / "tokens"
    token_dir.mkdir(parents=True, exist_ok=True)
    key_file = token_dir / "security_keys.txt"
    # This isolated directory is created fresh per fixture; never merge with a
    # pre-existing store (which could contain unrelated keys).
    key_file.write_text("", encoding="utf-8")
    fingerprints = []
    with key_file.open("a", encoding="utf-8") as f:
        for key in keys:
            # ecdsa NIST256p SubjectPublicKeyInfo DER is 91 bytes and starts
            # with an ASN.1 SEQUENCE. Reject anything else outright.
            if len(key) != 91 or key[0] != 0x30:
                raise SystemExit(f"fixture {fixture_id!r}: unexpected verification key encoding")
            f.write("verifying-key " + base64.b64encode(key).decode("ascii") + "\n")
            fingerprints.append(hashlib.sha256(key).hexdigest())
    return fingerprints


def find_fixtures_root(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).resolve()
    env = os.environ.get("V21_COMPAT_ROOT")
    if env:
        return Path(env).resolve()
    for candidate in (REPO_ROOT, *REPO_ROOT.parents):
        root = candidate / ".work/v21/compat-v20"
        if root.is_dir():
            return root
    return REPO_ROOT / ".work/v21/compat-v20"


def statement_file(current: str | None) -> str | None:
    """Extract 'game/story/x.rpy' from a repr'd statement tuple."""

    if not current:
        return None
    text = current.strip()
    if text.startswith("(") and len(text) > 1:
        text = text[1:].split(",", 1)[0].strip().strip("'\"")
    return text or None


def run(cmd: list[str]) -> int:
    print("\n$ " + " ".join(cmd))
    return subprocess.run(cmd, cwd=str(REPO_ROOT)).returncode


def load_last_state(path: Path) -> dict:
    if not path.is_file():
        return {}
    records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return records[-1] if records else {}


def check_fixture(fixture: dict, after: dict, rc: int) -> list[str]:
    """Return a list of human-readable problems (empty means pass)."""

    problems: list[str] = []
    expected_state = fixture["state"].get("state", {})
    actual_state = after.get("state", {})

    if rc != 0:
        problems.append(f"testcase failed with exit {rc}")

    for key in EXACT_KEYS:
        if key not in expected_state:
            continue
        if actual_state.get(key) != expected_state[key]:
            problems.append(f"{key}: expected {expected_state[key]!r}, got {actual_state.get(key)!r}")

    for key, sentinel in DEFAULT_SENTINELS.items():
        if key in expected_state:
            # A 2.0 capture that already had it must match that value.
            if actual_state.get(key) != expected_state[key]:
                problems.append(f"{key}: expected {expected_state[key]!r}, got {actual_state.get(key)!r}")
        elif actual_state.get(key) != sentinel:
            problems.append(f"{key}: expected 2.1 default {sentinel!r}, got {actual_state.get(key)!r}")

    expected_persistent = fixture["state"].get("persistent")
    actual_persistent = after.get("persistent")
    if expected_persistent is not None and actual_persistent != expected_persistent:
        problems.append(f"persistent: expected {expected_persistent!r}, got {actual_persistent!r}")

    # Resumed position: a real menu from the saved file, never a start fallback.
    expected_file = statement_file(fixture["state"].get("current"))
    actual_file = statement_file(after.get("current"))
    if actual_file is None:
        problems.append("no resumed statement recorded (save was not loaded)")
    else:
        if actual_file in START_FALLBACK_FILES:
            problems.append(f"resumed at start fallback {actual_file!r}, not the saved menu")
        if expected_file and actual_file != expected_file:
            problems.append(f"resumed in {actual_file!r}, captured in {expected_file!r}")

    captions = after.get("choice_captions")
    if not captions:
        problems.append("no choice menu was displayed after loading (no captions)")
    expected_captions = fixture["state"].get("choice_captions")
    if expected_captions is not None and captions != expected_captions:
        problems.append(f"menu captions: expected {expected_captions!r}, got {captions!r}")

    return problems


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default=str(QA_ROOT / "project"))
    parser.add_argument("--fixtures", default=None, help="fixtures root (default: <repo>/.work/v21/compat-v20)")
    parser.add_argument("--output", default=None, help="write a machine-readable JSON report here")
    parser.add_argument("--only", action="append", default=[])
    parser.add_argument("--keep", action="store_true", help="keep per-fixture save roots")
    parser.add_argument("--trace", action="store_true", help="write a QA trace JSONL per fixture")
    parser.add_argument(
        "--max-runtime",
        type=float,
        default=DEFAULT_MAX_RUNTIME,
        help=f"per-fixture Ren'Py runtime cap in seconds (default {DEFAULT_MAX_RUNTIME:g})",
    )
    args = parser.parse_args()

    fixtures_root = find_fixtures_root(args.fixtures)
    manifest_path = fixtures_root / "manifest.json"
    if not manifest_path.is_file():
        print(
            f"missing manifest: {manifest_path}\n"
            "pass --fixtures <compat-v20 dir> or set V21_COMPAT_ROOT",
            file=sys.stderr,
        )
        return 2

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    wanted = set(args.only)
    project = Path(args.project).resolve()
    results = []
    failed = False

    for fixture in manifest["fixtures"]:
        fixture_id = fixture["id"]
        if wanted and fixture_id not in wanted:
            continue

        work = QA_ROOT / "compat" / fixture_id
        if work.exists() and not args.keep:
            shutil.rmtree(work)
        saves = work / "saves"
        (saves / SAVE_DIRECTORY).mkdir(parents=True, exist_ok=True)

        # The fixture hash check comes first: the public key may only be
        # trusted once the bytes are exactly the approved captured fixture.
        hash_problems = []
        for entry in fixture["files"]:
            src = fixtures_root / fixture_id / entry["path"]
            if not src.is_file():
                hash_problems.append(f"missing fixture file {src}")
            elif sha256_file(src) != entry["sha256"]:
                hash_problems.append(f"fixture hash mismatch {src}")
        if hash_problems:
            print(f"fixture {fixture_id}: {'; '.join(hash_problems)}", file=sys.stderr)
            results.append(
                {
                    "fixture": fixture_id,
                    "arc": fixture.get("arc"),
                    "status": "failed",
                    "problems": hash_problems,
                    "exit": 3,
                }
            )
            failed = True
            continue

        for entry in fixture["files"]:
            src = fixtures_root / fixture_id / entry["path"]
            dst = saves / SAVE_DIRECTORY / Path(entry["path"]).name
            shutil.copy2(src, dst)

        key_fingerprints = trust_fixture_public_keys(
            fixture_id,
            saves,
            saves / SAVE_DIRECTORY / "1-1-LT1.save",
            saves / SAVE_DIRECTORY / "persistent",
        )

        state_path = work / "after-load.jsonl"
        log_path = QA_ROOT / "logs" / f"compat-{fixture_id}.log"
        if state_path.exists():
            state_path.unlink()

        rc = run(
            [
                sys.executable,
                str(REPO_ROOT / "tools/v21_run_tests.py"),
                "--project",
                str(project),
                "--saves",
                str(saves),
                "--case",
                f"compat::compat_{fixture_id}",
                "--log",
                str(log_path),
                "--state-file",
                str(state_path),
                "--label",
                f"compat:{fixture_id}",
                "--max-runtime",
                str(args.max_runtime),
                *(
                    ["--trace", str(QA_ROOT / "logs" / f"trace-compat-{fixture_id}.jsonl")]
                    if args.trace
                    else []
                ),
            ]
        )

        after = load_last_state(state_path)
        problems = check_fixture(fixture, after, rc)
        results.append(
            {
                "fixture": fixture_id,
                "arc": fixture.get("arc"),
                "status": "passed" if not problems else "failed",
                "problems": problems,
                "exit": rc,
                "loaded_current": after.get("current"),
                "expected_current": fixture["state"].get("current"),
                "choice_captions": after.get("choice_captions"),
                "persistent": after.get("persistent"),
                "log": str(log_path),
                "trusted_key_fingerprints": key_fingerprints,
            }
        )
        if problems:
            failed = True

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "fixtures_root": str(fixtures_root),
        "project": str(project),
        "max_runtime": args.max_runtime,
        "trust_policy": {
            "approved_fixtures": sorted(APPROVED_FIXTURES),
            "trusted_material": "public verification key from each fixture's own save/persistent signature only; no private key, no global token store",
        },
        "ok": not failed,
        "checked": len(results),
        "results": results,
    }

    if args.output:
        output = Path(args.output).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"\nreport: {output}")

    print("\n=== v2.0 save compatibility ===")
    for item in results:
        print(f"{item['status'].upper():6s} {item['fixture']}")
        for problem in item["problems"]:
            print(f"       {problem}")
        if item["loaded_current"]:
            print(f"       resumed at {item['loaded_current']}")
        if item["choice_captions"]:
            print(f"       menu: {len(item['choice_captions'])} option(s)")

    print(f"\n{len(results)} fixture(s), {'FAILED' if failed else 'all compatible'}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
