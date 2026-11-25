"""Exact conditional no-double-collision excursion checks, using integer weights."""
from collections import defaultdict
from fractions import Fraction
from itertools import product


def verify(L, B1, B2):
    p1, p2 = Fraction(1,B1), Fraction(1,B2)
    weights = {0:(B1-1)*(B2-1), 1:B2-1, -1:B1-1}
    denominator = (B1*B2-1)**L
    groups = defaultdict(list)
    loss = Fraction(0)
    c_weight = tie_weight = total = 0
    for path in product((0,1,-1), repeat=L):
        weight = 1
        positions, absolute, visible = [], [0], []
        z = last_zero = 0
        for i, x in enumerate(path):
            weight *= weights[x]
            if not x:
                continue
            positions.append(i)
            if abs(z+x) < abs(z):
                visible.append(i)
            z += x
            absolute.append(abs(z))
            if z == 0:
                last_zero = len(positions)
        total += weight
        n = len(positions)
        m = (n-abs(z))//2
        bottleneck = -1 if z>0 else 1
        if m and z:
            in_c = not any(i in visible for i in positions[last_zero:])
            c_weight += weight*in_c
            loss += weight*(path[visible[-1]] != bottleneck)
        elif m:
            tie_weight += weight
            loss += weight*p1*p2
        if visible:
            groups[(tuple(positions),tuple(absolute))].append((path,weight,tuple(visible),m,z))
    assert total == denominator
    assert loss == Fraction(c_weight,2)+p1*p2*tie_weight
    for group in groups.values():
        _,_,visible,m,z = group[0]
        # The terminal absolute value, not the orientation, is common.
        assert all(v==visible and mm==m and abs(zz)==abs(z) for _,_,v,mm,zz in group)
        scores = [sum(w for path,w,_,_,zz in group if zz and path[i]==(-1 if zz>0 else 1)) for i in visible]
        assert scores[-1] == max(scores)
    return len(groups)

if __name__ == '__main__':
    total = sum(verify(L,b1,b2) for L in range(1,8) for b1,b2 in [(2,2),(3,3),(2,3),(5,2)])
    print(f'PASS: 28 parameter configurations; {total} absolute-walk / active-position groups with visible slots.')
