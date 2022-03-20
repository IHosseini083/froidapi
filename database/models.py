from datetime import datetime as dt
from hashlib import sha256
from secrets import token_urlsafe
from typing import Any, Dict, Optional

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from .db import Base


class User(Base):
    """Model for registered users in the database."""
    __tablename__ = "users"

    id: int = sa.Column(sa.Integer, primary_key=True, index=True)
    """Unique identifier for the user in the database."""
    username: str = sa.Column(sa.String, unique=True, nullable=False)
    """Username of the user."""
    email: str = sa.Column(sa.String, unique=True, nullable=False)
    """Unique email address of the user."""
    hashed_password: str = sa.Column(sa.String, nullable=False)
    """Hashed password of the user."""
    created_at: dt = sa.Column(sa.DateTime, default=dt.now())
    """Creation datetime of the user."""
    token: Optional["Token"] = relationship("Token", uselist=False, back_populates="user")
    """User's token (if any)."""

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({", ".join(map(lambda k, v: f"{k}={v!r}", self.json().items()))})'

    def json(self) -> Dict[str, Any]:
        """Return a JSON representation of the user."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "token": self.token.json() if self.token else None
        }


class Token(Base):
    """Model for users' token in the database."""
    __tablename__ = "tokens"

    id: int = sa.Column(sa.Integer, primary_key=True, index=True)
    """Unique identifier for the token in the database."""
    token: str = sa.Column(sa.String, unique=True, nullable=False)
    """Unique token for the user."""
    user_id: int = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False)
    """Unique identifier for the user."""
    user: "User" = relationship("User", back_populates="token")
    """User that owns the token."""
    created_at: dt = sa.Column(sa.DateTime, default=dt.now())
    """Creation datetime of the token."""

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({", ".join(map(lambda k, v: f"{k}={v!r}", self.json().items()))})'

    def json(self) -> Dict[str, Any]:
        """Return a JSON representation of the token."""
        return {
            "id": self.id,
            "token": self.token,
            "user_id": self.user_id,
            "user": self.user.json() if self.user else None,
            "created_at": self.created_at.isoformat()
        }

    @staticmethod
    def generate_token_string() -> str:
        """Generate a random 32-character token string."""
        token = token_urlsafe(32).encode()
        return sha256(token).hexdigest()[:32]
