import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URI")
if not DATABASE_URL:
    raise Exception("SQLALCHEMY_DATABASE_URI is not set")
# Use sync psycopg2 driver
if DATABASE_URL.startswith("postgresql+asyncpg://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://", 1)

def alter_table():
    engine = create_engine(DATABASE_URL, echo=True)
    with engine.begin() as conn:
        try:
            conn.execute(
                text("ALTER TABLE institutefeedback ADD COLUMN IF NOT EXISTS service_received VARCHAR;")
            )
            print("Successfully added service_received column to institutefeedback table.")
        except Exception as e:
            print(f"Error altering table: {e}")

if __name__ == "__main__":
    alter_table()
