#!/usr/bin/env python3
from __future__ import annotations
import json, hashlib, argparse
from decimal import Decimal, getcontext
from pathlib import Path
getcontext().prec=80
def h(o): return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest()

def D(x): return Decimal(str(x))
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--inputs',nargs='+',required=True); ap.add_argument('--output',required=True); args=ap.parse_args()
    deps={}; C0=Decimal(0); C1=Decimal(0)
    for p in args.inputs:
        o=json.loads(Path(p).read_text()); name=o.get('hook') or Path(p).stem
        c0=D(o.get('C_value_upper_safe',o.get('C_value_upper'))); c1=D(o.get('C_sigma_derivative_upper_safe',o.get('C_sigma_derivative_upper')))
        C0+=c0; C1+=c1; deps[name]={'file':p,'proof_hash':o.get('proof_hash'),'C_value_upper_safe':str(c0),'C_sigma_derivative_upper_safe':str(c1)}
    cov={'boundary_hooks':sorted(deps)}; norm={'sector':'bd','side':'J_projected'}
    out={'status':'proved','sector':'bd','side':'J_projected','method':'strict_boundary_hook_sum_merger','C_value_upper_safe':str(C0),'C_sigma_derivative_upper_safe':str(C1),'dependencies':deps,'coverage_hash':h(cov),'normalization_hash':h(norm)}
    out['proof_hash']=h(out); Path(args.output).write_text(json.dumps(out,indent=2,sort_keys=True)); print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
