# Feedback coverage: unrun format example

This is synthetic teaching material, not Sebastian's original annotation, an actual independent review or a product result. It starts **NOT_ACCEPTED**. Use existing work records; these files demonstrate the optional parser format rather than a requirement to maintain duplicate records.

From the plugin folder:

```sh
python3 -B scripts/check_receipt.py --require-feedback \
  --contract templates/feedback-example/contract.json \
  --contract-sha256 2ea366c423f7b6c751ac13fe6c7391527b87d1e7f9c0ddccef65ff0e4c4bdbc6 \
  --feedback templates/feedback-example/feedback.json \
  --coverage-review templates/feedback-example/coverage-review.json \
  --receipt templates/feedback-example/receipt.json \
  --artifact-root templates/feedback-example
```

Expected: exit **1**, verdict **NOT_ACCEPTED**, source-audit gap, unresolved feedback and unrun browser case. The supplied digest only pins this teaching fixture; it is not an independently authorized acceptance contract.

To use the format on real work, replace the source with the actual complete, permissioned batch, retain original wording/context, and obtain the adopted contract and actual independent audit. Exercise the candidate and record real observations. Do not convert placeholders to passes or reinterpret a compound requirement as a source attribute. For images/PDFs inspect the originals. The helper validates declarations and file identity, not semantic completeness, actual reviewer independence or application execution. See [format and limits](../../references/evidence.md).
