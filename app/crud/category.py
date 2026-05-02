from sqlalchemy.orm import Session

from app.crud.base import BaseCRUD
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryCRUD(BaseCRUD[Category, CategoryCreate, CategoryUpdate]):
    def list_filtered(
        self,
        db: Session,
        *,
        name: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Category]:
        filters = []
        if name:
            filters.append(Category.name.ilike(f"%{name}%"))
        return self.list(db, skip=skip, limit=limit, filters=filters or None)


category_crud = CategoryCRUD(Category)
