# Git: preserve the work and its identity

Use for a source handoff, branch/worktree problem, PR integration, rejected push,
recovery or cleanup. A routine edit needs the relevant checks, not a repository
reorganization. An audit remains read-only. Commit, publish, merge and deploy are
separate endpoints under the current mandate; use existing grants without asking
again for each ordinary step.

This adapts the supplied **Veto Git** skill and *What your Git should look like*.
Their repository observations are dated snapshots, not a live-state certificate.
[Source decisions](../research/IDENTITY-GIT-PATCH.md) retain the provenance.

## 1. Establish the actual workspace

Read applicable repository instructions and the accepted task. Identify the repository,
base, current HEAD, intended integration target, writer and permitted endpoint. In a
trusted local checkout, these are inspection commands, not a setup/cleanup script:

```sh
git rev-parse --show-toplevel
git status --short --branch --untracked-files=all
git branch --show-current
git rev-parse --verify HEAD
git worktree list --porcelain
git diff --no-ext-diff --no-textconv --stat
git diff --no-ext-diff --no-textconv --cached --stat
```

Inspect intended untracked contents separately. Do not print credential-bearing
remotes, secrets or private records into evidence. Remote-tracking refs can be stale;
a permitted fetch contacts the remote and changes local refs, but does not integrate
the fetched source. No automatic pruning.

Preserve other writers' index, files, untracked work and local commits. Do not stash,
reset, clean, switch or commit their checkout to make yours usable. Detached HEAD
can be an intentional task/review checkout; establish its purpose before changing it.
Missing local access permits a connected read-only audit, not invented local results.

## 2. Keep one integration truth and isolated writers

The source snapshot describes `TryVeto/product`, `main` as the integration trunk,
and `cloudflare-preview` / `cloudflare-production` as promotion pointers. Confirm
current repository policy and triggers before using those names. Do not develop
separately on promotion branches or create a permanent branch for each agent role.
Keep an existing native isolated task workspace; do not nest another worktree merely
to follow this guide. Otherwise use an owned task branch/worktree from an identified
accepted base, with one writer. An occupied path or checked-out branch is a reason
to inspect ownership, not to add a force flag. Use a read-only reviewer or serial
work when safe write isolation is unavailable.

Worktrees isolate working files and indexes, not every repository setting or external
resource. Coordinate lockfiles, generated outputs and shared semantics. Isolate or
serialize databases, ports, queues, browser state and credentials separately. Keep
one integration owner through the accepted outcome; see [team guidance](../team/SHARED.md).

## 3. Make the intended change reviewable

Use explicit paths/hunks. Inspect the staged diff, remaining unstaged changes and
intended new files before committing; do not sweep another task into `add -A`.
A coherent change can be large when required by the outcome. Do not impose arbitrary
line counts, cosmetic commits or a directory migration. Apply the
[engineering floor](engineering-quality.md) to the actual consequence.

Tests run on a dirty tree prove that tested tree, not automatically the committed
HEAD. Qualify the committed specimen or retain sufficient tree/diff identity and its
limits. Keep the complete original requirement in the PR and acceptance record.
Do not attach another candidate's checks to this one.

For a published task branch, prefer a coordinated non-rewriting base update through
the existing workflow. A rebase can be appropriate for owned unpublished history.
A published rewrite needs specific authority, coordination and an exact expected-old
ref check; a generic force-with-lease is not a grant. Never force trunk or promotion
pointers to make a rejected push succeed. First inspect whether rejection reflects
new work, wrong target, policy, credentials or another failure. Reconcile uncertain
publication before retrying it.

## 4. Integrate under the real gate

Inspect the current required checks, trusted producer, subject SHA and effective
rules. An inaccessible protection endpoint means **unknown**, not no protection.
A CODEOWNERS file, `protected: true`, a familiar check name or one ruleset is not proof
of combined enforcement. Candidate edits to CI/policy cannot approve themselves.
An intentionally nonapplicable job follows an explicit accepted rule; a skipped
required check is not a pass. Do not disable controls or install a merge service
merely because a report recommends stronger enforcement.

Use the maintained server-guarded integration route. A client-side base check alone
cannot exclude a concurrent change at merge. Preserve this lineage in the existing
handoff record:

`reviewed task head -> accepted integration commit -> checks/build -> deployed version`

Squash/merge can create a different commit. Record it and qualify its relevant
integration result; do not relabel pre-merge evidence as a fresh integrated run.
Generate receipts after candidate identity exists rather than trying to commit a
file containing its own final commit SHA. For target promotion, follow
[candidate-bound delivery](preview-and-release.md). Main-tip equality applies when
current policy requires it; ancestry is not an equivalent guard.

## 5. Recover before tidying

Preserve discovered work before repair. Reflogs and an owned rescue reference can
retain useful commits, but do not restore uncommitted files. A Git bundle preserves
included reachable history, not the database, build assets or dirty workspace. Scope
backups and sharing to the actual material; avoid copying secrets as recovery proof.

A source revert, deployment rollback, data correction and credential revocation are
different operations. Do not rewrite applied migration history or claim that Git
reverted a sent message, leaked secret or issued record. Use authorized incident
handling for a credential exposure; removing a file from the newest commit is not
containment. Keep source, data and release recovery under their actual owners.

Before deleting an identified branch/worktree, check ownership, PR/squash mapping,
post-merge commits, staged/unstaged/untracked/ignored work, running processes and
retained evidence. Age and `--merged` alone cannot establish disposability. Avoid
blanket prune/clean/delete commands. Leave uncertain work preserved and named.

Return the requested source result, actual verification, remaining transition and
owner. A local commit is not a published PR; a merged PR is not a verified deployment.
A correct no-change audit can finish without manufacturing a patch.
