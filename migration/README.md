# Veto Stack → Veto Codex

This is a continuation of one maintained method, not another plugin to run beside it.

| Item | Before | After |
|---|---|---|
| Repository folder | `veto-stack/` | `veto-codex/` |
| Plugin source | `plugins/veto-stack/` | `plugins/veto-codex/` |
| Plugin identifier | `veto-stack` | `veto-codex` |
| Display name | Veto Stack | Veto Codex |
| Entry skill | `veto-stack` | `veto-codex` |
| Release | `2026.9.1202` | `2026.9.1203` |
| Bundled marketplace name | `veto-team` | `veto-team` |

The twelve other skill names and all nine role profiles are retained. Historical
records keep their original names. The rename does not change payment, customer,
release, model, or account permissions.

## Source history and installed identity are different

OpenAI documents the plugin name as its identifier and component namespace. Renaming
it is therefore a host cutover, not merely changing the README title. The repo source
continues; preservation of a hosted plugin ID is **not** claimed. See the official
[packaging reference](https://developers.openai.com/plugins/build/plugins).

`baseline-2026.9.1202.json` contains the complete prior repository’s file hashes.
The accompanying `veto-stack-to-veto-codex-2026.9.1203.patch` was generated from that
baseline. It is distributed beside this ZIP to avoid a self-referential patch in its
own payload. Paths in the patch are relative to the repository root.

For an existing checkout, start clean or preserve unrelated changes in a separate
worktree. Inspect the patch, then use `git apply --check` before `git apply --index`.
Do not force a failed application. Reconcile custom edits using the actual old source.
Run source checks and tests after reconciliation; commit on a review branch under the
existing repository history. The outer checkout directory can be renamed separately.

For a new repository, publish the extracted contents, including `.agents/` and `.github/`.
Do not claim that the initial commit recreates previous source history.

## Read-only catalog planner

From the new repository, using a nonsecret copy of the actual local marketplace:

```sh
python3 -B tools/migrate_catalog.py \
  --catalog /absolute/path/to/marketplace.json \
  --source-path ./plugins/veto-codex
```

The proposal changes only the matching name and local source path. The path is relative
to the existing marketplace root; this command does not copy files or find that root.
It preserves the marketplace name, other plugins, entry order, and installation policy.
It refuses duplicate identities, unknown sources, traversal, and a hosted `pluginId`.
It has no apply mode and does not edit configuration or claim a native installation.

The executable fixture is under `examples/migration/`. Run it, inspect the JSON, and
compare the output with the supplied expected catalog.

## Cutover

1. Capture the actual old source, marketplace entry, active settings, and tasks. Keep
   the rollback outside active plugin discovery. Do not archive a second plugin entry.
2. Reconcile and check this source. Resolve its local path from the real marketplace root.
3. Disable the old plugin through the applicable host control. Confirm it is inactive.
   Then apply the reviewed catalog change and install/enable the renamed replacement.
4. Start a fresh session. Inspect actual skill loading and confirm only the new method
   is effective. Run the native qualification in the guide.
5. Retain the previous source and settings until qualification succeeds. Do not delete
   the whole marketplace, disconnect shared apps, or replace a whole configuration file.

For local project settings, OpenAI documents the key as `plugin@marketplace`. The inert
example in `examples/migration/disable-old-plugin.toml` illustrates disabling the old
local entry. It is not an active configuration and is not a workspace policy change.
Workspace-managed imports require the administrator’s supported migration route.

## Rollback

Disable the replacement first. Restore the preceding reviewed source and the recorded
catalog/settings using the same host controls. Start a fresh session and confirm the
old version actually loads. Preserve all task state and evidence in the work repository.
Neither rollback nor a successful cutover authorizes a deployment.
