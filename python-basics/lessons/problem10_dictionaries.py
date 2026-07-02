#!/usr/bin/env python3
"""
🎯 PROBLEM 10: Dictionaries
=============================

TODO:
1. Add a new key "email" with value "john@example.com"
2. Print the user's name

Given: user = {"name": "John", "age": 30}

Remember:
- Use dict[key] = value to add/update
- Use dict[key] or dict.get(key) to access

Expected output:
    John
"""

user = {"name": "John", "age": 30}

user["email"] = "john@example.com"

print(user.get("name"))

# Your code here:
