"""Deterministic arithmetic checks for Study 003.

This is not a stochastic experiment or an independent research-novelty proof.
Only the Python standard library is required.
"""

from __future__ import annotations

from fractions import Fraction


def first_moment(h: int, i: int) -> int:
    """Expected steps to hit h from i, reflecting at 0."""
    return h * h - i * i


def second_moment(h: int, i: int) -> Fraction:
    """Exact polynomial solution of the hitting-time second-moment recurrence."""
    return Fraction(
        i**4 + (2 - 6 * h * h) * i * i + 5 * h**4 - 2 * h * h,
        3,
    )


def verify_moments(h: int) -> None:
    """Check every first-step equation using exact rational arithmetic."""
    if h < 1:
        raise ValueError("h must be a positive integer")
    f = lambda i: Fraction(first_moment(h, i))
    g = lambda i: second_moment(h, i)

    assert f(h) == 0
    assert g(h) == 0
    assert f(0) == 1 + f(1)
    assert g(0) == 1 + 2 * f(1) + g(1)

    for i in range(1, h):
        assert f(i) == 1 + (f(i - 1) + f(i + 1)) / 2
        assert g(i) == 2 * f(i) - 1 + (g(i - 1) + g(i + 1)) / 2

    assert f(0) == h**2
    assert g(0) == Fraction(5 * h**4 - 2 * h**2, 3)
    assert g(0) - f(0) ** 2 == Fraction(2 * h**2 * (h**2 - 1), 3)


def valid_heavy_hitter_lists(frequencies: dict[int, int], k: int) -> tuple[set[int], set[int]]:
    """Return mandatory and allowed identifiers for the churn example."""
    if k < 2:
        raise ValueError("k must be at least 2")
    phi = Fraction(1, k)
    eta = Fraction(1, 2 * k * (k + 1))
    total = sum(frequencies.values())
    if total <= 0 or any(v < 0 for v in frequencies.values()):
        raise ValueError("expected a nonempty nonnegative vector")
    mandatory = {x for x, count in frequencies.items() if count >= phi * total}
    allowed = {x for x, count in frequencies.items() if count >= (phi - eta) * total}
    return mandatory, allowed


def verify_churn(k: int) -> None:
    """Check forced list X -> empty -> X for the explicit-output example."""
    base = {x: 1 for x in range(1, k + 1)}
    expanded = {**base, k + 1: 1}
    x = set(base)
    assert valid_heavy_hitter_lists(base, k) == (x, x)
    assert valid_heavy_hitter_lists(expanded, k) == (set(), set())
    assert len(x.symmetric_difference(set())) == k


if __name__ == "__main__":
    for h in range(1, 13):
        verify_moments(h)
    for k in range(2, 21):
        verify_churn(k)
    print("PASS: exact walk recurrences for H=1..12")
    print("PASS: explicit heavy-hitter churn for k=2..20")
    print("Scope: finite algebraic checks only; no simulation or performance claims")
