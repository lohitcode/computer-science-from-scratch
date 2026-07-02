#!/usr/bin/env python3
"""
🎯 PROBLEM 8: List Comprehension
================================

TODO: Create a new list with each number squared
Given: numbers = [1, 2, 3, 4, 5]
Result should be: [1, 4, 9, 16, 25]

Remember:
- List comprehension: [expression for item in list]
- Use ** or pow() for squaring

Expected output:
    [1, 4, 9, 16, 25]
"""

numbers = [1, 2, 3, 4, 5]

# Your code here:
square = [n * n for n in numbers]

print(square)
