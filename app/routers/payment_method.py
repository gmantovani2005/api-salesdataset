from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.payment_method import payment_method_crud
from app.schemas.payment_method import PaymentMethodCreate, PaymentMethodRead, PaymentMethodUpdate

router = APIRouter()


@router.get("", response_model=list[PaymentMethodRead])
def list_payment_methods(
    name: str | None = Query(default=None, description="Partial name match (case-insensitive)"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    return payment_method_crud.list_filtered(db, name=name, skip=skip, limit=limit)


@router.post("/", response_model=PaymentMethodRead, status_code=201)
def create_payment_method(payload: PaymentMethodCreate, db: Session = Depends(get_db)):
    return payment_method_crud.create(db, payload)


@router.get("/{id}", response_model=PaymentMethodRead)
def get_payment_method(id: int, db: Session = Depends(get_db)):
    return payment_method_crud.get_or_404(db, id)


@router.patch("/{id}", response_model=PaymentMethodRead)
def update_payment_method(id: int, payload: PaymentMethodUpdate, db: Session = Depends(get_db)):
    obj = payment_method_crud.get_or_404(db, id)
    return payment_method_crud.update(db, obj, payload)


@router.delete("/{id}", response_model=PaymentMethodRead)
def delete_payment_method(id: int, db: Session = Depends(get_db)):
    return payment_method_crud.delete(db, id)
