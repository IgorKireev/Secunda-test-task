from fastapi import FastAPI

from app.core.exceptions import (
    NotFoundError,
    DataIntegrityError,
    Conflict,
    Unauthorized,
    Forbidden,
)
from app.core import exception_handlers
from app.api import (
    api_v1_router,
    auth_router,
    activity_router,
    building_router,
    organization_router,
    user_router,
)


app = FastAPI()
app.include_router(router=auth_router)
app.include_router(router=api_v1_router)
app.include_router(router=activity_router)
app.include_router(router=building_router)
app.include_router(router=organization_router)
app.include_router(router=user_router)

app.add_exception_handler(
    NotFoundError,
    exception_handlers.not_found_exception_handler,
)
app.add_exception_handler(
    DataIntegrityError,
    exception_handlers.data_integrity_exception_handler,
)
app.add_exception_handler(
    Conflict,
    exception_handlers.conflict_exception_handler,
)
app.add_exception_handler(
    Unauthorized,
    exception_handlers.unauthorized_exception_handler,
)
app.add_exception_handler(
    Forbidden,
    exception_handlers.forbidden_exception_handler,
)


@app.get("/")
async def main():
    return {"message": "Hello Secunda!"}
