# Lesson 2: Path Parameters

## 🎯 Learning Goals

- Define path parameters (dynamic segments in URL)
- Type hints for automatic conversion
- Auto-validation when wrong type passed

---

## 🔵 What Are Path Parameters?

**Path parameters = Dynamic parts of URL**

```
/users/123        → 123 is the parameter
/posts/abc/comments/456  → abc and 456 are parameters
```

---

## 📊 Express vs FastAPI

**Express:**
```javascript
app.get('/users/:userId', (req, res) => {
    const id = req.params.userId;  // Extract from req.params
    res.json({ userId: id });
});
```

**FastAPI:**
```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}  # Parameter comes directly!
```

**Key differences:**
- Express: `req.params.userId` (extract from request)
- FastAPI: `user_id` (direct function parameter)

---

## 🎯 Type Hints = Auto Conversion

**FastAPI converts based on type hint:**

```python
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    # item_id is automatically an int!
    return {"item_id": item_id, "doubled": item_id * 2}
```

**Examples:**

| Request | Result |
|---------|--------|
| `/items/42` | `{"item_id": 42, "doubled": 84}` |
| `/items/abc` | `422 Unprocessable Entity` (error!) |

**Without type hint:**
```python
@app.get("/items/{item_id}")  # No type hint
async def get_item(item_id):   # item_id is str!
    return {"item_id": item_id}  # Returns "42" not 42
```

---

## 🔢 Multiple Parameters

```python
@app.get("/users/{user_id}/posts/{post_id}")
async def get_post(user_id: int, post_id: int):
    return {
        "user_id": user_id,
        "post_id": post_id
    }
```

**Request:** `/users/123/posts/456`
**Response:** `{"user_id": 123, "post_id": 456}`

---

## 🎯 Common Types

```python
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    pass

@app.get("/users/{username}")
async def get_user(username: str):
    pass

@app.get("/products/{sku}")
async def get_product(sku: str):
    pass

# Float works too
@app.get("/price/{amount}")
async def get_price(amount: float):
    return {"price": amount, "with_tax": amount * 1.1}
```

---

## ⚠️ Parameter Name Must Match

```python
@app.get("/users/{user_id}")      # ← user_id
async def get_user(uid: int):      # ← uid (WRONG!)
    # This won't work - names must match!
```

**Correct:**
```python
@app.get("/users/{user_id}")      # ← user_id
async def get_user(user_id: int):  # ← user_id (MATCH!)
    return {"user_id": user_id}
```

---

## 🚀 Auto Validation

**FastAPI validates for you:**

```python
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"item_id": item_id}
```

| Request | Result |
|---------|--------|
| `/items/42` | ✅ `200 {"item_id": 42}` |
| `/items/abc` | ❌ `422 {"detail":...}` |

**The error response:**
```json
{
  "detail": [
    {
      "type": "int_parsing",
      "msg": "Input should be a valid integer",
      "loc": ["path", "item_id"]
    }
  ]
}
```

**Built-in validation - no extra code needed!**

---

## 📊 Summary

| Concept | Express | FastAPI |
|---------|---------|---------|
| Define param | `:userId` | `{user_id}` |
| Access value | `req.params.userId` | Function parameter |
| Type conversion | Manual `parseInt()` | Type hint |
| Validation | Manual | Auto |

---

## ✅ You Now Know:

- ✅ How to define path parameters with `{param}`
- ✅ How type hints auto-convert values
- ✅ How FastAPI validates automatically
- ✅ Multiple parameters in one path

**Next:** Query parameters, optional parameters, and request bodies!
