# Changes

## 2026.9.1203 — Veto Codex

Continues the supplied 2026.9.1202 repository. Renames the repository, plugin, display
name, source path, and entry skill. The other twelve public skills and nine role profiles
are retained. Veto’s separate ChatGPT web setup is unchanged.

Adds an offline catalog-migration planner with no apply mode, duplicate-identity checks,
a complete prior-source inventory, migration/rollback instructions, and rename regressions.
The planner preserves other plugins and installation policies; it rejects workspace IDs
rather than claiming it can transfer them.

The guide and agent-facing verification procedure now explicitly require decisive
runtime replay on the final integrated candidate. An unchanged patch-id cannot carry a
runtime verdict across a changed base. No native product replay is claimed in this release.

Prior verification records retain their original names and dates. Current results are
in `verification/README.md`. Native installation and agent dispatch remain unrun.

---

# Changelog

## 2026.9.1202 — 12 September 2026

Repository-ready source distribution of the existing Veto Stack plugin. Adds a root
README, maintained guide, local adoption assignment, repository validation, reproducible
packaging and GitHub checks/artifact workflows. Adds a read-only role context reader and
index over the nine existing charters; the 13 public skills are retained.

Explains the one-primary-coordinator proposal, qualified worker model choice and portable
roles without conflating persona, model, session, task ownership or authority. Includes
an inert bounded-reader configuration example and an unrun native qualification record.
No live settings, permissions, goals, agents, integrations or product releases changed.

The baseline's goal-classifier repairs, checked handoff machinery, tests, cases and
source snapshots are preserved. Historical results retain their dates. This edition's
verification is reported separately in verification/README.md.
