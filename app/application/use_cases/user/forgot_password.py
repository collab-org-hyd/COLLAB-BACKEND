"""Use case for forgot password flow"""

from typing import Dict, Optional
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.external_services.otp_service import OTPService
from app.infrastructure.external_services.email_service import EmailService
from app.infrastructure.external_services.sms_service import SMSService
from app.core.exceptions import (
    ResourceNotFoundError,
    BadRequestError,
    AuthenticationError
)
import secrets
import hashlib


class ForgotPasswordRequestOTPUseCase:
    """Use case to request OTP for password reset"""
    
    def __init__(self, user_repository: UserRepository, email_service: Optional[EmailService] = None, sms_service: Optional[SMSService] = None):
        self.user_repository = user_repository
        self.otp_service = OTPService()
        self.email_service = email_service or EmailService()
        self.sms_service = sms_service or SMSService()
    
    async def execute(self, email: Optional[str] = None, phone_number: Optional[str] = None) -> Dict:
        """
        Request OTP for password reset
        
        Args:
            email: User email (either email or phone_number must be provided)
            phone_number: User phone number (either email or phone_number must be provided)
            
        Returns:
            Dict with success status, message, and identifier
        """
        if not email and not phone_number:
            raise BadRequestError("Either email or phone_number must be provided")
        
        # Determine identifier
        identifier = email or phone_number
        
        # Check if user exists with this email or phone
        user = None
        if email:
            user = await self.user_repository.find_by_email(email)
        elif phone_number:
            user = await self.user_repository.find_by_phone(phone_number)
        
        if not user:
            raise ResourceNotFoundError("User not found")
        
        # Generate OTP
        otp = self.otp_service.generate_otp(identifier)
        
        # Send OTP via email or SMS
        sent_successfully = False
        if email:
            sent_successfully = self.email_service.send_otp_email(email, otp, user.display_name or user.username)
        elif phone_number:
            sent_successfully = self.sms_service.send_otp_sms(phone_number, otp)
        
        if not sent_successfully:
            raise BadRequestError("Failed to send OTP. Please try again.")
        
        return {
            "success": True,
            "message": f"OTP sent to {identifier}",
            "identifier": identifier
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
    
    def __init__(self, user_repository: UserRepository, email_service: Optional[EmailService] = None, sms_service: Optional[SMSService] = None):
        self.user_repository = user_repository
        self.otp_service = OTPService()
        self.email_service = email_service or EmailService()
        self.sms_service = sms_service or SMSService()
    
    async def execute(self, identifier: str, new_password: str, reset_token: str) -> Dict:
        """
        Reset password after OTP verification
        
        Args:
            identifier: Email or phone number
            new_password: New password
            reset_token: Reset token from OTP verification
            
        Returns:
            Dict with success status and message
        """
        # Check if OTP was verified
        if not self.otp_service.is_otp_verified(identifier):
            raise AuthenticationError("OTP not verified. Please verify OTP first.")
        
        # Find user by email or phone
        user = None
        if "@" in identifier:  # Email
            user = await self.user_repository.find_by_email(identifier)
        else:  # Phone
            user = await self.user_repository.find_by_phone(identifier)
        
        if not user:
            raise ResourceNotFoundError("User not found")
        
        # Hash password
        password_hash = hashlib.sha256(new_password.encode()).hexdigest()
        
        # Update password in auth credentials
        await self.user_repository.update_password(user.id, password_hash)
        
        # Send confirmation email or SMS
        if "@" in identifier:  # Email
            self.email_service.send_password_reset_confirmation(identifier, user.display_name or user.username)
        else:  # Phone
            self.sms_service.send_password_reset_confirmation_sms(identifier)
        
        # Clear OTP
        self.otp_service.clear_otp(identifier)
        
        return {
            "success": True,
            "message": "Password reset successfully",
            "user_id": str(user.id)
        }
