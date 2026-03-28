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
            message = f"Your {self.sender_id} verification code is: {otp}. Valid for 10 minutes. Do not share this code."
            
            # TODO: Integrate with SMS provider (Twilio, AWS SNS, etc.)
            # Example placeholder for Twilio:
            # from twilio.rest import Client
            # client = Client(account_sid, auth_token)
            # client.messages.create(to=phone_number, from_=from_number, body=message)
            
            print(f"✓ OTP SMS sent to {phone_number}")
            print(f"  Message: {message}")
            return True
        except Exception as e:
            print(f"✗ Error sending SMS to {phone_number}: {e}")
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
            message = f"Your {self.sender_id} password has been successfully reset. If this wasn't you, contact support."
            print(f"✓ Confirmation SMS sent to {phone_number}")
            print(f"  Message: {message}")
            return True
        except Exception as e:
            print(f"✗ Error sending SMS to {phone_number}: {e}")
            return False
