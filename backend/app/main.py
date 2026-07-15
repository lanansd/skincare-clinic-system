from fastapi import FastAPI

from app.api.v1.router import api_router

app = FastAPI(
    title="Skincare Clinic API",
    description="Backend API for the Skincare Clinic Management System",
    version="1.0.0",
)

app.include_router(api_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Welcome to the Skincare Clinic API"}