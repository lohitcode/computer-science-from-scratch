#!/usr/bin/env python3
"""
🎯 PROBLEM 1: Your First FastAPI Route
========================================

TODO: Create a FastAPI app with a GET route that returns a greeting

Steps:
1. Import FastAPI from fastapi
2. Create app instance: app = FastAPI()
3. Add a GET route "/" that returns {"message": "Hello World"}
4. Run it with: uvicorn main:app --reload

Remember:
- @app.get("/") defines a GET route (like app.get() in Express)
- async def makes it async (like async in JS)
- Return a dict (like res.json() in Express)

Expected response when visiting http://localhost:8000/:
    {"message": "Hello World"}

Run command:
    uvicorn main:app --reload
"""

# Your code here:
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
