from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
from enum import Enum
from typing import Optional, List


class UserRole(str, Enum):
    """User role enumeration"""
    CUSTOMER = "customer"
    INFLUENCER = "influencer"
    ADMIN = "admin"


@dataclass
class User:
    """User domain entity"""
    id: UUID
    username: str
    email: str
    display_name: Optional[str] = None
    role: UserRole = UserRole.CUSTOMER
    is_influencer: bool = False
    tags: Optional[List[str]] = None
    can_request_service: bool = True
    can_fulfill_service: bool = False
    bio: Optional[str] = None
    business_link: Optional[str] = None
    yt_link: Optional[str] = None
    x_link: Optional[str] = None
    facebook_link: Optional[str] = None
    other_link: Optional[str] = None
    what_to_expect: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class AuthCredentials:
    """Authentication credentials domain entity"""
    id: UUID
    user_id: UUID
    password_hash: str
    created_at: datetime = field(default_factory=datetime.utcnow)
