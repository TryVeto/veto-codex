# Local installation

This source is Veto Codex 2026.9.1203, renamed from Veto Stack 2026.9.1202.
Use the source repository’s ADOPT.md and migration/README.md when available.
This standalone plugin folder does not install itself.

Preserve the actual previous source and settings. Disable the old `veto-stack` entry
before enabling `veto-codex`, keep the existing marketplace and unrelated plugins, and
use the supported host installation path. Do not overwrite generated caches or presume
that a name change transfers a hosted plugin ID. Qualify loading in a fresh session.

Run `python3 -B scripts/doctor.py` and `python3 -B -m unittest discover -s tests -v`
from this plugin root. These are offline package checks, not native loading evidence.
The twelve non-entry skill names and nine role profiles remain. No alias skill or
second plugin should be registered. See [adoption checks](ADOPTION.md) and the
[rename note](MIGRATION.md).
