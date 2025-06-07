"""
Database models for SBTM v2
Enhanced SQLAlchemy models based on the original SBTM tool
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Table, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.models.database import Base

# Association tables for many-to-many relationships
session_charters = Table('session_charters', Base.metadata,
    Column('session_id', Integer, ForeignKey('sessions.id')),
    Column('charter_id', Integer, ForeignKey('charters.id'))
)

session_testers = Table('session_testers', Base.metadata,
    Column('session_id', Integer, ForeignKey('sessions.id')),
    Column('tester_id', Integer, ForeignKey('testers.id'))
)

session_products = Table('session_products', Base.metadata,
    Column('session_id', Integer, ForeignKey('sessions.id')),
    Column('product_id', Integer, ForeignKey('products.id'))
)

session_environments = Table('session_environments', Base.metadata,
    Column('session_id', Integer, ForeignKey('sessions.id')),
    Column('environment_id', Integer, ForeignKey('test_environments.id'))
)

session_documents = Table('session_documents', Base.metadata,
    Column('session_id', Integer, ForeignKey('sessions.id')),
    Column('document_id', Integer, ForeignKey('documents.id'))
)

session_tags = Table('session_tags', Base.metadata,
    Column('session_id', Integer, ForeignKey('sessions.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

charter_documents = Table('charter_documents', Base.metadata,
    Column('charter_id', Integer, ForeignKey('charters.id')),
    Column('document_id', Integer, ForeignKey('documents.id'))
)

charter_tags = Table('charter_tags', Base.metadata,
    Column('charter_id', Integer, ForeignKey('charters.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

tester_tags = Table('tester_tags', Base.metadata,
    Column('tester_id', Integer, ForeignKey('testers.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

product_tags = Table('product_tags', Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

environment_documents = Table('environment_documents', Base.metadata,
    Column('environment_id', Integer, ForeignKey('test_environments.id')),
    Column('document_id', Integer, ForeignKey('documents.id'))
)

environment_tags = Table('environment_tags', Base.metadata,
    Column('environment_id', Integer, ForeignKey('test_environments.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

document_tags = Table('document_tags', Base.metadata,
    Column('document_id', Integer, ForeignKey('documents.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)


class Project(Base):
    """Project model - supports multi-project isolation"""
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    settings = Column(JSON)  # Project-specific settings
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class User(Base):
    """User model for authentication and access control"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    role = Column(String(50), default='tester')  # tester, test_lead, manager
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Session(Base):
    """Session model - core SBTM session entity"""
    __tablename__ = 'sessions'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    local_charter = Column(Text)  # Up to 2k characters
    t_metric = Column(Float, nullable=False, default=0.0)  # Testing percentage
    b_metric = Column(Float, nullable=False, default=0.0)  # Bug investigation percentage
    s_metric = Column(Float, nullable=False, default=0.0)  # Setup/admin percentage
    start_time = Column(DateTime)
    duration = Column(Integer)  # Duration in minutes
    status = Column(String(50), default='Not Started')  # Not Started/In Progress/Completed/Accepted
    notes = Column(Text)  # 32K characters of markdown
    version = Column(Integer, default=1)  # For version history
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project")
    created_by_user = relationship("User")
    charters = relationship("Charter", secondary=session_charters, back_populates="sessions")
    testers = relationship("Tester", secondary=session_testers, back_populates="sessions")
    products = relationship("Product", secondary=session_products, back_populates="sessions")
    environments = relationship("TestEnvironment", secondary=session_environments, back_populates="sessions")
    documents = relationship("Document", secondary=session_documents, back_populates="sessions")
    tags = relationship("Tag", secondary=session_tags, back_populates="sessions")


class SessionHistory(Base):
    """Session version history for audit trail"""
    __tablename__ = 'session_history'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('sessions.id'), nullable=False)
    version = Column(Integer, nullable=False)
    changes = Column(JSON)  # Store what changed
    changed_by = Column(Integer, ForeignKey('users.id'))
    changed_at = Column(DateTime, default=datetime.utcnow)
    
    session = relationship("Session")
    changed_by_user = relationship("User")


class SessionTemplate(Base):
    """Session template model"""
    __tablename__ = 'session_templates'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    name = Column(String(255), nullable=False)
    notes = Column(Text)
    local_charter = Column(Text)
    group = Column(String(255))  # For organizing templates
    created_at = Column(DateTime, default=datetime.utcnow)
    
    project = relationship("Project")


class Charter(Base):
    """Charter model - reusable charter templates"""
    __tablename__ = 'charters'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    charter_statement = Column(Text, nullable=False)  # Up to 32K characters
    group = Column(String(255))  # For organizing charters
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project")
    sessions = relationship("Session", secondary=session_charters, back_populates="charters")
    documents = relationship("Document", secondary=charter_documents, back_populates="charters")
    tags = relationship("Tag", secondary=charter_tags, back_populates="charters")


class Tester(Base):
    """Tester model - can be project-specific"""
    __tablename__ = 'testers'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id'))  # Link to system user if exists
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project = relationship("Project")
    user = relationship("User")
    sessions = relationship("Session", secondary=session_testers, back_populates="testers")
    tags = relationship("Tag", secondary=tester_tags, back_populates="testers")


class Product(Base):
    """Product model with version tracking"""
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(Text)
    version = Column(String(128))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project = relationship("Project")
    sessions = relationship("Session", secondary=session_products, back_populates="products")
    tags = relationship("Tag", secondary=product_tags, back_populates="products")


class TestEnvironment(Base):
    """Test environment model with versioning"""
    __tablename__ = 'test_environments'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(Text)
    version = Column(String(128))
    configuration = Column(JSON)  # Environment-specific config
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project")
    sessions = relationship("Session", secondary=session_environments, back_populates="environments")
    documents = relationship("Document", secondary=environment_documents, back_populates="environments")
    tags = relationship("Tag", secondary=environment_tags, back_populates="environments")


class Tag(Base):
    """Hierarchical tag system"""
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    name = Column(String(80), nullable=False)
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey('tags.id'))  # For hierarchical tags
    color = Column(String(7))  # Hex color code
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project = relationship("Project")
    parent = relationship("Tag", remote_side=[id])
    children = relationship("Tag", overlaps="parent")
    
    sessions = relationship("Session", secondary=session_tags, back_populates="tags")
    charters = relationship("Charter", secondary=charter_tags, back_populates="tags")
    testers = relationship("Tester", secondary=tester_tags, back_populates="tags")
    products = relationship("Product", secondary=product_tags, back_populates="tags")
    environments = relationship("TestEnvironment", secondary=environment_tags, back_populates="tags")
    documents = relationship("Document", secondary=document_tags, back_populates="tags")


class Document(Base):
    """Document repository with version control"""
    __tablename__ = 'documents'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    path = Column(String(500), nullable=False)
    title = Column(String(255), nullable=False)
    current_version = Column(String(50), nullable=False)
    file_content = Column(Text)  # Store file content or reference
    doc_metadata = Column(JSON)  # Additional document metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project")
    sessions = relationship("Session", secondary=session_documents, back_populates="documents")
    charters = relationship("Charter", secondary=charter_documents, back_populates="documents")
    environments = relationship("TestEnvironment", secondary=environment_documents, back_populates="documents")
    tags = relationship("Tag", secondary=document_tags, back_populates="documents")