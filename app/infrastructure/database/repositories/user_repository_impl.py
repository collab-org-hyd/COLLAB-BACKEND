from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.domain.entities.user import User, AuthCredentials, UserRole
from app.domain.repositories.user_repository import UserRepository, AuthCredentialsRepository
from app.infrastructure.database.models.user_model import UserModel, AuthCredentialsModel


class UserRepositoryImpl(UserRepository):
    """Implementation of UserRepository with SQLAlchemy"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID"""
        user_model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return self._model_to_entity(user_model) if user_model else None
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        user_model = self.db.query(UserModel).filter(UserModel.email == email).first()
        return self._model_to_entity(user_model) if user_model else None
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        user_model = self.db.query(UserModel).filter(UserModel.username == username).first()
        return self._model_to_entity(user_model) if user_model else None
    
    async def create(self, user: User) -> User:
        """Create a new user"""
        user_model = UserModel(
            id=user.id,
            username=user.username,
            email=user.email,
            display_name=user.display_name,
            role=user.role,
            is_influencer=user.is_influencer,
            tags=user.tags,  # Store as JSON array
            can_request_service=user.can_request_service,
            can_fulfill_service=user.can_fulfill_service,
            bio=user.bio,
            business_link=user.business_link,
            yt_link=user.yt_link,
            x_link=user.x_link,
            facebook_link=user.facebook_link,
            other_link=user.other_link,
            what_to_expect=user.what_to_expect,
            created_at=user.created_at,
        )
        self.db.add(user_model)
        self.db.commit()
        self.db.refresh(user_model)
        return self._model_to_entity(user_model)
    
    async def update(self, user: User) -> User:
        """Update user"""
        user_model = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        if not user_model:
            raise ValueError(f"User with id {user.id} not found")
        
        user_model.username = user.username
        user_model.email = user.email
        user_model.display_name = user.display_name
        user_model.role = user.role
        user_model.is_influencer = user.is_influencer
        user_model.tags = user.tags  # Store as JSON array
        user_model.can_request_service = user.can_request_service
        user_model.can_fulfill_service = user.can_fulfill_service
        user_model.bio = user.bio
        user_model.business_link = user.business_link
        user_model.yt_link = user.yt_link
        user_model.x_link = user.x_link
        user_model.facebook_link = user.facebook_link
        user_model.other_link = user.other_link
        user_model.what_to_expect = user.what_to_expect
        
        self.db.commit()
        self.db.refresh(user_model)
        return self._model_to_entity(user_model)
    
    async def delete(self, user_id: UUID) -> bool:
        """Delete user"""
        user_model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user_model:
            return False
        
        self.db.delete(user_model)
        self.db.commit()
        return True
    
    @staticmethod
    def _model_to_entity(user_model: UserModel) -> User:
        """Convert UserModel to User entity"""
        return User(
            id=user_model.id,
            username=user_model.username,
            email=user_model.email,
            display_name=user_model.display_name,
            role=UserRole(user_model.role.value),
            is_influencer=user_model.is_influencer,
            tags=user_model.tags or [],  # Already a list from JSON
            can_request_service=user_model.can_request_service,
            can_fulfill_service=user_model.can_fulfill_service,
            bio=user_model.bio,
            business_link=user_model.business_link,
            yt_link=user_model.yt_link,
            x_link=user_model.x_link,
            facebook_link=user_model.facebook_link,
            other_link=user_model.other_link,
            what_to_expect=user_model.what_to_expect,
            created_at=user_model.created_at,
        )


class AuthCredentialsRepositoryImpl(AuthCredentialsRepository):
    """Implementation of AuthCredentialsRepository with SQLAlchemy"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def get_by_user_id(self, user_id: UUID) -> Optional[AuthCredentials]:
        """Get credentials by user ID"""
        creds_model = self.db.query(AuthCredentialsModel).filter(
            AuthCredentialsModel.user_id == user_id
        ).first()
        return self._model_to_entity(creds_model) if creds_model else None
    
    async def create(self, credentials: AuthCredentials) -> AuthCredentials:
        """Create authentication credentials"""
        creds_model = AuthCredentialsModel(
            id=credentials.id,
            user_id=credentials.user_id,
            password_hash=credentials.password_hash,
            created_at=credentials.created_at,
        )
        self.db.add(creds_model)
        self.db.commit()
        self.db.refresh(creds_model)
        return self._model_to_entity(creds_model)
    
    async def update(self, credentials: AuthCredentials) -> AuthCredentials:
        """Update credentials"""
        creds_model = self.db.query(AuthCredentialsModel).filter(
            AuthCredentialsModel.user_id == credentials.user_id
        ).first()
        if not creds_model:
            raise ValueError(f"Credentials for user {credentials.user_id} not found")
        
        creds_model.password_hash = credentials.password_hash
        self.db.commit()
        self.db.refresh(creds_model)
        return self._model_to_entity(creds_model)
    
    async def delete(self, user_id: UUID) -> bool:
        """Delete credentials by user ID"""
        creds_model = self.db.query(AuthCredentialsModel).filter(
            AuthCredentialsModel.user_id == user_id
        ).first()
        if not creds_model:
            return False
        
        self.db.delete(creds_model)
        self.db.commit()
        return True
    
    @staticmethod
    def _model_to_entity(creds_model: AuthCredentialsModel) -> AuthCredentials:
        """Convert AuthCredentialsModel to AuthCredentials entity"""
        return AuthCredentials(
            id=creds_model.id,
            user_id=creds_model.user_id,
            password_hash=creds_model.password_hash,
            created_at=creds_model.created_at,
        )
