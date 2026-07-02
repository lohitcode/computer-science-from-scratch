"""
CRUD operations - Create, Read, Update, Delete

These functions handle database operations.
Separating CRUD from routes keeps code clean and testable.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app import models, schemas


# ===== User CRUD =====

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """Get a user by ID"""
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Get a user by email"""
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    """Get all users with pagination"""
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Create a new user (password should be hashed before calling)"""
    # TODO: Add password hashing in Problem 5
    db_user = models.User(
        email=user.email,
        name=user.name,
        hashed_password=user.password  # Plain text for now - fix later!
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> Optional[models.User]:
    """Update an existing user"""
    db_user = get_user(db, user_id)
    if not db_user:
        return None

    # Update fields that were provided
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> Optional[models.User]:
    """Delete a user"""
    db_user = get_user(db, user_id)
    if not db_user:
        return None

    db.delete(db_user)
    db.commit()
    return db_user


# ===== Item CRUD =====

def get_item(db: Session, item_id: int) -> Optional[models.Item]:
    """Get an item by ID"""
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[models.Item]:
    """Get all items with pagination"""
    return db.query(models.Item).offset(skip).limit(limit).all()


def get_items_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> List[models.Item]:
    """Get all items owned by a specific user"""
    return db.query(models.Item).filter(models.Item.owner_id == owner_id).offset(skip).limit(limit).all()


def create_item(db: Session, item: schemas.ItemCreate, owner_id: int) -> models.Item:
    """Create a new item"""
    db_item = models.Item(**item.model_dump(), owner_id=owner_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: int, item_update: schemas.ItemUpdate) -> Optional[models.Item]:
    """Update an existing item"""
    db_item = get_item(db, item_id)
    if not db_item:
        return None

    # Update fields that were provided
    update_data = item_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)

    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int) -> Optional[models.Item]:
    """Delete an item"""
    db_item = get_item(db, item_id)
    if not db_item:
        return None

    db.delete(db_item)
    db.commit()
    return db_item


def search_items(db: Session, query: str, skip: int = 0, limit: int = 100) -> List[models.Item]:
    """Search items by title or description"""
    return db.query(models.Item).filter(
        or_(
            models.Item.title.ilike(f"%{query}%"),
            models.Item.description.ilike(f"%{query}%")
        )
    ).offset(skip).limit(limit).all()
