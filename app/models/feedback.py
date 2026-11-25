import uuid
from sqlalchemy import Column, String, Integer, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Feedback(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinic.id"), nullable=False)
    patient_name = Column(String, nullable=True)
    patient_phone = Column(String, nullable=True)
    rating_score = Column(Integer, nullable=False)
    private_feedback = Column(Text, nullable=True)
    generated_review_draft = Column(Text, nullable=True)
    redirected_to_google = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    question_ratings = Column(JSON, nullable=True)
    selected_services = Column(JSON, nullable=True)
    language = Column(String, nullable=True, default="en")
    service_received = Column(String, nullable=True)
    doctor_name = Column(String, nullable=True)

    clinic = relationship("Clinic", back_populates="feedbacks")
