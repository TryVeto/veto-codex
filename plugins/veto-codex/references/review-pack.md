# Share an inspectable candidate, not a folder of opinions

Recommended arrangement: **canonical app source at one revision + a compact versioned review pack**. Use `sandbox/reviews/<candidate-id>/` for the pack if that fits the repository. Do not copy the whole application into a second maintained `sandbox` tree just to request feedback. A genuinely separate experimental app may have its own sandbox directory, with a declared owner and relationship to the product.

## One entry point

A reviewer should open one README and know what decision is wanted, who is using the product, what task to attempt, what is fixed, and which candidate is under review. Start with the material needed to judge, not all prior reports or the founder's preferred answer.

Suggested layout, adapted to existing conventions:

```text
sandbox/reviews/<candidate-id>/
  README.md                  task, constraints, source/build identity, run route
  request.json               pinned review scope and required state IDs
  manifest.json              captured states, files, hashes, gaps, sanitization
  scenarios.md               starting conditions, task, expected endpoint
  screenshots/               full-resolution PNG/JPEG/WebP states
  evidence/                  actual relevant results and final output
  source/                    optional sanitized snapshot, or exact repo reference
  feedback/                  annotations and builder rationale, read after first pass
```

Keep the neutral and feedback paths distinct. Required constraints remain in the neutral brief. A missing optional file is a gap, not permission to invent it. Pack metadata lives alongside existing acceptance records; it does not replace the release contract.

## Capture journeys and states

“All screens” is an inventory, not necessarily a useful review. Select the states needed for the current task: ordinary entry, form input and validation, correction/Help, saved receipt, next-role retrieval; plus material narrow/keyboard/recovery states. Preserve a route/state inventory with unvisited areas. For a whole-product review, cover all supported journeys and their important states—not every arbitrary combination of fixture values.

Capture actual readable viewport images, not just extremely tall pages or tiny contact sheets. Full-resolution images preserve copy and hierarchy; a contact sheet or HTML index provides orientation. Use ordered frames for meaningful transitions. Do not assume a model can play the video, execute a ZIP, or fetch every repository image. Keep raw neutral captures separate from annotated copies. An image of a chat discussing a screen is not that screen's implementation.

For every capture retain candidate, scenario/fixture version, actor, state, route and viewport. Screenshot filenames are navigation; they do not prove the candidate. Record the served-build identity and limitations separately. Changes after capture make the affected images stale until recaptured or explicitly justified as unchanged.

## Source and execution

Prefer an exact commit over a moving branch. If changes are uncommitted, include a content-addressed sanitized snapshot covering relevant dirty/untracked files and say so. `git archive` alone captures committed files; it does not capture the active dirty workspace. Never stage, commit, push or discard unrelated user work to make a clean package.

A repository reference is useful only where the reviewer has access. Supply a curated ZIP/source snapshot when source retrieval is unavailable; preserve dependency versions, runtime instructions and known substitutions. A snapshot is for review, not a new canonical codebase. Exclude dependencies, build caches, credentials and live data. Inspect unfamiliar run scripts before any execution.

The best interactive target is the same authorized running candidate. A private staging URL is an option only if hosting and access are already permitted. Do not create public hosting, a tunnel, a new account or weaker authentication to share it. `127.0.0.1` from the builder's computer is not the reviewer environment's app.

## A review request can require evidence without claiming a pass

Use [the request template](../templates/review-request.json) and [manifest template](../templates/review-manifest.json) as a schema example. Pin the request's SHA-256 in the accepted work record before collecting results. Have an independent owner retain it where available. The builder must not silently change required state IDs to hide missing captures.

`review_pack.py check` compares the pinned request, candidate/environment, declared files and state coverage. `build` also makes a portable ZIP with a safe static index. Both explicitly distinguish COMPLETE from PARTIAL. **Complete means the requested review materials are present; it does not mean the product is good, safe, tested or accepted.**

Each screenshot has to be a real PNG/JPEG/WebP file with a matching declared hash. The helper checks basic format signatures, not pixel content, true candidate correspondence or rendered quality. It cannot inspect secrets inside images or nested archives. Sanitization is a recorded human/agent review, not a security certificate. Source hashes establish identity, not authenticity or correctness.

The helper never executes the application, calls Pro, starts a browser, uploads, modifies a repository, or creates a scheduled job. It reads only explicitly listed ordinary files and writes a new requested ZIP without overwriting existing output. Missing required materials produce a partial pack; unknown statuses or duplicate state IDs, unsafe paths and hash mismatches are invalid rather than silently ignored.

## Include observation context without changing the schema

For stateful reviews, put the [observation record](../templates/review-observations.md) in the pack's evidence directory. Populate only relevant fields from actual inspection: execution context, starting fixture/session, actions/results and identity recheck. In the existing manifest, list the file with `kind: evidence`, its real SHA-256 and candidate ID, and reference its path in the affected states' `evidence` arrays. Keep annotations in their existing feedback lane. Do not add unsupported top-level JSON fields or a second manifest.

The helper checks this file's declared bytes and references, not the truth or completeness of its contents. A state marked captured can show a failed product action; record the behavior result separately. A copied single-file specimen may change origin, headers, relative assets and persistence. It does not inherit the original application's service evidence.

## Run the optional helper

Populate the templates from actual materials first. These example paths are placeholders, not files the plugin claims exist. Set the request digest from the accepted work record; do not quietly regenerate it after removing a required state. From the plugin directory:

```sh
: "${REVIEW_REQUEST_SHA256:?Set the digest from the accepted review record}"
python3 -B scripts/review_pack.py check \
  --root /absolute/path/to/review-materials \
  --request /absolute/path/to/request.json \
  --request-sha256 "$REVIEW_REQUEST_SHA256" \
  --manifest /absolute/path/to/manifest.json
python3 -B scripts/review_pack.py build \
  --root /absolute/path/to/review-materials \
  --request /absolute/path/to/request.json \
  --request-sha256 "$REVIEW_REQUEST_SHA256" \
  --manifest /absolute/path/to/manifest.json \
  --output /absolute/path/to/new-neutral-review.zip
```

Exit codes: **0** requested materials complete; **1** valid but partial; **2** invalid input or execution failure. A partial pack can be useful and is labeled accordingly. Build requires a recorded sanitization review. Omitted feedback stays omitted by default; use `--include-feedback` only for an intentionally informed later review. Neither action calls a model or uploads anything.

To recheck an extracted generated pack, use `review-pack/payload` as the material root, its `request.json` and `manifest.json`, and the originally pinned request digest. The generated static index is for inspection; do not execute linked source without checking it.

## Send to Pro

Attach the neutral README/task and representative full-resolution images directly. Add the source ZIP or exact permitted repository/commit/path. Include the wider indexed pack for targeted follow-up. Ask the reviewer to state which materials and tools it actually accessed. Connected GitHub supports permitted code/document retrieval in supported ChatGPT experiences; it is not a running application. Direct image attachment avoids relying on repository image discovery or embedded-PDF support. [Current product documentation](../research/STRIPE-SOURCE-MAP.md).

Use [the review prompt](../templates/pro-review-prompt.md). Request an artifact-first pass, then compare with founder annotations. Separate product findings, source hypotheses and untested runtime claims. A repo pointer is not a request to read every file. A code-only review can still be useful when visual evidence is missing, but must retain that limitation.


## Final acceptance needs the original feedback

A neutral pack is suitable for an exploratory first pass. Its completeness only concerns the pinned review request, not every original user annotation. Before accepting a feedback revision, provide the original batch and its source-to-acceptance audit, either separately or in the intentional informed pass using the existing feedback inclusion option. Preserve screenshot/page context and unresolved earlier items. Do not mark a batch complete when only the neutral pack was inspected. See [feedback coverage](feedback-coverage.md); the pack helper does not infer missing requirements or perform that audit.
