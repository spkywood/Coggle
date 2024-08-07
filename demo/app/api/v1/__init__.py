from fastapi import APIRouter


from .users import router as users_router
from .llms import router as llms_router

v1_router = APIRouter()

v1_router.include_router(users_router, tags=["users"])
v1_router.include_router(llms_router, tags=["llms"])