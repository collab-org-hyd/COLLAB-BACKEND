import re
from app.presentation.schemas.auth_schema import ValidateEmailResponse

# Email validation pattern
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'


def is_valid_email(email: str) -> bool:
    """Validate email format using regex"""
    return bool(re.match(EMAIL_PATTERN, email))


def create_email_response(status: bool, message: str, email: str = None) -> ValidateEmailResponse:
    """Create email validation response"""
    return ValidateEmailResponse(
        status=status,
        message=message,
        data={"emailId": email} if email else None,
    )