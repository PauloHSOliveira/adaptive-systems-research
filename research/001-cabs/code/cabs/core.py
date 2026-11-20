"""CPU-only reference implementation of Weighted Space-Saving and CABS.

Experimental software: guarantees apply only to weighted counts within the
current epoch. No future hit-rate or regret guarantee is claimed.
"""
from __future__ import annotations
from dataclasses import dataclass
from collections import OrderedDict

@dataclass(slots=True)
class Entry:
    key: int
    upper: float
    error: float

    @property
    def lower(self) -> float:
        return self.upper - self.error

class WeightedSpaceSaving:
    """Fixed-size indexed min-heap. Every update has O(log capacity) worst-case time."""
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError('capacity must be positive')
        self.capacity = capacity
        self.heap: list[Entry] = []
        self.pos: dict[int, int] = {}

    def clear(self) -> None:
        self.heap.clear()
        self.pos.clear()

    def _less(self, a: Entry, b: Entry) -> bool:
        return (a.upper, a.key) < (b.upper, b.key)

    def _swap(self, i: int, j: int) -> None:
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.pos[self.heap[i].key] = i
        self.pos[self.heap[j].key] = j

    def _up(self, i: int) -> None:
        while i:
            p = (i - 1) // 2
            if not self._less(self.heap[i], self.heap[p]):
                break
            self._swap(i, p)
            i = p

    def _down(self, i: int) -> None:
        n = len(self.heap)
        while True:
            l = 2 * i + 1
            r = l + 1
            m = i
            if l < n and self._less(self.heap[l], self.heap[m]):
                m = l
            if r < n and self._less(self.heap[r], self.heap[m]):
                m = r
            if m == i:
                break
            self._swap(i, m)
            i = m

    def update(self, key: int, weight: float) -> Entry:
        if not 0 < weight < float('inf'):
            raise ValueError('weight must be finite and positive')
        if key in self.pos:
            idx = self.pos[key]
            item = self.heap[idx]
            item.upper += weight
            self._down(idx)
            return item
        if len(self.heap) < self.capacity:
            item = Entry(key, weight, 0.)
            self.heap.append(item)
            self.pos[key] = len(self.heap) - 1
            self._up(len(self.heap) - 1)
            return item
        prev = self.heap[0]
        floor = prev.upper
        del self.pos[prev.key]
        item = Entry(key, floor + weight, floor)
        self.heap[0] = item
        self.pos[key] = 0
        self._down(0)
        return item

    def bounds(self, key: int) -> tuple[float, float]:
        idx = self.pos.get(key)
        if idx is not None:
            x = self.heap[idx]
            return x.lower, x.upper
        if len(self.heap) < self.capacity:
            return 0., 0.
        return 0., self.heap[0].upper

    def check_structure(self) -> None:
        assert len(self.heap) == len(self.pos) <= self.capacity
        for i, entry in enumerate(self.heap):
            assert self.pos[entry.key] == i
            assert entry.lower >= -1e-7
            if i:
                assert not self._less(entry, self.heap[(i-1)//2])

@dataclass(slots=True)
class Resident:
    lower: float
    upper: float

class SketchAdmissionCache:
    def __init__(self, capacity=100, sketch_capacity=500, epoch=10000,
                 mode='cert', holdoff=0, debug=False):
        if capacity < 1 or epoch < 1:
            raise ValueError('invalid capacity/epoch')
        if mode not in ('cert', 'point'):
            raise ValueError('mode must be cert or point')
        self.capacity = capacity
        self.sketch = WeightedSpaceSaving(sketch_capacity)
        self.epoch = epoch
        self.mode = mode
        self.holdoff = holdoff
        self.debug = debug
        self.cache: dict[int, Resident] = {}
        self.t = 0
        self.hits = self.misses = self.switches = self.bypasses = 0
        self.weighted_misses = 0.
        self.certified = 0
        self.false_positive_admissions = 0
        self.oracle: dict[int, float] = {}  # for debug only; NOT part of policy state
        self.nonempty_rm_errors = 0

    def request(self, key: int, weight: float) -> bool:
        if self.t % self.epoch == 0:
            self.sketch.clear()
            for resident in self.cache.values():
                resident.lower = 0.
                resident.upper = 0.
            self.oracle.clear()
        epoch_age = self.t % self.epoch
        self.t += 1
        was_hit = key in self.cache
        self.sketch.update(key, weight)
        if self.debug:
            self.oracle[key] = self.oracle.get(key, 0.) + weight
        if was_hit:
            self.hits += 1
            r = self.cache[key]
            r.lower += weight
            r.upper += weight
        else:
            self.misses += 1
            self.weighted_misses += weight
            lower, upper = self.sketch.bounds(key)
            if len(self.cache) < self.capacity:
                self.cache[key] = Resident(lower, upper)
            else:
                victim = min(self.cache, key=lambda k: (self.cache[k].upper, k))
                threshold = self.cache[victim].upper
                score = lower if self.mode == 'cert' else upper
                if epoch_age >= self.holdoff and score > threshold:
                    if self.mode == 'cert':
                        self.certified += 1
                    if self.debug and self.oracle[key] <= self.oracle.get(victim, 0.) + 1e-9:
                        self.false_positive_admissions += 1
                        if self.mode == 'cert':
                            raise AssertionError('Invalid certificate')
                    del self.cache[victim]
                    self.cache[key] = Resident(lower, upper)
                    self.switches += 1
                else:
                    self.bypasses += 1
        if self.debug:
            self.validate()
        return was_hit

    def validate(self):
        self.sketch.check_structure()
        assert len(self.cache) <= self.capacity
        for key, r in self.cache.items():
            assert r.lower - 1e-7 <= self.oracle.get(key, 0.) <= r.upper + 1e-7, (
                key, r, self.oracle.get(key, 0.))
            if r.upper - r.lower > 1e-6:
                self.nonempty_rm_errors += 1
        for item in self.sketch.heap:
            exact = self.oracle.get(item.key, 0.)
            assert item.lower - 1e-7 <= exact <= item.upper + 1e-7, (
                item, exact)
        if len(self.sketch.heap) == self.sketch.capacity:
            floor = self.sketch.heap[0].upper
            for key, exact in self.oracle.items():
                if key not in self.sketch.pos:
                    assert exact <= floor + 1e-7

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()
        self.hits = self.misses = self.switches = self.bypasses = 0
        self.weighted_misses = 0.
    def request(self, key, weight):
        if key in self.cache:
            self.hits += 1
            self.cache.move_to_end(key)
            return True
        self.misses += 1
        self.weighted_misses += weight
        if len(self.cache) == self.capacity:
            self.cache.popitem(last=False)
            self.switches += 1
        self.cache[key] = None
        return False

class ExactLFUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = set()
        self.counts: dict[int, float] = {}  # unbounded: oracle-memory baseline
        self.hits = self.misses = self.switches = self.bypasses = 0
        self.weighted_misses = 0.
    def request(self, key, weight):
        self.counts[key] = self.counts.get(key, 0.) + weight
        if key in self.cache:
            self.hits += 1
            return True
        self.misses += 1
        self.weighted_misses += weight
        if len(self.cache) < self.capacity:
            self.cache.add(key)
        else:
            victim = min(self.cache, key=lambda k: (self.counts[k], k))
            if self.counts[key] > self.counts[victim]:
                self.cache.remove(victim)
                self.cache.add(key)
                self.switches += 1
            else:
                self.bypasses += 1
        return False
