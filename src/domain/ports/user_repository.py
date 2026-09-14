from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.user import User


class IUserRepository(ABC):

    @abstractmethod
    def create(self, user: User, hashed_password: str) -> User:
        """Create a new user. Hash is required — there's no valid create without one."""

    @abstractmethod
    def update(self, user: User) -> User:
        """Update an existing user's profile fields. Never touches credentials."""

    @abstractmethod
    def get_credentials_by_email(self, email: str) -> Optional[tuple[User, str]]:
        """For login only: returns (User, hashed_password)."""

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Fetch a single user by primary ID."""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Fetch a user by unique email address."""
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        """Fetch a user by unique username."""
        pass

    @abstractmethod
    def list_all(self) -> List[User]:
        """Retrieve all users."""
        pass

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """Hard delete only"""
        pass