from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
from app.config.settings import settings

# Database engine with psycopg2 optimizations
db_url = settings.database_url

# Ensure we're using psycopg2 driver
if db_url and not db_url.startswith("postgresql+psycopg2://"):
    if db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)

engine = create_engine(
    db_url,
    echo=False,  # Set to False to reduce noise, enable for debugging
    pool_pre_ping=True,
    pool_recycle=3600,
    poolclass=NullPool,  # Use NullPool for scripts to avoid connection issues
    connect_args={
        "connect_timeout": 10,
    },
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for models
Base = declarative_base()


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
