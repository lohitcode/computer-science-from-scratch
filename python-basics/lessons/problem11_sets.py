#!/usr/bin/env python3
"""
🎯 PROBLEM 11: Sets
====================

TODO: Create a set from the numbers list
Print the set (should only have unique values)

Given: numbers = [1, 2, 2, 3, 3, 3, 4, 5]

Remember:
- set() creates a set from a list
- Sets only store unique values (duplicates removed!)

Expected output:
    {1, 2, 3, 4, 5}
"""

numbers = [1, 2, 2, 3, 3, 3, 4, 5]

unique = list(set(numbers))

print(unique)

# Your code here:
