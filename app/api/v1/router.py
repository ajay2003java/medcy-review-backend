from fastapi import APIRouter
from app.api.v1.endpoints import management, patient_flow, institute_management, institute_flow

api_router = APIRouter()
api_router.include_router(management.router, prefix="/management", tags=["management"])
api_router.include_router(patient_flow.router, prefix="/patient", tags=["patient"])
api_router.include_router(institute_management.router, prefix="/institute-management", tags=["institute_management"])
api_router.include_router(institute_flow.router, prefix="/institute-flow", tags=["institute_flow"])
