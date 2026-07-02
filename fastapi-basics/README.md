# FastAPI for Express/Hono Developers

**Current: Lesson 3 - Query Parameters**

---

## 📚 Quick Reference

For full lesson content, see: **[lessons/03-query-parameters.md](lessons/03-query-parameters.md)**

Previous lessons:
- **[lessons/01-your-first-api.md](lessons/01-your-first-api.md)**
- **[lessons/02-path-parameters.md](lessons/02-path-parameters.md)**
- **[lessons/00-fundamentals.md](lessons/00-fundamentals.md)** - What is FastAPI?
- **[lessons/00-virtual-environments.md](lessons/00-virtual-environments.md)** - venv guide

---

## 🔵 Query Parameters

**Query parameters = The `?key=value` part of URLs**

**Express:**
```javascript
app.get('/items', (req, res) => {
    const { skip = 0, limit = 10 } = req.query;
    res.json({ skip, limit });
});
```

**FastAPI:**
```python
@app.get("/items")
async def get_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

**Query params are just function parameters with default values!**

---

## 📊 Path vs Query Parameters

| Type | URL Example | FastAPI Syntax |
|------|-------------|----------------|
| **Path** | `/users/123` | `{user_id}` in path |
| **Query** | `/items?skip=0&limit=10` | Function parameter with default |

---

**See `main.py` for your current exercise!**
