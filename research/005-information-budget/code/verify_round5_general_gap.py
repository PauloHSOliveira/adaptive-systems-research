"""Exact rational checks for the single-repeat row-feedback comparator."""
from itertools import product
from fractions import Fraction as F
from collections import defaultdict
from math import comb

def check(R, L, B):
    p, a, M = F(1,B), F(B-1,B), L+1
    vecs = list(product((0,1), repeat=R))
    row = gap = F(0)
    states = defaultdict(lambda:[F(0)]*(L+1))
    for vs in product(vecs, repeat=L):
        ones = sum(map(sum, vs))
        wt = p**ones * a**(R*L-ones)
        c = tuple(map(sum, zip(*vs)))
        m = min(c)
        J = [j for j in range(R) if c[j]==m]
        inc = [int(all(v[j] for j in J)) for v in vs]
        fresh = p**len(J)
        alpha = max([fresh]+inc)
        row += wt*(m+alpha)
        if m>0 and not any(inc):
            gap += wt*(1-fresh)
        hist = tuple(min(map(sum, zip(*vs[:t]))) for t in range(1,L+1))
        for k, d in enumerate(inc+[fresh]):
            states[hist][k] += wt*(m+d)
    scalar = sum(max(vals) for vals in states.values())
    tails = [1-a**(M-z+1) if z<=2 else sum(F(comb(L,k))*p**k*a**(L-k) for k in range(z-1,L+1)) for z in range(1,M+1)]
    env = sum(t**R for t in tails)
    assert env-row == gap, (R,L,B,env,row,gap)
    if R==2 and L==2:
        assert (row-scalar)/M == 2*p**4*a**2/3
        assert gap/M == 2*p**2*a**2*(1-p*p)/3
    return scalar/M,row/M,env/M

if __name__=='__main__':
    for B in range(2,11):
        print('R=2 L=2 B=',B, *map(str,check(2,2,B)))
    for R,L,B in product(range(1,4),range(1,4),range(2,5)):
        check(R,L,B)
    print('PASS: 9 small-instance checks and 27 general-gap checks (overlapping grids).')
