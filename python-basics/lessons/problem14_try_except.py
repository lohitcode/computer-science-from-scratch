#!/usr/bin/env python3
"""
🎯 PROBLEM 14: Try/Except
===========================

TODO: Handle the error when converting invalid string to int
- Use try/except to catch ValueError
- Print "Error: Invalid input" when conversion fails

Remember:
- try: (code that might fail)
- except ValueError as e: (handle the error)

Expected output:
    Error: Invalid input
"""

# Your code here:
try:
    result = int("invalid")
except ValueError as e:
    print("Error: Invalid input")
