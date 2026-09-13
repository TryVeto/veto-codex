"""Identity migration is local, conservative and read-only."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import migrate_catalog


def fixture():
    return {'name': 'existing-private-marketplace', 'interface': {'displayName': 'Keep Me'},
            'plugins': [
                {'name': 'other-tool', 'source': {'source': 'local', 'path': './plugins/other'},
                 'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'},
                 'category': 'Productivity'},
                {'name': 'veto-stack', 'source': {'source': 'local', 'path': './plugins/veto-stack'},
                 'policy': {'installation': 'NOT_AVAILABLE', 'authentication': 'ON_INSTALL'},
                 'category': 'Developer Tools', 'annotations': {'owner': 'Veto'}}]}


class MigrationTests(unittest.TestCase):
    def test_one_entry_renamed(self):
        result = migrate_catalog.plan(fixture())
        self.assertEqual(result['verdict'], 'MIGRATION_PLAN')
        self.assertEqual([p['name'] for p in result['proposed_catalog']['plugins']], ['other-tool', 'veto-codex'])

    def test_source_is_updated(self):
        entry = migrate_catalog.plan(fixture())['proposed_catalog']['plugins'][1]
        self.assertEqual(entry['source'], {'source': 'local', 'path': './plugins/veto-codex'})

    def test_does_not_mutate_input(self):
        value = fixture(); before = deepcopy(value)
        migrate_catalog.plan(value)
        self.assertEqual(value, before)

    def test_preserves_unrelated_plugin(self):
        value = fixture()
        self.assertEqual(migrate_catalog.plan(value)['proposed_catalog']['plugins'][0], value['plugins'][0])

    def test_preserves_existing_marketplace_identity(self):
        result = migrate_catalog.plan(fixture())['proposed_catalog']
        self.assertEqual(result['name'], 'existing-private-marketplace')
        self.assertEqual(result['interface'], {'displayName': 'Keep Me'})

    def test_preserves_install_policy_without_elevation(self):
        value = fixture()
        result = migrate_catalog.plan(value)['proposed_catalog']['plugins'][1]
        self.assertEqual(result['policy'], value['plugins'][1]['policy'])
        self.assertEqual(result['annotations'], {'owner': 'Veto'})

    def test_idempotent_on_proposed_catalog(self):
        first = migrate_catalog.plan(fixture())['proposed_catalog']
        result = migrate_catalog.plan(first)
        self.assertEqual(result['verdict'], 'NO_CHANGE')
        self.assertEqual(result['proposed_catalog'], first)

    def test_corrects_renamed_entry_with_old_path(self):
        value = fixture(); value['plugins'][1]['name'] = 'veto-codex'
        result = migrate_catalog.plan(value)
        self.assertEqual(result['verdict'], 'MIGRATION_PLAN')
        self.assertEqual(result['proposed_catalog']['plugins'][1]['source']['path'], './plugins/veto-codex')

    def test_rejects_two_identities(self):
        value = fixture(); extra = deepcopy(value['plugins'][1]); extra['name'] = 'veto-codex'
        value['plugins'].append(extra)
        with self.assertRaisesRegex(ValueError, 'Both identities'): migrate_catalog.plan(value)

    def test_rejects_duplicate_entries(self):
        value = fixture(); value['plugins'].append(deepcopy(value['plugins'][1]))
        with self.assertRaisesRegex(ValueError, 'Duplicate'): migrate_catalog.plan(value)

    def test_missing_old_and_new_is_not_new_install(self):
        value = fixture(); value['plugins'].pop()
        with self.assertRaisesRegex(ValueError, 'not an upgrade'): migrate_catalog.plan(value)

    def test_workspace_id_not_transferred(self):
        value = fixture(); value['plugins'][1]['pluginId'] = 'workspace-record'
        with self.assertRaisesRegex(ValueError, 'Workspace'): migrate_catalog.plan(value)

    def test_remote_source_not_changed(self):
        value = fixture(); value['plugins'][1]['source'] = {'source': 'git-subdir', 'url': 'https://example.test/repo'}
        with self.assertRaisesRegex(ValueError, 'local source'): migrate_catalog.plan(value)

    def test_string_source_retains_shape(self):
        value = fixture(); value['plugins'][1]['source'] = './old-plugin'
        self.assertEqual(migrate_catalog.plan(value)['proposed_catalog']['plugins'][1]['source'], './plugins/veto-codex')

    def test_custom_target_path(self):
        result = migrate_catalog.plan(fixture(), './.codex/plugins/veto-codex')
        self.assertEqual(result['proposed_catalog']['plugins'][1]['source']['path'], './.codex/plugins/veto-codex')

    def test_rejects_unsafe_target_paths(self):
        for target in ['/tmp/source', '../source', './x/../../y', './', './a//b', './a/./b', './x\\y', './https:x', './%2e%2e/x', './x\n', 3]:
            with self.subTest(target=target), self.assertRaises(ValueError):
                migrate_catalog.plan(fixture(), target)

    def test_source_metadata_preserved(self):
        value = fixture(); value['plugins'][1]['source']['custom'] = 'retained'
        self.assertEqual(migrate_catalog.plan(value)['proposed_catalog']['plugins'][1]['source']['custom'], 'retained')

    def test_bad_catalog_shapes(self):
        for value in [[], {}, {'name': 'x', 'plugins': []}, {'name': 'x', 'plugins': ['bad']}, {'name': 'x', 'plugins': [{'name': ''}]}]:
            with self.subTest(value=value), self.assertRaises(ValueError): migrate_catalog.plan(value)

    def test_secret_like_fields_refused_without_echo(self):
        value = fixture(); value['plugins'][0]['api_key'] = 'sensitive-test-content'
        with self.assertRaisesRegex(ValueError, 'Secret-like') as error: migrate_catalog.plan(value)
        self.assertNotIn('sensitive-test-content', str(error.exception))

    def test_explicit_no_side_effects(self):
        result = migrate_catalog.plan(fixture())
        self.assertFalse(result['writes_performed'])
        self.assertFalse(result['native_installation_changed'])
        self.assertEqual(len(result['source_catalog_sha256']), 64)

    def test_cli_reads_without_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'marketplace.json'; path.write_text(json.dumps(fixture()))
            before = path.read_bytes()
            result = subprocess.run([sys.executable, '-B', str(ROOT / 'tools/migrate_catalog.py'), '--catalog', str(path)], text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)['verdict'], 'MIGRATION_PLAN')
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(list(Path(directory).iterdir()), [path])

    def test_cli_duplicate_json_keys_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'marketplace.json'; path.write_text('{"name":"a","name":"b","plugins":[]}')
            result = subprocess.run([sys.executable, '-B', str(ROOT / 'tools/migrate_catalog.py'), '--catalog', str(path)], text=True, capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)['verdict'], 'BLOCKED')

    def test_readonly_tool_has_no_apply_mode(self):
        result = subprocess.run([sys.executable, '-B', str(ROOT / 'tools/migrate_catalog.py'), '--help'], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertNotIn('--apply', result.stdout)
        self.assertIn('--source-path', result.stdout)


if __name__ == '__main__': unittest.main()
