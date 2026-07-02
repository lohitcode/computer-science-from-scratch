# FastAPI for Express/Hono Developers

**Current: Lesson 1 - Your First API**

---

## 📚 Quick Reference

For full lesson content, see: **[lessons/01-your-first-api.md](lessons/01-your-first-api.md)**

---

## 🔵 Your First FastAPI App

FastAPI is like Express/Hono but with:
- **Built-in type validation** (Pydantic)
- **Auto-generated docs** (Swagger UI)
- **Async/await by default**

**JavaScript (Express):**
```javascript
app.get("/", (req, res) => {
  res.json({ message: "Hello" });
});
```

**Python (FastAPI):**
```python
@app.get("/")
async def root():
    return {"message": "Hello"}
```

---

## 📦 Setup (One Time)

```bash
pip install fastapi uvicorn
```

---

## ▶️ Run Your App

```bash
uvicorn main:app --reload
```

Then visit: http://localhost:8000/docs

---

**See `main.py` for your first exercise!**
