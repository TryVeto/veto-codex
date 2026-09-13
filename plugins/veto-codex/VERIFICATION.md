# Verification boundary — 2026.9.1203

This is the renamed Veto Codex source. The complete source-repository release includes
fresh local results under its root `verification/` directory. Historical records under
this plugin’s `verification/` and `research/` remain unchanged and are not new results.

Run `python3 -B scripts/doctor.py` and `python3 -B -m unittest discover -s tests -v`
from this folder. The inherited synthetic oracle and nine reviewer regressions remain
available. These checks exercise files and helpers. They do not prove native discovery,
agent dispatch, effective model routing, independent acceptance, or product deployment.

The current native qualification remains unrun. Use [ADOPTION.md](ADOPTION.md) to record
actual host behavior in the working repository, outside this distributed plugin.
