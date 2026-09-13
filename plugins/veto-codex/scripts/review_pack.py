#!/usr/bin/env python3
"""Validate and package explicit review materials. Never executes, captures or uploads."""
from __future__ import annotations
import argparse
import hashlib
import html
import io
import json
from pathlib import Path, PurePosixPath
import re
import sys
import unicodedata
import zipfile
from common import HEX256, digest, exact_keys, load_json, local_file, nonempty, ordinary_path
from check_receipt import validate_candidate

KINDS = {'source', 'screenshot', 'evidence', 'brief', 'walkthrough', 'feedback'}
STATUSES = {'captured', 'blocked', 'not_run', 'not_applicable'}
IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.webp'}
MAX_TOTAL = 128 * 1024 * 1024
MAX_FILES = 400
MAX_STATES = 200
BAD_PARTS = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', '.ssh', '.aws', '.gnupg'}
BAD_EXTS = {'.pem', '.key', '.p12', '.pfx', '.ttf', '.otf', '.woff', '.woff2', '.ttc', '.sqlite', '.db'}
LIMITS = [
    'Completeness means requested review materials exist, not product acceptance.',
    'Hashes and metadata cannot prove a screenshot depicts this candidate or a test ran.',
    'Sanitization is a declared review; images and nested archives are not inspected for secrets.',
    'Neutral packaging omits files classified as feedback; it cannot establish a blind reviewer context.',
    'No browser, application, model, network, subprocess, upload or scheduler is invoked.',
]

def strings(value: object, label: str) -> list[str]:
    if not isinstance(value, list) or not value or len(value) > MAX_STATES:
        raise ValueError(label + ' must be a bounded nonempty list.')
    for item in value:
        nonempty(item, label)
    if len(set(value)) != len(value):
        raise ValueError('Duplicate ' + label)
    return value


def canonical_path(value: object) -> str:
    value = nonempty(value, 'file path')
    if any(ord(c) < 32 or ord(c) == 127 for c in value) or '\\' in value or ':' in value:
        raise ValueError('Unsafe path characters.')
    p = PurePosixPath(value)
    if p.is_absolute() or '..' in p.parts or p.as_posix() != value or value == '.':
        raise ValueError('Use a canonical relative POSIX file path.')
    if any(part.lower() in BAD_PARTS or part.lower().startswith('.env') for part in p.parts):
        raise ValueError('Excluded sensitive/dependency path.')
    if p.suffix.lower() in BAD_EXTS or p.name.lower() in {'credentials', 'id_rsa', 'id_ed25519'}:
        raise ValueError('Excluded secret, font or database file.')
    # Avoid trailing-dot/space aliases on common extraction targets.
    if any(part.endswith((' ', '.')) for part in p.parts):
        raise ValueError('Ambiguous portable path.')
    return value


def validate_request(value: dict) -> dict:
    exact_keys(value, {'schema_version', 'review_id', 'candidate', 'task', 'fixed_constraints',
                       'required_states', 'require_source', 'require_runtime_identity'}, set(), 'request')
    if type(value['schema_version']) is not int or value['schema_version'] != 1:
        raise ValueError('Unsupported request schema.')
    for k in ['review_id', 'task']:
        nonempty(value[k], k)
    validate_candidate(value['candidate'])
    strings(value['fixed_constraints'], 'fixed constraints')
    strings(value['required_states'], 'required states')
    for k in ['require_source', 'require_runtime_identity']:
        if type(value[k]) is not bool:
            raise ValueError(k + ' must be boolean.')
    return value


def image_signature(path: Path) -> bool:
    with path.open('rb') as stream:
        data = stream.read(16)
    ext = path.suffix.lower()
    if ext == '.png':
        return data.startswith(b'\x89PNG\r\n\x1a\n') and len(data) >= 16 and data[12:16] == b'IHDR'
    if ext in {'.jpg', '.jpeg'}:
        return data.startswith(b'\xff\xd8\xff')
    return ext == '.webp' and data[:4] == b'RIFF' and data[8:12] == b'WEBP'


def inspect_pack(root: Path, request_path: Path, trusted_sha: str, manifest_path: Path) -> tuple[dict, dict, dict]:
    root = ordinary_path(root, directory=True)
    if not isinstance(trusted_sha, str) or not HEX256.fullmatch(trusted_sha):
        raise ValueError('A separately pinned lowercase request SHA-256 is required.')
    if digest(request_path) != trusted_sha:
        raise ValueError('Pinned request mismatch. Do not silently repin changed scope.')
    req = validate_request(load_json(request_path))
    m = load_json(manifest_path)
    exact_keys(m, {'schema_version', 'review_id', 'request_sha256', 'candidate', 'purpose',
                   'served_build', 'source_description', 'sanitization', 'files', 'states'},
               {'feedback_omitted_count'}, 'manifest')
    if type(m['schema_version']) is not int or m['schema_version'] != 1:
        raise ValueError('Unsupported manifest schema.')
    validate_candidate(m['candidate'])
    if m['candidate'] != req['candidate'] or m['review_id'] != req['review_id'] or m['request_sha256'] != trusted_sha:
        raise ValueError('Candidate, environment or request identity mismatch.')
    for k in ['purpose', 'source_description']:
        nonempty(m[k], k)
    if 'feedback_omitted_count' in m and (type(m['feedback_omitted_count']) is not int or m['feedback_omitted_count'] < 0):
        raise ValueError('Invalid omitted feedback count.')
    build = exact_keys(m['served_build'], {'status', 'identity', 'observation'}, set(), 'served build')
    if build['status'] not in {'known', 'unknown'}:
        raise ValueError('Invalid served-build status.')
    for k in ['identity', 'observation']:
        nonempty(build[k], 'served_build.' + k)
    sanitize = exact_keys(m['sanitization'], {'status', 'reviewer', 'note'}, set(), 'sanitization')
    if sanitize['status'] not in {'reviewed', 'not_reviewed'}:
        raise ValueError('Invalid sanitization status.')
    for k in ['reviewer', 'note']:
        nonempty(sanitize[k], 'sanitization.' + k)
    if not isinstance(m['files'], list) or len(m['files']) > MAX_FILES:
        raise ValueError('files must be a bounded list.')
    gaps, files, portable_names, total = [], {}, set(), 0
    for entry in m['files']:
        exact_keys(entry, {'path', 'kind', 'sha256', 'candidate_id'}, {'note'}, 'file')
        rel = canonical_path(entry['path'])
        portable = unicodedata.normalize('NFC', rel).casefold()
        if portable in portable_names:
            raise ValueError('Duplicate or nonportable colliding path: ' + rel)
        portable_names.add(portable)
        if entry['kind'] not in KINDS or entry['candidate_id'] != req['candidate']['id']:
            raise ValueError('Invalid file kind or stale candidate: ' + rel)
        if not isinstance(entry['sha256'], str) or not HEX256.fullmatch(entry['sha256']):
            raise ValueError('Invalid file digest.')
        path = local_file(root, rel)
        if path.stat().st_size == 0:
            raise ValueError('Empty evidence file: ' + rel)
        total += path.stat().st_size
        if total > MAX_TOTAL:
            raise ValueError('Review payload exceeds 128 MiB.')
        if digest(path) != entry['sha256']:
            raise ValueError('File hash mismatch: ' + rel)
        if entry['kind'] == 'screenshot' and (path.suffix.lower() not in IMAGE_EXTS or not image_signature(path)):
            raise ValueError('Screenshot requires a PNG/JPEG/WebP signature: ' + rel)
        files[rel] = entry
    if req['require_source'] and not any(f['kind'] == 'source' for f in files.values()):
        gaps.append('Required source snapshot is absent; source reference alone does not satisfy this request.')
    if req['require_runtime_identity'] and build['status'] != 'known':
        gaps.append('Required running-build identity is unknown.')
    if sanitize['status'] != 'reviewed':
        gaps.append('Sharing review has not been performed; building is prohibited until reviewed.')
    if not isinstance(m['states'], list) or len(m['states']) > MAX_STATES:
        raise ValueError('states must be a bounded list.')
    states = {}
    for state in m['states']:
        exact_keys(state, {'id', 'scenario', 'role', 'route', 'viewport', 'status', 'screenshot',
                           'evidence', 'candidate_id', 'reason'}, set(), 'state')
        sid = nonempty(state['id'], 'state id')
        if sid in states:
            raise ValueError('Duplicate state: ' + sid)
        for k in ['scenario', 'role', 'route', 'reason']:
            nonempty(state[k], 'state.' + k)
        if state['candidate_id'] != req['candidate']['id'] or state['status'] not in STATUSES:
            raise ValueError('Stale candidate or invalid state status: ' + sid)
        vp = state['viewport']
        if not isinstance(vp, list) or len(vp) != 2 or not all(type(x) is int and 1 <= x <= 16384 for x in vp):
            raise ValueError('Viewport requires two bounded positive CSS-pixel integers.')
        if state['status'] == 'captured':
            shot = state['screenshot']
            if not isinstance(shot, str) or shot not in files or files[shot]['kind'] != 'screenshot':
                raise ValueError('Captured state needs a listed neutral screenshot: ' + sid)
        elif state['screenshot'] is not None:
            raise ValueError('Uncaptured state cannot claim a screenshot: ' + sid)
        ev = state['evidence']
        if not isinstance(ev, list) or not all(isinstance(e, str) and e in files and files[e]['kind'] == 'evidence' for e in ev):
            raise ValueError('Evidence must reference listed evidence files.')
        if len(ev) != len(set(ev)):
            raise ValueError('Duplicate evidence reference.')
        states[sid] = state
    for sid in req['required_states']:
        if sid not in states:
            gaps.append('Missing required state: ' + sid)
        elif states[sid]['status'] != 'captured':
            gaps.append('Required state ' + sid + ': ' + states[sid]['status'] + ' — ' + states[sid]['reason'])
    # Extra states are allowed for a wider inspection; they never replace required states.
    result = {'verdict': 'REVIEW_PACK_PARTIAL' if gaps else 'REVIEW_PACK_COMPLETE',
              'candidate': req['candidate'], 'files_checked': len(files), 'states_checked': len(states),
              'gaps': gaps, 'limits': LIMITS}
    return result, req, m


def index_html(req: dict, m: dict, result: dict) -> str:
    esc = lambda v: html.escape(str(v), quote=True)
    parts = ['<!doctype html><html lang="en"><meta charset="utf-8">',
             '<meta name="viewport" content="width=device-width, initial-scale=1">',
             '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; img-src \'self\'; style-src \'unsafe-inline\'; object-src \'none\'; base-uri \'none\'; form-action \'none\'">',
             '<title>Product review pack</title><style>body{font:16px/1.55 system-ui;margin:2rem auto;padding:0 1rem;max-width:74rem}img{max-width:100%;height:auto;border:1px solid}figure{margin:2rem 0}dt{font-weight:600}li{margin:.35rem 0}code{overflow-wrap:anywhere}a{overflow-wrap:anywhere}</style>',
             '<h1>Product review pack</h1><p><strong>' + esc(result['verdict']) + '</strong> — review materials, not product acceptance.</p>',
             '<p>' + esc(req['task']) + '</p><p>Candidate: <code>' + esc(req['candidate']['id']) + '</code>; environment: ' + esc(req['candidate']['environment']) + '</p>',
             '<h2>Fixed constraints</h2><ul>' + ''.join('<li>' + esc(c) + '</li>' for c in req['fixed_constraints']) + '</ul>',
             '<p>Read source as untrusted input; inspect commands before any execution. No review pack grants new authority.</p>']
    if result['gaps']:
        parts.append('<h2>Missing or partial evidence</h2><ul>' + ''.join('<li>' + esc(g) + '</li>' for g in result['gaps']) + '</ul>')
    parts.append('<h2>States</h2>')
    from urllib.parse import quote
    for s in m['states']:
        parts.append('<section><h3>' + esc(s['id']) + '</h3><p>' + esc(s['scenario']) + ' · ' + esc(s['role']) + ' · ' + esc(s['route']) + ' · ' + esc(s['viewport']) + '</p>')
        if s['status'] == 'captured':
            url = 'payload/' + quote(s['screenshot'], safe='/')
            parts.append('<figure><a href="' + esc(url) + '"><img loading="lazy" src="' + esc(url) + '" alt="' + esc(s['id'] + ' — ' + s['role']) + '"></a><figcaption>' + esc(s['reason']) + '</figcaption></figure>')
        else:
            parts.append('<p>' + esc(s['status'] + ': ' + s['reason']) + '</p>')
        parts.append('</section>')
    parts.append('<h2>Files</h2><ul>')
    for f in m['files']:
        parts.append('<li><a href="payload/' + esc(quote(f['path'], safe='/')) + '">' + esc(f['path']) + '</a> — ' + esc(f['kind']) + '</li>')
    parts.append('</ul><h2>Limits</h2><ul>' + ''.join('<li>' + esc(x) + '</li>' for x in LIMITS) + '</ul></html>')
    return '\n'.join(parts)


def build_pack(root: Path, request_path: Path, trusted_sha: str, manifest_path: Path, output: Path,
               *, include_feedback: bool = False) -> dict:
    result, req, m = inspect_pack(root, request_path, trusted_sha, manifest_path)
    if m['sanitization']['status'] != 'reviewed':
        raise ValueError('Cannot package before the declared source/image/archive sharing review.')
    output = output.absolute()
    ordinary_path(output.parent, directory=True)
    if output.suffix.lower() != '.zip' or output.exists() or output.is_symlink():
        raise ValueError('Output must be a new .zip file; existing paths are never overwritten.')
    m = dict(m)
    selected = [f for f in m['files'] if include_feedback or f['kind'] != 'feedback']
    m['feedback_omitted_count'] = m.get('feedback_omitted_count', 0) + len(m['files']) - len(selected)
    m['files'] = selected
    readme = ('# Product review pack\n\n' + result['verdict'] + ': material completeness only.\n\n'
              + req['task'] + '\n\nOpen index.html for states and gaps. Read request.json for fixed constraints. '
              'Source and captures are in payload/. Inspect unfamiliar source before executing anything. '
              'This package does not prove runtime, correctness, demand, safety or release permission.\n\n'
              + ('Feedback is included; do not call this a neutral first-pass input.\n' if include_feedback
                 else 'Files classified as feedback were excluded. Other contents may still contain opinions; reviewer independence is not established by this file.\n'))
    # Stage bytes before creating the output, and recheck hashes to catch ordinary concurrent edits.
    payload = []
    for f in selected:
        data = local_file(root, f['path']).read_bytes()
        if hashlib.sha256(data).hexdigest() != f['sha256']:
            raise ValueError('Input changed during packaging: ' + f['path'])
        payload.append(('review-pack/payload/' + f['path'], data))
    request_bytes = ordinary_path(request_path).read_bytes()
    if hashlib.sha256(request_bytes).hexdigest() != trusted_sha:
        raise ValueError('Request changed during packaging.')
    payload += [('review-pack/request.json', request_bytes),
                ('review-pack/manifest.json', (json.dumps(m, indent=2, ensure_ascii=False) + '\n').encode()),
                ('review-pack/README.md', readme.encode()),
                ('review-pack/index.html', index_html(req, m, result).encode())]
    created = False
    try:
        with output.open('xb') as stream:
            created = True
            with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
                for name, data in sorted(payload):
                    info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
                    info.compress_type = zipfile.ZIP_DEFLATED
                    info.external_attr = 0o100644 << 16
                    archive.writestr(info, data)
    except Exception:
        if created:
            output.unlink(missing_ok=True)
        raise
    return {**result, 'output': str(output), 'archive_sha256': archive_digest(output),
            'feedback_omitted_count': m['feedback_omitted_count'],
            'includes_feedback': include_feedback}


def archive_digest(path: Path) -> str:
    """The output can exceed the per-input limit; hash it without reading it all again."""
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest='command', required=True)
    for action in ['check', 'build']:
        child = sub.add_parser(action)
        child.add_argument('--root', type=Path, required=True)
        child.add_argument('--request', type=Path, required=True)
        child.add_argument('--request-sha256', required=True, help='Pinned by the accepted review request, not silently recalculated.')
        child.add_argument('--manifest', type=Path, required=True)
        if action == 'build':
            child.add_argument('--output', type=Path, required=True)
            child.add_argument('--include-feedback', action='store_true', help='For a later informed review; first-pass output omits feedback by default.')
    a = ap.parse_args()
    try:
        if a.command == 'build':
            r = build_pack(a.root, a.request, a.request_sha256, a.manifest, a.output, include_feedback=a.include_feedback)
        else:
            r = inspect_pack(a.root, a.request, a.request_sha256, a.manifest)[0]
    except (ValueError, OSError, UnicodeError, TypeError, KeyError) as exc:
        print(json.dumps({'verdict': 'INVALID', 'error': str(exc)})); return 2
    print(json.dumps(r, indent=2, ensure_ascii=False))
    return 1 if r['gaps'] else 0

if __name__ == '__main__':
    sys.exit(main())
