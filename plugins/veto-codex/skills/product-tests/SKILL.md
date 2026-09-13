---
name: product-tests
description: "Define, run or assess Veto acceptance, Git candidate identity and WorkOS auth evidence; plan scoped production verification. Does not grant repair, release, access or customer-contact permission."
---

# Product tests

Establish what happened, not whether a completion story sounds convincing. Read [working boundaries](../../references/working-contract.md), the accepted goal/contract and relevant [Veto invariants](../../references/veto-contract.md). A test-plan request ends at the plan. An audit stays read-only; running checks and repair require their actual authority.


## Acceptance includes independent product review

Use [the review protocol](../../references/review-protocol.md) for material user-facing changes. Start from the task, fixed constraints and exact artifact, not the builder's explanation. Test the ordinary sufficient case as seriously as refusal, plus legitimate repair. Use [independent judgment](../../references/independent-judgment.md) to resolve conflicting assessments with evidence, not hierarchy or a vote.

Select tests that can defeat the claim. For the screenshot-derived regressions, test state-appropriate main actions, comprehensible party/reviewer/recipient labels and safe sample inputs; see the protocol's bounded cases. More confident critique or a changed screenshot baseline is not fresh acceptance. [Review-pack checks](../../references/review-pack.md) establish packaging consistency only.

## Audit coverage before testing the checklist

For feedback-driven work, follow [source-to-acceptance coverage](../../references/feedback-coverage.md). Read the actual complete annotation batch, not only the builder summary or selected checklist. Check missing items, narrowed clauses, questions and supersessions. Use the existing independent verifier, not a new committee. Missing originals or unresolved required items prevent a full batch-completion claim. Coverage and behavior are separate gates; test results cannot prove that the checklist captured the request.

## Fix the target and oracle

Identify candidate source plus dirty diff, environment, configuration, data fixture, route and scope. Locate the accepted requirements outside the builder's result receipt. Do not let the builder remove gates, change their meaning or refresh expected snapshots to certify its own output. A genuinely incorrect test may be corrected with source evidence and recorded agreement.

Choose [acceptance cases](../../references/acceptance-cases.md) by actual dependencies. A case catalog is not a backlog. Pair ordinary sufficiency with relevant refusal, repair and continuation. Use one connected fixture per episode rather than stitching separate demos into a pass. Inject faults only in disposable synthetic or expressly permitted historical environments.

## Test the distinct layers

| Layer | Evidence | Not supplied by that evidence alone |
|---|---|---|
| Rules | Permissions, versions, concerns, exact transformations and valid transitions. | A usable real interface. |
| Persistence/service | Saved identity and basis, restart, concurrency, operation reconciliation and adapter contract. | External provider or destination behavior from a mock. |
| Rendered journey | Operated supported UI, source inspection, correction, keyboard, help, truthful status, same-job retrieval. | Uncoached human comprehension or full accessibility conformance. |
| AI preparation | Source fidelity, omissions, contradictions, insufficient answers, useful uncertainty and disagreement. | Source authenticity, professional judgment or customer value. |
| Operations | Actual accepted owner, help delivered, agreed endpoint, coverage and supported recovery. | Bank execution from review completion. |
| Field value | Permissioned uncoached task observation and predeclared comparison with total burden. | Paid demand, prevention or scalable economics from one example. |

For AI evaluations, preserve model/prompt/tool/retrieval/case versions, held-out cases and qualified grader calibration. Repeated model agreement is not new external truth. Observe ordinary false alarms as well as missed problems. A correct refusal that strands legitimate work is incomplete.

## Challenge convincing failure

Ask what could look successful while the promise fails. Try wrong actor/file, simultaneous concerns, changed basis, absent original, irrelevant reply, interrupted or ambiguous save, undelivered help, failed filing and returning colleague as relevant. Test the successful repair, not only the block. Check truthful completion across file, queue and counts.

Inspect rendered output at named viewports and actual critical states, including long text and narrow layout. Review source adjacency and no decorative eyebrows semantically. Keep labels, status and disclosures. Automated accessibility and static slop checks are supporting evidence, not whole-product grades. Open the produced captures; a command that wrote a screenshot is not visual review.

For important regressions, mutate a disposable copy so the target property breaks and confirm the test detects it. Never mutate live transactions or weaken protected acceptance. Separate builder test development from final independent verification when the runtime supports it.

## Respect engineering and production test boundaries

For code/CI, apply [the engineering floor](../../references/engineering-quality.md); retain skips and retries. [Git handoff](../../references/git-workflow.md) distinguishes dirty, reviewed and integrated specimens. Hosted checks use [candidate-bound delivery](../../references/preview-and-release.md), not local SHA/HTTP 200. Auth changes use [WorkOS qualification](../../references/workos-environments.md): healthy controls, real assurance and configuration identity. Production also requires [bounded access and termination](../../references/production-verification.md). Keep broad fault injection nonproduction.

## Keep evidence usable

Use statuses **passed, failed, not_run, blocked, not_applicable**; N/A needs a scope reason accepted outside the builder's receipt. Record steps/command, expected/actual result, layer, provenance, exact candidate and evidence locations. Reuse earlier evidence only with a documented unchanged-input/environment rationale, labeled carried rather than freshly run.

The optional [receipt checker](../../scripts/check_receipt.py) compares a receipt with a separately pinned contract and local artifact hashes. Read [its format and limits](../../references/evidence.md). For feedback-batch completion, use `--require-feedback` with the independently pinned schema-2 contract, feedback and coverage audit; an evidence-only legacy result cannot close that batch. It cannot authenticate the author, prove execution, enforce release rights or inspect whether a screenshot tells the truth. A digest does not protect a contract if the builder controls the trusted digest too.

## Return a scoped verdict

Report acceptance for the actual stage: verified local candidate, not production release; simulated destination, not actual filing; authored scenarios, not executed tests. A material integrity or authority failure blocks readiness for its affected route. Missing evidence remains unverified, not assumed defective or passed.

Return reproducible findings in consequence order and the single next needed check or repair. Retain successes and limitations. If the candidate changes, rerun affected checks before approving that candidate. Do not keep testing unchanged code merely to generate activity.

## Test work control separately from product behavior

When evaluating this plugin, include the [queue/steer and goal scenarios](../../evals/cases.json): an ordinary queued correction, a consequential steer, explicit pause, a late worker return and a completed bet with open parent obligations. These are test specifications, not completed trials. Test in an actual authorized host and observe behavior; finding expected words in a skill is not the behavioral result.

For application changes, choose [primitive invariants](../../references/primitives.md) by dependency. The bundled [Prepare This Review example](../../examples/prepare-this-review/README.md) is a frozen synthetic reference, not production authentication, server persistence or an external-delivery oracle.

Use [application verification](../../references/application-verification.md) for the maintained launch and replay route.
