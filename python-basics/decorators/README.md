# Lesson 6: Decorators - The `@` Syntax

**Current: Problem 1 - Functions Are Values**

---

## 🎯 Learning Decorators Step by Step

**Decorator = A function that modifies another function**

Think of it like **middleware for functions** - just like Express middleware, but for individual functions.

---

## 📚 What You'll Learn

1. **Functions are values** (can be assigned, passed, returned)
2. **Functions can return functions**
3. **Functions can take functions as arguments**
4. **Putting it all together → Decorators!**
5. **The `@` syntax**
6. **Creating your own decorators**

---

## 🔵 Why Decorators Matter for FastAPI

FastAPI uses decorators EVERYWHERE:

```python
@app.get("/")              # This is a decorator!
async def root():
    return {"message": "Hello"}
```

**Understanding decorators = Understanding FastAPI!**

---

## 📋 Interactive Problems

You'll solve 5 problems, one at a time:

1. **Functions are values** - Understanding functions as objects
2. **Functions returning functions** - Higher-order functions
3. **Functions taking functions** - Callbacks
4. **Your first decorator** - Putting it all together
5. **The `@` syntax** - Making it clean
6. **Practical decorator** - Build a @timer decorator

---

**See `main.py` for your current problem!**
