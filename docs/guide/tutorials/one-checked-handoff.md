# Tutorial: one checked handoff

This is a small, executable introduction to the method. It uses synthetic saved notes,
not live escrow data. It was authored as a deterministic example, not performed by
independent native agents. You will see the difference between a failing behavior,
repaired behavior and a packet that merely preserves evidence correctly.

## Start with the requested result

The example concerns an office reopening a contribution saved under its own file.
Another file's contribution must not appear, and a fresh process must recover the
acknowledged value. The original failing fixture and repaired candidate are both shipped;
you do not need to alter either to follow the tutorial.

From the repository root, run the controlled checks:

```sh
python3 -B plugins/veto-codex/evals/oracles/focus_oracle.py \
  plugins/veto-codex/evals/fixtures/focus
```

Expect a nonzero exit and four false assertions. This is the deliberately broken
baseline, not a packaging failure. Preserve it rather than updating the expected result
to accept the bug.

Now run the identical oracle against the repaired example:

```sh
python3 -B plugins/veto-codex/evals/oracles/focus_oracle.py \
  plugins/veto-codex/examples/resume-work
```

Expect four true assertions: exact retrieval, separate file, separate office and a fresh
module reading the saved work. The test executes candidate Python and creates temporary
synthetic data. Only run untrusted candidates in a properly isolated environment.

## Check the handoff, not just the behavior

```sh
python3 -B plugins/veto-codex/scripts/check_handoff.py \
  --record plugins/veto-codex/examples/resume-work/handoff.json \
  --root plugins/veto-codex/examples/resume-work \
  --task-id synthetic-focus-repair --revision 1 \
  --sha256 5cb61526e9a9def7d123a2ec0981191c5bd1e27366cd91c55b6c137f807b5242
```

Expect `HANDOFF_INTEGRITY_PASSED`. Inspect the limitations in that JSON. The checker
establishes that the named task, revision and referenced bytes match the supplied
packet. It does not know the current native goal, grant permission or establish that a
new agent can continue correctly. Do not substitute it for the actual state readback.

## Prepare another role

```sh
python3 -B plugins/veto-codex/scripts/role_context.py --role independent-verifier
```

The returned sources contain the existing reviewer instructions and shared working
contract. Notice that `independent_review_established` is false. Merely printing or
reading the role does not create another reviewer. It gives a qualified, separately
commissioned run the right starting context.

## What you have learned

The same oracle rejects the broken fixture and accepts the repaired example. A checked
handoff identifies the work and bytes it describes. A role packet makes a maintained
responsibility available to another run. These are useful pieces of the loop, but none
means a real seller workflow has been deployed or that native agents behaved correctly.

The next step is [one authorized native-agent trial](../how-to/qualify.md): preserve the
original task, interrupt after a meaningful intermediate result, resume in a fresh run,
and obtain separate replay on the exact candidate. Your local agent performs the
procedure. Sebastian should only supply a reserved decision when one is actually needed.
