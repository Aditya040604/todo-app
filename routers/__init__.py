from fastapi import APIRouter

from .admin import router as admin_router
from .auth import router as auth_router
from .todos import router as todos_router
from .users import router as users_router

api_router = APIRouter()
api_router.include_router(admin_router)
api_router.include_router(auth_router)
api_router.include_router(todos_router)
api_router.include_router(users_router)


