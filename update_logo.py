import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("SQLALCHEMY_DATABASE_URI")

if DB_URL.startswith("postgresql+asyncpg://"):
    DB_URL = DB_URL.replace("postgresql+asyncpg://", "postgresql://", 1)

engine = create_engine(DB_URL)

try:
    with engine.begin() as conn:
        # Check if the institute exists matching the qr_identifier
        result = conn.execute(text("SELECT id, name, qr_identifier FROM institute WHERE qr_identifier LIKE '4be77d65%'"))
        institutes = result.fetchall()
        
        if not institutes:
            print("No institute found with qr_identifier starting with '4be77d65'")
        else:
            for inst in institutes:
                print(f"Found institute: {inst.name} (QR: {inst.qr_identifier})")
                conn.execute(
                    text("UPDATE institute SET logo_url = :logo_url WHERE id = :id"),
                    {"logo_url": "https://plain-apac-prod-public.komododecks.com/202608/17/j0WLmidDIs84I0JTcNMN/image.jpg", "id": inst.id}
                )
                print(f"Updated logo_url for {inst.name}")
except Exception as e:
    print(f"Error: {e}")
