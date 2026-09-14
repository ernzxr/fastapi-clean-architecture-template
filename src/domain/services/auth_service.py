from src.domain.entities.user import User
from src.domain.exceptions import InvalidCredentialsError
from src.domain.ports.password_hasher import IPasswordHasher
from src.domain.ports.token_service import ITokenService
from src.domain.ports.user_repository import IUserRepository


class AuthService:
    def __init__(
        self,
        user_repo: IUserRepository,
        password_hasher: IPasswordHasher,
        token_service: ITokenService,
    ) -> None:
        self.user_repo = user_repo
        self.password_hasher = password_hasher
        self.token_service = token_service

    def authenticate(self, email: str, password: str) -> User:
        result = self.user_repo.get_credentials_by_email(email)
        if not result:
            raise InvalidCredentialsError()
        user, stored_hash = result
        if not self.password_hasher.verify(password, stored_hash) or not user.is_active:
            raise InvalidCredentialsError()
        return user

    def login(self, email: str, password: str) -> str:
        user = self.authenticate(email, password)
        return self.token_service.create_access_token(user_id=user.id)