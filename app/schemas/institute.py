from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime
from app.core.constants import InstituteCategory, InstituteStatus

class InstituteBase(BaseModel):
    name: str
    logo_url: Optional[str] = None
    theme_color: str = "#3498db"
    google_review_url: str
    category: InstituteCategory

class InstituteCreate(InstituteBase):
    pass

class Institute(InstituteBase):
    id: UUID
    status: InstituteStatus
    qr_identifier: str
    created_at: datetime

    class Config:
        from_attributes = True
