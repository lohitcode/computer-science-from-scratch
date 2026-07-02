#!/usr/bin/env python3
"""
🎯 PROBLEM 12: Type Hints
==========================

TODO: Write a function 'add' with type hints:
- Takes two integers (a, b)
- Returns their sum

Remember type hint syntax:
- def function(param: type) -> return_type:

Expected output:
    8
"""


def add(a: int, b: int) -> int:
    return a + b


ans = add(2, 3)

print(ans)
