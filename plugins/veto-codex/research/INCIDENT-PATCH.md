# 2026.9.1104: repair the handoff from intent to proof

Prepared 11 September 2026. A local patch to the supplied **2026.9.1103** release, not an audit or update of the installed plugin. Baseline ZIP SHA-256: `032291924707accdae2cbcfb51c50b6ecef60fe3f801e761b21b4023411773bf`. The baseline's 129 helper/package tests were rerun before editing. See [current verification](../VERIFICATION.md) for this release's executed checks.

## Decision

Keep the 13 skills, existing feature team, Stripe-inspired direct-inspection loop, queue/steer rules, bounded bets, product boundaries and no-eyebrow rule. Add no orchestration layer. Repair three specific transitions: original feedback becoming an incomplete checklist; plausible explanation becoming diagnosis; and button wording becoming an assumed action effect.

The user supplied reports of an omitted/narrowed address-autocomplete request, a disputed sign-out explanation, a file-URL denial later overgeneralized to localhost, a separate successful Hello HTTP probe, and a form-opening action misread as a commitment. These are **reported incidents**, not failures freshly reproduced in this patch. The pasted conversation contains image URLs and references to other logs; those original incident images/logs were not retrieved or operated here. Do not fabricate verbatim annotations from their summaries.

## What changes

**Feedback.** Capture every original item with stable identity, wording, screenshot/page context, full interpreted meaning, owner and observable check. Preserve questions, supersession, repeated corrections and unresolved work across interruption. The existing independent reviewer checks whole sources against the inventory, then full intent against acceptance. Only afterward can observed behavior close the batch. A blind exploratory review remains useful, but cannot replace the informed original-feedback audit.

**Diagnosis.** Establish the approved actual HTTP preview and one interaction before substantial UI work. Record the precise candidate, session, target, tool and error. Separate reported symptoms, hypotheses and established causes. A success in another thread proves its own result only. An explicit content denial survives an unrelated successful diagnostic. Do not broaden permissions or take a different route to the denied content.

**Approval.** Supply actual effects and original scoped authority before ambiguous review, including effects on load. Form inspection and consequential submission remain distinct; labels and localhost alone establish neither harmlessness nor isolation. An optional prompt clarification is included as reference, not installed configuration. No policy file, access setting or approval mode is changed.

**Existing helper.** Extend the receipt checker with schema-2 original-feedback and coverage inputs, not a new service. Reject missing/stale/duplicate mappings and preserve open coverage alongside failing behavior. Retain schema-1 compatibility with coverage explicitly NOT_CHECKED. Mechanical consistency is not semantic truth: a fabricated reviewer report can still be internally consistent. The tests include that limitation deliberately.

## Sources and adoption boundaries

The latest supplied studies were consulted selectively for the decisions above, not reread exhaustively or installed wholesale:

| Supplied source | Relevant material | Use in this patch |
|---|---|---|
| Culture That Executes, 11 September 2026 | pp. 42–45; 79–81 | Small instruction layers, provenance, paired repair tests; no new constitution. |
| Working in Parallel, 11 September 2026 | pp. 21–25; 58–60 | Stable input revisions, ownership, source-based handoff; do not confuse runtime state with acceptance. |
| Beyond the Prompt, 11 September 2026 | pp. 32–33; 98 | Selective context and portable current work; no assumption that prose creates a runner. |
| The Delegation Contract, 11 September 2026 | pp. 14–17; 23–24; 38–39; 53–56 | Preserve intent when assigning work; inspect underlying evidence; fix the narrow failure layer. |
| The Useful Codex Plugin, 11 September 2026 | pp. 57–59 | Compare actual behavior against a credible baseline; retain holdouts and identify unexecuted trials. |

These source recommendations support the design. They are not controlled evidence that this patch improves agents, and they do not adopt new budget, release or operating mandates. Other attached organization books/skills remain optional source material rather than automatically activated workflow.

Current official platform details were checked separately:

- [OpenAI browser documentation](https://learn.chatgpt.com/docs/browser): running a development server and opening the local page is the documented UI-inspection route. The preflight acceptance rule is this patch's recommendation, not proof of any running browser.
- [OpenAI auto-review documentation](https://learn.chatgpt.com/docs/sandboxing/auto-review): compact reviewer context, explicit denials, separate app approvals and replacement—not additive—policy overrides. The optional clarification must not replace a complete effective policy on its own.
- [OpenAI harness engineering](https://openai.com/index/harness-engineering/): repository-backed task continuity and concise maps inform the source-first handoff; this is an engineering account, not a Veto result.
- [OpenAI evaluation guidance](https://developers.openai.com/api/docs/guides/evaluation-best-practices): task-specific checks and calibrated judgment inform the evaluation design. No model trial is claimed.

## Adoption test

Stage against the actual installed source and identify its loaded revision/path. Do not infer that this ZIP is installed. Preserve local customizations, current assignment, team, settings and latest pause/resume. On the next authorized run, replay one complete original feedback batch through capture → independent coverage → exact-candidate behavior → honest closeout. No fresh charter-writing round.

Check the autocomplete behavior, signed-out seller link and Back on the actual candidate where still in scope. Keep inaccessible originals, unreproduced issues and blocked browser checks visible. Compare with the prior method using whether a recorded correction must be repeated, material omissions, unsupported diagnoses, completion and founder reconstruction. Additional documents or test counts are not the success measure. Do not invent a target, customer proof or new budget.

The next useful evidence is a real run of this loop, not another expansion of the instruction library.
