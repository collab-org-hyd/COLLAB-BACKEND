from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime


class UserCreateDTO(BaseModel):
    """DTO for creating a user"""
    username: str
    email: EmailStr
    display_name: Optional[str] = None
    role: str = "customer"
    bio: Optional[str] = None


class UserResponseDTO(BaseModel):
    """DTO for user response"""
    id: UUID
    username: str
    email: str
    display_name: Optional[str] = None
    role: str
    is_influencer: bool
    created_at: datetime

    class Config:
        from_attributes = True


class AuthCredentialsCreateDTO(BaseModel):
    """DTO for creating auth credentials"""
    user_id: UUID
    password_hash: str
