#!/usr/bin/env python3
"""Exact H-DATE-2 round-4 HMM polynomial audit (sympy only).

Convention: a=P(+|A)=P(-|B); r=P(S_{t+1}=S_t).
Five observed emissions, last positive; K counts negative emissions among prior four.
Do not confuse current hidden-state posterior with next-step predictive state.
"""
from itertools import product
from sympy import (Matrix, Rational, symbols, diag, factor, cancel, diff,
                   count_roots, nroots, Poly)

r, a = symbols('r a', real=True)
T = Matrix([[r, 1-r], [1-r, r]])
E = {1: diag(a, 1-a), -1: diag(1-a, a)}
prior = Matrix([[Rational(1,2), Rational(1,2)]])

polynomials = {}
for k in (3, 4):
    mass, future_diff = 0, 0
    for seq in product((-1, 1), repeat=4):
        if seq.count(-1) != k:
            continue
        row = prior * E[seq[0]]
        for y in seq[1:] + (1,):
            row = row * T * E[y]
        mass += sum(row)
        future = row * T
        future_diff += future[1] - future[0]
    Q = factor(cancel(future_diff / ((2*a - 1)*(2*r - 1))))
    polynomials[k] = Q
    print(f'K={k}: signed joint future difference = (2a-1)(2r-1) Q_k')
    print('  Q_k(a,r) =', Q)
    print('  Q_k(1/2,r) =', factor(Q.subs(a, Rational(1,2))))
    print('  Q_k(1,r)   =', factor(Q.subs(a, 1)))
    print('  number of distinct roots in r ∈ (1/2,1) at a=1/2:',
          count_roots(Q.subs(a, Rational(1,2)), Rational(1,2), 1))
    assert count_roots(Q.subs(a, Rational(1,2)), Rational(1,2), 1) == 1
    print('  dQ/da at a=1/2 =', factor(diff(Q, a).subs(a, Rational(1,2))))
    print()


def interior_roots(k, alpha):
    roots = nroots(Poly(polynomials[k].subs(a, Rational(str(alpha))), r), maxsteps=200)
    return sorted(float(z.as_real_imag()[0]) for z in roots if abs(float(z.as_real_imag()[1])) < 1e-9
                  and 0.5 < float(z.as_real_imag()[0]) < 1.0)

print(' alpha       r1 (K=4)        r2 (K=3)       width')
for alpha in ['0.500001','0.51','0.6','0.7','0.8','0.9','0.95','0.99','0.999']:
    roots4, roots3 = interior_roots(4, alpha), interior_roots(3, alpha)
    assert len(roots4) == len(roots3) == 1, (alpha, roots4, roots3)
    w = roots3[0] - roots4[0]
    print(f'{alpha:>8} {roots4[0]:>16.10f} {roots3[0]:>16.10f} {w:>14.10f}')

r1=interior_roots(4,'0.500001')[0]
r2=interior_roots(3,'0.500001')[0]
assert abs(r1 - .7593950318) < 1e-5
assert abs(r2 - .8706354553) < 1e-5
assert abs(r2-r1 - .1112404234) < 1e-5
assert abs(interior_roots(4, '0.8')[0] - .8412296) < 1e-5
assert abs(interior_roots(3, '0.8')[0] - .9315755) < 1e-5
print('\nAll symbolic and numerical assertions passed.')