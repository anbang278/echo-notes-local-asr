#!/usr/bin/env python3
"""Validate the exact public inventory without reading unlisted private files."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
PRIVATE_PARTS = {'.git', '.runtime', '.developer', '.current-task', 'local-evidence',
                 '.local-evidence', 'private-fixtures',
                 '__pycache__', 'node_modules', '.venv', 'sessions'}
PRIVATE_SUFFIXES = {'.wav', '.mp3', '.m4a', '.webm', '.flac', '.safetensors',
                    '.gguf', '.onnx', '.pem', '.p12', '.p8', '.key', '.log', '.pyc'}
SECRET = re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|'
                    r'\bgh[pousr]_[A-Za-z0-9]{20,}\b|\bgithub_pat_[A-Za-z0-9_]{20,}\b')


def validate(root: Path, names: list[str], *, check_git: bool = True) -> list[str]:
    errors: list[str] = []
    if not names:
        errors.append('Public inventory is empty.')
    if len(names) != len(set(names)):
        errors.append('Duplicate public paths.')
    for name in names:
        rel = PurePosixPath(name)
        if (rel.is_absolute() or '..' in rel.parts or '\\' in name
                or not name or str(rel) != name or any(ord(c) < 32 for c in name)):
            errors.append(f'Unsafe public path: {name!r}')
            continue
        if (PRIVATE_PARTS.intersection(rel.parts) or rel.parts[0] in {'models', 'model-cache'}
                or rel.suffix.lower() in PRIVATE_SUFFIXES
                or any(part == '.env' or part.startswith('.env.') for part in rel.parts)
                or name.startswith('.trellis/workspace/') and name != '.trellis/workspace/index.md'
                or name in {'本地ASR初始化.zip', '本地ASR设计与研发计划.md'}):
            errors.append(f'Private material listed: {name}')
            continue
        path = root / name
        if any((root.joinpath(*rel.parts[:i])).is_symlink() for i in range(1, len(rel.parts) + 1)):
            errors.append(f'Symlink not permitted: {name}')
            continue
        if not path.is_file():
            errors.append(f'Missing public file: {name}')
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            errors.append(f'Unexpected binary public file: {name}')
            continue
        if SECRET.search(text):
            errors.append(f'Credential-shaped material: {name}')
        # Public examples may mention other platforms' generic home paths.
        # Reject actual owner paths without printing matching content.
        if re.search(r'/(?:Users|home)/anbang(?:/|\b)', text):
            errors.append(f'Personal absolute path: {name}')
    if check_git and (root / '.git').exists():
        result = subprocess.run(['git', '-C', str(root), 'ls-files', '-z'],
                                text=True, capture_output=True, check=True)
        tracked = set(filter(None, result.stdout.split('\0')))
        listed = set(names)
        if tracked - listed:
            errors.append('Tracked files outside public inventory: ' + ', '.join(sorted(tracked - listed)))
        if listed - tracked:
            errors.append('Public files not tracked/staged: ' + ', '.join(sorted(listed - tracked)))
    return errors


def main() -> int:
    manifest = ROOT / 'scripts/public-files.txt'
    if manifest.is_symlink() or not manifest.is_file():
        print('Missing regular public inventory.', file=sys.stderr)
        return 1
    names = [line for line in manifest.read_text().splitlines()
             if line and not line.startswith('#')]
    errors = validate(ROOT, names)
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'PASS: {len(names)} public files; privacy, paths and Git inventory checked.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
