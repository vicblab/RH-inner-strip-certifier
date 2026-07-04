#!/usr/bin/env python3
from __future__ import annotations
import json, hashlib

def hash_obj(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

try:
    from flint import arb, acb, ctx
except Exception:
    arb = acb = ctx = None

def require_flint():
    if arb is None:
        raise SystemExit("python-flint is required: python -m pip install python-flint")

def set_prec(bits=120):
    require_flint(); ctx.prec = bits

class ADy2:
    """Second-order automatic differentiation in y for acb/arb boxes."""
    def __init__(self, v, d1=None, d2=None):
        require_flint()
        self.v=acb(v); self.d1=acb(0) if d1 is None else acb(d1); self.d2=acb(0) if d2 is None else acb(d2)
    def __add__(self,o):
        o=toADy2(o); return ADy2(self.v+o.v,self.d1+o.d1,self.d2+o.d2)
    __radd__=__add__
    def __neg__(self): return ADy2(-self.v,-self.d1,-self.d2)
    def __sub__(self,o): return self+(-toADy2(o))
    def __rsub__(self,o): return toADy2(o)+(-self)
    def __mul__(self,o):
        o=toADy2(o); return ADy2(self.v*o.v,self.d1*o.v+self.v*o.d1,self.d2*o.v+2*self.d1*o.d1+self.v*o.d2)
    __rmul__=__mul__
    def inv(self):
        v=self.v; return ADy2(1/v, -self.d1/(v*v), 2*self.d1*self.d1/(v*v*v)-self.d2/(v*v))
    def __truediv__(self,o): return self*toADy2(o).inv()
    def __rtruediv__(self,o): return toADy2(o)*self.inv()
    def exp(self):
        ev=self.v.exp(); return ADy2(ev, ev*self.d1, ev*(self.d1*self.d1+self.d2))
    def log(self):
        return ADy2(self.v.log(), self.d1/self.v, self.d2/self.v - self.d1*self.d1/(self.v*self.v))
    def pow_real(self,p): return (self.log()*p).exp()
    def __pow__(self,n):
        if n==0: return ADy2(1)
        if n<0: return (self**(-n)).inv()
        out=ADy2(1)
        for _ in range(n): out=out*self
        return out

def toADy2(x): return x if isinstance(x,ADy2) else ADy2(x)

def midrad(a,b):
    require_flint()
    a=arb(str(a)); b=arb(str(b)); return (a+b)/2 + arb(f"0 +/- {float((b-a)/2)}")

def mag(z):
    require_flint(); return float(acb(z).abs_upper())

def pow_pos(x,p):
    require_flint(); return (acb(x).log()*acb(p)).exp()

def cexp_i(theta):
    require_flint(); return (acb(0,1)*acb(theta)).exp()

def chi_cubic(y,Y):
    require_flint(); Y=arb(str(Y)); twoY=2*Y
    yy = y.v.real if hasattr(y,'v') else y
    if bool(yy <= Y): return ADy2(1) if hasattr(y,'v') else arb(1)
    if bool(yy >= twoY): return ADy2(0) if hasattr(y,'v') else arb(0)
    t=(y-ADy2(Y))/Y if hasattr(y,'v') else (y-Y)/Y
    return ADy2(1)-3*t*t+2*t*t*t if hasattr(y,'v') else 1-3*t*t+2*t*t*t

def eta_cubic(y,Y):
    return (ADy2(1) if hasattr(y,'v') else arb(1)) - chi_cubic(y,Y)
