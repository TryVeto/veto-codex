"""Pure guards for native goal adoption and blocked-title updates.

The host owns goals and task titles.  These helpers only classify intent,
describe the supported next action, verify a native readback and calculate a
single stop-sign prefix.  They never call a host API, write a file or infer a
state change from prose alone.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any


STOP_PREFIX = "🛑 "

# This classifier is a routing hint, never an authorization decision. Only a
# direct, unquoted request may reach the native-goal procedure. Ambiguity takes
# the non-mutating path; the receiving agent still checks the actual user turn.
_DIRECT = re.compile(
    r"^(?:(?:please|then)\s+|(?:can|could|would)\s+you\s+)*"
    r"(?:(?:set(?:/adopt)?|adopt|activate|configure|update|replace)\b.{0,100}"
    r"\b(?:(?:native|current)\s+)?goal\b|"
    r"make\s+(?:this|that|it)\s+(?:your\s+|the\s+)?"
    r"(?:(?:native|current)\s+)?goal\b)", re.I,
)
_GOAL = re.compile(r"\b(?:goals?|completion(?:\.md|\s+criteria?))\b", re.I)
_NON_EXECUTING = re.compile(
    r"\b(?:review|explain|discuss|quote|hypothetical|example|documentation|"
    r"what\s+does|how\s+(?:to|do|would)|not\s+asking)\b|"
    r"\b(?:do\s+not|don't|never|without)\s+(?:actually\s+)?"
    r"(?:execute|activate|set|adopt|configure|make|resume|replace|update)\b", re.I,
)


def _text(value: Any) -> str:
    return value if isinstance(value, str) else ""


def _normalized(value: Any) -> str:
    return " ".join(_text(value).replace("\r\n", "\n").replace("\r", "\n").split())


def _unquoted(value: str) -> str:
    # Remove code, quoted lines and quoted strings before looking for a command.
    # Unclosed code is also treated as quoted rather than as a new instruction.
    value = re.sub(r"```[\s\S]*?(?:```|$)|~~~[\s\S]*?(?:~~~|$)", " ", value)
    value = re.sub(r"(?m)^\s*>.*$", " ", value)
    value = re.sub(r'`[^`]*`|"[^"\n]*"|“[^”]*”|‘[^’]*’', " ", value)
    value = re.sub(r"(?<!\w)'[^'\n]+'(?!\w)", " ", value)
    return value


def classify_goal_request(prompt: str) -> dict[str, Any]:
    """Return a conservative routing hint. It cannot confer native authority."""
    original = _text(prompt)
    result: dict[str, Any] = {"intent": "unrelated", "requires_native_readback": False,
                              "authorization_established": False}
    if not _GOAL.search(original):
        return result
    text = _unquoted(original).replace("’", "'")
    # A mixed request containing review/negation is deliberately not auto-routed
    # to mutation. False negatives are preferable to false permission claims.
    if _NON_EXECUTING.search(text):
        result["intent"] = "draft"
        return result
    clauses = re.split(r"[;\n]|(?:,?\s+then\s+)", text)
    for clause in clauses:
        clause = clause.strip()
        if _DIRECT.search(clause) and not re.search(r"\bgoal(?:\.md|\s+file)\b", clause, re.I):
            result.update(intent="adopt", requires_native_readback=True,
                          native_action="get_goal_then_supported_update_or_create_goal")
            return result
    result["intent"] = "draft"
    return result


def goal_action(current_goal: Any, expected_objective: str, *, paused: bool = False) -> dict[str, Any]:
    """Choose a safe native action from a current readback.

    An active mismatching goal is deliberately not replaced here: callers must
    use a host-supported update operation, and must never close an unfinished
    goal merely to make room for a new one.
    """
    expected = _normalized(expected_objective)
    if not expected:
        return {"action": "inspect_native_goal", "can_report_success": False,
                "reason": "A nonempty accepted objective is required before planning a change."}
    if type(paused) is not bool:
        return {"action": "inspect_native_goal", "can_report_success": False,
                "reason": "Paused must be a boolean; do not coerce unknown state."}
    if paused:
        return {"action": "preserve_pause", "can_report_success": False,
                "reason": "The task is explicitly paused; adoption must not resume it."}
    if current_goal is None:
        return {"action": "create_goal", "can_report_success": False,
                "reason": "No native goal is present; create it and read it back."}
    if not isinstance(current_goal, dict):
        return {"action": "inspect_native_goal", "can_report_success": False,
                "reason": "Native goal readback is malformed."}
    status = _text(current_goal.get("status")).lower()
    current = _normalized(current_goal.get("objective"))
    if "paused" in current_goal and type(current_goal["paused"]) is not bool:
        return {"action": "inspect_native_goal", "can_report_success": False,
                "reason": "Native pause state is malformed."}
    if status in {"paused", "blocked", "waiting", "stopped"} or current_goal.get("paused") is True:
        return {"action": "preserve_pause", "can_report_success": False,
                "reason": "Preserve the observed stop; adoption must not resume it."}
    if status == "complete":
        return {"action": "create_goal", "can_report_success": False,
                "reason": "The prior goal is complete; create the new goal and read it back."}
    if status == "active" and current == expected:
        return {"action": "verify_existing_goal", "can_report_success": False,
                "reason": "The requested objective already matches; verify the same native goal."}
    if status == "active":
        return {"action": "supported_update_required", "can_report_success": False,
                "reason": "An unfinished native goal differs; no unsafe close-and-replace is permitted."}
    return {"action": "inspect_native_goal", "can_report_success": False,
            "reason": "Native goal status is unknown; inspect before changing it."}


def verify_goal_readback(after: Any, expected_objective: str, *, thread_id: str | None = None) -> dict[str, Any]:
    """Verify the native goal postcondition needed for an adoption claim."""
    issues: list[str] = []
    expected = _normalized(expected_objective)
    if not expected:
        issues.append("accepted objective must be nonempty")
    if not isinstance(thread_id, str) or not thread_id.strip():
        issues.append("expected task identity is required")
    if not isinstance(after, dict):
        issues.append("native goal readback is not an object")
        return {"verified": False, "issues": issues}
    if _text(after.get("status")).lower() != "active":
        issues.append("native goal is not active")
    current = _normalized(after.get("objective"))
    if not current:
        issues.append("observed objective must be nonempty")
    elif expected and current != expected:
        issues.append("native objective does not match the accepted objective")
    if "paused" in after and type(after["paused"]) is not bool:
        issues.append("native pause flag is not a boolean")
    elif after.get("paused") is True:
        issues.append("native readback is paused, not active")
    if isinstance(thread_id, str) and thread_id.strip() and _text(after.get("threadId")) != thread_id:
        issues.append("native readback is for a different task")
    return {"verified": not issues, "issues": issues}


def normalize_title(title: str, blocked: bool) -> str:
    """Add/remove only the automation-owned leading stop-sign prefix."""
    value = _text(title)
    base = re.sub(r"^(?:🛑[ \t])+", "", value)
    return (STOP_PREFIX + base) if blocked else base


def title_update(title: str, blocked: bool) -> dict[str, Any]:
    desired = normalize_title(title, blocked)
    return {"current": _text(title), "desired": desired, "changed": desired != _text(title),
            "blocked": bool(blocked), "prefix": STOP_PREFIX}


def inspect_event(event: dict[str, Any]) -> dict[str, Any]:
    """Return a host-facing decision record without performing a mutation."""
    prompt = _text(event.get("prompt"))
    request = classify_goal_request(prompt)
    result: dict[str, Any] = {"request": request}
    if request["intent"] == "adopt":
        expected = _text(event.get("expected_objective"))
        if "current_goal" not in event:
            result["goal"] = {"action": "inspect_native_goal", "can_report_success": False,
                              "reason": "Missing readback is not an observed empty goal."}
        else:
            result["goal"] = goal_action(event["current_goal"], expected,
                                          paused=event.get("paused", False))
        if "readback" in event:
            result["readback"] = verify_goal_readback(event.get("readback"), expected,
                                                       thread_id=event.get("thread_id"))
    if "title" in event and "assignment_blocked" in event:
        if type(event["assignment_blocked"]) is not bool:
            result["title"] = {"changed": False, "error": "assignment_blocked must be a boolean"}
        else:
            result["title"] = title_update(_text(event.get("title")), event["assignment_blocked"])
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--event", type=argparse.FileType("r"), default=sys.stdin,
                        help="JSON event containing prompt/state; output is a decision record")
    args = parser.parse_args()
    try:
        event = json.load(args.event)
        if not isinstance(event, dict):
            raise ValueError("event must be an object")
        print(json.dumps(inspect_event(event), ensure_ascii=False, indent=2))
        return 0
    except (ValueError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"verdict": "INVALID", "error": str(exc)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
