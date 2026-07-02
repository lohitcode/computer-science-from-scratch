#!/usr/bin/env python3
"""
🎯 PROBLEM 6: Conditionals (if/elif/else)
==========================================

TODO: Write code that:
- If age is less than 18, print "Minor"
- If age is 18-64, print "Adult"
- If age is 65 or more, print "Senior"

The variable 'age' is already set to 25

Remember:
- Use 'if', 'elif', 'else'
- Use ':' after each condition
- Indent the code block
- No parentheses needed around conditions

Expected output (with age=25):
    Adult
"""

age = 25

if age < 18:
    print("Minor")
elif age < 65:
    print("Adult")
else:
    print("Senior")
