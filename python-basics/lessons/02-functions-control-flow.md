# Lesson 2: Functions & Control Flow

## 🔵 Functions

Coming from JavaScript:
- **JavaScript:** `function greet(name) { return \`Hello, \${name}\`; }`
- **Python:** `def greet(name): return f"Hello, {name}"`

## 🎯 Function Syntax

```python
def greet(name: str, age: int = 18) -> str:
    """Function with type hints"""
    return f"Hello, {name}, age {age}"

# Call it
result = greet("John")
```

## 🔄 Multiple Return Values

Python can return multiple values (as a tuple):

```python
def get_user():
    return "John", 30  # Returns ("John", 30)

name, age = get_user()  # Unpacking!
```

## 🎛️ Conditionals

```python
# JavaScript: if (score > 90) { } else if (score > 80) { } else { }
# Python:
if score > 90:
    grade = "A"
elif score > 80:    # else if
    grade = "B"
else:
    grade = "C"
```

## 🔄 Loops

```python
# JavaScript: for (let i = 0; i < 5; i++)
# Python:
for i in range(5):    # 0, 1, 2, 3, 4
    print(i)

# Loop over list (like for...of)
fruits = ["apple", "banana"]
for fruit in fruits:
    print(fruit)

# With index (like forEach with index)
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")
```

## 📋 List Comprehensions

Like `map()` and `filter()` in JavaScript:

```python
# JavaScript: numbers.map(n => n * 2)
# Python:
numbers = [1, 2, 3, 4, 5]
doubled = [n * 2 for n in numbers]

# JavaScript: numbers.filter(n => n % 2 === 0)
# Python:
evens = [n for n in numbers if n % 2 == 0]
```

## 🎯 Operators

| JavaScript | Python |
|------------|--------|
| `&&` | `and` |
| `||` | `or` |
| `!` | `not` |
| `? :` | `x if cond else y` |

## Completed Problems

- ✅ Problem 5: Basic function
