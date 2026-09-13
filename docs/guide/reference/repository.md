# Repository reference

## Ownership of files

| Location | Responsibility |
| --- | --- |
| Root README / docs/guide | Human entry, explanation, tutorials, operating instructions |
| Root AGENTS.md | Instructions for maintaining this repository, not universal policy |
| plugins/veto-codex | Installable continuation, renamed from Veto Stack |
| Plugin skills | Named reusable methods; same 13 public entries |
| Plugin playbooks | Conditional lifecycle procedures |
| Plugin team | Existing nine role guides and their explicit index |
| Plugin scripts / tests | Offline checks and helper regressions |
| Plugin evals | Behavioral specifications; no automatic claim they were executed |
| examples/codex | Inert native configuration example, not auto-installed |
| tools / tests | Repository validation and release tooling |
| verification | Dated author-run checks and limitations |
| provenance | Baseline identity and scope; not active instructions |

Actual `verify-veto`, the Feature Map and application driving commands belong in the
product repository. Runtime permissions belong in the actual host and connected systems.
An assignment's current owner, revision, pause, evidence and next action belong in its
working record. Credentials, customer evidence and private identity memory are not
portable plugin material.

## Local commands

All commands start at this repository root and use Python 3.11+.

| Command | Effect |
| --- | --- |
| `python3 -B tools/repo.py check` | Read source, verify structure/hashes/links; nonzero on failure |
| `python3 -B tools/repo.py test` | Run local plugin/repo tests and synthetic oracle probes |
| `python3 -B tools/repo.py hashes --write` | Explicitly rewrite source hash inventories |
| `python3 -B tools/repo.py package --output dist` | Run checks/tests, then create new deterministic ZIP and sidecar |
| `python3 -B plugins/veto-codex/scripts/role_context.py --list` | Return registered role IDs and manifest digest |
| `python3 -B plugins/veto-codex/scripts/role_context.py --role ROLE` | Return checked role/shared instruction content; no runtime action |

Repository tests execute supplied Python in temporary locations and can write disposable
fixtures. They do not call an AI provider. Plugin helpers retain their documented effect
boundaries; the new role reader is read-only. No tool in this repo provides a distributed
lock, native scheduler, role checkout service or proof of permission.

## Supported role context

The registry schema has `schema_version`, a fixed ordered `shared` source list, and a
`roles` map from stable role ID to its `team/<id>/AGENTS.md` path. It contains no model,
permission, account or active task fields. The helper rejects extra fields, path aliases,
escaping paths, symlinks, hash mismatch, empty text and oversized role material. Optional
manifest pins detect a different local release; they do not authenticate the author.

Packet source paths are relative to the plugin root. Each source includes exact content
and SHA-256. The context fingerprint binds the ordered source paths and hashes. Flags
for native loading, authority, ownership and independent review remain false because
preparing context performs none of those acts.

## Host configuration example

[examples/codex/veto-reader.toml](../../../examples/codex/veto-reader.toml) illustrates a
read-only bounded reader using an explicitly named model and effort. It is not in an
active `.codex/agents` directory. After separate adoption, verify current host support,
source loading and effective permissions, including inherited runtime overrides. Do not
turn the reader into a release agent by editing a role label.

## Status vocabulary

**Proposed:** a recommendation or test design. **Packaged:** source exists in this release.
**Locally checked:** named deterministic checks actually ran on identified bytes.
**Natively observed:** a host/run observation exists for the stated behavior.
**Independently reviewed:** a different qualified run reviewed the actual scope and
candidate; it is not merely a second persona. **Authorized:** the proper owner permitted
a specific act. **Deployed:** an actual deployment is observed. These labels are separate,
not an automatic progression supplied by publishing the repository.

## Rename planner

`python3 -B tools/migrate_catalog.py --catalog <local-json> --source-path ./plugins/veto-codex`
returns a proposed local catalog to stdout. It performs no writes. Migration instructions
and the old-source inventory are under `migration/`. Current source identity is
`veto-codex`; prior records intentionally retain `veto-stack`.
