from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.settings import settings
from app.utils.validators import is_valid_email, create_email_response
from app.presentation.schemas.auth_schema import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
    ValidateEmailRequest,
    ValidateEmailResponse,
    ForgotPasswordRequestOTPRequest,
    ForgotPasswordRequestOTPResponse,
    VerifyOTPRequest,
    VerifyOTPResponse,
    ResetPasswordRequest,
    ResetPasswordResponse,
    ResetPasswordDirectRequest,
    ResetPasswordDirectResponse,
)
from app.application.use_cases.user.login_user import LoginUseCase, CreateUserUseCase
from app.application.use_cases.user.forgot_password import (
    ForgotPasswordRequestOTPUseCase,
    VerifyOTPUseCase,
    ResetPasswordUseCase,
    ResetPasswordDirectUseCase,
)
from app.infrastructure.database.repositories.user_repository_impl import (
    UserRepositoryImpl,
    AuthCredentialsRepositoryImpl,
)
from app.infrastructure.external_services.email_service import EmailService
from app.core.exceptions import ResourceNotFoundError, BadRequestError, AuthenticationError

router = APIRouter(prefix="/auth", tags=["auth"])


async def get_login_use_case(db: Session = Depends(get_db)) -> LoginUseCase:
    """Dependency to get login use case"""
    user_repo = UserRepositoryImpl(db)
    auth_repo = AuthCredentialsRepositoryImpl(db)
    return LoginUseCase(user_repo, auth_repo)


async def get_create_user_use_case(db: Session = Depends(get_db)) -> CreateUserUseCase:
    """Dependency to get create user use case"""
    user_repo = UserRepositoryImpl(db)
    auth_repo = AuthCredentialsRepositoryImpl(db)
    return CreateUserUseCase(user_repo, auth_repo)


async def get_forgot_password_otp_use_case(db: Session = Depends(get_db)) -> ForgotPasswordRequestOTPUseCase:
    """Dependency to get forgot password OTP use case"""
    user_repo = UserRepositoryImpl(db)
    email_service = EmailService(
        smtp_server=settings.smtp_server,
        smtp_port=settings.smtp_port,
        sender_email=settings.sender_email,
        sender_password=settings.sender_password,
        sender_name=settings.sender_name
    )
    return ForgotPasswordRequestOTPUseCase(user_repo, email_service)


async def get_verify_otp_use_case(db: Session = Depends(get_db)) -> VerifyOTPUseCase:
    """Dependency to get verify OTP use case"""
    user_repo = UserRepositoryImpl(db)
    return VerifyOTPUseCase(user_repo)


async def get_reset_password_use_case(db: Session = Depends(get_db)) -> ResetPasswordUseCase:
    """Dependency to get reset password use case"""
    user_repo = UserRepositoryImpl(db)
    email_service = EmailService(
        smtp_server=settings.smtp_server,
        smtp_port=settings.smtp_port,
        sender_email=settings.sender_email,
        sender_password=settings.sender_password,
        sender_name=settings.sender_name
    )
    return ResetPasswordUseCase(user_repo, email_service)


async def get_reset_password_direct_use_case(db: Session = Depends(get_db)) -> ResetPasswordDirectUseCase:
    """Dependency to get reset password direct use case (without OTP)"""
    user_repo = UserRepositoryImpl(db)
    auth_repo = AuthCredentialsRepositoryImpl(db)
    email_service = EmailService(
        smtp_server=settings.smtp_server,
        smtp_port=settings.smtp_port,
        sender_email=settings.sender_email,
        sender_password=settings.sender_password,
        sender_name=settings.sender_name
    )
    return ResetPasswordDirectUseCase(user_repo, auth_repo, email_service)


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(
    request: LoginRequest,
    use_case: LoginUseCase = Depends(get_login_use_case),
):
    """
    User login endpoint
    
    - **email**: User email
    - **password**: User password
    """
    try:
        result = await use_case.execute(request.email, request.password)
        return LoginResponse(**result)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case),
):
    """
    User registration endpoint
    
    - **username**: Unique username
    - **email**: User email
    - **password**: User password (min 6 chars)
    - **display_name**: Optional display name
    - **role**: User role (customer, influencer, admin)
    """
    try:
        result = await use_case.execute(
            username=request.username,
            email=request.email,
            password=request.password,
            display_name=request.display_name,
            role=request.role,
        )
        return RegisterResponse(**result)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/validate-email", response_model=ValidateEmailResponse, status_code=status.HTTP_200_OK)
async def validate_email(
    email: str,
    db: Session = Depends(get_db),
):
    """
    Validate if email exists in database
    
    - **email**: Email to validate (query parameter)
    """
    # Validate email format
    if not is_valid_email(email):
        return create_email_response(False, "Invalid email format")
    
    # Check if email exists in database
    user_repo = UserRepositoryImpl(db)
    user = await user_repo.get_by_email(email)
    
    email_exists = user is not None
    email = user.email if email_exists else None
    message = "Email exists" if email_exists else "Email does not exist"
    
    return create_email_response(email_exists, message, email)


@router.post("/forgot-password/request-otp", response_model=ForgotPasswordRequestOTPResponse, status_code=status.HTTP_200_OK)
async def request_forgot_password_otp(
    request: ForgotPasswordRequestOTPRequest,
    use_case: ForgotPasswordRequestOTPUseCase = Depends(get_forgot_password_otp_use_case),
):
    """
    Request OTP for password reset via email
    
    - **email**: User email
    """
    try:
        result = await use_case.execute(email=request.email)
        return ForgotPasswordRequestOTPResponse(
            success=result.get("success"),
            message=result.get("message"),
            identifier=result.get("identifier")
        )
    except ResourceNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except BadRequestError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/forgot-password/verify-otp", response_model=VerifyOTPResponse, status_code=status.HTTP_200_OK)
async def verify_forgot_password_otp(
    request: VerifyOTPRequest,
    use_case: VerifyOTPUseCase = Depends(get_verify_otp_use_case),
):
    """
    Verify OTP for password reset
    
    - **email**: User email
    - **otp**: 6-digit OTP code
    """
    try:
        result = await use_case.execute(request.email, request.otp)
        return VerifyOTPResponse(
            success=result.get("success"),
            message=result.get("message"),
            token=result.get("reset_token")
        )
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.post("/forgot-password/reset", response_model=ResetPasswordResponse, status_code=status.HTTP_200_OK)
async def reset_password(
    request: ResetPasswordRequest,
    use_case: ResetPasswordUseCase = Depends(get_reset_password_use_case),
):
    """
    Reset password after OTP verification
    
    - **email**: User email
    - **new_password**: New password (min 6 characters)
    - **reset_token**: Token from OTP verification
    """
    try:
        result = await use_case.execute(
            email=request.email,
            new_password=request.new_password,
            reset_token=request.reset_token
        )
        return ResetPasswordResponse(
            success=result.get("success"),
            message=result.get("message"),
            user_id=result.get("user_id")
        )
    except (AuthenticationError, ResourceNotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
    except BadRequestError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/forgot-password/reset-direct", response_model=ResetPasswordDirectResponse, status_code=status.HTTP_200_OK)
async def reset_password_direct(
    request: ResetPasswordDirectRequest,
    use_case: ResetPasswordDirectUseCase = Depends(get_reset_password_direct_use_case),
):
    """
    ⚠️  DEPRECATED: Reset password without OTP or current password verification (DEBUG MODE ONLY)
    
    This endpoint is for debugging/testing only when email service is broken.
    It bypasses all security checks and should NEVER be used in production.
    
    - **email**: User email
    - **new_password**: New password (min 6 characters)
    """
    try:
        result = await use_case.execute(
            email=request.email,
            new_password=request.new_password
        )
        return ResetPasswordDirectResponse(
            success=result.get("success"),
            message=result.get("message"),
            user_id=result.get("user_id")
        )
    except (AuthenticationError, ResourceNotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
    except BadRequestError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
