from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.clinic import ClinicCreate, Clinic
from app.crud import crud_clinic
from typing import List

router = APIRouter()

@router.post("/", response_model=Clinic, status_code=status.HTTP_201_CREATED)
def create_clinic(clinic: ClinicCreate, db: Session = Depends(get_db)):
    """
    Onboard a new clinic (Used internally by Medcy Team).
    """
    return crud_clinic.create_clinic(db, clinic)

@router.get("/", response_model=List[Clinic])
def list_clinics(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all onboarded clinics.
    """
    return crud_clinic.get_clinics(db, skip=skip, limit=limit)
