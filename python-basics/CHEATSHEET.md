# 🐍 Python for JavaScript Developers - Quick Reference

**Save this for later!**

---

## 📋 Naming Conventions (CRITICAL)

```python
# ✅ CORRECT
user_name = "John"           # Variables: snake_case
def get_user():              # Functions: snake_case
class UserProfile:           # Classes: PascalCase
MAX_RETRIES = 3              # Constants: UPPER_SNAKE_CASE

# ❌ WRONG (JavaScript style)
userName = "John"             # Don't use camelCase!
def GetUser():               # Don't use PascalCase for functions!
```

---

## 🔤 Variables & Types

```python
# No let/const keywords
name = "John"                 # Can be reassigned
MAX_SIZE = 100               # Constant (convention only)

# Types
text = "Hello"                # str
count = 42                    # int
price = 19.99                 # float
is_active = True              # bool
nothing = None                # None (like null)

# F-strings (like template literals)
name = "John"
age = 30
message = f"Hello, {name}, you are {age}"
```

---

## 🎛️ Operators

```python
# JavaScript → Python
&&        → and
||        → or
!         → not
===       → ==
null      → None
true/false → True/False
```

---

## 📞 Functions

```python
def greet(name: str, age: int = 18) -> str:
    """Function with type hints"""
    return f"Hello {name}, age {age}"

# Multiple return values (returns tuple)
def get_user():
    return "John", 30         # Returns ("John", 30)

name, age = get_user()        # Unpacking

# Lambda (arrow functions)
add = lambda a, b: a + b
```

---

## 🔄 Loops

```python
# Range loop (like for(let i=0; i<5; i++))
for i in range(5):
    print(i)                  # 0, 1, 2, 3, 4

# Loop over list (like for item of array)
fruits = ["apple", "banana"]
for fruit in fruits:
    print(fruit)

# With index (like forEach with index)
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")

# List comprehension (like map/filter)
numbers = [1, 2, 3, 4, 5]
evens = [n for n in numbers if n % 2 == 0]
```

---

## 📦 Data Structures

```python
# List (like Array)
items = [1, 2, 3]
items.append(4)              # Push
items.pop()                   # Pop
items[0]                      # Access
items[-1]                     # Last item
items[1:3]                    # Slice [1, 3)

# Dictionary (like Object)
user = {
    "name": "John",
    "age": 30
}
user["email"] = "john@example.com"  # Add/set
user.get("phone", "N/A")             # Safe get
del user["age"]                      # Delete

# Set (like Set)
unique = set([1, 2, 2, 3])    # {1, 2, 3}
unique.add(4)
unique.remove(2)

# Tuple (immutable, no JS equivalent)
coords = (10, 20)             # Can't change!
x, y = coords                 # Unpacking
```

---

## 🎯 Conditionals

```python
if score > 90:
    grade = "A"
elif score > 80:              # else if
    grade = "B"
else:
    grade = "C"

# Ternary
message = "Pass" if score > 50 else "Fail"
```

---

## ⚠️ Error Handling

```python
try:
    result = int("invalid")
except ValueError as e:        # Specific error
    print(f"Error: {e}")
except Exception as e:         # Catch-all
    print(f"Unexpected: {e}")
finally:                       # Always runs
    print("Cleanup")

# Raising errors
def validate_age(age):
    if age < 0:
        raise ValueError("Age can't be negative")
```

---

## ⏱️ Async/Await

```python
import asyncio

async def fetch_data():
    await asyncio.sleep(1)     # Like await
    return "data"

async def main():
    # Sequential
    result = await fetch_data()

    # Parallel
    results = await asyncio.gather(
        fetch_data(),
        fetch_data()
    )

asyncio.run(main())
```

---

## 📦 Classes

```python
class User:
    def __init__(self, name, email):  # Constructor
        self.name = name
        self.email = email

    def greet(self):                  # Method
        return f"Hi, {self.name}"

    def __repr__(self):               # toString
        return f"User({self.name})"

# With type hints
class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def get_discounted(self, pct: float) -> float:
        return self.price * (1 - pct/100)
```

---

## 🎯 Common Patterns

```python
# Loop through dict with key/value
for key, value in user_dict.items():
    print(f"{key}: {value}")

# Check if in list/set
if item in my_list:
    print("Found!")

# Get with default
value = my_dict.get("key", "default")

# String formatting
name = "John"
print(f"Hello {name}")              # F-string (preferred)
print("Hello {}".format(name))      # Format
print("Hello " + name)              # Concatenation

# List operations
my_list = [1, 2, 3]
len(my_list)                        # Length
my_list.extend([4, 5])              # Add multiple
my_list.index(2)                    # Find index
```

---

## 🚀 Ready for FastAPI?

If you know all this, you're ready for FastAPI!

**Next:**
1. Install FastAPI: `pip install fastapi uvicorn`
2. Learn basic routes
3. Build AI API

---

**Keep this cheat sheet handy!** 📌
