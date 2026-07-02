#!/usr/bin/env python3
from decimal import Decimal, getcontext
getcontext().prec = 80
C = Decimal('387983784453.34570013486357394399212036290592556640627403482826815918742177195616')
g0 = Decimal('0.2')
A = C/g0
low = Decimal(1); high = Decimal('1e40')
while high/(high.ln()) < 2*A:
    high *= 10
for _ in range(300):
    mid=(low+high)/2
    if mid/(mid.ln()) > 2*A:
        high=mid
    else:
        low=mid
T = high*high
print('C_inner =', C)
print('g0 =', g0)
print('minimal_T_approx =', T)
print('log10_minimal_T =', T.log10())
print('clean_power_of_ten_height = 1e29')
for p in [28,29,30]:
    TT=Decimal(10)**p
    ok=TT.sqrt() > A*TT.ln()
    print(f'T=1e{p}:', ok)
