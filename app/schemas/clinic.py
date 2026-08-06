from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime
from app.core.constants import ClinicCategory, ClinicStatus

class ClinicBase(BaseModel):
    name: str
    logo_url: Optional[str] = None
    theme_color: str = "#3498db"
    google_review_url: str
    category: ClinicCategory

class ClinicCreate(ClinicBase):
    pass

class Clinic(ClinicBase):
    id: UUID
    status: ClinicStatus
    qr_identifier: str
    created_at: datetime

    class Config:
        from_attributes = True
