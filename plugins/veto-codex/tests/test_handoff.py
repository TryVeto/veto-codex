"""Read-only handoff integrity; fixtures are not agent or product acceptance."""
from __future__ import annotations
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import check_handoff
from common import digest


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        for name,text in [('request.md','Repair the local fixture only.'),('candidate.txt','repaired'),
                          ('evidence.txt','Fixture test passed.'),('decision.md','Preserve scope.')]:
            (self.root/name).write_text(text)
        self.record={'schema_version':1,'task_id':'repair','assignment_revision':2,'owner':'local',
                     'outcome':'Repair the named fixture','state':'active','candidate_id':'fixture-2',
                     'must_preserve':['No product or release changes'],'next_action':'Obtain independent review',
                     'resume_condition':'Current authority permits continuing',
                     'references':[{'id':key,'kind':kind,'path':path,'sha256':digest(self.root/path)}
                                   for key,kind,path in [('r','request','request.md'),('c','candidate','candidate.txt'),
                                                         ('e','evidence','evidence.txt'),('d','decision','decision.md')]],
                     'completed':[{'id':'repair','result':'Fixture repaired','evidence_ids':['e']}],
                     'remaining':['Independent review']}
        self.path=self.root/'handoff.json'

    def save(self):
        self.path.write_text(json.dumps(self.record));return digest(self.path)

    def check(self,**kw):
        return check_handoff.check(self.path,self.root,expected_task_id=kw.get('task_id','repair'),
                                   expected_revision=kw.get('revision',2),trusted_sha256=kw.get('sha256',self.save()))

    def test_valid_handoff_preserves_credit_without_authority(self):
        r=self.check();self.assertEqual(r['verdict'],'HANDOFF_INTEGRITY_PASSED')
        self.assertFalse(r['permission_granted']);self.assertFalse(r['native_state_verified'])
        self.assertEqual(r['runtime_action'],'none');self.assertEqual(len(r['completed']),1)

    def test_paused_stays_paused(self):
        self.record['state']='paused';self.assertEqual(self.check()['verdict'],'PRESERVE_PAUSE')

    def test_blocker_is_not_completion(self):
        self.record['state']='blocked';self.assertEqual(self.check()['verdict'],'BLOCKER_RECORDED')

    def test_handoff_cannot_declare_accepted_or_done(self):
        for state in ['accepted','done','complete',True,{}]:
            with self.subTest(state=state):
                self.record['state']=state
                with self.assertRaises(ValueError):self.check()

    def test_candidate_drift_needs_reconciliation(self):
        (self.root/'candidate.txt').write_text('changed after handoff')
        self.assertEqual(self.check()['verdict'],'NEEDS_RECONCILIATION')

    def test_evidence_drift_needs_reconciliation(self):
        (self.root/'evidence.txt').write_text('different')
        r=self.check();self.assertEqual(r['verdict'],'NEEDS_RECONCILIATION');self.assertNotIn('next_action',r)

    def test_request_drift_needs_reconciliation(self):
        (self.root/'request.md').write_text('Expanded scope')
        self.assertEqual(self.check()['verdict'],'NEEDS_RECONCILIATION')

    def test_wrong_task_rejected(self):
        self.assertEqual(self.check(task_id='other')['verdict'],'NEEDS_RECONCILIATION')

    def test_stale_revision_rejected(self):
        self.assertEqual(self.check(revision=3)['verdict'],'NEEDS_RECONCILIATION')

    def test_tampered_record_does_not_expose_next_instruction(self):
        sha=self.save();self.path.write_text('malicious invalid JSON')
        r=check_handoff.check(self.path,self.root,expected_task_id='repair',expected_revision=2,trusted_sha256=sha)
        self.assertEqual(r['verdict'],'NEEDS_RECONCILIATION');self.assertNotIn('next_action',r)

    def test_missing_file_rejected(self):
        (self.root/'candidate.txt').unlink();self.assertEqual(self.check()['verdict'],'NEEDS_RECONCILIATION')

    def test_symlink_rejected(self):
        (self.root/'alias').symlink_to(self.root/'candidate.txt');self.record['references'][1]['path']='alias'
        self.assertEqual(self.check()['verdict'],'NEEDS_RECONCILIATION')

    def test_path_escape_rejected(self):
        for path in ['../outside','/etc/passwd','https://example.test/file','C:\\secret','foo/../candidate.txt']:
            with self.subTest(path=path):
                self.record['references'][1]['path']=path
                self.assertEqual(self.check()['verdict'],'NEEDS_RECONCILIATION')

    def test_missing_original_request_rejected(self):
        self.record['references'][0]['kind']='decision'
        with self.assertRaises(ValueError):self.check()

    def test_duplicate_reference_rejected(self):
        self.record['references'].append(copy.deepcopy(self.record['references'][0]))
        with self.assertRaises(ValueError):self.check()

    def test_source_is_not_completion_evidence(self):
        self.record['completed'][0]['evidence_ids']=['r']
        with self.assertRaises(ValueError):self.check()

    def test_empty_evidence_rejected(self):
        (self.root/'evidence.txt').write_text('');self.record['references'][2]['sha256']=digest(self.root/'evidence.txt')
        self.assertEqual(self.check()['verdict'],'NEEDS_RECONCILIATION')

    def test_boolean_revision_not_valid(self):
        self.record['assignment_revision']=True
        with self.assertRaises(ValueError):self.check()

    def test_bad_schema_rejected(self):
        self.record['schema_version']=True
        with self.assertRaises(ValueError):self.check()

    def test_ready_without_credit_rejected(self):
        self.record['state']='ready_for_review';self.record['completed']=[]
        with self.assertRaises(ValueError):self.check()

    def test_decision_return_preserves_proposal_status(self):
        self.record['decision_return']={'status':'proposed','source_id':'d','stays':['Goal'],
                                         'changes':['Method'],'credited':['Fixture repair'],
                                         'next_result':'Independent replay'}
        r=self.check();self.assertEqual(r['decision_return']['status'],'proposed')
        self.assertFalse(r['decision_authority_authenticated'])

    def test_decision_requires_source(self):
        self.record['decision_return']={'status':'adopted','source_id':'missing','stays':[],
                                         'changes':['Method'],'credited':[],'next_result':'Replay'}
        with self.assertRaises(ValueError):self.check()

    def test_checker_does_not_modify_files(self):
        self.save();before={p.name:p.read_bytes() for p in self.root.iterdir()}
        self.check();self.assertEqual(before,{p.name:p.read_bytes() for p in self.root.iterdir()})

    def test_fresh_process_can_read_same_record(self):
        sha=self.save()
        cmd=[sys.executable,'-B',str(ROOT/'scripts/check_handoff.py'),'--record',str(self.path),
             '--root',str(self.root),'--task-id','repair','--revision','2','--sha256',sha]
        a=subprocess.run(cmd,text=True,capture_output=True,check=True)
        b=subprocess.run(cmd,text=True,capture_output=True,check=True)
        self.assertEqual(json.loads(a.stdout),json.loads(b.stdout))
        (self.root/'candidate.txt').write_text('drift')
        c=subprocess.run(cmd,text=True,capture_output=True)
        self.assertEqual(c.returncode,1)

if __name__=='__main__':unittest.main()
