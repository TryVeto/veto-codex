# Verification — 2026.9.1202

Author-run local checks, 12 September 2026. No native host installation, role/model
dispatch, independent agent review, paid-model experiment or product deployment.

## Executed checks

| Check | Result | Evidence and limit |
| --- | --- | --- |
| Untouched 1201 baseline suite | 245 passed | Rerun before source changes; not new agent qualification |
| Candidate plugin suite | 270 passed, no failures or skips | [Unit log](unit-tests.txt); includes 25 new role-context test methods |
| Repository-tool suite | 24 passed, no failures or skips | Same log; deterministic packaging, rejection cases, source/file handling |
| Original reviewer probes | 9 passed | [Replay results](replay-results.txt); offline helper calls |
| Synthetic baseline/candidate | Four false, then four true, using unchanged oracle | Same replay log; expected baseline exit 1, repaired exit 0 |
| Documented role/handoff commands | Passed | [CLI receipts](cli-smoke.json); context and integrity only |
| Original tests and nine role guides | Preserved byte-for-byte | Checked against prior inventory; no assertion weakened |
| Manifests, local path links and source inventory | Passed | Reproduce with `python3 -B tools/repo.py check` |
| CI workflow YAML | Parsed; read-only contents permission and no pull_request_target | [Syntax receipt](workflow-syntax.json); GitHub Actions execution is unrun |

The total is **294 unit-test methods**, not 294 independent agent trials. The nine
reviewer probes and synthetic checks are separate observations, not additional unique
unit tests or proof of general safety. The original behavioral catalog remains 114
written scenarios, not completed native evaluations.

The unit log includes a harmless inherited terminal-display warning from an original
test; both suites exited successfully. No skipped or failing test was hidden.

## What the tests cover

The new role reader is tested for every maintained role, deterministic context, byte
identity, manifest pins, changed sources, empty/oversized profiles, duplicate fields,
invalid role IDs, role/path mismatch, attempted extra authority fields, symlink/path
refusal, and no file mutation. Its outputs explicitly deny that preparing instructions
performed any runtime, permission, ownership or independent-review act. These are
helper guarantees, not claims about what an arbitrary model will do with the text.

Repository tests cover normalized ZIP metadata, identical archive bytes for identical
source, preservation of dot-directories and file bytes, no overwrite, escaping links,
ignored generated output, manifest identity and tests/validation failing closed before
packaging. Checks also screen a limited set of file types and credential patterns; this
is not a complete secret audit or trusted-origin verification.

The source archive is produced only after repeating structural checks and tests. The
final archive's checksum and fresh-extraction report are delivered alongside it, not
embedded as a self-referential claim inside the same ZIP. The per-file source manifests
identify its contents.

## Open qualification

Follow [the native trial](../docs/guide/how-to/qualify.md) to establish actual installation,
source loading, effective worker model/effort, a stopped old writer, fresh continuation
and separate acceptance. Record the original task and current authority. The example
JSON deliberately remains unrun.

The new code was authored and checked in this build session. No separate agent was
used as an independent reviewer. No claim is made that Luna Max is supported by the
user's selected host, cheaper after rework, or appropriate for every task. The role
name Lunentic remains undefined pending its actual accepted charter.
