# 1109: keep source and identity boundaries explicit

Prepared 11 September 2026. This is an instruction-package revision of **1108**,
not a repository, WorkOS, deployment or running-agent audit.

## Decision and baseline

The new inputs concern the boundary between a reviewed source change, its released
artifact and the authority that artifact accepts. Adapt them into the existing
implementation, integration, testing and delivery routes rather than install three
more overlapping skills. Keep the Stripe-inspired whole-job loop and the feedback
coverage mechanism intact.

Baseline archive: `Veto-Stack-2026.9.1108.zip`.
SHA-256: `cee755123594d05595ee31aa4e382c1a6cd51e570da1616a0218140167e30efd`.
The baseline was inspected, CRC-checked, safely extracted and tested before editing.
This edition keeps all **13 active skill names** and **nine role guides**. Helpers,
executable tests, goals, accepted-evidence formats and original test fixtures are
unchanged. There is no automatic installer, publisher, auth runner or Git cleanup.

## Source account: all five attachments

Hashes and source-copy paths are recorded in [identity-git-inputs.json](identity-git-inputs.json).
The three skill files were read in full; the two books were read selectively at
relevant decision, workflow, evidence, testing, release and recovery sections.
Rendered WorkOS pages 3, 5, 22, 55, 56 and 59–60 were inspected alongside their text;
these distinguish observed settings, proposed routing and unexecuted acceptance.
This is not an exhaustive reread of every page or a new audit of their linked code.
The PDF originals stay in the user's source collection rather than being duplicated
inside the runtime plugin. Archived skill bytes are outside active discovery and
retain optional source links as text, not claims that their companions are installed.

| Source | What transfers | Destination and what does not transfer |
|---|---|---|
| `veto-git`, supplied as `SKILL(20260911-232711)(1).md` | Modes, preservation-first inspection, owned writers, deliberate commits, exact candidate/gate lineage, rejected-push diagnosis and scoped cleanup. | [Git reference](../references/git-workflow.md). No new active skill, branch policy, cleanup command or publication authority. [Original](source-skills/veto-git-1109.source.txt). |
| *What your Git should look like*, especially pp. 3–6, 19–31, 35–51, 55–62, 67–74 and 85–98 | One trunk and controlled promotion pointers; source/worktree/runtime differences; PR/squash identity; live enforcement limits; backup and recovery distinctions. | Same conditional Git reference and existing delivery procedure. Snapshot names and policy remain discovery leads, not a live-state certificate. |
| *WorkOS for Veto: Preview and production*, especially pp. 3–4, 8–33, 37–46 and 54–63 | Two provider environments, one implementation; effective bindings, stable entry, canonical admission, assurance, session recovery and causal tests. | [WorkOS reference](../references/workos-environments.md), auth-specific routing, existing production-verification boundary. No dashboard changes, observer role, fixture provisioning or adopted session policy. |
| `ship-to-preview`, supplied as `SKILL(20260911-232005)(1).md` | Canonical app rather than a parallel demo, exact final serving target, post-login routing, intermediate-version evidence, complete requested shared-preview handoff. | [Existing delivery reference](../references/preview-and-release.md). No duplicated deployment skill or new release mechanism. [Original](source-skills/ship-to-preview-1109.source.txt). |
| `ship-preview-to-production`, supplied as `SKILL(20260911-231559)(1).md` | Assess/prepare/execute scope; source/artifact/configuration/schema/exposure tuple; guarded exact-main transition; uncertain activation and recovery. | Same delivery reference. No production permission, new approval variable, recovery command or claim that the source's tests ran here. [Original](source-skills/ship-preview-to-production-1109.source.txt). |

## Preserve the sources' qualifications

**Git's snapshot is not today's control plane.** The book identifies repository source
at `64db045ce8e8ace8d25cd6e8aee126d00dff302d`. It reports GitHub Actions `Veto CI`,
Cloudflare Workers Builds, promotion-pointer branches and sampled check/PR evidence.
It also reports that classic-protection inspection lacked permissions. That neither
proves no protection nor establishes complete effective enforcement. The source
record does not select a provider migration, grant merge authority or authorize
removing an old branch. The active task and actual repository contract govern.

**A source identity is not all executable inputs.** Dirty/untracked changes,
merge/squash results, target-specific builds, configuration and schema can change
what an observation means. Preserve lineage; requalify affected inputs without
pretending every change invalidates every unrelated test. A current-main-tip rule
requires equality when that rule actually applies. The new production skill also
makes the timing precise: eligibility belongs at the guarded transition. Later
trunk progress does not retrospectively make a properly authorized activation
unauthorized. Do not create a perpetual redeploy-to-latest loop.

**Two equal samples are not a continuous observation.** The preview skill warns
that a before/after identity can hide an intervening deployment. The update requires
using the existing review ownership and available deployment/request evidence,
or retaining that limit. It does not assert that a mixed revision occurred without
observations. Likewise, a versioned entry URL does not pin a different host reached
after authentication. Match evidence to the actual final candidate.

**The WorkOS overlap is reported configuration, not a demonstrated leak.** Its book
pins selected repository source to `e6fe80a54e050c13594ce23ff974575c09bf95fd`. It
reports a Production app named Preview, preview-directed defaults, and crossed
Staging logout/default entries. It explicitly did not inspect deployed secret values,
resource bindings, live authentication, full route enforcement or whether that
commit was deployed. This update retains those limits instead of repeating the
observations as today's incident. No current account state was read here.

**Application, environment and role names do not confer isolation.** The WorkOS book
separates identity, data, credential, browser and operational boundaries. It describes
Admin/User normalization, including a legacy `limited` label that is not a proven
observer. The new reference preserves official protocol handling, canonical company
and office membership, valid selected-organization changes, and action-specific
assurance. It does not invent a role or let an agent name its way into safe access.

**Do not reconcile differing production proposals by weakening the guard.** The
existing automated-verification method requires an enforced operation ceiling and
observable termination. The later WorkOS book separately recommends a human-completed
ceremony and tightly supervised synthetic qualification while observer containment
is unproved. That may be considered under a separately explicit assignment; it does
not replace unattended enforcement or constitute current authorization. An already
approved, genuinely bounded runner remains usable without repetitive permissions.

**Policies proposed in a report are not installed policies.** Its suggested session
durations, invitation-led default and possible future environment changes are not
adopted by this ZIP. Do not tighten timeouts, disable signup, enable authentication
methods, rotate secrets or build webhook machinery without the actual scoped need
and permission. Preserve successful legitimate use alongside consequential denials.

## Narrow public-document checks

Checked 11 September 2026 only to corroborate published mechanics. These are not
private Veto account observations or evidence of installed-version behavior.

- [WorkOS applications](https://workos.com/docs/authkit/applications): applications
  in one environment share users/organizations; default-application entry and token
  issuer/client semantics are distinct from isolated environments.
- [WorkOS MFA](https://workos.com/docs/authkit/mfa): the provider's required setting
  does not apply to SSO users. Preserve separate action assurance rather than infer
  factor completion from policy or a recent authentication timestamp.
- [WorkOS session resilience](https://workos.com/docs/authkit/session-resilience):
  transient and terminal refresh failures differ; behavior varies with SDK/version.
  Retain the application's current-membership requirement. Session recovery is not
  permission to accept expired credentials or guessed office authority.
- [Git push](https://git-scm.com/docs/git-push): rejected/non-fast-forward updates
  and lease checks need precise ref context; they do not supply task authorization.
  The reference avoids a ready-to-run force-push recipe.
- [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins):
  retained packaging and source-discovery guidance, without a host-compatibility claim.

No connected repository, WorkOS environment, browser session, production record or
provider control plane was fetched or changed for this update. Public documentation
and historical source references do not establish those current states.

## Evaluation scope

All **85** earlier behavioral cases are retained unchanged. **E86–E97** add dirty-tree
identity, concurrent writer preservation, sufficient squash evidence, stale versus
valid transition timing, shared-provider isolation, SSO/MFA, valid organization
switching, causal denials, observer-role limits, config/post-login identity and
paused-source adoption. They are **specifications, not executed trials**.

Local helper/package tests do not test these judgments. Use [ADOPTION.md](../ADOPTION.md)
on one relevant already-authorized task, with 1108 as the baseline unless a comparison
already has a declared baseline. Use held-out cases, fixed sources/permissions and
both positive and adverse controls. Do not provoke a live auth incident or alter
production to measure this package.

The desired change is fewer lost or misattributed source handoffs and fewer unsupported
authentication/readiness claims, without more founder reconstruction or weakened
boundaries. [Verification](../VERIFICATION.md) records what was actually checked.
