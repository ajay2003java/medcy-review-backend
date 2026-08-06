import app.db.base
from app.db.session import SessionLocal
from app.crud.crud_clinic import create_clinic
from app.schemas.clinic import ClinicCreate

db = SessionLocal()
try:
    c = ClinicCreate(name='T', category='Dentist', google_review_url='http://google.com', theme_color='#ffffff')
    create_clinic(db, c)
    print("Success")
except Exception as e:
    import traceback
    traceback.print_exc()
