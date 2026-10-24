#!/usr/bin/env python3
"""Freeze reviewed Ren'Py 8.5.3 product bytecode IDs for reproducible clean builds."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('compiled_project', type=Path, help='isolated, already compiled and reviewed project')
    args = parser.parse_args()
    project = args.compiled_project.resolve()
    entries = []
    names = subprocess.check_output(['git', 'ls-files', 'game'], cwd=root, text=True).splitlines()
    for name in names:
        if not name.endswith('.rpy') or name == 'game/testcases.rpy':
            continue
        source = root / name
        compiled_source = project / name
        compiled = compiled_source.with_suffix('.rpyc')
        if not compiled_source.is_file() or source.read_bytes() != compiled_source.read_bytes():
            raise SystemExit(f'Isolated source differs from release source: {name}')
        if not compiled.is_file():
            raise SystemExit(f'Missing compiled product: {compiled}')
        # Ren'Py 8.5.3 appends this source digest after the two RPYC slots.
        if compiled.read_bytes()[-16:] != hashlib.md5(source.read_bytes() + b'_2025-07-06').digest():
            raise SystemExit(f'Compiled source digest is stale: {compiled}')
        target = root / 'old-game' / Path(name).relative_to('game').with_suffix('.rpyc')
        entries.append((source, compiled, target))
    # Validate the entire input set before updating any map.
    manifest = []
    for source, compiled, target in entries:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(compiled, target)
        manifest.append({'source': str(source.relative_to(root)),
                         'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                         'compiled': str(target.relative_to(root)),
                         'compiled_sha256': hashlib.sha256(target.read_bytes()).hexdigest()})
    receipt = {'renpy': '8.5.3.26051504', 'version': '2.1.0',
               'seed': 'v20-compiled-lineage.json',
               'purpose': 'Keep original v2.0 IDs and new v2.1 IDs across clean source builds.',
               'files': manifest}
    (root / 'doc/collaboration/v2.1/compiled-lineage.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(f'Frozen {len(manifest)} product statement mappings; test and observer files excluded.')


if __name__ == '__main__':
    main()
