from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.patient import (
    PatientCreate,
    PatientResponse,
    PatientUpdate,
)
from app.services.patient_service import PatientService


router = APIRouter(
    prefix="/patients",
    tags=["Patients"],
)


@router.post(
    "/me",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_my_patient_profile(
    data: PatientCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PatientResponse:
    patient = await PatientService(db).create_my_profile(
        current_user=current_user,
        data=data,
    )

    return PatientResponse.model_validate(patient)


@router.get(
    "/me",
    response_model=PatientResponse,
)
async def get_my_patient_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PatientResponse:
    patient = await PatientService(db).get_my_profile(current_user)

    return PatientResponse.model_validate(patient)


@router.patch(
    "/me",
    response_model=PatientResponse,
)
async def update_my_patient_profile(
    data: PatientUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PatientResponse:
    patient = await PatientService(db).update_my_profile(
        current_user=current_user,
        data=data,
    )

    return PatientResponse.model_validate(patient)