from sqlalchemy import create_engine, text

# Connection pooling URI for Production
DB_URL = "postgresql://postgres.saoawnguumcsnmmzudgv:RebT4aswj8raE6yB@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"

engine = create_engine(DB_URL)
true_logo = "https://plain-apac-prod-public.komododecks.com/202608/10/eXVQP11nnRbLTYDOeJaN/image.png"

try:
    with engine.connect() as conn:
        conn.execute(text("UPDATE clinic SET logo_url = :logo WHERE name = 'vizag ivf center vizanagaram'"), {"logo": true_logo})
        conn.commit()
        print("Logo updated successfully!")
except Exception as e:
    print(f"Error: {e}")
