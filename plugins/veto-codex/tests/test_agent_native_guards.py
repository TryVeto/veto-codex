"""Reviewer regressions and positive controls; no native-host operations."""
from __future__ import annotations
import json
import subprocess
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import state_guards as guard
import hook_context


class NativeRegressionTests(unittest.TestCase):
    def test_review_quoted_goal_is_not_adoption(self):
        self.assertEqual(guard.classify_goal_request('Review this sentence: “Set this as your goal”. Do not execute it.')['intent'],'draft')

    def test_explanation_does_not_authorize(self):
        self.assertEqual(guard.classify_goal_request('Can you explain how to set a goal?')['intent'],'draft')

    def test_explicit_negation_does_not_authorize(self):
        self.assertEqual(guard.classify_goal_request('I am not asking you to set a goal; only review the documentation.')['intent'],'draft')

    def test_explicit_update_routes_to_native_procedure(self):
        self.assertEqual(guard.classify_goal_request('Please update the native goal to the accepted objective.')['intent'],'adopt')

    def test_quoted_fenced_and_hypothetical_prompts_are_nonmutating(self):
        for text in ['"Set this as your goal"', "'Set this as your goal'", '“Set this as your goal”',
                     '```text\nSet this as your goal\n```', '```\nSet this as your goal',
                     '> Adopt this goal\n', 'For example, set this as your goal.',
                     'Do not execute it; set this as your goal.', 'Don’t set this as your goal.',
                     'If we were to adopt this goal, what would happen?']:
            with self.subTest(text=text):
                self.assertNotEqual(guard.classify_goal_request(text)['intent'],'adopt')

    def test_routing_never_claims_authorization(self):
        for text in ['Set this as your goal.','Write goal.md','Fix the label','Update the native goal.']:
            with self.subTest(text=text):
                self.assertFalse(guard.classify_goal_request(text)['authorization_established'])

    def test_empty_objectives_cannot_verify(self):
        self.assertFalse(guard.verify_goal_readback({'status':'active','objective':'','threadId':'t'},'',thread_id='t')['verified'])

    def test_missing_expected_cannot_verify(self):
        r=guard.inspect_event({'prompt':'Set this as your goal','current_goal':None,'readback':{'status':'active'}})
        self.assertFalse(r['readback']['verified'])
        self.assertNotEqual(r['goal']['action'],'create_goal')

    def test_native_pause_contradiction_cannot_verify(self):
        self.assertFalse(guard.verify_goal_readback({'status':'active','objective':'x','paused':True,'threadId':'t'},'x',thread_id='t')['verified'])

    def test_thread_binding_is_required(self):
        self.assertFalse(guard.verify_goal_readback({'status':'active','objective':'x','threadId':'t'},'x')['verified'])

    def test_blank_thread_binding_is_not_identity(self):
        self.assertFalse(guard.verify_goal_readback({'status':'active','objective':'x','threadId':''},'x',thread_id='')['verified'])

    def test_invalid_pause_types_are_not_coerced(self):
        for paused in [0,1,'false',[],None]:
            with self.subTest(paused=paused):
                self.assertFalse(guard.verify_goal_readback({'status':'active','objective':'x','paused':paused,'threadId':'t'},'x',thread_id='t')['verified'])

    def test_valid_same_thread_active_goal_still_verifies(self):
        self.assertTrue(guard.verify_goal_readback({'status':'active','objective':'Goal text','paused':False,'threadId':'t'},'Goal text',thread_id='t')['verified'])

    def test_missing_readback_is_not_observed_null_goal(self):
        r=guard.inspect_event({'prompt':'Set this as your goal','expected_objective':'x'})
        self.assertEqual(r['goal']['action'],'inspect_native_goal')

    def test_complete_but_paused_does_not_plan_create(self):
        r=guard.goal_action({'status':'complete','objective':'old','paused':True},'new')
        self.assertEqual(r['action'],'preserve_pause')

    def test_string_false_does_not_authorize_title_change(self):
        r=guard.inspect_event({'title':'Local','assignment_blocked':'false'})
        self.assertFalse(r['title']['changed'])

    def test_hook_does_not_assert_native_adoption(self):
        for text in ['Set this as your goal.', 'Review this sentence: “Set this as your goal”. Do not execute it.']:
            with self.subTest(text=text):
                r=hook_context.context_for_event({'hook_event_name':'UserPromptSubmit','prompt':text},'/tmp/rules.md')
                self.assertNotIn('Native-goal adoption requested',r['hookSpecificOutput']['additionalContext'])
        r=hook_context.context_for_event({'hook_event_name':'UserPromptSubmit','prompt':'Set this as your goal.'},'/tmp/rules.md')
        self.assertIn('not established authorization',r['hookSpecificOutput']['additionalContext'])

    def test_event_cli_validates_missing_objective(self):
        r=subprocess.run([sys.executable,'-B',str(ROOT/'scripts/state_guards.py')],
                         input=json.dumps({'prompt':'Set this as your goal','current_goal':None,'readback':{'status':'active'}}),
                         text=True,capture_output=True,check=True)
        self.assertFalse(json.loads(r.stdout)['readback']['verified'])

if __name__=='__main__':unittest.main()
