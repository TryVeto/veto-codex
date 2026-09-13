# How Veto Works with Codex

The guide to Veto Codex, for a company with one human and many possible agents.

The purpose is not to run the most agents. It is to finish useful work without Sebastian
becoming the scheduler, context restorer, or default manual tester. Keep him close to
choices that deserve his judgment. Make ordinary execution dependable enough to delegate.

## Start here

Read [the operating model](explanation/operating-model.md) for the recommendation on one
pinned coordinator, worker models and portable identities. Then follow
[one checked handoff](tutorials/one-checked-handoff.md) to see what this package actually
checks. The example is synthetic and explicitly separates author-run checks from native
agent qualification.

## Solve a specific problem

[Install or upgrade](how-to/install.md) explains the private repo and existing-plugin
path. [Use a role](how-to/use-roles.md) covers borrowing expertise, delegation, and owner
transfer. [Qualify the loop](how-to/qualify.md) is the first native-agent trial.
[Change and release the method](how-to/maintain.md) covers regression tests and releases.
[Check integrated work](how-to/check-integrated-work.md) prevents an old runtime verdict
from following a patch onto a different base. [Scope](explanation/scope.md) keeps the
Codex method separate from the ChatGPT web setup and product-reference library.

## Look up the machinery

[Repository reference](reference/repository.md) defines where things belong, the local
commands, configuration example and status labels. [Sources](reference/sources.md)
distinguishes the supplied reference material from this implementation and current host
documentation. The [plugin entry point](../../plugins/veto-codex/skills/veto-codex/SKILL.md)
is the shortest route for an agent doing work.

## What a good interaction looks like

You: “The seller's submitted correction disappears when the officer reopens the file.
Fix the authorized local candidate. Preserve the existing request and give me proof.”

The owner retrieves the original report and accepted behavior, recreates the failure,
works through the relevant cause, and exercises the same episode on the repaired
candidate. A reviewer receives the original task and exact candidate, not a request to
agree with the owner's account. You receive the before/after result and any real decision
that remains. You do not have to reconstruct the assignment or run the browser for them.

That paragraph describes the method to qualify. It is not a record of a Veto product fix
performed by this repository release.

## How to read this guide

A tutorial teaches through a controlled example. A how-to gets a particular job done.
Reference states the interface. Explanation gives the reasons and tradeoffs. Do not turn
all four into one enormous compulsory prompt. Agents should read the relevant procedure
and the actual task, not memorize this book before working.

The guide is maintained with the plugin. Change the affected explanation, mechanism and
check together. Retire obsolete advice rather than adding another exception paragraph.
