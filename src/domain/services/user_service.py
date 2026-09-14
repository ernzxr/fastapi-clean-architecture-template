from typing import Any, Dict, List, Optional, Set

from src.domain.entities.user import User
from src.domain.ports.password_hasher import IPasswordHasher
from src.domain.ports.user_repository import IUserRepository


class UserService:
    def __init__(self, user_repo: IUserRepository, password_hasher: IPasswordHasher) -> None:  # noqa: E501
        self.user_repo = user_repo
        self.password_hasher = password_hasher

    def _apply_field_updates(
        self, 
        user_id: int, 
        update_data: Dict[str, Any], 
        allowed_fields: Set[str]
    ) -> Optional[User]:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return None

        for key, value in update_data.items():
            if key in allowed_fields and hasattr(user, key):
                setattr(user, key, value)

        return self.user_repo.update(user)

    def create_user(self, email: str, username: str, password: str) -> User:
        if self.user_repo.get_by_email(email):
            raise ValueError(f"User with email '{email}' already exists.")
        hashed_pw = self.password_hasher.hash(password)
        new_user = User(id=None, email=email, username=username)
        return self.user_repo.create(new_user, hashed_pw)

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.user_repo.get_by_id(user_id)

    def list_users(self) -> List[User]:
        return self.user_repo.list_all()

    def hard_delete_user(self, user_id: int) -> bool:
        return self.user_repo.delete(user_id)

    def update_user(
        self,
        user_id: int,
        email: Optional[str] = None,
        username: Optional[str] = None,
    ) -> Optional[User]:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return None

        if email is not None:
            user.email = email
        if username is not None:
            user.username = username

        return self.user_repo.update(user)

    def update_user_fields(
        self, 
        user_id: int, 
        update_data: Dict[str, Any]
    ) -> Optional[User]:
        return self._apply_field_updates(
            user_id, 
            update_data, 
            allowed_fields={"email", "username"}
        )

    def update_user_fields_admin(
        self, 
        user_id: int, 
        update_data: Dict[str, Any]
    ) -> Optional[User]:
        return self._apply_field_updates(
            user_id, 
            update_data, 
            allowed_fields={"email", "username", "is_active"}
        )

    def soft_delete_user(self, user_id: int) -> bool:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return False
        user.is_active = False
        self.user_repo.update(user)
        return True

    def get_user_by_username(self, username: str) -> User | None:
        return self.user_repo.get_by_username(username)