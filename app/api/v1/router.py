from fastapi import APIRouter
from app.api.v1 import organizations, buildings, activities

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(organizations.router)
api_router.include_router(buildings.router)
api_router.include_router(activities.router)
