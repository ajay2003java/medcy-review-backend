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

def test_kishore_bhavana_flow():
    print("\n--- 1. Testing GET /api/v1/institute-flow/institute/kishore ---")
    res_k = client.get("/api/v1/institute-flow/institute/kishore")
    assert res_k.status_code == 200, f"Expected 200, got {res_k.status_code}: {res_k.text}"
    data_k = res_k.json()
    print("Dr. Kishore Response:", data_k["name"], "|", data_k["doctor_name"], "|", data_k["specialty"])
    assert data_k["name"] == "Kishore Bhavana Clinic"
    assert data_k["doctor_name"] == "Dr. Kishore"
    assert data_k["specialty"] == "Orthopedician"
    assert len(data_k["questions"]) > 0
    assert len(data_k["services"]) > 0
    clinic_id = data_k["clinic_id"]

    print("\n--- 2. Testing GET /api/v1/institute-flow/institute/bhavana ---")
    res_b = client.get("/api/v1/institute-flow/institute/bhavana")
    assert res_b.status_code == 200, f"Expected 200, got {res_b.status_code}: {res_b.text}"
    data_b = res_b.json()
    print("Dr. Bhavana Response:", data_b["name"], "|", data_b["doctor_name"], "|", data_b["specialty"])
    assert data_b["name"] == "Kishore Bhavana Clinic"
    assert data_b["doctor_name"] == "Dr. Bhavana"
    assert data_b["specialty"] == "Pediatrician"
    assert data_b["clinic_id"] == clinic_id, "Both doctors must share the exact same clinic ID!"
    assert data_b["google_review_url"] == data_k["google_review_url"], "Both forms must use the exact same Google review URL!"

    print("\n--- 3. Testing Feedback Submission for Dr. Kishore (5 Stars) ---")
    payload_k = {
        "clinic_id": clinic_id,
        "clinic_name": "Kishore Bhavana Clinic",
        "doctor_name": "Dr. Kishore",
        "category": "Orthopedics",
        "rating_score": 5,
        "service_received": "Joint & Knee Pain",
        "private_feedback": None,
        "language": "en"
    }
    fb_res_k = client.post("/api/v1/patient/feedback", json=payload_k)
    assert fb_res_k.status_code == 200, f"Expected 200, got {fb_res_k.status_code}: {fb_res_k.text}"
    fb_data_k = fb_res_k.json()
    print("Dr. Kishore Draft Review:", fb_data_k["generated_review_draft"])
    print("Google URL:", fb_data_k["google_url"])
    assert "Kishore Bhavana Clinic" in fb_data_k["generated_review_draft"]
    assert fb_data_k["google_url"] == data_k["google_review_url"]

    print("\n--- 4. Testing Feedback Submission for Dr. Bhavana (5 Stars) ---")
    payload_b = {
        "clinic_id": clinic_id,
        "clinic_name": "Kishore Bhavana Clinic",
        "doctor_name": "Dr. Bhavana",
        "category": "Pediatrics",
        "rating_score": 5,
        "service_received": "Child Vaccination",
        "private_feedback": None,
        "language": "en"
    }
    fb_res_b = client.post("/api/v1/patient/feedback", json=payload_b)
    assert fb_res_b.status_code == 200, f"Expected 200, got {fb_res_b.status_code}: {fb_res_b.text}"
    fb_data_b = fb_res_b.json()
    print("Dr. Bhavana Draft Review:", fb_data_b["generated_review_draft"])
    print("Google URL:", fb_data_b["google_url"])
    assert "Kishore Bhavana Clinic" in fb_data_b["generated_review_draft"]
    assert fb_data_b["google_url"] == data_b["google_review_url"]

    print("\n--- 5. Testing Equal Opportunity (Rating <= 3 Stars) ---")
    payload_constructive = {
        "clinic_id": clinic_id,
        "clinic_name": "Kishore Bhavana Clinic",
        "doctor_name": "Dr. Kishore",
        "category": "Orthopedics",
        "rating_score": 2,
        "service_received": "Spine & Back Care",
        "private_feedback": "Wait time was a bit longer than expected.",
        "language": "en"
    }
    fb_res_priv = client.post("/api/v1/patient/feedback", json=payload_constructive)
    assert fb_res_priv.status_code == 200
    fb_data_priv = fb_res_priv.json()
    print("Private feedback action_flow:", fb_data_priv["action_flow"])
    print("Equal opportunity Google URL:", fb_data_priv["google_url"])
    assert fb_data_priv["action_flow"] == "PRIVATE"
    assert fb_data_priv["google_url"] == data_k["google_review_url"], "Google URL must be provided even for private feedback for equal opportunity!"

    print("\n--- 6. Verifying Database Records in 'feedback' table ---")
    db = SessionLocal()
    records = db.query(Feedback).filter(Feedback.clinic_id == clinic_id).all()
    print(f"Total feedback records stored for Kishore Bhavana Clinic ({clinic_id}): {len(records)}")
    for r in records:
        print(f"Record ID: {r.id} | Doctor: {r.doctor_name} | Score: {r.rating_score} | Service: {r.service_received}")
    
    kishore_records = [r for r in records if r.doctor_name == "Dr. Kishore"]
    bhavana_records = [r for r in records if r.doctor_name == "Dr. Bhavana"]
    assert len(kishore_records) >= 1, "Expected Dr. Kishore feedback in DB"
    assert len(bhavana_records) >= 1, "Expected Dr. Bhavana feedback in DB"
    db.close()

    print("\n>>> ALL TESTS PASSED SUCCESSFULLY! <<<")

if __name__ == "__main__":
    test_kishore_bhavana_flow()
