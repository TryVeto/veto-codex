# Veto Codex: a Stripe-inspired product organization

Supporting product-team reference retained from **2026.9.1107**. The current agent-native method is [GUIDE.md](GUIDE.md); the following material is contextual reference, not a second controller. Use [local readiness](references/sandbox-and-local.md) and the [review protocol](references/review-protocol.md) to keep the served candidate and replay state stable. The optional [observation record](templates/review-observations.md) connects local collection to review without a new bridge. Existing requirements, pauses and approval boundaries remain.

The recommendation is to copy the mechanisms aggressively: direct user evidence, complete first use, high craft, informed ownership, easy correction and fast safe change. Do not copy another company's organizational size, branding, or rituals simply because it succeeded. The supplied study makes that distinction explicit; the public sources support particular practices, not a guarantee of the same result. [Sources](research/STRIPE-SOURCE-MAP.md)

## 1. What changes across the plugin

This is not one extra Stripe-themed prompt. The prior Stripe-inspired edition established the shared operating reference, review tools and role guides. The current 13-skill edition preserves their loop and adds explicit work control:

**Observe the job → choose a consequential change → build it together → operate the actual journey → fix the important friction → deliver within authority → examine use.**

The Head remains a hands-on integration owner. The designer carries the experience through implementation; frontend and backend contribute to the same result. PM, research and data join for specific decisions, not an organizational diagram. The reviewer examines the candidate before hearing a persuasive explanation. Good work survives review; criticism needs evidence and a consequence.

Use more effort on hard integration, distinct alternatives, direct observation and counterexamples. Do not aim for a token minimum, a fixed swarm size or perpetual debate. A short correction can remove a large obstacle. Conversely, “smallest complete” permits a substantial implementation when that is what the promised capability needs.

The source study's first-mile and support lessons become reusable defaults: make the first attempt reproducible; show useful safe examples where sample input is required; turn repeated questions into product repairs; make the next independent attempt easier. Every repeat founder annotation is a candidate for a clearer component, example or regression—not a reason to ask him again.

## 2. The best prototype package for Pro

**Keep one canonical application. Put its versioned review evidence in `sandbox/reviews/<candidate-id>/`; do not automatically copy the entire application into a second maintained `sandbox` tree.** A genuinely separate experiment may deserve its own app directory, but it needs an owner, explicit limits and an integration or retirement decision.

Recommended shape, adapted to existing repository conventions:

```text
product/
  <existing application and tests>       canonical implementation
  sandbox/reviews/<candidate-id>/
    README.md                          task, fixed constraints, questions, limits
    request.json                       independently established review scope
    manifest.json                      candidate, states, evidence and file hashes
    screenshots/                       readable originals, not chat thumbnails
    evidence/                          relevant test results and continuity records
    fixtures/                          safe scenario data or its exact source path
    source/                            optional frozen snapshot for portable review
    feedback/                          founder annotations; later informed pass
```

Source identity means the actual commit and any meaningful dirty/untracked changes. A branch name or a `git archive` of an older commit does not identify an uncommitted local preview. Establish which process/build answered the browser, its configuration and fixture version. If identity cannot be established, say so and limit the review. Do not commit private data or dependencies just to make a ZIP convenient.

The front-door README should let a new reviewer understand who arrives, the job, the useful endpoint, the intended constraints, what changed, what is simulated and which questions are genuinely open. Include exact verified run/setup/scenario commands and prerequisites when execution is supported. Do not provide made-up commands or a localhost address as though it worked on another machine.

Organize captures by **journey state**, not merely by route. The same screen may have empty, editing, validation, pending, failed, saved, changed and restricted states. Capture every distinct state needed for the requested review at readable size, with desktop/narrow variants where meaningful. A broad product review needs broader coverage; a focused label repair does not need a full museum of every screen. Include a meaningful recovery and endpoint, not only the favorable path. Keep state IDs, actor, scenario, viewport and candidate in the textual manifest or captions.

For the first Pro message, attach the README, representative full-resolution **PNG/JPEG** captures, and either the safe source ZIP or an exact permitted repository/commit/path. A contact sheet helps navigation but cannot replace readable originals. Keep the larger indexed pack available for targeted inspection. OpenAI's documentation supports repository retrieval and direct image inputs; neither implies that a connected model ran the app. Do not assume it saw images embedded in a PDF or browsed all repo screenshots. The current image FAQ also describes video attachment support with platform/account and analysis limits: a short walkthrough can supplement the pack, but keep decisive still frames and reproducible steps. [OpenAI source details](research/STRIPE-SOURCE-MAP.md)

The optional [pack helper](references/review-pack.md) checks a separately pinned request against supplied files and state coverage, then creates an indexed ZIP. It does not take screenshots or judge the product. It excludes files explicitly classified as founder/builder feedback by default. Share those only after the first-pass review. Do not call a review blind when the reviewer already saw the opinions.

Start with [the ready-to-paste review prompt](templates/pro-review-prompt.md). Ask for consequential findings, exact locations, preserved strengths, the best correction and what must be tested. Ask for no minimum number of defects. “No supported finding” is a legitimate result.

## 3. Make these reviews a team responsibility

The missing capability is not another executive persona. It is a reliable path from a changed candidate to an observable review, an accountable repair and a recheck.

**At the first real join and before handoff:** the Head identifies the candidate and task; a fresh reviewer operates it using the authorized browser or reviews the available packet; findings enter the existing work record; the relevant builder repairs them; the reviewer checks the changed state and affected journey. The Head resolves ordinary product/engineering tradeoffs. Sebastian sees reserved decisions, material unresolved risks and the resulting candidate—not every screenshot task.

A review must operate the product without a private explanation of what each screen was supposed to mean. Try the main act, a meaningful interruption, correction and the endpoint. Review what is useful first, whether the meanings/state agree second, and craft throughout. Preserve accessible labels and genuine distinctions while removing repeated framing. Use the existing acceptance contract; do not let the builder rewrite the required checks to fit the result.

The latest screenshots suggest useful conditional checks: can an officer find seller-link creation when it is the real next task; do labels distinguish the seller from an app account, reviewer and downstream colleague; is navigation state visible; can a reviewer obtain safe sample input without asking you; do seller collection and buyer funding remain distinct tasks in the same file? These are feedback patterns, not findings newly reproduced here. A seller-link button must not stay primary after the seller has already contributed. A waiting state need not invent an action.

Every sandbox input should provide the relevant fictional specimen or an explicit explanation of why a specimen is unavailable. Copy/Fill is a deliberate action; it does not submit, approve, change role, silently replace a draft or contact a real recipient. Test identifiers need enforced nonlive routing—plausible-looking account numbers and a banner are not enough. [Sandbox rules](references/sandbox-and-local.md)

Give the team the practical capabilities needed: a known workspace and run route, scenario reset limited to owned data, permitted browser/render access, local test output, safe storage for evidence and a way to hand the exact candidate to a separate reviewer. Preserve the existing Codex-browser restriction. Do not route around a policy failure with a different browser or public tunnel.

For reviews during an active authorized run, the lead can invoke this method without another founder prompt. **Unattended later runs require a real existing runner/event hook and its permissions.** This edition does not install one or schedule Pro. The first implementation task is to connect the existing authorized host's candidate-ready event to the review step, if that capability exists—not to build an agent platform. If it does not exist, finish the review in the current run and report that scheduling remains unconfigured.

## 4. Build agents with earned opinions

An agent cannot become the better expert by being called an expert. It needs decision rights, superior task evidence, a way to test alternatives and a record of being right or usefully correcting itself.

Treat founder suggestions as distinct from founder decisions. A suggestion about means can be challenged. A clear adopted product constraint must be preserved. An informed, authorized and permissible final decision gets executed even when the agent still records a tradeoff. More confidence is not more authority.

For an open material choice, have the specialist commit to its best first-pass recommendation before showing the founder's preferred answer. Give it the goal, constraints, sources and candidate, but not social pressure to praise the builder. Keep safety information and contrary evidence. Then compare the proposals on the same task and run the smallest discriminating test. An independent context reduces one source of anchoring; it does not supply independent evidence or cure every model bias. [Judgment method and research limits](references/independent-judgment.md)

Require a decision-ready objection, not a performance of dissent:

> I recommend this mechanism rather than the proposed one because of this observed consequence. It preserves these constraints. The strongest contrary case is this. I would change my mind after this test. This is the action I will take within my authority.

Do not require three objections, five findings or a critic who always votes no. Such quotas punish correct agreement. Likewise, do not reward confident agreement simply because it feels efficient. Track consequential misses, false alarms, good decisions preserved, useful alternatives, verified repairs and founder intervention—not eloquence. Use qualified human calibration where the claim requires it; an agent impersonating an escrow officer is not that evidence.

Your side of the arrangement is to give the outcome before the preferred solution when possible, make decision rights clear, reward demonstrated corrections, and avoid overruling a supported specialist choice merely by repeating a preference. This does not mean accepting every criticism. Demand the source, consequence and test. The desired relationship is an expert colleague with a view, not an agreeable subordinate or a reflexive contrarian.

The [calibration plan](evals/JUDGMENT-CALIBRATION.md) compares old and new instructions on representative tasks. Until that comparison is run, better behavior is the design intent—not a measured outcome.

## Activate without restarting the organization

Use the [README activation message](README.md). Preserve useful code, current context, unrelated skills, permissions and the latest pause/resume instruction. Do not restart charter writing or assume installation resumed the product goal. On the next authorized substantial candidate, complete one neutral review-and-repair cycle and retain its evidence. That is the first useful test of this edition.

## Current control model

The prototype/review practices above remain. In 2026.9.1103, use [the queue, steer and goal-mode guide](OPERATOR-GUIDE.md) for managing ongoing work. Keep one active bounded bet under the accepted commitment. Routine annotations can wait for a named checkpoint; evidence that defeats the current approach should change it. An update does not automatically activate a new goal, resume work or authorize another bet.
