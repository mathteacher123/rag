from fastapi import APIRouter

from app.api.v1.endpoints.test import router as test_router

api_router = APIRouter()
api_router.include_router(test_router)
