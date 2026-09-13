# Engineering quality update — 2026.9.1107

Prepared 11 September 2026. Base: the supplied **2026.9.1106** ZIP. This continues
the established attachment-driven package update. The authorized work here is a
local shareable artifact; it does not modify the installed plugin, product,
WorkOS environment, production authority or active goal.

## Decision

Keep the coherent 13-skill toolkit. Put the new engineering detail at the decisions
where it matters: code and CI review, shared component contracts, local startup,
production-test planning and correction of an unsupported diagnosis. Do not add
five overlapping skills or another product organization.

This is not another claim that stronger prose solves the recurring failures.
The supplied 1104 review says the coverage mechanism already improved materially;
the unproved part is actual adoption and a behavioral comparison. Its duplicate
upload does not undo 1105's existing `--require-feedback` repair. This version adds
relevant engineering distinctions but leaves executable helpers and test logic alone.

## Sources and their treatment

The source inventory records filenames and SHA-256 in
[engineering-inputs.json](engineering-inputs.json). All 13 attachments are accounted
for. Five skill files were read as source material, not installed wholesale.
The six books were examined at their relevant operating standards, examples and
acceptance sections; this is not a fresh exhaustive literature review or a
line-by-line audit of every page. Rendered pages were inspected for the compact
coding standard (59), code-quality policy (55), CI receipt (73), component contract
(18), WorkOS acceptance matrix (63) and pushback contract (64).

| Source | Useful contribution | Destination / limit |
|---|---|---|
| Good Enough Coding Standards for a Startup Codebase, especially pp. 59–63 | Minimal standard, consequence over style, current repo path, boundary validation, persistent integrity, owned async work and incremental adoption. | Engineering floor. Illustrations do not select a framework or mandate broad cleanup. |
| Good Enough Code Quality for a Startup Codebase, pp. 47–56 | Complete requirements, server isolation, truthful failure, meaningful tests and evidence tied to the candidate. | Engineering floor. “Existing” safe-core/first-attempt/performance requirements must be confirmed in actual current repo policy before applying them. |
| Good Enough CI/CD, pp. 71–78 and relevant identity/recovery passages | Expected work must run; first failures/skips remain visible; stable staging; artifact/configuration/migration identity; compatible recovery and separate release rights. | Engineering floor, build and tests. No CI runner, paid Actions workflow or release automation created. |
| startup-design-system skill; A Good Enough Design System, component and adoption chapters | Four responsibilities without four packages; intentional component contracts; complete forms; representative consumers; existing visual direction. | Conditional design-system reference. Preserve Review Record versus book terminology; no rename, palette or catalog mandate. |
| push-back-with-evidence skill; Loyal to the Goal, Honest About the Facts, especially pp. 64–65 and casebook | Inspect before contradicting; distinguish fact/preference/authority; correct your own answer; change for evidence, not pressure; act faithfully after a permitted decision. | Existing judgment route and Head guidance. No debate added to a typo or legitimate preference. |
| review-local-sandbox skill | Candidate/source/session/store separation and evidence the reviewer actually saw. Complete review versus healthy candidate are different conclusions. | Existing review method; no second browser, tunnel, Pro-mode assumption or runtime activation. |
| veto-local-development skill | Real target/loader/launcher, fixed callback origins, process ownership, dependencies, precise HMR and configuration claims. | Existing local reference. Transcript commands, port 3045, database ports and laptop paths remain historical hints, not defaults. |
| internal-tooling skill | Use an existing launcher quietly; bound readiness and logs; do not stop the requested service or turn starting it into an improvement project. | Build route's fast path. No Makefile, daemon or supervisor added. |
| Agents in Production: A WorkOS access architecture for Veto, especially pp. 3–9, 18–29, 52–67 and source register | Dedicated synthetic scope, genuine auth and canonical admission/MFA, subtractive server limits, protected credential custody, named reviewed suite and observable termination. | Conditional production-verification reference and inactive request template. Architecture only; no auth, connection inspection, credential retrieval or application modification here. |
| veto-integration-sample.md | Same-request seller contribution → officer reopen, explicit identity, unknown-outcome reconciliation and meaningful endpoint. | Exact bytes retained as an inactive example. No selected vendor, live contract, permission or executed test. |
| veto-stack-1104-review(3).md | Earlier independent package review and its stated evidence limits. | Byte-identical to the previously supplied 1104 review. Preserve its operational-adoption recommendation; do not label it a review of 1107. |

## Resolve source tensions explicitly

**Standards versus migration.** The books recommend aligning with an existing
repository. They do not authorize replacing package managers, frameworks,
formatting conventions, CI providers or permission models. Improve a relevant
boundary while delivering an actual outcome.

**Shared UI versus product meaning.** The component system standardizes how an act
is shown, not who can perform it or what it proves. The accepted no-eyebrow rule
coexists with necessary labels, status and disclosures. The book's Escrow
Supervision File wording is not permission to rename the current Review Record.

**Production access versus testing shortcuts.** The WorkOS study's inspected SHA
was `74016ab7e51e501cd0cb93c7046a9e172a00b2c8`; production equivalence was not
established. Its reported environment settings and Admin/User role definitions are
dated source observations, not this session's live findings. A new provider role
cannot substitute for application enforcement. A supported genuine programmatic
session can be valid setup but does not test hosted UI/email and cannot fabricate
canonical membership or session-bound MFA. A synthetic tenant alone does not
prevent all prohibited effects.

**Self-criticism versus obstruction.** Unknown is not false. A justified agreement
is valid; an authorized experiment need not wait for the market proof it is meant
to obtain. An informed decision governs execution without making its factual
premise true. No positive-control case rewards needless dissent or repeated approval.

**Review completed versus product accepted.** Coverage can be complete while a
blocker is found. No blocker observed in a partial review is not universal
readiness. In a production smoke, a successful read and uncertain cleanup coexist;
the overall operational job stays on hold.

## Narrow external checks, separated from the supplied studies

Official pages were checked on 11 September 2026 only for implementation-sensitive
claims. These checks do not establish a connected account's configuration:

- [WorkOS testing](https://workos.com/docs/authkit/testing): emulator versus real
  staging; discourages routine automated live Hosted AuthKit UI; programmatic
  sessions have narrower coverage; Magic Auth setup sends email. The generic
  password example does not authorize changing Veto's method.
- [WorkOS sessions](https://workos.com/docs/authkit/sessions): access tokens,
  refresh-token handling and sign-out are distinct. Local browser closure alone
  cannot establish all access termination.
- [OpenAI packaging](https://developers.openai.com/plugins/build/plugins): checked
  for the existing package/install shape. No new host API or guaranteed loading
  behavior is asserted; native loading remains untested.
- [Google review standard](https://google.github.io/eng-practices/review/reviewer/standard.html):
  code-health improvement rather than perfection, and separation of personal taste
  from blocking findings. Used as a cross-check, not new repository policy.

The rest of the design is source adaptation and explicitly conditional guidance,
not newly observed production behavior. No public APIs were called to inspect
Veto settings, and no accounts, sources or acceptance rules were silently updated.

## Change scope and preservation

Added three conditional references, one inactive production-check request, one
exact integration example, this note and its source inventory. Updated existing
build, design, testing, review, judgment and integration entry points plus the
relevant role pointers. E70–E77 are new **unexecuted behavior specifications**.
They exercise consequential-versus-stylistic scrutiny, false-green CI, complete
shared fields, missing production authority, uncertain termination, fixed-origin
startup, correcting oneself and sample-versus-actual integration.

The same 13 active skill identities and nine role files remain. Both goals,
all executable helpers and test implementations, feedback schemas, existing
acceptance/review JSON templates, original fixtures/oracles and the central
feedback/evidence/diagnosis controls are preserved byte-for-byte against 1106.
Historical release notes and source snapshots remain historical.

Run the existing offline package suite and doctor, inspect links/metadata and
compare a fresh ZIP extraction before delivery. The resulting verification record
will distinguish those checks from native activation, agent trials and product
behavior. No new helper test count can establish better product sense.

## Next proof

Stage against the installed source without overwriting customizations. On one
already-authorized change, compare 1107 with 1106 using the same originals,
starting state, tools and accepted endpoint. Include a correct ordinary result
that should pass without ceremony and a decision-changing missing clause or
failed gate that must not disappear. Use held-out material for a genuine comparison;
a published example is training context, not automatically held out.

Do not build production access simply to try this edition. Validate its planning
boundary without credentials first. Any actual staging/production capability is
its own engineering and approval undertaking. The practical success measure is
complete, usable work with fewer repeated founder corrections and no weakened
safeguards—not the number of new documents or rules.
