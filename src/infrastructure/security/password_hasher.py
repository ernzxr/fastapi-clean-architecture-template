from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher

from src.domain.ports.password_hasher import IPasswordHasher


class PwdlibPasswordHasher(IPasswordHasher):
    def __init__(self) -> None:
        self._hasher = PasswordHash((Argon2Hasher(), BcryptHasher()))

    def hash(self, plain_password: str) -> str:
        return self._hasher.hash(plain_password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return self._hasher.verify(plain_password, hashed_password)