from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.patient import Patient
from app.models.user import User, UserRole
from app.repositories.patient_repository import PatientRepository
from app.schemas.patient import PatientCreate, PatientUpdate


class PatientService:
    def __init__(self, db: AsyncSession) -> None:
        self.repository = PatientRepository(db)

    @staticmethod
    def ensure_patient_role(user: User) -> None:
        if user.role != UserRole.PATIENT:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only patients can access patient profiles.",
            )

    async def create_my_profile(
        self,
        current_user: User,
        data: PatientCreate,
    ) -> Patient:
        self.ensure_patient_role(current_user)

        existing_profile = await self.repository.get_by_user_id(
            current_user.id
        )

        if existing_profile is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A patient profile already exists.",
            )

        return await self.repository.create(
            user_id=current_user.id,
            data=data,
        )

    async def get_my_profile(self, current_user: User) -> Patient:
        self.ensure_patient_role(current_user)

        patient = await self.repository.get_by_user_id(current_user.id)

        if patient is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient profile not found.",
            )

        return patient

    async def update_my_profile(
        self,
        current_user: User,
        data: PatientUpdate,
    ) -> Patient:
        patient = await self.get_my_profile(current_user)

        return await self.repository.update(
            patient=patient,
            data=data,
        )