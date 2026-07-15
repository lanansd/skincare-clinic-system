from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserRegister


class AuthService:
    def __init__(self, db: AsyncSession) -> None:
        self.repository = UserRepository(db)

    async def register_patient(self, data: UserRegister) -> User:
        normalized_email = data.email.lower()

        existing_user = await self.repository.get_by_email(normalized_email)

        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists.",
            )

        hashed_password = hash_password(data.password)

        try:
            return await self.repository.create_patient(
                email=normalized_email,
                hashed_password=hashed_password,
            )
        except IntegrityError as exc:
            await self.repository.db.rollback()

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists.",
            ) from exc