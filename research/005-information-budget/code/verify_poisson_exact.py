from itertools import product
from fractions import Fraction as F
from collections import defaultdict
from math import comb, exp

def finite(L,B):
    groups=defaultdict(lambda:[0]*(L+1)); oracle=last=0
    den=B**(2*L+2)
    for xs in product(range(4), repeat=L):
        x=y=0; hist=[]
        for v in xs:
            x+=v&1; y+=(v>>1)&1; hist.append(min(x,y))
        m=min(x,y); mask=(1 if x==m else 0)|(2 if y==m else 0)
        weight=(B-1)**(2*L-sum(v.bit_count() for v in xs))
        rewards=[B*B*int(v&mask==mask) for v in xs]+[B**(2-mask.bit_count())]
        for i,v in enumerate(rewards): groups[tuple(hist)][i]+=weight*v
        oracle+=weight*max(rewards)
        j=max((i for i,h in enumerate(hist) if h>(hist[i-1] if i else 0)),default=L)
        last+=weight*rewards[j]
    scalar=sum(max(v) for v in groups.values())
    assert last<=scalar<=oracle
    w=max(1,int(L**.5)); p=F(1,B); r=2*p*(1-p)/(1-p*p)
    err=L*p*p + 2*w*r + L*w*r*r + L*r/w + p
    assert F(scalar-last,den)<=err
    return F(oracle-scalar,den),F(oracle-last,den),F(scalar-last,den)

def marked(n):
    count=0; reward2=0
    for marks in product((-1,1),repeat=n):
        d=0; lasttie=0; lastvis=0; visible=False
        for t,v in enumerate(marks,1):
            if d*v<0: lastvis=t; visible=True
            d+=v
            if d==0: lasttie=t
        A=visible and d!=0
        C=A and lastvis<=lasttie
        count+=C
        if A: reward2+=2 if not C else 1
    expected=2*sum(comb(2*k,k) for k in range(1,(n-1)//2+1))
    assert count==expected
    return F(count,2**n)

def limit(lam, N=200):
    prob=exp(-2*lam); g=0.; mass=prob
    for n in range(1,N+1):
        prob*=2*lam/n; mass+=prob
        g+=prob*sum(comb(2*k,k) for k in range(1,(n-1)//2+1))/2**n
    assert abs(mass-1)<1e-12
    t=exp(-lam); d=0.
    for k in range(1,N+1):
        t*=lam/k; d+=t*t
    return g,d,g/(g+d)

def finite_last_gap(L,B):
    p=1/B; r=2*p/(1+p); prob=(1-r)**L; g=0.
    for n in range(1,min(L,200)+1):
        prob*=(L-n+1)/n*r/(1-r)
        g+=prob*sum(comb(2*k,k) for k in range(1,(n-1)//2+1))/2**n
    return g

if __name__=='__main__':
    for n in range(15): marked(n)
    print('PASS: 15 exact walk count checks')
    for L in range(2,9):
        for B in (2,3,4,8):
            s,o,delta=finite(L,B)
            if B==4: print('finite',L,B,s,o,delta)
    print('PASS: 28 exact finite decision comparisons')
    for lam in (.25,.5,1,1.5,2,3,5): print('limit',lam,*limit(lam))
    for B in (16,64,256,1024,4096): print('conditional no-double last-visible gap',B,finite_last_gap(B,B))
