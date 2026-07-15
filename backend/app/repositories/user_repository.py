from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserRole


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(
            select(User).where(User.email == email.lower())
        )
        return result.scalar_one_or_none()

    async def create_patient(
        self,
        email: str,
        hashed_password: str,
    ) -> User:
        user = User(
            email=email.lower(),
            hashed_password=hashed_password,
            role=UserRole.PATIENT,
        )

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user