from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.institute_feedback import InstituteFeedbackCreate, InstituteFeedbackResponse
from app.crud import crud_institute, crud_institute_feedback
from app.services.ai_generator import generate_institute_review_draft, generate_review_draft
from app.core.constants import INSTITUTE_ROLE_QUESTIONS, INSTITUTE_SERVICES, InstituteCategory, CATEGORY_QUESTIONS, ClinicCategory
from app.core.image_resolver import resolve_image_url

router = APIRouter()

@router.get("/institute/{qr_identifier}")
def get_institute_by_qr(qr_identifier: str, db: Session = Depends(get_db)):
    if qr_identifier.startswith("demo-"):
        if qr_identifier == "demo-laboratory":
            return {
                "id": "22222222-2222-2222-2222-222222222222",
                "name": "Demo Diagnostic Laboratory",
                "logo_url": None,
                "theme_color": "#10b981",
                "category": "Laboratory",
                "questions": CATEGORY_QUESTIONS.get(ClinicCategory.LABORATORY, []),
                "services": INSTITUTE_SERVICES.get(InstituteCategory.LABORATORY, [])
            }
        return {
            "id": "22222222-2222-2222-2222-222222222222",
            "name": "Demo Junior College",
            "logo_url": None,
            "theme_color": "#10b981",
            "category": "Junior College",
            "questions": INSTITUTE_ROLE_QUESTIONS,
            "services": INSTITUTE_SERVICES.get(InstituteCategory.JUNIOR_COLLEGE, [])
        }

    institute = crud_institute.get_institute_by_qr(db, qr_identifier)
    if not institute:
        raise HTTPException(status_code=404, detail="Institute not found")
    
    questions = CATEGORY_QUESTIONS.get(ClinicCategory.LABORATORY, []) if institute.category == InstituteCategory.LABORATORY else INSTITUTE_ROLE_QUESTIONS
    return {
        "id": institute.id,
        "name": institute.name,
        "logo_url": resolve_image_url(institute.logo_url) if institute.logo_url else None,
        "theme_color": institute.theme_color,
        "category": institute.category,
        "questions": questions,
        "services": INSTITUTE_SERVICES.get(institute.category, [])
    }

@router.post("/feedback", response_model=InstituteFeedbackResponse)
def submit_institute_feedback(feedback: InstituteFeedbackCreate, db: Session = Depends(get_db)):
    is_demo = str(feedback.institute_id) == "22222222-2222-2222-2222-222222222222"
    
    institute = None
    if not is_demo:
        institute = db.query(crud_institute.Institute).filter(crud_institute.Institute.id == feedback.institute_id).first()
        if not institute:
            raise HTTPException(status_code=404, detail="Institute not found")

    is_positive = feedback.rating_score >= 4
    generated_draft = None
    action_flow = "POSITIVE" if is_positive else "PRIVATE"

    if is_positive:
        i_name = institute.name if institute else (feedback.institute_name or "Demo Institute")
        i_cat = institute.category if institute else (feedback.category or (InstituteCategory.LABORATORY if not feedback.reviewer_role else InstituteCategory.JUNIOR_COLLEGE))
        if i_cat == InstituteCategory.LABORATORY or not feedback.reviewer_role:
            generated_draft = generate_review_draft(
                clinic_name=i_name,
                category=ClinicCategory.LABORATORY,
                rating=feedback.rating_score,
                service_received=feedback.service_received
            )
        else:
            generated_draft = generate_institute_review_draft(
                institute_name=i_name, 
                role=feedback.reviewer_role, 
                rating=feedback.rating_score,
                service_received=feedback.service_received
            )
    
    if not is_demo:
        crud_institute_feedback.create_institute_feedback(
            db=db, 
            feedback=feedback, 
            generated_review=generated_draft, 
            redirected=is_positive
        )
    
    return InstituteFeedbackResponse(
        action_flow=action_flow,
        generated_review_draft=generated_draft,
        google_url="https://g.page/r/demo" if is_demo and is_positive else (institute.google_review_url if is_positive else None)
    )
