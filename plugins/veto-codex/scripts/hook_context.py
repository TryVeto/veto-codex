"""Build the existing prompt-hook reminder from current task intent.

This is a reminder adapter, not an enforcement service. It has no host API,
filesystem mutation or title writer. The host-facing compatibility entry point
can call it so one existing hook carries the native action/readback boundary.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from state_guards import classify_goal_request


def context_for_event(event: dict[str, Any], instructions: str) -> dict[str, Any] | None:
    name = event.get("hook_event_name")
    if name != "UserPromptSubmit" and not (name == "SessionStart" and event.get("source") == "compact"):
        return None
    policy = Path(instructions)
    reminder = (
        f"Checkpoint: follow the current title, pinning, goal and communication rules in {policy}. "
        "Reuse current context and native state; read only missing sections. "
        "Preserve the active assignment, explicit stops, existing authority and other owners. "
        "For Veto UI work, use the shared v10 design reference named there. "
        "Bounded subagents do not administer the parent task. "
        "This reminder does not change goals, settings or permissions."
    )
    prompt = event.get("prompt", "")
    intent = classify_goal_request(prompt)
    if intent["intent"] == "adopt":
        reminder += (
            " Possible native-goal request, not established authorization: first inspect the current user's unquoted, non-hypothetical instruction and any explicit negation. Only if it actually authorizes this change, call get_goal first and use only a supported "
            "create/update operation, then read back the same task's objective and state. "
            "Do not report adoption from goal.md/completion.md files or an adopted label. "
            "Do not mark the goal complete unless the user explicitly authorizes completion "
            "and the accepted criteria are evidenced. Do not close an unfinished goal; if "
            "replacement is unsupported, report the native goal as unchanged."
        )
    elif intent["intent"] == "draft":
        reminder += (
            " Treat this as a document-only or discussion request unless the current user clearly asks to "
            "activate it; writing the files does not change native task state."
        )
    if any(word in str(prompt).lower() for word in ("blocked", "stop sign", "stop-sign", "title")):
        reminder += (
            " For a blocked-title update, establish a genuine current blocker first, "
            "read the current title, add or remove only one automation-owned '🛑 ' prefix "
            "with set_thread_title, and read the title back. Do not infer a blocker from "
            "this prompt or turn a pause/idle state into a stop sign."
        )
    return {"hookSpecificOutput": {"hookEventName": name, "additionalContext": reminder}}


def main() -> int:
    import argparse
    import sys

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--instructions", default=str(Path.home() / ".codex" / "AGENTS.md"))
    args = parser.parse_args()
    try:
        event = json.loads(sys.stdin.read(1_000_000))
    except (ValueError, OSError):
        return 0
    if not isinstance(event, dict):
        return 0
    result = context_for_event(event, args.instructions)
    if result is not None:
        print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
