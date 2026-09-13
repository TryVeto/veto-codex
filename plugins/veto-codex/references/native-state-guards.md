# Native goal and blocked-title guards

The host owns runtime state. These helpers produce local hints and verify declared
readbacks; they cannot perform a native mutation or authenticate an authorization.

## Language is not permission

`classify_goal_request` routes only narrow unquoted direct forms toward the native
procedure. It returns `authorization_established: false` even for those forms.
Quoted/code-block examples, explanations, negations and ambiguous mixed requests
stay on a non-mutating path. The classifier is intentionally incomplete: a receiving
agent must inspect the actual current user instruction and source context before
any consequential operation. A false negative is not a reason to pretend the user
gave a new request; read the instruction and use judgment within the actual mandate.

The reminder says a native change is **possible, not authorized**. No hook is
registered by this package. An existing external wrapper may use the adapter only
through its already-authorized host configuration; inspect that installation
separately. A reference to a tool name does not mean the current host exposes it.

## Native adoption, only when actually requested

Read the current task and goal with the supported host control. Missing input is not
proof that no goal exists. Preserve an observed pause, stop, blocked state and all
unfinished obligations. Verify a nonempty accepted objective before planning an act.

Use only an exposed create/update operation appropriate to that readback. An active
unfinished goal must not be closed to make room for another. If update is unsupported,
preserve the existing goal and state the limitation. A goal document is not adoption.

Read back the same task after the operation. `verify_goal_readback` requires an
explicit nonempty expected task ID, nonempty expected and observed objectives,
a matching objective, active status and no contradictory pause. A supplied pause
flag must be a boolean. An empty objective matching another empty value cannot pass.

The expected task/objective must come from the accepted request and pre-operation
native context, not be copied from the post-operation readback to force a match.
A valid returned object is still a caller-supplied object; the agent must establish
its actual native source. Reconcile uncertain effects before another attempt.

## Blocked-title display

Where the actual host supports title read/write, establish the genuine blocker,
read the latest title and add/remove only the automation-owned leading stop-sign
prefix. Preserve the base title and any concurrent rename. Repeated application
must not add duplicate prefixes. Read back the title after a permitted mutation.

A paused/idle task is not automatically blocked. A prompt containing "blocked" is
not a current-state observation. The event helper refuses nonboolean
`assignment_blocked` values instead of treating the string "false" as true.
A title is visibility, never permission to resume or release.

## Limits

`state_guards.py` reads a JSON event from stdin or an explicit file and returns a
plan. `hook_context.py` returns reminder text only. Neither calls host APIs, writes
files, schedules work or establishes that an agent followed the reminder. Unit tests
cover these deterministic behaviors; native behavior remains a separate test.
