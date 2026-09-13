"""Synthetic helper tests. These are not product reviews or agent performance runs."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import zipfile
import zlib

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import review_pack
from common import digest


def png():
    def chunk(kind, data):
        return struct.pack('!I', len(data)) + kind + data + struct.pack('!I', zlib.crc32(kind + data) & 0xffffffff)
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('!IIBBBBB', 2, 2, 8, 2, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(b'\0\0\0\0\0\0\0' * 2)) + chunk(b'IEND', b'')


class ReviewPackTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base / 'materials'
        self.root.mkdir()
        self.rp, self.mp = self.base/'request.json', self.base/'manifest.json'
        self.c = {'id': 'synthetic-candidate-01', 'environment': 'disposable-unit-fixture'}
        self.req = {'schema_version': 1, 'review_id': 'synthetic-review-01', 'candidate': self.c,
                    'task': 'Inspect fixture packaging only.', 'fixed_constraints': ['No external effects.'],
                    'required_states': ['ordinary', 'repair'], 'require_source': True, 'require_runtime_identity': True}
        self.m = {'schema_version': 1, 'review_id': self.req['review_id'], 'request_sha256': '', 'candidate': self.c,
                  'purpose': 'Synthetic helper exercise, not a real app.',
                  'served_build': {'status': 'known', 'identity': 'synthetic-only', 'observation': 'No actual server; declared test metadata.'},
                  'source_description': 'Synthetic source stub, not runnable product evidence.',
                  'sanitization': {'status': 'reviewed', 'reviewer': 'unit-fixture', 'note': 'Only generated synthetic bytes.'},
                  'files': [], 'states': []}
        self.addfile('source/app.txt', 'source', b'Synthetic source; not a product.')
        self.addfile('images/ordinary.png', 'screenshot', png())
        self.addfile('images/repair.png', 'screenshot', png())
        self.addfile('evidence/observed.txt', 'evidence', b'Synthetic record: packaging only.')
        for sid in self.req['required_states']:
            self.m['states'].append({'id': sid, 'scenario': 'synthetic-v1', 'role': 'test-role', 'route': '/'+sid,
                                     'viewport': [390, 844], 'status': 'captured', 'screenshot': 'images/'+sid+'.png',
                                     'evidence': ['evidence/observed.txt'], 'candidate_id': self.c['id'],
                                     'reason': 'Synthetic image validates format handling only.'})
        self.save()

    def addfile(self, rel, kind, data):
        p=self.root/rel; p.parent.mkdir(parents=True, exist_ok=True);p.write_bytes(data)
        self.m['files'].append({'path':rel,'kind':kind,'sha256':hashlib.sha256(data).hexdigest(),'candidate_id':self.c['id']})

    def save(self):
        self.rp.write_text(json.dumps(self.req))
        self.pin=digest(self.rp)
        self.m['request_sha256']=self.pin
        self.mp.write_text(json.dumps(self.m))

    def check(self):
        return review_pack.inspect_pack(self.root,self.rp,self.pin,self.mp)[0]

    def invalid(self):
        self.save()
        with self.assertRaises((ValueError, OSError)):
            self.check()

    def test_complete_is_materials_not_acceptance(self):
        r=self.check(); self.assertEqual(r['verdict'],'REVIEW_PACK_COMPLETE')
        self.assertTrue(any('not product acceptance' in s for s in r['limits']))

    def test_missing_required_state_is_partial(self):
        self.m['states'].pop();self.save();r=self.check()
        self.assertEqual(r['verdict'],'REVIEW_PACK_PARTIAL');self.assertTrue(any('repair' in g for g in r['gaps']))

    def test_blocked_is_partial_not_success(self):
        self.m['states'][1].update(status='blocked',screenshot=None,reason='Allowed browser unavailable.')
        self.save();self.assertEqual(self.check()['verdict'],'REVIEW_PACK_PARTIAL')

    def test_required_na_cannot_waive_request(self):
        self.m['states'][1].update(status='not_applicable',screenshot=None)
        self.save();self.assertEqual(self.check()['verdict'],'REVIEW_PACK_PARTIAL')

    def test_blocked_cannot_claim_screenshot(self):
        self.m['states'][0]['status']='blocked';self.invalid()

    def test_duplicate_states_invalid(self):
        self.m['states'].append(copy.deepcopy(self.m['states'][0]));self.invalid()

    def test_extra_states_do_not_replace_missing_required(self):
        self.m['states'][1]['id']='different';self.save()
        self.assertEqual(self.check()['verdict'],'REVIEW_PACK_PARTIAL')

    def test_unknown_status_invalid(self):
        self.m['states'][0]['status']='passed';self.invalid()

    def test_stale_capture_invalid(self):
        self.m['states'][0]['candidate_id']='old';self.invalid()

    def test_stale_file_invalid(self):
        self.m['files'][0]['candidate_id']='old';self.invalid()

    def test_environment_mismatch_invalid(self):
        self.m['candidate']=dict(self.c,environment='production');self.invalid()

    def test_request_pin_blocks_scope_change(self):
        pin=self.pin;self.req['required_states'].pop();self.save()
        with self.assertRaises(ValueError):
            review_pack.inspect_pack(self.root,self.rp,pin,self.mp)

    def test_digest_mismatch_invalid(self):
        (self.root/'images/ordinary.png').write_bytes(b'changed')
        with self.assertRaises(ValueError):self.check()

    def test_missing_file_invalid_not_silently_skipped(self):
        (self.root/'images/ordinary.png').unlink()
        with self.assertRaises(OSError):self.check()

    def test_empty_source_invalid(self):
        (self.root/'source/app.txt').write_bytes(b'');self.m['files'][0]['sha256']=hashlib.sha256(b'').hexdigest();self.invalid()

    def test_disguised_text_is_not_screenshot(self):
        f=self.root/'images/ordinary.png';f.write_text('not an image')
        self.m['files'][1]['sha256']=digest(f);self.invalid()

    def test_svg_is_not_allowed_capture(self):
        self.addfile('images/a.svg','screenshot',b'<svg/>');self.invalid()

    def test_capture_reference_must_be_neutral(self):
        self.m['files'][1]['kind']='feedback';self.invalid()

    def test_evidence_reference_must_be_evidence(self):
        self.m['states'][0]['evidence']=['source/app.txt'];self.invalid()

    def test_duplicate_evidence_reference_invalid(self):
        self.m['states'][0]['evidence'] *= 2;self.invalid()

    def test_zero_viewport_invalid(self):
        self.m['states'][0]['viewport']=[0,844];self.invalid()

    def test_boolean_viewport_invalid(self):
        self.m['states'][0]['viewport']=[True,844];self.invalid()

    def test_duplicate_file_invalid(self):
        self.m['files'].append(copy.deepcopy(self.m['files'][0]));self.invalid()

    def test_case_collision_invalid(self):
        self.addfile('source/APP.txt','source',b'case collision');self.invalid()

    def test_symlink_file_invalid(self):
        f=self.root/'source/app.txt';f.unlink();f.symlink_to(self.rp)
        with self.assertRaises(ValueError):self.check()

    def test_symlink_parent_invalid(self):
        target=self.base/'outside';target.mkdir();(target/'x.txt').write_text('not authorized')
        (self.root/'linked').symlink_to(target,target_is_directory=True)
        self.m['files'].append({'path':'linked/x.txt','kind':'source','sha256':digest(target/'x.txt'),'candidate_id':self.c['id']})
        self.invalid()

    def test_path_traversal_invalid(self):
        self.m['files'][0]['path']='../outside.txt';self.invalid()

    def test_noncanonical_path_invalid(self):
        self.m['files'][0]['path']='source//app.txt';self.invalid()

    def test_control_character_path_invalid(self):
        self.m['files'][0]['path']='source/\napp.txt';self.invalid()

    def test_env_path_invalid(self):
        self.addfile('.env.example','source',b'not even examples auto-share');self.invalid()

    def test_dependency_path_invalid(self):
        self.addfile('node_modules/a.txt','source',b'dependency');self.invalid()

    def test_font_path_invalid(self):
        self.addfile('assets/font.woff2','source',b'not a font');self.invalid()

    def test_database_path_invalid(self):
        self.addfile('data/app.sqlite','source',b'not a database');self.invalid()

    def test_private_key_path_invalid(self):
        self.addfile('config/test.pem','source',b'not an actual key');self.invalid()

    def test_unlisted_files_never_exported(self):
        (self.root/'.env').write_text('SYNTHETIC=not-to-include')
        out=self.base/'output.zip';review_pack.build_pack(self.root,self.rp,self.pin,self.mp,out)
        with zipfile.ZipFile(out) as z:self.assertFalse(any('.env' in x for x in z.namelist()))

    def test_not_reviewed_cannot_build(self):
        self.m['sanitization']['status']='not_reviewed';self.save()
        self.assertEqual(self.check()['verdict'],'REVIEW_PACK_PARTIAL')
        with self.assertRaises(ValueError):review_pack.build_pack(self.root,self.rp,self.pin,self.mp,self.base/'unsafe.zip')
        self.assertFalse((self.base/'unsafe.zip').exists())

    def test_unknown_build_retains_gap(self):
        self.m['served_build']['status']='unknown';self.save()
        self.assertEqual(self.check()['verdict'],'REVIEW_PACK_PARTIAL')

    def test_noninteractive_review_need_not_claim_build(self):
        self.req['require_runtime_identity']=False;self.m['served_build']['status']='unknown';self.save()
        self.assertEqual(self.check()['verdict'],'REVIEW_PACK_COMPLETE')

    def test_source_required_is_not_satisfied_by_reference(self):
        self.m['files'].pop(0);self.save()
        self.assertEqual(self.check()['verdict'],'REVIEW_PACK_PARTIAL')

    def test_source_not_required_can_use_accessible_reference(self):
        self.req['require_source']=False;self.m['files'].pop(0);self.save()
        self.assertEqual(self.check()['verdict'],'REVIEW_PACK_COMPLETE')

    def test_invalid_schema_bool(self):
        self.req['schema_version']=True;self.invalid()

    def test_duplicate_json_keys_invalid(self):
        self.mp.write_text('{"schema_version":1,"schema_version":1}')
        with self.assertRaises(ValueError):self.check()

    def test_no_empty_required_state_scope(self):
        self.req['required_states']=[];self.invalid()

    def test_unknown_request_fields_invalid(self):
        self.req['skip_safety']=True;self.invalid()

    def test_local_check_does_not_mutate(self):
        paths=[self.rp,self.mp,*[p for p in self.root.rglob('*') if p.is_file()]]
        before={str(p):digest(p) for p in paths};self.check()
        self.assertEqual(before,{str(p):digest(p) for p in paths})

    def test_existing_output_never_overwritten(self):
        out=self.base/'existing.zip';out.write_bytes(b'keep')
        with self.assertRaises(ValueError):review_pack.build_pack(self.root,self.rp,self.pin,self.mp,out)
        self.assertEqual(out.read_bytes(),b'keep')

    def test_neutral_pack_omits_feedback(self):
        self.addfile('feedback/founder.txt','feedback',b'Founder favors the wrong thing (synthetic).');self.save()
        out=self.base/'neutral.zip';r=review_pack.build_pack(self.root,self.rp,self.pin,self.mp,out)
        self.assertEqual(r['feedback_omitted_count'],1)
        with zipfile.ZipFile(out) as z:
            self.assertFalse(any('founder.txt' in x for x in z.namelist()))
            m=json.loads(z.read('review-pack/manifest.json'))
            self.assertFalse(any(f['kind']=='feedback' for f in m['files']))

    def test_later_pack_can_include_feedback_explicitly(self):
        self.addfile('feedback/founder.txt','feedback',b'Synthetic later opinion.');self.save()
        out=self.base/'informed.zip';review_pack.build_pack(self.root,self.rp,self.pin,self.mp,out,include_feedback=True)
        with zipfile.ZipFile(out) as z:self.assertTrue(any('founder.txt' in x for x in z.namelist()))

    def test_partial_pack_can_be_shared_as_partial(self):
        self.m['states'].pop();self.save();out=self.base/'partial.zip'
        r=review_pack.build_pack(self.root,self.rp,self.pin,self.mp,out)
        self.assertEqual(r['verdict'],'REVIEW_PACK_PARTIAL');self.assertTrue(out.exists())
        with zipfile.ZipFile(out) as z:self.assertIn(b'REVIEW_PACK_PARTIAL',z.read('review-pack/README.md'))

    def test_fresh_extracted_pack_rechecks(self):
        self.addfile('feedback/founder.txt','feedback',b'Synthetic opinion.');self.save()
        out=self.base/'pack.zip';review_pack.build_pack(self.root,self.rp,self.pin,self.mp,out)
        extract=self.base/'fresh';extract.mkdir()
        with zipfile.ZipFile(out) as z:z.extractall(extract)
        root=extract/'review-pack'
        r=review_pack.inspect_pack(root/'payload',root/'request.json',self.pin,root/'manifest.json')[0]
        self.assertEqual(r['verdict'],'REVIEW_PACK_COMPLETE')

    def test_archive_reproducible_for_identical_inputs(self):
        a,b=self.base/'a.zip',self.base/'b.zip'
        review_pack.build_pack(self.root,self.rp,self.pin,self.mp,a)
        review_pack.build_pack(self.root,self.rp,self.pin,self.mp,b)
        self.assertEqual(digest(a),digest(b))

    def test_html_escapes_untrusted_metadata(self):
        self.req['task']='<script>bad()</script>';self.save();r,req,m=review_pack.inspect_pack(self.root,self.rp,self.pin,self.mp)
        text=review_pack.index_html(req,m,r)
        self.assertNotIn('<script>',text);self.assertIn('&lt;script&gt;',text);self.assertIn("default-src 'none'",text)

    def test_cli_complete_exit_zero(self):
        result=subprocess.run([sys.executable,'-B',str(ROOT/'scripts/review_pack.py'),'check','--root',str(self.root),'--request',str(self.rp),'--request-sha256',self.pin,'--manifest',str(self.mp)],capture_output=True,text=True)
        self.assertEqual(result.returncode,0);self.assertEqual(json.loads(result.stdout)['verdict'],'REVIEW_PACK_COMPLETE')

    def test_cli_partial_exit_one(self):
        self.m['states'].pop();self.save()
        result=subprocess.run([sys.executable,'-B',str(ROOT/'scripts/review_pack.py'),'check','--root',str(self.root),'--request',str(self.rp),'--request-sha256',self.pin,'--manifest',str(self.mp)],capture_output=True,text=True)
        self.assertEqual(result.returncode,1)

    def test_cli_invalid_exit_two(self):
        result=subprocess.run([sys.executable,'-B',str(ROOT/'scripts/review_pack.py'),'check','--root',str(self.root),'--request',str(self.rp),'--request-sha256','0'*64,'--manifest',str(self.mp)],capture_output=True,text=True)
        self.assertEqual(result.returncode,2)


if __name__=='__main__':unittest.main()
