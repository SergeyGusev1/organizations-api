from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.activity_repository import ActivityRepository
from app.models.activity import Activity


class ActivityService:
    def __init__(self, db: Session) -> None:
        self._repo = ActivityRepository(db)

    def get_all(self) -> List[Activity]:
        return self._repo.get_all()

    def get_by_id(self, activity_id: int) -> Activity:
        activity = self._repo.get_by_id(activity_id)
        if activity is None:
            raise ValueError(f"Activity with id={activity_id} not found")
        return activity

    def get_descendant_ids(self, activity_id: int) -> List[int]:
        self.get_by_id(activity_id)  # raises 404 if not found
        return self._repo.get_descendant_ids(activity_id)

    def create(self, name: str, parent_id: Optional[int] = None) -> Activity:
        return self._repo.create(name=name, parent_id=parent_id)
