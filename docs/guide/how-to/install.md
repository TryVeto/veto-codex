# Install Veto Codex

The source archive is ready to publish. Nothing in it has already been installed in
your Codex environment.

## Existing Veto Stack installation

Read [the migration](../../../migration/README.md) first. Reconcile the source, preserve
custom work and rollback, and disable the old effective plugin before enabling the new
identity. A renamed directory is not evidence that an installed cache changed.

Do not copy both versions into discovery paths. Do not overwrite a marketplace containing
other plugins or Veto’s separate ChatGPT web setup.

## New private source

Publish the **contents of `veto-codex/`** as the root of the intended private repository.
Include `.agents/` and `.github/`. Do not upload only the ZIP as the repository content.
No remote URL is assumed or created by this package.

From the checkout:

```sh
python3 -B tools/repo.py check
python3 -B tools/repo.py test
```

The included marketplace points at `./plugins/veto-codex` and retains the catalog name
`veto-team`. Confirm that this is not already registered from another source. Current
OpenAI documentation describes these authoring commands:

```sh
codex plugin marketplace list
codex plugin marketplace add .
```

Use the supported plugin browser for your client to install **Veto Codex**, then start a
fresh session. A Git-backed source can be pinned to a reviewed ref. Resolve your actual
private repository identity rather than pasting a made-up repository URL.
See [current host documentation](../reference/sources.md#current-host-documentation).
Availability and installed-cache refresh behavior must be checked on the actual client.

## Establish what loaded

Record client version, source commit or inventory digest, plugin version, resolved
installed path, and applicable overrides. Have the fresh agent read the current
`skills/veto-codex/SKILL.md` and perform a harmless bounded exercise. Inspect actual
file reads or host-visible loading evidence. A directory on disk or the sentence
“I am using Veto Codex” does not prove effective loading.

Run [native qualification](qualify.md). File-based use—explicitly asking an agent to read
the entry file—can be useful, but is not proof of plugin discovery. Missing host access
remains a recorded prerequisite, not a fabricated success.

The manifests retain the portable entry point and Codex compatibility metadata.
The inherited Claude-compatible metadata is retained for source continuity only;
this release does not install or qualify a separate Claude or ChatGPT web workflow.
No MCP server, automatic hook, credential, or scheduler is bundled.

[ADOPT.md](../../../ADOPT.md) is the local agent’s complete assignment. The
[migration guide](../../../migration/README.md) includes rollback.
