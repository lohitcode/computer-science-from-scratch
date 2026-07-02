# Lesson 4: Classes & Type Hints

## 🔵 Type Hints (Critical for FastAPI!)

Python 3.5+ supports optional type hints:

```python
def greet(name: str) -> str:
    return f"Hello, {name}"

def calculate(a: int, b: int) -> int:
    return a + b
```

## 🔵 Classes

```python
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def greet(self) -> str:
        return f"Hi, I'm {self.name}"

# Use it
user = User("John", "john@example.com")
print(user.greet())
```

## 🔵 Pydantic Models (Used in FastAPI!)

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int = 18  # default value
```

## Completed Problems

- ✅ Problem 12: Function with type hints
