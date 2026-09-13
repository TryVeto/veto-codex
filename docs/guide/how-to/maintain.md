# Improve and release the method

Start from a failure you actually observed: the agent did not read the relevant source,
selected the wrong task, lost an accepted decision, or produced a result nobody could
verify. Preserve a minimal reproduction before changing the instructions.

Choose the repair that makes the failure harder to repeat. An architectural constraint
or deterministic test is preferable for an invariant. A maintained control tool is
preferable when agents repeatedly improvise the same unreliable interaction. A focused
skill helps when the missing work is judgment or a repeatable investigative method.
Another paragraph in AGENTS.md is not the default answer.

## Change one coherent unit

Update the procedure, relevant implementation/check and affected guide page together.
Keep role responsibilities separate from host/model settings. Retain original feedback
and sources. Changes to authority or a role's substantive remit need their actual review;
a cleaner explanation does not adopt them.

Run the tests at the right layer. A unit test establishes helper behavior. A synthetic
exercise establishes that exercise. A native-agent trial establishes observed agent
behavior under its actual configuration. Product acceptance and field proof have their
own evidence. Do not average these into one green score.

## Build a source release

From the repo root:

```sh
python3 -B tools/repo.py hashes --write
python3 -B tools/repo.py check
python3 -B tools/repo.py test
python3 -B tools/repo.py package --output dist
```

Review changes before refreshing hashes. That command records current bytes; it does
not decide whether they are good. Update the repository and plugin version fields and
current release note for a new version. Keep dated historical receipts unchanged.

The package command reruns checks and tests, then writes a deterministic source ZIP and
its SHA-256 sidecar under the requested output directory. It refuses to overwrite an
existing release. Build again in another directory from identical source to compare
archive bytes. No credentials, .git directory, caches or runtime artifacts belong in it.

CI checks pull requests and pushes. The separate packaging workflow can run on a reviewed
version tag or manual dispatch and uploads an artifact; it does not publish a public
package or deploy the product. Keep repository protection and actual review requirements
outside this ZIP under their existing owner.

## Qualify the change without inventing a new team

Use the existing verifier to inspect the changed mechanism and run the appropriate
native cases when available. Preserve unrun status when it is not. A role guide, installer,
and test suite can be ready for adoption without already being used successfully in a
real host.

After acceptance, distribute the reviewed source version through the existing marketplace.
Retain its predecessor for rollback. Current task records stay in their working repo,
so an upgrade does not erase unfinished work or create a new mandate.
