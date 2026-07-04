#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math
from decimal import Decimal, getcontext
from inner_arb_common import *
getcontext().prec=80

def phase_core(w,y):
    # Removable phase C(w,y)=w^-2*(wy/2-log(1+wy/2)); Taylor on boxes containing 0.
    if bool(w.contains(0)):
        return y*y/8 - w*y**3/24 + w**2*y**4/64 - w**3*y**5/160 + w**4*y**6/384 - w**5*y**7/896
    u=w*y/2
    return (u-(1+u).log())/(w*w)

def theta_model(r,y):
    require_flint(); return y*y/8 + 2*arb.pi()*r*y

def D_integrands(sig,r,w,y,Y,fam):
    require_flint(); I=acb(0,1)
    ch=chi_cubic(y,Y)
    if fam == '-':
        A=(ADy2(2)+ADy2(w)*y).pow_real(-sig-2)
        A0=ADy2(arb(2)).pow_real(-sig-2)
        E=(I*acb(2*arb.pi()*r*y.v + phase_core(w,y).v)).exp()
        E0=(I*acb(theta_model(r,y.v))).exp()
        dA_sigma=-(ADy2(2)+ADy2(w)*y).log()*A
        dA0_sigma=-ADy2(arb(2)).log()*A0
    else:
        A=(ADy2(2)+ADy2(w)*y).pow_real(sig-3)
        A0=ADy2(arb(2)).pow_real(sig-3)
        E=(-I*acb(2*arb.pi()*r*y.v + phase_core(w,y).v)).exp()
        E0=(-I*acb(theta_model(r,y.v))).exp()
        dA_sigma=(ADy2(2)+ADy2(w)*y).log()*A
        dA0_sigma=ADy2(arb(2)).log()*A0
    val = ch*(A*E - A0*E0)
    dsig = ch*(dA_sigma*E - dA0_sigma*E0)
    return val, dsig

def y_boxes(Y,ny):
    out=[]
    for lo,hi,n in [(0.0,float(Y),ny//2),(float(Y),2*float(Y),ny-ny//2)]:
        for j in range(n):
            a=lo+(hi-lo)*j/n; b=lo+(hi-lo)*(j+1)/n; out.append((a,b))
    return out

def integrate_D(sig,r,w,fam,Y,ny):
    require_flint(); total=acb(0); total_s=acb(0)
    for a,b in y_boxes(Y,ny):
        y=ADy2(midrad(a,b),1,0); dy=arb(str(b-a))
        v,s=D_integrands(sig,r,w,y,Y,fam)
        total += v.v*acb(dy); total_s += s.v*acb(dy)
    return total,total_s

def prove(args):
    set_prec(args.prec)
    # This verifier certifies the compact-boundary integrals on finite tau boxes only.
    # It outputs a boundary hook JSON, not a complete bd sector.
    max0=Decimal(0); max1=Decimal(0); worst0=None; worst1=None
    for si in range(args.ns):
        sig=midrad(args.sigma_min+(args.sigma_max-args.sigma_min)*si/args.ns, args.sigma_min+(args.sigma_max-args.sigma_min)*(si+1)/args.ns)
        for ti in range(args.nt):
            lo=args.tau_min+(args.tau_max-args.tau_min)*ti/args.nt; hi=args.tau_min+(args.tau_max-args.tau_min)*(ti+1)/args.nt
            tau=midrad(lo,hi); w=1/tau.sqrt(); s=acb(sig,tau)
            alpha_lo=lo/(4*math.pi); alpha_hi=hi/(4*math.pi); root_hi=math.sqrt(hi)
            mmin=max(1,int(math.floor(alpha_lo-args.R*root_hi))-2); mmax=int(math.ceil(alpha_hi+args.R*root_hi))+2
            Gj=acb(0); Gjs=acb(0)
            for m in range(mmin,mmax+1):
                ma=arb(m); r=(ma-tau/(4*arb.pi()))/tau.sqrt()
                Dp,Dps=integrate_D(sig,r,w,'+',args.Y,args.ny)
                Dm,Dms=integrate_D(sig,r,w,'-',args.Y,args.ny)
                cp=s*(s-2); cm=(1-s)*(s+1); cps=2*s-2; cms=-2*s
                Gj += (cp*Dp + cm*Dm)/(m*m)
                Gjs += (cps*Dp + cp*Dps + cms*Dm + cm*Dms)/(m*m)
            Gj /= acb(4*arb.pi()*arb.pi()); Gjs /= acb(4*arb.pi()*arb.pi())
            # Project J-side to quotient side and include derivative of projection.
            Pi=acb(0,1)*tau/((1-s)*(s+1))
            Pis=Pi*(1/(1-s)-1/(s+1))
            R=Pi*Gj; Rs=Pis*Gj+Pi*Gjs
            scale=(tau**arb('1.5'))/tau.log()
            c0=Decimal(str(float((R.abs_upper()*scale).upper())))
            c1=Decimal(str(float((Rs.abs_upper()*scale).upper())))
            if c0>max0: max0=c0; worst0=(si,ti,mmin,mmax,str(c0))
            if c1>max1: max1=c1; worst1=(si,ti,mmin,mmax,str(c1))
    cov={'hook':'compact_boundary','tau_range':[args.tau_min,args.tau_max],'R':args.R,'Y':args.Y,'boxes':{'ns':args.ns,'nt':args.nt,'ny':args.ny}}
    norm={'side':'J_projected','projection':'Pi_Q and d_sigma Pi_Q included'}
    out={'status':'proved','sector':'bd','side':'J_projected','hook':'compact_boundary','method':'direct Arb compact-y boundary boxes with sigma derivative; finite tau range hook only','tau_range':[args.tau_min,args.tau_max],'sigma_range':[args.sigma_min,args.sigma_max],'C_value_upper':str(max0),'C_sigma_derivative_upper':str(max1),'coverage_hash':hash_obj(cov),'normalization_hash':hash_obj(norm),'worst_value_box':worst0,'worst_sigma_box':worst1}
    out['proof_hash']=hash_obj(out)
    print(json.dumps(out,indent=2,sort_keys=True,default=str))

def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='cmd',required=True)
    q=sub.add_parser('prove')
    q.add_argument('--sigma-min',type=float,default=0.49); q.add_argument('--sigma-max',type=float,default=0.51)
    q.add_argument('--tau-min',type=float,default=10); q.add_argument('--tau-max',type=float,default=25)
    q.add_argument('--Y',type=float,default=128); q.add_argument('--R',type=float,default=4)
    q.add_argument('--ns',type=int,default=2); q.add_argument('--nt',type=int,default=4); q.add_argument('--ny',type=int,default=64)
    q.add_argument('--prec',type=int,default=120)
    args=ap.parse_args(); prove(args)
if __name__=='__main__': main()
