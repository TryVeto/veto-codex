"""The rename has one active identity and does not silently extend host authority."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins/veto-codex'
sys.path.insert(0, str(PLUGIN / 'scripts'))
import doctor


class RenameContractTests(unittest.TestCase):
    def test_one_plugin_one_entry(self):
        self.assertFalse((ROOT / 'plugins/veto-stack').exists())
        self.assertFalse((PLUGIN / 'skills/veto-stack').exists())
        self.assertTrue((PLUGIN / 'skills/veto-codex/SKILL.md').is_file())
        self.assertEqual(len(list(PLUGIN.glob('skills/*/SKILL.md'))), 13)

    def test_three_manifests_same_identity(self):
        for name in ['plugin.json', '.codex-plugin/plugin.json', '.claude-plugin/plugin.json']:
            value = json.loads((PLUGIN / name).read_text())
            self.assertEqual(value['name'], 'veto-codex')
            self.assertEqual(value['version'], '2026.9.1203')

    def test_marketplace_preserves_name(self):
        value = json.loads((ROOT / '.agents/plugins/marketplace.json').read_text())
        self.assertEqual(value['name'], 'veto-team')
        self.assertEqual([v['name'] for v in value['plugins']], ['veto-codex'])

    def test_no_automatic_authority_changes(self):
        value = json.loads((PLUGIN / 'RELEASE.json').read_text())
        self.assertEqual(value['external_services'], [])
        self.assertEqual(value['automatic_hooks'], [])
        self.assertFalse(value['native_host_installation_tested'])
        self.assertFalse((ROOT / '.codex').exists())

    def test_old_and_new_catalog_entries_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); plugin = root / 'plugins/veto-codex'; plugin.mkdir(parents=True)
            catalog = root / '.agents/plugins/marketplace.json'; catalog.parent.mkdir(parents=True)
            entries = [{'name': name, 'source': {'source': 'local', 'path': './plugins/' + name}}
                       for name in ['veto-stack', 'veto-codex']]
            catalog.write_text(json.dumps({'name': 'test', 'plugins': entries}))
            errors, _ = doctor.check_enclosing_marketplace(plugin, 'veto-codex')
            self.assertTrue(any('both discoverable' in e for e in errors))

    def test_integrated_candidate_requirement_in_execution_path(self):
        for name in ['playbooks/finish-and-handoff.md', 'references/application-verification.md']:
            text = (PLUGIN / name).read_text()
            self.assertIn('patch-id', text)
            self.assertIn('replay', text)
            self.assertIn('integrated', text)

    def test_separate_chatgpt_scope_is_explicit(self):
        text = (ROOT / 'docs/guide/explanation/scope.md').read_text()
        self.assertIn('ChatGPT web setup', text)
        self.assertIn('does not rename it', text)
        self.assertIn('payment authority', text)


if __name__ == '__main__': unittest.main()
