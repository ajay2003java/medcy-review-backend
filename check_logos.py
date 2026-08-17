from sqlalchemy import create_engine, text

# Connection pooling URI for Production
DB_URL = "postgresql://postgres.saoawnguumcsnmmzudgv:RebT4aswj8raE6yB@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"

engine = create_engine(DB_URL)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, name, logo_url FROM institute WHERE name ILIKE '%bansal%'"))
        institutes = result.fetchall()
        for i in institutes:
            print(f"Name: {i.name}")
            print(f"Logo URL: {i.logo_url}")
            print("-" * 30)
except Exception as e:
    print(f"Error: {e}")
