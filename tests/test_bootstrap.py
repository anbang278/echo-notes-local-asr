"""Local-only publication-script tests using fake gh and real, temporary git repos.

These tests do not create repositories on GitHub and do not validate macOS ASR.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FAKE_GH = r'''#!/usr/bin/env python3
import json, os, pathlib, subprocess, sys
args = sys.argv[1:]
state = pathlib.Path(os.environ['FAKE_GH_STATE'])
scenario = os.environ.get('FAKE_GH_SCENARIO', 'success')
with (state / 'calls.jsonl').open('a') as stream:
    stream.write(json.dumps(args) + '\n')
if args[:2] == ['auth', 'status']:
    sys.exit(1 if scenario == 'authfail' else 0)
if args[:1] == ['api'] and 'user' in args:
    print('other-account' if scenario == 'wronguser' else 'anbang278')
    sys.exit(0)
if args[:2] == ['repo', 'view']:
    if scenario != 'existing' and not (state / 'created').exists():
        sys.exit(1)
    field = args[args.index('--json') + 1]
    if field == 'visibility':
        print('PRIVATE' if scenario == 'wrongvisibility' else 'PUBLIC')
    elif field == 'defaultBranchRef':
        print('main')
    else:
        print(json.dumps({'nameWithOwner': 'anbang278/echo-notes-local-asr'}))
    sys.exit(0)
if args[:2] == ['repo', 'create']:
    if scenario == 'createfail':
        sys.exit(1)
    assert '--public' in args and '--push' in args and '--remote' in args
    source = args[args.index('--source') + 1]
    sha = subprocess.check_output(['git', '-C', source, 'rev-parse', 'HEAD'], text=True).strip()
    (state / 'created').write_text(sha)
    sys.exit(0)
if args[:2] == ['repo', 'edit']:
    assert args[-2:] == ['--default-branch', 'main']
    sys.exit(0)
if args[:1] == ['api'] and any('/commits/main' in item for item in args):
    print('0' * 40 if scenario == 'wrongsha' else (state / 'created').read_text())
    sys.exit(0)
raise SystemExit('Unexpected gh invocation: ' + repr(args))
'''

@unittest.skipUnless(shutil.which('git') and shutil.which('bash'), 'git and bash required')
class BootstrapTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix='asr-bootstrap-test-')
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
        self.repo = base / 'project with spaces'
        shutil.copytree(ROOT, self.repo, ignore=shutil.ignore_patterns('.git', '__pycache__'))
        self.state = base / 'state'
        self.state.mkdir()
        binary = base / 'bin'
        binary.mkdir()
        gh = binary / 'gh'
        gh.write_text(FAKE_GH)
        gh.chmod(0o755)
        self.env = dict(os.environ)
        self.env.update({
            'PATH': str(binary) + os.pathsep + os.environ.get('PATH', ''),
            'FAKE_GH_STATE': str(self.state),
            'GIT_CONFIG_NOSYSTEM': '1',
            'GIT_CONFIG_GLOBAL': os.devnull,
            'GIT_CEILING_DIRECTORIES': str(base),
            'GIT_TERMINAL_PROMPT': '0',
        })
        # Prevent caller's repository variables from redirecting temporary git operations.
        for name in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE'):
            self.env.pop(name, None)

    def run_script(self, scenario: str = 'success', mode: str = '--publish') -> subprocess.CompletedProcess[str]:
        env = dict(self.env, FAKE_GH_SCENARIO=scenario)
        return subprocess.run(['bash', str(self.repo / 'scripts/create-github-repo.sh'), mode],
                              env=env, text=True, capture_output=True, timeout=15)

    def calls(self) -> list[list[str]]:
        p = self.state / 'calls.jsonl'
        return [json.loads(x) for x in p.read_text().splitlines()] if p.exists() else []

    def test_dry_run_has_no_remote_or_git_write(self) -> None:
        result = self.run_script(mode='--dry-run')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.calls())
        self.assertFalse((self.repo / '.git').exists())

    def test_success_commits_only_allowlist(self) -> None:
        (self.repo / 'private-extra.txt').write_text('Never publish this unlisted file.')
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        tracked = subprocess.check_output(['git', '-C', str(self.repo), 'ls-files'],
                                          text=True, env=self.env).splitlines()
        expected = [x for x in (self.repo / 'scripts/public-files.txt').read_text().splitlines()
                    if x and not x.startswith('#')]
        self.assertEqual(set(tracked), set(expected))
        self.assertIn('已核验公开仓库', result.stdout)
        self.assertEqual(sum(x[:2] == ['repo', 'create'] for x in self.calls()), 1)

    def test_wrong_account_stops_before_write(self) -> None:
        result = self.run_script('wronguser')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.repo / '.git').exists())
        self.assertFalse(any(x[:2] == ['repo', 'create'] for x in self.calls()))

    def test_existing_remote_is_not_touched(self) -> None:
        result = self.run_script('existing')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.repo / '.git').exists())
        self.assertFalse(any(x[:2] in (['repo', 'create'], ['repo', 'edit']) for x in self.calls()))

    def test_auth_failure_has_no_write(self) -> None:
        result = self.run_script('authfail')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.repo / '.git').exists())

    def test_create_failure_does_not_report_success(self) -> None:
        result = self.run_script('createfail')
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('已核验公开仓库', result.stdout)
        self.assertTrue((self.repo / '.git').exists())
        self.assertFalse(any(x[:2] == ['repo', 'edit'] for x in self.calls()))

    def test_sha_mismatch_fails_verification(self) -> None:
        result = self.run_script('wrongsha')
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('已核验公开仓库', result.stdout)

    def test_private_remote_fails_verification(self) -> None:
        result = self.run_script('wrongvisibility')
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('已核验公开仓库', result.stdout)

    def test_symlink_rejected_before_network(self) -> None:
        readme = self.repo / 'README.md'
        readme.unlink()
        readme.symlink_to(self.repo / 'LICENSE')
        result = self.run_script()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.calls())

    def test_existing_local_git_is_not_changed(self) -> None:
        subprocess.run(['git', '-C', str(self.repo), 'init'], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=self.env)
        result = self.run_script()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.calls())

if __name__ == '__main__':
    unittest.main()
