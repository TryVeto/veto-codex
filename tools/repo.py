#!/usr/bin/env python3
"""Validate, test and package the local Veto Codex repository. Never install or deploy."""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import zipfile
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_REL = 'plugins/veto-codex'
sys.path.insert(0, str(ROOT/PLUGIN_REL/'scripts'))
from common import load_json, ordinary_path
import doctor
import role_context

MANIFEST = 'SOURCE-MANIFEST.json'
SKIP_ROOT = {'.git', 'dist', '.artifacts', '.venv', '.pytest_cache'}
SKIP_ANY = {'__pycache__', '.DS_Store'}
BLOCK_SUFFIXES = {'.pem','.key','.p12','.pfx','.ttf','.otf','.woff','.woff2','.ttc'}
BLOCK_DIRS = {'node_modules', '.codex'}
PATTERNS = [re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
            re.compile(rb'\bgh[pousr]_[A-Za-z0-9]{36,}\b'),
            re.compile(rb'\bsk-proj-[A-Za-z0-9_-]{40,}\b')]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root: Path) -> list[Path]:
    root = ordinary_path(root, directory=True)
    files = []
    for here, dirs, names in os.walk(root, followlinks=False):
        directory = Path(here)
        dirs[:] = sorted(d for d in dirs if d not in SKIP_ANY and
                         not (directory == root and d in SKIP_ROOT))
        for name in dirs:
            p = directory/name
            if p.is_symlink(): raise ValueError('Symlink directory in source: '+str(p.relative_to(root)))
        for name in sorted(names):
            if name in SKIP_ANY or name.endswith(('.pyc','.pyo')): continue
            p = directory/name
            if p.is_symlink() or not stat.S_ISREG(p.stat().st_mode):
                raise ValueError('Only ordinary files may be packaged: '+str(p.relative_to(root)))
            files.append(p)
    return sorted(files, key=lambda p:p.relative_to(root).as_posix())


def source_map(root: Path, *, exclude: str) -> dict:
    return {p.relative_to(root).as_posix():sha(p) for p in inventory(root)
            if p.relative_to(root).as_posix() != exclude}


def refresh_hashes(root: Path) -> None:
    plugin = root/PLUGIN_REL
    (plugin/'FILES.sha256.json').write_text(json.dumps(source_map(plugin,exclude='FILES.sha256.json'),indent=2)+'\n')
    (root/MANIFEST).write_text(json.dumps(source_map(root,exclude=MANIFEST),indent=2)+'\n')


def local_link_errors(root: Path, files: list[Path]) -> list[str]:
    errors=[]
    for path in files:
        rel=path.relative_to(root).as_posix()
        if path.suffix != '.md' or rel.startswith((PLUGIN_REL+'/', 'provenance/releases/')): continue
        text=path.read_text(encoding='utf-8')
        # Path checks only. Headings are editorial links, not an HTML rendering promise.
        for target in re.findall(r'\[[^\]\n]+\]\(([^)\s]+)\)',text):
            parts=urlsplit(target)
            if parts.scheme or parts.netloc or not parts.path: continue
            resolved=(path.parent/unquote(parts.path)).resolve()
            if not resolved.is_relative_to(root.resolve()) or not resolved.exists():
                errors.append(f'Broken or escaping link: {rel} -> {target}')
    return errors


def check(root: Path) -> dict:
    root=ordinary_path(root,directory=True)
    files=inventory(root)
    errors=[]
    metadata=load_json(root/'REPOSITORY.json')
    if metadata.get('name') != 'veto-codex' or metadata.get('plugin') != PLUGIN_REL:
        errors.append('Repository identity or plugin path mismatch.')
    if not isinstance(metadata.get('version'),str) or not re.fullmatch(r'\d+\.\d+\.\d+',metadata['version']):
        errors.append('Repository version must be a three-part numeric version.')
    plugin=root/PLUGIN_REL
    plugin_result=doctor.run(plugin)
    errors.extend(plugin_result['errors'])
    if metadata.get('version') != plugin_result['package_version']:
        errors.append('Repository/plugin version mismatch.')
    registry,_,_=role_context.catalog(plugin)
    for role in registry['roles']: role_context.prepare(plugin,role)
    actual=source_map(root,exclude=MANIFEST)
    declared=load_json(root/MANIFEST)
    if set(actual) != set(declared): errors.append('Repository payload inventory mismatch.')
    for rel,value in actual.items():
        if declared.get(rel) != value: errors.append('Repository hash mismatch: '+rel)
    for p in files:
        rel=p.relative_to(root).as_posix()
        if p.suffix.lower() in BLOCK_SUFFIXES or p.name=='.env' or (p.name.startswith('.env.') and p.name!='.env.example'):
            errors.append('Forbidden secret/font file type: '+rel)
        if any(part in BLOCK_DIRS for part in p.relative_to(root).parts):
            errors.append('Unexpected active environment/dependency directory: '+rel)
        if p.suffix=='.py':
            try: ast.parse(p.read_text(encoding='utf-8'),filename=rel)
            except SyntaxError as exc: errors.append(f'Python syntax error: {rel}:{exc.lineno}')
        if p.suffix.lower() in {'.md','.txt','.json','.toml','.yml','.yaml','.py','.sh'}:
            raw=p.read_bytes()
            if any(pattern.search(raw) for pattern in PATTERNS):
                errors.append('Possible credential material; inspect before release: '+rel)
    errors.extend(local_link_errors(root,files))
    baseline=load_json(root/'provenance/baseline-files.json')
    preserved=[rel for rel in baseline if rel.startswith('tests/') or
               (rel.startswith('team/') and rel.endswith('/AGENTS.md'))]
    for rel in preserved:
        raw = (plugin/rel).read_bytes()
        original_form = raw.replace(b'veto-codex', b'veto-stack').replace(b'Veto Codex', b'Veto Stack')
        if hashlib.sha256(original_form).hexdigest() != baseline[rel]:
            errors.append('Original test/role guide changed beyond identity rename: '+rel)
    rename_baseline = load_json(root/'migration/baseline-2026.9.1202.json')['files']
    retained = [rel for rel in rename_baseline if rel.startswith('tests/') or
                rel.startswith('plugins/veto-stack/tests/') or
                (rel.startswith('plugins/veto-stack/team/') and rel.endswith('/AGENTS.md'))]
    for rel in retained:
        current = rel.replace('plugins/veto-stack/', PLUGIN_REL+'/')
        raw = (root/current).read_bytes()
        original_form = raw.replace(b'veto-codex', b'veto-stack').replace(b'Veto Codex', b'Veto Stack')
        if hashlib.sha256(original_form).hexdigest() != rename_baseline[rel]:
            errors.append('Immediate baseline test/role changed beyond identity rename: '+rel)
    if (root/'plugins/veto-stack').exists():
        errors.append('Old plugin source directory is still discoverable.')
    return {'verdict':'FAIL' if errors else 'REPOSITORY_CHECKS_PASSED',
            'version':metadata['version'],'files_checked':len(files),
            'skills':plugin_result['skills_checked'],'role_profiles':len(registry['roles']),
            'immediate_baseline_test_and_role_files_retained':len(retained),
            'original_tests_and_role_files_preserved_after_identity_mapping':len(preserved),
            'errors':errors,'warnings':plugin_result['warnings'],
            'limits':['Source integrity and local structure only; not authenticated origin.',
                      'No native installation, worker dispatch, model cost result or product deployment.',
                      'Credential-pattern scanning is a limited check, not a complete security audit.']}


def run_command(root: Path, args: list[str], expected: int = 0) -> dict:
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    result=subprocess.run([sys.executable,'-B',*args],cwd=root,env=env,
                          text=True,capture_output=True,timeout=180)
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    if result.returncode != expected:
        raise ValueError(f'Unexpected exit {result.returncode} (expected {expected}): {args}')
    return {'command':['python3','-B',*args], 'expected_exit':expected,'observed_exit':result.returncode}


def test(root: Path) -> dict:
    runs=[]
    runs.append(run_command(root,['-m','unittest','discover','-s',PLUGIN_REL+'/tests','-v']))
    runs.append(run_command(root,['-m','unittest','discover','-s','tests','-v']))
    oracle=PLUGIN_REL+'/evals/oracles/focus_oracle.py'
    runs.append(run_command(root,[oracle,PLUGIN_REL+'/evals/fixtures/focus'],expected=1))
    runs.append(run_command(root,[oracle,PLUGIN_REL+'/examples/resume-work']))
    runs.append(run_command(root,[PLUGIN_REL+'/verification/1201/reproduce_guards.py',PLUGIN_REL]))
    return {'verdict':'LOCAL_TEST_COMMANDS_PASSED','runs':runs,
            'native_agent_evaluation':False,'independent_review':False}


def write_zip(root: Path, target: Path) -> None:
    """Create a new normalized source archive. Caller owns validation and test gates."""
    files=inventory(root)
    if target.exists(): raise ValueError('Refusing to overwrite an existing release.')
    target.parent.mkdir(parents=True,exist_ok=True)
    created=False
    try:
        with zipfile.ZipFile(target,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
            created=True
            for path in files:
                name='veto-codex/'+path.relative_to(root).as_posix()
                info=zipfile.ZipInfo(name,date_time=(2026,9,12,0,0,0))
                info.create_system=3
                info.external_attr=(stat.S_IFREG | 0o644)<<16
                info.compress_type=zipfile.ZIP_DEFLATED
                archive.writestr(info,path.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    except Exception:
        if created: target.unlink(missing_ok=True)
        raise


def package(root: Path, output: Path) -> dict:
    root=root.resolve()
    output=output.absolute()
    if any(p.is_symlink() for p in (output,*output.parents)):
        raise ValueError('Output cannot be a symlink path.')
    resolved=output.resolve()
    if resolved.is_relative_to(root) and not resolved.is_relative_to(root/'dist'):
        raise ValueError('Within this repository, output must be under dist/.')
    result=check(root)
    if result['errors']: raise ValueError('\n'.join(result['errors']))
    version=result['version']
    target=resolved/f'veto-codex-repo-{version}.zip'
    sidecar=target.with_suffix('.zip.sha256')
    if target.exists() or sidecar.exists(): raise ValueError('Release or checksum already exists; choose a new output directory.')
    test(root)
    # Recheck after tests to reject source mutation during qualification.
    after=check(root)
    if after['errors']: raise ValueError('\n'.join(after['errors']))
    write_zip(root,target)
    checksum=sha(target)
    with sidecar.open('x',encoding='utf-8') as stream: stream.write(f'{checksum}  {target.name}\n')
    return {'verdict':'SOURCE_ARCHIVE_CREATED','archive':str(target),'sha256':checksum,
            'checksum_file':str(sidecar),'version':version,'installed':False,'deployed':False}


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    subs=parser.add_subparsers(dest='command',required=True)
    subs.add_parser('check');subs.add_parser('test')
    hashes=subs.add_parser('hashes');hashes.add_argument('--write',action='store_true',required=True)
    release=subs.add_parser('package');release.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    try:
        if args.command=='check': result=check(ROOT)
        elif args.command=='test': result=test(ROOT)
        elif args.command=='hashes':
            refresh_hashes(ROOT);result={'verdict':'HASH_INVENTORIES_WRITTEN','approved':False}
        else: result=package(ROOT,args.output)
        print(json.dumps(result,indent=2))
        return 1 if result.get('errors') else 0
    except (OSError,ValueError,TypeError,KeyError,UnicodeError,subprocess.TimeoutExpired) as exc:
        print(json.dumps({'verdict':'ERROR','error':str(exc)},indent=2));return 2


if __name__=='__main__': sys.exit(main())
