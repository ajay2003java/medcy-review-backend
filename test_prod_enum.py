from sqlalchemy import create_engine, text

# Connection pooling URI for Production
DB_URL = "postgresql://postgres.saoawnguumcsnmmzudgv:RebT4aswj8raE6yB@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"

engine = create_engine(DB_URL)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT enumlabel FROM pg_enum JOIN pg_type ON pg_enum.enumtypid = pg_type.oid WHERE typname = 'cliniccategory';")).fetchall()
        print("Production Enum values in DB:")
        for row in result:
            print(row[0])
except Exception as e:
    print("Error:", e)
