"""
Charter endpoints for SBTM v2 API
"""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models import models

router = APIRouter()


@router.get("/")
def get_charters(db: Session = Depends(get_db)):
    """Get all charters"""
    return db.query(models.Charter).all()


@router.get("/{charter_id}")
def get_charter(charter_id: int, db: Session = Depends(get_db)):
    """Get a specific charter"""
    return db.query(models.Charter).filter(models.Charter.id == charter_id).first()