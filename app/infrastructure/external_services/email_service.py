"""Email service for sending OTPs and notifications"""

from typing import Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailService:
    """Service to send emails (OTPs, notifications, etc.)"""
    
    def __init__(self, smtp_server: str = "smtp.gmail.com", smtp_port: int = 587, sender_email: Optional[str] = None, sender_password: Optional[str] = None):
        """Initialize email service with SMTP configuration"""
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
    
    def send_otp_email(self, recipient_email: str, otp: str, user_name: Optional[str] = None) -> bool:
        """
        Send OTP via email
        
        Args:
            recipient_email: Recipient's email address
            otp: OTP code
            user_name: Recipient's name (optional)
            
        Returns:
            True if email sent successfully, False otherwise
        """
        if not self.sender_email or not self.sender_password:
            print(f"[Mock Email] OTP for {recipient_email}: {otp}")
            return True
        
        try:
            subject = "Password Reset OTP"
            body = self._build_otp_email_body(otp, user_name)
            
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = recipient_email
            
            message.attach(MIMEText(body, "html"))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
            
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def send_password_reset_confirmation(self, recipient_email: str, user_name: Optional[str] = None) -> bool:
        """
        Send password reset confirmation email
        
        Args:
            recipient_email: Recipient's email address
            user_name: Recipient's name (optional)
            
        Returns:
            True if email sent successfully, False otherwise
        """
        if not self.sender_email or not self.sender_password:
            print(f"[Mock Email] Password reset confirmation sent to {recipient_email}")
            return True
        
        try:
            subject = "Password Reset Successful"
            body = self._build_reset_confirmation_body(user_name)
            
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = recipient_email
            
            message.attach(MIMEText(body, "html"))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
            
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    @staticmethod
    def _build_otp_email_body(otp: str, user_name: Optional[str] = None) -> str:
        """Build HTML email body for OTP"""
        name = user_name or "User"
        return f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                <div style="background-color: white; border-radius: 8px; padding: 30px; max-width: 500px; margin: 0 auto;">
                    <h2 style="color: #333; text-align: center;">Password Reset OTP</h2>
                    <p style="color: #666; font-size: 16px; line-height: 1.6;">
                        Hi {name},
                    </p>
                    <p style="color: #666; font-size: 16px; line-height: 1.6;">
                        We received a request to reset your password. Here's your One-Time Password (OTP):
                    </p>
                    <div style="text-align: center; margin: 30px 0;">
                        <div style="background-color: #f0f0f0; padding: 20px; border-radius: 8px; font-size: 24px; letter-spacing: 5px; font-weight: bold; color: #333;">
                            {otp}
                        </div>
                    </div>
                    <p style="color: #999; font-size: 14px;">
                        This OTP is valid for 10 minutes.
                    </p>
                    <p style="color: #999; font-size: 14px;">
                        If you didn't request this, please ignore this email.
                    </p>
                    <hr style="border: 1px solid #ddd; margin: 20px 0;">
                    <p style="color: #999; font-size: 12px; text-align: center;">
                        © 2026 COLLAB. All rights reserved.
                    </p>
                </div>
            </body>
        </html>
        """
    
    @staticmethod
    def _build_reset_confirmation_body(user_name: Optional[str] = None) -> str:
        """Build HTML email body for password reset confirmation"""
        name = user_name or "User"
        return f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                <div style="background-color: white; border-radius: 8px; padding: 30px; max-width: 500px; margin: 0 auto;">
                    <h2 style="color: #333; text-align: center;">Password Reset Successful</h2>
                    <p style="color: #666; font-size: 16px; line-height: 1.6;">
                        Hi {name},
                    </p>
                    <p style="color: #666; font-size: 16px; line-height: 1.6;">
                        Your password has been successfully reset. You can now log in with your new password.
                    </p>
                    <p style="color: #999; font-size: 14px;">
                        If you didn't perform this action, please contact our support team immediately.
                    </p>
                    <hr style="border: 1px solid #ddd; margin: 20px 0;">
                    <p style="color: #999; font-size: 12px; text-align: center;">
                        © 2026 COLLAB. All rights reserved.
                    </p>
                </div>
            </body>
        </html>
        """
