from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.repositories.base import BaseRepository
from app.models.organization import Organization, Phone
from app.models.activity import Activity


class OrganizationRepository(BaseRepository[Organization]):
    def __init__(self, db: Session) -> None:
        super().__init__(Organization, db)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _eager_query(self):
        return (
            self.db.query(Organization)
            .options(
                joinedload(Organization.building),
                joinedload(Organization.phones),
                joinedload(Organization.activities),
            )
        )

    # ------------------------------------------------------------------
    # Overrides
    # ------------------------------------------------------------------

    def get_by_id(self, entity_id: int) -> Optional[Organization]:
        return (
            self._eager_query()
            .filter(Organization.id == entity_id)
            .first()
        )

    # ------------------------------------------------------------------
    # Lookups
    # ------------------------------------------------------------------

    def get_by_building(self, building_id: int) -> List[Organization]:
        return (
            self._eager_query()
            .filter(Organization.building_id == building_id)
            .all()
        )

    def get_by_building_ids(self, building_ids: List[int]) -> List[Organization]:
        return (
            self._eager_query()
            .filter(Organization.building_id.in_(building_ids))
            .all()
        )

    def get_by_activity_ids(self, activity_ids: List[int]) -> List[Organization]:
        return (
            self._eager_query()
            .join(Organization.activities)
            .filter(Activity.id.in_(activity_ids))
            .distinct()
            .all()
        )

    def search_by_name(self, name: str) -> List[Organization]:
        return (
            self._eager_query()
            .filter(Organization.name.ilike(f"%{name}%"))
            .all()
        )

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def create(
        self,
        name: str,
        building_id: int,
        phone_numbers: List[str],
        activity_ids: List[int],
    ) -> Organization:
        org = Organization(name=name, building_id=building_id)
        self.db.add(org)
        self.db.flush()

        for number in phone_numbers:
            self.db.add(Phone(number=number, organization_id=org.id))

        if activity_ids:
            activities = (
                self.db.query(Activity)
                .filter(Activity.id.in_(activity_ids))
                .all()
            )
            org.activities = activities

        self.db.commit()
        self.db.refresh(org)
        return self.get_by_id(org.id)  # type: ignore[return-value]
