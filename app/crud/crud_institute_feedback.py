from sqlalchemy.orm import Session
from app.models.institute_feedback import InstituteFeedback
from app.schemas.institute_feedback import InstituteFeedbackCreate

def create_institute_feedback(db: Session, feedback: InstituteFeedbackCreate, generated_review: str = None, redirected: bool = False):
    services_str = feedback.service_received
    if not services_str and feedback.selected_services:
        services_str = ", ".join(feedback.selected_services)

    db_feedback = InstituteFeedback(
        institute_id=feedback.institute_id,
        reviewer_role=feedback.reviewer_role,
        reviewer_name=feedback.reviewer_name,
        reviewer_phone=feedback.reviewer_phone,
        rating_score=feedback.rating_score,
        service_received=services_str,
        private_feedback=feedback.private_feedback,
        generated_review_draft=generated_review,
        redirected_to_google=redirected,
        question_ratings=feedback.question_ratings,
        selected_services=feedback.selected_services,
        language=feedback.language or "en",
        doctor_name=feedback.doctor_name
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def get_institute_feedbacks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(InstituteFeedback).order_by(InstituteFeedback.created_at.desc()).offset(skip).limit(limit).all()
