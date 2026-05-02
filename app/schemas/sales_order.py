import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class SalesOrderBase(BaseModel):
    date: datetime.date
    product_id: int
    region_id: int
    payment_method_id: int
    units_sold: int
    unit_price: Decimal
    total_revenue: Decimal


class SalesOrderCreate(SalesOrderBase):
    id: int


class SalesOrderUpdate(BaseModel):
    date: datetime.date | None = None
    product_id: int | None = None
    region_id: int | None = None
    payment_method_id: int | None = None
    units_sold: int | None = None
    unit_price: Decimal | None = None
    total_revenue: Decimal | None = None


class SalesOrderRead(SalesOrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
