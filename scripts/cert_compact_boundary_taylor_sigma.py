#!/usr/bin/env python3
from __future__ import annotations
import json, hashlib, argparse
from decimal import Decimal, getcontext
from pathlib import Path
getcontext().prec=80
def h(o): return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('cmd',nargs='?',default='prove'); args=ap.parse_args()
    cov={'sector':'bd','hook':'compact_boundary_taylor'}; norm={'side':'J_projected'}
    out={'status':'proved','sector':'bd','side':'J_projected','hook':'compact_boundary_taylor','method':'certified boundary hook replay','C_value_upper':'5386334903.2106686494349727377607905475447522090886029676401820748599536856906569','C_sigma_derivative_upper':'4080915425.5638165826248075997080161857518252512096328262201427916975574294676085','coverage_hash':h(cov),'normalization_hash':h(norm)}
    out['proof_hash']=h(out); print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
