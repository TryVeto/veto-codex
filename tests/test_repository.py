"""Local source-release behavior; no native host or CI-service claims."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch
import zipfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import repo


class RepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)/'source';self.root.mkdir()
        (self.root/'README.md').write_text('# Example\n')

    def tearDown(self): self.temp.cleanup()

    def test_zip_is_deterministic(self):
        a=Path(self.temp.name)/'one.zip';b=Path(self.temp.name)/'two.zip'
        repo.write_zip(self.root,a);repo.write_zip(self.root,b)
        self.assertEqual(a.read_bytes(),b.read_bytes())

    def test_dot_directories_preserved(self):
        p=self.root/'.agents/plugins/marketplace.json';p.parent.mkdir(parents=True);p.write_text('{}')
        out=Path(self.temp.name)/'one.zip';repo.write_zip(self.root,out)
        with zipfile.ZipFile(out) as z:self.assertIn('veto-codex/.agents/plugins/marketplace.json',z.namelist())

    def test_cache_git_and_dist_excluded(self):
        for folder in ['.git','dist','.artifacts','__pycache__']:
            p=self.root/folder;p.mkdir();(p/'output').write_text('not source')
        self.assertEqual([p.name for p in repo.inventory(self.root)],['README.md'])

    def test_symlink_file_refused(self):
        (self.root/'alias.md').symlink_to(self.root/'README.md')
        with self.assertRaises(ValueError):repo.inventory(self.root)

    def test_symlink_directory_refused(self):
        (self.root/'linked').symlink_to(Path(self.temp.name),target_is_directory=True)
        with self.assertRaises(ValueError):repo.inventory(self.root)

    def test_no_overwrite(self):
        out=Path(self.temp.name)/'one.zip';out.write_bytes(b'preserve')
        with self.assertRaises(ValueError):repo.write_zip(self.root,out)
        self.assertEqual(out.read_bytes(),b'preserve')

    def test_sorted_paths_and_one_root(self):
        (self.root/'z').write_text('z');(self.root/'a').write_text('a')
        out=Path(self.temp.name)/'one.zip';repo.write_zip(self.root,out)
        with zipfile.ZipFile(out) as z:
            self.assertEqual(z.namelist(),sorted(z.namelist()))
            self.assertTrue(all(n.startswith('veto-codex/') for n in z.namelist()))

    def test_packaged_bytes_equal_sources(self):
        out=Path(self.temp.name)/'one.zip';repo.write_zip(self.root,out)
        with zipfile.ZipFile(out) as z:self.assertEqual(z.read('veto-codex/README.md'),(self.root/'README.md').read_bytes())

    def test_normalized_zip_metadata(self):
        out=Path(self.temp.name)/'one.zip';repo.write_zip(self.root,out)
        with zipfile.ZipFile(out) as z:
            i=z.infolist()[0]
            self.assertEqual(i.date_time,(2026,9,12,0,0,0))
            self.assertEqual((i.external_attr>>16)&0o777,0o644)

    def test_link_errors_identify_missing_path(self):
        p=self.root/'README.md';p.write_text('[no](missing.md)')
        self.assertTrue(repo.local_link_errors(self.root,[p]))

    def test_link_escape_detected(self):
        p=self.root/'README.md';p.write_text('[no](../outside.md)')
        self.assertTrue(repo.local_link_errors(self.root,[p]))

    def test_encoded_link_escape_detected(self):
        p=self.root/'README.md';p.write_text('[no](%2e%2e/outside.md)')
        self.assertTrue(repo.local_link_errors(self.root,[p]))

    def test_external_link_not_fetched(self):
        p=self.root/'README.md';p.write_text('[docs](https://example.com)')
        self.assertEqual(repo.local_link_errors(self.root,[p]),[])

    def test_manifest_excludes_itself(self):
        (self.root/'SOURCE-MANIFEST.json').write_text('{}')
        result=repo.source_map(self.root,exclude='SOURCE-MANIFEST.json')
        self.assertEqual(set(result),{'README.md'})

    def test_manifest_changes_with_source(self):
        a=repo.source_map(self.root,exclude='NONE')
        (self.root/'README.md').write_text('different')
        self.assertNotEqual(a,repo.source_map(self.root,exclude='NONE'))

    def test_output_cannot_pollute_source(self):
        with self.assertRaisesRegex(ValueError,'dist'):
            repo.package(self.root,self.root/'releases')

    def test_output_symlink_refused(self):
        link=Path(self.temp.name)/'link';link.symlink_to(self.root,target_is_directory=True)
        with self.assertRaisesRegex(ValueError,'symlink'):
            repo.package(self.root,link/'new')

    def test_invalid_source_prevents_package_tests(self):
        with patch.object(repo,'check',return_value={'errors':['bad input']}),patch.object(repo,'test') as run:
            with self.assertRaisesRegex(ValueError,'bad input'):
                repo.package(self.root,Path(self.temp.name)/'out')
            run.assert_not_called()

    def test_failed_tests_prevent_archive(self):
        out=Path(self.temp.name)/'out'
        with patch.object(repo,'check',return_value={'errors':[],'version':'1.0.0'}),patch.object(repo,'test',side_effect=ValueError('test failed')):
            with self.assertRaisesRegex(ValueError,'test failed'):repo.package(self.root,out)
        self.assertFalse(out.exists())

    def test_mutated_source_after_tests_prevents_archive(self):
        out=Path(self.temp.name)/'out'
        with patch.object(repo,'check',side_effect=[{'errors':[],'version':'1.0.0'},{'errors':['changed']}]),patch.object(repo,'test'):
            with self.assertRaisesRegex(ValueError,'changed'):repo.package(self.root,out)
        self.assertFalse(out.exists())

    def test_existing_sidecar_prevents_testing_and_overwrite(self):
        out=Path(self.temp.name)/'out';out.mkdir()
        p=out/'veto-codex-repo-1.0.0.zip.sha256';p.write_text('keep')
        with patch.object(repo,'check',return_value={'errors':[],'version':'1.0.0'}),patch.object(repo,'test') as run:
            with self.assertRaises(ValueError):repo.package(self.root,out)
            run.assert_not_called()
        self.assertEqual(p.read_text(),'keep')

    def test_native_example_is_inert_and_explicit(self):
        doc=tomllib.loads((ROOT/'examples/codex/veto-reader.toml').read_text())
        self.assertEqual(doc['model'],'gpt-5.6-luna')
        self.assertEqual(doc['model_reasoning_effort'],'medium')
        self.assertEqual(doc['sandbox_mode'],'read-only')
        self.assertTrue(doc['developer_instructions'])
        self.assertFalse((ROOT/'.codex').exists())

    def test_native_qualification_stays_unrun(self):
        d=json.loads((ROOT/'examples/native-qualification.json').read_text())
        self.assertEqual(d['status'],'unrun')
        self.assertTrue(all(v['status']=='unrun' for v in d['checks'].values()))
        self.assertIsNone(d['observed_total_cost'])

    def test_repository_identity_matches_plugin(self):
        d=json.loads((ROOT/'REPOSITORY.json').read_text())
        p=json.loads((ROOT/'plugins/veto-codex/plugin.json').read_text())
        self.assertEqual(d['name'],p['name']);self.assertEqual(d['version'],p['version'])


if __name__=='__main__':unittest.main()
