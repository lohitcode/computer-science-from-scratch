#!/usr/bin/env python3
"""
🎯 PROBLEM 13: Classes
========================

TODO: Create a 'User' class with:
1. __init__ method that takes name and email
2. A greet() method that returns "Hi, I'm {name}"

Then create an instance and call greet()

Expected output:
    Hi, I'm John
"""


class User:
    def __init__(self, name: str):
        self.name = name

    def greet(self) -> str:
        return f"Hi, I'm {self.name}"


user = User("lohit")
print(user.greet())
