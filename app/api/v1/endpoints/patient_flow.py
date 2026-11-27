from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.feedback import FeedbackCreate, FeedbackResponse
from app.crud import crud_clinic, crud_feedback
from app.services.ai_generator import generate_review_draft
from app.core.constants import CATEGORY_QUESTIONS, CATEGORY_SERVICES
from app.core.image_resolver import resolve_image_url

router = APIRouter()

@router.get("/clinic/{qr_identifier}")
def get_clinic_by_qr(qr_identifier: str, db: Session = Depends(get_db)):
    if qr_identifier in ["kishore", "bhavana", "kishore-bhavana"]:
        is_kishore = qr_identifier == "kishore"
        is_bhavana = qr_identifier == "bhavana"
        doctor_name = "Dr. Kishore" if is_kishore else ("Dr. Bhavana" if is_bhavana else None)
        specialty = "Orthopedician" if is_kishore else ("Pediatrician" if is_bhavana else "Multi-Specialty")
        category_name = "Orthopedics" if is_kishore else ("Pediatrics" if is_bhavana else "General Hospital")
        
        ortho_questions = [
            "Were you satisfied with Dr. Kishore's orthopedic consultation and treatment plan?",
            "Did the doctor explain your diagnosis and recovery clearly?",
            "Was the clinic environment clean, hygienic and well-maintained?",
            "Did the doctor listen attentively to your pain concerns and perform a thorough examination?"
        ]
        pedia_questions = [
            "Did Dr. Bhavana make your child feel comfortable and well-cared for during the visit?",
            "Did the doctor explain your child's diagnosis and treatment clearly?",
            "Was the clinic environment child-friendly, clean and hygienic?",
            "Were the reception and nursing staff gentle, polite and helpful?"
        ]
        ortho_services = [
            "Joint & Knee Pain", "Fracture Care", "Spine & Back Care",
            "Arthritis Treatment", "Sports Injury", "Bone Density Check",
            "General Orthopedic Consultation"
        ]
        pedia_services = [
            "Child Vaccination", "Newborn & Infant Care", "Growth & Nutrition",
            "Fever & Infection Care", "Asthma & Allergy Care", "Child Health Checkup",
            "General Pediatric Consultation"
        ]
        
        clinic = db.query(crud_clinic.Clinic).filter(
            (crud_clinic.Clinic.qr_identifier == "kishore-bhavana") | 
            (crud_clinic.Clinic.id == "b0101010-b010-b010-b010-b01010101010")
        ).first()
        
        clinic_id = str(clinic.id) if clinic else "b0101010-b010-b010-b010-b01010101010"
        google_url = clinic.google_review_url if (clinic and clinic.google_review_url) else "https://www.google.com/maps/search/?api=1&query=Kishore+Bhavana+Clinic"
        
        return {
            "id": clinic_id,
            "clinic_id": clinic_id,
            "name": "Kishore Bhavana Clinic",
            "doctor_name": doctor_name,
            "specialty": specialty,
            "logo_url": clinic.logo_url if clinic else None,
            "theme_color": "#0284c7",
            "category": category_name,
            "google_review_url": google_url,
            "isDoctorClinic": True,
            "questions": ortho_questions if is_kishore else (pedia_questions if is_bhavana else ortho_questions),
            "services": ortho_services if is_kishore else (pedia_services if is_bhavana else ortho_services)
        }

    if qr_identifier.startswith("demo-"):
        category_str = qr_identifier.replace("demo-", "")
        # Map string back to Enum
        category_map = {
            "ivf": "IVF",
            "dermatology": "Dermatology",
            "gynecology": "Gynecology",
            "dentist": "Dentist",
            "general-hospital": "General Hospital",
            "laboratory": "Laboratory"
        }
        category_enum = category_map.get(category_str, "General Hospital")
        
        return {
            "id": "11111111-1111-1111-1111-111111111111",
            "name": f"Demo {category_enum} Center" if category_enum == "Laboratory" else f"Demo {category_enum} Clinic",
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
        "logo_url": resolve_image_url(clinic.logo_url) if clinic.logo_url else None,
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
        c_name = clinic.name if clinic else (feedback.clinic_name or "Demo Clinic")
        c_category = clinic.category if clinic else (feedback.category or list(CATEGORY_QUESTIONS.keys())[0])
        generated_draft = generate_review_draft(
            clinic_name=c_name, 
            category=c_category, 
            rating=feedback.rating_score, 
            service_received=feedback.service_received,
            doctor_name=feedback.doctor_name
        )
    
    if not is_demo:
        crud_feedback.create_feedback(
            db=db, 
            feedback=feedback, 
            generated_review=generated_draft, 
            redirected=is_positive
        )
    
    # Ensure patients have equal opportunity to post reviews on Google regardless of score
    g_url = clinic.google_review_url if clinic else ("https://g.page/r/demo" if is_demo else None)
    
    return FeedbackResponse(
        action_flow=action_flow,
        generated_review_draft=generated_draft,
        google_url=g_url
    )
