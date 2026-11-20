#!/usr/bin/env python3
"""Exact arithmetic certificates for particular finite-window HMM comparisons.

All probabilities are represented as integer counts over a common denominator.
Only the fixed 2-state HMM and one-step decision loss are considered.
"""
from fractions import Fraction
from collections import defaultdict
import json


def value(alpha: Fraction, r: Fraction, s: int, w: int):
    if not (0 < s < w and s%2 and w%2):raise ValueError('Odd 1<=s<w required')
    an, ad = alpha.numerator, alpha.denominator
    rn, rd = r.numerator, r.denominator
    # first timestep: state prior 1/2, emission denominator ad
    d={(0,0,0):an,(0,0,1):ad-an,(1,int(s==w),0):ad-an,(1,int(s==w),1):an}
    # initial event belongs to short segment iff w=s, which is excluded, so short count 0
    assert w>s
    for i in range(1,w):
        nxt=defaultdict(int)
        for (count,longshort,state),n in d.items():
            for next_state,tnum in ((state,rn),(1-state,rd-rn)):
                n0=n*tnum
                plus = an if next_state==0 else ad-an
                minus= ad-an if next_state==0 else an
                nxt[(count,longshort,next_state)] += n0*plus
                nxt[(count+1,longshort+(1 if i>=w-s else 0),next_state)] += n0*minus
        d=nxt
    denom=2*ad*(rd*ad)**(w-1)
    f=Fraction((2*an-ad)*(2*rn-rd), ad*rd)
    sum_abs=0; sums=[0,0]; massdiff=[[0,0] for _ in range(2)]
    disagreement_count=0
    nonzero_reasons=[]
    for total in range(w+1):
        for short in range(s+1):
            a=d.get((total,short,0),0);b=d.get((total,short,1),0)
            if a+b==0:continue
            S=short <= s//2;L=total<=w//2
            if S==L:continue
            idx=0 if S else 1
            # loss_short - loss_long = -future sign if short+long-, +future sign if short-long+
            signed=(b-a) if S else (a-b)
            sum_abs+=abs(signed)
            sums[idx]+=signed
            disagreement_count+=a+b
            if signed:
                nonzero_reasons.append((total,short,int(signed>0)))
    V=f*Fraction(sum_abs-sum(abs(x) for x in sums),2*denom)
    assert V >=0,(V,s,w)
    return V, Fraction(disagreement_count,denom), len(nonzero_reasons)


def main():
    cases=[]
    for alpha, r, windows, short in [
        (Fraction(4,5),Fraction(9,10),range(3,32,2),1),
        (Fraction(4,5),Fraction(99,100),range(3,12,2),1),
        (Fraction(4,5),Fraction(99,100),[11],5),
        (Fraction(3,5),Fraction(19,20),range(3,12,2),1),
        (Fraction(3,5),Fraction(19,20),[11],5),
    ]:
        entries=[]
        for w in windows:
            V,pm,number=value(alpha,r,short,w)
            entries.append({'s':short,'w':w,'V_exact':str(V),'V':float(V),'P_disagree':float(pm),'nonzero_cells':number})
            print(f'a={str(alpha)} r={str(r)} s={short} w={w} V={float(V):.12f}')
        cases.append({'alpha':str(alpha),'r':str(r),'rows':entries})
    v5=value(Fraction(4,5),Fraction(9,10),1,5)[0]
    assert v5 == Fraction(84231,7812500),(v5,'expected exact from previous audit')
    assert all(v5>value(Fraction(4,5),Fraction(9,10),1,w)[0] for w in range(11,31,2))
    v_s5=value(Fraction(4,5),Fraction(99,100),5,11)[0]
    assert v_s5>0
    assert all(value(Fraction(4,5),Fraction(99,100),1,w)[0]==0 for w in range(3,12,2))
    with open('/mnt/data/hdate2_round6/exact_certificates.json','w') as f:json.dump({'cases':cases},f,indent=2)
    print('\nALL EXACT RATIONAL ASSERTIONS PASSED')

if __name__=='__main__':main()


def risks(alpha: Fraction, r: Fraction, s:int, w:int):
    '''Exact full Bayes risks with and without |m| (for each pair of actions).'''
    an,ad=alpha.numerator,alpha.denominator;rn,rd=r.numerator,r.denominator
    state={(0,0,0):an,(0,0,1):ad-an,(1,0,0):ad-an,(1,0,1):an}
    for i in range(1,w):
        tmp=defaultdict(int)
        for (k,ks,hidden),mass in state.items():
            for dest,tp in ((hidden,rn),(1-hidden,rd-rn)):
                plus=an if dest==0 else ad-an
                minus=ad-an if dest==0 else an
                tmp[(k,ks,dest)] += mass*tp*plus
                tmp[(k+1,ks+(i>=w-s),dest)] += mass*tp*minus
        state=tmp
    D=2*ad*(rd*ad)**(w-1)
    factor=Fraction((2*an-ad)*(2*rn-rd),ad*rd)
    total_loss=Fraction(0); abs_fine=Fraction(0)
    groups=defaultdict(Fraction)
    for k in range(w+1):
      for ks in range(s+1):
        A=Fraction(state.get((k,ks,0),0),D); B=Fraction(state.get((k,ks,1),0),D)
        mass=A+B
        if not mass:continue
        short_pos=ks<=s//2; long_pos=k<=w//2
        signed_next=factor*(A-B)
        pplus=(mass+signed_next)/2;pminus=(mass-signed_next)/2
        ls=pminus if short_pos else pplus
        ll=pminus if long_pos else pplus
        total_loss+=(ls+ll)/2
        d=ls-ll
        abs_fine+=abs(d)/2
        groups[(short_pos,long_pos)]+=d
    r_fine=total_loss-abs_fine
    r_coarse=total_loss-sum(map(abs,groups.values()))/2
    return r_coarse,r_fine,r_coarse-r_fine

if __name__=='__main__':
  for a,r in [(Fraction(4,5),Fraction(99,100)),(Fraction(4,5),Fraction(9,10))]:
    for s,w in [(1,11),(5,11),(1,5),(1,9)]:
       if s>=w:continue
       c,f,v=risks(a,r,s,w)
       print('RISK','alpha',a,'r',r,'windows',s,w,'R_Z',float(c),'R_ZM',float(f),'V',float(v))
       assert v == value(a,r,s,w)[0],(s,w,v,value(a,r,s,w)[0])