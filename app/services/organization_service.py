from typing import List
from sqlalchemy.orm import Session
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.building_repository import BuildingRepository
from app.repositories.activity_repository import ActivityRepository
from app.models.organization import Organization


class OrganizationService:
    def __init__(self, db: Session) -> None:
        self._org_repo = OrganizationRepository(db)
        self._building_repo = BuildingRepository(db)
        self._activity_repo = ActivityRepository(db)

    def get_by_id(self, org_id: int) -> Organization:
        org = self._org_repo.get_by_id(org_id)
        if org is None:
            raise ValueError(f"Organization with id={org_id} not found")
        return org

    def get_by_building(self, building_id: int) -> List[Organization]:
        return self._org_repo.get_by_building(building_id)

    def get_by_activity(self, activity_id: int) -> List[Organization]:
        """Return organizations that belong to the activity or any of its descendants."""
        all_ids = self._activity_repo.get_descendant_ids(activity_id)
        return self._org_repo.get_by_activity_ids(all_ids)

    def get_in_radius(
        self, lat: float, lon: float, radius_km: float
    ) -> List[Organization]:
        buildings = self._building_repo.get_in_radius(lat, lon, radius_km)
        if not buildings:
            return []
        return self._org_repo.get_by_building_ids([b.id for b in buildings])

    def get_in_rectangle(
        self,
        min_lat: float,
        max_lat: float,
        min_lon: float,
        max_lon: float,
    ) -> List[Organization]:
        buildings = self._building_repo.get_in_rectangle(
            min_lat, max_lat, min_lon, max_lon
        )
        if not buildings:
            return []
        return self._org_repo.get_by_building_ids([b.id for b in buildings])

    def search_by_name(self, name: str) -> List[Organization]:
        return self._org_repo.search_by_name(name)
