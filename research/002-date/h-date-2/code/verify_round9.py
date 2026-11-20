#!/usr/bin/env python3
"""H-DATE-2 round 9: finite-HMM exact risks and certified analytic bounds.

No web or Monte Carlo.  Rational probabilities for finite risk comparisons.
The q*log(1/q) leading constant is a known published rare-transition result
(Nair, Ordentlich & Weissman, IEEE ISIT 2005), not derived numerically here.
"""
from fractions import Fraction
from collections import defaultdict
from math import log, ceil, floor, sqrt
import argparse
from pathlib import Path
import json


def risk_exact(alpha: Fraction, r: Fraction, short: int, long: int):
    """Compute stationary one-step 0/1 risk using signed short/long counts.

    Hidden states 0 and 1; Y=+ occurs with P=alpha under S=0.
    Enumerates (negative_count_long, negative_count_short, latent_state)
    without enumerating all binary sequences. Returns rational risks.
    """
    assert Fraction(1, 2) < alpha < 1
    assert Fraction(1, 2) < r < 1
    assert 1 <= short < long and short % 2 and long % 2
    a,b = alpha, 1-alpha
    d={(0,0,0): a/2, (1,0,0): b/2, (0,0,1): b/2, (1,0,1): a/2}
    for t in range(1,long):
        z=defaultdict(Fraction)
        for (nlong,nshort,hidden), p in d.items():
            for nxt, pt in ((hidden,r),(1-hidden,1-r)):
                for neg,pe in ((0,a if nxt==0 else b),(1,b if nxt==0 else a)):
                    z[(nlong+neg,nshort+(neg if t>=long-short else 0),nxt)] += p*pt*pe
        d=z
    grouped=defaultdict(lambda:[Fraction(0),Fraction(0)])
    fine_loss=Fraction(0)
    factor=(2*a-1)*(2*r-1)
    for nlong in range(long+1):
        for nshort in range(short+1):
            mass_a=d.get((nlong,nshort,0),Fraction(0))
            mass_b=d.get((nlong,nshort,1),Fraction(0))
            total=mass_a+mass_b
            if not total:continue
            # +1 is action 0; -1 is action 1.
            short_positive=nshort<=short//2
            long_positive=nlong<=long//2
            next_plus=(total+factor*(mass_a-mass_b))/2
            next_minus=total-next_plus
            loss_s=next_minus if short_positive else next_plus
            loss_l=next_minus if long_positive else next_plus
            fine_loss+=min(loss_s,loss_l)
            cell=grouped[(short_positive,long_positive)]
            cell[0]+=loss_s;cell[1]+=loss_l
    coarse_loss=sum(min(x) for x in grouped.values())
    return {"risk_signs":coarse_loss,"risk_margins":fine_loss,"value":coarse_loss-fine_loss}


def lower_bound_parameters(alpha,q):
    lam=alpha/(1-alpha)
    m=max(1,floor(log(1/q)/(2*log(lam))))
    pdiff=(1-(1-2*q)**(m+1))/2
    posterior_odds_upper=pdiff/(1-pdiff)*lam**m
    # if this is <1, state oracle at t-m remains optimal for every last m emissions.
    assert posterior_odds_upper<1, (q,m,posterior_odds_upper)
    return {"q":q,"m":m,"p_diff":pdiff,"posterior_odds_bound":posterior_odds_upper,"lower_excess_risk":(2*alpha-1)*pdiff}


def upper_bound_parameters(alpha,q):
    delta=alpha-.5
    w=ceil(log(1/q)/(2*delta**2))
    if w%2==0:w+=1
    return {"q":q,"w":w,"upper_excess_risk":(2*alpha-1)*(w*q+__import__('math').exp(-2*w*delta**2))}


def main():
    parser=argparse.ArgumentParser(description="Verify exact H-DATE-2 risks and illustrate published rare-transition bounds")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent.parent/"data"/"round9_verification_reproduced.json")
    args=parser.parse_args()
    a=Fraction(4,5);r=Fraction(9,10)
    pair3=risk_exact(a,r,1,3)
    pair5=risk_exact(a,r,1,5)
    assert pair3['value']==0
    assert pair5['value']==Fraction(84231,7812500)
    assert pair3['risk_margins']<pair5['risk_margins']
    assert pair5['risk_signs']-pair5['risk_margins']==pair5['value']
    print('Exact risk: (1,3)', {k:str(v) for k,v in pair3.items()})
    print('Exact risk: (1,5)', {k:str(v) for k,v in pair5.items()})
    alpha=.8
    rows=[]
    for q in [1e-4,1e-6,1e-8,1e-10]:
        lower=lower_bound_parameters(alpha,q)
        upper=upper_bound_parameters(alpha,q)
        common={'q':q,'lower':lower,'upper':upper,
            'asymptotic_leading':q*log(1/q)/log(alpha/(1-alpha))}
        print('Asymptotic certificate:',common)
        assert lower['lower_excess_risk']<=upper['upper_excess_risk']
        rows.append(common)
    delta=alpha-.5
    assert 2*delta*delta<0.5
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('w',encoding='utf-8') as f:
        json.dump({'exact_comparison':{'(1,3)':{k:str(v) for k,v in pair3.items()},'(1,5)':{k:str(v) for k,v in pair5.items()}},
        'bounds':rows,'alpha_threshold_claim':{'alpha':.5+1/(2*sqrt(2)),'2delta_squared_at_claim':.25}},f,indent=2)
    print('ALL TESTS PASS')

if __name__=='__main__':main()