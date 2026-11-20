#!/usr/bin/env python3
"""Computer-assisted *exact rational interval* proof of d(width)/du < 0.

u=(2alpha-1)^2, p=2r-1, F4(p,u)=0 -> lower root,
F3(p,u)=0 -> upper root. Both roots are unique and strictly increasing.

Method: for each slab [i/N,(i+1)/N], certify strict rational root
brackets at both endpoints, then interval-evaluate dp4/du-dp3/du
on the encompassing root rectangles. Interval arithmetic is implemented
with fractions.Fraction (no floating point in certified inequalities).
Floating point scipy.brentq proposes endpoints only; all proposed bounds
and resulting interval inequalities are checked with exact fractions.
"""
from fractions import Fraction as F
from math import floor,ceil
from dataclasses import dataclass
import argparse
from scipy.optimize import brentq


@dataclass(frozen=True)
class I:
    lo:F
    hi:F
    def __init__(self,lo,hi=None):
        object.__setattr__(self,'lo',F(lo))
        object.__setattr__(self,'hi',F(hi if hi is not None else lo))
        assert self.lo<=self.hi
    @staticmethod
    def wrap(a):return a if isinstance(a,I) else I(a)
    def __add__(self,b):
        b=I.wrap(b);return I(self.lo+b.lo,self.hi+b.hi)
    __radd__=__add__
    def __neg__(self):return I(-self.hi,-self.lo)
    def __sub__(self,b):return self+-I.wrap(b)
    def __rsub__(self,b):return I.wrap(b)+-self
    def __mul__(self,b):
        b=I.wrap(b);x=[self.lo*b.lo,self.lo*b.hi,self.hi*b.lo,self.hi*b.hi]
        return I(min(x),max(x))
    __rmul__=__mul__
    def __truediv__(self,b):
        b=I.wrap(b)
        if b.lo<=0<=b.hi:raise ZeroDivisionError((b.lo,b.hi))
        return self*I(1/b.hi,1/b.lo)
    def __pow__(self,n):
        assert isinstance(n,int) and n>=0
        if n==0:return I(1)
        if n%2==0 and self.lo<0<self.hi:return I(0,max(self.lo**n,self.hi**n))
        if n%2==0:return I(min(self.lo**n,self.hi**n),max(self.lo**n,self.hi**n))
        return I(self.lo**n,self.hi**n)


def F3(p,u):return p**4+(1-2*u)*p**3+(1-2*u+2*u*u)*p*p+p-2

def F4(p,u):return p**4+(1+u)*p**3+(1-u*u)*p*p+(1-3*u)*p-1

def dp3(p,u):
    numerator=2*p*p*(p+1-2*u)
    denominator=4*p**3+3*(1-2*u)*p*p+2*(1-2*u+2*u*u)*p+1
    return numerator/denominator

def dp4(p,u):
    numerator=p*(3+2*u*p-p*p)
    denominator=4*p**3+3*(1+u)*p*p+2*(1-u*u)*p+1-3*u
    return numerator/denominator


def root_enclosure(k, u: F, precision:int=10**12, pad:int=1000):
    f=F3 if k==3 else F4
    uf=float(u)
    if u == 1:return F(1),F(1)
    root=brentq(lambda p: float(f(p,uf)),.0,1.,xtol=1e-14)
    low=max(0,floor(root*precision)-pad)
    high=min(precision,ceil(root*precision)+pad)
    L=F(low,precision); H=F(high,precision)
    assert f(L,u) <= 0 <= f(H,u), ('invalid proposed root bracket',k,u,root,L,H,f(L,u),f(H,u))
    return L,H


def certify(N):
    root_lows={};root_highs={}
    smallest=None
    for i in range(N):
        ul,uh=F(i,N),F(i+1,N)
        l4,_=root_enclosure(4,ul);_,h4=root_enclosure(4,uh)
        l3,_=root_enclosure(3,ul);_,h3=root_enclosure(3,uh)
        P4=I(l4,h4);P3=I(l3,h3); U=I(ul,uh)
        D4=dp4(P4,U);D3=dp3(P3,U)
        margin=D4.lo-D3.hi
        if margin <= 0:return False, i, float(margin)
        if smallest is None or margin<smallest:smallest=margin
    return True,N,float(smallest)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--intervals',type=int,default=512)
    args=parser.parse_args();print(certify(args.intervals))