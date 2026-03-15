from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from app.domain.entities.user import User, AuthCredentials


class UserRepository(ABC):
    """Interface for user repository"""
    
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID"""
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        pass
    
    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        pass
    
    @abstractmethod
    async def create(self, user: User) -> User:
        """Create a new user"""
        pass
    
    @abstractmethod
    async def update(self, user: User) -> User:
        """Update user"""
        pass
    
    @abstractmethod
    async def delete(self, user_id: UUID) -> bool:
        """Delete user"""
        pass


class AuthCredentialsRepository(ABC):
    """Interface for authentication credentials repository"""
    
    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> Optional[AuthCredentials]:
        """Get credentials by user ID"""
        pass
    
    @abstractmethod
    async def create(self, credentials: AuthCredentials) -> AuthCredentials:
        """Create authentication credentials"""
        pass
    
    @abstractmethod
    async def update(self, credentials: AuthCredentials) -> AuthCredentials:
        """Update credentials"""
        pass
    
    @abstractmethod
    async def delete(self, user_id: UUID) -> bool:
        """Delete credentials by user ID"""
        pass
