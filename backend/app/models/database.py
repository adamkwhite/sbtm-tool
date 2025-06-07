"""
Database configuration and session management for SBTM v2
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings

# Create SQLAlchemy engine
engine = create_engine(
    str(settings.DATABASE_URL),
    pool_pre_ping=True,
    echo=(settings.ENVIRONMENT == "development"),
    connect_args={
        "check_same_thread": False  # Only needed for SQLite
    } if "sqlite" in str(settings.DATABASE_URL) else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


async def init_db():
    """Initialize the database"""
    # Import all models to ensure they are registered
    from app.models import models  # noqa
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create default project if needed
    db = SessionLocal()
    try:
        from app.models.models import Project
        if not db.query(Project).first():
            default_project = Project(
                name="Default Project",
                description="Default SBTM v2 project"
            )
            db.add(default_project)
            db.commit()
    finally:
        db.close()


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()