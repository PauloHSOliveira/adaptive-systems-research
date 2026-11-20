import random
import unittest
from cabs.core import WeightedSpaceSaving, SketchAdmissionCache

class TestWeightedSpaceSaving(unittest.TestCase):
    def test_weighted_bounds_and_unmonitored(self):
        s = WeightedSpaceSaving(8)
        exact = {}
        rng = random.Random(77)
        for t in range(900):
            obj = rng.randrange(40)
            weight = rng.randrange(1, 11)
            exact[obj] = exact.get(obj, 0) + weight
            s.update(obj, weight)
            s.check_structure()
            for other, true_val in exact.items():
                lo, hi = s.bounds(other)
                self.assertLessEqual(lo-1e-9, true_val)
                self.assertLessEqual(true_val, hi+1e-9)

    def test_sketch_can_drop_resident_without_corrupting_rm(self):
        p = SketchAdmissionCache(3, 2, epoch=100, debug=True)
        for key in [1,2,3,4,5,6,7,8,2,1,8,9,2,9,2,9]:
            p.request(key,1.0)
        self.assertGreater(p.nonempty_rm_errors, 0)

    def test_random_invariants_many_epochs(self):
        p = SketchAdmissionCache(5, 6, epoch=37, debug=True)
        rng = random.Random(13)
        for _ in range(500):
            p.request(rng.randrange(30),float(rng.randrange(1,20)))
        self.assertEqual(p.false_positive_admissions, 0)

    def test_prefix_causality(self):
        common=[(i%7,float(i%3+1)) for i in range(90)]
        a=SketchAdmissionCache(3, 5, 37,debug=True)
        b=SketchAdmissionCache(3, 5, 37,debug=True)
        for key,w in common:
            self.assertEqual(a.request(key,w),b.request(key,w))
            self.assertEqual(a.cache,b.cache)
        # Different suffix cannot change earlier decisions.
        for key,w in [(i%7,1.) for i in range(90)]: a.request(key,w)
        for key,w in [(100+i,2.) for i in range(90)]: b.request(key,w)

if __name__ == '__main__': unittest.main()

class TestMoreCases(unittest.TestCase):
    def test_resident_metadata_can_be_inexact(self):
        p=SketchAdmissionCache(2, 2, epoch=100, debug=True)
        for key in [1, 2, 3, 4, 3, 4, 3, 4, 3, 4, 3, 4]:
            p.request(key,1.0)
        # Inherited interval on admission can be broader than an exact counter.
        for key, rm in p.cache.items():
            assert rm.lower <= p.oracle[key] <= rm.upper

    def test_many_random_seeds_certificates(self):
        for seed in range(15):
            rng = random.Random(seed)
            p = SketchAdmissionCache(7, 8, epoch=53, debug=True)
            for _ in range(300):
                p.request(rng.randrange(80), float(rng.randrange(1,10)))
            self.assertEqual(p.false_positive_admissions, 0)
