#!/usr/bin/env python3
"""Check pinned acceptance, optional source-feedback coverage, and declared evidence. No execution."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from common import HEX256, digest, exact_keys, load_json, local_file, nonempty, ordinary_path

PROVENANCE = {
    'rules': {'static', 'unit', 'simulation'},
    'persistence': {'service', 'integration-sandbox', 'simulation'},
    'journey': {'browser'},
    'preparation': {'model-evaluation', 'qualified-evaluation'},
    'operations': {'external-observation', 'staffed-rehearsal'},
    'field': {'user-observation'},
}
STATUSES = {'passed', 'failed', 'not_run', 'blocked', 'not_applicable'}
LIMITS = [
    'Validates declared evidence and local artifact identity; does not prove execution or truth.',
    'A contract digest is not a signature or permission; its trusted copy must be outside builder control.',
    'No production, external delivery, user benefit, accessibility or security certification is issued.',
    'Source inventory completeness, semantic fidelity, reviewer identity and independence need actual independent review.',
    'Schema 1 does not evaluate original-feedback coverage. Use schema 2 and --require-feedback for feedback-batch acceptance.',
    'The require-feedback flag constrains this invocation only; it does not authenticate reviews or install a completion gate.',
]

def validate_candidate(value: object) -> dict:
    value = exact_keys(value, {'id', 'environment'}, set(), 'candidate')
    for key in value:
        nonempty(value[key], 'candidate.' + key)
    return value

def validate_contract(c: dict) -> dict[str, dict]:
    if type(c.get('schema_version')) is not int or c['schema_version'] not in {1, 2}:
        raise ValueError('Unsupported contract schema_version.')
    required = {'schema_version', 'contract_id', 'candidate', 'requirements'}
    if c['schema_version'] == 2:
        required.add('feedback')
    exact_keys(c, required, set(), 'contract')
    if c['schema_version'] == 2:
        guard = exact_keys(c['feedback'], {'sha256', 'builder', 'reviewer'}, set(), 'feedback guard')
        if not isinstance(guard['sha256'], str) or not HEX256.fullmatch(guard['sha256']):
            raise ValueError('Invalid pinned feedback digest.')
        nonempty(guard['builder'], 'builder')
        nonempty(guard['reviewer'], 'reviewer')
        if guard['builder'] == guard['reviewer']:
            raise ValueError('Coverage reviewer must be distinct from the builder.')
    nonempty(c['contract_id'], 'contract_id')
    validate_candidate(c['candidate'])
    if not isinstance(c['requirements'], list) or not c['requirements']:
        raise ValueError('Contract requires at least one acceptance case.')
    by_id = {}
    for r in c['requirements']:
        exact_keys(r, {'id', 'expected', 'layer', 'allowed_provenance', 'required'}, set(), 'requirement')
        key = nonempty(r['id'], 'requirement.id')
        nonempty(r['expected'], 'requirement.expected')
        if key in by_id:
            raise ValueError('Duplicate contract requirement: ' + key)
        if not isinstance(r['layer'], str) or r['layer'] not in PROVENANCE:
            raise ValueError('Unknown evidence layer.')
        allowed = r['allowed_provenance']
        if not isinstance(allowed, list) or not allowed or not all(isinstance(p, str) for p in allowed):
            raise ValueError('allowed_provenance must be a nonempty string list.')
        if len(set(allowed)) != len(allowed) or not set(allowed) <= PROVENANCE[r['layer']]:
            raise ValueError('Provenance is incompatible with required layer.')
        if type(r['required']) is not bool:
            raise ValueError('required must be a boolean.')
        by_id[key] = r
    if not any(r['required'] for r in by_id.values()):
        raise ValueError('At least one independently selected requirement must be required.')
    return by_id

def unique_rows(value: object, label: str) -> dict[str, dict]:
    if not isinstance(value, list) or not value:
        raise ValueError(label + ' must be a nonempty list.')
    result = {}
    for row in value:
        if not isinstance(row, dict):
            raise ValueError(label + ' entries must be objects.')
        key = nonempty(row.get('id'), label + '.id')
        if key in result:
            raise ValueError('Duplicate ' + label + ' ID: ' + key)
        result[key] = row
    return result


def artifact(item: object, root: Path) -> Path:
    exact_keys(item, {'path', 'sha256'}, set(), 'artifact')
    if not isinstance(item['sha256'], str) or not HEX256.fullmatch(item['sha256']):
        raise ValueError('Invalid artifact SHA-256.')
    path = local_file(root, item['path'])
    if path.stat().st_size == 0 or digest(path) != item['sha256']:
        raise ValueError('Empty, stale or changed feedback artifact: ' + item['path'])
    return path


def feedback_coverage(contract: dict, contract_digest: str, batch_path: Path,
                      review_path: Path, root: Path) -> dict:
    """Validate a declared independent audit, not semantic correctness or who wrote it."""
    guard = contract['feedback']
    if digest(batch_path) != guard['sha256']:
        raise ValueError('Pinned feedback changed; obtain a new accepted contract before closing.')
    batch, review = load_json(batch_path), load_json(review_path)
    exact_keys(batch, {'schema_version', 'batch_id', 'sources', 'items'}, set(), 'feedback batch')
    if type(batch['schema_version']) is not int or batch['schema_version'] != 1:
        raise ValueError('Unsupported feedback schema_version.')
    nonempty(batch['batch_id'], 'batch_id')
    sources = unique_rows(batch['sources'], 'source')
    items = unique_rows(batch['items'], 'feedback')
    texts, gaps = {}, []
    for key, source in sources.items():
        exact_keys(source, {'id', 'kind', 'artifact'}, set(), 'source')
        if source['kind'] not in ('text', 'image', 'pdf', 'reported_summary'):
            raise ValueError('Unknown feedback source kind.')
        path = artifact(source['artifact'], root)
        if source['kind'] == 'text':
            texts[key] = path.read_text(encoding='utf-8')
        if source['kind'] == 'reported_summary':
            gaps.append({'id': key, 'status': 'original_unavailable',
                         'reason': 'A report is not the original annotation; coverage remains partial.'})
    for key, item in items.items():
        exact_keys(item, {'id', 'source_id', 'original', 'context', 'interpretation', 'kind', 'owner'},
                   set(), 'feedback item')
        for field in ('source_id', 'original', 'context', 'interpretation', 'owner'):
            nonempty(item[field], 'feedback.' + field)
        if item['source_id'] not in sources:
            raise ValueError('Feedback refers to an unknown source: ' + key)
        if item['kind'] not in ('requirement', 'question', 'observation', 'suggestion', 'decision'):
            raise ValueError('Unknown feedback kind.')
        if item['source_id'] in texts and item['original'] not in texts[item['source_id']]:
            raise ValueError('Original wording is absent from the pinned text: ' + key)
    exact_keys(review, {'schema_version', 'batch_id', 'feedback_sha256', 'contract_sha256',
                       'reviewer', 'audit_evidence', 'source_reviews', 'items'}, set(), 'coverage review')
    if type(review['schema_version']) is not int or review['schema_version'] != 1:
        raise ValueError('Unsupported coverage review schema_version.')
    if (review['batch_id'] != batch['batch_id'] or review['feedback_sha256'] != guard['sha256'] or
            review['contract_sha256'] != contract_digest or review['reviewer'] != guard['reviewer']):
        raise ValueError('Coverage audit is stale or belongs to a different contract, batch or reviewer.')
    artifact(review['audit_evidence'], root)
    source_reviews = unique_rows(review['source_reviews'], 'source review')
    if set(source_reviews) != set(sources):
        raise ValueError('Coverage audit must account for every original source, not just listed items.')
    for key, row in source_reviews.items():
        exact_keys(row, {'id', 'status', 'finding'}, set(), 'source review')
        nonempty(row['finding'], 'source review finding')
        if row['status'] not in ('complete', 'gap', 'unavailable'):
            raise ValueError('Unknown source review status.')
        if row['status'] != 'complete':
            gaps.append({'id': key, 'status': row['status'], 'reason': row['finding']})
    mappings = unique_rows(review['items'], 'coverage item')
    if set(mappings) != set(items):
        raise ValueError('Coverage audit dropped or added feedback IDs.')
    requirements = {r['id']: r for r in contract['requirements']}
    for key, row in mappings.items():
        exact_keys(row, {'id', 'status', 'requirement_ids', 'reason'},
                   {'answer', 'decision'}, 'coverage item')
        nonempty(row['reason'], 'coverage reason')
        ids = row['requirement_ids']
        if (not isinstance(ids, list) or not all(isinstance(i, str) for i in ids) or
                len(ids) != len(set(ids)) or not set(ids) <= set(requirements)):
            raise ValueError('Invalid, duplicate or unknown acceptance IDs for ' + key)
        status = row['status']
        if status not in ('covered', 'answered', 'superseded', 'not_applicable', 'deferred', 'unresolved'):
            raise ValueError('Unknown coverage status.')
        if status == 'covered':
            if not ids or not all(requirements[i]['required'] for i in ids):
                raise ValueError('Covered feedback needs required acceptance cases: ' + key)
        elif status == 'answered':
            if items[key]['kind'] != 'question' or ids:
                raise ValueError('Only a question can close as answered; behavior needs acceptance cases.')
            artifact(row.get('answer'), root)
        elif status in ('superseded', 'not_applicable'):
            if ids:
                raise ValueError('A disposition must not also silently carry acceptance mappings.')
            decision = exact_keys(row.get('decision'), {'source_id', 'quote'}, set(), 'disposition decision')
            nonempty(decision['quote'], 'decision quote')
            # Nontext decisions need a reviewed text transcript in the source inventory.
            if decision['source_id'] not in texts or decision['quote'] not in texts[decision['source_id']]:
                raise ValueError('Disposition needs a decision in the pinned original text.')
        else:
            gaps.append({'id': key, 'status': status, 'reason': row['reason']})
    return {'verdict': 'NOT_ACCEPTED' if gaps else 'DECLARED_COVERAGE_CONSISTENT',
            'batch_id': batch['batch_id'], 'source_count': len(sources), 'item_count': len(items),
            'reviewer': review['reviewer'], 'gaps': gaps}


def check(contract_path: Path, trusted_digest: str, receipt_path: Path, artifact_root: Path, *,
          feedback_path: Path | None = None, coverage_path: Path | None = None,
          require_feedback: bool = False) -> dict:
    if not isinstance(trusted_digest, str) or not HEX256.fullmatch(trusted_digest):
        raise ValueError('Expected a lowercase 64-character trusted contract SHA-256.')
    if digest(contract_path) != trusted_digest:
        raise ValueError('Accepted contract digest mismatch. Do not silently update the trusted digest.')
    contract, receipt = load_json(contract_path), load_json(receipt_path)
    requirements = validate_contract(contract)
    if type(require_feedback) is not bool:
        raise ValueError('require_feedback must be a boolean.')
    if require_feedback and contract['schema_version'] != 2:
        raise ValueError('Feedback coverage is required for this invocation; use a pinned schema-2 contract, not evidence-only schema 1.')
    ordinary_path(artifact_root, directory=True)
    coverage = {'verdict': 'NOT_CHECKED', 'gaps': []}
    if contract['schema_version'] == 2:
        if feedback_path is None or coverage_path is None:
            raise ValueError('Schema 2 requires --feedback and --coverage-review; evidence alone cannot close this batch.')
        coverage = feedback_coverage(contract, trusted_digest, feedback_path, coverage_path, artifact_root)
    elif feedback_path is not None or coverage_path is not None:
        raise ValueError('Pin feedback in a schema-2 accepted contract before checking coverage.')
    exact_keys(receipt, {'schema_version', 'contract_id', 'contract_sha256', 'candidate', 'results'}, set(), 'receipt')
    if type(receipt['schema_version']) is not int or receipt['schema_version'] != contract['schema_version']:
        raise ValueError('Unsupported receipt schema_version.')
    if receipt['contract_id'] != contract['contract_id'] or receipt['contract_sha256'] != trusted_digest:
        raise ValueError('Receipt refers to a different contract.')
    validate_candidate(receipt['candidate'])
    if receipt['candidate'] != contract['candidate']:
        raise ValueError('Candidate or environment mismatch.')
    ordinary_path(artifact_root, directory=True)
    if not isinstance(receipt['results'], list):
        raise ValueError('results must be a list.')
    seen, gaps, verified = set(), list(coverage['gaps']), 0
    for row in receipt['results']:
        exact_keys(row, {'id', 'status', 'layer', 'actual', 'evidence'},
                   {'provenance', 'procedure', 'mode', 'carry_reason', 'reason'}, 'result')
        key = nonempty(row['id'], 'result.id')
        if key not in requirements or key in seen:
            raise ValueError('Unknown or duplicate result: ' + key)
        seen.add(key)
        req = requirements[key]
        status = row['status']
        if not isinstance(status, str) or status not in STATUSES:
            raise ValueError('Unknown result status.')
        if row['layer'] != req['layer']:
            raise ValueError('Result layer does not match the contract.')
        nonempty(row['actual'], 'result.actual')
        if not isinstance(row['evidence'], list):
            raise ValueError('evidence must be a list.')
        # Validate supplied artifacts even for a failed or blocked case.
        paths = set()
        for item in row['evidence']:
            exact_keys(item, {'path', 'sha256'}, set(), 'evidence item')
            if not isinstance(item['sha256'], str) or not HEX256.fullmatch(item['sha256']):
                raise ValueError('Invalid artifact SHA-256.')
            f = local_file(artifact_root, item['path'])
            if f in paths:
                raise ValueError('Duplicate evidence artifact in one result.')
            paths.add(f)
            if f.stat().st_size == 0 or digest(f) != item['sha256']:
                raise ValueError('Artifact is empty or its digest does not match.')
            verified += 1
        if status == 'passed':
            nonempty(row.get('procedure'), 'passed result procedure')
            if row.get('provenance') not in req['allowed_provenance']:
                raise ValueError('Passing result does not have required evidence provenance.')
            if not row['evidence']:
                raise ValueError('A passing result requires artifact evidence.')
            if row.get('mode') not in {'fresh', 'carried'}:
                raise ValueError('A passing result must declare fresh or carried evidence.')
            if row.get('mode') == 'carried':
                nonempty(row.get('carry_reason'), 'carried evidence rationale')
        elif status == 'not_applicable':
            nonempty(row.get('reason'), 'not_applicable reason')
            if req['required']:
                gaps.append({'id': key, 'status': status, 'reason': 'Required case cannot be waived in receipt.'})
        else:
            nonempty(row.get('reason'), 'unpassed result reason')
            gaps.append({'id': key, 'status': status, 'reason': row['reason']})
    missing = sorted(requirements.keys() - seen)
    if missing:
        raise ValueError('Missing acceptance results: ' + ', '.join(missing))
    consistent = ('DECLARED_COVERAGE_AND_EVIDENCE_CONSISTENT' if contract['schema_version'] == 2
                  else 'DECLARED_EVIDENCE_CONSISTENT')
    return {'verdict': 'NOT_ACCEPTED' if gaps else consistent,
            'feedback_required': require_feedback, 'feedback_coverage': coverage,
            'contract_id': contract['contract_id'], 'candidate': contract['candidate'],
            'requirements_checked': len(requirements), 'artifact_references_checked': verified,
            'gaps': gaps, 'limits': LIMITS}

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--contract', required=True, type=Path)
    ap.add_argument('--contract-sha256', required=True, help='Digest from the accepted, independently held record.')
    ap.add_argument('--receipt', required=True, type=Path)
    ap.add_argument('--artifact-root', required=True, type=Path)
    ap.add_argument('--require-feedback', action='store_true',
                    help='Reject evidence-only schema-1 contracts for a feedback-batch completion check.')
    ap.add_argument('--feedback', type=Path, help='Pinned original-feedback capture required by a schema-2 contract.')
    ap.add_argument('--coverage-review', type=Path, help='Independent source-to-contract audit, not a builder summary.')
    args = ap.parse_args()
    try:
        result = check(args.contract, args.contract_sha256, args.receipt, args.artifact_root,
                       feedback_path=args.feedback, coverage_path=args.coverage_review,
                       require_feedback=args.require_feedback)
    except (ValueError, OSError, UnicodeError, TypeError) as exc:
        print(json.dumps({'verdict': 'INVALID', 'error': str(exc), 'limits': LIMITS}, indent=2))
        return 2
    print(json.dumps(result, indent=2))
    return 1 if result['gaps'] else 0

if __name__ == '__main__':
    sys.exit(main())
