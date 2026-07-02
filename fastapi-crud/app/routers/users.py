"""
User routes - CRUD operations for users
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas, models

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.

    - **email**: User's email (must be unique)
    - **name**: User's name
    - **password**: User's password
    """
    # Check if email already exists
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    return crud.create_user(db=db, user=user)


@router.get("/", response_model=List[schemas.UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all users with pagination.

    - **skip**: Number of users to skip (for pagination)
    - **limit**: Maximum number of users to return
    """
    return crud.get_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a specific user by ID.

    - **user_id**: The user's ID
    """
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user


@router.patch("/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    """
    Update a user.

    - **user_id**: The user's ID
    - Only provided fields will be updated
    """
    db_user = crud.update_user(db, user_id=user_id, user_update=user_update)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user.

    - **user_id**: The user's ID
    """
    db_user = crud.delete_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return None  # 204 No Content
