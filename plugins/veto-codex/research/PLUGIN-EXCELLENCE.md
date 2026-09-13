# What makes a plugin excellent—and what Veto Stack does about it

Research and design decisions · 11 September 2026

## Judgment

An excellent agent plugin makes a recognizable class of work easier to finish correctly, with less user coordination and fewer avoidable failures. It activates when relevant, stays out of the way when not, supplies context and tools that actually help, and leaves an inspectable result. A plugin containing more skills, personas, hooks or integrations is not necessarily more capable.

That is this release's design thesis, not an empirically established universal score. The package is a tested implementation of local helpers and a research-informed set of workflows. Its effectiveness in Sebastian's agent environment still needs the actual-host and behavior comparisons described below.

## What was reviewed

This review used current primary specifications and authoring guidance, the public plugin/skill artifacts listed below, the earlier supplied Veto Stack ZIP, the feature-team charters/skill, and the attached Veto product studies and six skill files. It examined concrete mechanisms: manifest identity, discovery descriptions, resource paths, workflow scope, failure behavior, authority, progressive loading, evaluation and upgrades.

This is a broad, curated review—not an exhaustive audit of every plugin or a controlled ranking. Public repositories are living sources; URLs record inspected artifacts, not immutable commits. No third-party plugin was installed or benchmarked. No claim that a company's success was caused by its plugin is made. External packaging guidance, internal product requirements, report recommendations and newly authored implementation remain distinguishable in the [source map](SOURCE-MAP.md).

## The quality standard

### 1. A specific useful job

A plugin needs a purpose a person can recognize before installation. “Ten expert agents” names components, not a benefit. For Veto the benefit is stronger product choices, a complete integrated capability, deliberate craft and credible acceptance—not a larger simulated organization.

The proof question is counterfactual: what task becomes more likely to finish, or needs less intervention, with this plugin than with the existing agent and tools? That question can produce a useful smaller plugin. It also justifies substantial instructions when a difficult recurring distinction would otherwise be lost.

**Implementation:** one entry workflow owns the existing outcome. Narrow requests route directly to the applicable skill or no skill. The package does not impose a new project system, codebase, model configuration or mandatory headcount.

### 2. Discovery that does not crowd the work

OpenAI's 11 September guidance warns that accumulated skill descriptions can crowd context and be shortened by the host. It recommends revisiting old scaffolding as model capability improves. The implication is selective, compact activation rather than an ever-growing library of broadly overlapping descriptions. [W2]

**Implementation:** nine entry points with brief, differentiated descriptions. Whole-outcome delivery, product decisions, open design, craft, engineering, verification, integrations, field evidence and goal writing are distinct. The exact package inventory and description-character total are checked by the local doctor. Character count is not a claim of token use or model performance.

### 3. Context at the point of decision

Agent Skills guidance emphasizes project-specific expertise, moderate detail and coherent workflows, with deeper references loaded when needed. It recommends tracing real execution rather than assuming a well-written instruction is sufficient. [W5]

**Implementation:** short workflow bodies with shared working/Veto contracts and task-specific references. The hundreds of pages of source studies are not bundled into every runtime context. Team roles, test catalogs, first-feature/surface proposals and research are available without compulsory ingestion. Safety-critical recurring mistakes remain near the relevant action rather than hidden in a general reading list.

### 4. One consistent product meaning

The supplied Veto sources repeatedly distinguish an accepted service, the engine needed to perform it, and the interface a customer must attend. They also distinguish a supplied source, interpretation, professional act, issued result, normal-file handoff and bank outcome. Flattening those distinctions would make the plugin shorter but the product less trustworthy. [I1, I3–I7]

**Implementation:** preserve those semantics in a shared domain contract and continuity reference. The surfaces and integration recommendations remain proposals with conditions, not an adopted architecture or evidence of implementation. Historical prototype defects become regression candidates, not perpetual declarations that today's application is broken.

### 5. A complete workflow without ceremony

Useful autonomy includes selecting a consequential bottleneck and carrying a bounded outcome through its joins. It does not mean that every edit starts a PM brief, design exploration, frontend/backend handoff, review committee and retrospective. The attached autonomous-development material specifically distinguishes method discretion from authority to affect the outside world. [I8, I9]

**Implementation:** a hands-on Head, stable designer/frontend/backend responsibilities, conditional specialists and independent challenge. The Head owns the canonical preview and integration. Role addenda are not automatic subagent registrations. Setup-only and paused tasks stop at the setup boundary. The founder is not the routing layer for routine specialist handoffs.

### 6. Deterministic checks where there is a real oracle

Syntax, identity, package paths and artifact consistency can be checked mechanically. Product usefulness, source truth and user comprehension cannot be reduced to finding words in a Markdown file. The distinction matters because a polished receipt can be as misleading as a polished interface.

**Implementation:** `doctor.py` checks this package's structure; `lint_slop.py` returns literal source-pattern review candidates; `check_receipt.py` compares results against a separately pinned contract. The receipt cannot silently choose its own requirements. Missing browser/field evidence cannot masquerade as another layer. These are local consistency checks, not proof that events occurred or permission to release.

### 7. Failure that preserves truth and legitimate progress

An excellent plugin does not succeed by preventing all action, nor by pretending that a failed external boundary is complete. It should preserve completed work, distinguish failure from uncertainty, identify the actual missing condition and continue independent authorized progress.

**Implementation:** ordinary sufficient cases and useful repair are positive acceptance conditions. Unknown saves reconcile the original operation; failed notices/filing do not repeat committed decisions. A required browser denied by policy remains unverified, not substituted with a tunnel or another browser. An exhausted method changes hypothesis rather than producing more status messages.

### 8. Minimal capability and explicit external effects

OpenAI's security guidance emphasizes constrained access, consent and treating untrusted input appropriately. Its app guidelines require a clear purpose and reliable behavior, but following written guidance is not certification. [W7, W8]

**Implementation:** no MCP server, hooks, credentials, telemetry, automatic updates, external connections or deployment automation. This plugin's missing capability is not another account connector; it is reusable product judgment and acceptance. The host's actual controls still govern tool use. A future connector needs a separately reviewed purpose, data/permission contract and recovery path.

### 9. Installation and upgrades that preserve the user's work

The current portable Agent Plugins manifest provides shared identity; host extensions carry presentation details. OpenAI supports root manifests and its compatibility overlay. Claude Code documents its own metadata and validation mechanisms. These formats are not interchangeable with automatic agent registration. [W1, W3, W4]

**Implementation:** portable root manifest, synchronized OpenAI and Claude metadata, a local OpenAI marketplace wrapper, existing brand asset, explicit loading instructions and a migration map. The edition stages beside the old stack. It does not overwrite unrelated skills, a personal catalog, repository instructions, the active goal or running application. Native-host acceptance remains untested until the receiving agent performs it.

### 10. Evaluation that can say no

The Agent Skills evaluation guide recommends fresh-context comparisons against no skill or the previous edition, examining actual artifacts and traces. Its emphasis on small initial case sets informed the three starter exercises rather than a requirement to run every case at installation. [W6]

**Implementation:** three supplied fixtures for consequential prioritization, functional-label-preserving craft and paused setup; eighteen total host-neutral scenarios including negative triggers. The mechanical oracles are tested on deliberately broken and corrected fixtures. That establishes some oracle sensitivity, **not that any model using this plugin performed better**. Real comparative runs, costs, interventions and visual judgments remain to be observed.

## Public examples: transfer the mechanism, not the whole stack

| Artifact inspected | Useful mechanism | Deliberately not imported |
|---|---|---|
| OpenAI Figma manifest [E1] | Clear concrete workflows and explicit component identity. | Figma account access or a new design source of truth. |
| OpenAI Notion manifest [E2] | Cohesive related workflows with declared integrations. | A new workspace requirement or inherited Notion permission. |
| OpenAI Build Web Apps manifest [E3] | A workflow-focused plugin need not declare a custom server. | Payment/deployment authority from an example's use cases. |
| Anthropic plugin-dev README [E4] | Structure, purpose, validation and testing treated as a maintained toolchain. | Every optional hook, command or agent as mandatory machinery. |
| Its plugin-structure skill [E5] | Discoverable layout and explicit relative resources. | Older example conventions over current normative schemas. |
| Anthropic skill-creator [E6] | Execution, output inspection and iterative evaluation. | A claim that the presence of evaluation prompts equals evaluation results. |
| gstack README [E7] | Recognizable work modes and explicit review/QA responsibility. | Browser replacement, updates, cookies or a mandatory full operating stack. |
| Impeccable entry skill [E8] | Task-scoped critique/refinement and purposeful design judgment. | A blanket aesthetic, arbitrary iteration cap or new tool permissions. |

These are eight inspected public artifacts, not eight tested plugins or independently demonstrated world-class outcomes. The toolkit uses original synthesis rather than vendoring their implementation.

## Concrete design choices versus the previous Veto package

The prior release already contained product skills, anti-slop heuristics and local tests. This edition should not claim to have invented those. Its meaningful changes are consolidation around the stable feature team, integration of the new surface/first-feature/PM/integration studies with adoption limits, shorter discovery descriptions, explicit native packaging, and separate acceptance-contract identity.

The earlier receipt shape placed requirements inside the completion receipt. That can be convenient, but it permits a builder to decide what it is graded on unless some other system protects the criteria. This edition separates contract and receipt and requires an externally recorded digest. The limitation remains explicit: changing both trusted contract and digest defeats independence. Host enforcement—not stronger wording—must protect that boundary.

The earlier scanner treated several named decorative patterns as errors. This version treats every match as contextual review because a functional label can use an overline class and decoration can be produced without one. The product rule remains strict; the heuristic's authority becomes narrower. That is a stronger acceptance design, not a weaker no-eyebrow preference.

The old source files and new sources are mapped rather than blindly concatenated. Basecamp remains an optional coordination reference. The plugin does not merge the old complete installed stack it cannot inspect, or promise that all earlier named commands exist as aliases. The migration record makes those changes visible.

## How to judge this release after installation

First establish that the intended edition loads and selects the right workflow. Then run the three starter tasks against the old stack under comparable settings. Require the critical saved-path repair to outrank cosmetic work, craft to preserve meaning while removing decoration, and setup to preserve the pause. Inspect actual effects and burden, not reassuring final prose.

Only then extend to the remaining scenarios and a real authorized development task. Keep technical correctness, rendered quality, actual operations and customer value separate. If the plugin creates needless work or overtriggers, remove the responsible instruction. If a serious omission recurs, add the smallest rule/example/test that prevents it. Do not respond to every mistake by adding another skill.

The evidence needed to call Veto Stack excellent is repeated useful completion with less avoidable intervention, while the user's decisions and boundaries survive. This release makes that standard testable; it does not claim the result in advance.

## Primary references

Sources inspected on 11 September 2026; living pages may change. Source descriptions establish documented patterns, not measured Veto performance.

- **W1** — OpenAI, [Package your plugin](https://developers.openai.com/plugins/build/plugins).
- **W2** — OpenAI, [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra), 11 September 2026.
- **W3** — Agent Plugins, [1.0.0 manifest schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json).
- **W4** — Anthropic, [Claude Code plugins reference](https://code.claude.com/docs/en/plugins-reference).
- **W5** — Agent Skills, [Best practices for skill creators](https://agentskills.io/skill-creation/best-practices).
- **W6** — Agent Skills, [Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills).
- **W7** — OpenAI, [Security and privacy](https://developers.openai.com/plugins/guides/security-privacy).
- **W8** — OpenAI, [Plugin guidelines](https://developers.openai.com/plugins/app-guidelines).
- **E1** — OpenAI, [Figma plugin manifest](https://github.com/openai/plugins/blob/main/plugins/figma/.codex-plugin/plugin.json).
- **E2** — OpenAI, [Notion plugin manifest](https://github.com/openai/plugins/blob/main/plugins/notion/.codex-plugin/plugin.json).
- **E3** — OpenAI, [Build Web Apps plugin manifest](https://github.com/openai/plugins/blob/main/plugins/build-web-apps/.codex-plugin/plugin.json).
- **E4** — Anthropic, [Plugin development toolkit](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/plugin-dev/README.md).
- **E5** — Anthropic, [Plugin structure skill](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/plugin-dev/skills/plugin-structure/SKILL.md).
- **E6** — Anthropic, [Skill creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md).
- **E7** — Garry Tan, [gstack](https://github.com/garrytan/gstack/blob/main/README.md).
- **E8** — Paul Bakaus, [Impeccable entry skill](https://github.com/pbakaus/impeccable/blob/main/.agents/skills/impeccable/SKILL.md).
