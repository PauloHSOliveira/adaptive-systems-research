from fractions import Fraction as F
from itertools import product
from math import comb

def exact(L,B):
    p=F(1,B);r=2*p/(1+p)
    gap=F(0); g=F(0); tie=F(0)
    for xs in product((0,1,2), repeat=L):
        c=[0,0]; last=None; lasttie=0; vis=[]
        n=0
        for i,x in enumerate(xs,1):
            m=min(c)
            if x: c[x-1]+=1;n+=1
            if min(c)>m: last=x;vis.append(i)
            if c[0]==c[1]: lasttie=i
        w=(1-r)**(L-n)*(r/2)**n
        m=min(c); j=[i for i in range(2) if c[i]==m]
        fresh=p**len(j)
        oracle=F(1) if m>0 and len(j)==1 else fresh
        lastval=fresh if last is None else F(int(len(j)==1 and last==j[0]+1))
        gap+=w*(oracle-lastval)
        g+=w*F(int(m>0 and len(j)==1 and max(vis,default=0)<=lasttie),2)
        tie+=w*int(m>0 and len(j)==2)
    assert gap==g+p*p*tie
    return gap,g,tie

def formula(L,B):
    p=1/B;r=2*p/(1+p);prob=(1-r)**L;g=tie=0.
    for n in range(1,min(L,200)+1):
        prob*=(L-n+1)/n*r/(1-r)
        g+=prob*sum(comb(2*k,k) for k in range(1,(n-1)//2+1))/2**n
        if n%2==0: tie+=prob*comb(n,n//2)/2**n
    return g, p*p*tie, g+p*p*tie

if __name__=='__main__':
    for L in range(2,9):
        for B in (2,3,4,8):
            x,g,tie=exact(L,B)
            assert abs(float(x)-formula(L,B)[2])<1e-12
    print('PASS: 28 exact conditional-gap identities')
    for B in (16,64,256,1024,4096):print(B,*formula(B,B))
