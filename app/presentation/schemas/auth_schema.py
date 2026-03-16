from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class LoginRequest(BaseModel):
    """Request schema for login"""
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., min_length=6, description="User password")


class LoginResponse(BaseModel):
    """Response schema for login"""
    success: bool
    user_id: str
    username: str
    email: str
    role: str
    message: str


class RegisterRequest(BaseModel):
    """Request schema for user registration"""
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., min_length=6, description="User password")
    display_name: str = Field(None, max_length=255, description="Display name")
    role: str = Field(default="customer", description="User role")


class RegisterResponse(BaseModel):
    """Response schema for user registration"""
    success: bool
    user_id: str
    username: str
    email: str
    message: str


class ValidateEmailRequest(BaseModel):
    """Request schema for email validation"""
    email: EmailStr = Field(..., description="Email to validate")


class ValidateEmailData(BaseModel):
    """Data object for email validation response"""
    emailId: str = Field(..., description="Email being validated")


class ValidateEmailResponse(BaseModel):
    """Response schema for email validation"""
    status: bool = Field(..., description="Whether email exists in database")
    message: str = Field(..., description="Response message")
    data: Optional[ValidateEmailData] = Field(None, description="Response data")
