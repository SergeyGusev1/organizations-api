from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, List


class ActivityCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    parent_id: Optional[int] = None


class ActivityRead(BaseModel):
    id: int
    name: str
    level: int
    parent_id: Optional[int] = None
    children: List[ActivityRead] = []

    model_config = {"from_attributes": True}


ActivityRead.model_rebuild()


class ActivitySimple(BaseModel):
    """Flat activity representation used inside OrganizationRead."""

    id: int
    name: str
    level: int

    model_config = {"from_attributes": True}
