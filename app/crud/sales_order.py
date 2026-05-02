import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.crud.base import BaseCRUD
from app.models.sales_order import SalesOrder
from app.schemas.sales_order import SalesOrderCreate, SalesOrderUpdate


class SalesOrderCRUD(BaseCRUD[SalesOrder, SalesOrderCreate, SalesOrderUpdate]):
    def list_filtered(
        self,
        db: Session,
        *,
        product_id: int | None = None,
        region_id: int | None = None,
        payment_method_id: int | None = None,
        date_from: datetime.date | None = None,
        date_to: datetime.date | None = None,
        min_total: Decimal | None = None,
        max_total: Decimal | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[SalesOrder]:
        filters = []
        if product_id is not None:
            filters.append(SalesOrder.product_id == product_id)
        if region_id is not None:
            filters.append(SalesOrder.region_id == region_id)
        if payment_method_id is not None:
            filters.append(SalesOrder.payment_method_id == payment_method_id)
        if date_from is not None:
            filters.append(SalesOrder.date >= date_from)
        if date_to is not None:
            filters.append(SalesOrder.date <= date_to)
        if min_total is not None:
            filters.append(SalesOrder.total_revenue >= min_total)
        if max_total is not None:
            filters.append(SalesOrder.total_revenue <= max_total)
        return self.list(db, skip=skip, limit=limit, filters=filters or None)


sales_order_crud = SalesOrderCRUD(SalesOrder)
