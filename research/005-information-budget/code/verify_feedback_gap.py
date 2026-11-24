"""Exact finite mathematical collision model; no external system is used."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import comb


def envelope(M,R,B,z):
    p=F(1,B); a=1-p; L=M-1
    return ((1-a**(M-z+1)) if z<=2 else sum((comb(L,i)*p**i*a**(L-i) for i in range(z-1,L+1)), F(0)))**R


def oracle_tails(M,R,B):
    # Full row observation relaxation, one repeat maximum.
    L=M-1; p=F(1,B); den=B**(R*L)
    tails=[F(0) for _ in range(M)]
    for bits in product((0,1),repeat=R*L):
        rows=[sum(bits[R*i+j] for i in range(L)) for j in range(R)]
        m=min(rows); S=[j for j in range(R) if rows[j]==m]
        covered=any(all(bits[R*i+j] for j in S) for i in range(L))
        inc=F(1) if covered else p**len(S)
        w=F((B-1)**(R*L-sum(bits)),den)
        for z in range(1,M+1):
            tails[z-1]+=w*(1 if z<=m else inc if z==m+1 else 0)
    return tails


def scalar_optimum(M,R,B,threshold=None):
    # Finite perfect-recall scalar observation model. Fresh keys exchangeable.
    patterns=tuple(product((0,1),repeat=R*M))
    weights=tuple((B-1)**(R*M-sum(h)) for h in patterns)
    @lru_cache(None)
    def estimate(c,h):
        return min(sum(c[i]*patterns[h][R*i+j] for i in range(M)) for j in range(R))
    @lru_cache(None)
    def dp(c,belief):
        t=sum(c)
        if t==M:
            return sum(weights[h]*(estimate(c,h) if threshold is None else int(estimate(c,h)>=threshold)) for h in belief)
        best=-1; usedfresh=False
        for i in range(M):
            if c[i]==0:
                if usedfresh: continue
                usedfresh=True
            nc=list(c); nc[i]+=1; nc=tuple(nc)
            if t+1-sum(x>0 for x in nc)>1: continue
            if t+1==M:
                val=dp(nc,belief)
            else:
                groups={}
                for h in belief: groups.setdefault(estimate(nc,h),[]).append(h)
                val=sum(dp(nc,tuple(v)) for v in groups.values())
            best=max(best,val)
        assert best>=0
        return best
    return F(dp((0,)*M,tuple(range(len(patterns)))),B**(R*M)*(M if threshold is None else 1))


def main():
    n=0; gap1=0; gap2=0
    for M in range(2,6):
        for R in (1,2,3):
            if R*M>12: continue
            for B in (2,3,4):
                o=oracle_tails(M,R,B)
                e=[envelope(M,R,B,z) for z in range(1,M+1)]
                s=[scalar_optimum(M,R,B,z) for z in range(1,M+1)]
                sm=scalar_optimum(M,R,B)
                om=sum(o)/M; em=sum(e)/M
                assert all(a<=b<=c for a,b,c in zip(s,o,e))
                assert sm<=om<=em
                if R==1:
                    assert sm==om==em and s==o==e
                n+=M+1
                gap1+=int(sm<om);gap2+=int(om<em)
                print(M,R,B,sm,om,em)
    print('CHECKS',n,'STRICT_SCALAR_ORACLE_MEAN',gap1,'STRICT_ORACLE_ENVELOPE_MEAN',gap2)
    for B in range(2,11):
        p=F(1,B); a=1-p
        sm=scalar_optimum(3,2,B)
        om=sum(oracle_tails(3,2,B))/3
        em=sum(envelope(3,2,B,z) for z in range(1,4))/3
        assert om-sm==2*p**4*a*a/3
        assert em-om==2*p*p*a*a*(1-p*p)/3
    print('PASS: 18 closed-form gap comparisons')
if __name__=='__main__': main()
