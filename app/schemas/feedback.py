from pydantic import BaseModel
from uuid import UUID
from typing import Optional, Any
from datetime import datetime

class FeedbackBase(BaseModel):
    patient_name: Optional[str] = None
    patient_phone: Optional[str] = None
    rating_score: int
    private_feedback: Optional[str] = None

class FeedbackCreate(FeedbackBase):
    clinic_id: UUID
    service_received: Optional[str] = None
    question_ratings: Optional[Any] = None
    selected_services: Optional[list[str]] = None
    language: Optional[str] = "en"
    clinic_name: Optional[str] = None
    category: Optional[str] = None

class Feedback(FeedbackBase):
    id: UUID
    clinic_id: UUID
    generated_review_draft: Optional[str] = None
    redirected_to_google: bool = False
    created_at: datetime
    question_ratings: Optional[Any] = None
    selected_services: Optional[list[str]] = None
    language: Optional[str] = "en"
    service_received: Optional[str] = None

    class Config:
        from_attributes = True

class FeedbackResponse(BaseModel):
    action_flow: str # "POSITIVE" or "PRIVATE"
    generated_review_draft: Optional[str] = None
    google_url: Optional[str] = None
