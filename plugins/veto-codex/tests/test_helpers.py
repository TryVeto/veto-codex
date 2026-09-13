"""Checks helper behavior on synthetic temporary files, not the live Veto app."""
from __future__ import annotations
import copy
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from common import digest, load_json, local_file
import check_receipt
import doctor
import lint_slop

class ReceiptTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name); self.art=self.root/'evidence'; self.art.mkdir()
        (self.art/'run.txt').write_text('Synthetic browser check evidence; not a real application test.\n')
        self.cp=self.root/'contract.json'; self.rp=self.root/'receipt.json'
        self.c={'schema_version':1,'contract_id':'test-contract','candidate':{'id':'fixture-build+diff','environment':'isolated-test'},'requirements':[{'id':'J13','expected':'Synthetic contract expectation','layer':'journey','allowed_provenance':['browser'],'required':True}]}
        self.r={'schema_version':1,'contract_id':'test-contract','contract_sha256':'','candidate':copy.deepcopy(self.c['candidate']),'results':[{'id':'J13','status':'passed','layer':'journey','actual':'Synthetic expected result observed in a unit fixture.','provenance':'browser','procedure':'Fixture procedure only','mode':'fresh','evidence':[{'path':'run.txt','sha256':digest(self.art/'run.txt')}]}]}
        self.save()
    def save(self):
        self.cp.write_text(json.dumps(self.c)); self.d=digest(self.cp)
        self.r['contract_sha256']=self.d; self.rp.write_text(json.dumps(self.r))
    def call(self): return check_receipt.check(self.cp,self.d,self.rp,self.art)
    def invalid(self):
        self.save()
        with self.assertRaises((ValueError,OSError,TypeError)): self.call()
    def test_valid_declared_evidence_is_not_product_certificate(self):
        result=self.call(); self.assertEqual(result['verdict'],'DECLARED_EVIDENCE_CONSISTENT'); self.assertTrue(result['limits'])
    def test_contract_digest_is_pinned(self):
        self.cp.write_text(self.cp.read_text()+' ')
        with self.assertRaises(ValueError): self.call()
    def test_receipt_digest_mismatch(self):
        self.r['contract_sha256']='0'*64; self.rp.write_text(json.dumps(self.r))
        with self.assertRaises(ValueError): self.call()
    def test_no_contract_requirements_rejected(self): self.c['requirements']=[]; self.invalid()
    def test_all_optional_contract_rejected(self): self.c['requirements'][0]['required']=False; self.invalid()
    def test_required_must_be_boolean(self): self.c['requirements'][0]['required']='true'; self.invalid()
    def test_duplicate_contract_requirement(self): self.c['requirements'].append(copy.deepcopy(self.c['requirements'][0])); self.invalid()
    def test_receipt_cannot_drop_required_case(self): self.r['results']=[]; self.invalid()
    def test_receipt_cannot_add_requirement(self): self.r['requirements']=[]; self.invalid()
    def test_duplicate_result_rejected(self): self.r['results'].append(copy.deepcopy(self.r['results'][0])); self.invalid()
    def test_unknown_result_rejected(self): self.r['results'][0]['id']='OTHER'; self.invalid()
    def test_candidate_mismatch(self): self.r['candidate']['id']='stale'; self.invalid()
    def test_environment_mismatch(self): self.r['candidate']['environment']='different'; self.invalid()
    def test_schema_bool_is_not_version(self): self.r['schema_version']=True; self.invalid()
    def test_empty_observed_result(self): self.r['results'][0]['actual']=' '; self.invalid()
    def test_missing_procedure_rejected(self): self.r['results'][0].pop('procedure'); self.invalid()
    def test_missing_artifact_rejected(self): self.r['results'][0]['evidence']=[]; self.invalid()
    def test_artifact_hash_mismatch(self): self.r['results'][0]['evidence'][0]['sha256']='0'*64; self.invalid()
    def test_empty_artifact_rejected(self):
        (self.art/'run.txt').write_text(''); self.r['results'][0]['evidence'][0]['sha256']=digest(self.art/'run.txt'); self.invalid()
    def test_traversal_rejected(self): self.r['results'][0]['evidence'][0]['path']='../contract.json'; self.invalid()
    def test_absolute_path_rejected(self): self.r['results'][0]['evidence'][0]['path']=str(self.art/'run.txt'); self.invalid()
    def test_windows_path_rejected(self): self.r['results'][0]['evidence'][0]['path']='C:\\evidence\\run.txt'; self.invalid()
    def test_symlink_artifact_rejected(self):
        (self.art/'link.txt').symlink_to(self.art/'run.txt'); self.r['results'][0]['evidence'][0]['path']='link.txt'; self.invalid()
    def test_symlink_root_rejected(self):
        link=self.root/'linked'; link.symlink_to(self.art,target_is_directory=True)
        with self.assertRaises(ValueError): check_receipt.check(self.cp,self.d,self.rp,link)
    def test_duplicate_artifact_in_row(self): self.r['results'][0]['evidence']*=2; self.invalid()
    def test_wrong_provenance_for_browser(self): self.r['results'][0]['provenance']='unit'; self.invalid()
    def test_contract_cannot_call_simulation_field_observation(self):
        self.c['requirements'][0].update(layer='field',allowed_provenance=['simulation']); self.invalid()
    def test_required_case_cannot_be_waived_in_receipt(self):
        self.r['results'][0].update(status='not_applicable',reason='Builder prefers to skip'); self.save()
        self.assertEqual(self.call()['verdict'],'NOT_ACCEPTED')
    def test_blocked_case_is_not_pass(self):
        self.r['results'][0].update(status='blocked',reason='No permitted browser'); self.save()
        self.assertEqual(self.call()['verdict'],'NOT_ACCEPTED')
    def test_not_run_case_is_not_pass(self):
        self.r['results'][0].update(status='not_run',reason='Fixture only'); self.save()
        self.assertEqual(self.call()['verdict'],'NOT_ACCEPTED')
    def test_failed_case_is_not_pass(self):
        self.r['results'][0].update(status='failed',reason='Observed regression'); self.save()
        self.assertEqual(self.call()['verdict'],'NOT_ACCEPTED')
    def test_carried_evidence_requires_reason(self): self.r['results'][0]['mode']='carried'; self.invalid()
    def test_carried_evidence_is_explicit(self):
        self.r['results'][0].update(mode='carried',carry_reason='Synthetic unchanged dependency and same environment verified'); self.save()
        self.assertEqual(self.call()['verdict'],'DECLARED_EVIDENCE_CONSISTENT')
    def test_unknown_status(self): self.r['results'][0]['status']='looks-good'; self.invalid()
    def test_optional_case_allows_explicit_na_only(self):
        self.c['requirements'].append({'id':'OPTIONAL','expected':'Scoped optional check','layer':'rules','allowed_provenance':['unit'],'required':False})
        self.r['results'].append({'id':'OPTIONAL','status':'not_applicable','layer':'rules','actual':'Not involved in this synthetic change','reason':'Contract owner excluded this dependency','evidence':[]})
        self.save(); self.assertEqual(self.call()['verdict'],'DECLARED_EVIDENCE_CONSISTENT')
    def test_duplicate_json_keys_rejected(self):
        self.rp.write_text('{"schema_version":1,"schema_version":1}')
        with self.assertRaises(ValueError): self.call()
    def test_nonfinite_json_rejected(self):
        self.rp.write_text('{"value":NaN}')
        with self.assertRaises(ValueError): load_json(self.rp)
    def test_read_only_check_leaves_files_unchanged(self):
        before={p:digest(p) for p in [self.cp,self.rp,self.art/'run.txt']}; self.call()
        self.assertEqual(before,{p:digest(p) for p in before})

class SlopTests(unittest.TestCase):
    def test_decorative_component_is_review_not_semantic_error(self):
        found=lint_slop.inspect_text('<Eyebrow>Workspace</Eyebrow>','x.tsx')
        self.assertTrue(found); self.assertTrue(all(f['severity']=='review' for f in found))
    def test_functional_plain_label_not_flagged(self):
        self.assertEqual(lint_slop.inspect_text('<label for="a">ACCOUNT NUMBER</label>','x.html'),[])
    def test_named_overline_needs_context_not_blind_deletion(self):
        found=lint_slop.inspect_text('<label class="overline" for="a">Account</label>','x.html')
        self.assertTrue(found); self.assertEqual(found[0]['severity'],'review')
    def test_comments_and_data_assets_are_masked(self):
        text='<!-- <Eyebrow>bad</Eyebrow> -->\n/* .eyebrow { } */\n<img src="data:text/plain,fraud-proof">'
        self.assertEqual(lint_slop.inspect_text(text,'x.html'),[])
    def test_line_numbers_survive_masking(self):
        found=lint_slop.inspect_text('<!-- a\nb -->\n<Eyebrow>Title</Eyebrow>','x.tsx')
        self.assertEqual(found[0]['line'],3)
    def test_unsupported_assurance_is_only_a_review_finding(self):
        found=lint_slop.inspect_text('<p>100% secure</p>','x.html')
        self.assertEqual(found[0]['rule'],'unsupported-assurance')
    def test_no_visible_focus_pattern_requires_inspection(self):
        found=lint_slop.inspect_text(':focus { outline: none; }','x.css')
        self.assertEqual(found[0]['severity'],'review')
    def test_dynamic_decoration_can_be_missed(self):
        self.assertEqual(lint_slop.inspect_text('<div>{categoryLabel}</div><h1>{title}</h1>','x.tsx'),[])
    def test_scan_excludes_dependencies_and_preserves_source(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td); (p/'view.html').write_text('<h1>Review</h1>'); before=digest(p/'view.html')
            (p/'node_modules').mkdir(); (p/'node_modules/bad.html').write_text('<Eyebrow>Bad</Eyebrow>')
            r=lint_slop.scan(p); self.assertEqual(len(r['scanned_files']),1); self.assertTrue(r['skipped']); self.assertEqual(digest(p/'view.html'),before)
    def test_scan_reports_symlink_exclusion(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td); (p/'a.html').write_text('<h1>Review</h1>'); (p/'b.html').symlink_to(p/'a.html')
            self.assertTrue(any(x['reason']=='symlink not followed' for x in lint_slop.scan(p)['skipped']))
    def test_invalid_target_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError): lint_slop.scan(Path(td)/'missing.html')
    def test_unsupported_extension_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'source.pdf'; p.write_text('not a source format')
            with self.assertRaises(ValueError): lint_slop.scan(p)

class PackageTests(unittest.TestCase):
    def copy_package(self):
        td=tempfile.TemporaryDirectory(); self.addCleanup(td.cleanup)
        path=Path(td.name)/'plugin'; shutil.copytree(ROOT,path); return path
    def test_actual_package_structure(self):
        self.assertEqual(doctor.run(ROOT,verify_hashes=False)['errors'],[])

    def test_personal_marketplace_allows_unrelated_entries_and_reports_archives(self):
        with tempfile.TemporaryDirectory() as td:
            home=Path(td)/'home'; root=home/'plugins'/'veto-codex'
            root.parent.mkdir(parents=True)
            shutil.copytree(ROOT,root)
            catalog_dir=home/'.agents'/'plugins'; catalog_dir.mkdir(parents=True)
            (catalog_dir/'marketplace.json').write_text(json.dumps({'name':'personal','plugins':[
                {'name':'veto-codex','source':{'source':'local','path':'./plugins/veto-codex'}},
                {'name':'use-ai-well','source':{'source':'local','path':'./plugins/use-ai-well'}},
                {'name':'archived-veto-codex-v5','source':{'source':'local','path':'./plugins/archived-veto-codex-v5'}},
            ]}))
            result=doctor.run(root,verify_hashes=False)
            self.assertEqual(result['errors'],[])
            self.assertTrue(any('archived-veto-codex-v5' in warning for warning in result['warnings']))

    def test_personal_marketplace_duplicate_canonical_entry_fails(self):
        with tempfile.TemporaryDirectory() as td:
            home=Path(td)/'home'; root=home/'plugins'/'veto-codex'
            root.parent.mkdir(parents=True)
            shutil.copytree(ROOT,root)
            catalog_dir=home/'.agents'/'plugins'; catalog_dir.mkdir(parents=True)
            entry={'name':'veto-codex','source':{'source':'local','path':'./plugins/veto-codex'}}
            (catalog_dir/'marketplace.json').write_text(json.dumps({'name':'personal','plugins':[entry,entry]}))
            result=doctor.run(root,verify_hashes=False)
            self.assertTrue(any('duplicate veto-codex' in error for error in result['errors']))
    def test_bad_skill_frontmatter(self):
        with self.assertRaises(ValueError): doctor.frontmatter('name: bad')
    def test_manifest_versions_must_match(self):
        p=self.copy_package(); m=load_json(p/'.codex-plugin/plugin.json'); m['version']='0.1.0'; (p/'.codex-plugin/plugin.json').write_text(json.dumps(m))
        self.assertTrue(any('mismatch' in x for x in doctor.run(p,verify_hashes=False)['errors']))
    def test_broken_reference_detected(self):
        p=self.copy_package(); f=p/'README.md'; f.write_text(f.read_text()+'\n[missing](nowhere.md)\n')
        self.assertTrue(any('Broken' in x for x in doctor.run(p,verify_hashes=False)['errors']))
    def test_escaping_link_detected(self):
        p=self.copy_package(); (p.parent/'outside.md').write_text('external'); f=p/'README.md'; f.write_text(f.read_text()+'\n[outside](../outside.md)\n')
        self.assertTrue(any('escaping' in x for x in doctor.run(p,verify_hashes=False)['errors']))
    def test_goal_limit_is_strict(self):
        p=self.copy_package(); (p/'templates/goal.md').write_text('x'*4000)
        self.assertTrue(any('4,000' in x for x in doctor.run(p,verify_hashes=False)['errors']))
    def test_fonts_not_redistributed(self):
        p=self.copy_package(); (p/'assets/test.woff2').write_bytes(b'not an actual font')
        self.assertTrue(any('font/secret' in x for x in doctor.run(p,verify_hashes=False)['errors']))
    def test_new_mcp_surface_detected(self):
        p=self.copy_package(); (p/'mcp.json').write_text('{}')
        self.assertTrue(any('dependency surface' in x for x in doctor.run(p,verify_hashes=False)['errors']))
    def test_payload_hash_changes_detected(self):
        p=self.copy_package()
        inventory={f.relative_to(p).as_posix():digest(f) for f in p.rglob('*') if f.is_file() and f.name!='FILES.sha256.json'}
        (p/'FILES.sha256.json').write_text(json.dumps(inventory)); (p/'templates/goal.md').write_text('# changed\n')
        self.assertTrue(any('hash mismatch' in x for x in doctor.run(p)['errors']))
    def test_unknown_portable_field_rejected(self):
        p=self.copy_package(); m=load_json(p/'plugin.json'); m['unexpected']='value'; (p/'plugin.json').write_text(json.dumps(m))
        self.assertTrue(any('root fields' in x for x in doctor.run(p,verify_hashes=False)['errors']))
    def test_nested_manifest_named_file_cannot_hide(self):
        p=self.copy_package()
        inventory={f.relative_to(p).as_posix():digest(f) for f in p.rglob('*') if f.is_file() and f.relative_to(p).as_posix()!='FILES.sha256.json'}
        (p/'FILES.sha256.json').write_text(json.dumps(inventory)); (p/'assets/FILES.sha256.json').write_text('{}')
        self.assertTrue(any('inventory differs' in x for x in doctor.run(p)['errors']))
    def test_unlisted_payload_detected(self):
        p=self.copy_package()
        inventory={f.relative_to(p).as_posix():digest(f) for f in p.rglob('*') if f.is_file() and f.name!='FILES.sha256.json'}
        (p/'FILES.sha256.json').write_text(json.dumps(inventory)); (p/'unexpected.txt').write_text('new')
        self.assertTrue(any('inventory differs' in x for x in doctor.run(p)['errors']))

class OracleSensitivityTests(unittest.TestCase):
    def load(self,name):
        p=ROOT/'evals/oracles'/f'{name}_oracle.py'; spec=importlib.util.spec_from_file_location(name,p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
    def test_focus_oracle_rejects_bundled_broken_retrieval(self):
        self.assertFalse(all(self.load('focus').evaluate(ROOT/'evals/fixtures/focus').values()))
    def test_focus_oracle_accepts_controlled_corrected_fixture(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td); shutil.copytree(ROOT/'evals/fixtures/focus',p,dirs_exist_ok=True)
            f=p/'store.py'; s=f.read_text(); s=s.replace("return {'office':office,'file':file,'request':'demo-request','contribution':{'note':'demo material'}}","return json.loads(_path(root,office,file).read_text())"); f.write_text(s)
            self.assertTrue(all(self.load('focus').evaluate(p).values()))
    def test_craft_oracle_distinguishes_controlled_subtraction(self):
        oracle=self.load('craft'); original=ROOT/'evals/fixtures/craft/review.html'
        self.assertFalse(all(oracle.evaluate(original).values()))
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'review.html'; s=original.read_text().replace('<p class="eyebrow">Workspace</p>','').replace('<p class="orientation">Review the receiving instructions below.</p>',''); p.write_text(s)
            self.assertTrue(all(oracle.evaluate(p).values()))
    def test_craft_oracle_rejects_deleted_functional_label(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'review.html'; s=(ROOT/'evals/fixtures/craft/review.html').read_text().replace('<label class="overline" for="account">Receiving account</label>',''); p.write_text(s)
            self.assertFalse(self.load('craft').evaluate(p)['functional_label'])

if __name__=='__main__': unittest.main()
