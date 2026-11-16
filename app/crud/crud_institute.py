from sqlalchemy.orm import Session
from app.models.institute import Institute
from app.schemas.institute import InstituteCreate
from app.core.image_resolver import resolve_image_url
import uuid

def get_institute_by_qr(db: Session, qr_identifier: str):
    return db.query(Institute).filter(Institute.qr_identifier == qr_identifier).first()

def create_institute(db: Session, institute: InstituteCreate):
    qr_id = str(uuid.uuid4())[:8]
    resolved_logo = resolve_image_url(institute.logo_url) if institute.logo_url else None
    db_institute = Institute(
        name=institute.name,
        logo_url=resolved_logo,
        theme_color=institute.theme_color,
        google_review_url=institute.google_review_url,
        category=institute.category,
        qr_identifier=qr_id
    )
    db.add(db_institute)
    db.commit()
    db.refresh(db_institute)
    return db_institute

def get_institutes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Institute).offset(skip).limit(limit).all()
