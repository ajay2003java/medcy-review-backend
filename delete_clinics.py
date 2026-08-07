from sqlalchemy import create_engine, text

# Connection pooling URI for Production
DB_URL = "postgresql://postgres.saoawnguumcsnmmzudgv:RebT4aswj8raE6yB@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"

engine = create_engine(DB_URL)

try:
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(text("UPDATE clinic SET logo_url = 'https://plain-apac-prod-public.komododecks.com/202608/07/HC4TTimm9fPrPd7AivDZ/image.png' WHERE qr_identifier = 'e0f507f7';"))
            print("Successfully fixed logo URL in database!")
except Exception as e:
    print("Error:", e)
