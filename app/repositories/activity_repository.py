from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.activity import Activity, MAX_ACTIVITY_LEVEL


class ActivityRepository(BaseRepository[Activity]):
    def __init__(self, db: Session) -> None:
        super().__init__(Activity, db)

    def get_descendant_ids(self, activity_id: int) -> List[int]:
        """Return the given activity's ID plus all its descendants' IDs (BFS)."""
        collected: List[int] = [activity_id]
        queue: List[int] = [activity_id]

        while queue:
            parent_id = queue.pop(0)
            children = (
                self.db.query(Activity)
                .filter(Activity.parent_id == parent_id)
                .all()
            )
            for child in children:
                collected.append(child.id)
                queue.append(child.id)

        return collected

    def create(self, name: str, parent_id: Optional[int] = None) -> Activity:
        level = 1
        if parent_id is not None:
            parent = self.get_by_id(parent_id)
            if parent is None:
                raise ValueError(f"Parent activity with id={parent_id} not found")
            if parent.level >= MAX_ACTIVITY_LEVEL:
                raise ValueError(
                    f"Cannot nest activity deeper than level {MAX_ACTIVITY_LEVEL}"
                )
            level = parent.level + 1

        activity = Activity(name=name, parent_id=parent_id, level=level)
        self.db.add(activity)
        self.db.commit()
        self.db.refresh(activity)
        return activity
