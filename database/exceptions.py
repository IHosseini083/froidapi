class DatabaseError(Exception):
    """Base exception class for all the database errors."""

    def __init__(self, message: str, *args) -> None:
        super().__init__(message, *args)


class UserNotFoundError(DatabaseError):
    """Raised when a user is not found."""


class AuthenticationError(DatabaseError):
    """Raised when user authentication fails."""


class OldCredentialsError(DatabaseError):
    """Raised when old credentials are used."""
    
    
class TokenNotFoundError(DatabaseError):
    """Raised when a token is not found."""
    