from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.api.deps import require_api_key
from app.repositories.building_repository import BuildingRepository
from app.schemas.building import BuildingRead

router = APIRouter(prefix="/buildings", tags=["Buildings"])

_auth = Depends(require_api_key)
_db = Depends(get_db)


def _repo(db: Session = _db) -> BuildingRepository:
    return BuildingRepository(db)


@router.get(
    "/",
    response_model=List[BuildingRead],
    summary="Список всех зданий",
)
def get_all(
    repo: BuildingRepository = Depends(_repo),
    _: str = _auth,
):
    return repo.get_all()


@router.get(
    "/{building_id}",
    response_model=BuildingRead,
    summary="Здание по ID",
)
def get_by_id(
    building_id: int,
    repo: BuildingRepository = Depends(_repo),
    _: str = _auth,
):
    building = repo.get_by_id(building_id)
    if building is None:
        raise HTTPException(status_code=404, detail=f"Building id={building_id} not found")
    return building
