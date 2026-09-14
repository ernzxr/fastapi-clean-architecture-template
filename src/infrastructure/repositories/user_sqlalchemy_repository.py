from typing import List, Optional

from sqlalchemy.orm import Session

from src.domain.entities.user import User
from src.domain.ports.user_repository import IUserRepository
from src.infrastructure.db.models.user_model import UserModel


class SqlAlchemyUserRepository(IUserRepository):

    def __init__(self, db: Session) -> None:
        self.db = db

    def _to_entity(self, db_user: UserModel) -> User:
        return User(
            id=db_user.id,
            email=db_user.email,
            username=db_user.username,
            is_active=db_user.is_active,
            is_admin=db_user.is_admin,
            created_at=db_user.created_at,
        )

    def create(self, user: User, hashed_password: str) -> User:
        db_user = UserModel(
            email=user.email,
            username=user.username,
            hashed_password=hashed_password,
            is_active=user.is_active,
            is_admin=user.is_admin,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return self._to_entity(db_user)

    def update(self, user: User) -> User:
        db_user = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        if not db_user:
            raise ValueError(f"User {user.id} not found")
        db_user.email = user.email
        db_user.username = user.username
        db_user.is_active = user.is_active
        db_user.is_admin = user.is_admin
        self.db.commit()
        self.db.refresh(db_user)
        return self._to_entity(db_user)

    def get_credentials_by_email(self, email: str) -> Optional[tuple[User, str]]:
        db_user = self.db.query(UserModel).filter(UserModel.email == email).first()
        if not db_user:
            return None
        return self._to_entity(db_user), db_user.hashed_password

    def get_by_id(self, user_id: int) -> Optional[User]:
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return self._to_entity(db_user) if db_user else None

    def get_by_email(self, email: str) -> Optional[User]:
        db_user = self.db.query(UserModel).filter(UserModel.email == email).first()
        return self._to_entity(db_user) if db_user else None

    def get_by_username(self, username: str) -> Optional[User]:
        db_user = self.db.query(UserModel).filter(UserModel.username == username).first()
        return self._to_entity(db_user) if db_user else None

    def list_all(self) -> List[User]:
        users = self.db.query(UserModel).all()
        return [self._to_entity(u) for u in users]

    def delete(self, user_id: int) -> bool:
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not db_user:
            return False
        self.db.delete(db_user)
        self.db.commit()
        return True