#!/usr/bin/env python3
"""Read verified local role instructions. No dispatch, ownership, or permission changes."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from common import digest, exact_keys, load_json, local_file, nonempty, ordinary_path

MAX_TEXT_BYTES = 40 * 1024
SHARED = ['references/working-contract.md', 'team/SHARED.md']
ROLE_ID = re.compile(r'^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$')
SHA256 = re.compile(r'^[0-9a-f]{64}$')


def catalog(root: Path, expected_manifest_sha256: str | None = None) -> tuple[dict, dict, str]:
    root = ordinary_path(root, directory=True)
    manifest_path = local_file(root, 'FILES.sha256.json')
    manifest_digest = digest(manifest_path)
    if expected_manifest_sha256 is not None:
        if not SHA256.fullmatch(expected_manifest_sha256):
            raise ValueError('Expected manifest digest must be a lowercase SHA-256.')
        if manifest_digest != expected_manifest_sha256:
            raise ValueError('Plugin manifest digest differs from the supplied pin.')
    manifest = load_json(manifest_path)
    for path in ['team/roles.json', 'RELEASE.json', 'plugin.json']:
        checked_file(root, path, manifest)
    registry = load_json(local_file(root, 'team/roles.json'))
    exact_keys(registry, {'schema_version', 'shared', 'roles'}, set(), 'role registry')
    if type(registry['schema_version']) is not int or registry['schema_version'] != 1:
        raise ValueError('Unsupported role registry schema.')
    if registry['shared'] != SHARED:
        raise ValueError('Registry must use the maintained shared-contract sources.')
    roles = registry['roles']
    if not isinstance(roles, dict) or not roles:
        raise ValueError('Registry must contain at least one role.')
    for role_id, record in roles.items():
        if not ROLE_ID.fullmatch(role_id):
            raise ValueError('Invalid registered role id.')
        exact_keys(record, {'path'}, set(), 'role record')
        if record['path'] != f'team/{role_id}/AGENTS.md':
            raise ValueError('Role path must match its registered team guide.')
        checked_file(root, record['path'], manifest)
    release = load_json(local_file(root, 'RELEASE.json'))
    plugin = load_json(local_file(root, 'plugin.json'))
    if release.get('name') != 'veto-codex' or plugin.get('name') != 'veto-codex':
        raise ValueError('Unexpected plugin identity.')
    if release.get('version') != plugin.get('version'):
        raise ValueError('Plugin and release versions disagree.')
    nonempty(release.get('version'), 'plugin version')
    return registry, manifest, manifest_digest


def checked_file(root: Path, relative: str, manifest: dict) -> Path:
    expected = manifest.get(relative)
    if not isinstance(expected, str) or not SHA256.fullmatch(expected):
        raise ValueError(f'Missing or invalid manifest entry: {relative}')
    path = local_file(root, relative)
    if digest(path) != expected:
        raise ValueError(f'Changed source: {relative}')
    return path


def prepare(root: Path, role_id: str, expected_manifest_sha256: str | None = None) -> dict:
    if not isinstance(role_id, str) or not ROLE_ID.fullmatch(role_id):
        raise ValueError('Use a registered role id, not a path or alias.')
    registry, manifest, manifest_digest = catalog(root, expected_manifest_sha256)
    if role_id not in registry['roles']:
        raise ValueError('Unknown role. Use --list; import an accepted charter before adding an alias.')
    sources = []
    for relative in [*SHARED, registry['roles'][role_id]['path']]:
        path = checked_file(root, relative, manifest)
        if path.stat().st_size > MAX_TEXT_BYTES:
            raise ValueError('Role context source exceeds 40 KiB; split supporting references.')
        content = nonempty(path.read_text(encoding='utf-8'), 'role source')
        sources.append({'path': relative, 'sha256': manifest[relative], 'content': content})
    identity = '\n'.join(f"{s['path']}:{s['sha256']}" for s in sources)
    return {
        'verdict': 'ROLE_CONTEXT_PREPARED',
        'plugin': 'veto-codex',
        'plugin_version': load_json(local_file(root, 'RELEASE.json'))['version'],
        'plugin_manifest_sha256': manifest_digest,
        'role_id': role_id,
        'role_context_sha256': hashlib.sha256(identity.encode('utf-8')).hexdigest(),
        'sources': sources,
        'runtime_changed': False,
        'authority_granted': False,
        'ownership_transferred': False,
        'native_loading_verified': False,
        'independent_review_established': False,
        'next': 'Load in a supported agent run with the actual current assignment, permissions, and evidence. Resolve links relative to each source path.',
        'limits': ['Local content integrity, not authenticated authorship or safe instructions.',
                   'No task state, credentials, model configuration, or native-agent registration is included.',
                   'A renamed or re-roled builder is not an independent reviewer.',
                   'This is not a hostile-filesystem sandbox; use a stable, trusted source checkout.']
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument('--role')
    selector.add_argument('--list', action='store_true')
    parser.add_argument('--expect-manifest-sha256', help='Optional independently retained release-manifest pin.')
    args = parser.parse_args()
    try:
        if args.list:
            registry, _, fingerprint = catalog(args.root, args.expect_manifest_sha256)
            result = {'verdict': 'ROLE_CATALOG_READ', 'roles': sorted(registry['roles']),
                      'plugin_manifest_sha256': fingerprint, 'runtime_changed': False}
        else:
            result = prepare(args.root, args.role, args.expect_manifest_sha256)
    except (OSError, ValueError, TypeError, KeyError, UnicodeError) as exc:
        print(json.dumps({'verdict': 'INVALID', 'error': str(exc)}))
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
