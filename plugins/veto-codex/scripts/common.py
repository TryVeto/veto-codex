"""Local file helpers. Integrity checks, not a hostile-filesystem sandbox."""
from __future__ import annotations
import hashlib
import json
import re
import stat
from pathlib import Path, PurePosixPath

MAX_BYTES = 64 * 1024 * 1024
HEX256 = re.compile(r'^[0-9a-f]{64}$')

def ordinary_path(path: Path, *, directory: bool = False) -> Path:
    path = path.absolute()
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError('Symlinks and paths through symlinks are not accepted.')
    mode = path.stat().st_mode
    if directory:
        if not stat.S_ISDIR(mode):
            raise ValueError('Expected a directory.')
    elif not stat.S_ISREG(mode):
        raise ValueError('Expected an ordinary file.')
    return path

def local_file(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or '\\' in relative or ':' in relative:
        raise ValueError('Evidence path must be a relative POSIX path.')
    p = PurePosixPath(relative)
    if p.is_absolute() or '..' in p.parts or not p.parts:
        raise ValueError('Evidence path escapes its root.')
    root = ordinary_path(root, directory=True)
    return ordinary_path(root.joinpath(*p.parts))

def digest(path: Path) -> str:
    path = ordinary_path(path)
    if path.stat().st_size > MAX_BYTES:
        raise ValueError('File exceeds the 64 MiB verification limit.')
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def _unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'Duplicate JSON key: {key}')
        result[key] = value
    return result

def load_json(path: Path) -> dict:
    path = ordinary_path(path)
    if path.stat().st_size > 2 * 1024 * 1024:
        raise ValueError('JSON input exceeds 2 MiB.')
    value = json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=_unique_object,
                       parse_constant=lambda x: (_ for _ in ()).throw(ValueError('Nonfinite JSON number.')))
    if not isinstance(value, dict):
        raise ValueError('Expected a JSON object.')
    return value

def nonempty(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{label} must be a nonempty string.')
    return value

def exact_keys(obj: object, required: set[str], optional: set[str], label: str) -> dict:
    if not isinstance(obj, dict):
        raise ValueError(f'{label} must be an object.')
    missing, extra = required - obj.keys(), obj.keys() - required - optional
    if missing or extra:
        raise ValueError(f'{label}: missing={sorted(missing)}, unexpected={sorted(extra)}')
    return obj
