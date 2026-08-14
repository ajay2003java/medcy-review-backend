import uuid
from sqlalchemy import Column, String, Integer, Text, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.core.constants import ReviewerRole

class InstituteFeedback(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    institute_id = Column(UUID(as_uuid=True), ForeignKey("institute.id", ondelete="CASCADE"), nullable=False)
    
    reviewer_role = Column(Enum(ReviewerRole, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    reviewer_name = Column(String, nullable=True)
    reviewer_phone = Column(String, nullable=True)
    
    rating_score = Column(Integer, nullable=False)
    service_received = Column(String, nullable=True)
    private_feedback = Column(Text, nullable=True)
    generated_review_draft = Column(Text, nullable=True)
    redirected_to_google = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    institute = relationship("Institute", back_populates="feedbacks")
