from datetime import datetime, timedelta, timezone

import jwt

from src.domain.exceptions import InvalidTokenError
from src.domain.ports.token_service import ITokenService


class JWTTokenService(ITokenService):
    def __init__(self, secret_key: str, algorithm: str = "HS256", expire_minutes: int = 30) -> None:
        self._secret = secret_key
        self._algorithm = algorithm
        self._expire_minutes = expire_minutes

    def create_access_token(self, user_id: int) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=self._expire_minutes)
        payload = {"sub": str(user_id), "exp": expire}
        return jwt.encode(payload, self._secret, algorithm=self._algorithm)

    def decode_access_token(self, token: str) -> int:
        try:
            payload = jwt.decode(token, self._secret, algorithms=[self._algorithm])
            return int(payload["sub"])
        except jwt.PyJWTError:
            raise InvalidTokenError()