from fastapi import APIRouter
from app.api.v1.endpoints import management, patient_flow

api_router = APIRouter()
api_router.include_router(management.router, prefix="/management", tags=["management"])
api_router.include_router(patient_flow.router, prefix="/patient", tags=["patient"])
