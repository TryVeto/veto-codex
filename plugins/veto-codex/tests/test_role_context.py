"""Portable role content checks, not a simulation of native agent behavior."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import role_context as rc


class RoleContextTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)/'plugin'
        shutil.copytree(ROOT, self.root)
        self.role = 'backend-engineer'

    def tearDown(self):
        self.temp.cleanup()

    def reseal(self, rel):
        p = self.root/'FILES.sha256.json'
        data = json.loads(p.read_text())
        data[rel] = hashlib.sha256((self.root/rel).read_bytes()).hexdigest()
        p.write_text(json.dumps(data))

    def registry_change(self, change):
        p = self.root/'team/roles.json'
        data = json.loads(p.read_text()); change(data)
        p.write_text(json.dumps(data)); self.reseal('team/roles.json')

    def test_all_nine_roles_prepare(self):
        registry, _, _ = rc.catalog(self.root)
        self.assertEqual(len(registry['roles']), 9)
        for role in registry['roles']:
            with self.subTest(role=role):
                result = rc.prepare(self.root, role)
                self.assertEqual(result['role_id'], role)
                self.assertEqual(len(result['sources']), 3)

    def test_deterministic_packet(self):
        self.assertEqual(rc.prepare(self.root,self.role),rc.prepare(self.root,self.role))

    def test_packet_never_grants_runtime_or_independence(self):
        p = rc.prepare(self.root,'independent-verifier')
        for k in ['runtime_changed','authority_granted','ownership_transferred',
                  'native_loading_verified','independent_review_established']:
            self.assertIs(p[k], False)
        self.assertNotIn('model',p)
        self.assertNotIn('credentials',p)

    def test_sources_equal_actual_bytes(self):
        for s in rc.prepare(self.root,self.role)['sources']:
            self.assertEqual(s['content'],(self.root/s['path']).read_text())
            self.assertEqual(s['sha256'],hashlib.sha256((self.root/s['path']).read_bytes()).hexdigest())

    def test_role_context_fingerprint_changes_with_approved_role_change(self):
        old = rc.prepare(self.root,self.role)['role_context_sha256']
        rel = 'team/backend-engineer/AGENTS.md'
        with (self.root/rel).open('a') as stream: stream.write('\nA scoped example.\n')
        self.reseal(rel)
        self.assertNotEqual(old,rc.prepare(self.root,self.role)['role_context_sha256'])

    def test_unknown_named_identity_rejected(self):
        with self.assertRaises(ValueError): rc.prepare(self.root,'lunentic')

    def test_role_id_cannot_be_path(self):
        for name in ['../backend-engineer','/tmp/role','backend/engineer','backend_engineer','', 'Backend']:
            with self.subTest(name=name),self.assertRaises(ValueError): rc.prepare(self.root,name)

    def test_role_path_escape_rejected(self):
        self.registry_change(lambda d:d['roles'][self.role].update(path='../../outside.md'))
        with self.assertRaises(ValueError): rc.prepare(self.root,self.role)

    def test_role_path_cannot_borrow_verifier(self):
        self.registry_change(lambda d:d['roles'][self.role].update(path='team/independent-verifier/AGENTS.md'))
        with self.assertRaises(ValueError): rc.prepare(self.root,self.role)

    def test_extra_authority_field_rejected(self):
        self.registry_change(lambda d:d['roles'][self.role].update(authority='production'))
        with self.assertRaises(ValueError): rc.prepare(self.root,self.role)

    def test_shared_sources_cannot_be_replaced(self):
        self.registry_change(lambda d:d.update(shared=['team/backend-engineer/AGENTS.md']))
        with self.assertRaises(ValueError): rc.prepare(self.root,self.role)

    def test_registry_hash_mismatch_rejected(self):
        with (self.root/'team/roles.json').open('a') as stream: stream.write(' ')
        with self.assertRaises(ValueError): rc.prepare(self.root,self.role)

    def test_role_hash_mismatch_rejected(self):
        with (self.root/'team/backend-engineer/AGENTS.md').open('a') as stream: stream.write(' ')
        with self.assertRaises(ValueError): rc.prepare(self.root,self.role)

    def test_shared_hash_mismatch_rejected(self):
        with (self.root/'team/SHARED.md').open('a') as stream: stream.write(' ')
        with self.assertRaises(ValueError): rc.prepare(self.root,self.role)

    def test_independent_manifest_pin(self):
        pin = hashlib.sha256((self.root/'FILES.sha256.json').read_bytes()).hexdigest()
        self.assertEqual(rc.prepare(self.root,self.role,pin)['plugin_manifest_sha256'],pin)
        with self.assertRaises(ValueError): rc.prepare(self.root,self.role,'0'*64)

    def test_invalid_manifest_pin_rejected(self):
        with self.assertRaises(ValueError): rc.prepare(self.root,self.role,'a-hash')

    def test_symlink_role_rejected(self):
        p = self.root/'team/backend-engineer/AGENTS.md'
        original = p.read_bytes(); p.unlink()
        target = Path(self.temp.name)/'outside.md';target.write_bytes(original);p.symlink_to(target)
        with self.assertRaises(ValueError): rc.prepare(self.root,self.role)

    def test_root_symlink_rejected(self):
        alias = Path(self.temp.name)/'alias';alias.symlink_to(self.root,target_is_directory=True)
        with self.assertRaises(ValueError): rc.prepare(alias,self.role)

    def test_empty_source_rejected(self):
        rel='team/backend-engineer/AGENTS.md';(self.root/rel).write_text('   ');self.reseal(rel)
        with self.assertRaises(ValueError): rc.prepare(self.root,self.role)

    def test_oversized_source_rejected(self):
        rel='team/backend-engineer/AGENTS.md';(self.root/rel).write_text('x'*(rc.MAX_TEXT_BYTES+1));self.reseal(rel)
        with self.assertRaises(ValueError): rc.prepare(self.root,self.role)

    def test_duplicate_json_key_rejected(self):
        rel='team/roles.json';(self.root/rel).write_text('{"schema_version":1,"schema_version":1}')
        self.reseal(rel)
        with self.assertRaises(ValueError): rc.prepare(self.root,self.role)

    def test_versions_must_agree(self):
        rel='RELEASE.json';p=self.root/rel;d=json.loads(p.read_text());d['version']='0.0.0';p.write_text(json.dumps(d));self.reseal(rel)
        with self.assertRaises(ValueError): rc.prepare(self.root,self.role)

    def test_boolean_schema_is_not_integer_version(self):
        self.registry_change(lambda d:d.update(schema_version=True))
        with self.assertRaises(ValueError): rc.prepare(self.root,self.role)

    def test_missing_manifest_entry_rejected(self):
        p=self.root/'FILES.sha256.json';d=json.loads(p.read_text());del d['team/SHARED.md'];p.write_text(json.dumps(d))
        with self.assertRaises(ValueError): rc.prepare(self.root,self.role)

    def test_no_file_writes(self):
        def state():
            return {str(p.relative_to(self.root)):hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in self.root.rglob('*') if p.is_file()}
        before=state();rc.prepare(self.root,self.role);self.assertEqual(before,state())


if __name__ == '__main__': unittest.main()
