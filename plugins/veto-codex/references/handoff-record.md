# A checked record for interrupted work

Optional for a substantial handoff. Keep it in the existing project/work directory,
not the plugin, and reuse your present record when it is already sufficient. This
is a read-only integrity helper, not a task database, scheduler or authority engine.

Start from [the worked synthetic record](../examples/resume-work/handoff.json).
Preserve the original request, candidate files and evidence using relative POSIX
paths under a declared working root. No symlinks, parent traversal or remote URLs.
Each reference has an ID, kind, path and SHA-256. Each credited result identifies
actual evidence; an assertion in the original brief is not completion evidence.
Candidate identity is a declared label; hashes cover only the files listed.

The schema preserves task, assignment revision, owner, outcome, state, constraints,
credited work, remaining work, next action and resume condition. An optional decision
return carries proposed/adopted status, its source, what stays, what changes, what
is credited and the next result. These are recorded claims, not authenticated acts.
Native goals, current authority and the accepted contract remain authoritative.

The sender supplies the record's hash, task ID and assignment revision in the
existing handoff channel. The receiver obtains those expected values from that
channel—not by trusting the file being checked—and runs:

```sh
python3 -B /path/to/veto-codex/scripts/check_handoff.py \
  --record /path/to/work/handoff.json --root /path/to/work \
  --task-id accepted-task-id --revision 1 --sha256 DIGEST_FROM_HANDOFF
```

Exit 0 means a consistent record (including a preserved pause or recorded blocker).
Exit 1 means changed/missing evidence or task/revision mismatch; exit 2 means invalid
input. Do not interpret any exit code as permission to resume or accept work.
On mismatch the helper does not return next-action text from the changed record.

`HANDOFF_INTEGRITY_PASSED` means only that the declared bytes and record match.
`PRESERVE_PAUSE` retains the recorded stop. `BLOCKER_RECORDED` retains a dependency.
None starts an agent. Before any new effect, read current host state and confirm the
mandate/owner are still valid. Check unlisted dependencies and configuration where
needed. A later pause overrides an older active packet.

No record state can declare accepted/done. Use the existing acceptance contract,
`check_receipt.py` and required independent replay for completion. If the file is
stale, reconcile the change and issue an attributable revised handoff; do not simply
update the trusted hash to suppress the failure.

Privacy: list only the files needed for continuation. Do not include credentials,
private client stores or unrelated transcripts. This helper reads only declared
paths and does not crawl a home directory, copy files, make network calls or write.
The underlying filesystem remains trusted; this is not a hostile-filesystem sandbox.
