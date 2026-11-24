"""Finite arithmetic check of baseline inequalities; no interactive attack.
Python standard library only. Counts are exact; log/sqrt use floating point.
"""
from itertools import product
from math import log, sqrt

patterns = list(product((0, 1), repeat=4))
n = len(patterns)

def xlog(x, y):
    return 0.0 if x == 0 else x * log(x / y)

def kl(a, q):
    return xlog(a, q) + xlog(1-a, 1-q)

def main():
    max_success = 0.0
    max_kl_gap = float("-inf")
    for mask in range(1 << n):
        prob = mask.bit_count() / n
        info = -(xlog(prob, 1) + xlog(1-prob, 1))
        hit = sum(
            min(p[2*((mask >> i)&1):2*((mask >> i)&1)+2])
            for i, p in enumerate(patterns)
        ) / n
        assert kl(hit, .25) <= info + 1e-12
        assert hit <= min(1, .5 + sqrt(info/4)) + 1e-12
        max_success = max(max_success, hit)
        max_kl_gap = max(max_kl_gap, kl(hit, .25)-info)
    print({"selectors": 1 << n, "fixed_selector_success": .25,
           "max_success": max_success, "max_KL_minus_I": max_kl_gap})

if __name__ == "__main__":
    main()
