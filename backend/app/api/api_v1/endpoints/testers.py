"""
Tester endpoints for SBTM v2 API
"""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models import models

router = APIRouter()


@router.get("/")
def get_testers(db: Session = Depends(get_db)):
    """Get all testers"""
    return db.query(models.Tester).all()


@router.get("/{tester_id}")
def get_tester(tester_id: int, db: Session = Depends(get_db)):
    """Get a specific tester"""
    return db.query(models.Tester).filter(models.Tester.id == tester_id).first()