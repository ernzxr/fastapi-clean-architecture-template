from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.domain.entities.user import User
from src.domain.exceptions import InvalidTokenError
from src.domain.ports.password_hasher import IPasswordHasher
from src.domain.ports.token_service import ITokenService
from src.domain.ports.user_repository import IUserRepository
from src.domain.services.auth_service import AuthService
from src.domain.services.user_service import UserService
from src.infrastructure.config import settings
from src.infrastructure.db.session import get_db
from src.infrastructure.repositories.user_sqlalchemy_repository import (
    SqlAlchemyUserRepository,
)
from src.infrastructure.security.jwt_service import JWTTokenService
from src.infrastructure.security.password_hasher import PwdlibPasswordHasher

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# --- Infrastructure bindings (only place concrete classes are chosen) -------
def get_user_repository(db: Session = Depends(get_db)) -> IUserRepository:
    return SqlAlchemyUserRepository(db)


def get_password_hasher() -> IPasswordHasher:
    return PwdlibPasswordHasher()


def get_token_service() -> ITokenService:
    return JWTTokenService(secret_key=settings.SECRET_KEY,
                           algorithm=settings.ALGORITHM,
                           expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
)


# --- Application services ----------------------------------------------------
def get_user_service(
    repo: IUserRepository = Depends(get_user_repository),
    hasher: IPasswordHasher = Depends(get_password_hasher),
) -> UserService:
    return UserService(repo, hasher)


def get_auth_service(
    repo: IUserRepository = Depends(get_user_repository),
    hasher: IPasswordHasher = Depends(get_password_hasher),
    tokens: ITokenService = Depends(get_token_service),
) -> AuthService:
    return AuthService(repo, hasher, tokens)


# --- Current-user resolution --------------------------------------------------
def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: UserService = Depends(get_user_service),
    tokens: ITokenService = Depends(get_token_service),
) -> User:
    try:
        user_id = tokens.decode_access_token(token)
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")  # noqa: E501

    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")  # noqa: E501
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return current_user


def get_current_admin_user(current_user: User = Depends(get_current_active_user)) -> User:  # noqa: E501
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")  # noqa: E501
    return current_user