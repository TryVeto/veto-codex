"""Local checker tests on synthetic claims. No browser, reviewer model or live product runs."""
from __future__ import annotations
import copy
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import check_receipt
from common import digest

class FeedbackCoverageTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.cp, self.rp, self.fp, self.ap = [self.root/n for n in ('contract.json','receipt.json','feedback.json','audit.json')]
        self.original = 'Autocomplete must expand into editable address fields. Save and reopen the corrected values.'
        self.decision = 'The optional tour is outside this accepted task.'
        (self.root/'original.txt').write_text(self.original+'\n'+self.decision+'\n')
        (self.root/'audit.txt').write_text('Synthetic audit assertion for checker tests; no actual independent reviewer ran.')
        (self.root/'run.txt').write_text('Synthetic browser-result assertion for checker tests; no browser ran.')
        self.f = {'schema_version':1,'batch_id':'synthetic-batch','sources':[{'id':'S1','kind':'text','artifact':self.art('original.txt')}],
                  'items':[{'id':'F1','source_id':'S1','original':self.original,'context':'synthetic intake screen',
                            'interpretation':'Select, expand, edit, save and reopen the same address.','kind':'requirement','owner':'frontend'}]}
        self.c = {'schema_version':2,'contract_id':'synthetic-contract','candidate':{'id':'fixture-build','environment':'disposable'},
                  'feedback':{'sha256':'','builder':'fixture-builder','reviewer':'fixture-verifier'},
                  'requirements':[{'id':'AC1','expected':self.original,'layer':'journey','allowed_provenance':['browser'],'required':True}]}
        self.a = {'schema_version':1,'batch_id':'synthetic-batch','feedback_sha256':'','contract_sha256':'','reviewer':'fixture-verifier',
                  'audit_evidence':self.art('audit.txt'),'source_reviews':[{'id':'S1','status':'complete','finding':'Fixture declares the whole source inventoried.'}],
                  'items':[{'id':'F1','status':'covered','requirement_ids':['AC1'],'reason':'Fixture maps the full compound behavior.'}]}
        self.r = {'schema_version':2,'contract_id':'synthetic-contract','contract_sha256':'','candidate':copy.deepcopy(self.c['candidate']),
                  'results':[{'id':'AC1','status':'passed','layer':'journey','actual':'Synthetic declared observation; not a product test.',
                              'evidence':[self.art('run.txt')],'provenance':'browser','procedure':'Fixture declaration only','mode':'fresh'}]}
        self.save()
    def art(self, path): return {'path':path,'sha256':digest(self.root/path)}
    def save(self):
        self.fp.write_text(json.dumps(self.f)); self.c['feedback']['sha256']=digest(self.fp)
        self.cp.write_text(json.dumps(self.c)); self.pin=digest(self.cp)
        self.a.update(feedback_sha256=digest(self.fp),contract_sha256=self.pin)
        self.ap.write_text(json.dumps(self.a)); self.r['contract_sha256']=self.pin; self.rp.write_text(json.dumps(self.r))
    def call(self):
        return check_receipt.check(self.cp,self.pin,self.rp,self.root,feedback_path=self.fp,coverage_path=self.ap)
    def invalid(self):
        self.save()
        with self.assertRaises((ValueError,OSError,TypeError)): self.call()
    def test_consistent_declarations_not_product_proof(self):
        result=self.call(); self.assertEqual(result['verdict'],'DECLARED_COVERAGE_AND_EVIDENCE_CONSISTENT')
        self.assertEqual(result['feedback_coverage']['item_count'],1)
        self.assertTrue(any('semantic' in x for x in result['limits']))
    def test_feedback_cannot_be_omitted(self):
        with self.assertRaises(ValueError): check_receipt.check(self.cp,self.pin,self.rp,self.root)
    def test_review_cannot_be_omitted(self):
        with self.assertRaises(ValueError): check_receipt.check(self.cp,self.pin,self.rp,self.root,feedback_path=self.fp)
    def test_feedback_guard_cannot_be_omitted(self):
        self.c.pop('feedback'); self.cp.write_text(json.dumps(self.c))
        with self.assertRaises(ValueError): check_receipt.validate_contract(self.c)
    def test_same_reviewer_as_builder_rejected(self):
        self.c['feedback']['reviewer']='fixture-builder';self.invalid()
    def test_different_unassigned_reviewer_rejected(self):
        self.a['reviewer']='other';self.invalid()
    def test_changed_feedback_fails_pin(self):
        self.fp.write_text(self.fp.read_text()+' ')
        with self.assertRaises(ValueError): self.call()
    def test_stale_contract_audit_rejected(self):
        self.a['contract_sha256']='0'*64;self.ap.write_text(json.dumps(self.a))
        with self.assertRaises(ValueError): self.call()
    def test_stale_feedback_audit_rejected(self):
        self.a['feedback_sha256']='0'*64;self.ap.write_text(json.dumps(self.a))
        with self.assertRaises(ValueError): self.call()
    def test_missing_source_review_rejected(self):
        self.a['source_reviews']=[];self.invalid()
    def test_duplicate_source_review_rejected(self):
        self.a['source_reviews']*=2;self.invalid()
    def test_source_audit_exposes_omitted_annotation_even_with_green_tests(self):
        self.a['source_reviews'][0].update(status='gap',finding='Second original annotation omitted from the inventory.')
        self.save(); self.assertEqual(self.call()['verdict'],'NOT_ACCEPTED')
    def test_unavailable_image_review_is_not_pass(self):
        self.a['source_reviews'][0].update(status='unavailable',finding='Cannot inspect original screenshot context.')
        self.save(); self.assertEqual(self.call()['verdict'],'NOT_ACCEPTED')
    def test_reported_summary_cannot_substitute_for_original(self):
        self.f['sources'][0]['kind']='reported_summary';self.save()
        self.assertEqual(self.call()['verdict'],'NOT_ACCEPTED')
    def test_invented_original_quote_rejected(self):
        self.f['items'][0]['original']='Made-up original words';self.invalid()
    def test_source_file_tamper_rejected(self):
        (self.root/'original.txt').write_text('changed')
        with self.assertRaises(ValueError): self.call()
    def test_source_path_traversal_rejected(self):
        self.f['sources'][0]['artifact']['path']='../outside.txt';self.invalid()
    def test_missing_audit_artifact_rejected(self):
        self.a['audit_evidence']['path']='absent.txt';self.invalid()
    def test_changed_audit_artifact_rejected(self):
        (self.root/'audit.txt').write_text('changed')
        with self.assertRaises(ValueError): self.call()
    def test_duplicate_feedback_id_rejected(self):
        self.f['items']*=2;self.invalid()
    def test_empty_feedback_batch_rejected(self):
        self.f['items']=[];self.invalid()
    def test_mapped_item_omission_rejected(self):
        second=copy.deepcopy(self.f['items'][0]);second['id']='F2';self.f['items'].append(second);self.invalid()
    def test_unknown_acceptance_mapping_rejected(self):
        self.a['items'][0]['requirement_ids']=['MISSING'];self.invalid()
    def test_empty_acceptance_mapping_rejected(self):
        self.a['items'][0]['requirement_ids']=[];self.invalid()
    def test_duplicate_acceptance_mapping_rejected(self):
        self.a['items'][0]['requirement_ids']*=2;self.invalid()
    def test_optional_case_cannot_close_required_feedback(self):
        opt=copy.deepcopy(self.c['requirements'][0]);opt.update(id='OPTIONAL',required=False)
        self.c['requirements'].append(opt);self.a['items'][0]['requirement_ids']=['OPTIONAL'];self.invalid()
    def test_narrowing_flag_blocks_green_test_receipt(self):
        self.a['items'][0].update(status='unresolved',reason='Autocomplete attribute omits suggestions, expansion and persistence.')
        self.save(); self.assertEqual(self.call()['verdict'],'NOT_ACCEPTED')
    def test_deferral_stays_open(self):
        self.a['items'][0].update(status='deferred',reason='After the current checkpoint.')
        self.save(); self.assertEqual(self.call()['verdict'],'NOT_ACCEPTED')
    def test_answer_cannot_replace_required_behavior(self):
        self.a['items'][0].update(status='answered',requirement_ids=[],answer=self.art('run.txt'));self.invalid()
    def test_question_can_close_with_evidenced_answer(self):
        self.f['items'][0]['kind']='question'
        self.a['items'][0].update(status='answered',requirement_ids=[],answer=self.art('run.txt'))
        self.save(); self.assertEqual(self.call()['verdict'],'DECLARED_COVERAGE_AND_EVIDENCE_CONSISTENT')
    def test_supersession_requires_decision_source(self):
        self.a['items'][0].update(status='superseded',requirement_ids=[]);self.invalid()
    def test_disposition_with_recorded_decision_is_structurally_valid(self):
        self.a['items'][0].update(status='not_applicable',requirement_ids=[],reason='Synthetic disposition for schema test only.',
                                 decision={'source_id':'S1','quote':self.decision})
        self.save();self.assertEqual(self.call()['verdict'],'DECLARED_COVERAGE_AND_EVIDENCE_CONSISTENT')
    def test_unknown_disposition_decision_rejected(self):
        self.a['items'][0].update(status='not_applicable',requirement_ids=[],decision={'source_id':'S1','quote':'Unrecorded waiver'})
        self.invalid()
    def test_green_coverage_cannot_hide_failed_behavior(self):
        self.r['results'][0].update(status='failed',reason='Saved values differ on reopen.')
        self.save();self.assertEqual(self.call()['verdict'],'NOT_ACCEPTED')
    def test_green_coverage_cannot_hide_missing_browser(self):
        self.r['results'][0].update(status='blocked',reason='Required preview cannot be inspected.')
        self.save();self.assertEqual(self.call()['verdict'],'NOT_ACCEPTED')
    def test_semantic_judgment_is_not_falsely_claimed_as_automated(self):
        # The checker cannot detect an inaccurate semantic audit. Document this limitation.
        self.c['requirements'][0]['expected']='An HTML autocomplete attribute is present.'
        self.save();result=self.call()
        self.assertEqual(result['verdict'],'DECLARED_COVERAGE_AND_EVIDENCE_CONSISTENT')
        self.assertTrue(any('semantic fidelity' in x for x in result['limits']))
    def test_legacy_receipt_explicitly_lacks_coverage(self):
        self.c.pop('feedback');self.c['schema_version']=1;self.r['schema_version']=1
        self.cp.write_text(json.dumps(self.c));self.r['contract_sha256']=digest(self.cp);self.rp.write_text(json.dumps(self.r))
        result=check_receipt.check(self.cp,digest(self.cp),self.rp,self.root)
        self.assertEqual(result['feedback_coverage']['verdict'],'NOT_CHECKED')
    def test_boolean_schema_rejected(self):
        self.f['schema_version']=True;self.invalid()
    def test_cli_refuses_coverage_omission_with_exit_2(self):
        out=io.StringIO()
        with patch.object(sys,'argv',['check_receipt','--contract',str(self.cp),'--contract-sha256',self.pin,'--receipt',str(self.rp),'--artifact-root',str(self.root)]),redirect_stdout(out):
            code=check_receipt.main()
        self.assertEqual(code,2);self.assertEqual(json.loads(out.getvalue())['verdict'],'INVALID')

    def as_legacy(self):
        self.c.pop('feedback'); self.c['schema_version']=1; self.r['schema_version']=1
        self.cp.write_text(json.dumps(self.c)); self.pin=digest(self.cp)
        self.r['contract_sha256']=self.pin; self.rp.write_text(json.dumps(self.r))

    def flagged(self):
        return check_receipt.check(self.cp,self.pin,self.rp,self.root,
                                   feedback_path=self.fp,coverage_path=self.ap,require_feedback=True)

    def cli_flagged(self, *, include_sources=True):
        args=['check_receipt','--require-feedback','--contract',str(self.cp),
              '--contract-sha256',self.pin,'--receipt',str(self.rp),'--artifact-root',str(self.root)]
        if include_sources:
            args += ['--feedback',str(self.fp),'--coverage-review',str(self.ap)]
        out=io.StringIO()
        with patch.object(sys,'argv',args),redirect_stdout(out): code=check_receipt.main()
        return code,json.loads(out.getvalue())

    def test_required_feedback_preserves_valid_declared_coverage(self):
        result=self.flagged()
        self.assertEqual(result['verdict'],'DECLARED_COVERAGE_AND_EVIDENCE_CONSISTENT')
        self.assertIs(result['feedback_required'],True)

    def test_required_feedback_rejects_green_evidence_only_contract(self):
        self.as_legacy()
        old=check_receipt.check(self.cp,self.pin,self.rp,self.root)
        self.assertEqual(old['verdict'],'DECLARED_EVIDENCE_CONSISTENT')
        self.assertIs(old['feedback_required'],False)
        with self.assertRaisesRegex(ValueError,'Feedback coverage is required'):
            check_receipt.check(self.cp,self.pin,self.rp,self.root,require_feedback=True)

    def test_required_feedback_flag_is_not_a_string(self):
        with self.assertRaisesRegex(ValueError,'must be a boolean'):
            check_receipt.check(self.cp,self.pin,self.rp,self.root,require_feedback='false')

    def test_required_feedback_does_not_supply_missing_sources(self):
        with self.assertRaisesRegex(ValueError,'requires --feedback'):
            check_receipt.check(self.cp,self.pin,self.rp,self.root,require_feedback=True)

    def test_required_feedback_keeps_source_gaps_open(self):
        self.a['source_reviews'][0].update(status='gap',finding='Another annotation is omitted.')
        self.save(); self.assertEqual(self.flagged()['verdict'],'NOT_ACCEPTED')

    def test_cli_required_feedback_refuses_legacy_with_exit_2(self):
        self.as_legacy(); code,result=self.cli_flagged(include_sources=False)
        self.assertEqual(code,2); self.assertEqual(result['verdict'],'INVALID')
        self.assertIn('Feedback coverage is required',result['error'])

    def test_cli_required_feedback_accepts_consistent_declarations_only(self):
        code,result=self.cli_flagged()
        self.assertEqual(code,0)
        self.assertEqual(result['verdict'],'DECLARED_COVERAGE_AND_EVIDENCE_CONSISTENT')
        self.assertIs(result['feedback_required'],True)
        self.assertTrue(any('does not prove execution' in x for x in result['limits']))

    def test_cli_required_feedback_retains_unresolved_batch_exit_1(self):
        self.a['items'][0].update(status='unresolved',reason='The requested expanded fields are unverified.')
        self.save(); code,result=self.cli_flagged()
        self.assertEqual(code,1); self.assertEqual(result['verdict'],'NOT_ACCEPTED')
        self.assertIs(result['feedback_required'],True)

if __name__=='__main__': unittest.main()
