# Load a role or transfer its work

Use this when another model or session needs a maintained responsibility. Loading a
profile is a context operation; acting on a task still needs its actual assignment.

## Borrow expertise without appointing another owner

From the repository root:

```sh
python3 -B plugins/veto-codex/scripts/role_context.py --list
python3 -B plugins/veto-codex/scripts/role_context.py --role product-designer
```

The JSON contains the shared contract and existing role text, their relative paths and
digests, and explicit false flags for runtime change, permission and ownership transfer.
The reader verifies the selected sources against the package manifest before returning
them. An optional `--expect-manifest-sha256` checks an independently retained release pin.
It never fetches private data, starts an agent or writes a persona into global settings.

Give the result to a supported agent run with the actual question, exact candidate and
relevant original sources. Ask for a recommendation back to the existing owner. Follow
links relative to each printed source path. Read the relevant skill rather than every
other profile. A successful local read is not proof of native loading or role performance.

Example assignment:

> Read the product-designer profile from the supplied Veto Codex source. Inspect the
> attached authorized local candidate and the original requirement. Recommend the
> smallest change that makes the next action and completion state clear. Do not edit,
> deploy or change the task owner. Return source locations and the proposed check.

## Run a bounded worker on another model

Use the actual host's supported spawn/configuration path. Supply the profile, task ID,
assignment revision, exact input/candidate, permitted tools and data, write boundaries,
acceptance check, budget and stopping conditions. Inspect the effective child model and
effort once for the chosen configuration. Do not assume children use Luna merely because
the parent said “use cheap workers.”

The optional [Codex reader example](../../../examples/codex/veto-reader.toml) is inert
until deliberately installed and tested. It is a read-only example, not a general
implementation-worker configuration, and does not prove that Luna supports Max in your
client. No sample here changes your current configuration.

## Move an unfinished task

The old owner records what remains and its latest accepted revision in the working repo.
The successor reads the original assignment, handoff and current runtime state, checks
candidate identity and current permissions, and accepts the next bounded action. A pause
stays paused. A timeout does not prove an old writer stopped. Resolve conflicting active
writers through the actual runtime or authorized isolation before continuing.

Record the new run's role revision and effective model next to its task result. Preserve
prior evidence and mark affected evidence stale when its basis changes. Do not copy the
whole task record into the reusable role definition. Do not copy secrets into the handoff.

The [handoff checker](../../../plugins/veto-codex/references/handoff-record.md) checks
packet integrity, not who has current authority. The [team contract](../../../plugins/veto-codex/team/SHARED.md)
defines how an accepted transfer fits the shared result.

## Add a personal identity later

Start from the accepted source for that identity. Decide whether it is only an alias for
an existing profile, a different enduring responsibility, or just presentation. Create
another role only for distinct work. Add one reviewed registry entry, appropriate tests
and an explanation. Never derive Lunentic's remit from its name, and never let an alias
silently import its private memory, logged-in accounts or broader permissions.
