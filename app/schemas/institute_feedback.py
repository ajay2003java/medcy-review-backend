from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime
from app.core.constants import ReviewerRole

class InstituteFeedbackBase(BaseModel):
    reviewer_role: ReviewerRole
    reviewer_name: Optional[str] = None
    reviewer_phone: Optional[str] = None
    rating_score: int
    service_received: Optional[str] = None
    private_feedback: Optional[str] = None

class InstituteFeedbackCreate(InstituteFeedbackBase):
    institute_id: UUID

class InstituteFeedback(InstituteFeedbackBase):
    id: UUID
    institute_id: UUID
    generated_review_draft: Optional[str] = None
    redirected_to_google: bool = False
    created_at: datetime

    class Config:
        from_attributes = True

class InstituteFeedbackResponse(BaseModel):
    action_flow: str # "POSITIVE" or "PRIVATE"
    generated_review_draft: Optional[str] = None
    google_url: Optional[str] = None
