from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    NotFoundError,
    DataIntegrityError,
    Conflict,
    Unauthorized,
    Forbidden,
)


async def not_found_exception_handler(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"message": exc.detail})


async def data_integrity_exception_handler(request: Request, exc: DataIntegrityError):
    return JSONResponse(status_code=400, content={"message": str(exc)})


async def conflict_exception_handler(request: Request, exc: Conflict):
    return JSONResponse(status_code=409, content={"message": str(exc)})


async def unauthorized_exception_handler(request: Request, exc: Unauthorized):
    return JSONResponse(status_code=401, content={"message": str(exc)})


async def forbidden_exception_handler(request: Request, exc: Forbidden):
    return JSONResponse(status_code=403, content={"message": str(exc)})
