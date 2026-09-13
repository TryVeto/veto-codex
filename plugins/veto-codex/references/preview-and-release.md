# Carry the exact capability from source to its authorized destination

Use for a canonical-app preview handoff or release-readiness assessment. For actual
publication or production activation, use the repository's current maintained
procedure and authority; this reference adds evidence checks, not another controller.
A local-only task does not become a deployment task by loading this file.

This adapts the supplied *From Sandbox to Preview* and *From Preview to Production*.
Their repository observations belong to snapshot
`64db045ce8e8ace8d25cd6e8aee126d00dff302d`, not a recommended deployment candidate or
this plugin's inspection of current service state. See the [source decisions](../research/DELIVERY-PATCH.md).

## 1. Establish what is being delivered

Read the actual assignment, applicable repository instructions, current work record,
source state and maintained delivery/verification commands. Identify the recipient's
usable endpoint before selecting a host. Keep ordinary authorized work moving; ask
only for a consequential unresolved choice, not routine permission already granted.

| Input or requested endpoint | Correct boundary |
|---|---|
| Local worktree of the canonical application | Use that application's normal verification and publication path. A different machine does not imply a different product. |
| Standalone saved sandbox | Preserve the reference. Transfer only accepted behavior into canonical identity, permissions, storage and routes when integration is requested. |
| Share a prototype | Preserve its prototype label and evidence limits; use the approved sharing route. Sharing does not establish canonical integration. |
| Branch preview | Publish and qualify the selected branch artifact; do not implicitly replace shared preview. |
| Shared preview | Qualify the integrated candidate and coordinate its separate promotion. Branch evidence is not proof of a different merged candidate. |
| Production | Prepare or execute only the specific authorized release phase through the maintained production path. |

For a sandbox transfer, map entry, actor, command, retained state, visible result,
critical denial and recovery to the actual application. Classify what is reusable,
already present, needs a bounded adaptation or remains outside accepted scope.
Do not replace this with a screenshot port, rewrite the entire product, or copy the
sandbox's private store, generated credentials and sessions into a deployable bundle.
Preserve buyer funding and all other accepted obligations while sequencing the slice.

The books describe branch versions of `veto-preview`, shared promotion through
`cloudflare-preview`, and production through `cloudflare-production`/`veto-production`.
Treat these names, `control-veto`, `verify-veto`, recorded hostnames and exact-main
policy as discovery hints. Reinspect the actual checkout, current help, executable
configuration and relevant live control plane. Do not execute historical commands
or use a report's SHA just because they look familiar.

## 2. Qualify publication before triggering it

Use the existing task or release record for the source/base, target, accepted
behavior, test plan, allowed effects and stop condition. Inspect build scripts and
triggers: a push, upload or build can publish a URL, use credentials or activate work.
Build, upload, activate, verify, enable customer exposure and announce are distinct.

Confirm the target's identity provider, storage, schema, external-provider modes,
notification sinks and resource ownership. Branch names and unique URLs do not
prove isolated data or side effects. Shared nonproduction storage can be adequate
with enforced run namespaces and compatible schema; do not demand a database per
branch without a reason. Do not hide a missing required provider behind a success
mock. Name simulations and any test result they cannot support.

Keep ordinary branch code away from production credentials and trusted release
controls. Do not expose private source material or authentication state in an
artifact. Cloudflare's [preview documentation](https://developers.cloudflare.com/workers/versions-and-deployments/preview-urls/)
distinguishes version URLs from movable aliases and notes public access when enabled;
publication exposure must be understood before upload, not after production traffic
changes. Use existing authorized protection, not an unrequested public tunnel.

Select the real required CI check, trusted producer and accepted policy for the exact
candidate. Conflicting old/new CI guides are a question to resolve, not permission
to choose whichever result is green. A failed or absent required gate blocks that
promotion. Improve the maintained path within scope; do not use a disabled direct
upload, retired workflow, force push or alternate credential as a shortcut.

## 3. Prove the hosted artifact, then its behavior

Keep expected and observed identities separate. Record the source commit, provider
build/version, relevant component identities, nonsecret configuration reference,
schema compatibility and exposure policy. A branch, alias or the word “latest” is
only a locator. A source SHA alone does not identify all executable inputs.

Obtain identity from the actual hosted application and trusted publication evidence
before and after the acceptance episode. Check final routing after permitted auth
redirects and every host the accepted contract actually requires. Never fill an
unknown remote SHA with the runner's local checkout SHA. On a mismatch, retain the
observations and resolve routing/candidate selection; do not modify expectations to
make the check pass. Mid-review changes require a successor attempt, not mixed proof.
Equal before/after identities do not exclude an intervening revision. Use the existing
review ownership window and applicable deployment/request evidence; disclose gaps.
If authentication lands on a mutable alias, qualify that final target explicitly.
A versioned entry URL does not pin a different post-login application.

Establish the useful dependency-readiness contract, not only HTTP success. A health
response is enough only when its semantics establish the required property. A
storage-dependent journey remains unqualified when required storage is unavailable,
even if an endpoint returns 200. Test that negative case and a healthy positive
control in isolation. Do not blindly copy a preview boolean into production or use
a readiness check that performs unapproved writes or sends.

Then operate the named journey in the served application: ordinary success, the
relevant critical denial, and persistence/recovery appropriate to the change. Use
the same request and retained edition across actors. Inspect actual copy, primary
action, errors, keyboard/narrow states and generated output where relevant. A green
source test, health check or browser launch cannot substitute for this episode.

Qualify the real authentication boundary separately from application-session setup.
A reused or supported programmatic session can test admitted application behavior;
it does not prove fresh hosted login, delivery of an email code or MFA completion.
Use the actual approved browser/runner and bounded auth transitions. Do not remove
origin restrictions or fabricate a session to get a green result. Use
[WorkOS environment qualification](workos-environments.md) and, for a requested
production smoke, [the bounded capability](production-verification.md).

The sandbox-to-preview report identifies host-allowlist, off-origin-auth, doctor-host
and local-SHA-fallback gaps at its inspected revision. These are regression leads,
not four newly reproduced bugs. Inspect their current implementation before repair;
keep unrelated/production hosts denied in a preview-only verifier. Missing access
blocks only the dependent claim; finish independent authorized work.

## 4. Keep integration, shared preview and production separate

Merge only through the active repository gate and its granted authority. Record the
resulting integrated SHA; preserve the reviewed-head to merge/squash-result mapping
using [Git handoff](git-workflow.md). If it differs from the branch specimen, qualify
the new candidate rather than carrying over acceptance without a justified basis.

One owner controls shared-preview mutation through verification. Use existing
serialization and expected-current-state checks; source worktrees do not isolate a
shared deployment. Recheck eligibility before mutation and reject stale attempts.
When active policy requires the current main tip, establish exact equality at the
guarded transition; ancestry or a prior green SHA is insufficient. If main advances
before activation, requalify or use an authorized bounded integration hold—never
force a pointer backward. Main advancing after a legitimately authorized activation
does not retroactively invalidate that release.
If a push or activation times out, read the existing attempt's actual state before
retrying. Do not rebuild or cancel a mutating deployment merely because a newer
stateless validation run can supersede an older one.

For production readiness, inspect the intended configuration differences, schema,
old-client compatibility, provider behavior, migrations, exposure and recovery.
When build-time configuration differs, qualify the production artifact from the
approved source; do not claim preview and production are identical bytes. Approval
must remain applicable to the candidate and intended effects; a material change
requires renewed qualification and any corresponding authorization.

Preserve Sebastian's required production decision. An approval environment variable
may carry a recorded decision; setting it does not create one. Release permission
does not silently include account provisioning, synthetic writes, real messages,
customer admission or payment actions. Reuse a valid standing grant when it covers
the exact act. Prepare the smallest missing decision while other permitted work
continues. No new approval committee or automatic feature-flag project is required.

During an authorized release, retain the controller's prior-state capture, eligibility,
publication and readback checks. Verify canonical routing, actual version, essential
readiness, the authorized journey and its represented consequences. A deployment
can succeed while acceptance is blocked or failed. Customer use remains separate.

## 5. Recover the actual failed boundary

Distinguish source selection, missing CI, build, routing, verifier, authentication,
authorization, storage and external effects. Repair the causal boundary; do not
repeatedly redeploy unchanged code or ask for a broader permission by default.
Preserve the first failure and any changed inputs.

For consequential changes, check old tabs/drafts, assets and stale commands against
the new server. Preserve user work and require a safe refresh or current-basis act
when necessary. Do not turn every release into a new compatibility framework.

Recovery must account for code, schema, data, configuration, queues and effects.
An exact-main source policy may require a new revert commit and requalification;
an approved provider-state restoration is a different emergency operation. Use the
current incident/runbook authority, not an improvised old-SHA promotion. Rolling
back code cannot unsend a notice or reverse a disclosure. Read back restored state,
reconcile uncertain effects and retain their owner. Do not promise monitoring
without an actual supported runtime and bounded observation assignment.

## 6. Close at the requested endpoint

Reuse existing evidence fields; this is not a new mandatory ledger or JSON schema:

```text
Outcome and accepted plan / original feedback coverage:
Reference specimen (if any) / source + integration identity:
Target / observed artifact + before/after identity:
Configuration/schema/exposure references (no secret values):
Authority / actual publication or activation effect:
Readiness / journey / denial / recovery results and substitutions:
Remaining obligations, owner and next action:
```

The plugin's existing receipt helper checks declared relationships only. It does
not authenticate remote version claims, enforce release rights, validate a new
release schema or repair the Veto verifier. A supported, correctly scoped pass
should end the assignment without extra ceremony. A blocked result should identify
the exact missing proof or action, not claim the product shipped or abandon the
remaining independently executable work. A requested shared-preview update remains
open when only a branch URL was published. Archive-only work can finish at the archive
without silently creating a hosted deployment.
