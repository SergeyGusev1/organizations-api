from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.api.deps import require_api_key
from app.services.organization_service import OrganizationService
from app.schemas.organization import OrganizationRead

router = APIRouter(prefix="/organizations", tags=["Organizations"])

_auth = Depends(require_api_key)
_db = Depends(get_db)


def _service(db: Session = _db) -> OrganizationService:
    return OrganizationService(db)


@router.get(
    "/search",
    response_model=List[OrganizationRead],
    summary="Поиск организаций по названию",
)
def search_by_name(
    name: str = Query(..., min_length=1, description="Подстрока названия"),
    service: OrganizationService = Depends(_service),
    _: str = _auth,
):
    return service.search_by_name(name)


@router.get(
    "/geo/radius",
    response_model=List[OrganizationRead],
    summary="Организации в радиусе от точки",
)
def get_in_radius(
    lat: float = Query(..., ge=-90, le=90, description="Широта центра"),
    lon: float = Query(..., ge=-180, le=180, description="Долгота центра"),
    radius_km: float = Query(..., gt=0, description="Радиус в километрах"),
    service: OrganizationService = Depends(_service),
    _: str = _auth,
):
    return service.get_in_radius(lat, lon, radius_km)


@router.get(
    "/geo/rectangle",
    response_model=List[OrganizationRead],
    summary="Организации в прямоугольной области",
)
def get_in_rectangle(
    min_lat: float = Query(..., ge=-90, le=90),
    max_lat: float = Query(..., ge=-90, le=90),
    min_lon: float = Query(..., ge=-180, le=180),
    max_lon: float = Query(..., ge=-180, le=180),
    service: OrganizationService = Depends(_service),
    _: str = _auth,
):
    return service.get_in_rectangle(min_lat, max_lat, min_lon, max_lon)


@router.get(
    "/by-building/{building_id}",
    response_model=List[OrganizationRead],
    summary="Организации в конкретном здании",
)
def get_by_building(
    building_id: int,
    service: OrganizationService = Depends(_service),
    _: str = _auth,
):
    return service.get_by_building(building_id)


@router.get(
    "/by-activity/{activity_id}",
    response_model=List[OrganizationRead],
    summary="Организации по виду деятельности (включая дочерние)",
)
def get_by_activity(
    activity_id: int,
    service: OrganizationService = Depends(_service),
    _: str = _auth,
):
    return service.get_by_activity(activity_id)


@router.get(
    "/{org_id}",
    response_model=OrganizationRead,
    summary="Информация об организации по ID",
)
def get_by_id(
    org_id: int,
    service: OrganizationService = Depends(_service),
    _: str = _auth,
):
    try:
        return service.get_by_id(org_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
