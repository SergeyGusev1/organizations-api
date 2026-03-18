from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.api.deps import require_api_key
from app.services.activity_service import ActivityService
from app.schemas.activity import ActivityRead

router = APIRouter(prefix="/activities", tags=["Activities"])

_auth = Depends(require_api_key)
_db = Depends(get_db)


def _service(db: Session = _db) -> ActivityService:
    return ActivityService(db)


def _build_tree(activities) -> List[ActivityRead]:
    """Convert a flat list of Activity ORM objects into a nested tree."""
    by_id = {a.id: ActivityRead.model_validate(a) for a in activities}
    roots: List[ActivityRead] = []

    for activity in activities:
        node = by_id[activity.id]
        if activity.parent_id is None:
            roots.append(node)
        else:
            parent = by_id.get(activity.parent_id)
            if parent is not None:
                parent.children.append(node)

    return roots


@router.get(
    "/",
    response_model=List[ActivityRead],
    summary="Дерево видов деятельности",
)
def get_tree(
    service: ActivityService = Depends(_service),
    _: str = _auth,
):
    return _build_tree(service.get_all())


@router.get(
    "/{activity_id}",
    response_model=ActivityRead,
    summary="Вид деятельности по ID",
)
def get_by_id(
    activity_id: int,
    service: ActivityService = Depends(_service),
    _: str = _auth,
):
    try:
        activity = service.get_by_id(activity_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    # Include immediate children for the single-item view
    return ActivityRead.model_validate(activity)
