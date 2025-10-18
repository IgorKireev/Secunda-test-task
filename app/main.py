from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions.exceptions import NotFoundError, DataIntegrityError
from app.api import (
    api_v1_router,
    activity_router,
    building_router,
    organization_router,
    user_router,
)


app = FastAPI()
app.include_router(router=api_v1_router)
app.include_router(router=activity_router)
app.include_router(router=building_router)
app.include_router(router=organization_router)
app.include_router(router=user_router)


@app.exception_handler(NotFoundError)
async def not_found_exception_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={"message": exc.detail}
    )


@app.exception_handler(DataIntegrityError)
async def data_integrity_exception_handler(request: Request, exc: DataIntegrityError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)}
    )

@app.get("/")
async def main():
    return {
        "message": "Hello Secunda!"
    }