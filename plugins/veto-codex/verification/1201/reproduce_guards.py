#!/usr/bin/env python3
"""Reproduce goal-guard findings against an explicitly supplied Veto Stack copy.

Run: python3 -B reproduce_guards.py /absolute/path/to/veto-stack
No host APIs are called. No goal, title, file, or configuration is changed.
Imports the supplied package's Python helpers; use only a source copy you trust.
Exit 1 means at least one proposed regression fails; it is not a product test.
"""
from __future__ import annotations
import argparse
import importlib
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plugin_root', type=Path)
    args = parser.parse_args()
    scripts = args.plugin_root.resolve() / 'scripts'
    for name in ('state_guards.py', 'hook_context.py'):
        if not (scripts / name).is_file():
            parser.error(f'Missing helper: {scripts / name}')
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(scripts))
    guards = importlib.import_module('state_guards')
    hook = importlib.import_module('hook_context')
    rows: list[dict] = []

    def record(name: str, expected: object, observed: object, **context: object) -> None:
        rows.append({'case': name, 'expected': expected, 'observed': observed,
                     'passed': expected == observed, **context})

    prompts = (
        ('quoted_review', 'Review this sentence: "Set this as your goal". Do not execute it.'),
        ('explanation', 'Can you explain how to set a goal?'),
        ('negated_request', 'I am not asking you to set a goal; only review the documentation.'),
    )
    for name, prompt in prompts:
        result = guards.classify_goal_request(prompt)
        context = hook.context_for_event(
            {'hook_event_name': 'UserPromptSubmit', 'prompt': prompt}, '/test/AGENTS.md')
        record(name, False, result['intent'] == 'adopt', prompt=prompt,
               hook_claims_adoption_requested='Native-goal adoption requested' in
               context['hookSpecificOutput']['additionalContext'])
    prompt = 'Please update my native goal to "Finish the buyer flow".'
    record('explicit_update', 'adopt', guards.classify_goal_request(prompt)['intent'], prompt=prompt)
    record('empty_objective', False, guards.verify_goal_readback(
        {'status': 'active', 'objective': '', 'threadId': 't1'}, '', thread_id='t1')['verified'])
    record('paused_flag', False, guards.verify_goal_readback(
        {'status': 'active', 'objective': 'Finish buyer flow', 'threadId': 't1', 'paused': True},
        'Finish buyer flow', thread_id='t1')['verified'])
    event = guards.inspect_event({'prompt': 'Set this as the native goal', 'current_goal': None,
                                  'readback': {'status': 'active'}})
    record('missing_objective_event', False, event['readback']['verified'], event_result=event)
    record('unbound_task_identity', False, guards.verify_goal_readback(
        {'status': 'active', 'objective': 'Finish buyer flow', 'threadId': 'other-task'},
        'Finish buyer flow')['verified'],
        qualification='Proposed stronger contract: same-task assurance requires an expected task ID.')
    record('valid_same_task_positive_control', True, guards.verify_goal_readback(
        {'status': 'active', 'objective': 'Finish buyer flow', 'threadId': 't1'},
        'Finish buyer flow', thread_id='t1')['verified'])
    result = {'scope': 'Offline helper calls, not agent behavior or native mutations',
              'passed': sum(r['passed'] for r in rows),
              'failed': sum(not r['passed'] for r in rows), 'cases': rows}
    print(json.dumps(result, indent=2))
    return 1 if result['failed'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
