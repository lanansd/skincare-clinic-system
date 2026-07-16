from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class PatientCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    phone: str | None = Field(default=None, max_length=30)
    date_of_birth: date | None = None
    gender: str | None = Field(default=None, max_length=30)
    skin_type: str | None = Field(default=None, max_length=50)
    allergies: str | None = None
    medical_notes: str | None = None


class PatientUpdate(BaseModel):
    first_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    last_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    phone: str | None = Field(default=None, max_length=30)
    date_of_birth: date | None = None
    gender: str | None = Field(default=None, max_length=30)
    skin_type: str | None = Field(default=None, max_length=50)
    allergies: str | None = None
    medical_notes: str | None = None


class PatientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    first_name: str | None
    last_name: str | None
    phone: str | None
    date_of_birth: date | None
    gender: str | None
    skin_type: str | None
    allergies: str | None
    medical_notes: str | None
    created_at: datetime
    updated_at: datetime