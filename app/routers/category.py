from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.category import category_crud
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate

router = APIRouter()


@router.get("", response_model=list[CategoryRead])
def list_categories(
    name: str | None = Query(default=None, description="Partial name match (case-insensitive)"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    return category_crud.list_filtered(db, name=name, skip=skip, limit=limit)


@router.post("/", response_model=CategoryRead, status_code=201)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    return category_crud.create(db, payload)


@router.get("/{id}", response_model=CategoryRead)
def get_category(id: int, db: Session = Depends(get_db)):
    return category_crud.get_or_404(db, id)


@router.patch("/{id}", response_model=CategoryRead)
def update_category(id: int, payload: CategoryUpdate, db: Session = Depends(get_db)):
    obj = category_crud.get_or_404(db, id)
    return category_crud.update(db, obj, payload)


@router.delete("/{id}", response_model=CategoryRead)
def delete_category(id: int, db: Session = Depends(get_db)):
    return category_crud.delete(db, id)
