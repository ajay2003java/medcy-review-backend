from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.institute import InstituteCreate, Institute
from app.crud import crud_institute
from typing import List

router = APIRouter()

@router.post("/", response_model=Institute, status_code=status.HTTP_201_CREATED)
def create_institute(institute: InstituteCreate, db: Session = Depends(get_db)):
    """
    Onboard a new educational institute.
    """
    return crud_institute.create_institute(db, institute)

@router.get("/", response_model=List[Institute])
def list_institutes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all onboarded institutes.
    """
    return crud_institute.get_institutes(db, skip=skip, limit=limit)
