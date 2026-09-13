#!/usr/bin/env python3
"""Check a bounded work handoff without resuming work or accepting a deliverable.

Read-only; no host calls, subprocesses, network, recursive source collection or
writes. Hashes bind the declared files, not all files in a checkout. A passing
result establishes integrity, not truth, authorship, authority or agent loading.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from common import HEX256, digest, exact_keys, load_json, local_file, nonempty, ordinary_path

STATES = {"active", "paused", "blocked", "ready_for_review"}
KINDS = {"request", "decision", "candidate", "evidence"}
LIMITS = [
    "Only declared files were checked; no complete-checkout identity is established.",
    "A hash does not prove execution, authorship, independent review or source truth.",
    "Read current native state and authority before continuing; this helper grants neither.",
]


def strings(value: Any, label: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not value and not allow_empty):
        raise ValueError(f"{label} must be a {'possibly empty' if allow_empty else 'nonempty'} list.")
    for item in value:
        nonempty(item, label)
    if len(set(value)) != len(value):
        raise ValueError(f"{label} contains duplicates.")
    return value


def validate(record: dict[str, Any]) -> dict[str, dict[str, Any]]:
    exact_keys(record, {"schema_version", "task_id", "assignment_revision", "owner", "outcome",
                        "state", "candidate_id", "must_preserve", "next_action", "resume_condition",
                        "references", "completed", "remaining"}, {"decision_return"}, "handoff")
    if type(record["schema_version"]) is not int or record["schema_version"] != 1:
        raise ValueError("Unsupported handoff schema_version.")
    if type(record["assignment_revision"]) is not int or record["assignment_revision"] < 1:
        raise ValueError("assignment_revision must be a positive integer.")
    for key in ("task_id", "owner", "outcome", "candidate_id", "next_action", "resume_condition"):
        nonempty(record[key], key)
    if not isinstance(record["state"], str) or record["state"] not in STATES:
        raise ValueError("Invalid handoff state. Handoffs cannot declare acceptance or completion.")
    strings(record["must_preserve"], "must_preserve")
    strings(record["remaining"], "remaining", allow_empty=True)
    refs = record["references"]
    if not isinstance(refs, list) or not refs:
        raise ValueError("references must be a nonempty list.")
    by_id: dict[str, dict[str, Any]] = {}
    paths: set[str] = set()
    for ref in refs:
        exact_keys(ref, {"id", "kind", "path", "sha256"}, set(), "reference")
        key = nonempty(ref["id"], "reference.id")
        path = nonempty(ref["path"], "reference.path")
        if key in by_id or path in paths:
            raise ValueError("Duplicate reference identity or path.")
        if not isinstance(ref["kind"], str) or ref["kind"] not in KINDS:
            raise ValueError("Invalid reference kind.")
        if not isinstance(ref["sha256"], str) or not HEX256.fullmatch(ref["sha256"]):
            raise ValueError("Invalid reference sha256.")
        by_id[key] = ref
        paths.add(path)
    kinds = {r["kind"] for r in refs}
    if not {"request", "candidate"} <= kinds:
        raise ValueError("A handoff needs the original request and candidate file references.")
    completed = record["completed"]
    if not isinstance(completed, list):
        raise ValueError("completed must be a list.")
    completed_ids: set[str] = set()
    for row in completed:
        exact_keys(row, {"id", "result", "evidence_ids"}, set(), "completed row")
        key = nonempty(row["id"], "completed.id")
        if key in completed_ids:
            raise ValueError("Duplicate completed result ID.")
        completed_ids.add(key)
        nonempty(row["result"], "completed.result")
        for evidence_id in strings(row["evidence_ids"], "evidence_ids"):
            if evidence_id not in by_id or by_id[evidence_id]["kind"] != "evidence":
                raise ValueError("Completed work needs an evidence reference, not a source assertion.")
    if record["state"] == "ready_for_review" and not completed:
        raise ValueError("ready_for_review needs at least one evidenced result.")
    if "decision_return" in record:
        decision = exact_keys(record["decision_return"],
                              {"status", "source_id", "stays", "changes", "credited", "next_result"},
                              set(), "decision return")
        if decision["status"] not in ("proposed", "adopted"):
            raise ValueError("Decision status must be proposed or adopted.")
        source_id = nonempty(decision["source_id"], "decision source_id")
        if source_id not in by_id or by_id[source_id]["kind"] != "decision":
            raise ValueError("Decision return needs the exact source decision.")
        for key in ("stays", "changes", "credited"):
            strings(decision[key], "decision." + key, allow_empty=True)
        nonempty(decision["next_result"], "decision.next_result")
    return by_id


def check(record_path: Path, root: Path, *, expected_task_id: str,
          expected_revision: int, trusted_sha256: str) -> dict[str, Any]:
    nonempty(expected_task_id, "expected task ID")
    if type(expected_revision) is not int or expected_revision < 1:
        raise ValueError("Expected revision must be a positive integer.")
    if not isinstance(trusted_sha256, str) or not HEX256.fullmatch(trusted_sha256):
        raise ValueError("A trusted handoff SHA-256 from the delivery record is required.")
    root = ordinary_path(root, directory=True)
    record_path = ordinary_path(record_path)
    result: dict[str, Any] = {"verdict": "NEEDS_RECONCILIATION", "issues": [],
                              "native_state_verified": False, "permission_granted": False,
                              "runtime_action": "none", "limits": LIMITS}
    if digest(record_path) != trusted_sha256:
        result["issues"].append("Handoff changed from the pinned delivery digest.")
        return result  # Do not return untrusted instructions from a changed record.
    record = load_json(record_path)
    refs = validate(record)
    if record["task_id"] != expected_task_id:
        result["issues"].append("Handoff belongs to a different task.")
    if record["assignment_revision"] != expected_revision:
        result["issues"].append("Handoff belongs to a different assignment revision.")
    resolved_paths: set[Path] = set()
    for ref in refs.values():
        try:
            path = local_file(root, ref["path"])
            if path in resolved_paths:
                raise ValueError("Two references alias the same file.")
            resolved_paths.add(path)
            if path.stat().st_size == 0 and ref["kind"] != "candidate":
                raise ValueError("Request, decision and evidence files cannot be empty.")
            if digest(path) != ref["sha256"]:
                raise ValueError("File changed from the pinned reference digest.")
        except (ValueError, OSError) as exc:
            result["issues"].append(ref["id"] + ": " + str(exc))
    if result["issues"]:
        return result
    result.update(verdict="HANDOFF_INTEGRITY_PASSED", task_id=record["task_id"],
                  assignment_revision=record["assignment_revision"], owner=record["owner"],
                  recorded_state=record["state"], declared_candidate_id=record["candidate_id"],
                  references_checked=len(refs), completed=record["completed"],
                  remaining=record["remaining"], must_preserve=record["must_preserve"],
                  next_action=record["next_action"], resume_condition=record["resume_condition"])
    if record["state"] == "paused":
        result["verdict"] = "PRESERVE_PAUSE"
    elif record["state"] == "blocked":
        result["verdict"] = "BLOCKER_RECORDED"
    if "decision_return" in record:
        result["decision_return"] = record["decision_return"]
        result["decision_authority_authenticated"] = False
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", type=Path, required=True)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--revision", type=int, required=True)
    parser.add_argument("--sha256", required=True, help="Digest from the original delivery record, not the file itself")
    args = parser.parse_args()
    try:
        result = check(args.record, args.root, expected_task_id=args.task_id,
                       expected_revision=args.revision, trusted_sha256=args.sha256)
    except (ValueError, OSError, UnicodeError, TypeError, KeyError) as exc:
        print(json.dumps({"verdict": "INVALID", "error": str(exc), "runtime_action": "none"}))
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if result["issues"] else 0


if __name__ == "__main__":
    sys.exit(main())
