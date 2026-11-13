import os, sys
from dotenv import load_dotenv

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)
load_dotenv(os.path.join(backend_dir, ".env"))

from fastapi.testclient import TestClient
from main import app
from app.db.session import engine
from sqlalchemy import text

client = TestClient(app)

def test_api():
    print("Testing GET /api/v1/patient/clinic/demo-laboratory...")
    res = client.get("/api/v1/patient/clinic/demo-laboratory")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
    data = res.json()
    assert data["category"] == "Laboratory"
    assert len(data["questions"]) == 4, f"Expected 4 questions, got {len(data['questions'])}"
    assert len(data["services"]) == 18, f"Expected 18 services, got {len(data['services'])}"
    print("✓ GET clinic demo-laboratory passed. Questions:", len(data["questions"]), "Services:", len(data["services"]))

    print("\nTesting GET /api/v1/institute-flow/institute/demo-laboratory...")
    res = client.get("/api/v1/institute-flow/institute/demo-laboratory")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
    data = res.json()
    assert data["category"] == "Laboratory"
    assert len(data["questions"]) == 4, f"Expected 4 questions, got {len(data['questions'])}"
    assert len(data["services"]) == 18, f"Expected 18 services, got {len(data['services'])}"
    print("✓ GET institute demo-laboratory passed.")

    print("\nTesting POST /api/v1/patient/feedback (demo submission)...")
    res = client.post("/api/v1/patient/feedback", json={
        "clinic_id": "11111111-1111-1111-1111-111111111111",
        "rating_score": 5,
        "question_ratings": {0: 5, 1: 5, 2: 5, 3: 5},
        "selected_services": ["Blood Tests", "Health Packages", "Other: MRI Brain"],
        "service_received": "Blood Tests, Health Packages, Other: MRI Brain",
        "language": "te",
        "private_feedback": "Great service and clean laboratory!"
    })
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
    data = res.json()
    assert data["action_flow"] == "POSITIVE"
    assert data["generated_review_draft"] is not None
    print("✓ POST clinic feedback passed. Draft:", data["generated_review_draft"])

    print("\nTesting POST /api/v1/institute-flow/feedback (demo submission)...")
    res = client.post("/api/v1/institute-flow/feedback", json={
        "institute_id": "22222222-2222-2222-2222-222222222222",
        "rating_score": 5,
        "question_ratings": {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5},
        "selected_services": ["Full Body Checkup"],
        "service_received": "Full Body Checkup",
        "language": "en",
        "private_feedback": "Everything was smooth."
    })
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
    data = res.json()
    assert data["action_flow"] == "POSITIVE"
    print("✓ POST institute feedback passed.")

    print("\nTesting Existing Forms Regression:")
    # General Hospital
    hosp_res = client.get("/api/v1/patient/clinic/demo-general-hospital")
    assert hosp_res.status_code == 200
    assert hosp_res.json()["category"] == "General Hospital"
    assert len(hosp_res.json()["questions"]) == 4
    print("✓ Hospital form intact:", hosp_res.json()["category"])

    # Junior College
    jc_res = client.get("/api/v1/institute-flow/institute/demo-junior-college")
    assert jc_res.status_code == 200
    assert jc_res.json()["category"] == "Junior College"
    print("✓ Junior College form intact:", jc_res.json()["category"])

    # IVF
    ivf_res = client.get("/api/v1/patient/clinic/demo-ivf")
    assert ivf_res.status_code == 200
    assert ivf_res.json()["category"] == "IVF"
    print("✓ IVF form intact:", ivf_res.json()["category"])

    print("\nAll API tests passed successfully!")

if __name__ == "__main__":
    test_api()

