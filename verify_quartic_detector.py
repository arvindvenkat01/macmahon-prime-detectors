#!/usr/bin/env python3
"""
Quartic MacMahonesque Prime Detector Verification

This script:
  - Computes MacMahonesque statistics M_k(n) for k = 1..4
    (sum over partitions of n with exactly k distinct part sizes
     of the product of multiplicities).
  - Evaluates the quartic detector
        L4(n) = (12915n^2 - 4305n^3 - 8610n) M1(n)
              + (18368n^2 - 2296n^3) M2(n)
              + (48640n^2 - 3200n^3) M3(n)
              + 967680n M4(n)
  - Verifies, for 2 <= n <= N_MAX, whether:
        n is prime  <=>  L4(n) == 0

Requires: sympy
"""

from functools import lru_cache
from math import prod
import sympy


# =========================
# 1. MacMahonesque M_k(n)
# =========================

def compute_M_up_to_4(n_max):
    """
    Compute M_k(n) for k = 1..4 and 0 <= n <= n_max.

    M_k(n) = sum over partitions of n with exactly k distinct part sizes
             of (product of multiplicities).

    Returns:
        Ms: dict
            Ms[n][k] = M_k(n) for k in {1,2,3,4}.
    """

    @lru_cache(maxsize=None)
    def rec(remaining, min_part, distinct_used):
        """
        Recursive DP over partitions with nondecreasing distinct parts.

        State:
            remaining      : how much is left to sum to n
            min_part       : minimum allowed next part value (to keep order)
            distinct_used  : how many distinct part sizes have been chosen so far

        Returns:
            V: tuple of length 5, V[k] is the cumulative sum of products of
               multiplicities over all completions from this state that
               end with exactly k distinct part sizes in total, for k=0..4.
        """
        # V[k] accumulates contributions for exact total distinct size k
        V = [0, 0, 0, 0, 0]

        # Base case: exact partition completed
        if remaining == 0:
            # If total distinct sizes is between 1 and 4, contribute 1
            # (product over an empty set of future multiplicities is 1)
            if 1 <= distinct_used <= 4:
                V[distinct_used] = 1
            return tuple(V)

        # Choose the next distinct part value i >= min_part
        # We never care about more than 4 distinct part sizes
        for i in range(min_part, remaining + 1):
            if distinct_used + 1 > 4:
                break  # adding a new distinct part would exceed 4

            max_m = remaining // i
            # Choose multiplicity m >= 1 for part i
            for m in range(1, max_m + 1):
                new_rem = remaining - m * i
                child = rec(new_rem, i + 1, distinct_used + 1)

                # Each partition in child has multiplicity-product already
                # for the "future" distinct parts. Including i with
                # multiplicity m multiplies that by m.
                if m != 1:
                    for k in range(1, 5):
                        if child[k]:
                            V[k] += m * child[k]
                else:
                    # Slightly faster branch when m=1
                    for k in range(1, 5):
                        if child[k]:
                            V[k] += child[k]

        return tuple(V)

    Ms = {}
    for n in range(0, n_max + 1):
        V = rec(n, 1, 0)
        Ms[n] = {k: V[k] for k in range(1, 5)}
    return Ms


# =========================
# 2. Quartic detector L4(n)
# =========================

COEFFS = {
    'M1_n3': -4305,
    'M1_n2': 12915,
    'M1_n1': -8610,
    'M2_n3': -2296,
    'M2_n2': 18368,
    'M3_n3': -3200,
    'M3_n2': 48640,
    'M4_n1': 967680,
}


def quartic_L4(n, Ms_for_n):
    """
    Evaluate your quartic MacMahonesque detector L4(n).

    Arguments:
        n        : integer >= 0
        Ms_for_n : dict {1: M1(n), 2: M2(n), 3: M3(n), 4: M4(n)}

    Returns:
        Integer value of L4(n).
    """
    m1 = Ms_for_n.get(1, 0)
    m2 = Ms_for_n.get(2, 0)
    m3 = Ms_for_n.get(3, 0)
    m4 = Ms_for_n.get(4, 0)

    term1 = (COEFFS['M1_n3'] * n**3 + COEFFS['M1_n2'] * n**2 + COEFFS['M1_n1'] * n) * m1
    term2 = (COEFFS['M2_n3'] * n**3 + COEFFS['M2_n2'] * n**2) * m2
    term3 = (COEFFS['M3_n3'] * n**3 + COEFFS['M3_n2'] * n**2) * m3
    term4 = (COEFFS['M4_n1'] * n) * m4

    return term1 + term2 + term3 + term4


# =========================
# 3. Verification driver
# =========================

def verify_range(N_max, verbose=True):
    """
    Verify the quartic detector on the range 2 <= n <= N_max.

    For each n:
        - Compute M_k(n) for k=1..4.
        - Evaluate L4(n).
        - Check:
              n prime      => L4(n) == 0
              n composite  => L4(n) != 0

    Returns:
        failures: list of tuples (n, is_prime, L4(n))
                  where the detector's behavior does NOT match the spec.
    """
    if verbose:
        print(f"Computing M_k(n) for 0 <= n <= {N_max} ...")
    Ms = compute_M_up_to_4(N_max)

    failures = []
    if verbose:
        print(f"{'n':>5} | {'type':>9} | {'L4(n)':>20} | status")
        print("-" * 50)

    for n in range(2, N_max + 1):
        val = quartic_L4(n, Ms[n])
        is_prime = sympy.isprime(n)
        ok = (is_prime and val == 0) or ((not is_prime) and val != 0)

        if verbose:
            t = "prime" if is_prime else "composite"
            status = "OK" if ok else "FAIL"
            print(f"{n:5d} | {t:>9} | {val:20d} | {status}")

        if not ok:
            failures.append((n, is_prime, val))

    return failures


# =========================
# 4. Main entry point
# =========================

if __name__ == "__main__":
    # Adjust this as high as your machine can comfortably handle.
    # Start with a modest bound, e.g. 100 or 200, then increase.
    N_MAX = 1000

    failures = verify_range(N_MAX, verbose=True)

    print("-" * 50)
    if not failures:
        print(f"No counterexamples found in 2 <= n <= {N_MAX}.")
    else:
        print("Counterexamples found:")
        for n, is_prime, val in failures:
            print(f"  n = {n}, prime = {is_prime}, L4(n) = {val}")
