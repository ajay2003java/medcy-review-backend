from sqlalchemy.orm import Session
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate

def create_feedback(db: Session, feedback: FeedbackCreate, generated_review: str = None, redirected: bool = False):
    services_str = feedback.service_received
    if not services_str and feedback.selected_services:
        services_str = ", ".join(feedback.selected_services)

    db_feedback = Feedback(
        clinic_id=feedback.clinic_id,
        patient_name=feedback.patient_name,
        patient_phone=feedback.patient_phone,
        rating_score=feedback.rating_score,
        private_feedback=feedback.private_feedback,
        generated_review_draft=generated_review,
        redirected_to_google=redirected,
        question_ratings=feedback.question_ratings,
        selected_services=feedback.selected_services,
        language=feedback.language or "en",
        service_received=services_str,
        doctor_name=feedback.doctor_name
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback
