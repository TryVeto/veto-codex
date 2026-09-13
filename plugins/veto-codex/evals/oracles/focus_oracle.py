#!/usr/bin/env python3
"""Execute a synthetic candidate only inside a disposable, isolated environment."""
from pathlib import Path
import importlib.util
import json
import sys
import tempfile

def evaluate(target):
    spec=importlib.util.spec_from_file_location('fixture_candidate',Path(target)/'store.py')
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory() as storage:
        a=module.submit(storage,'office_A','file_A','request_A',{'note':'the actual first contribution'})
        b=module.submit(storage,'office_A','file_B','request_B',{'note':'a separate file'})
        c=module.submit(storage,'office_B','file_A','request_C',{'note':'a separate office'})
        cases={'exact_retrieval':module.retrieve(storage,'office_A','file_A')==a,
               'separate_file':module.retrieve(storage,'office_A','file_B')==b,
               'separate_office':module.retrieve(storage,'office_B','file_A')==c}
        # Reimport to defeat an in-memory-only implementation.
        spec2=importlib.util.spec_from_file_location('fresh_fixture_candidate',Path(target)/'store.py')
        fresh=importlib.util.module_from_spec(spec2); spec2.loader.exec_module(fresh)
        cases['fresh_module_reads_saved_work']=fresh.retrieve(storage,'office_A','file_A')==a
    return cases

if __name__=='__main__':
    try:
        results=evaluate(sys.argv[1]); print(json.dumps(results,indent=2)); sys.exit(0 if all(results.values()) else 1)
    except Exception as exc:
        print(json.dumps({'oracle_error':str(exc)})); sys.exit(2)
