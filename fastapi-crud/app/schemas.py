from pydantic import BaseModel, EmailStr
from datetime import datetime


# ===== User Schemas =====

class UserBase(BaseModel):
    """Base user fields (shared)"""
    email: EmailStr
    name: str


class UserCreate(UserBase):
    """Schema for creating a user"""
    password: str


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    name: str | None = None
    email: EmailStr | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    """Schema for user response (from DB)"""
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Allow SQLAlchemy model → Pydantic


# ===== Item Schemas =====

class ItemBase(BaseModel):
    """Base item fields (shared)"""
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    """Schema for creating an item"""
    pass


class ItemUpdate(BaseModel):
    """Schema for updating an item"""
    title: str | None = None
    description: str | None = None
    is_active: bool | None = None


class ItemResponse(ItemBase):
    """Schema for item response (from DB)"""
    id: int
    owner_id: int | None = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
