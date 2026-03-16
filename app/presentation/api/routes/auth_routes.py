from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.utils.validators import is_valid_email, create_email_response
from app.presentation.schemas.auth_schema import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
    ValidateEmailRequest,
    ValidateEmailResponse,
)
from app.application.use_cases.user.login_user import LoginUseCase, CreateUserUseCase
from app.infrastructure.database.repositories.user_repository_impl import (
    UserRepositoryImpl,
    AuthCredentialsRepositoryImpl,
)

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
