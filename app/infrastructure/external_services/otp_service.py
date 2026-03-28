"""OTP (One-Time Password) service for email and phone verification"""

import random
import string
from datetime import datetime, timedelta, timezone
from typing import Dict, Tuple


class OTPService:
    """Service to generate, store, and validate OTPs"""
    
    # In-memory storage for OTPs (in production, use Redis or database)
    _otp_store: Dict[str, Dict] = {}
    
    OTP_LENGTH = 6
    OTP_EXPIRY_MINUTES = 10
    MAX_ATTEMPTS = 3
    
    @classmethod
    def generate_otp(cls, identifier: str) -> str:
        """
        Generate a 6-digit OTP for the given identifier (email/phone)
        
        Args:
            identifier: Email or phone number
            
        Returns:
            Generated OTP code
        """
        # Generate 6-digit OTP
        otp = ''.join(random.choices(string.digits, k=cls.OTP_LENGTH))
        
        # Store OTP with expiry
        expiry_time = datetime.now(timezone.utc) + timedelta(minutes=cls.OTP_EXPIRY_MINUTES)
        cls._otp_store[identifier] = {
            'otp': otp,
            'expiry': expiry_time,
            'attempts': 0,
            'verified': False,
            'created_at': datetime.now(timezone.utc)
        }
        
        return otp
    
    @classmethod
    def verify_otp(cls, identifier: str, otp_code: str) -> Tuple[bool, str]:
        """
        Verify OTP for the given identifier
        
        Args:
            identifier: Email or phone number
            otp_code: OTP code to verify
            
        Returns:
            Tuple of (is_valid, message)
        """
        if identifier not in cls._otp_store:
            return False, "OTP not found. Please request a new OTP."
        
        otp_data = cls._otp_store[identifier]
        
        # Check if OTP is expired
        if datetime.now(timezone.utc) > otp_data['expiry']:
            del cls._otp_store[identifier]
            return False, "OTP has expired. Please request a new OTP."
        
        # Check attempt count
        if otp_data['attempts'] >= cls.MAX_ATTEMPTS:
            del cls._otp_store[identifier]
            return False, "Maximum OTP attempts exceeded. Please request a new OTP."
        
        # Verify OTP
        if otp_data['otp'] != otp_code:
            otp_data['attempts'] += 1
            remaining_attempts = cls.MAX_ATTEMPTS - otp_data['attempts']
            return False, f"Invalid OTP. {remaining_attempts} attempts remaining."
        
        # Mark as verified
        otp_data['verified'] = True
        return True, "OTP verified successfully"
    
    @classmethod
    def is_otp_verified(cls, identifier: str) -> bool:
        """Check if OTP is verified for the identifier"""
        if identifier not in cls._otp_store:
            return False
        return cls._otp_store[identifier]['verified']
    
    @classmethod
    def clear_otp(cls, identifier: str) -> None:
        """Clear OTP for the identifier after password reset"""
        if identifier in cls._otp_store:
            del cls._otp_store[identifier]
    
    @classmethod
    def get_otp(cls, identifier: str) -> str:
        """Get OTP for testing purposes (should be used only in development)"""
        if identifier in cls._otp_store:
            return cls._otp_store[identifier]['otp']
        return None
