# Source lineage

The immediate baseline is `veto-stack-repo-2026.9.1202.zip`, supplied in this conversation.
Its exact checksum and complete repository inventory are in
[the migration baseline](../migration/baseline-2026.9.1202.json).
`REPOSITORY.json` records the same archive identity.

The earlier `baseline-files.json` and `../provenance-1201.json` remain unmodified
historical records. The former covers the 2026.9.1201 plugin. The latter’s paths refer to
that old bundle. `releases/2026.9.1202/` retains the previous repository verification
records exactly; links within those snapshots refer to their original layout.

The nine role guide bodies remain unchanged. Retained helper tests have only the
necessary package-name substitutions; assertions are not weakened. Current hashes
identify the new sources. They are not signatures, authorization, or native loading proof.

Historical plugin research, source snapshots, and verification records retain their
original bytes, except `research/next-inputs.json` advances its current `release` pointer
without changing the referenced source inputs. Old filenames are intentional there.

No `.git` history was supplied in the source ZIP. No prior commits have been invented.
Use the migration patch in the actual existing repository to preserve its history.
The source ZIP, patch, and local verification record are separate release artifacts.
