from typing import Any, Generic, Type, TypeVar

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import Base

ModelT = TypeVar("ModelT", bound=Base)
CreateT = TypeVar("CreateT", bound=BaseModel)
UpdateT = TypeVar("UpdateT", bound=BaseModel)


class BaseCRUD(Generic[ModelT, CreateT, UpdateT]):
    def __init__(self, model: Type[ModelT]):
        self.model = model

    def get(self, db: Session, id: int) -> ModelT | None:
        return db.get(self.model, id)

    def get_or_404(self, db: Session, id: int) -> ModelT:
        obj = self.get(db, id)
        if obj is None:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} {id} not found")
        return obj

    def list(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: list[Any] | None = None,
    ) -> list[ModelT]:
        q = db.query(self.model)
        if filters:
            q = q.filter(*filters)
        return q.offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: CreateT) -> ModelT:
        db_obj = self.model(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: ModelT, obj_in: UpdateT) -> ModelT:
        for field, value in obj_in.model_dump(exclude_unset=True).items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int) -> ModelT:
        db_obj = self.get_or_404(db, id)
        db.delete(db_obj)
        db.commit()
        return db_obj
