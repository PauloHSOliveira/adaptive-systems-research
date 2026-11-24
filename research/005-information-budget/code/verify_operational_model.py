from itertools import product
from functools import lru_cache
from fractions import Fraction
from math import comb, log

# Three possible keys, two rows, two buckets; target absent.
H = tuple(product((0, 1), repeat=6))
M, R, N = 4, 2, 3

def estimate(h, counts):
    return min(sum(counts[i]*h[2*i+j] for i in range(N)) for j in range(R))

def solve(K, checkpoints, threshold=None):
    @lru_cache(None)
    def dp(counts, belief):
        t = sum(counts)
        if t == M:
            y = [estimate(H[h], counts) for h in belief]
            return sum(y) if threshold is None else sum(x >= threshold for x in y)
        best = -1
        for i in range(N):
            nc = list(counts)
            nc[i] += 1
            nc = tuple(nc)
            repeats = t + 1 - sum(x > 0 for x in nc)
            if repeats > K:
                continue
            if t+1 not in checkpoints:
                val = dp(nc, belief)
            else:
                groups = {}
                for h in belief:
                    groups.setdefault(estimate(H[h], nc), []).append(h)
                val = sum(dp(nc, tuple(v)) for v in groups.values())
            best = max(best, val)
        assert best >= 0
        return best
    num = dp((0,)*N, tuple(range(len(H))))
    return Fraction(num, len(H)*(M if threshold is None else 1))

def tail(K, z):
    n = M-K
    a = z-K
    p = sum(Fraction(comb(n,i), 2**n) for i in range(max(0,a), n+1))
    return p**R

if __name__ == '__main__':
    for K in (1,2,3):
        for cp in ((),(2,),(1,2,3)):
            e = solve(K,cp)
            t = [solve(K,cp,z) for z in (1,2,3,4)]
            bounds = [tail(K,z) for z in (1,2,3,4)]
            assert all(a<=b for a,b in zip(t,bounds))
            assert e<=sum(bounds)/M
            print(K,cp,str(e),[str(x) for x in t],[str(x) for x in bounds])
    M0 = 100000
    q = 256
    blocks = [M0//q+int(i<M0%q) for i in range(q)]
    print('capacity',q*log(M0+1),sum(log(d+1) for d in blocks))
