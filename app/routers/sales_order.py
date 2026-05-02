import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.sales_order import sales_order_crud
from app.schemas.sales_order import SalesOrderCreate, SalesOrderRead, SalesOrderUpdate

router = APIRouter()


@router.get("", response_model=list[SalesOrderRead])
def list_sales_orders(
    product_id: int | None = Query(default=None, description="Filter by product ID"),
    region_id: int | None = Query(default=None, description="Filter by region ID"),
    payment_method_id: int | None = Query(default=None, description="Filter by payment method ID"),
    date_from: datetime.date | None = Query(default=None, description="Orders from this date (inclusive)"),
    date_to: datetime.date | None = Query(default=None, description="Orders up to this date (inclusive)"),
    min_total: Decimal | None = Query(default=None, description="Minimum total revenue"),
    max_total: Decimal | None = Query(default=None, description="Maximum total revenue"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    return sales_order_crud.list_filtered(
        db,
        product_id=product_id,
        region_id=region_id,
        payment_method_id=payment_method_id,
        date_from=date_from,
        date_to=date_to,
        min_total=min_total,
        max_total=max_total,
        skip=skip,
        limit=limit,
    )


@router.post("/", response_model=SalesOrderRead, status_code=201)
def create_sales_order(payload: SalesOrderCreate, db: Session = Depends(get_db)):
    return sales_order_crud.create(db, payload)


@router.get("/{id}", response_model=SalesOrderRead)
def get_sales_order(id: int, db: Session = Depends(get_db)):
    return sales_order_crud.get_or_404(db, id)


@router.patch("/{id}", response_model=SalesOrderRead)
def update_sales_order(id: int, payload: SalesOrderUpdate, db: Session = Depends(get_db)):
    obj = sales_order_crud.get_or_404(db, id)
    return sales_order_crud.update(db, obj, payload)


@router.delete("/{id}", response_model=SalesOrderRead)
def delete_sales_order(id: int, db: Session = Depends(get_db)):
    return sales_order_crud.delete(db, id)
