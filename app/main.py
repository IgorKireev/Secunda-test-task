from fastapi import FastAPI

from app.core import (
    NotFoundError,
    DataIntegrityError,
    Conflict,
    Unauthorized,
    Forbidden,
    not_found_exception_handler,
    data_integrity_exception_handler,
    conflict_exception_handler,
    unauthorized_exception_handler,
    forbidden_exception_handler,
)
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
    not_found_exception_handler,
)
app.add_exception_handler(
    DataIntegrityError,
    data_integrity_exception_handler,
)
app.add_exception_handler(
    Conflict,
    conflict_exception_handler,
)
app.add_exception_handler(
    Unauthorized,
    unauthorized_exception_handler,
)
app.add_exception_handler(
    Forbidden,
    forbidden_exception_handler,
)


@app.get("/")
async def main():
    return {"message": "Hello Secunda!"}
