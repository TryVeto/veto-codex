# Good enough engineering: protect the promise, keep change affordable

Use for an actual code change, engineering review, or delivery-system repair. This
adapts the supplied coding-standards, code-quality and CI/CD studies; it is not an
audit of the running repository or a new production gate. Follow the actual
repository policy. Source distinctions and page references are in the
[engineering update note](../research/ENGINEERING-PATCH.md).

## Choose checks by consequence

Preserve a simple implementation that satisfies the whole requirement. Spend more
scrutiny on authority, sensitive data, durable records, concurrent effects and
recovery than on incidental style. A one-line authorization change can matter more
than a large mechanical diff. Do not require a framework, coverage percentage,
rewrite, or new reviewer ceremony to make an ordinary change acceptable.

Before editing, inspect the actual commands, lockfile, relevant rules and current
changes. Separate **obligations**, **guidelines** and **preferences**. A mandatory
repository check remains mandatory; a reviewer's preferred abstraction does not
become a release blocker. Preserve the strongest competent existing implementation.
Improve the touched boundary with a ratchet, not a repository-wide cleanup campaign.

| Changed boundary | Evidence to select, in addition to existing required gates |
|---|---|
| Copy or local visual adjustment | Exact meaning and allowed scope; rendered affected state and relevant accessibility. No unrelated architecture project. |
| Shared field, status or component | Its contract plus representative consumers; ordinary correction and persistence if represented; buyer/participant consequences where shared. |
| Authorization, evidence or durable state | Allowed and denied server paths; actual object/office scope; stale basis, duplicate/concurrent work and valid repair as relevant. |
| Schema or integration | Existing-record behavior, compatibility, migration interruption/retry and destination reconciliation; a viable recovery path. |
| Runtime, build or CI | Expected checks discovered and executed; nonsecret configuration, packaged-runtime startup, candidate identity and relevant recovery. |

These are selection rules, not a mandatory Cartesian product. A table row does
not waive other accepted requirements. Investigate unknown blast radius; do not
automatically label it low risk. A supported source-level defect need not be
reproduced against live data, but label that evidence layer. Keep unreproduced
behavior and hypotheses distinct from observed execution.

## Keep the implementation honest

Use existing formatting, types, validators, components and tests. Names and types
should expose important units, identity and state distinctions; broad casts,
suppressions and catch-and-succeed fallbacks must not hide an unmet contract.
Validate untrusted inputs at the real boundary. Keep important shared policy in one
maintained place; tolerate harmless local repetition rather than inventing an
unstable universal abstraction.

Put durable invariants in durable mechanisms: applicable constraints, transactions,
conditional writes and a defined concurrency policy. A check-then-insert sequence
is not automatically safe against simultaneous requests. Inspect the actual storage
semantics. Await essential work or hand it to an existing durable mechanism; an
unawaited promise is not dependable follow-through.

Distinguish a known failure from an unknown remote outcome. Bound external work
and retries. Reconcile a consequential operation using its original identity;
a new retry key can create a new act. A local deduplication flag cannot establish
exactly-once behavior at an arbitrary provider. Saved review, issued edition,
notification and filing have different recovery paths.

Protect actor, office, object and action in trusted server paths, including affected
exports, downloads, background work and retrieval of a prior idempotent result.
Knowing an operation key does not grant access to its saved response. Preserve canonical evidence and immutable
issued history. Keep NPI and secrets out of ordinary logs; use allowlisted,
sanitized diagnostics. UI simplification never creates professional or bank authority.

## Keep the delivery system small and truthful

Use repository-owned verification logic through the existing runner. Keep quick
edit feedback, required integration checks, packaged-runtime checks and an approved
staging review distinct. Reuse the existing provider and cost constraints; this is
not permission to create GitHub Actions spend or migrate infrastructure.

A green job is insufficient when no relevant tests were discovered, a required job
was skipped, a wrapper swallowed the failure, or results describe another candidate.
Compare required work with executed work. Retain first failures, retries, flakes,
skips and explicit exemptions. A retry that passes does not retroactively become a
clean first attempt. Preserve a first-attempt or full safe-core requirement **where
current repository policy actually requires it**; historical reports are not newly
adopted universal gates.

When selecting checks, an unknown merge base or changed shared/pipeline logic
needs wider coverage or a stated blocker—not an empty green run. Verify the
required check identity, trusted producer and protected policy, not a matching
label alone. A proposed CI-provider cutover does not remove the active gate:
qualify the replacement on the relevant integrated candidate, inspect actual
enforcement and preserve rollback before the authorized switch. Avoid circular
gates and permissive “either provider passed” shortcuts. Cancel superseded
stateless validation where safe; reconcile mutating deployment or migration
attempts instead of treating cancellation as undo.

Pin source, relevant dirty inputs, integration base, lockfile, artifact/build,
nonsecret configuration, migration/flag state and target as the claim needs. Prefer
promoting the tested artifact when supported. If preview and production are rebuilt,
record the difference and qualify the actual target rather than claiming identical
bytes. A source SHA alone does not identify runtime configuration or data schema.

One owner controls a shared staging candidate while it is verified. Another worker
must not replace it beneath a review. Use existing serialization or supported
ownership mechanisms; do not build a lease platform merely to write this receipt.
Unreviewed candidate code must not get production secrets or silently modify the
trusted checks by which it is accepted.

For a durable change, establish the compatible recovery target or forward-repair
path. Expand/migrate/contract when compatibility requires it; do not force that
sequence on harmless changes. Exercise meaningful interruption and existing-data
cases in disposable environments. Rolling back code cannot unsend a message,
reverse every migration, recover disclosed data, or undo money movement.

## Close the actual change

Audit the originals against the acceptance contract, then the contract against
observed results. Never make an obsolete assertion permanent, but change a test
only with evidence of its error or a valid requirement change; preserve the original
failure and remaining coverage. Do not refresh snapshots or reduce scanner scope
to manufacture a pass.

In the existing PR/work record retain the candidate, changed behavior, commands and
results, expected/executed coverage, significant first failures, relevant latency
samples and accepted budgets, compatibility/recovery, and missing exposure gates.
Do not invent a performance threshold or create a second release ledger.

End at the authorized endpoint. Implementation, staging evidence, production
approval, deployment and observed usefulness are separate. For an explicitly
requested production check, use [bounded production verification](production-verification.md),
not ordinary local credentials. The next proof is one complete useful change,
not a larger standards manual. For preview/release handoffs, apply
[candidate-bound delivery](preview-and-release.md) through the maintained repository
path. The [1108 source note](../research/DELIVERY-PATCH.md) records the incremental
coding/CI guidance and its limits.
