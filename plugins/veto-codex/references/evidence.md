# Acceptance coverage and evidence receipts

Use existing work records and protected project checks. This optional helper checks a machine-readable export; it does not require a second tracking system. **First ask whether acceptance covers the original request. Then ask whether observed behavior satisfies acceptance.**

## What is pinned, and by whom

An authorized acceptance owner holds the contract digest outside the builder's write scope. The contract identifies the exact candidate/environment, stable requirements, full expected behavior, evidence layer and permitted provenance. The builder's receipt cannot drop cases or waive required cases. A mutable branch name alone is not a candidate identity. Include material dirty changes, build and configuration identity as needed.

For feedback batches, use **contract schema 2**. It also pins the complete captured feedback batch and the assigned builder/reviewer identities. A separately performed source audit compares the originals with that inventory and the inventory with the contract. The same incomplete builder summary cannot supply both sides. Use the [coverage procedure](feedback-coverage.md) before collecting the final receipt.

This is not a security boundary. Digests establish byte identity, not truth or authority. Declared different reviewer names do not prove independence. A reviewer must actually inspect the originals, context, mappings and candidate. The helper cannot discover an omitted source outside the supplied inventory, detect every narrowed interpretation, authenticate a reviewer, assess a disposition's authority, or prove any test ran. Keep the accepted sources/contract and actual reviewer process outside the builder's ability to silently rewrite them.

## Contract and receipt

Both contract versions contain `schema_version`, `contract_id`, `candidate` (`id`, `environment`) and a nonempty `requirements` list. Each requirement contains `id`, `expected`, `layer`, `allowed_provenance` and boolean `required`. At least one case is required. Schema 2 adds `feedback` with the captured batch's `sha256` and distinct, nonempty `builder` and `reviewer` identifiers. Changing feedback or the contract invalidates the prior audit; obtain the accepted revision, not a self-authorized new digest.

A receipt matches the contract's schema version, ID, digest and candidate. Its `results` contains every contract ID exactly once. Each row includes `id`, `status`, `layer`, `actual` and `evidence` (relative local `path` and `sha256`). Passing rows also require `provenance`, `procedure` and `mode`: `fresh` or `carried`. Carried evidence includes `carry_reason`, explaining why its dependencies and environment still apply. Nonpassing/N/A rows include `reason`.

Statuses: `passed`, `failed`, `not_run`, `blocked`, `not_applicable`. A required case cannot become N/A inside the receipt. Even an optional observed failure stays visible. Unrun or blocked checks never become passes.

| Layer | Permitted provenance vocabulary |
|---|---|
| rules | static, unit, simulation |
| persistence | service, integration-sandbox, simulation |
| journey | browser |
| preparation | model-evaluation, qualified-evaluation |
| operations | external-observation, staffed-rehearsal |
| field | user-observation |

Pin the relevant subset in the contract. A browser running a mock is still mock-bound in the result; it does not establish an external provider or destination. The checker validates declared provenance, not the reality behind the declaration.

## Feedback capture and independent coverage

[The complete unrun example](../templates/feedback-example/README.md) demonstrates the format. All its people, evidence and cases are synthetic.

The feedback batch uses `schema_version: 1`, `batch_id`, `sources` and `items`. Each source has `id`, `kind` (`text`, `image`, `pdf`, `reported_summary`) and an `artifact` path/digest. Each item has stable `id`, `source_id`, exact `original` wording, `context`, `interpretation`, `kind` (`requirement`, `question`, `observation`, `suggestion`, `decision`) and `owner`. Preserve compound clauses, screenshot context, repeated occurrences and original decision provenance. For text sources, the helper checks that the quoted original appears in the pinned text. Images/PDFs require actual inspection. A report without originals remains a coverage gap.

The coverage review uses `schema_version: 1`, matching `batch_id`, `feedback_sha256`, `contract_sha256`, assigned `reviewer`, an `audit_evidence` artifact, `source_reviews` and `items`. Every source has a review row (`id`, `status`: `complete`/`gap`/`unavailable`, and `finding`). This forces the declaration to address the entire source, not merely selected extracted items. A gap or unavailable source keeps acceptance open.

Every feedback ID has one mapping row with `id`, `status`, `requirement_ids` and `reason`. `covered` maps to required acceptance cases. `answered` is only for a question, has no acceptance mappings, and requires an `answer` artifact; an explanation cannot replace behavior. `superseded`/`not_applicable` have no mappings and require a `decision` with `source_id` and exact `quote` in a pinned text source. The reviewer must judge whether that decision actually authorizes the disposition. Nontext decisions need a reviewed text transcript. `deferred`/`unresolved` remain open. A new accepted scope may narrow a batch, but cannot quietly erase outstanding obligations from the broader goal.

## Run

From the plugin folder, using real paths and the independently held contract digest:

```sh
python3 -B scripts/check_receipt.py --require-feedback \
  --contract /path/to/accepted-contract.json \
  --contract-sha256 THE_INDEPENDENTLY_RECORDED_64_HEX_DIGEST \
  --feedback /path/to/captured-feedback.json \
  --coverage-review /path/to/independent-coverage.json \
  --receipt /path/to/receipt.json \
  --artifact-root /path/to/permitted-evidence
```

Schema 2 refuses omission of either feedback input. Exit `0` means **DECLARED_COVERAGE_AND_EVIDENCE_CONSISTENT**. Exit `1` means structurally valid but not accepted; exit `2` means invalid, missing, stale or unsafe input. None authorizes release or certifies the product.

Schema 1 remains compatible with existing [contract](../templates/acceptance.contract.json) and [receipt](../templates/acceptance.receipt.json) examples. Omit `--require-feedback` and the two feedback arguments for that evidence-only format. It returns **DECLARED_EVIDENCE_CONSISTENT** with feedback coverage **NOT_CHECKED**, never full feedback-batch acceptance. These old examples also remain deliberately unrun.

The helper performs no network calls, subprocesses or application tests. Evidence files must be ordinary, nonempty, inside the artifact root, without symlinks/traversal, and below 64 MiB; JSON inputs have a 2 MiB limit. Duplicate JSON keys are rejected. Use stable permissioned copies: this is not protection from concurrent hostile filesystem mutation. Minimize/redact sensitive material; do not place credentials or raw session data in shared evidence.

## Require coverage at the calling boundary

For an original-feedback batch, call with `--require-feedback`. A valid schema-1 evidence-only contract is then rejected with `INVALID` and exit 2, even if every declared result passes. A schema-2 contract still requires `--feedback` and `--coverage-review`; omissions or inconsistent pins remain errors. `NOT_ACCEPTED` with exit 1 means valid inputs still declare open gates. Exit 0 describes consistent declarations, never verified product behavior.

The flag is optional for backward compatibility. The accepted workflow or existing gate must require it where appropriate; dropping the flag, replacing both the contract and its trusted digest, or falsifying a review cannot be prevented by this helper. No automatic hook or host integration is installed. Follow [the adoption check](../ADOPTION.md) once when enabling or diagnosing the route.
