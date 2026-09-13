"""Synthetic local JSON store: intentionally broken retrieval for evaluation."""
import json
import re
from pathlib import Path

def _path(root, office, file):
    if not all(re.fullmatch(r'[A-Za-z0-9_-]+',v) for v in (office,file)):
        raise ValueError('Invalid synthetic identifier')
    return Path(root)/f'{office}--{file}.json'

def submit(root, office, file, request, contribution):
    row={'office':office,'file':file,'request':request,'contribution':contribution}
    Path(root).mkdir(parents=True,exist_ok=True)
    _path(root,office,file).write_text(json.dumps(row))
    return row

def retrieve(root, office, file):
    return {'office':office,'file':file,'request':'demo-request','contribution':{'note':'demo material'}}
