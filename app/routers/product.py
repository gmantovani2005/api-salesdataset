from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.product import product_crud
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate

router = APIRouter()


@router.get("", response_model=list[ProductRead])
def list_products(
    name: str | None = Query(default=None, description="Partial name match (case-insensitive)"),
    category_id: int | None = Query(default=None, description="Filter by category ID"),
    min_price: Decimal | None = Query(default=None, description="Minimum unit price"),
    max_price: Decimal | None = Query(default=None, description="Maximum unit price"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    return product_crud.list_filtered(
        db,
        name=name,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        skip=skip,
        limit=limit,
    )


@router.post("/", response_model=ProductRead, status_code=201)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    return product_crud.create(db, payload)


@router.get("/{id}", response_model=ProductRead)
def get_product(id: int, db: Session = Depends(get_db)):
    return product_crud.get_or_404(db, id)


@router.patch("/{id}", response_model=ProductRead)
def update_product(id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    obj = product_crud.get_or_404(db, id)
    return product_crud.update(db, obj, payload)


@router.delete("/{id}", response_model=ProductRead)
def delete_product(id: int, db: Session = Depends(get_db)):
    return product_crud.delete(db, id)
