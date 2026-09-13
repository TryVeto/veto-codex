# Check the final integrated candidate

Use this when a branch is rebased, retargeted, squashed, merged, or rebuilt with a changed
configuration before acceptance. The owner is the agent integrating the work; a separate
run supplies independent acceptance where required.

A stable patch-id can show that a diff is textually equivalent. It does not show that the
surrounding application, dependency, configuration, schema, or behavior is equivalent.
Do not let an unchanged patch reuse a stale runtime verdict.

## Carry review analysis; renew decisive proof

Keep useful code-review findings. Record the exact final commit/tree, base, lockfile,
build/configuration identity, data scope, and the acceptance path under review. Rebuild
or launch the integrated candidate using the working repository’s maintained harness.
Replay the behavior that would accept or reject the original request on that candidate.

For Veto, consult the product repository’s existing `verify-veto` skill, `control-veto`
commands, and Feature Map. Do not clone them into this plugin or run those nonproduction
controls against production. Follow the separate approved production procedure when it
is actually in scope.

Ask a fresh reviewer to inspect the same artifact and original acceptance condition.
Give it direct evidence access, not only the builder’s verdict. If the integrated path
fails, keep the failure and stop that dependent delivery. An unrelated passing PR cannot
make the failed dependency acceptable.

## Small test that should fail

Consider a patch adding a `ready` badge when a shared setting equals `true`. The patch
can remain identical while the base changes that setting’s meaning or default. A limited
unit suite can stay green; the displayed behavior changes. The decisive observation is
the badge in the integrated application, not the patch’s hash.

This is a qualification scenario, not a claim that such a defect exists in Veto.
Add the corresponding local behavior test only where the actual implementation needs it.

## Record

Keep the old analysis, the old candidate identity, the new candidate identity, the exact
replay command/path, observed result, reviewer run, and remaining limits. A checker that
validates these fields has checked a record; it has not performed the replay or authenticated
the reviewer. No native or product replay was run while building this repository release.
