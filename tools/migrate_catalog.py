#!/usr/bin/env python3
"""Prepare one local marketplace rename. Read-only: never install or edit settings."""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'plugins/veto-codex/scripts'))
from common import load_json, nonempty

OLD_NAME = 'veto-stack'
NEW_NAME = 'veto-codex'
DEFAULT_PATH = './plugins/veto-codex'
SECRET_KEY = re.compile(r'(?:password|secret|token|credential|api[_-]?key|private[_-]?key)', re.I)


def source_path(value: str) -> str:
    """Restrict suggestions to a literal, in-root local marketplace path."""
    if not isinstance(value, str) or not value.startswith('./'):
        raise ValueError('Source must start with ./ and be relative to the marketplace root.')
    if any(ord(c) < 32 for c in value) or '\\' in value or ':' in value or '%' in value:
        raise ValueError('Source contains an unsafe or encoded path component.')
    tail = value[2:]
    path = PurePosixPath(tail)
    if not tail or path.is_absolute() or any(p in {'', '.', '..'} for p in tail.split('/')):
        raise ValueError('Source must stay inside its marketplace root, without traversal.')
    return value


def refuse_secrets(value: object) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if SECRET_KEY.search(key):
                raise ValueError('Secret-like metadata detected; use a nonsecret marketplace catalog.')
            refuse_secrets(item)
    elif isinstance(value, list):
        for item in value:
            refuse_secrets(item)


def local_source(entry: dict) -> dict | str:
    value = entry.get('source')
    if isinstance(value, str):
        source_path(value)
        return value
    if not isinstance(value, dict) or value.get('source') != 'local':
        raise ValueError('Only a local source can be renamed here; reconcile remote sources separately.')
    source_path(value.get('path'))
    return value


def plan(catalog: dict, target: str = DEFAULT_PATH) -> dict:
    """Return the proposed JSON, preserving unrelated entries and policy fields exactly."""
    target = source_path(target)
    if not isinstance(catalog, dict):
        raise ValueError('Marketplace must be an object.')
    nonempty(catalog.get('name'), 'marketplace name')
    refuse_secrets(catalog)
    entries = catalog.get('plugins')
    if not isinstance(entries, list) or not entries:
        raise ValueError('Marketplace plugins must be a nonempty list.')
    names = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError('Every marketplace entry must be an object.')
        names.append(nonempty(entry.get('name'), 'plugin name'))
    if len(set(names)) != len(names):
        raise ValueError('Duplicate plugin entries must be reconciled before renaming.')
    if OLD_NAME in names and NEW_NAME in names:
        raise ValueError('Both identities are present; do not create two competing installations.')
    current = OLD_NAME if OLD_NAME in names else NEW_NAME if NEW_NAME in names else None
    if current is None:
        raise ValueError('Neither the old nor the renamed plugin is present; this is not an upgrade.')
    index = names.index(current)
    entry = entries[index]
    if 'pluginId' in entry:
        raise ValueError('Workspace pluginId is present; a local rename cannot transfer a hosted plugin identity.')
    old_source = local_source(entry)
    proposed = deepcopy(catalog)
    new_entry = proposed['plugins'][index]
    new_entry['name'] = NEW_NAME
    if isinstance(old_source, str):
        new_entry['source'] = target
    else:
        new_entry['source']['path'] = target
    canonical = json.dumps(catalog, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()
    return {
        'verdict': 'NO_CHANGE' if proposed == catalog else 'MIGRATION_PLAN',
        'marketplace': catalog['name'],
        'from_plugin': current,
        'to_plugin': NEW_NAME,
        'source_catalog_sha256': hashlib.sha256(canonical).hexdigest(),
        'proposed_catalog': proposed,
        'unchanged_other_entries': len(entries) - 1,
        'writes_performed': False,
        'native_installation_changed': False,
        'requirements': [
            'Reconcile source and verify the target path before applying the proposed catalog.',
            'Disable the old plugin through the actual host control before enabling the new identity.',
            'Keep the old source and settings for rollback, outside active discovery.',
            'Verify loading in a fresh session; this plan does not prove installation.'
        ]
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', type=Path, required=True)
    parser.add_argument('--source-path', default=DEFAULT_PATH,
                        help='./ path relative to the existing marketplace root; no files are moved.')
    args = parser.parse_args()
    try:
        result = plan(load_json(args.catalog), args.source_path)
    except (OSError, ValueError, TypeError, KeyError, UnicodeError) as exc:
        print(json.dumps({'verdict': 'BLOCKED', 'error': str(exc), 'writes_performed': False}))
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
