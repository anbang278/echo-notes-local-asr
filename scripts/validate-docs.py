#!/usr/bin/env python3
"""Validate bootstrap document links and public-file inventory. No network access."""
from __future__ import annotations
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    manifest = ROOT / 'scripts/public-files.txt'
    if not manifest.is_file():
        print('Missing public-file manifest.', file=sys.stderr)
        return 1
    names = [line for line in manifest.read_text(encoding='utf-8').splitlines()
             if line and not line.startswith('#')]
    errors: list[str] = []
    if len(names) != len(set(names)):
        errors.append('Duplicate entries in public-file manifest.')
    for name in names:
        rel = Path(name)
        if rel.is_absolute() or '..' in rel.parts:
            errors.append(f'Unsafe public path: {name}')
            continue
        p = ROOT / rel
        if not p.is_file():
            errors.append(f'Missing public file: {name}')
            continue
        if p.is_symlink() or any(parent.is_symlink() for parent in p.parents if parent != ROOT):
            errors.append(f'Symlink not permitted: {name}')
        # Upstream bundled skills retain their own links and source examples.
        # Check project-owned Markdown, including spec/task documents.
        if p.suffix != '.md' or (name.startswith(('.codex/', '.pi/', '.agents/skills/trellis-'))):
            continue
        text = p.read_text(encoding='utf-8')
        if len(re.findall(r'^```', text, flags=re.MULTILINE)) % 2:
            errors.append(f'Unbalanced fenced code block: {name}')
        if '\ufffd' in text or '' in text or 'sandbox:/' in text:
            errors.append(f'Invalid encoding or chat-only marker: {name}')
        for target in re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)', text):
            target = target.strip().split(' "', 1)[0]
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            resolved = (p.parent / unquote(parsed.path)).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                errors.append(f'Local link leaves repository: {name}: {target}')
                continue
            if not resolved.exists():
                errors.append(f'Broken local link: {name}: {target}')
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'PASS: {len(names)} public files; local Markdown targets and code fences checked.')
    print('This is a documentation check, not ASR, macOS, or remote GitHub validation.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
