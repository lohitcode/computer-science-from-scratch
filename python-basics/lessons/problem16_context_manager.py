#!/usr/bin/env python3
"""
🎯 PROBLEM 16: Context Manager (FINAL PROBLEM!)
==================================================

TODO: Use 'with' statement to open a file and read its content
- Create a file named 'test.txt'
- Write 'Hello, World!' to it
- Read it back using 'with open()'

Remember:
- with open(filename, 'w') as f: for writing
- with open(filename, 'r') as f: for reading
- File closes automatically after with block!

Expected output:
    Content: Hello, World!
"""

import os

# Your code here:
with open("test.txt", "w") as f:
    f.write("Hello, World!")

content = ""
with open("test.txt", "r") as f:
    content = f.read()

print(content)

os.remove("test.txt")
