# Veto Codex

**Give the outcome. The agent carries the method.**

Version **2026.9.1203** · 12 September 2026 · Renamed repository edition, continuing **2026.9.1202**.
New `veto-codex` identifier, **13 public skills** and nine retained role guides. No second controller,
new service, automatic hook, remote dependency or product deployment.

[Operating agreement](GUIDE.md) · [Install and qualify](ADOPTION.md) ·
[Verification](VERIFICATION.md) · [Changes](CHANGELOG.md)

## What this release does

The existing [veto-codex skill](skills/veto-codex/SKILL.md) is the entry point.
It selects the relevant procedure and keeps execution moving to the accepted result.
Five contextual playbooks connect start/resume, investigation/build, manager return,
finish/handoff and improvement of the method. Agents load them when needed, not as
another giant prompt. Existing product, design, craft, review and integration skills
remain in place.

The method follows selected pstack patterns while retaining Veto's company/product
principles and current release permissions. Sebastian is the only human; agents own
context recovery, routine coordination, verification and durable handoffs. Useful
manager conversations remain. [Source and adaptation decisions](research/AGENT-NATIVE-METHOD.md).

The [verification route](references/application-verification.md) reuses the actual
product repository's `verify-veto` and Feature Map. The new
[handoff checker](references/handoff-record.md) detects changed files, wrong tasks,
stale assignment revisions and completion rows without evidence references in a declared packet.
It does not authorize execution or replace native state.

Goal helpers now treat language classification as a hint, never authorization.
Quoted/negated review requests remain non-mutating. Verification requires a nonempty
objective, same-task identity and a consistent active state. The existing reminder
adapter is conditional; no automatic hook is registered by this package.

## Use it

In a host that has loaded the plugin, give the accepted outcome or say "continue"
with the existing context. Explicitly select the Veto Codex skill when needed; no
command catalog is required. A file-based agent can read the entry skill and its
relative references from the whole plugin folder.

Install into the **existing Veto Codex source and marketplace** using [ADOPTION.md](ADOPTION.md).
The enclosing repository includes a complete marketplace wrapper. Reconcile the
existing authoring source before adoption; do not register a duplicate marketplace
or overwrite custom work. The repository adoption guide owns the upgrade process.

## Local checks

Python 3.10+; no third-party runtime dependencies. From this plugin folder:

```sh
python3 -B scripts/doctor.py .
python3 -B -m unittest discover -s tests -v
python3 -B scripts/check_handoff.py --help
python3 -B scripts/check_receipt.py --help
```

The doctor checks declared structure and file hashes, not native loading. The
handoff checker reads only declared local files and never writes, starts a process,
calls a host API or makes a network request. Existing review packaging writes only
a new explicitly requested ZIP. No helper installs or upgrades itself.

Native installation, automatic skill selection and independent agent performance
remain separate qualification gates. See the actual executed checks and limits in
[VERIFICATION.md](VERIFICATION.md). Historical `verification/` receipts retain their
dated scope; 1201 records remain historical. Repository-edition status is recorded in
[verification/1202](verification/1202/README.md).

## Portable roles

Use the [role context helper](references/portable-roles.md) to load an existing
responsibility into a different qualified agent. It prepares checked context only;
it does not implement an identity server or change runtime permissions.

## Scope of this name

This is the Codex operating method, renamed from Veto Stack. It does not replace Veto’s
separate ChatGPT web setup. The entry skill is `veto-codex`. Existing installations need
the [rename procedure](MIGRATION.md), not a second active plugin. Historical research
and verification records retain their original names and do not prove this release loaded.
