from sqlalchemy import create_engine, text

# Connection pooling URI for Production
DB_URL = "postgresql://postgres.saoawnguumcsnmmzudgv:RebT4aswj8raE6yB@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"

engine = create_engine(DB_URL)

try:
    with engine.connect() as conn:
        # Start a transaction
        with conn.begin():
            conn.execute(text("DELETE FROM clinic WHERE id != '0a7eb363-0e25-4fe8-adcb-02b862901a18';"))
            print("Successfully deleted test clinics.")
except Exception as e:
    print("Error:", e)
