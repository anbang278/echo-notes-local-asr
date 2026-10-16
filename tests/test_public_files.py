"""Public-inventory boundary tests; fixtures never contain real credentials."""
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[1] / 'scripts/check_public_files.py'
SPEC = importlib.util.spec_from_file_location('public_check', MODULE)
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


class PublicInventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='asr-public-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'README.md').write_text('# Public project\n')

    def check(self, names):
        return CHECK.validate(self.root, names, check_git=False)

    def test_regular_file_accepted(self):
        self.assertEqual(self.check(['README.md']), [])

    def test_traversal_and_ambiguous_paths_rejected(self):
        for path in ['../secret', '/tmp/secret', './README.md', 'docs//x', 'a\\b', 'a\nb']:
            with self.subTest(path=path):
                self.assertTrue(self.check([path]))

    def test_duplicate_and_empty_inventory_rejected(self):
        self.assertTrue(self.check([]))
        self.assertTrue(self.check(['README.md', 'README.md']))

    def test_private_paths_rejected_before_read(self):
        for path in ['.env', '.env.local', 'models/weights.json', 'sample.wav',
                     '.trellis/.developer', '.trellis/workspace/person/journal.md',
                     'local-evidence/output.md', '本地ASR初始化.zip']:
            with self.subTest(path=path):
                self.assertTrue(any('Private material' in e for e in self.check([path])))

    def test_symlink_parent_rejected(self):
        (self.root / 'alias').symlink_to(self.root, target_is_directory=True)
        self.assertTrue(any('Symlink' in e for e in self.check(['alias/README.md'])))

    def test_secrets_and_owner_paths_rejected_without_echo(self):
        samples = ['gh' + 'p_' + 'X' * 32, '/' + 'Users/' + 'anbang/private/file']
        for sample in samples:
            (self.root / 'README.md').write_text(sample)
            errors = self.check(['README.md'])
            self.assertTrue(errors)
            self.assertNotIn(sample, '\n'.join(errors))

    def test_git_inventory_rejects_unlisted_tracked_file(self):
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        (self.root / 'extra.md').write_text('Unexpected tracked content')
        subprocess.run(['git', '-C', str(self.root), 'add', '.'], check=True)
        errors = CHECK.validate(self.root, ['README.md'])
        self.assertTrue(any('outside public inventory' in e for e in errors))


if __name__ == '__main__':
    unittest.main()
