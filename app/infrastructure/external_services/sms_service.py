"""SMS service for sending OTPs via phone"""

from typing import Optional


class SMSService:
    """Service to send SMS (OTPs, notifications, etc.)"""
    
    def __init__(self, api_key: Optional[str] = None, sender_id: Optional[str] = "COLLAB"):
        """Initialize SMS service with API configuration"""
        self.api_key = api_key
        self.sender_id = sender_id
    
    def send_otp_sms(self, phone_number: str, otp: str) -> bool:
        """
        Send OTP via SMS
        
        Args:
            phone_number: Recipient's phone number
            otp: OTP code
            
        Returns:
            True if SMS sent successfully, False otherwise
        """
        if not self.api_key:
            print(f"[Mock SMS] OTP for {phone_number}: {otp}")
            return True
        
        try:
            # TODO: Integrate with SMS provider (Twilio, AWS SNS, etc.)
            # For now, just log the message
            message = f"Your COLLAB verification code is: {otp}. Valid for 10 minutes. Do not share this code."
            print(f"[SMS] Sending to {phone_number}: {message}")
            return True
        except Exception as e:
            print(f"Error sending SMS: {e}")
            return False
    
    def send_password_reset_confirmation_sms(self, phone_number: str) -> bool:
        """
        Send password reset confirmation via SMS
        
        Args:
            phone_number: Recipient's phone number
            
        Returns:
            True if SMS sent successfully, False otherwise
        """
        if not self.api_key:
            print(f"[Mock SMS] Password reset confirmation sent to {phone_number}")
            return True
        
        try:
            message = "Your COLLAB password has been successfully reset. If this wasn't you, contact support."
            print(f"[SMS] Sending to {phone_number}: {message}")
            return True
        except Exception as e:
            print(f"Error sending SMS: {e}")
            return False
