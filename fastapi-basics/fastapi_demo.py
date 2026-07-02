#!/usr/bin/env python3
"""
🟢 AFTER: FastAPI Server (The Easy Way)
========================================

This is what writing an API looks like WITH FastAPI.

Run: uvicorn fastapi_demo:app --reload
Visit: http://localhost:8000/
Docs: http://localhost:8000/docs
"""

from fastapi import FastAPI
from typing import List

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users")
async def get_users():
    return {"users": ["Alice", "Bob"]}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    # FastAPI auto-converts user_id to int!
    return {"user_id": user_id, "name": "Alice"}

@app.post("/users")
async def create_user(user: dict):
    # FastAPI auto-parses JSON body!
    return {"created": user}

# Run with: uvicorn fastapi_demo:app --reload
