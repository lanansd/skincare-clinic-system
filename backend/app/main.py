from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.project_name,
    description="Backend API for the Skincare Clinic Management System",
    version="1.0.0",
)

app.include_router(
    api_router,
    prefix=settings.api_v1_prefix,
)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": f"Welcome to the {settings.project_name}"}