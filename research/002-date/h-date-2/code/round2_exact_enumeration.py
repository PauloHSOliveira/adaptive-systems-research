#!/usr/bin/env python3
"""Exact rational enumeration of a two-state HMM for H-DATE-2 round 2.

No external dependencies. State is A=0 or B=1. Emission is C=+1 or V=-1.
At an admission opportunity for C, the current request y_t=C.
Short decision uses y_t; long decision uses y_(t-4):y_t.
Next-request loss difference: L_short-L_long = 1{V_(t+1)}-1{C_(t+1)}
if the decisions disagree with short admitting C and long retaining V.
"""
from fractions import Fraction as Q
from itertools import product
from collections import defaultdict
import json


def analyze(r):
    # unnormalized joint mass by signs, magnitude, future state
    joint = defaultdict(lambda: Q(0))
    for states in product((0, 1), repeat=6):
        prior = Q(1, 2)
        for a, b in zip(states, states[1:]):
            prior *= r if a == b else 1-r
        for e in product((1,-1), repeat=5):
            p = prior
            for s, y in zip(states[:5], e):
                p *= Q(4, 5) if (s == 0 and y == 1) or (s == 1 and y == -1) else Q(1, 5)
            signs=(1 if e[-1]>0 else 0,1 if sum(e)>0 else 0)
            magnitude=abs(sum(e))
            joint[(signs,magnitude,states[-1])]+=p

    z_mass = defaultdict(lambda: Q(0))
    for (signs, magnitude, st), mass in joint.items():
        z_mass[signs]+=mass
    report={}
    V_all=Q(0)
    V_candidate_weighted=Q(0)
    for signs in sorted(z_mass):
        mz=z_mass[signs]
        rows=[]
        mean_d=Q(0)
        expected_abs_d=Q(0)
        for mag in (1,3,5):
            a=joint[(signs,mag,0)]
            b=joint[(signs,mag,1)]
            mass=a+b
            if mass==0:continue
            pBnext=b/mass
            # Emission at t+1 under A is 0.8 for C, 0.2 for V.
            # Conditional loss difference for short admitting C and long retaining V.
            base_d=Q(3,5)*(2*pBnext-1)
            if signs==(1,0): d=base_d
            elif signs==(0,1): d=-base_d
            else: d=Q(0)
            w=mass/mz
            mean_d+=w*d
            expected_abs_d+=w*abs(d)
            rows.append({
                'abs_long_margin':f'{mag}/5',
                'P_magnitude_cond_Z':float(w),
                'P_S_tplus1_B_cond_ZM':float(pBnext),
                'conditional_loss_short_minus_long':float(d),
            })
        val=(expected_abs_d-abs(mean_d))/2
        V_all+=mz*val
        if signs[0] == 1:  # current emission is a miss for a resident-V cache
            V_candidate_weighted+=mz*val
        report[f'short={signs[0]},long={signs[1]}']={
            'P_Z':float(mz),
            'd_Z':float(mean_d),
            'V_cond_Z':float(val),
            'magnitude_cells':rows,
        }
    # With a fixed cached V, candidate C is eligible only if e_t=C,
    # which has probability one half by symmetry.
    V_eligible=V_candidate_weighted / Q(1,2)
    return {'p_stay':str(r),'V_global_exact':str(V_all),'V_global':float(V_all),
            'V_per_C_candidate_opportunity_exact':str(V_eligible),'V_per_C_candidate_opportunity':float(V_eligible),'cells':report}


def positive_value_persistence_interval():
    """Boundaries of V_M>0 for r in (1/2,1), under the fixed HMM.

    Unnormalized posterior state differences for Z=(+,-), with K preceding
    V-emissions, have a common positive factor 3*(2*r-1)/6250 and quartics:
      K=3: 1250*r**4-2325*r**3+1781*r**2-506*r-136
      K=4:  625*r**4- 825*r**3+ 436*r**2-136*r- 16
    The latter crosses zero first; the former later.
    """
    def q3(x): return 1250*x**4-2325*x**3+1781*x*x-506*x-136
    def q4(x): return 625*x**4-825*x**3+436*x*x-136*x-16
    def bisect(f,a,b):
        fa=f(a)
        for _ in range(80):
            m=(a+b)/2
            if f(m)*fa <= 0: b=m
            else: a=m;fa=f(m)
        return (a+b)/2
    return bisect(q4,0.8,0.9),bisect(q3,0.9,0.99)


def main():
    outputs=[analyze(Q(9,10)),analyze(Q(3,5))]
    assert outputs[0]['V_global_exact']=='84231/7812500', outputs[0]['V_global_exact']
    assert outputs[1]['V_global']==0.0
    lo, hi = positive_value_persistence_interval()
    assert 0.84 < lo < 0.85 and 0.93 < hi < 0.94
    print(json.dumps({'positive_V_interval_for_r_in_half_to_one':[lo,hi],
                      'HMM_analyses':outputs},ensure_ascii=False,indent=2))


if __name__ == '__main__':main()