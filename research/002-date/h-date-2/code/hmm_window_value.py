#!/usr/bin/env python3
"""Finite-dimensional HMM enumeration of the ideal marginal value of magnitudes.

A=0, B=1; plus event has emission probability alpha under A and 1-alpha under B.
Stationary initial distribution is (1/2, 1/2); transition persistence r.
Two moving-window averages of +/-1 emissions, with odd lengths s<w.
The loss is at the next emission, with unit miss costs and 2 possible cache actions.
The summary Z comprises only short/long signs, the features M are their absolute
averages. Since signs plus magnitudes recover the two (integer) counts, grouping
on counts is equivalent to conditioning on (Z,M).

DP tracks joint probability of the final latent state and number of - emissions
in the full window and in the final short window. O(w^2 * s) with numpy arrays.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
import json
import numpy as np


@dataclass(frozen=True)
class ValueResult:
    alpha: float
    stay: float
    short: int
    long: int
    value: float
    disagreement_mass: float
    information_mass_by_cell: tuple[float, float]


def joint_counts(alpha: float, r: float, s: int, w: int) -> np.ndarray:
    if not (0.5 < alpha < 1.0 and 0.5 < r < 1.0):
        raise ValueError("Require 1/2 < alpha,r < 1")
    if not (s >= 1 and s < w and s % 2 and w % 2):
        raise ValueError("Odd windows with 1 <= short < long required")
    d = np.zeros((w + 1, s + 1, 2))
    d[0, 0, :] = .5
    t = np.array([[r, 1 - r], [1 - r, r]])
    eplus = np.array([alpha, 1 - alpha]); eminus=1-eplus
    for i in range(w):
        if i:
            d = np.einsum('...i,ij->...j', d, t)
        new = np.zeros_like(d)
        new += d * eplus
        if i >= w-s:
            new[1:, 1:, :] += d[:-1, :-1, :] * eminus
        else:
            new[1:, :, :] += d[:-1, :, :] * eminus
        d = new
    return d


def value(alpha: float, r: float, s: int, w: int) -> ValueResult:
    masses = joint_counts(alpha,r,s,w)
    expectation_future_plus_minus = (2*alpha-1)*(2*r-1)*(masses[:,:,0]-masses[:,:,1])
    short_positive = (np.arange(s+1) <= s//2)[None,:]
    long_positive = (np.arange(w+1) <= w//2)[:,None]
    p_sm_lm = short_positive & (~long_positive)
    p_sp_lp = (~short_positive) & long_positive
    dmasses = np.where(p_sm_lm,-expectation_future_plus_minus,np.where(p_sp_lp,expectation_future_plus_minus,0))
    abs_by_cell = []
    disagreement_mass=0
    for mask in (p_sm_lm,p_sp_lp):
        dx=dmasses[mask]
        abs_by_cell.append((np.abs(dx).sum() - abs(dx.sum()))/2)
        disagreement_mass += masses.sum(axis=2)[mask].sum()
    return ValueResult(alpha,r,s,w,float(sum(abs_by_cell)),float(disagreement_mass),tuple(map(float,abs_by_cell)))


def sample_rows(alpha:float,r:float,srange=range(1,22,2),wmax:int=65):
    result = []
    for s in srange:
        for w in range(s+2,wmax+1,2):
            v = value(alpha,r,s,w)
            result.append(v)
    return result


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',default='window_results.json')
    args=parser.parse_args()
    assert abs(value(.8,.9,1,5).value - 84231/7812500) < 2e-15, value(.8,.9,1,5)
    assert value(.8,.6,1,5).value < 1e-14
    assert value(.8,.9,1,3).value < 1e-14
    scenarios=[]
    for r in (.55,.6,.7,.8,.85,.9,.95,.98):
        rows=sample_rows(.8,r,wmax=51,srange=range(1,16,2))
        best1=max((v for v in rows if v.short==1),key=lambda v:v.value)
        best=max(rows,key=lambda v:v.value)
        scenarios.append({'alpha':.8,'r':r,'best_short_1':best1.__dict__,'best_any':best.__dict__,'w1_3_5_7_9_11_13_15_21_31_51':[value(.8,r,1,w).__dict__ for w in (3,5,7,9,11,13,15,21,31,51)]})
        print('r',r,'best short1',(best1.short,best1.long,best1.value),'best any',(best.short,best.long,best.value))
    with open(args.output,'w') as f:json.dump({'scenarios':scenarios},f,indent=2)

if __name__=='__main__':main()