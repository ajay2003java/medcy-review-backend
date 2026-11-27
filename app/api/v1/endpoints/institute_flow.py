from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.institute_feedback import InstituteFeedbackCreate, InstituteFeedbackResponse
from app.crud import crud_institute, crud_institute_feedback, crud_clinic, crud_feedback
from app.schemas.feedback import FeedbackCreate
from app.services.ai_generator import generate_institute_review_draft, generate_review_draft
from app.core.constants import INSTITUTE_ROLE_QUESTIONS, INSTITUTE_SERVICES, InstituteCategory, CATEGORY_QUESTIONS, ClinicCategory
from app.core.image_resolver import resolve_image_url

router = APIRouter()

KISHORE_BHAVANA_CLINIC_ID = "b0101010-b010-b010-b010-b01010101010"
KISHORE_BHAVANA_GOOGLE_URL = "https://www.google.com/maps/search/?api=1&query=Kishore+Bhavana+Clinic"

@router.get("/institute/{qr_identifier}")
def get_institute_by_qr(qr_identifier: str, db: Session = Depends(get_db)):
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
            (crud_clinic.Clinic.id == KISHORE_BHAVANA_CLINIC_ID)
        ).first()
        
        clinic_id = str(clinic.id) if clinic else KISHORE_BHAVANA_CLINIC_ID
        google_url = clinic.google_review_url if clinic else KISHORE_BHAVANA_GOOGLE_URL
        
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
    is_kishore_bhavana = str(feedback.institute_id) == KISHORE_BHAVANA_CLINIC_ID or bool(feedback.doctor_name)
    
    institute = None
    clinic = None
    if is_kishore_bhavana:
        clinic = db.query(crud_clinic.Clinic).filter(
            (crud_clinic.Clinic.id == KISHORE_BHAVANA_CLINIC_ID) | 
            (crud_clinic.Clinic.qr_identifier == "kishore-bhavana")
        ).first()
    elif not is_demo:
        institute = db.query(crud_institute.Institute).filter(crud_institute.Institute.id == feedback.institute_id).first()
        if not institute:
            raise HTTPException(status_code=404, detail="Institute not found")

    is_positive = feedback.rating_score >= 4
    generated_draft = None
    action_flow = "POSITIVE" if is_positive else "PRIVATE"

    if is_positive:
        if is_kishore_bhavana:
            c_name = clinic.name if clinic else "Kishore Bhavana Clinic"
            c_cat = feedback.category or ("Orthopedics" if "kishore" in (feedback.doctor_name or "").lower() else "Pediatrics")
            generated_draft = generate_review_draft(
                clinic_name=c_name,
                category=c_cat,
                rating=feedback.rating_score,
                service_received=feedback.service_received,
                doctor_name=feedback.doctor_name
            )
        else:
            i_name = institute.name if institute else (feedback.institute_name or "Demo Institute")
            i_cat = institute.category if institute else (feedback.category or (InstituteCategory.LABORATORY if not feedback.reviewer_role else InstituteCategory.JUNIOR_COLLEGE))
            if i_cat == InstituteCategory.LABORATORY or not feedback.reviewer_role:
                generated_draft = generate_review_draft(
                    clinic_name=i_name,
                    category=ClinicCategory.LABORATORY,
                    rating=feedback.rating_score,
                    service_received=feedback.service_received,
                    doctor_name=feedback.doctor_name
                )
            else:
                generated_draft = generate_institute_review_draft(
                    institute_name=i_name, 
                    role=feedback.reviewer_role, 
                    rating=feedback.rating_score,
                    service_received=feedback.service_received
                )
    
    if is_kishore_bhavana:
        # Save to clinic feedback table
        clinic_id_to_use = clinic.id if clinic else feedback.institute_id
        fb_create = FeedbackCreate(
            clinic_id=clinic_id_to_use,
            patient_name=feedback.reviewer_name,
            patient_phone=feedback.reviewer_phone,
            rating_score=feedback.rating_score,
            private_feedback=feedback.private_feedback,
            doctor_name=feedback.doctor_name,
            service_received=feedback.service_received,
            question_ratings=feedback.question_ratings,
            selected_services=feedback.selected_services,
            language=feedback.language or "en"
        )
        crud_feedback.create_feedback(
            db=db,
            feedback=fb_create,
            generated_review=generated_draft,
            redirected=is_positive
        )
    elif not is_demo:
        crud_institute_feedback.create_institute_feedback(
            db=db, 
            feedback=feedback, 
            generated_review=generated_draft, 
            redirected=is_positive
        )
    
    # Ensure equal opportunity to post reviews on Google
    if is_kishore_bhavana:
        g_url = clinic.google_review_url if clinic else KISHORE_BHAVANA_GOOGLE_URL
    else:
        g_url = institute.google_review_url if institute else ("https://g.page/r/demo" if is_demo else None)
    
    return InstituteFeedbackResponse(
        action_flow=action_flow,
        generated_review_draft=generated_draft,
        google_url=g_url
    )
