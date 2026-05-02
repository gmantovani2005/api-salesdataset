from decimal import Decimal

from sqlalchemy.orm import Session

from app.crud.base import BaseCRUD
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductCRUD(BaseCRUD[Product, ProductCreate, ProductUpdate]):
    def list_filtered(
        self,
        db: Session,
        *,
        name: str | None = None,
        category_id: int | None = None,
        min_price: Decimal | None = None,
        max_price: Decimal | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Product]:
        filters = []
        if name:
            filters.append(Product.name.ilike(f"%{name}%"))
        if category_id is not None:
            filters.append(Product.category_id == category_id)
        if min_price is not None:
            filters.append(Product.unit_price >= min_price)
        if max_price is not None:
            filters.append(Product.unit_price <= max_price)
        return self.list(db, skip=skip, limit=limit, filters=filters or None)


product_crud = ProductCRUD(Product)
