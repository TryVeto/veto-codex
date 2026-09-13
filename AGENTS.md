# Maintain Veto Codex

This is Veto’s reusable Codex method, not the application or its live work. Sebastian
is the only human. Do not make him restore routine context or operate the checklists.

Read README.md, the accepted request, and `plugins/veto-codex/AGENTS.md` before editing
the plugin. The approved rename is `veto-stack` → `veto-codex`; do not create an alias
plugin or change Veto’s separate ChatGPT web setup. The twelve other public skill names
and the nine existing role responsibilities remain stable.

Identify the exact baseline and a check that could reject the change. Read affected
implementation and tests. Keep reusable instructions here; keep application-specific
harnesses, active assignments, and private evidence in their actual working repository.
Load role instructions through `team/roles.json` and `scripts/role_context.py`, not an
invented identity or a second set of permissions.

Preserve actual source history. `migration/baseline-2026.9.1202.json` records the
preceding archive, not the state of Sebastian’s local checkout. Reconcile custom edits;
do not overwrite a divergent source or generated installed cache.

For consequential verification, replay the decisive behavior on the final integrated
candidate. A stable patch-id is not proof that a changed base behaves the same. Never
substitute the implementer’s summary for independent acceptance.

Before delivery:

1. Run `python3 -B tools/repo.py check` and `python3 -B tools/repo.py test`.
2. Check affected guide links, manifest identity, rollback, and the declared source diff.
3. Refresh hash inventories with `python3 -B tools/repo.py hashes --write` only after
   explaining the source changes. A new hash does not approve a change.
4. Package using `python3 -B tools/repo.py package --output dist`, extract into a fresh
   directory, and rerun checks and tests there.

Keep source snapshots and previous verification records unchanged. Retained test bodies
may change their package-name literals for this rename, not their assertions. Add new
regressions separately. Do not create live `.codex/config.toml`, schedulers, hooks,
credentials, remote posts, or deployment permissions by editing this repository.

Report Done / Exceptions / Next. Distinguish source checks, synthetic behavior, native
loading, independent agent behavior, hosted CI, and deployment. Never report one as another.
