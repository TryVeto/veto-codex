# Application verification

Use before and after material product work and before a review handoff. This is the
Veto adaptation of pstack's **Launch, Doctor, Drive, Evidence, Cleanup** method.
It routes to maintained application machinery; it does not add a competing runner.
See [source decisions](../research/AGENT-NATIVE-METHOD.md).

## For TryVeto/product

Inspect current root/scoped `AGENTS.md`, `.agents/skills/verify-veto/SKILL.md` and the
relevant row of `docs/agent/FEATURE_MAP.md`. These repository paths were read on
12 September 2026; refresh them in the actual checkout before use. They govern
exact commands and permitted effects. The supplied package has not run the product.

**Launch.** Reuse the correct local instance or start the app through the maintained
repository route. Establish source revision, dirty changes, origin, configuration,
process ownership and data scope. Do not substitute a loose HTML prototype for a
product candidate. Do not overwrite another agent's storage or test session.

**Doctor.** Run `npm run control-veto -- environment --json`. For staging/shared
Preview, run `npm run control-veto -- doctor --json` and bind results to `/api/version`.
If startup, access or candidate identity fails, report that boundary before driving.
These checks are not a deployment authorization.

**Drive.** Discover maintained cases with `npm run control-veto -- journey list --json`.
Choose the original acceptance row; inspect browser-plan guidance before adding a
plan. Capture baseline, repair and replay through the same real interface. Exercise
relevant failure-and-repair paths and actual persisted state, not hidden endpoint
substitutions. Validate a new plan with the documented dry-run before applying it.
Any data mutation requires the mission's authority and the harness's explicit apply
control. Use synthetic or expressly authorized data.

**Evidence.** Preserve the run receipt in `.artifacts/control-veto/<run-id>/receipt.json`
and the available browser, accessibility, screenshot, video, trace, console and
network evidence. Record expected versus observed behavior, timestamp, exact source
and deployed identity, configuration and manual substitutions. A fresh validator
replays the acceptance row on the exact deployed artifact where required. Unit tests
and a screenshot alone do not close that gate.

**Cleanup.** Close only processes and contexts created for the test, according to the
repository contract. Preserve receipts and the reviewable candidate. Restore only
owned disposable fixtures. Do not globally kill browsers or erase shared data.

Production is off limits to `verify-veto` and `control-veto`. Keep the current
repository's separate production-read and release procedures, permissions and
exact-candidate requirements. An available production credential is not a mandate.

## Integration can invalidate runtime proof

An unchanged patch on a changed base can produce a different result. Preserve useful
code-review analysis, but rerun the decisive acceptance path on the final integrated
commit/tree and build configuration after a rebase, retarget, squash, merge, or material
configuration change. Green limited CI and a matching patch-id do not replace that
replay. The independent verifier must inspect the actual integrated candidate.

## When the existing route does not cover the new behavior

Add the smallest replayable journey and its Feature Map entry inside the maintained
harness. Test the harness on one ordinary sufficient case and one relevant refusal
followed by legitimate recovery. A product failure stays a product failure; do not
rewrite the verification docs or expected result to make it disappear.

For another application or artifact, inspect its actual launch and verification
surface first. A CLI needs real command execution; a document needs render/content
checks; a plugin needs package checks, actual loading and behavior qualification.
Use the same five responsibilities, not invented Veto commands on another repository.

## Qualifying this plugin is a different task

`doctor.py` checks package structure and hashes; unit tests exercise helpers;
`check_handoff.py` checks declared file continuity. None proves that a native host
loaded the skills, that an agent selected them, or that a Veto customer journey works.
[ADOPTION.md](../ADOPTION.md) retains those distinct native checks.
