"""
FastAPI CRUD Application with PostgreSQL

Run with: uvicorn app.main:app --reload
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine, Base
from app.core.config import settings
from app.routers import users, items


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager - runs on startup and shutdown.

    Startup: Create database tables
    Shutdown: Cleanup (close DB connections)
    """
    # Startup: Create tables
    Base.metadata.create_all(bind=engine)
    print("🚀 Application startup")
    yield
    # Shutdown
    print("👋 Application shutdown")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="CRUD API with FastAPI and PostgreSQL",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(users.router)
app.include_router(items.router)


@app.get("/")
async def root():
    """Root endpoint - API info"""
    return {
        "message": "FastAPI CRUD API",
        "docs": "/docs",
        "users": "/users",
        "items": "/items"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
