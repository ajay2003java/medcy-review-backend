import uuid
from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.core.constants import ClinicCategory, ClinicStatus

class Clinic(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    logo_url = Column(String, nullable=True)
    theme_color = Column(String, nullable=False, default="#3498db")
    google_review_url = Column(String, nullable=False)
    category = Column(Enum(ClinicCategory), nullable=False)
    status = Column(Enum(ClinicStatus), nullable=False, default=ClinicStatus.ACTIVE)
    qr_identifier = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    feedbacks = relationship("Feedback", back_populates="clinic")
