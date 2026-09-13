# Local verification — Veto Codex 2026.9.1203

Built from the supplied `veto-stack-repo-2026.9.1202.zip`. The baseline’s source check
passed and all 294 existing tests passed before editing. Its exact archive checksum
is recorded in `../migration/baseline-2026.9.1202.json`.

## Executed here

- **324 unit tests passed:** 270 plugin-helper tests and 54 repository/migration tests.
  The 30 additional tests cover the rename, read-only catalog proposal, conflicting
  identities, unchanged policies, unsupported hosted IDs, malformed inputs, and scope.
- **Nine original reviewer probes passed.** The same probe script remains under the
  plugin’s historical 1201 verification folder; the current test command executes it.
- **Same synthetic oracle, two outcomes.** The original deficient fixture fails all four
  observations; the repaired example passes all four. This is an author-run exercise,
  not evidence of a fresh autonomous agent or a live office workflow.
- **No prior source file discarded.** The source-diff record maps all 282 prior files to
  their current locations. The nine role guides are byte-identical. The retained tests
  have only package-name literals changed; assertions are not relaxed.
- The catalog example produces its exact expected output without writing its input.

See [test output](local-tests.txt), [source mapping](source-diff.json),
[baseline check](baseline-check.json), and [catalog example](migration-example.json).

The release packager reruns source checks, local tests, the synthetic oracle, and the
original probes before producing the ZIP. The separate release verification JSON
records fresh extraction, patch application, checksum, and deterministic repack results
for the delivered archive, avoiding a self-referential archive hash in this source.

## Not established

Native plugin installation or effective source loading; active worker dispatch and
model routing; independent agent acceptance; a live Veto product journey; GitHub Actions
execution; remote repository publication; or any deployment. These remain unrun or not
performed. The integrated-candidate replay rule is packaged guidance, not a newly
observed native replay.

Checksums establish local byte identity, not authorship, security, authorization, or
agent performance. Credential-pattern checks are limited, not a security audit. Tests
run supplied code locally; they do not call an AI provider or change host configuration.

Previous release records remain under `../provenance/releases/2026.9.1202/` and the
plugin’s historical research/verification folders. They have not been relabeled as
current observations.
