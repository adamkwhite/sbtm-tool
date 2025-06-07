"""
Pydantic schemas for Session endpoints
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class SessionBase(BaseModel):
    """Base session schema"""
    project_id: int
    local_charter: Optional[str] = None
    t_metric: float = Field(0.0, ge=0.0, le=100.0)
    b_metric: float = Field(0.0, ge=0.0, le=100.0)
    s_metric: float = Field(0.0, ge=0.0, le=100.0)
    start_time: Optional[datetime] = None
    duration: Optional[int] = None
    status: str = "Not Started"
    notes: Optional[str] = None


class SessionCreate(SessionBase):
    """Schema for creating a session"""
    pass


class SessionUpdate(BaseModel):
    """Schema for updating a session"""
    local_charter: Optional[str] = None
    t_metric: Optional[float] = Field(None, ge=0.0, le=100.0)
    b_metric: Optional[float] = Field(None, ge=0.0, le=100.0)
    s_metric: Optional[float] = Field(None, ge=0.0, le=100.0)
    start_time: Optional[datetime] = None
    duration: Optional[int] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class SessionResponse(SessionBase):
    """Schema for session responses"""
    id: int
    version: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True