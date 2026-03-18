from pydantic import BaseModel, Field


class BuildingCreate(BaseModel):
    address: str = Field(..., min_length=1, max_length=500)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class BuildingRead(BaseModel):
    id: int
    address: str
    latitude: float
    longitude: float

    model_config = {"from_attributes": True}
