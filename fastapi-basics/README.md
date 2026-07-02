# FastAPI for Express/Hono Developers

**Current: Lesson 2 - Path Parameters**

---

## 📚 Quick Reference

For full lesson content, see: **[lessons/02-path-parameters.md](lessons/02-path-parameters.md)**

Previous lessons:
- **[lessons/01-your-first-api.md](lessons/01-your-first-api.md)**
- **[lessons/00-fundamentals.md](lessons/00-fundamentals.md)** - What is FastAPI?
- **[lessons/00-virtual-environments.md](lessons/00-virtual-environments.md)** - venv guide

---

## 🔵 Path Parameters

**Express:**
```javascript
app.get("/users/:id", (req, res) => {
    const id = req.params.id;
    res.json({ id });
});
```

**FastAPI:**
```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}
```

**No `req.params` - the parameter comes straight into your function!**

---

## 🎯 Type Conversion

FastAPI auto-converts based on type hint:

```python
@app.get("/items/{item_id}")
async def get_item(item_id: int):  # ← Auto converts to int!
    return {"item_id": item_id}
```

**Visit `/items/42` → `{"item_id": 42}` (int, not string!)**

**Visit `/items/abc` → `422 Unprocessable Entity` (auto validation!)**

---

**See `main.py` for your current exercise!**
