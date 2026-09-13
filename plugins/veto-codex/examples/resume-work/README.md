# Checked handoff example

Synthetic, author-run rehearsal. This is not a native agent run, independent review,
a customer result, or Veto application code. The original evaluation fixture and
its oracle are unchanged. The copied fixture failed all four oracle assertions
before the retrieval repair and passed those same four afterward.

The logs retain the exact source and oracle hashes. The source in this directory
is the repaired candidate; the original failing source remains in
`evals/fixtures/focus/store.py`.

From the plugin root, validate the shipped example using the delivery digest:

```sh
python3 -B scripts/check_handoff.py \
  --record examples/resume-work/handoff.json \
  --root examples/resume-work \
  --task-id synthetic-focus-repair --revision 1 \
  --sha256 5cb61526e9a9def7d123a2ec0981191c5bd1e27366cd91c55b6c137f807b5242
```

Expected: `HANDOFF_INTEGRITY_PASSED`, with permission and native-state verification
false. The same digest appears in the outer bundle's delivery record.

The checker only establishes that declared bytes match. To observe the code's
behavior again in a disposable local environment:

```sh
python3 -B evals/oracles/focus_oracle.py examples/resume-work
```

That runs candidate Python code and creates temporary synthetic data, unlike the
read-only handoff checker. Do not run an untrusted candidate outside isolation.
Preserve any host pause; neither command starts a native agent or accepts work.
