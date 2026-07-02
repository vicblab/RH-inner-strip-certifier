#!/usr/bin/env python3
from __future__ import annotations
import json, hashlib, argparse
from decimal import Decimal, getcontext
from pathlib import Path
getcontext().prec=80
def h(o): return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest()

def D(x): return Decimal(str(x))
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--inputs',nargs='+',required=True); ap.add_argument('--bracket',required=True); ap.add_argument('--height',required=True); ap.add_argument('--g0',default='0.2'); ap.add_argument('--output',required=True); args=ap.parse_args()
    br=json.loads(Path(args.bracket).read_text())
    if br.get('status')!='proved': raise SystemExit('bracket not proved')
    sectors=['band','bd','far','end','nonstat','floor','core']; by={}; deps={}
    import glob, math
    paths=[]
    for pat in args.inputs: paths += glob.glob(pat)
    for p in sorted(set(paths)):
        o=json.loads(Path(p).read_text()); sec=o.get('sector')
        if sec in sectors:
            c0=D(o['C_value_upper_safe']); c1=D(o['C_sigma_derivative_upper_safe']); by[sec]=(c0,c1); deps[sec]={'file':p,'side':o.get('side'),'proof_hash':o.get('proof_hash'),'coverage_hash':o.get('coverage_hash'),'normalization_hash':o.get('normalization_hash'),'C_value_upper_safe':str(c0),'C_sigma_derivative_upper_safe':str(c1)}
    miss=[s for s in sectors if s not in by]
    if miss: raise SystemExit('missing sector certificates: '+str(miss))
    C0=sum(v[0] for v in by.values()); C1=sum(v[1] for v in by.values()); C=(C0*C0+C1*C1).sqrt(); T=D(args.height); g0=D(args.g0); ok=math.sqrt(float(T)) > float(C/g0)*math.log(float(T))
    out={'status':'inner_full_certificate' if ok else 'inner_certificate_height_failed','u0':br.get('u0'),'g0_bracket_vector_lower':str(g0),'height_tested':str(T),'height_condition':'sqrt(T) > (C_inner/g0)*log(T)','height_condition_holds':ok,'C_even_residual_upper':str(C0),'C_sigma_residual_upper':str(C1),'C_inner_vector_upper':str(C),'bracket_certificate':{'file':args.bracket,'proof_hash':br.get('proof_hash')},'sectors':deps}
    out['proof_hash']=h(out); Path(args.output).write_text(json.dumps(out,indent=2,sort_keys=True)); print(json.dumps(out,indent=2,sort_keys=True))
    if not ok: raise SystemExit(2)
if __name__=='__main__': main()
