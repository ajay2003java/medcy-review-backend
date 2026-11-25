import uuid
from sqlalchemy import text
from app.db.session import SessionLocal

def run_migration():
    db = SessionLocal()
    try:
        print("1. Adding doctor_name column to feedback and institutefeedback tables...")
        db.execute(text("ALTER TABLE feedback ADD COLUMN IF NOT EXISTS doctor_name VARCHAR;"))
        db.execute(text("ALTER TABLE institutefeedback ADD COLUMN IF NOT EXISTS doctor_name VARCHAR;"))
        db.commit()
        print("Columns added successfully.")

        print("2. Checking / creating Kishore Bhavana Clinic in clinic table...")
        clinic_id = "b0101010-b010-b010-b010-b01010101010"
        existing = db.execute(text("SELECT id, name FROM clinic WHERE id = :id OR qr_identifier = 'kishore-bhavana'"), {"id": clinic_id}).fetchone()
        
        if existing:
            print(f"Clinic already exists: {existing}")
        else:
            db.execute(text("""
                INSERT INTO clinic (id, name, logo_url, theme_color, google_review_url, category, status, qr_identifier)
                VALUES (:id, :name, :logo, :color, :g_url, 'General Hospital', 'ACTIVE', 'kishore-bhavana')
            """), {
                "id": clinic_id,
                "name": "Kishore Bhavana Clinic",
                "logo": None,
                "color": "#0284c7",
                "g_url": "https://search.google.com/local/writereview?placeid=ChIJ_kishore_bhavana_clinic"
            })
            db.commit()
            print("Kishore Bhavana Clinic inserted successfully into clinic table.")

        print("Migration complete!")
    except Exception as e:
        db.rollback()
        print(f"Migration error: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    run_migration()
