# Python for JavaScript Developers

**Current: Lesson 6 - Decorators (Essential for FastAPI!)**

---

## 📚 Quick Reference

For full lesson content, see: **[lessons/06-decorators.md](lessons/06-decorators.md)**

Previous lessons:
- **[lessons/01-variables-types.md](lessons/01-variables-types.md)** - Variables, types, f-strings
- **[lessons/02-functions-control-flow.md](lessons/02-functions-control-flow.md)** - Functions, conditionals, loops
- **[lessons/03-data-structures.md](lessons/03-data-structures.md)** - Lists, dicts, sets, tuples
- **[lessons/04-classes-type-hints.md](lessons/04-classes-type-hints.md)** - Classes, type hints, Pydantic
- **[lessons/05-async-error-handling.md](lessons/05-async-error-handling.md)** - Try/except, async/await, context managers
- **[lessons/06-decorators.md](lessons/06-decorators.md)** - The `@` syntax (FastAPI uses this!)

---

## 🔵 Decorators: The `@` Syntax

**Decorator = A function that modifies another function**

**Express middleware vs Python decorator:**

```javascript
// Express
app.get("/", (req, res) => {
    res.json({ message: "Hello" });
});
```

```python
# FastAPI
@app.get("/")
async def root():
    return {"message": "Hello"}
```

**`@app.get("/")` is a decorator!** It registers your function for the GET `/` route.

---

## 🎯 Why Decorators Matter for FastAPI

FastAPI uses decorators EVERYWHERE:

```python
@app.get("/")              # Route decorator
@app.post("/users")         # Route decorator
@app.delete("/items/{id}")  # Route decorator
```

**Every route definition uses the `@` syntax!**

---

**See `lessons/06-decorators.md` for the complete guide!**

**Now you're ready for FastAPI!** 🚀
