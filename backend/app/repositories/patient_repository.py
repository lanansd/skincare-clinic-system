from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate


class PatientRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_user_id(
        self,
        user_id: str,
    ) -> Patient | None:
        result = await self.db.execute(
            select(Patient).where(Patient.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        user_id: str,
        data: PatientCreate,
    ) -> Patient:
        patient = Patient(
            user_id=user_id,
            **data.model_dump(),
        )

        self.db.add(patient)
        await self.db.commit()
        await self.db.refresh(patient)

        return patient

    async def update(
        self,
        patient: Patient,
        data: PatientUpdate,
    ) -> Patient:
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(patient, field, value)

        await self.db.commit()
        await self.db.refresh(patient)

        return patient