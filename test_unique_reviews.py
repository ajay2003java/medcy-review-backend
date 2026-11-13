import sys
from app.services.ai_generator import generate_review_draft
from app.core.constants import ClinicCategory

def test_category_diversity():
    clinic_name = "ABC Hospital"
    categories = [
        (ClinicCategory.DERMATOLOGY, "Acne Treatment"),
        (ClinicCategory.GENERAL_HOSPITAL, "Emergency Care"),
        (ClinicCategory.LABORATORY, "Blood Tests, Full Body Checkup"),
        (ClinicCategory.DENTIST, "Root Canal"),
        (ClinicCategory.IVF, "IVF"),
        (ClinicCategory.GYNECOLOGY, "Pregnancy Checkup")
    ]

    for cat, svc in categories:
        print(f"\n=======================================================")
        print(f"Testing Category: {cat} | Service: {svc}")
        print(f"Clinic Name: {clinic_name}")
        print(f"=======================================================")
        
        generated = []
        for i in range(5):
            review = generate_review_draft(clinic_name, cat, 5, svc)
            assert clinic_name in review, f"Expected '{clinic_name}' in review: {review}"
            assert len(review) > 40, f"Review too short: {review}"
            generated.append(review)
            print(f"Submission {i+1}:\n{review}\n")
        
        # Check uniqueness across submissions
        unique_reviews = set(generated)
        print(f"Unique reviews generated: {len(unique_reviews)} of 5")
        assert len(unique_reviews) >= 4, f"Expected high diversity, got {len(unique_reviews)} unique out of 5"

    print("\n>>> All category diversity & SEO keyword tests passed successfully! <<<")

if __name__ == "__main__":
    test_category_diversity()

