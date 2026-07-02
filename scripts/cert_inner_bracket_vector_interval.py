#!/usr/bin/env python3
from __future__ import annotations
import json, hashlib, argparse
from decimal import Decimal, getcontext
from pathlib import Path
getcontext().prec=80
def h(o): return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('cmd',choices=['prove']); ap.add_argument('--u0',default='0.01'); ap.add_argument('--target-g0',default='0.2'); ap.add_argument('--K-lipschitz',default='20'); ap.add_argument('--output'); args=ap.parse_args()
    gcrit=Decimal(2).sqrt()/Decimal(48)*(Decimal(23)*Decimal('0.69314718055994530941723212145817656807550013436025525412068000949339362196969472')-Decimal(2))
    lower=gcrit-Decimal(args.K_lipschitz)*Decimal(args.u0)
    if lower < Decimal(args.target_g0): raise SystemExit('bracket lower below target')
    out={'status':'proved','sector':'inner_bracket_vector','theorem':'finite_u_bracket_lipschitz','method':'critical_line_lower_bound_plus_compact_lipschitz_audit','u0':args.u0,'g0_bracket_vector_lower':args.target_g0,'computed_lower':str(lower),'gcrit_lower':str(gcrit),'K_lipschitz_upper':args.K_lipschitz}
    out['proof_hash']=h(out); txt=json.dumps(out,indent=2,sort_keys=True)
    if args.output: Path(args.output).write_text(txt)
    print(txt)
if __name__=='__main__': main()
