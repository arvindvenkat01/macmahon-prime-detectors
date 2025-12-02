# MIT License
#
# Copyright (c) 2025 Arvind N. Venkat
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#!/usr/bin/env python3
"""
EXPLICIT VERIFICATION: Checks EVERY number 2..1000
"""

import sympy
from functools import lru_cache
import sys

# Increase recursion depth
sys.setrecursionlimit(20000)

def compute_M_up_to_3(n_max):
    """Pruned partition generator for M1, M2, M3"""
    
    @lru_cache(maxsize=None)
    def rec(remaining, min_part, distinct_used):
        V = [0, 0, 0, 0] 
        if remaining == 0:
            if 1 <= distinct_used <= 3:
                V[distinct_used] = 1
            return tuple(V)

        if distinct_used >= 3:
            # Optimization: If we have 3 distinct parts, we can ONLY add the LAST part
            # to keep distinct count at 3.
            # If we add a NEW part (i > min_part-1), distinct count becomes 4 (PRUNE).
            # So we only loop i where i == (min_part - 1).
            # But min_part is passed as i+1. So previous part was min_part-1.
            # We can just loop i = min_part-1? No, logic is tricky.
            # Let's stick to the standard loop but break early.
            pass

        for i in range(min_part, remaining + 1):
            # If we are already at 3 distinct parts, we CANNOT pick a new part.
            # We can only pick 'i' if 'i' was the SAME as the last part.
            # But in this recursion structure, 'min_part' forces i >= last_part.
            # If we are at distinct=3, we effectively stop unless we implement 
            # specific logic for "add same part".
            # For safety/simplicity in this script, we just use the generic break:
            if distinct_used + 1 > 3:
                break 

            max_m = remaining // i
            for m in range(1, max_m + 1):
                new_rem = remaining - m * i
                child = rec(new_rem, i + 1, distinct_used + 1)
                mult = m if m > 1 else 1
                for k in range(1, 4):
                    if child[k]: V[k] += mult * child[k]
        return tuple(V)

    Ms = {}
    # Pre-compute
    print(f"Pre-computing partition stats for n=1..{n_max}...")
    for n in range(0, n_max + 1):
        V = rec(n, 1, 0)
        Ms[n] = {k: V[k] for k in range(1, 4)}
    return Ms

def binomial_cubic_detector(n, Ms_for_n):
    if n < 3: return 0
    m1 = Ms_for_n.get(1, 0)
    m2 = Ms_for_n.get(2, 0)
    m3 = Ms_for_n.get(3, 0)
    
    binom_part = (n - 1) * (n - 2) # 2 * C(n-1, 2)
    val = binom_part * (m1 + m2) - 5 * (n - 1) * m2 - 80 * m3
    return val

# --- MAIN LOOP CHECKING EVERY NUMBER ---
N_MAX = 1000
Ms = compute_M_up_to_3(N_MAX)

failures = []
print(f"\n{'N':<5} | {'Type':<10} | {'Detector Value':<20} | {'Status'}")
print("-" * 55)

for n in range(2, N_MAX + 1):
    # 1. Compute Formula
    val = binomial_cubic_detector(n, Ms[n])
    
    # 2. Check Truth
    is_prime = sympy.isprime(n)
    
    # 3. Verify
    passed = False
    if is_prime and val == 0: passed = True
    if not is_prime and val != 0: passed = True
    
    status = "OK" if passed else "FAIL !!!"
    type_str = "PRIME" if is_prime else "Comp"
    
    if not passed:
        failures.append(n)
    
    # PRINT EVERY SINGLE LINE
    print(f"{n:<5} | {type_str:<10} | {val:<20} | {status}")

print("-" * 55)
if len(failures) == 0:
    print(f"VERIFIED: Formula works perfectly for ALL integers 2 to {N_MAX}")
else:
    print(f"FAILED on {len(failures)} numbers: {failures}")
