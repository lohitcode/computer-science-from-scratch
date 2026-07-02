"""
Item routes - CRUD operations for items
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/items", tags=["items"])


@router.post("/", response_model=schemas.ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: schemas.ItemCreate, owner_id: int = Query(...), db: Session = Depends(get_db)):
    """
    Create a new item.

    - **title**: Item title
    - **description**: Item description (optional)
    - **owner_id**: ID of the user who owns this item
    """
    return crud.create_item(db=db, item=item, owner_id=owner_id)


@router.get("/", response_model=List[schemas.ItemResponse])
def get_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all items with pagination.

    - **skip**: Number of items to skip (for pagination)
    - **limit**: Maximum number of items to return
    """
    return crud.get_items(db, skip=skip, limit=limit)


@router.get("/search", response_model=List[schemas.ItemResponse])
def search_items(q: str = Query(..., min_length=1), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Search items by title or description.

    - **q**: Search query
    - **skip**: Number of items to skip
    - **limit**: Maximum number of items to return
    """
    return crud.search_items(db, query=q, skip=skip, limit=limit)


@router.get("/{item_id}", response_model=schemas.ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """
    Get a specific item by ID.

    - **item_id**: The item's ID
    """
    db_item = crud.get_item(db, item_id=item_id)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return db_item


@router.get("/owner/{owner_id}", response_model=List[schemas.ItemResponse])
def get_items_by_owner(owner_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all items owned by a specific user.

    - **owner_id**: The user's ID
    - **skip**: Number of items to skip
    - **limit**: Maximum number of items to return
    """
    return crud.get_items_by_owner(db, owner_id=owner_id, skip=skip, limit=limit)


@router.patch("/{item_id}", response_model=schemas.ItemResponse)
def update_item(item_id: int, item_update: schemas.ItemUpdate, db: Session = Depends(get_db)):
    """
    Update an item.

    - **item_id**: The item's ID
    - Only provided fields will be updated
    """
    db_item = crud.update_item(db, item_id=item_id, item_update=item_update)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return db_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """
    Delete an item.

    - **item_id**: The item's ID
    """
    db_item = crud.delete_item(db, item_id=item_id)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return None  # 204 No Content
