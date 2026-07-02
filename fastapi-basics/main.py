#!/usr/bin/env python3
"""
🎯 PROBLEM 2: Path Parameters
================================

TODO: Create a route that accepts a user_id parameter

Steps:
1. Import FastAPI
2. Create app instance
3. Add route "/users/{user_id}" that returns the user_id
4. Type hint user_id as int

Remember:
- {user_id} in path = parameter (like :id in Express)
- Function parameter must match path parameter name
- FastAPI auto-converts to int (if you type hint it!)

Expected response when visiting http://localhost:8000/users/123:
    {"user_id": 123, "doubled": 246}

vs Express:
    app.get('/users/:id', (req, res) => {
        const id = parseInt(req.params.id);
        res.json({ id, doubled: id * 2 });
    });
"""

# Your code here:
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id, "doubled": user_id * 2}
