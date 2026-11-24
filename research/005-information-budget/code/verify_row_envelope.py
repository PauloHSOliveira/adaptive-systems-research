"""Exact finite check of a mathematical collision-model envelope.
No external system, network, or production data is used.
"""
from fractions import Fraction as F
from functools import lru_cache
from math import comb
from itertools import product

def upper_tail(M,K,R,B,z):
    p=F(1,B); a=1-p; L=M-K
    if z<=0: return F(1)
    if z>M: return F(0)
    if z<=K+1:
        t=1-a**(M-z+1)
    else:
        t=sum((comb(L,i)*p**i*a**(L-i) for i in range(z-K,L+1)),F(0))
    return t**R

def optimal(M,K,R,B,cp,threshold=None):
    N=M
    pats=tuple(product((0,1),repeat=R*N))
    weights=tuple((B-1)**(R*N-sum(h)) for h in pats)
    @lru_cache(None)
    def estimate(c,h):
        return min(sum(c[i]*pats[h][R*i+j] for i in range(N)) for j in range(R))
    @lru_cache(None)
    def dp(c,belief):
        t=sum(c)
        if t==M:
            return sum(weights[h]*(estimate(c,h) if threshold is None else int(estimate(c,h)>=threshold)) for h in belief)
        best=-1
        unused=False
        for i in range(N):
            if c[i]==0:
                if unused: continue
                unused=True
            nc=list(c); nc[i]+=1; nc=tuple(nc)
            if t+1-sum(v>0 for v in nc)>K: continue
            if t+1 in cp:
                g={}
                for h in belief: g.setdefault(estimate(nc,h),[]).append(h)
                val=sum(dp(nc,tuple(v)) for v in g.values())
            else:
                val=dp(nc,belief)
            best=max(best,val)
        assert best>=0
        return best
    return F(dp((0,)*N,tuple(range(len(pats)))),B**(R*N)*(M if threshold is None else 1))

def main():
    one=0
    for M in range(1,6):
        for B in (2,3,4):
            for K in range(M):
                cp=tuple(range(1,M))
                for z in range(1,M+1):
                    assert optimal(M,K,1,B,cp,z)==upper_tail(M,K,1,B,z)
                    one+=1
                p=F(1,B); L=M-K
                expected=(L*p+K-(1-p)**(L+1)*(1-(1-p)**K)/p)/M
                assert optimal(M,K,1,B,cp)==expected
                one+=1
    two=0
    for M in range(2,5):
        for B in (2,3):
            for K in range(M):
                cp=tuple(range(1,M))
                a=optimal(M,K,2,B,cp)
                u=sum(upper_tail(M,K,2,B,z) for z in range(1,M+1))/M
                assert a<=u
                two+=1
                for z in range(1,M+1):
                    assert optimal(M,K,2,B,cp,z)<=upper_tail(M,K,2,B,z)
                    two+=1
                if K and M==4:
                    print(M,B,K,a,u)
    print("PASS:",one,"one-row and",two,"two-row comparisons")
if __name__=="__main__":
    main()
