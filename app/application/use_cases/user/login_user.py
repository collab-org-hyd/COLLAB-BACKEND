from uuid import uuid4
from app.domain.entities.user import User, AuthCredentials, UserRole
from app.domain.repositories.user_repository import UserRepository, AuthCredentialsRepository
from app.core.security import hash_password, verify_password


class LoginUseCase:
    """Use case for user login"""
    
    def __init__(
        self,
        user_repository: UserRepository,
        auth_repository: AuthCredentialsRepository,
    ):
        self.user_repository = user_repository
        self.auth_repository = auth_repository
    
    async def execute(self, email: str, password: str) -> dict:
        """
        Execute login use case
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Dictionary with user info and success status
            
        Raises:
            ValueError: If credentials are invalid
        """
        # Find user by email
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise ValueError("Invalid email or password")
        
        # Get credentials
        credentials = await self.auth_repository.get_by_user_id(user.id)
        if not credentials:
            raise ValueError("Invalid email or password")
        
        # Verify password
        if not verify_password(password, credentials.password_hash):
            raise ValueError("Invalid email or password")
        
        return {
            "success": True,
            "user_id": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role.value,
            "message": "Login successful",
        }


class CreateUserUseCase:
    """Use case for user registration"""
    
    def __init__(
        self,
        user_repository: UserRepository,
        auth_repository: AuthCredentialsRepository,
    ):
        self.user_repository = user_repository
        self.auth_repository = auth_repository
    
    async def execute(
        self,
        username: str,
        email: str,
        password: str,
        display_name: str = None,
        role: str = "customer",
    ) -> dict:
        """
        Execute user creation use case
        
        Args:
            username: User username
            email: User email
            password: User password
            display_name: Display name
            role: User role
            
        Returns:
            Dictionary with created user info
            
        Raises:
            ValueError: If user already exists
        """
        # Check if user already exists
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user:
            raise ValueError("Email already registered")
        
        existing_user = await self.user_repository.get_by_username(username)
        if existing_user:
            raise ValueError("Username already taken")
        
        # Create user
        user_id = uuid4()
        user = User(
            id=user_id,
            username=username,
            email=email,
            display_name=display_name or username,
            role=UserRole(role),
        )
        
        created_user = await self.user_repository.create(user)
        
        # Create credentials
        password_hash = hash_password(password)
        credentials = AuthCredentials(
            id=uuid4(),
            user_id=user_id,
            password_hash=password_hash,
        )
        
        await self.auth_repository.create(credentials)
        
        return {
            "success": True,
            "user_id": str(created_user.id),
            "username": created_user.username,
            "email": created_user.email,
            "message": "User created successfully",
        }
