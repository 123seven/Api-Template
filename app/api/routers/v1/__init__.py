from fastapi import APIRouter

from .example import router as example_router

v1_router = APIRouter()

v1_router.include_router(
    example_router,
    prefix="/example",
    tags=["example"],
)
