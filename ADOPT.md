# Adopt Veto Codex

For the local Codex agent. Replace the existing Veto Stack method with this source,
without creating a second active plugin or modifying Veto’s ChatGPT web setup.
The user will publish the private repository separately. Do not create a remote,
change active goals or models, install hooks, connect accounts, or deploy the product.

## Reconcile source

Read README.md and migration/README.md. Locate the actual authoring checkout, Git status,
marketplace, installed identity, and overrides. Preserve uncommitted and custom work.
Do not edit a generated cache as source. The baseline is the supplied 2026.9.1202 archive,
not an assertion about the local machine. Apply the accompanying migration patch only
against a matching base; otherwise reconcile explicitly. Preserve real Git history.

Run:

```sh
python3 -B tools/repo.py check
python3 -B tools/repo.py test
```

## Cut over the one plugin

Use `tools/migrate_catalog.py` to prepare a read-only change to an existing local catalog.
Review the exact proposal and resolve its target relative to the marketplace root.
Keep the marketplace name, unrelated entries, and their policies. Preserve an actual
rollback copy before changing the source or host settings.

Disable `veto-stack` in the actual host before enabling `veto-codex`. Use the supported
host controls; do not assume deleting a catalog entry removes the installed copy.
Do not disable shared apps or remove an entire marketplace to rename this one plugin.
A workspace-managed plugin identity must be reconciled by its workspace controls; a
local name change cannot transfer its ID or policies.

Install/update the replacement using the supported local route. Start a fresh session.
Record the client version, source identity, resolved plugin path, actual entry-skill
read, and any active overrides. Confirm there is one effective method, not duplicate
skills from old and new copies.

## Qualify behavior

Follow docs/guide/how-to/qualify.md on a synthetic or already-authorized local task.
Record actual role loading, delegation if available, stopping behavior, pause/resume,
and separate acceptance. Include the final integrated candidate, not just a pre-rebase
diff. No agent dispatch means that condition remains unrun, not passed.

Return Done / Exceptions / Next with the source version, cutover result, test evidence,
native trial results, rollback location, and one next action. Store runtime evidence
with the task, not inside the distributed plugin. Restore the previous effective
installation if the replacement cannot load; do not discard completed work.
