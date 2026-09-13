#!/usr/bin/env python3
"""Offline structural checks for this Veto Codex edition, not host installation validation."""
from __future__ import annotations
import argparse
import ast
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit
from common import digest, load_json, local_file, nonempty, ordinary_path

SCHEMA = 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json'
SKILLS = {'veto-codex', 'product-sense', 'product-design', 'remove-slop', 'build-a-capability',
          'product-tests', 'integration-design', 'field-proof', 'make-a-goal',
          'review-a-prototype', 'independent-judgment', 'sandbox-experience', 'work-control'}
FONT_EXTENSIONS = {'.ttf','.otf','.woff','.woff2','.ttc'}
SECRET_EXTENSIONS = {'.pem','.key','.p12','.pfx'}


def frontmatter(text: str) -> dict:
    if not text.startswith('---\n') or '\n---\n' not in text[4:]:
        raise ValueError('Missing skill frontmatter.')
    raw = text[4:].split('\n---\n', 1)[0]
    fields = {}
    for line in raw.splitlines():
        key, sep, val = line.partition(':')
        if not sep or key in fields or key not in {'name','description'}:
            raise ValueError('Unexpected/duplicate frontmatter field in this edition.')
        fields[key] = json.loads(val.strip()) if val.strip().startswith('"') else val.strip()
    if set(fields) != {'name','description'}:
        raise ValueError('Expected name and description.')
    return fields


def check_manifest(root: Path) -> list[str]:
    errors=[]
    primary=load_json(root/'plugin.json')
    allowed={'$schema','name','version','description','author','homepage','repository','license','keywords','extensions'}
    if set(primary)-allowed or primary.get('$schema') != SCHEMA:
        errors.append('Portable manifest schema or root fields invalid.')
    name=primary.get('name','')
    if not isinstance(name,str) or not (1<=len(name)<=64) or not re.fullmatch(r'(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?',name):
        errors.append('Portable manifest name invalid.')
    version=primary.get('version','')
    if not isinstance(version,str) or not re.fullmatch(r'\d+\.\d+\.\d+',version):
        errors.append('This edition requires a three-part numeric version.')
    for key in ['description','version']:
        nonempty(primary.get(key),key)
    if name!='veto-codex': errors.append('Unexpected plugin identity.')
    ext=primary.get('extensions')
    if not isinstance(ext,dict) or set(ext)!={'com.openai'} or not isinstance(ext['com.openai'],dict):
        raise ValueError('Missing OpenAI presentation overlay.')
    interface=ext['com.openai'].get('interface')
    if not isinstance(interface,dict) or interface.get('displayName')!='Veto Codex':
        raise ValueError('Missing Veto Codex display name.')
    for key in ['composerIcon','logo']:
        local_file(root,interface.get(key))
    for legacy in ['.codex-plugin/plugin.json','.claude-plugin/plugin.json']:
        overlay=load_json(root/legacy)
        if overlay.get('name')!=name or overlay.get('version')!=version or overlay.get('skills')!='./skills/':
            errors.append(f'Manifest identity/version/skill root mismatch: {legacy}')
        if any(k in overlay for k in ['mcpServers','hooks','lspServers','dependencies']):
            errors.append('Unexpected executable or external component.')
    codex=load_json(root/'.codex-plugin/plugin.json')
    if codex.get('interface')!=interface:
        errors.append('Compatibility OpenAI interface does not match inline overlay.')
    return errors



def check_source_snapshots(root: Path) -> list[str]:
    """Check declared byte identity only; hashes do not establish source truth or authority."""
    errors=[]
    try:
        manifest=load_json(root/'research/next-inputs.json')
        if manifest.get('release') != load_json(root/'RELEASE.json').get('version'):
            errors.append('Source manifest release mismatch.')
        inputs=manifest.get('inputs')
        if not isinstance(inputs,list) or not inputs:
            raise ValueError('Missing source input inventory.')
        for item in inputs:
            if not isinstance(item,dict): raise ValueError('Invalid source input.')
            nonempty(item.get('input'),'source input name')
            declared=item.get('sha256')
            if not isinstance(declared,str) or not re.fullmatch(r'[0-9a-f]{64}',declared):
                raise ValueError('Invalid source input digest.')
            snapshot=item.get('packaged_snapshot')
            if snapshot is not None and digest(local_file(root,snapshot))!=declared:
                errors.append('Source snapshot hash mismatch: '+str(snapshot))
    except (ValueError,OSError,TypeError,KeyError) as exc:
        errors.append('Invalid source snapshot manifest: '+str(exc))
    return errors


def check_enclosing_marketplace(root: Path, plugin_name: str) -> tuple[list[str], list[str]]:
    """Validate this plugin's catalog entry without treating unrelated tools as duplicates.

    A personal marketplace can intentionally contain several independent plugins. The
    package check only owns the entry for this plugin; archived siblings are surfaced as
    a warning so they remain visible evidence rather than silently becoming a pass.
    """
    errors: list[str] = []
    warnings: list[str] = []
    marketplace = root.parent.parent / '.agents/plugins/marketplace.json'
    if not marketplace.exists():
        return errors, warnings
    try:
        catalog = load_json(marketplace)
        entries = catalog.get('plugins')
        if not isinstance(entries, list):
            errors.append('Enclosing marketplace plugins must be a list.')
            return errors, warnings
        named = [entry for entry in entries
                 if isinstance(entry, dict) and entry.get('name') == plugin_name]
        if len(named) != 1:
            if not named:
                errors.append(f'Enclosing marketplace is missing the {plugin_name} entry.')
            else:
                errors.append(f'Enclosing marketplace contains duplicate {plugin_name} entries.')
            return errors, warnings
        if plugin_name == 'veto-codex' and any(
            isinstance(entry, dict) and entry.get('name') == 'veto-stack'
            for entry in entries
        ):
            errors.append('Old veto-stack and new veto-codex are both discoverable; reconcile the rename.')
        expected = {'source': 'local', 'path': f'./plugins/{plugin_name}'}
        if named[0].get('source') != expected:
            errors.append('Enclosing marketplace does not point to this local plugin.')
        archive_prefix = f'archived-{plugin_name}'
        archived = sorted({entry.get('name') for entry in entries
                           if isinstance(entry, dict)
                           and isinstance(entry.get('name'), str)
                           and entry.get('name', '').startswith(archive_prefix)})
        if archived:
            warnings.append('Enclosing marketplace retains archived Veto entries: '
                            + ', '.join(archived)
                            + '. The host has no supported per-entry retirement control.')
    except (ValueError, OSError, TypeError, KeyError) as exc:
        errors.append('Invalid enclosing marketplace: ' + str(exc))
    return errors, warnings


def run(root: Path, *, verify_hashes: bool = True) -> dict:
    root=ordinary_path(root,directory=True)
    errors=check_manifest(root) + check_source_snapshots(root)
    warnings: list[str] = []
    files=[]
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            errors.append('Symlink in payload: '+str(path.relative_to(root))); continue
        if path.is_file(): files.append(path)
        if path.suffix.lower() in FONT_EXTENSIONS|SECRET_EXTENSIONS or path.name=='.env':
            errors.append('Forbidden font/secret file type: '+str(path.relative_to(root)))
        if path.name in ['mcp.json','.mcp.json','hooks.json','package.json'] or path.is_dir() and path.name in ['hooks','node_modules']:
            errors.append('Unexpected executable dependency surface: '+str(path.relative_to(root)))
    discovered={p.parent.name for p in root.glob('skills/*/SKILL.md')}
    if discovered!=SKILLS:
        errors.append('Skill inventory mismatch.')
    description_chars=0
    for path in files:
        rel=path.relative_to(root).as_posix()
        if path.suffix=='.py':
            try: ast.parse(path.read_text(),filename=rel)
            except SyntaxError as exc: errors.append(f'{rel}: Python syntax error {exc.lineno}')
        if path.suffix!='.md': continue
        text=path.read_text(encoding='utf-8')
        if path.name=='SKILL.md':
            try:
                fields=frontmatter(text)
                if fields['name']!=path.parent.name or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',fields['name']):
                    errors.append('Skill name/path mismatch: '+rel)
                desc=nonempty(fields['description'],'skill description')
                description_chars+=len(desc)
                if len(desc)>240: errors.append('Description exceeds this edition budget: '+rel)
                if len(text)>8500: errors.append('Entry skill exceeds this edition budget: '+rel)
            except (ValueError,TypeError): errors.append('Invalid frontmatter: '+rel)
        for target in re.findall(r'\[[^\]\n]+\]\(([^)\s]+)\)',text):
            parts=urlsplit(target)
            if parts.scheme or parts.netloc or not parts.path: continue
            decoded=unquote(parts.path)
            dest=(path.parent/decoded).resolve()
            if not dest.is_relative_to(root) or not dest.exists():
                errors.append(f'Broken or escaping local link: {rel} -> {target}')
    goal=root/'templates/goal.md'
    if not goal.exists() or len(goal.read_text())>=4000:
        errors.append('Goal template must be below 4,000 characters.')
    bounded_goal=root/'templates/bounded-goal.md'
    if not bounded_goal.exists() or len(bounded_goal.read_text())>=4000:
        errors.append('Bounded goal template must be below 4,000 characters.')
    release=load_json(root/'RELEASE.json')
    if release.get('version')!=load_json(root/'plugin.json').get('version'):
        errors.append('Release metadata version mismatch.')
    if verify_hashes:
        manifest=load_json(root/'FILES.sha256.json')
        actual={p.relative_to(root).as_posix() for p in files if p.relative_to(root).as_posix()!='FILES.sha256.json'}
        if set(manifest)!=actual: errors.append('Payload inventory differs from hash manifest.')
        for rel,sha in manifest.items():
            try:
                if digest(local_file(root,rel))!=sha: errors.append('Payload hash mismatch: '+rel)
            except (ValueError,OSError): errors.append('Missing/unsafe payload hash path: '+rel)
    cases=load_json(root/'evals/cases.json')
    entries=cases.get('cases',[])
    if not isinstance(entries,list) or not entries:
        errors.append('Missing behavioral cases.')
    else:
        ids=[]
        for case in entries:
            if not isinstance(case,dict): errors.append('Invalid behavior case.'); continue
            ids.append(case.get('id'))
            for key in ['id','prompt','expected_route']:
                if not isinstance(case.get(key),str) or not case[key].strip(): errors.append('Invalid eval '+key)
            for key in ['must','must_not']:
                if not isinstance(case.get(key),list) or not case[key]: errors.append('Missing eval assertions.')
        if len(set(ids))!=len(ids): errors.append('Duplicate behavioral case ids.')
    # Enclosing marketplace is optional for a plugin-folder-only transfer. Other
    # personal plugins are valid; only this plugin's identity and source are owned.
    plugin_name = load_json(root/'plugin.json').get('name')
    catalog_errors, catalog_warnings = check_enclosing_marketplace(root, plugin_name)
    errors.extend(catalog_errors)
    warnings.extend(catalog_warnings)
    return {'verdict':'FAIL' if errors else 'STRUCTURAL_CHECKS_PASSED','errors':errors,
            'package_version':release.get('version'),'plugin_root':str(root.resolve()),
            'files_checked':len(files),'skills_checked':len(discovered),'description_characters':description_chars,
            'goal_characters':len(goal.read_text()) if goal.exists() else None,
            'bounded_goal_characters':len(bounded_goal.read_text()) if bounded_goal.exists() else None,
            'warnings': warnings,
            'limits':['Local package checks only; not the native host validator.',
                      'Reported version/path identify the checked files, not instructions loaded by a running agent.',
                      'No host registration, application tests or agent-behavior evaluation is established.']}


def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('root',nargs='?',type=Path,default=Path(__file__).resolve().parents[1])
    args=ap.parse_args()
    try: result=run(args.root)
    except (ValueError,OSError,UnicodeError,KeyError,TypeError) as exc:
        print(json.dumps({'verdict':'INVALID','error':str(exc)},indent=2)); return 2
    print(json.dumps(result,indent=2)); return 1 if result['errors'] else 0

if __name__=='__main__':
    sys.exit(main())
