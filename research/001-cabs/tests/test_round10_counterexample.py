"""Regression case: certified admission can be useful without a historical point false positive."""
import unittest
from cabs.core import SketchAdmissionCache


class TestCounterexample(unittest.TestCase):
    def test_certification_can_win_even_when_point_admission_is_historically_correct(self):
        certified = SketchAdmissionCache(capacity=3, sketch_capacity=3, epoch=10000,
                                         mode='cert', debug=True)
        point = SketchAdmissionCache(capacity=3, sketch_capacity=3, epoch=10000,
                                     mode='point', debug=True)
        prefix = [(1, 1.0), (5, 1.0), (3, 1.0), (7, 2.0), (1, 1.0)]
        for key, cost in prefix:
            certified.request(key, cost)
            point.request(key, cost)

        # The fifth request puts the higher-weight object 1 into point's cache.
        # It evicts object 3, which has smaller *true cumulative historical* weight.
        self.assertEqual(certified.oracle[1], 2.0)
        self.assertEqual(certified.oracle[3], 1.0)
        self.assertIn(3, certified.cache)
        self.assertNotIn(3, point.cache)
        self.assertIn(1, point.cache)
        self.assertNotIn(1, certified.cache)

        # An arbitrary future can reverse the usefulness of the historical choice.
        for _ in range(40):
            certified.request(3, 1.0)
            point.request(3, 1.0)

        self.assertEqual(certified.weighted_misses, 6.0)
        self.assertEqual(point.weighted_misses, 7.0)
        self.assertEqual(certified.switches, 1)
        self.assertEqual(point.switches, 3)


if __name__ == '__main__':
    unittest.main()
