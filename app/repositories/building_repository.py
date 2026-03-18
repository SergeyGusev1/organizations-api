from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.repositories.base import BaseRepository
from app.models.building import Building


class BuildingRepository(BaseRepository[Building]):
    def __init__(self, db: Session) -> None:
        super().__init__(Building, db)

    def get_in_radius(self, lat: float, lon: float, radius_km: float) -> List[Building]:
        """Return buildings within `radius_km` kilometres of (lat, lon).

        Uses the Haversine formula expressed in SQL so the filtering happens
        in the database without loading all rows into Python.
        """
        stmt = text(
            """
            SELECT id
            FROM buildings
            WHERE (
                6371 * acos(
                    LEAST(1.0,
                        cos(radians(:lat)) * cos(radians(latitude))
                        * cos(radians(longitude) - radians(:lon))
                        + sin(radians(:lat)) * sin(radians(latitude))
                    )
                )
            ) <= :radius
            """
        )
        rows = self.db.execute(stmt, {"lat": lat, "lon": lon, "radius": radius_km})
        ids = [row[0] for row in rows]
        if not ids:
            return []
        return self.db.query(Building).filter(Building.id.in_(ids)).all()

    def get_in_rectangle(
        self,
        min_lat: float,
        max_lat: float,
        min_lon: float,
        max_lon: float,
    ) -> List[Building]:
        """Return buildings inside the given bounding box."""
        return (
            self.db.query(Building)
            .filter(
                Building.latitude >= min_lat,
                Building.latitude <= max_lat,
                Building.longitude >= min_lon,
                Building.longitude <= max_lon,
            )
            .all()
        )
