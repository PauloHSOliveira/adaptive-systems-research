from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from math import comb, exp


def exact(L, B):
    """One repeat, two rows, L fresh inserts and one final decision."""
    groups = defaultdict(lambda: [0]*(L+1))
    oracle = 0
    base = 0
    den = B**(2*L+2)
    for xs in product(range(4), repeat=L):
        c = [0,0]; hist = []
        for x in xs:
            c[0] += x&1; c[1] += (x>>1)&1
            hist.append(min(c))
        m = min(c)
        j = (1 if c[0]==m else 0) | (2 if c[1]==m else 0)
        weight = (B-1)**(2*L-sum(x.bit_count() for x in xs))
        fresh = B**(2-j.bit_count())
        rewards = [B*B*int((x&j)==j) for x in xs]
        g = groups[tuple(hist)]
        for i,r in enumerate(rewards+[fresh]): g[i] += weight*r
        oracle += weight*max(rewards+[fresh])
        base += weight*m*B*B
    s = F(base+sum(max(g) for g in groups.values()),den)
    o = F(base+oracle,den)
    p=F(1,B); a=1-p
    event = 2*comb(L,3)*p**3*a**(2*L-3) if L>=3 else F(0)
    lb = sum((2*(t-1)*(L-t)*p**3*a**(2*L-3)*(1-max(p,F(1,t-1))) for t in range(2,L)),F(0))
    loose = max(F(0),event*(1-p-F(3,L)))
    assert 0<=loose<=lb<=o-s
    def tail(z):
        if z<=2:
            return (1-a**(L+2-z))**2
        return sum((comb(L,k)*p**k*a**(L-k) for k in range(z-1,L+1)),F(0))**2
    env=sum((tail(z) for z in range(1,L+2)),F(0))
    shared=(1-p*p)*sum((comb(L,k)*comb(L-k,k)*p**(2*k)*a**(2*L-2*k)
                       for k in range(1,L//2+1)),F(0))
    assert env-o==shared
    return s,o,lb


def asymptotic(lam):
    # P(equal and positive), computed with a convergent Poisson sum.
    term=exp(-lam); tie=0.0
    for k in range(1, max(100,int(lam+20*lam**.5+20))):
        term *= lam/k; tie += term*term
    return lam**3*exp(-2*lam)/3, tie


def finite_bounds(L,B):
    p=1/B; a=1-p
    event=2*comb(L,3)*p**3*a**(2*L-3)
    lower=max(0.,event*(1-p-3/L))
    term=a**(2*L); shared=0.
    for k in range(L//2):
        term *= (L-2*k)*(L-2*k-1)/(k+1)**2*(p/a)**2
        shared += term
    return lower,(1-p*p)*shared

if __name__=='__main__':
    count=0
    for L in range(2,9):
        for B in (2,3,4,8):
            s,o,lb=exact(L,B); count+=1
            if B==4 and L in (3,4,6,8): print(L,B,s,o,o-s,lb)
    print('PASS',count,'exact finite configurations')
    for lam in (.25,.5,1,1.5,2,3,5):
        g,t=asymptotic(lam)
        print(lam,g,t,g/(g+t))
    for B in (16,64,256,1024,4096):
        print('lambda=1',B,*finite_bounds(B,B))
