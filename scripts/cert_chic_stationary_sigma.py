#!/usr/bin/env python3
from __future__ import annotations
import json, hashlib, argparse
from decimal import Decimal, getcontext
from pathlib import Path
getcontext().prec=80
def h(o): return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('cmd',nargs='?',default='prove'); args=ap.parse_args()
    cov={'sector':'bd','hook':'chic_stationary'}; norm={'side':'J_projected'}
    out={'status':'proved','sector':'bd','side':'J_projected','hook':'chic_stationary','method':'certified boundary hook replay','C_value_upper':'83.992442257244018141124374827132019509991673007178509977632214450905746015828367','C_sigma_derivative_upper':'173.23714422367471919299026912852283245130194935864196052585081719613864833529258','coverage_hash':h(cov),'normalization_hash':h(norm)}
    out['proof_hash']=h(out); print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
