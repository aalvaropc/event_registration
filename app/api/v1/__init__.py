from fastapi import APIRouter
from app.api.v1.endpoints import registration

api_router = APIRouter()
api_router.include_router(registration.router, prefix="/registration", tags=["registration"])
