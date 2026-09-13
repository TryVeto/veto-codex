# A small design system with real contracts

Use only when changing shared tokens, controls, form/status patterns, or their
adoption. This is adapted from the supplied startup-design-system skill and study;
it is not a new brand, framework migration or universal page template. Keep the
[chosen Veto meaning and identity](veto-contract.md).

## Inspect, compose, then extract

Read the existing tokens, component APIs, representative consumers and their tests.
Keep one general-purpose interaction foundation; use native semantics and existing
accessible primitives before building a custom combobox or focus trap. Do not
install a library to satisfy a catalog target.

Keep four responsibilities distinct without making four packages:

| Layer | Owns | Does not establish |
|---|---|---|
| Foundations | A shallow mapping for text, surfaces, actions, borders, spacing and focus. | Business state or source truth. |
| Primitives | Accessible control semantics, keyboard behavior and interaction states. | Authorization to perform a workflow action. |
| Patterns | Forms, correction, changed evidence, recovery and completion presentation. | Every page's layout or every future use case. |
| Domain components | The exact question, evidence, judgment and result for this job. | A new professional decision or server-side permission. |

Compose the actual workflow first. Extract when real reuse or consequence justifies
it and the contract is stable. A second consumer can test an abstraction; a fixed
number of appearances is neither necessary nor sufficient. A wrapper must own a
useful decision. Allow justified local geometry rather than tokenizing every number.

## Make components explicit

For a changed shared component, keep its purpose, permitted states, semantics,
keyboard/focus, content rules, save/error behavior where applicable, and extension
boundary beside the implementation or existing examples. Prefer intention-revealing
variants and valid state combinations to many independent booleans. A generic badge
must not turn an absent value into Verified.

For a field: associate label, hint, error and control; preserve correctable input;
save every editable value as represented or explicitly reject it. An unavailable
provider is not invalid user input. For a dialog: define entry/return focus,
dismissal and unsaved-work behavior. For a button: define the actual act, pending
state and duplicate handling without treating disabling as server enforcement.

Keep retrieval, domain and action states separate. Pending, durably saved, failed,
unknown and stale mean different things. On an uncertain save, reconcile before
retrying the consequential act. A failed notice must not repeat the saved decision.
Cross-view queues, counts, receipts and next actions use the same scoped facts.

## Teach with one complete pattern

Use an affected real workflow and representative synthetic states in the existing
component explorer or restricted development route. Do not build another explorer
when an existing page and its tests are sufficient.

For the recorded address requirement, suggestions alone do not pass. Select a
suggestion, expand the required individual fields, edit them, save, reopen and
check the actual values. Exercise manual fallback when required. Do not substitute
an HTML autocomplete attribute for this behavior or demand a universal form engine.

Keep source material independent of editable proposals. Preserve private audiences,
independent concerns and permitted remedies. A participant's help needs a usable
answer or route; a note saying it happened is not the answer. Completion names the
actual act, not a generic success claim.

## Enforce craft without erasing meaning

No decorative eyebrow, kicker or overline above headings. Preserve actual field
labels, meaningful status, Sandbox disclosure and required notices. Use shared
components and focused checks where they can enforce the distinction; a class-name
scanner cannot establish semantic compliance. Keep full identifiers and relevant
uncertainty readable. Remove repetition before shrinking type.

Maintain the accepted WCAG 2.2 AA target. Check relevant keyboard/focus, labels,
errors, status announcements, contrast, enlargement and narrow reflow in the actual
render. Numeric product defaults are not automatically WCAG mandates. An automated
scan or mobile viewport does not prove full conformance or physical-device behavior.
Keep necessary content available without waiting for motion.

Verify the shared contract at component level, representative consumer behavior,
actual rendering and affected domain/service joins. Preserve buyer funding when it
shares the changed controls. Review intended baseline changes explicitly instead of
accepting all snapshots to get green. Reuse the existing
[coverage and behavior gates](feedback-coverage.md).

Finish with the adopted component contract, its consumers, a usable example and
actual regression evidence. Remove obsolete alternatives only after checking their
uses. Stop when the requested workflow and next consumer are easier to build
correctly; component count is not the achievement.
