from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

class FeedbackBase(BaseModel):
    patient_name: Optional[str] = None
    patient_phone: Optional[str] = None
    rating_score: int
    private_feedback: Optional[str] = None

class FeedbackCreate(FeedbackBase):
    clinic_id: UUID
    service_received: Optional[str] = None

class Feedback(FeedbackBase):
    id: UUID
    clinic_id: UUID
    generated_review_draft: Optional[str] = None
    redirected_to_google: bool = False
    created_at: datetime

    class Config:
        from_attributes = True

class FeedbackResponse(BaseModel):
    action_flow: str # "POSITIVE" or "PRIVATE"
    generated_review_draft: Optional[str] = None
    google_url: Optional[str] = None
