"""
Session endpoints for SBTM v2 API
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models import models
from app.schemas import sessions as session_schemas

router = APIRouter()


@router.get("/", response_model=List[session_schemas.SessionResponse])
def get_sessions(
    project_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all sessions, optionally filtered by project"""
    query = db.query(models.Session)
    
    if project_id:
        query = query.filter(models.Session.project_id == project_id)
    
    sessions = query.offset(skip).limit(limit).all()
    return sessions


@router.get("/{session_id}", response_model=session_schemas.SessionResponse)
def get_session(session_id: int, db: Session = Depends(get_db)):
    """Get a specific session by ID"""
    session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.post("/", response_model=session_schemas.SessionResponse)
def create_session(
    session_data: session_schemas.SessionCreate,
    db: Session = Depends(get_db)
):
    """Create a new session"""
    db_session = models.Session(**session_data.dict())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


@router.put("/{session_id}", response_model=session_schemas.SessionResponse)
def update_session(
    session_id: int,
    session_data: session_schemas.SessionUpdate,
    db: Session = Depends(get_db)
):
    """Update a session"""
    session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    for field, value in session_data.dict(exclude_unset=True).items():
        setattr(session, field, value)
    
    db.commit()
    db.refresh(session)
    return session


@router.delete("/{session_id}")
def delete_session(session_id: int, db: Session = Depends(get_db)):
    """Delete a session"""
    session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db.delete(session)
    db.commit()
    return {"message": "Session deleted successfully"}