from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.feedback import FeedbackCreate, FeedbackResponse
from app.crud import crud_clinic, crud_feedback
from app.services.ai_generator import generate_review_draft
from app.core.constants import CATEGORY_QUESTIONS, CATEGORY_SERVICES

router = APIRouter()

@router.get("/clinic/{qr_identifier}")
def get_clinic_by_qr(qr_identifier: str, db: Session = Depends(get_db)):
    if qr_identifier.startswith("demo-"):
        category_str = qr_identifier.replace("demo-", "")
        # Map string back to Enum
        category_map = {
            "ivf": "IVF",
            "dermatology": "Dermatology",
            "gynecology": "Gynecology",
            "dentist": "Dentist",
            "general-hospital": "General Hospital"
        }
        category_enum = category_map.get(category_str, "General Hospital")
        
        return {
            "id": "11111111-1111-1111-1111-111111111111",
            "name": f"Demo {category_enum} Clinic",
            "logo_url": None,
            "theme_color": "#ec4899" if category_str == "ivf" else "#8b5cf6" if category_str == "dermatology" else "#f43f5e" if category_str == "gynecology" else "#0ea5e9" if category_str == "dentist" else "#10b981",
            "category": category_enum,
            "questions": CATEGORY_QUESTIONS.get(category_enum, []),
            "services": CATEGORY_SERVICES.get(category_enum, [])
        }

    clinic = crud_clinic.get_clinic_by_qr(db, qr_identifier)
    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")
    
    questions = CATEGORY_QUESTIONS.get(clinic.category, [])
    
    return {
        "id": clinic.id,
        "name": clinic.name,
        "logo_url": clinic.logo_url,
        "theme_color": clinic.theme_color,
        "category": clinic.category,
        "questions": questions,
        "services": CATEGORY_SERVICES.get(clinic.category, [])
    }

@router.post("/feedback", response_model=FeedbackResponse)
def submit_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    is_demo = str(feedback.clinic_id) == "11111111-1111-1111-1111-111111111111"
    
    clinic = None
    if not is_demo:
        clinic = db.query(crud_clinic.Clinic).filter(crud_clinic.Clinic.id == feedback.clinic_id).first()
        if not clinic:
            raise HTTPException(status_code=404, detail="Clinic not found")

    is_positive = feedback.rating_score >= 4
    generated_draft = None
    action_flow = "POSITIVE" if is_positive else "PRIVATE"

    if is_positive:
        c_name = "Demo Clinic" if is_demo else clinic.name
        # Fallback to general hospital enum if we don't know the demo category here
        # For full demo logic we could pass category, but this works for demo draft
        c_category = list(CATEGORY_QUESTIONS.keys())[0] if is_demo else clinic.category 
        generated_draft = generate_review_draft(c_name, c_category, feedback.rating_score, feedback.service_received)
    
    if not is_demo:
        crud_feedback.create_feedback(
            db=db, 
            feedback=feedback, 
            generated_review=generated_draft, 
            redirected=is_positive
        )
    
    return FeedbackResponse(
        action_flow=action_flow,
        generated_review_draft=generated_draft,
        google_url="https://g.page/r/demo" if is_demo and is_positive else (clinic.google_review_url if is_positive else None)
    )
