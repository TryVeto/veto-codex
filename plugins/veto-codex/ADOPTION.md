# Adopt the repository edition

Version 2026.9.1203. The maintained source repository contains `ADOPT.md` and
`docs/guide/how-to/install.md`. Use those for reconciliation, installation, native
loading, qualification and rollback. This plugin folder can also be used explicitly
by a file-based agent, but that is not proof of native plugin discovery.

Rename the previous Veto Stack identity through a controlled cutover. Preserve its
canonical source history, custom changes, current
assignments, pauses and permissions. Do not author into a generated cache or register
a duplicate plugin. The repository supplies a prior source inventory, not permission
to overwrite an actual newer local version.

From this staged plugin, run:

```sh
python3 -B scripts/doctor.py .
python3 -B -m unittest discover -s tests -v
python3 -B scripts/role_context.py --list
```

Observe actual source loading and exercise a safe task in a fresh host session.
Use [portable roles](references/portable-roles.md) for delegated context. Native
configuration, identity transfer and model-cost qualification remain separate.
Keep active work and its evidence in its working repository, outside this package.

[The 1201 adoption work order](verification/1201/historical-adoption.txt) is historical;
its paths refer to its original archive, not to required files in the current repo.
