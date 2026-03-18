from pydantic import BaseModel, Field
from typing import List
from app.schemas.building import BuildingRead
from app.schemas.activity import ActivitySimple


class PhoneRead(BaseModel):
    id: int
    number: str

    model_config = {"from_attributes": True}


class OrganizationCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=500)
    building_id: int
    phone_numbers: List[str] = Field(default_factory=list)
    activity_ids: List[int] = Field(default_factory=list)


class OrganizationRead(BaseModel):
    id: int
    name: str
    building: BuildingRead
    phones: List[PhoneRead]
    activities: List[ActivitySimple]

    model_config = {"from_attributes": True}
