# 2026.9.1108 — finish the handoff on the actual candidate

Prepared 11 September 2026. A source/instruction update to Veto Stack, not a Veto
application audit, deployment, authentication repair or permission change.

## Baseline and scope

Parent: **2026.9.1107**, archive SHA-256
`45782b1558f3635974e15ed3af39bf438abc9e2d82ad8cd953c1a7335d82c781`.
The newly attached **1106** ZIP is byte-identical to the earlier 1106 archive
(`b64658d719e0d39b658df1045c71bf31326e7e35dc7320731d27a05df08e58eb`).
An older attachment does not request a rollback; 1107's engineering, shared-UI,
feedback and production-planning work is retained.

The useful addition is a precise handoff: **which application, which candidate,
which environment, which permitted effect, and which observed outcome?** The
books do not justify another pipeline, generic release agent or orchestration
skill. One conditional reference supplies these distinctions to existing routes.

This release keeps all 13 active skill identities and nine role guides. Goals,
executable helpers, executable tests, original fixtures, existing acceptance/feedback
schemas and source-coverage mechanisms are not changed. E78–E85 are added behavioral
specifications; they are not model runs. No production command or new tool is provided.

## Account for the supplied material

All ten attachments, including duplicate instances, have verified local hashes in
[delivery-inputs.json](delivery-inputs.json). Five unique skill files were read in
full. The two books were studied at their decision, delivery, identity, verification,
recovery, example and evidence-boundary sections. This is not a new exhaustive
literature review or a claim to have audited the code linked by the books. Relevant
rendered PDF pages, including the lane map, readiness/replay and preview contract,
were inspected alongside extracted text.

| Supplied source | Contribution | Treatment and limit |
|---|---|---|
| `codex-operator` (two identical uploads) | Smallest useful mode, instruction delivery, requested artifact/stage, timing versus intent/authority, intact commitments. | Existing work-control/reference/operator guide; no duplicate active skill, new lead or runtime control. |
| *From Sandbox to Preview*, especially pp. 4–9, 17–29, 33–35, 42–60, 64–78 (two identical PDFs) | Canonical app versus saved sandbox; branch/shared distinction; exact hosted identity; meaningful readiness and real replay; source-inspected verifier gaps. | New conditional preview/release reference and build/test routing. Recorded commands, hosts and source SHA are discovery hints, not current configuration or permission. |
| *From Preview to Production*, chapters 1–9, 11–13, 15–22 and appendices A–D | Source/artifact/configuration/schema/exposure identity; exact-source environment-specific builds; shared ownership; approval, readiness and recovery. | Same reference, not a second deployment manual or an implemented controller. Chapter 19 asks a testable health-contract question; it does not establish a current production failure. |
| `good-enough-code-quality` | Whole requirements, consequence-weighted judgment, unknown impact, source-level evidence and replay authorization. | Incremental engineering-quality patch. No imposed architecture, test count or repository-wide cleanup. |
| `startup-coding-standards` | Obligations versus guidelines/preferences; durable boundaries; complete success/failure/recovery; actual tooling. | Consolidated with existing engineering floor. Overlap does not earn another skill. |
| `good-enough-cicd` | Trusted check identity/policy, unknown impact, expected work, provider cutover and cancellation boundaries. | Narrow engineering guidance only. No selected CI vendor, replacement gate, paid runner, branch rule or configuration change. |
| `workos-production-verification` | Valid organization switching versus mismatched admission; same-source setup recovery; Records/exports beyond Files; cleanup versus incident. | Existing conditional production-verification reference. Incidents are attributed to this supplied skill's transcript account, not independently replayed here. |
| Reuploaded 1106 package | Earlier implementation/reference. | Compared, not adopted as the parent. No rollback of 1107. |

## Keep the distinctions that change execution

**A saved sandbox is not necessarily the deployable app.** The preview book describes
a separate Node/accounts/SQLite implementation and a canonical Next.js/Workers
product. Its implementation evidence is pinned to
`64db045ce8e8ace8d25cd6e8aee126d00dff302d`. The release book uses the same snapshot.
That is historical report provenance, not the version this package recommends
shipping. Hosting the prototype, transferring behavior and replacing the app remain
different tasks. Preserve useful reference work without importing private runtime state.

**A reported proof gap is not a current bug.** The preview study identifies a branch
host allowlist, off-origin authentication, doctor-host selection and local-SHA fallback
at its inspected source. The plugin now directs the agent to inspect those boundaries
when relevant and never borrow local identity to certify a remote artifact. It does
not claim to repair the actual verifier. The proposed publication commands in the book
are not exposed as real commands in this plugin.

**Readiness needs the intended contract.** Chapter 19 of the release book observes
different health-verification invocation shapes and asks whether production HTTP
semantics already protect required dependencies. The patch preserves that uncertainty:
qualify the property with healthy and unavailable-dependency fixtures, rather than
blindly copying a boolean or asserting that production is broken. No live fault test
is authorized by this source.

**CI text, live enforcement and authority can disagree.** The books report changing
Buildkite/`Veto CI` documentation. This release does not choose a winner. The execution
owner must inspect the applicable instructions, real producer/check, candidate and
protected mechanism. A proposed provider migration is not a new standing gate.

**The WorkOS regression narrows an assumption, not authorization.** The supplied skill
reports a selected-org token differing from an original-org session listing after a
legitimate switch. It retains verified token/session, current membership, canonical
binding, office and lifecycle checks. The patch keeps this as a source-attributed case
and pairs valid switching with denied mismatches and out-of-run-scope access. It does
not endorse trusting a decoded JWT or deleting organization checks. Original transcript
and current implementation were not inspected anew in this release.

The same source describes Files succeeding while Records failed on D1, plus a merged
repair whose validation was still running. Those are reasons to inspect the named
adjacent path, not proof of either a current defect or a deployed fix. Clearing a memo
for a smaller diagnostic cannot pass the original memo requirement. Known prohibited
access after a stop is an incident; unknown termination remains a hold.

## Narrow public-document cross-checks

Checked on 11 September 2026; these establish published mechanics, not Veto's live
settings or installed-client capabilities. The rest is explicitly source adaptation.

- [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins):
  portable root metadata, skills and local marketplace remain appropriate to the
  existing package shape. Metadata validity is not native loading or execution.
- [OpenAI prompting](https://learn.chatgpt.com/docs/prompting): Steer targets the
  current run and Queue the next run. Neither conveys the whole goal's dependency
  ordering or a new authority grant. Existing timing advice remains; no settings changed.
- [Cloudflare preview URLs](https://developers.cloudflare.com/workers/versions-and-deployments/preview-urls/):
  version URLs and aliases differ, and enabled preview access can expose a newly
  uploaded version. Inspect publication access before upload; a preview address does
  not establish separate storage or provider permissions.
- [WorkOS testing](https://workos.com/docs/authkit/testing): use emulation for most
  tests and smaller real-environment integration coverage; supported programmatic
  session setup and testing live Hosted AuthKit are not equivalent. This corroborates
  the retained layered-test procedure, not the historical Veto org-switch diagnosis.

No connected repository, WorkOS configuration, provider deployment or branch rule
was fetched or modified during this package update. Current commands and state must
be inspected by the authorized execution owner rather than inferred from these notes.

## Verify the change without confusing the layers

The unchanged local suite and doctor test helper/package behavior. The new behavioral
cases specify: sandbox transfer (E78), missing versus valid remote identity (E79), shared
ownership and uncertain activation (E80), production rebuild/approval boundaries (E81),
org switching (E82), false-green CI selection (E83), readiness positive/negative controls
(E84), and queue/review-stage fidelity (E85). They have not been executed by agents.

For the next authorized adoption comparison, use 1107 as the baseline unless an existing
experiment has already selected another. Hold inputs, tools, grants, candidate and
acceptance constant. Use a genuinely held-out task as well as a correct positive control.
A supplied receipt can test whether an agent preserves an unknown remote identity without
any login or deployment. An actual preview test requires its own already-authorized path.
Do not create a production-access or CI migration project to try this update.

The desired observed difference is a complete, correctly attributed handoff with less
founder reconstruction and no weakened safeguards. Publishing this package establishes
neither that improvement nor a working preview. See [verification](../VERIFICATION.md)
for the checks actually executed and [adoption](../ADOPTION.md) for the next proof.
