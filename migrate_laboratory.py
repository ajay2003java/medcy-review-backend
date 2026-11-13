import os, sys
from dotenv import load_dotenv

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)
load_dotenv(os.path.join(backend_dir, ".env"))

from app.db.session import engine
from sqlalchemy import text

def run_migrations():
    # In PostgreSQL, ALTER TYPE ... ADD VALUE cannot run inside a multi-statement transaction block in some versions
    # so we use autocommit connection
    with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
        print("Adding 'Laboratory' to cliniccategory enum...")
        try:
            conn.execute(text("ALTER TYPE cliniccategory ADD VALUE IF NOT EXISTS 'Laboratory';"))
            print("Successfully updated cliniccategory enum.")
        except Exception as e:
            print("Notice/Error updating cliniccategory enum:", e)

        print("Adding 'Laboratory' to institutecategory enum...")
        try:
            conn.execute(text("ALTER TYPE institutecategory ADD VALUE IF NOT EXISTS 'Laboratory';"))
            print("Successfully updated institutecategory enum.")
        except Exception as e:
            print("Notice/Error updating institutecategory enum:", e)

    with engine.begin() as conn:
        print("Updating feedback table columns...")
        conn.execute(text("ALTER TABLE feedback ADD COLUMN IF NOT EXISTS question_ratings JSONB;"))
        conn.execute(text("ALTER TABLE feedback ADD COLUMN IF NOT EXISTS selected_services JSONB;"))
        conn.execute(text("ALTER TABLE feedback ADD COLUMN IF NOT EXISTS language VARCHAR(10) DEFAULT 'en';"))
        conn.execute(text("ALTER TABLE feedback ADD COLUMN IF NOT EXISTS service_received VARCHAR;"))
        print("Successfully updated feedback table.")

        print("Updating institutefeedback table columns...")
        conn.execute(text("ALTER TABLE institutefeedback ADD COLUMN IF NOT EXISTS question_ratings JSONB;"))
        conn.execute(text("ALTER TABLE institutefeedback ADD COLUMN IF NOT EXISTS selected_services JSONB;"))
        conn.execute(text("ALTER TABLE institutefeedback ADD COLUMN IF NOT EXISTS language VARCHAR(10) DEFAULT 'en';"))
        conn.execute(text("ALTER TABLE institutefeedback ALTER COLUMN reviewer_role DROP NOT NULL;"))
        print("Successfully updated institutefeedback table.")

    print("All migrations completed successfully!")

if __name__ == "__main__":
    run_migrations()

