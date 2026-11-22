"""Small exact-arithmetic consistency tests for the Study 003 report."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))

from verify_report import (  # noqa: E402
    first_moment,
    second_moment,
    valid_heavy_hitter_lists,
    verify_churn,
    verify_moments,
)
from fractions import Fraction


class TestReflectedWalk(unittest.TestCase):
    def test_exact_recursions(self) -> None:
        for h in range(1, 13):
            with self.subTest(h=h):
                verify_moments(h)

    def test_closed_form(self) -> None:
        self.assertEqual(first_moment(3, 0), 9)
        self.assertEqual(second_moment(3, 0), Fraction(5 * 3**4 - 2 * 3**2, 3))
        self.assertEqual(second_moment(1, 0), 1)

    def test_input_validation(self) -> None:
        with self.assertRaises(ValueError):
            verify_moments(0)


class TestExplicitListChurn(unittest.TestCase):
    def test_churn(self) -> None:
        for k in range(2, 21):
            with self.subTest(k=k):
                verify_churn(k)

    def test_forced_lists(self) -> None:
        self.assertEqual(valid_heavy_hitter_lists({1: 1, 2: 1}, 2), ({1, 2}, {1, 2}))
        self.assertEqual(valid_heavy_hitter_lists({1: 1, 2: 1, 3: 1}, 2), (set(), set()))


if __name__ == "__main__":
    unittest.main()
