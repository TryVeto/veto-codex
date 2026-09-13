# Veto Codex

**How Veto’s agents work in Codex.**

Skills, tools, verification, and handoffs—with a guide for the human directing them.

[**Read the guide**](docs/guide/README.md) · [**Install Veto Codex**](docs/guide/how-to/install.md) · [**Inspect the agent entry point**](plugins/veto-codex/skills/veto-codex/SKILL.md)

Sebastian is the only human in Veto. He sets direction, judges the experience, and makes
reserved decisions. Agents carry the investigation, design, implementation, coordination,
checks, and handoffs. The aim is finished work, not a larger roster of agents.

This repository is the source for that method in **Codex**. Veto’s separate ChatGPT web
setup stays separate. This package does not install instructions into ChatGPT.com,
change connected accounts, or create another management application.

## Give the outcome

> Use Veto Codex. Fix the reported save-and-reopen problem in the authorized local
> candidate. Preserve the submitted request and its office/file identity. Reproduce
> it first, verify the same path afterward, and return the working result with evidence.
> Do not deploy or use live customer data.

The owner establishes the starting state, chooses the relevant procedure, and delegates
only where it helps. It runs the work, checks the result, and leaves a resumable record.
A separate reviewer checks the actual candidate when independent acceptance is required.
Failures, missing access, and unrun checks remain visible.

Start with [one checked handoff](docs/guide/tutorials/one-checked-handoff.md). It is a
runnable synthetic example, not a claim about a real transaction or an autonomous agent.
[Native qualification](docs/guide/how-to/qualify.md) is a separate exercise.

## One place to direct work; reusable expertise underneath

Use one primary pinned coordinator as the usual entry point. Keep useful specialist
conversations and direct access to their original work. Do not force every undertaking
into one endless conversation or create a hierarchy of approval requests.

The existing nine [role profiles](plugins/veto-codex/team/roles.json) are reusable
instructions. A role can be loaded by a qualified model; it is not a model, a running
session, credentials, or permission. A builder adopting the verifier role is still
self-review.

[Coordinator and model choices](docs/guide/explanation/operating-model.md) ·
[Load a role](docs/guide/how-to/use-roles.md) ·
[What belongs here](docs/guide/explanation/scope.md)

## Readable source; executable method

```text
veto-codex/
├── README.md
├── AGENTS.md                    # Maintain this repository
├── docs/guide/                  # Tutorial, how-to, reference, explanation
├── plugins/veto-codex/          # The one installable plugin
│   ├── skills/                  # 13 public skills, one entry point
│   ├── team/                    # Nine reusable role profiles
│   ├── playbooks/               # Five contextual procedures
│   ├── scripts/                 # Offline checks and context helpers
│   ├── tests/
│   └── evals/                   # Behavioral cases; not claimed native passes
├── migration/                  # Previous identity, exact baseline, safe cutover
├── tools/                      # Source checks, tests, packaging, catalog planner
├── tests/
└── .github/workflows/           # Checks and packaging; no deployment
```

Application-specific verification belongs beside the application. Active work and
private evidence belong with their undertaking, not in an installed plugin cache.
The [reference-library boundary](docs/guide/explanation/scope.md) keeps product
inspiration separate from the Codex operating method.

## Run the checks

Python 3.11 or later. No third-party Python dependency is needed.

```sh
python3 -B tools/repo.py check
python3 -B tools/repo.py test
python3 -B plugins/veto-codex/scripts/role_context.py --list
python3 -B tools/repo.py package --output dist
```

`package` reruns checks and tests before creating a reproducible source ZIP. The source
archive includes dot-directories. The commands do not install the plugin, spawn workers,
change a goal, or deploy anything.

## Renamed from Veto Stack

This is version **2026.9.1203**, continued from the supplied **2026.9.1202** repository.
The repository, package, and entry skill are now `veto-codex`. The other twelve skill
names remain unchanged. History is not rewritten into a new name.

The rename changes the host-facing identifier. Existing users must follow the
[migration](migration/README.md): preserve the current source and settings, disable the
old identity, and qualify the replacement. Do not leave both plugins active or assume
that renaming a source folder renames an installed copy.

Publish the contents of `veto-codex/` as your private repository root. Use the migration
patch for an existing checkout rather than starting over and losing real Git history.
No hosted repository or synthetic commit history is included.

## What has been proved

See the [verification record](verification/README.md) for executed checks and the
[change log](CHANGELOG.md) for scope. **Native loading, worker dispatch, independent
agent qualification, and hosted CI remain unrun.** The local checks are not substitutes.

Give the local agent [ADOPT.md](ADOPT.md) for the complete adoption assignment.
