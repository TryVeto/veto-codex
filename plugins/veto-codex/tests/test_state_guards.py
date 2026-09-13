"""Regression tests for goal adoption and blocked-title state guards.

These tests exercise only deterministic classification and postcondition checks;
they do not pretend to call the native Codex host or prove model behavior.
"""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import state_guards
import hook_context


class GoalRequestTests(unittest.TestCase):
    def test_file_only_request_does_not_activate(self):
        result = state_guards.classify_goal_request(
            "Write goal.md and completion.md as drafts; do not activate them."
        )
        self.assertEqual(result["intent"], "draft")
        self.assertFalse(result["requires_native_readback"])

    def test_explicit_adoption_requires_native_readback(self):
        result = state_guards.classify_goal_request(
            "Set/adopt these as your goal and completion criteria."
        )
        self.assertEqual(result["intent"], "adopt")
        self.assertTrue(result["requires_native_readback"])
        self.assertIn("get_goal", result["native_action"])

    def test_explicit_adoption_wins_over_document_words(self):
        result = state_guards.classify_goal_request(
            "Write goal.md, then configure it as the native goal; do not just edit files."
        )
        self.assertEqual(result["intent"], "adopt")

    def test_make_this_your_goal_is_explicit_adoption(self):
        result = state_guards.classify_goal_request("Make this your native goal and use these criteria.")
        self.assertEqual(result["intent"], "adopt")

    def test_make_a_goal_file_stays_document_only(self):
        result = state_guards.classify_goal_request("Make a goal file from this brief and leave it as a draft.")
        self.assertEqual(result["intent"], "draft")

    def test_negated_make_does_not_activate(self):
        result = state_guards.classify_goal_request("Do not make this the native goal; save it as a proposal.")
        self.assertEqual(result["intent"], "draft")

    def test_unrelated_request_is_quiet(self):
        result = state_guards.classify_goal_request("Fix the obvious button label.")
        self.assertEqual(result["intent"], "unrelated")
        self.assertFalse(result["requires_native_readback"])

    def test_null_goal_requires_create_and_readback(self):
        result = state_guards.goal_action(None, "Goal text")
        self.assertEqual(result["action"], "create_goal")
        self.assertFalse(result["can_report_success"])

    def test_completed_goal_can_be_replaced_without_closing_unfinished_work(self):
        result = state_guards.goal_action({"status": "complete", "objective": "old"}, "new")
        self.assertEqual(result["action"], "create_goal")

    def test_active_mismatch_requires_supported_update(self):
        result = state_guards.goal_action({"status": "active", "objective": "old"}, "new")
        self.assertEqual(result["action"], "supported_update_required")
        self.assertFalse(result["can_report_success"])
        self.assertIn("unfinished", result["reason"])

    def test_active_match_is_verified_not_duplicated(self):
        result = state_guards.goal_action({"status": "active", "objective": "same"}, "same")
        self.assertEqual(result["action"], "verify_existing_goal")

    def test_paused_goal_preserves_pause(self):
        result = state_guards.goal_action({"status": "active", "objective": "old"}, "new", paused=True)
        self.assertEqual(result["action"], "preserve_pause")
        self.assertFalse(result["can_report_success"])

    def test_native_readback_requires_active_matching_objective(self):
        self.assertTrue(state_guards.verify_goal_readback(
            {"status": "active", "objective": "Goal text", "threadId": "t1"},
            "Goal text", thread_id="t1"
        )["verified"])
        mismatch = state_guards.verify_goal_readback(
            {"status": "complete", "objective": "other", "threadId": "t2"},
            "Goal text", thread_id="t1"
        )
        self.assertFalse(mismatch["verified"])
        self.assertEqual(len(mismatch["issues"]), 3)


class TitleGuardTests(unittest.TestCase):
    def test_blocking_adds_one_prefix(self):
        self.assertEqual(state_guards.normalize_title("Preview", True), "🛑 Preview")

    def test_duplicate_prefixes_collapse(self):
        self.assertEqual(state_guards.normalize_title("🛑 🛑 Preview", True), "🛑 Preview")

    def test_clearing_removes_only_owned_prefix(self):
        self.assertEqual(state_guards.normalize_title("🛑 Renamed Preview", False), "Renamed Preview")

    def test_rename_while_blocked_is_preserved(self):
        result = state_guards.title_update("🛑 Preview — candidate B", True)
        self.assertEqual(result["desired"], "🛑 Preview — candidate B")
        self.assertFalse(result["changed"])

    def test_unblocked_title_does_not_gain_prefix(self):
        self.assertEqual(state_guards.title_update("Preview", False)["desired"], "Preview")


class EventAndCliTests(unittest.TestCase):
    def test_event_contains_action_and_title_plan_without_mutation(self):
        event = state_guards.inspect_event({
            "prompt": "Adopt these as the goal and completion criteria.",
            "current_goal": None,
            "expected_objective": "Accepted objective",
            "title": "Preview",
            "assignment_blocked": True,
        })
        self.assertEqual(event["goal"]["action"], "create_goal")
        self.assertEqual(event["title"]["desired"], "🛑 Preview")

    def test_cli_emits_structured_decision(self):
        event = {
            "prompt": "Set this as the native goal and completion criteria.",
            "current_goal": {"status": "active", "objective": "old"},
            "expected_objective": "new",
        }
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts/state_guards.py")],
            input=json.dumps(event), text=True, capture_output=True, check=True,
        )
        result = json.loads(proc.stdout)
        self.assertEqual(result["goal"]["action"], "supported_update_required")

    def test_hook_adds_native_adoption_gate_for_explicit_request(self):
        result = hook_context.context_for_event(
            {"hook_event_name": "UserPromptSubmit",
             "prompt": "Set/adopt this as the goal and completion criteria."},
            "/tmp/AGENTS.md",
        )
        text = result["hookSpecificOutput"]["additionalContext"]
        self.assertIn("get_goal", text)
        self.assertIn("read back", text)
        self.assertIn("Do not report adoption", text)
        self.assertIn("Do not mark the goal complete", text)

    def test_hook_keeps_document_request_draft_only(self):
        result = hook_context.context_for_event(
            {"hook_event_name": "UserPromptSubmit",
             "prompt": "Write goal.md and completion.md; do not activate them."},
            "/tmp/AGENTS.md",
        )
        self.assertIn("document-only", result["hookSpecificOutput"]["additionalContext"])

    def test_hook_title_guidance_does_not_infer_blocker(self):
        result = hook_context.context_for_event(
            {"hook_event_name": "UserPromptSubmit",
             "prompt": "The title says Preview but I am not blocked."},
            "/tmp/AGENTS.md",
        )
        text = result["hookSpecificOutput"]["additionalContext"]
        self.assertIn("establish a genuine current blocker first", text)

    def test_hook_ignores_unrelated_events(self):
        self.assertIsNone(hook_context.context_for_event(
            {"hook_event_name": "PreToolUse", "prompt": "Set the goal"}, "/tmp/AGENTS.md"
        ))


if __name__ == "__main__":
    unittest.main()
