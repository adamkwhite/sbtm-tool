"""
Project endpoints for SBTM v2 API
"""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models import models

router = APIRouter()


@router.get("/")
def get_projects(db: Session = Depends(get_db)):
    """Get all projects"""
    return db.query(models.Project).all()


@router.get("/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db)):
    """Get a specific project"""
    return db.query(models.Project).filter(models.Project.id == project_id).first()