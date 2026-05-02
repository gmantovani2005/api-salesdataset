from sqlalchemy.orm import Session

from app.crud.base import BaseCRUD
from app.models.payment_method import PaymentMethod
from app.schemas.payment_method import PaymentMethodCreate, PaymentMethodUpdate


class PaymentMethodCRUD(BaseCRUD[PaymentMethod, PaymentMethodCreate, PaymentMethodUpdate]):
    def list_filtered(
        self,
        db: Session,
        *,
        name: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[PaymentMethod]:
        filters = []
        if name:
            filters.append(PaymentMethod.name.ilike(f"%{name}%"))
        return self.list(db, skip=skip, limit=limit, filters=filters or None)


payment_method_crud = PaymentMethodCRUD(PaymentMethod)
