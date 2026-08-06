from app.db.session import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("SELECT enumlabel FROM pg_enum JOIN pg_type ON pg_enum.enumtypid = pg_type.oid WHERE typname = 'cliniccategory';")).fetchall()
    print("Enum values in DB:")
    for row in result:
        print(row[0])
