"""Repeatable synthetic request generators. This is not a public trace dataset."""
import random

def events(kind: str, n: int, seed: int, catalog: int = 100_000):
    rng = random.Random(seed)
    block = 2_000
    for t in range(n):
        if kind == 'uniform':
            key = rng.randrange(catalog)
        elif kind == 'stationary':
            key = (int((rng.random() ** 2) * 400)
                   if rng.random() < .9 else rng.randrange(catalog))
        elif kind == 'drift':
            hot_block = (t // block) % (catalog // 400)
            key = (400*hot_block + int((rng.random() ** 2)*400)
                   if rng.random() < .9 else rng.randrange(catalog))
        elif kind == 'reset_churn':
            # Alternating stable hot set and cold scans around epoch boundaries.
            offset = ((t // 10_000) % 2) * 400
            key = (offset + int((rng.random() ** 2)*400)
                   if rng.random() < .83 else rng.randrange(catalog))
        else:
            raise ValueError(kind)
        weight = float(1 + ((key * 37 + 19) % 17))
        yield key, weight
