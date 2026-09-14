from abc import ABC, abstractmethod


class ITokenService(ABC):
    @abstractmethod
    def create_access_token(self, user_id: int) -> str: ...

    @abstractmethod
    def decode_access_token(self, token: str) -> int:
        """Returns user_id. Raises InvalidTokenError if invalid/expired."""