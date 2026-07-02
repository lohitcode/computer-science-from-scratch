# Lesson 1: Your First FastAPI API

## 🎯 Learning Goals

- Understand FastAPI basics
- Create your first route
- Run the server
- See auto-generated docs

---

## 🔵 What is FastAPI?

**FastAPI = Express + Zod + Swagger Docs**

| Feature | Express/Hono | FastAPI |
|---------|-------------|---------|
| Routes | `app.get()` | `@app.get()` |
| Validation | Manual/Zod | Built-in (Pydantic) |
| Docs | Manual | Auto-generated |
| Async | Optional | Native |

---

## 📦 Installation

```bash
pip install fastapi uvicorn
```

- **fastapi**: The framework
- **uvicorn**: The server (like node's http server)

---

## 🔵 Your First App

**main.py:**
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

**Run it:**
```bash
uvicorn main:app --reload
```

- `main:app` = file `main.py`, variable `app`
- `--reload` = auto-restart on changes (like nodemon)

---

## 🎯 Routes (The Basics)

```python
from fastapi import FastAPI

app = FastAPI()

# GET /
@app.get("/")
async def root():
    return {"message": "Hello"}

# GET /users/123
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}

# POST /users
@app.post("/users")
async def create_user(user: dict):
    return {"created": user}
```

**vs Express:**
```javascript
app.get("/", (req, res) => res.json({message: "Hello"}));
app.get("/users/:id", (req, res) => res.json({id: req.params.id}));
app.post("/users", (req, res) => res.json(req.body));
```

---

## 📚 Auto-Generated Docs

Visit these URLs:

| URL | What |
|-----|------|
| `http://localhost:8000/docs` | Swagger UI (interactive!) |
| `http://localhost:8000/redoc` | ReDoc (pretty docs) |

**No extra work needed!** FastAPI reads your type hints and generates docs.

---

## 🎯 Key Differences from Express

| Express | FastAPI | Why? |
|---------|---------|------|
| `req, res` params | Just return dict | Cleaner |
| `res.json()` | `return {"key": val}` | Pythonic |
| `req.params.id` | Function param | Type-safe! |
| `req.body` | Pydantic model | Validated! |
| Manual validation | Auto validation | Less code |

---

## 🚀 Next Steps

After this lesson, you'll know:
- ✅ How to create a FastAPI app
- ✅ How to define routes
- ✅ How to run the server
- ✅ Where to find auto docs

**Next:** Path parameters, query params, and request bodies!
