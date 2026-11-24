"""Exact finite counterexample to the fresh-prefix reduction for K=2.
Abstract fixed-target CMS model; two rows, two buckets, six updates.
All 4**6 collision arrays are equally likely. Rewards are in counts.
"""
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import product

M, K, R = 6, 2, 2
patterns = tuple(product(range(4), repeat=M))
D = len(patterns)

@lru_cache(None)
def observation(counts, h):
    return min(sum(c * ((v >> j) & 1) for c, v in zip(counts, patterns[h]))
               for j in range(R))

@lru_cache(None)
def value(counts, belief, prefix):
    t, n = sum(counts), sum(c > 0 for c in counts)
    if t == M:
        return sum(observation(counts, h) for h in belief)
    return max(action_value(counts, belief, prefix, i)
               for i in range(min(n + 1, M))
               if i == n or (t >= prefix and t - n < K))

def action_value(counts, belief, prefix, i):
    new = list(counts)
    new[i] += 1
    new = tuple(new)
    if sum(new) == M:
        return value(new, belief, prefix)
    groups = defaultdict(list)
    for h in belief:
        groups[observation(new, h)].append(h)
    return sum(value(new, tuple(g), prefix) for g in groups.values())

if __name__ == '__main__':
    root = (0,) * M
    all_h = tuple(range(D))
    unrestricted = Fraction(value(root, all_h, 0), D)
    prefix3 = Fraction(value(root, all_h, 3), D)
    prefix4 = Fraction(value(root, all_h, 4), D)
    assert unrestricted == prefix3 == Fraction(12597, 4096)
    assert prefix4 == Fraction(12565, 4096)
    print('Unrestricted:', unrestricted)
    print('Three fresh initially:', prefix3)
    print('Four fresh initially:', prefix4)
    print('Gap in counts:', unrestricted - prefix4)
    print('Normalized gap:', (unrestricted - prefix4) / M)
    groups = defaultdict(list)
    for h in all_h:
        hist = tuple(observation((1,) * t + (0,) * (M - t), h)
                     for t in range(1, 4))
        groups[hist].append(h)
    counts = (1, 1, 1, 0, 0, 0)
    print('history | patterns | best weighted sum | forced-fresh weighted sum')
    for hist, g in sorted(groups.items()):
        g = tuple(g)
        print(hist, len(g), value(counts, g, 3), value(counts, g, 4))
    g = tuple(groups[(0, 1, 2)])
    scores = [action_value(counts, g, 3, i) for i in range(4)]
    assert len(g) == 448 and scores == [1520, 1840, 1840, 1808]
    print('Action scores at (0,1,2):', scores)
    print('PASS')
