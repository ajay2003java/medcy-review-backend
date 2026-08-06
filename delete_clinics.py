from sqlalchemy import create_engine, text

# Connection pooling URI for Production
DB_URL = "postgresql://postgres.saoawnguumcsnmmzudgv:RebT4aswj8raE6yB@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"

engine = create_engine(DB_URL)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, name, logo_url, qr_identifier FROM clinic ORDER BY created_at DESC;")).fetchall()
        print("Clinics in DB:")
        for row in result:
            print(f"Name: {row[1]}, Logo URL: {row[2]}, QR: {row[3]}")
except Exception as e:
    print("Error:", e)
