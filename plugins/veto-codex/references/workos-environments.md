# WorkOS: two trust boundaries, one implementation

Use when an authorized task concerns WorkOS configuration, authentication, company/
office admission, or release evidence. Do not run this playbook for unrelated UI
work. Read the current repository policy and existing integration first. A setup
study is not permission to change provider settings, rotate credentials, create
memberships, enable authentication methods or release a product.

This adapts *WorkOS for Veto: Preview and production*, particularly pp. 3–4, 8–33,
37–46 and 54–63. [Source decisions](../research/IDENTITY-GIT-PATCH.md) separate its
read-only observations, recommendations and current public documentation. Nothing
here establishes today's deployed credentials, policy or route behavior.

## 1. Identify the effective boundary

Keep the existing provider and meaningful application admission checks. The report's
default is **Staging for nonproduction preview; Production for the customer app**,
with one authentication implementation. Multiple AuthKit applications in one
provider environment share users and organizations; names or different client IDs
are not environment isolation. [Applications](https://workos.com/docs/authkit/applications)

For the relevant lane identify, without exposing credentials:

`origin -> source/artifact -> WorkOS environment/application -> canonical data/store -> external effects`

Include configuration/secret-version references, schema compatibility and test
principal scope. Do not hash secret values into a shareable fingerprint. A correct
dashboard does not prove correct deployed bindings. Check the final effective
configuration after overrides and build-time settings. Same Git SHA does not imply
same target artifact. Configuration-only changes require affected requalification.

| Lane | Intended boundary | Evidence limit |
|---|---|---|
| Local fast tests | Explicit local emulator or narrow doubles; disposable fixtures | Does not establish real authentication. |
| Stable preview | Real Staging; nonproduction stores and sinks | Qualifies only the exercised policy and candidate. |
| Approved branch preview | Exact registered origin; owned fixtures/resources; Staging for trusted branch code | Shared provider credentials can exceed the branch namespace. |
| Customer production | Production identity and customer resources | A successful login is not proof of every action's authority. |
| Approved synthetic production smoke | Dedicated principal/company/office and actual operation restrictions | Not broad exploratory access or customer validation. |

Do not give untrusted branch code a shared environment-wide credential and call it
isolated because its database or cookie key is unique. Remove credentials from
that lane or arrange a separately authorized isolation boundary. Do not automatically
create a third environment or a new identity system.

## 2. Keep durable entry points in the right environment

The report observed a Production application called Preview with preview defaults,
and a Staging default loopback callback plus a production logout entry. Treat these
as **historical configuration overlaps to check**, not evidence of a deployed leak
or permission to change settings. Preserve existing identities when repairing
confirmed routing; do not recreate accounts as cleanup.

For an authorized change, verify that the actual callback sent, provider registration
and final serving origin agree. The provider URI list and Veto's own allowed-host
predicate must both admit the intended route. Keep shared defaults stable; disposable
branch/local registrations need an owner and retirement condition. Retiring a branch
must not break invitations, SSO entry, webhooks or stable review.

Reported target paths are `/auth/workos/sign-in`, `/auth/callback`, `/files/`, logout
action `/auth/workos/sign-out`, and post-logout landing `/sign-out`. They are discovery
leads to verify on the target, not commands to apply. Test dashboard/API invitation
and applicable IdP-initiated SSO entry, not just a manually constructed sign-in URL.
A default application's role and current token issuer/client semantics matter;
follow the official SDK and documented token contract rather than inventing one.

Do not build a callback relay, put tokens in return URLs, broaden CORS, add wildcard
callbacks or enable passwords/passkeys to remove ordinary test friction. Preserve
transaction state, one-time code handling and safe same-origin return-path validation.
Callback failures must not echo credential-bearing URLs into logs.

## 3. Keep browser and server authority distinct

Use host-only session/assurance cookies in hosted lanes, with appropriate Secure,
HttpOnly, path and expiry attributes; no parent `.tryveto.com` session scope. Where
SDK-compatible, a `__Host-` cookie requires Secure, path `/` and no Domain; HttpOnly
is separate. Inspect actual response headers. Limit local HTTP exceptions to the
explicit local lane. Preview and production sibling hosts can be same-site but not
same-origin; SameSite does not replace Origin/CSRF defenses.

An outer preview gate is not a Veto session or company/office membership. Keep its
service credentials separate. Do not bypass an explicit browser/content denial via
another browser, tunnel, hidden route or injected identity.

Keep protocol work in the installed official AuthKit integration. Verify actual SDK
and framework versions before using current APIs or renaming interception files.
Model incomplete admission explicitly:

`identity -> selected company -> canonical membership -> permitted office -> allowed action -> required assurance`

Bootstrap identity is not file authority. Provider organization mappings must use
the actual environment/client namespace and canonical constraints; never infer
membership from a display name, email suffix, first office or client-supplied ID.
Recheck the actual actor, context and resource on server operations.

A legitimate organization switch can keep the provider session while changing its
verified selected context. Do not freeze the first session-list organization as the
only authorized selection. Revalidate membership and office; reject or reconcile
old-context forms, caches and assurance proofs without silently writing in the new
company. Preserve the successful switch as well as the denial case.

## 4. Separate assurance, freshness and continuity

Factor enrollment, current-session assurance and freshness are different facts.
WorkOS's required-MFA setting excludes SSO users; `auth_time` alone is not proof of
factors. Preserve current action-specific assurance, bound to the actual session,
company and office. Test the accepted SSO policy separately. An optional-MFA staging
path cannot establish required-MFA production behavior.
[Provider MFA semantics](https://workos.com/docs/authkit/mfa)

For refresh failures, inspect the installed SDK's typed result and documented policy.
A transient outage is not definitive revocation. Preserve recoverable state and use
bounded supported retries; expired/revoked/terminal sessions require reauthentication.
Do not authorize a consequential act whose required authority cannot be verified.
The source's session-duration recommendations are proposals, not adopted settings;
refresh inactivity is not proof of human activity.
[Version-sensitive refresh behavior](https://workos.com/docs/authkit/session-resilience)

Test logout through the real action and then a protected read/mutation. A landing
page or UI label is not sign-out proof. Cookie clearing, provider revocation and
cookie-key rotation are distinct effects. Keep legitimate draft recovery separate
from retaining invalid authority; do not use a longer session to conceal a defect.

## 5. Qualify the boundary at its actual layer

Select only cases implicated by the change, plus existing required gates. Establish
healthy positive controls so a failed database or invalid fixture cannot masquerade
as successful authorization denial. Keep results separated by local/emulator, real
Staging and expressly authorized synthetic production.

| Contract | Positive and adverse evidence |
|---|---|
| Environment and entry | Correct lane reaches its intended file; wrong origin/client/issuer is rejected for the intended reason. |
| Admission | Valid company/office access and valid switching work; cross-tenant, revoked membership and stale-context commands do not. |
| Assurance | Legitimate required challenge succeeds; enrollment-only, stale or wrong-context proof cannot authorize the action. |
| Continuity | Valid rotation/refresh recovers; terminal revocation and actual logout stop protected access. |
| Browser scope | Actual cookie flags and callback behavior match the host; disallowed cross-origin mutation fails. |
| Lifecycle, when used | Verified event receipt survives interruption; duplicates do not repeat effects; stale activation or incomplete reconciliation cannot restore/delete authority. |

Add webhook/lifecycle machinery only for a demonstrated need. Use stable
same-environment endpoints, signature verification, durable receipt, idempotency
and reconciliation. Preserve independent office decisions and live admission
checks unless a replacement consistency policy is separately authorized and tested.
Do not infer deletion from partial pagination or replay old activation as current
permission.

## 6. Do not manufacture an observer role

The report's inspected canonical model contained Admin and User; a legacy `limited`
label normalized to User. This is historical source evidence, not current permission
inspection. A provider role named `qa-reader` does not establish server-enforced
read-only behavior. Inspect effective operations, not labels.

Use [production verification](production-verification.md) for an existing approved
runner and its access-termination evidence. Its unattended containment requirement
is not waived by this new study. The study separately proposes human-completed
authentication plus narrowly supervised synthetic qualification while observer
controls are unproven. That is a **different assignment requiring its own explicit
scope**; it does not turn an ordinary User into read-only or enable autonomous
production exploration. Do not ask again for steps already covered by a valid grant.

Return what was inspected or changed, the exact configuration/artifact, checks
actually run, unverified layers and the next owned gate. Missing live access can
leave a useful source assessment complete without pretending the deployment passed.
