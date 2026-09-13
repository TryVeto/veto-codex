#!/usr/bin/env python3
"""Read-only, dependency-free source-pattern review. Not a semantic design audit."""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

EXTENSIONS = {'.html', '.htm', '.jsx', '.tsx', '.js', '.ts', '.css', '.vue', '.svelte'}
EXCLUDED = {'.git', 'node_modules', '.next', 'dist', 'build', 'coverage', '__pycache__',
            'tests', 'test', '__tests__', 'fixtures', 'product-quality'}
MAX_BYTES = 20 * 1024 * 1024
RULES = [
 ('decorative-component', 'review',
  r'<(?:[\w]+\.)?(?:Eyebrow|Kicker|Overline)(?=[\s/>])',
  'Remove the decorative preheading; retain necessary functional labels.'),
 ('decorative-class', 'review',
  r'\b(?:class|className)\s*=\s*(?:\{\s*)?["\'][^"\'\n]*\b(?:eyebrow|kicker|overline)\b[^"\'\n]*["\']',
  'Inspect the named decorative marker and remove redundant preheading UI, not just its name.'),
 ('decorative-css', 'review',
  r'\.[\w-]*(?:eyebrow|kicker|overline)[\w-]*(?=\s*[{,:.>])',
  'Check rendered usage. Remove obsolete decorative styles only when no necessary behavior relies on them.'),
 ('inert-link', 'review',
  r'\bhref\s*=\s*["\'](?:#|javascript:\s*void\(0\);?)["\']',
  'Use a real destination or a semantic action control; verify behavior before changing it.'),
 ('generic-hype', 'review',
  r'\b(?:unlock seamless|seamlessly orchestrate|revolutionize your workflow|effortless intelligence)\b',
  'Replace vague promotional language with the actual job or result, where this is UI copy.'),
 ('unsupported-assurance', 'review',
  r'\b(?:100%\s+(?:safe|secure)|fraud[- ]proof|AI[- ]verified|guaranteed safe)\b',
  'Check the evidence and scope. A source match, model output or badge is not universal assurance.'),
 ('focus-removed', 'review',
  r'\boutline\s*:\s*(?:none|0(?:px)?)\s*[;}]',
  'Verify an adequate visible replacement focus indicator; this pattern alone does not prove a defect.'),
]

def mask_noncontent(text: str) -> str:
    """Keep character and line positions while masking comments and data assets."""
    def blank(match: re.Match) -> str:
        return ''.join('\n' if c == '\n' else ' ' for c in match.group())
    for pattern in [r'<!--.*?-->', r'/\*.*?\*/', r'(?m)^\s*//[^\n]*',
                    r'data:[^\s"\'<>]+']:
        text = re.sub(pattern, blank, text, flags=re.S)
    return text

def inspect_text(text: str, path: str) -> list[dict]:
    masked = mask_noncontent(text)
    findings = []
    for rule, severity, pattern, action in RULES:
        for match in re.finditer(pattern, masked, re.I):
            findings.append({'rule': rule, 'severity': severity, 'path': path,
                             'line': masked.count('\n', 0, match.start()) + 1,
                             'evidence': match.group()[:160], 'action': action})
    return sorted(findings, key=lambda f: (f['path'], f['line'], f['rule']))

def scan(target: Path) -> dict:
    if not target.exists() or target.is_symlink():
        raise ValueError('Target must be an existing, non-symlink file or directory.')
    for ancestor in target.absolute().parents:
        if ancestor.is_symlink():
            raise ValueError('Target path cannot pass through a symlink.')
    if not target.is_file() and not target.is_dir():
        raise ValueError('Target must be an ordinary file or directory.')
    files: list[Path] = []
    skipped: list[dict] = []
    def walk(folder: Path) -> None:
        for path in sorted(folder.iterdir()):
            if path.is_symlink():
                skipped.append({'path': str(path), 'reason': 'symlink not followed'})
            elif path.name in EXCLUDED and path.is_dir():
                skipped.append({'path': str(path), 'reason': 'excluded directory'})
            elif path.is_dir():
                walk(path)
            elif path.is_file() and path.suffix.lower() in EXTENSIONS:
                files.append(path)
    if target.is_dir():
        walk(target)
    elif target.suffix.lower() in EXTENSIONS:
        files.append(target)
    else:
        raise ValueError('Unsupported target extension; select actual UI-source files.')
    findings, scanned = [], []
    for path in files:
        if path.stat().st_size > MAX_BYTES:
            skipped.append({'path': str(path), 'reason': 'over 20 MiB; inspect separately'})
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except (UnicodeError, OSError) as exc:
            skipped.append({'path': str(path), 'reason': type(exc).__name__})
            continue
        scanned.append(str(path))
        findings.extend(inspect_text(text, str(path)))
    return {'scope': str(target), 'scanned_files': scanned, 'skipped': skipped,
            'findings': findings, 'limits': [
                'Literal source patterns only; dynamic UI and semantic slop can be missed.',
                'All findings require semantic review; no files were changed.',
                'No rendered, accessibility, product-value or authority claim is certified.']}

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('target', type=Path)
    ap.epilog = 'Exit 0: no heuristic matches; 1: review findings; 2: invalid input or incomplete coverage. Never a quality certificate.'
    ap.add_argument('--json', action='store_true', dest='as_json')
    args = ap.parse_args()
    try:
        result = scan(args.target)
    except (ValueError, OSError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    if args.as_json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Inspected {len(result['scanned_files'])} source file(s); "
              f"{len(result['skipped'])} scope exclusion(s).")
        for finding in result['findings']:
            print(f"{finding['severity'].upper()} {finding['path']}:{finding['line']} "
                  f"[{finding['rule']}] {finding['action']}")
        for item in result['skipped']:
            print(f"SCOPE {item['path']}: {item['reason']}")
        print('No matches does not establish a slop-free or usable product.')
    if not result['scanned_files'] or any(item['reason'] != 'excluded directory' for item in result['skipped']):
        return 2
    return 1 if result['findings'] else 0

if __name__ == '__main__':
    raise SystemExit(main())
