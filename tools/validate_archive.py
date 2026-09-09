"""Read-only integrity checks; no LSST imports, network or science processing."""
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

def check(condition, message):
    if not condition:
        errors.append(message)

manifest = json.loads((ROOT/'data/input_exposures.json').read_text())
exposures = manifest['exposures']
check(len(exposures) == 32, 'Expected 32 exposures')
check(len({x['visit'] for x in exposures}) == 32, 'Duplicate visit')
check(Counter((x['field'],x['band']) for x in exposures) ==
      Counter({(f,b):4 for f in ['ClusterRot','FRB'] for b in 'ugri'}), 'Field/band coverage')
for entry in exposures:
    check(entry['ccd_ids'] == list(range(36)), f"CCD coverage: {entry['visit']}")
    check(entry['fits_extensions'] == list(range(1,37)), f"FITS HDUs: {entry['visit']}")
    product = str(entry['visit']) + 'p'
    check(entry['cadc_input_product_id'] == product, 'Wrong CADC input ID')
    check(entry['download_url'].endswith('/' + product + '.fits.fz'), 'Wrong CADC URL')
    check(bool(re.fullmatch(r'md5:[0-9a-f]{32}',entry['cadc_current_checksum'])), 'Invalid checksum')
urls=(ROOT/'data/download_urls.txt').read_text().splitlines()
check(urls == [e['download_url'] for e in exposures], 'URL list differs from manifest')

records = json.loads((ROOT/'provenance/source_inventory.json').read_text())
for record in records:
    f = ROOT/record['path']
    check(f.is_file(), 'Missing archived file: '+record['path'])
    if f.is_file():
        check(hashlib.sha256(f.read_bytes()).hexdigest() == record['archived_sha256'],
              'Archive hash mismatch: '+record['path'])

syntax_count=0
for folder in ('processing','qc','tools'):
    for f in (ROOT/folder).rglob('*'):
        if f.is_file() and re.search(r'\.py(?:~\d+)?$',f.name):
            try: ast.parse(f.read_text(encoding='utf-8'),filename=str(f))
            except SyntaxError as e: errors.append(f'Syntax: {f.relative_to(ROOT)}:{e.lineno}: {e.msg}')
            syntax_count += 1

# Public files must not retain credentials or private source storage locations.
for f in ROOT.rglob('*'):
    if not f.is_file() or '.git' in f.parts or '__pycache__' in f.parts:
        continue
    check(f.stat().st_size < 10_000_000, 'Unexpected large file: '+str(f.relative_to(ROOT)))
    if f.suffix in ('.pyc',): continue
    data=f.read_text(encoding='utf-8',errors='replace')
    patterns=[r'/(?:gpfs|oscar|storage2)/', r'-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----',
              r'gh[pousr]_[A-Za-z0-9]{30,}',r'github_pat_[A-Za-z0-9_]{30,}']
    # Pattern literals in this validator are not matches to actual private data.
    for pattern in patterns:
        check(not re.search(pattern,data), 'Sensitive/site content: '+str(f.relative_to(ROOT)))

if errors:
    print('\n'.join(errors))
    sys.exit(1)
print(f'PASS: 32 visits, 1152 CCD records; {len(records)} source checksums; {syntax_count} Python syntax checks.')
print('Scientific end-to-end reproduction is NOT tested. Read provenance/KNOWN_GAPS.md.')
