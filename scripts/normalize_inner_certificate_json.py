#!/usr/bin/env python3
from __future__ import annotations
import json, hashlib, argparse
from decimal import Decimal, getcontext
from pathlib import Path
getcontext().prec=80
def h(o): return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest()

def D(x): return Decimal(str(x))
def safe(x):
    x=D(x)
    return Decimal(0) if x==0 else x*(Decimal(1)+Decimal('1e-12'))+Decimal(100)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('raw'); ap.add_argument('safe'); args=ap.parse_args()
    o=json.loads(Path(args.raw).read_text())
    if o.get('status')!='proved': raise SystemExit('raw JSON must have status=proved')
    for k in ['sector','side','C_value_upper','C_sigma_derivative_upper','coverage_hash','normalization_hash']:
        if k not in o: raise SystemExit(f'missing {k}')
    out=dict(o); out['C_value_upper_safe']=str(safe(o['C_value_upper'])); out['C_sigma_derivative_upper_safe']=str(safe(o['C_sigma_derivative_upper']))
    out['safe_normalization_rule']='safe=0 if raw=0 else raw*(1+1e-12)+100'; out['source_raw_file']=args.raw; out['proof_hash']=h(out)
    Path(args.safe).write_text(json.dumps(out,indent=2,sort_keys=True),encoding='utf-8'); print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
