#!/usr/bin/env python3
"""
🎯 PROBLEM 6: Create Your Own @timer Decorator
================================================

Now you'll create a REAL decorator that measures how long functions take!

TODO: Create a @timer decorator

Your decorator should:
    1. Import time module
    2. Start timer before calling function
    3. Call the function
    4. End timer after function finishes
    5. Print how long it took
    6. Return the function's result

Task:
    1. Create a timer decorator (follow the structure below)
    2. Apply @timer to slow_function
    3. Call slow_function()

Expected output:
    Function slow_function took 0.50s
    Done!

Remember:
    - import time at the top
    - time.time() gives current time
    - end - start = elapsed time
    - Return result from the function!

Structure hint:
    import time

    def timer(func):
        def wrapper():
            start = time.time()
            result = func()
            end = time.time()
            print(f"Function {func.__name__} took {end-start:.2f}s")
            return result
        return wrapper

The test function:
    @timer
    def slow_function():
        import time
        time.sleep(0.5)
        return "Done!"
"""

# Your code here:
import time


def timer(func):
    def wrapper():
        start = time.time()
        result = func()
        end = time.time()
        print(f"Function {func.__name__} took {end - start:.2f}s")
        return result

    return wrapper


@timer
def slow_function():
    time.sleep(3)
    return "Done!"


slow_function()
