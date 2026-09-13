# Production verification is a bounded capability, not a shared login

**Conditional design and run guidance. No runner, login, production grant or new
server-side control is implemented by this plugin.** Read only for an explicitly
requested production-verification design, review or authorized run. Ordinary local
work stays in the [local loop](sandbox-and-local.md).

The supplied *Agents in Production* study proposes this architecture after a dated
read of WorkOS and repository snapshot `74016ab7e51e501cd0cb93c7046a9e172a00b2c8`.
It did not establish deployment equivalence, current entitlements, hosted acceptance,
or a successful production test. Reinspect current configuration/code through
actual authorized tools before relying on those observations. The
[source note](../research/ENGINEERING-PATCH.md) separates the study from current
public documentation and this adaptation.

## Pick the evidence layer

| Layer | What it can establish | What it cannot establish alone |
|---|---|---|
| Isolated local simulation/emulator | Repeatable integration/failure logic and controlled browser behavior. | Genuine provider authentication or production configuration. |
| Real staging | Actual provider integration, canonical admission, required MFA and bounded rejection/recovery. | The current production deployment. |
| Explicitly approved production smoke | The named deployed revision and admitted synthetic path under the approved effects. | Full regression coverage, customer usability or a deployment grant. |

Keep broad destructive/adversarial tests local or in isolated staging. WorkOS's
[current testing guidance](https://workos.com/docs/authkit/testing) recommends a
local emulator for most tests, a smaller real-environment suite, and supported
programmatic sessions instead of repeatedly automating live Hosted AuthKit. Check
feature support and the installed SDK. Its generic password example is not
permission to enable passwords in Veto; Magic Auth creation has an email effect.
A programmatic bootstrap does not test email delivery or the hosted sign-in UI.

Use human-assisted qualification of the real required ceremony where appropriate
and authorized. Then automate only an approved acquisition method in protected
custody. Do not fake verified-email/MFA claims, seal your own fabricated user
identity, borrow Sebastian's session, or disable controls to run a test. A genuine
provider-authenticated session produced through the supported SDK is different
from fabricated authentication; it must still pass Veto's canonical admission.

## Inspect the complete authority chain

Resolve exact origin, deployment, provider environment/client, approved synthetic
persona, canonical organization/office, fixture set and named suite before
obtaining credentials. Similar names such as Preview do not establish isolation.
Unknown bindings stop that operation, not unrelated local repair.

The study observed canonical Admin/User roles and additional session-bound MFA
checks in its inspected code. Treat those as dated inspection hints, not live
facts. A provider role named qa-reader does not implement a Veto read-only role.
An enrolled factor, MFA-required setting or recent login is not necessarily proof
that this session completed the required challenge for this office and action.
Preserve current normal membership, session, origin and step-up checks.

Where the approved design uses automation restrictions, effective authority is the
intersection of normal application permissions and the narrower run/resource/
operation ceiling. Recognize the restricted principal in server-controlled state;
omitting a caller-supplied test header must not remove the ceiling. No arbitrary
identity, URL, script, office, factor or duration supplied by the requesting agent.
Separate fixture provisioning from a smoke run; the smoke must not self-grant
membership, repair credentials or create its own test office.

Enforcement belongs in the server, runner and credential boundary. A page label,
HTTP GET, hidden button or promise to be read-only is insufficient. Inspect any
load-triggered jobs, exports, provider inquiries and communications in scope. A
safe rejection must occur before the prohibited business effect. Qualify denials
against synthetic resources, never a real customer file as a test target.

## Diagnose admission and adjacent routes without weakening their contract

The supplied `workos-production-verification` skill reports an organization-switch
regression: a verified token selected a new organization while the provider session
listing retained the original. This is a historical report, not a newly reproduced
failure or a universal provider guarantee. Inspect the installed integration and
current provider contract before changing checks. Do not impose
`listedSession.organizationId === verifiedToken.org_id` as an unexamined invariant.

Use the official verified token/session path, current membership and canonical
organization/office binding. Preserve user/session/lifecycle, expiry, revocation,
impersonation and action-level MFA checks. Pair valid switching with rejected
mismatched fetched organization, inactive membership and unauthorized office cases
in isolated qualification. The routine automation scope remains pinned: a valid
human switch outside the approved run office still must not gain automation access.
`auth_time` alone is not proof of completed MFA. Authentication-only bookkeeping
must not grant business access or create membership before admission.

A redirect failure can follow committed setup. Reconcile the original operation
before creating another company, office or account. A successful Files view does
not establish Records/exports on the actual backend: the new source reports a D1
failure at that later boundary. Select that path only when the suite relies on it.
A Money empty state is not funding proof; clearing a problematic memo for diagnosis
does not pass the original memo case. Keep the initial input and unresolved check.
The source reports a merged repair with validation still running, not a final live
acceptance. No current defect or repair status is asserted by this plugin.

Read the [delivery source note](../research/DELIVERY-PATCH.md) for provenance.
A smoke run executes its approved suite, not account setup, fixture repair or a
production code fix. Route those to their actual owners and authority.

## Keep authentication material out of general execution

A trusted component holds broad provider credentials and factor/session material;
the coding agent gets only the approved operation and sanitized evidence. Merely
placing a secret in an environment variable does not isolate it from code executing
in that process. Unreviewed branches must not execute beside production secrets.
An authenticated browser handle still carries power and needs its own boundaries.

Start serially with one controlled identity/session and one reviewed suite. Give
one component ownership of refresh. Separate concurrent sessions if concurrency
later earns its cost; do not copy one rotating session between workers. Agent Auth
and M2M are different principal/integration choices, not shortcuts into an existing
browser-user authorization path. Qualify them separately for API-native work.

## Authorize, qualify and terminate

Reuse an actual scoped standing grant when it covers the run. Otherwise prepare
only the missing decision using [the inactive request](../templates/production-verification-request.md).
It names target-selection rule, synthetic scope, suite/runner identity, permitted
authentication and business effects, real limits, observer, expiry and stop/cleanup
route. Do not invent a time budget or approval. A document upload, plugin adoption,
Green CI, urgency or a successful login supplies none of these permissions.

Before admitting production, qualify normal synthetic admission and MFA, the useful
read path, direct server denial and the absence of prohibited effects in staging.
Exercise expiry, omitted metadata, stale session/office scope and worker-crash
cleanup at the appropriate nonproduction layer. Do not begin a production run
until its enforced boundary and required cleanup path are ready.

Register the independent cleanup/expiry route before authentication.
Bind the run to an absolute deadline under server control; refreshing a provider
token must not renew the job's authority. End business access, perform the supported
provider-session cleanup, verify protected-access denial, then dispose of local
authentication state. Preserve the ability to perform logout safely while ending
business permissions. A browser closing, local file deletion or short access-token
expiry does not independently prove access ended. WorkOS
[session documentation](https://workos.com/docs/authkit/sessions) distinguishes
access tokens, refresh and sign-out.

Return separate results for the observed journey and access termination. If the
read succeeded but cleanup or revocation is uncertain, retain the success evidence
and report an overall hold; do not call the run safely complete or silently launch
another one. Stop on wrong deployment, unexpected customer data, unclassified
operation or an exceeded permission; preserve sanitized evidence and the actual
owner's recovery route. Proven prohibited effects or continued business access
after the enforced stop are an incident, not merely missing cleanup evidence.
Contain within authority and escalate; do not use a second identity to continue.
Keep operational incident/hold wording separate from the existing receipt schema.

Use existing evidence records: approved scope reference, observed candidate,
bootstrap fidelity, actual checks and failures, prohibited-effect observations,
termination results and remaining limitations. A receipt checker can check these
declarations; it cannot enforce the ceiling or authenticate the evidence.

## Later environment study: preserve the automation boundary

For configuration, cookies, callback defaults, admission, MFA/SSO and policy parity,
load [WorkOS environment qualification](workos-environments.md). The later supplied
study inspects a different source revision; neither snapshot certifies deployment.
Its Admin/User findings mean that naming an observer is not implementing one.

That study proposes human-completed authentication and tightly supervised synthetic
qualification before observer controls are proven. This is a separate scoped
proposal, not a waiver of the server-enforced limits for this automated capability.
Do not start it, export a founder session or replace an existing approved runner
merely because the proposal exists. Once a valid standing scope and enforced runner
are established, reuse them without requiring repetitive approvals.
