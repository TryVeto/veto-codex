"""Local regression checks only: these do not evaluate model steering or goal behavior."""
from __future__ import annotations
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import doctor

class WorkControlPackageTests(unittest.TestCase):
    def copy(self):
        tmp=tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        root=Path(tmp.name)/'plugin'; shutil.copytree(ROOT,root); return root
    def test_bounded_goal_strict_limit(self):
        root=self.copy(); (root/'templates/bounded-goal.md').write_text('x'*4000)
        self.assertTrue(any('Bounded goal' in e for e in doctor.run(root,verify_hashes=False)['errors']))
    def test_bounded_goal_required(self):
        root=self.copy(); (root/'templates/bounded-goal.md').unlink()
        self.assertTrue(any('Bounded goal' in e for e in doctor.run(root,verify_hashes=False)['errors']))
    def test_goal_count_is_unicode_characters_not_bytes(self):
        root=self.copy(); (root/'templates/bounded-goal.md').write_text('🧪'*3999)
        result=doctor.run(root,verify_hashes=False)
        self.assertEqual(result['bounded_goal_characters'],3999)
        self.assertFalse(any('Bounded goal' in e for e in result['errors']))
    def test_original_source_snapshot_bytes_match(self):
        self.assertEqual(doctor.check_source_snapshots(ROOT),[])
    def test_tampered_source_snapshot_detected(self):
        root=self.copy(); path=root/'research/source-skills/veto-primitives.source.txt'
        path.write_text(path.read_text()+'changed')
        self.assertTrue(any('hash mismatch' in e for e in doctor.check_source_snapshots(root)))
    def test_source_snapshot_cannot_escape_package(self):
        root=self.copy(); path=root/'research/next-inputs.json'; data=json.loads(path.read_text())
        data['inputs'][0]['packaged_snapshot']='../outside.txt'
        path.write_text(json.dumps(data))
        self.assertTrue(any('Invalid source' in e for e in doctor.check_source_snapshots(root)))
    def test_source_digest_must_be_sha256(self):
        root=self.copy(); path=root/'research/next-inputs.json'; data=json.loads(path.read_text())
        data['inputs'][0]['sha256']='not-a-hash'; path.write_text(json.dumps(data))
        self.assertTrue(any('digest' in e for e in doctor.check_source_snapshots(root)))
    def test_source_manifest_version_mismatch_detected(self):
        root=self.copy(); path=root/'research/next-inputs.json'; data=json.loads(path.read_text())
        data['release']='0.0.0';path.write_text(json.dumps(data))
        self.assertTrue(any('release mismatch' in e for e in doctor.check_source_snapshots(root)))

    def test_doctor_identifies_checked_package_not_runtime_loading(self):
        result=doctor.run(ROOT,verify_hashes=False)
        expected=json.loads((ROOT/'RELEASE.json').read_text())['version']
        self.assertEqual(result['package_version'],expected)
        self.assertEqual(Path(result['plugin_root']),ROOT.resolve())
        self.assertTrue(any('not instructions loaded' in x for x in result['limits']))

if __name__=='__main__': unittest.main()
