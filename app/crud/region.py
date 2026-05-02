from sqlalchemy.orm import Session

from app.crud.base import BaseCRUD
from app.models.region import Region
from app.schemas.region import RegionCreate, RegionUpdate


class RegionCRUD(BaseCRUD[Region, RegionCreate, RegionUpdate]):
    def list_filtered(
        self,
        db: Session,
        *,
        name: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Region]:
        filters = []
        if name:
            filters.append(Region.name.ilike(f"%{name}%"))
        return self.list(db, skip=skip, limit=limit, filters=filters or None)


region_crud = RegionCRUD(Region)
