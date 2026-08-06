from sqlalchemy.orm import Session
from app.models.clinic import Clinic
from app.schemas.clinic import ClinicCreate
import uuid

def get_clinic_by_qr(db: Session, qr_identifier: str):
    return db.query(Clinic).filter(Clinic.qr_identifier == qr_identifier).first()

def create_clinic(db: Session, clinic: ClinicCreate):
    # generate a unique qr identifier
    qr_id = str(uuid.uuid4())[:8]
    db_clinic = Clinic(
        name=clinic.name,
        logo_url=clinic.logo_url,
        theme_color=clinic.theme_color,
        google_review_url=clinic.google_review_url,
        category=clinic.category,
        qr_identifier=qr_id
    )
    db.add(db_clinic)
    db.commit()
    db.refresh(db_clinic)
    return db_clinic

def get_clinics(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Clinic).offset(skip).limit(limit).all()
