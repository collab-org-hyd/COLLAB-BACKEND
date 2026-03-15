from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from datetime import datetime, timezone
from uuid import uuid4
import enum

from app.config.database import Base


class UserRole(str, enum.Enum):
    """User role enumeration"""
    CUSTOMER = "customer"
    INFLUENCER = "influencer"
    ADMIN = "admin"


class UserModel(Base):
    """User database model"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    display_name = Column(String(255), nullable=True)
    role = Column(SQLEnum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    is_influencer = Column(Boolean, default=False, nullable=False)
    tags = Column(ARRAY(String), nullable=True)  # PostgreSQL ARRAY type
    can_request_service = Column(Boolean, default=True, nullable=False)
    can_fulfill_service = Column(Boolean, default=False, nullable=False)
    bio = Column(Text, nullable=True)
    business_link = Column(String(500), nullable=True)
    yt_link = Column(String(500), nullable=True)
    x_link = Column(String(500), nullable=True)
    facebook_link = Column(String(500), nullable=True)
    other_link = Column(String(500), nullable=True)
    what_to_expect = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class AuthCredentialsModel(Base):
    """Authentication credentials database model"""
    __tablename__ = "auth_credentials"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
