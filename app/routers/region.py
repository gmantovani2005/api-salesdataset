from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.region import region_crud
from app.schemas.region import RegionCreate, RegionRead, RegionUpdate

router = APIRouter()


@router.get("", response_model=list[RegionRead])
def list_regions(
    name: str | None = Query(default=None, description="Partial name match (case-insensitive)"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    return region_crud.list_filtered(db, name=name, skip=skip, limit=limit)


@router.post("/", response_model=RegionRead, status_code=201)
def create_region(payload: RegionCreate, db: Session = Depends(get_db)):
    return region_crud.create(db, payload)


@router.get("/{id}", response_model=RegionRead)
def get_region(id: int, db: Session = Depends(get_db)):
    return region_crud.get_or_404(db, id)


@router.patch("/{id}", response_model=RegionRead)
def update_region(id: int, payload: RegionUpdate, db: Session = Depends(get_db)):
    obj = region_crud.get_or_404(db, id)
    return region_crud.update(db, obj, payload)


@router.delete("/{id}", response_model=RegionRead)
def delete_region(id: int, db: Session = Depends(get_db)):
    return region_crud.delete(db, id)
