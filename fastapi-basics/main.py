#!/usr/bin/env python3
"""
🎯 PROBLEM 4: Request Bodies (POST with Pydantic)
=================================================

TODO: Create a POST route that accepts JSON data

FastAPI uses Pydantic models for request validation:
    - Auto-validates JSON against your model
    - Auto-converts types
    - Returns 422 if validation fails
    - Provides autocomplete in docs

Task:
    1. Import BaseModel from pydantic
    2. Create a User model with name (str) and email (str)
    3. Create a POST /users route that accepts User model
    4. Return the received data

Expected request body:
    {
        "name": "John",
        "email": "john@example.com"
    }

Expected response:
    {
        "name": "John",
        "email": "john@example.com"
    }

Remember:
    - from pydantic import BaseModel
    - class User(BaseModel): ...
    - async def create_user(user: User): ...

vs Express:
    app.post('/users', (req, res) => {
        const { name, email } = req.body;  // Manual, no validation!
        res.json({ name, email });
    });
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# Pydantic model for validation
class User(BaseModel):
    name: str
    email: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id, "doubled": user_id * 2}


@app.post("/users")
async def create_user(user: User):
    return user


@app.get("/items")
async def get_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}


# Your code here - add POST /users route:
