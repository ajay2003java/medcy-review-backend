from app.db.base_class import Base
from app.db.session import engine
from app.models.clinic import Clinic
from app.models.feedback import Feedback
from app.models.institute import Institute
from app.models.institute_feedback import InstituteFeedback

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done!")
