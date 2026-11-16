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
        # Update sms diagnostic center
        res = conn.execute(
            text("UPDATE clinic SET logo_url = :url WHERE qr_identifier = :qr RETURNING id, name, qr_identifier, logo_url"),
            {
                "url": "https://plain-apac-prod-public.komododecks.com/202611/16/p3NyglOoQsrkeA1M6z5T/image.png",
                "qr": "aef79f18"
            }
        )
        print("Updated clinic:", res.fetchall())

        # Update bansal junior college
        res2 = conn.execute(
            text("UPDATE institute SET logo_url = :url WHERE qr_identifier = :qr RETURNING id, name, qr_identifier, logo_url"),
            {
                "url": "https://plain-apac-prod-public.komododecks.com/202608/17/j0WLmidDIs84I0JTcNMN/image.jpg",
                "qr": "de50e3c3"
            }
        )
        print("Updated institute:", res2.fetchall())
except Exception as e:
    print(f"Error: {e}")
