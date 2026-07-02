# Lesson 1: Variables & Types

## 🔵 Variables

Coming from JavaScript:
- **JavaScript:** `let x = 1;` or `const x = 1;`
- **Python:** `x = 1` (no keywords!)

## 🔤 Basic Types

```python
text = "Hello"           # str
count = 42               # int
price = 19.99            # float
is_active = True         # bool (capitalized!)
nothing = None           # None (like null in JS)
```

## 🔤 Type Conversion

```python
# String to number
num = int("42")          # 42

# Number to string
text = str(42)           # "42"

# Float to int (truncates!)
price_int = int(19.99)   # 19
```

## 💬 F-Strings

```python
# JavaScript: `Hello, ${name}, you are ${age}`
# Python: f"Hello, {name}, you are {age}"

name = "John"
age = 25
message = f"Hello, {name}, you are {age}"
```

## 🎯 Naming Conventions

```python
# ✅ Variables: snake_case
user_name = "John"

# ✅ Constants: UPPER_SNAKE_CASE
MAX_USERS = 1000

# ❌ WRONG: camelCase
userName = "John"  # Don't do this!
```

## ⚖️ Operators

| JavaScript | Python |
|------------|--------|
| `&&` | `and` |
| `||` | `or` |
| `!` | `not` |
| `null` | `None` |
| `true/false` | `True/False` |

## Completed Problems

- ✅ Problem 1: Create variables (`user_age = 30`)
- ✅ Problem 2: Constants (`MAX_USERS = 1000`)
- ✅ Problem 3: F-strings (print full name)
- ✅ Problem 4: Type conversion
