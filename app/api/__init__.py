from fastapi import APIRouter
from app.api.v1 import api_router as v1_api_router

router = APIRouter()
router.include_router(v1_api_router, prefix="/v1")
