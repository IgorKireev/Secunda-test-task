from app.api.v1.handlers import router as api_v1_router
from app.api.auth import router as auth_router
from app.api.activities import router as activity_router
from app.api.buildings import router as building_router
from app.api.organizations import router as organization_router
from app.api.users import router as user_router


__all__ = [
    "api_v1_router",
    "auth_router",
    "activity_router",
    "building_router",
    "organization_router",
    "user_router",
]
