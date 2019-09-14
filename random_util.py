#!/usr/bin/env python3

import random

# get a random number in [0, end), except for [exclude_end - exclude_size, exclude_end).
# uniform distribution.
def restricted(end, exclude_end, exclude_size):
    r = random.randrange(end - exclude_size)
    ans = exclude_end + r
    if ans >= end:
        ans -= end
    return ans

# generates two random numbers in [0, end).
# the second number will not be in [first - pad, first + pad].
def random_pair(end, pad):
    first = random.randrange(end)
    exclude_end = first + pad + 1
    if exclude_end > end:
        exclude_end -= end
    return first, restricted(end, exclude_end, 2 * pad + 1)

