from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import UserRegister, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_patient(
    data: UserRegister,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    user = await AuthService(db).register_patient(data)
    return UserResponse.model_validate(user)