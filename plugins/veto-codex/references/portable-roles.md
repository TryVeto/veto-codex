# Load a role, not somebody else's authority

A role is a reusable responsibility and method. A model is the engine used for a run.
A task record preserves current work. The host and the accepted assignment determine
access and authority. None of these substitutes for the others.

The maintained profiles are the existing nine [team guides](../team/SHARED.md), indexed
in [roles.json](../team/roles.json). They are not new workers, registrations, or a
second organization. A personal name can point to an accepted profile; it must not
supply an invented responsibility or a hidden credential.

## Obtain the context

From the plugin root:

```sh
python3 -B scripts/role_context.py --list
python3 -B scripts/role_context.py --role backend-engineer
```

The helper checks the local manifest and returns JSON containing the shared contract,
role guide, paths and their SHA-256 digests. It is read-only. It does not start an agent,
change a model, install instructions, claim a task, read private memory, or grant access.
Integrity against a local manifest does not authenticate its author. Review the source
before treating its instructions as trusted. Relative references remain relative to the
source file shown in the packet, not the recipient's working directory.

## Apply the context

Use the host's actual supported delegation mechanism. Send the selected role material
with the original request, current task and assignment revision, exact candidate,
allowed operations, evidence location, stopping conditions and returning owner.
Read the relevant referenced skill when needed. Confirm that the recipient actually
loaded the intended sources and received the correct assignment. A printed packet is
not proof that a running agent used it.

Use an explicit model and supported effort for workers when cost is part of the
experiment. Check the effective spawned configuration rather than assuming a cheap
worker was selected. If the host cannot expose or honor that choice, report the limit;
do not label the run a measured cheap-worker experiment.

## Borrow judgment or transfer responsibility

For a bounded consultation, another agent can load the same profile and return advice.
That does not replace the current execution owner. An owner transfer needs an accepted
handoff, current revision and evidence; old writers must be stopped or their write scope
fenced through the actual authorized runtime. Loading a new role cannot clear a pause,
revive superseded work, or inherit another agent's credentials or approvals.

Never treat the builder switching to the verifier profile as independent review.
Use a separate run with the original assignment and exact artifact. Prefer a fresh,
artifact-first context and disclose any shared assumptions or prior explanations.
Another model alone is not an independent source. If a verifier authors a fix, obtain
another reviewer for that change or label the result self-review.

Names such as SOUL.md may hold optional voice or working preferences, but they are not
special authority files. Keep secrets and active task state outside the distributed
plugin. The requested name Lunentic has no supplied accepted charter in this package;
resolve its real role source before creating an alias. Do not guess it from the name.
