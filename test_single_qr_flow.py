import os, sys
from dotenv import load_dotenv

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)
load_dotenv(os.path.join(backend_dir, ".env"))

from fastapi.testclient import TestClient
from main import app
from app.db.session import SessionLocal
from app.models.feedback import Feedback
from app.models.clinic import Clinic
from sqlalchemy import text

client = TestClient(app)

def test_single_qr_flow():
    print("\n--- 1. Testing GET /api/v1/patient/clinic/kishore-bhavana (Shared QR link) ---")
    res = client.get("/api/v1/patient/clinic/kishore-bhavana")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
    data = res.json()
    print("Shared Clinic Response:", data["name"], "| Clinic ID:", data["id"])
    assert data["name"] == "Kishore Bhavana Clinic"
    assert data["id"] == "b0101010-b010-b010-b010-b01010101010"
    shared_clinic_id = data["id"]
    shared_google_url = data["google_review_url"]
    print("Shared Google Review URL:", shared_google_url)
    assert "google.com" in shared_google_url

    print("\n--- 2. Selecting Dr. Kishore and Submitting 5-Star Feedback ---")
    payload_kishore = {
        "clinic_id": shared_clinic_id,
        "clinic_name": "Kishore Bhavana Clinic",
        "doctor_name": "Dr. Kishore",
        "category": "Orthopedics",
        "rating_score": 5,
        "service_received": "Joint & Knee Pain",
        "private_feedback": None,
        "language": "en"
    }
    res_k = client.post("/api/v1/patient/feedback", json=payload_kishore)
    assert res_k.status_code == 200, f"Dr. Kishore submission failed: {res_k.text}"
    data_k = res_k.json()
    print("Dr. Kishore Review Draft:", data_k.get("generated_review_draft"))
    print("Dr. Kishore Redirect Google URL:", data_k.get("google_url"))
    assert "Dr. Kishore" in data_k.get("generated_review_draft", "")
    assert data_k.get("google_url") == shared_google_url

    print("\n--- 3. Selecting Dr. Bhavana and Submitting 5-Star Feedback ---")
    payload_bhavana = {
        "clinic_id": shared_clinic_id,
        "clinic_name": "Kishore Bhavana Clinic",
        "doctor_name": "Dr. Bhavana",
        "category": "Pediatrics",
        "rating_score": 5,
        "service_received": "Child Vaccination",
        "private_feedback": None,
        "language": "en"
    }
    res_b = client.post("/api/v1/patient/feedback", json=payload_bhavana)
    assert res_b.status_code == 200, f"Dr. Bhavana submission failed: {res_b.text}"
    data_b = res_b.json()
    print("Dr. Bhavana Review Draft:", data_b.get("generated_review_draft"))
    print("Dr. Bhavana Redirect Google URL:", data_b.get("google_url"))
    assert "Dr. Bhavana" in data_b.get("generated_review_draft", "")
    assert data_b.get("google_url") == shared_google_url

    print("\n--- 4. Verifying Database: Both records use the same clinic ID with correct doctor attribution ---")
    db = SessionLocal()
    # Check feedbacks
    feedbacks = db.query(Feedback).filter(Feedback.clinic_id == shared_clinic_id).order_by(Feedback.created_at.desc()).limit(10).all()
    print(f"Recent feedbacks found for clinic {shared_clinic_id}: {len(feedbacks)}")
    kishore_records = [f for f in feedbacks if f.doctor_name == "Dr. Kishore"]
    bhavana_records = [f for f in feedbacks if f.doctor_name == "Dr. Bhavana"]
    assert len(kishore_records) >= 1, "Expected Dr. Kishore feedback in DB"
    assert len(bhavana_records) >= 1, "Expected Dr. Bhavana feedback in DB"
    print(f"Verified: Found {len(kishore_records)} Dr. Kishore records and {len(bhavana_records)} Dr. Bhavana records under clinic ID {shared_clinic_id}")

    print("\n--- 5. Verifying Database: Kishore Bhavana Clinic is unique (no duplicate records) ---")
    kb_clinics = db.query(Clinic).filter(
        (Clinic.qr_identifier == "kishore-bhavana") | (Clinic.name.ilike("%Kishore Bhavana%"))
    ).all()
    print(f"Total Kishore Bhavana Clinic records in DB: {len(kb_clinics)}")
    assert len(kb_clinics) == 1, f"Expected exactly 1 Kishore Bhavana Clinic record, found {len(kb_clinics)}"
    assert str(kb_clinics[0].id) == shared_clinic_id

    print("\n--- 6. Verifying Other Templates & Clinics Unaffected ---")
    other_clinics = db.query(Clinic).filter(Clinic.id != shared_clinic_id).all()
    print(f"Other clinics intact in DB: {len(other_clinics)}")
    for c in other_clinics[:3]:
        print(f"  - Clinic: {c.name} | Category: {c.category} | QR: {c.qr_identifier}")
    
    db.close()
    print("\n>>> ALL VERIFICATION CHECKS PASSED SUCCESSFULLY! <<<")

if __name__ == "__main__":
    test_single_qr_flow()
