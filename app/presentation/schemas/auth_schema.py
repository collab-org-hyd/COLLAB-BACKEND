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


class ForgotPasswordRequestOTPRequest(BaseModel):
    """Request schema for forgot password OTP request"""
    email: EmailStr = Field(..., description="User email")


class ForgotPasswordRequestOTPResponse(BaseModel):
    """Response schema for forgot password OTP request"""
    success: bool
    message: str
    identifier: str  # email


class VerifyOTPRequest(BaseModel):
    """Request schema for OTP verification"""
    email: EmailStr = Field(..., description="User email")
    otp: str = Field(..., min_length=6, max_length=6, description="OTP code")


class VerifyOTPResponse(BaseModel):
    """Response schema for OTP verification"""
    success: bool
    message: str
    token: Optional[str] = None  # Temporary token for password reset


class ResetPasswordRequest(BaseModel):
    """Request schema for password reset"""
    email: EmailStr = Field(..., description="User email")
    new_password: str = Field(..., min_length=6, description="New password")
    reset_token: str = Field(..., description="Reset token from OTP verification")


class ResetPasswordResponse(BaseModel):
    """Response schema for password reset"""
    success: bool
    message: str
    user_id: Optional[str] = None


class ResetPasswordDirectRequest(BaseModel):
    """Request schema for direct password reset (without OTP)"""
    email: EmailStr = Field(..., description="User email")
    new_password: str = Field(..., min_length=6, description="New password")


class ResetPasswordDirectResponse(BaseModel):
    """Response schema for direct password reset"""
    success: bool
    message: str
    user_id: Optional[str] = None
    warning: str = "DEPRECATED: This endpoint bypasses OTP verification and should only be used for debugging/testing"
