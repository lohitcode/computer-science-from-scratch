# Lesson 5: Async & Error Handling

## 🔵 Try/Except (Error Handling)

```python
try:
    result = int("invalid")
except ValueError as e:
    print(f"Error: {e}")
```

## 🔵 Raising Exceptions

```python
def validate_age(age: int):
    if age < 0:
        raise ValueError("Age can't be negative")
```

## 🔵 Async/Await

```python
import asyncio

async def fetch_data():
    await asyncio.sleep(1)
    return "data"

async def main():
    result = await fetch_data()

asyncio.run(main())
```

## Completed Problems

- ✅ Problem 14: Try/Except
- ✅ Problem 15: Async Function
- ✅ Problem 16: Context Manager
