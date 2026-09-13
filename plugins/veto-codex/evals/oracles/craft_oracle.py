#!/usr/bin/env python3
"""Source-only guardrails for a synthetic craft exercise. Not rendered acceptance."""
from html.parser import HTMLParser
from pathlib import Path
import json
import sys

class Inspector(HTMLParser):
    def __init__(self):
        super().__init__(); self.labels=[]; self.nodes=[]; self.text=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs); self.nodes.append((tag,a))
        if tag=='label': self.labels.append(a)
    def handle_data(self,data): self.text.append(data.strip())

def evaluate(path):
    parser=Inspector(); parser.feed(Path(path).read_text()); text=' '.join(parser.text)
    return {'functional_label':any(a.get('for')=='account' for a in parser.labels) and 'Receiving account' in text,
            'status_retained':any(a.get('id')=='review-status' and a.get('role')=='status' for _,a in parser.nodes) and 'Office review required' in text,
            'source_retained':'Original source' in text and 'Compare the supplied instruction with the prepared details.' in text,
            'disclosure_retained':'Synthetic rehearsal. Saving a review does not send a wire.' in text,
            'actions_retained':'Save office review' in text and 'Return a question' in text,
            'decorative_text_removed':'Workspace' not in text,
            'repetition_removed':'Review the receiving instructions below.' not in text}

if __name__=='__main__':
    try:
        results=evaluate(sys.argv[1]); print(json.dumps(results,indent=2)); sys.exit(0 if all(results.values()) else 1)
    except Exception as exc:
        print(json.dumps({'oracle_error':str(exc)})); sys.exit(2)
