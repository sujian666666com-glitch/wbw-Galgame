#!/usr/bin/env python3
"""Build a macOS release and source archive from one clean Git commit."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import plistlib
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sdk', type=Path, default=root / '.work/renpy-sdk/renpy-8.5.3-sdk')
    parser.add_argument('--output', type=Path, default=root / 'releases/v2.1.0')
    args = parser.parse_args()
    sdk = args.sdk.resolve()
    output = args.output.resolve()
    if not (sdk / 'renpy.sh').is_file():
        raise SystemExit(f'Ren\'Py SDK not found: {sdk}')
    if subprocess.check_output(['git', 'status', '--porcelain'], cwd=root).strip():
        raise SystemExit('Commit the reviewed source before packaging; working tree is not clean.')
    lineage = root / 'doc/collaboration/v2.1/compiled-lineage.json'
    if not lineage.is_file():
        raise SystemExit('Freeze and verify old-game statement identities before packaging.')
    mapping = json.loads(lineage.read_text())
    for entry in mapping['files']:
        for field in ('source', 'compiled'):
            path = root / entry[field]
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != entry[field + '_sha256']:
                raise SystemExit(f'Statement mapping is stale: {path}')
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
    output.mkdir(parents=True, exist_ok=True)
    work_parent = root / '.work/v21/builds'
    work_parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=commit[:8] + '-', dir=work_parent))
    source_zip = output / 'wbw-galgame-2.1.0-source.zip'
    subprocess.run(['git', 'archive', '--format=zip', f'--output={source_zip}', commit], cwd=root, check=True)
    project = stage / 'project'
    with zipfile.ZipFile(source_zip) as archive:
        archive.extractall(project)
    launcher = stage / 'launcher'
    shutil.copytree(sdk / 'launcher', launcher,
                    ignore=shutil.ignore_patterns('cache', 'saves', '*.pyc'))
    environment = os.environ.copy()
    environment['RENPY_PATH_TO_SAVES'] = str(stage / 'saves')
    environment['PYTHONDONTWRITEBYTECODE'] = '1'
    log = stage / 'build.log'
    print(f'Building commit {commit}; log: {log}', flush=True)
    with log.open('w') as stream:
        subprocess.run(['python3', str(root / 'tools/v21_gui_lock_exec.py'),
                        '--lock', str(root / '.work/v21/gui.lock'), '--label', 'macOS fixed-commit build',
                        '--max-runtime', '900', '--',
                        str(sdk / 'renpy.sh'), str(launcher), 'distribute', str(project),
                        '--package', 'mac', '--format', 'app-zip', '--no-update',
                        '--destination', str(stage / 'packages')],
                       cwd=stage, env=environment, stdout=stream, stderr=subprocess.STDOUT, check=True)
    packages = list((stage / 'packages').glob('*-mac.zip'))
    if len(packages) != 1:
        raise SystemExit(f'Expected one macOS archive; inspect {log}')
    mac_zip = output / 'wbw-galgame-2.1.0-mac.zip'
    # The SDK injects build_info and bytecode cache after project classifiers.
    # This unsigned distribution omits those generated files as scoped. Keep
    # ZipInfo metadata unchanged so executable modes and symlinks survive.
    stripped_cache = []
    with zipfile.ZipFile(packages[0]) as original:
        if any('/_CodeSignature/' in name for name in original.namelist()):
            raise SystemExit('Refusing to rewrite an already signed application.')
        with zipfile.ZipFile(mac_zip, 'w') as filtered:
            for entry in original.infolist():
                if '/game/cache/' in entry.filename:
                    stripped_cache.append(entry.filename)
                    continue
                data = original.read(entry.filename)
                if entry.filename.endswith('.app/Contents/Info.plist'):
                    info = plistlib.loads(data)
                    info['CFBundleIdentifier'] = 'com.wbw.galgame'
                    data = plistlib.dumps(info)
                filtered.writestr(entry, data)
    with zipfile.ZipFile(mac_zip) as archive:
        paths = archive.namelist()
        forbidden = [name for name in paths if any(part in name.split('/') for part in
                     ('.git', '.work', '.omc', 'ik.md', 'AGENTS.md', 'testcases.rpy', 'testcases.rpyc'))
                     or '/game/saves/' in name or '/game/cache/' in name
                     or '/image/' in name or '/doc/' in name or '/tools/' in name or '/old-game/' in name]
        if forbidden:
            raise SystemExit(f'Development files found in game package: {forbidden[:10]}')
        if not any(name.endswith('/licenses/SourceHanSansLite-OFL.txt') for name in paths):
            raise SystemExit('Font license is missing from the game package.')
        if not any(name.endswith('/THIRD_PARTY_NOTICES.txt') for name in paths):
            raise SystemExit('Third-party notices are missing from the game package.')
        if not any('.app/Contents/Info.plist' in name for name in paths):
            raise SystemExit('macOS application bundle is missing.')
    artifacts = {p.name: {'bytes': p.stat().st_size,
                 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in (source_zip, mac_zip)}
    receipt = {'source_commit': commit, 'sdk': str(sdk), 'build_log': str(log),
               'notarized': False, 'bundle_identifier': 'com.wbw.galgame', 'stripped_sdk_cache': stripped_cache, 'artifacts': artifacts, 'statement_mapping_sha256': hashlib.sha256(lineage.read_bytes()).hexdigest(),
               'runtime_acceptance': 'pending: launch the extracted final application separately'}
    (output / 'build-receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
    (output / 'SHA256SUMS').write_text(''.join(f'{v["sha256"]}  {k}\n' for k, v in artifacts.items()))
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
