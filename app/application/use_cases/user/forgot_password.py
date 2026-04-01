"""Use case for forgot password flow"""

from typing import Dict, Optional
from app.domain.repositories.user_repository import UserRepository, AuthCredentialsRepository
from app.infrastructure.external_services.otp_service import OTPService
from app.infrastructure.external_services.email_service import EmailService
from app.core.exceptions import (
    ResourceNotFoundError,
    BadRequestError,
    AuthenticationError
)
from app.core.security import hash_password, verify_password
import secrets
import hashlib


class ForgotPasswordRequestOTPUseCase:
    """Use case to request OTP for password reset"""
    
    def __init__(self, user_repository: UserRepository, email_service: Optional[EmailService] = None):
        self.user_repository = user_repository
        self.otp_service = OTPService()
        self.email_service = email_service or EmailService()
    
    async def execute(self, email: str) -> Dict:
        """
        Request OTP for password reset
        
        Args:
            email: User email
            
        Returns:
            Dict with success status, message, and identifier
        """
        if not email:
            raise BadRequestError("Email is required")
        
        # Check if user exists with this email
        user = await self.user_repository.find_by_email(email)
        
        if not user:
            raise ResourceNotFoundError("User not found")
        
        # Generate OTP
        otp = self.otp_service.generate_otp(email)
        
        # Send OTP via email
        sent_successfully = self.email_service.send_otp_email(email, otp, user.display_name or user.username)
        
        if not sent_successfully:
            raise BadRequestError("Failed to send OTP. Please try again.")
        
        return {
            "success": True,
            "message": f"OTP sent to {email}",
            "identifier": email
        }


class VerifyOTPUseCase:
    """Use case to verify OTP during password reset"""
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.otp_service = OTPService()
    
    async def execute(self, identifier: str, otp_code: str) -> Dict:
        """
        Verify OTP for password reset
        
        Args:
            identifier: Email or phone number
            otp_code: OTP code to verify
            
        Returns:
            Dict with success status, message, and reset token
        """
        # Verify OTP
        is_valid, message = self.otp_service.verify_otp(identifier, otp_code)
        
        if not is_valid:
            raise AuthenticationError(message)
        
        # Generate reset token
        reset_token = secrets.token_urlsafe(32)
        
        # Store reset token (in production, store with expiry in Redis or database)
        # For now, we'll just return it and expect it to be provided in password reset
        
        return {
            "success": True,
            "message": "OTP verified successfully",
            "reset_token": reset_token,
            "identifier": identifier
        }


class ResetPasswordUseCase:
    """Use case to reset password after OTP verification"""
    
    def __init__(self, user_repository: UserRepository, email_service: Optional[EmailService] = None):
        self.user_repository = user_repository
        self.otp_service = OTPService()
        self.email_service = email_service or EmailService()
    
    async def execute(self, email: str, new_password: str, reset_token: str) -> Dict:
        """
        Reset password after OTP verification
        
        Args:
            email: User email
            new_password: New password
            reset_token: Reset token from OTP verification
            
        Returns:
            Dict with success status and message
        """
        # Check if OTP was verified
        if not self.otp_service.is_otp_verified(email):
            raise AuthenticationError("OTP not verified. Please verify OTP first.")
        
        # Find user by email
        user = await self.user_repository.find_by_email(email)
        
        if not user:
            raise ResourceNotFoundError("User not found")
        
        # Hash password
        password_hash = hashlib.sha256(new_password.encode()).hexdigest()
        
        # Update password in auth credentials
        await self.user_repository.update_password(user.id, password_hash)
        
        # Send confirmation email
        self.email_service.send_password_reset_confirmation(email, user.display_name or user.username)
        
        # Clear OTP
        self.otp_service.clear_otp(email)
        
        return {
            "success": True,
            "message": "Password reset successfully",
            "user_id": str(user.id)
        }


class ResetPasswordDirectUseCase:
    """
    Use case to reset password without OTP (for debugging - NO password verification)
    
    ⚠️  DEPRECATED: This is for testing/debugging only. Allows password reset without 
    verifying current password. Should NEVER be used in production.
    """
    
    def __init__(self, user_repository: UserRepository, auth_repository: AuthCredentialsRepository, email_service: Optional[EmailService] = None):
        self.user_repository = user_repository
        self.auth_repository = auth_repository
        self.email_service = email_service or EmailService()
    
    async def execute(self, email: str, new_password: str) -> Dict:
        """
        Reset password without OTP verification or current password check.
        
        ⚠️  WARNING: This function is for debugging/testing only. It bypasses all 
        security checks. Remove before production deployment.
        
        Args:
            email: User email
            new_password: New password
            
        Returns:
            Dict with success status and message
        """
        if not email:
            raise BadRequestError("Email is required")
        
        if not new_password:
            raise BadRequestError("New password is required")
        
        # Find user by email
        user = await self.user_repository.find_by_email(email)
        
        if not user:
            raise ResourceNotFoundError("User not found")
        
        # Hash new password
        password_hash = hash_password(new_password)
        
        # Update password in auth credentials
        await self.user_repository.update_password(user.id, password_hash)
        
        # Try to send confirmation email (but don't fail if email service is broken)
        if self.email_service:
            try:
                self.email_service.send_password_reset_confirmation(email, user.display_name or user.username)
            except Exception:
                # Continue even if email fails to send (since email is not working)
                pass
        
        return {
            "success": True,
            "message": "Password reset successfully (DEBUG MODE - No verification required)",
            "user_id": str(user.id)
        }
