class DomainError(Exception):
    """Base class for domain-level errors."""


class InvalidCredentialsError(DomainError):
    """Raised when email/password don't match or account is inactive."""


class InvalidTokenError(DomainError):
    """Raised when a token is malformed, expired, or has an invalid signature."""