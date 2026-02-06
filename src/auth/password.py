"""Password hashing and validation using bcrypt."""

import bcrypt
import re
from typing import Tuple


class PasswordValidator:
    """Validates password requirements."""

    MIN_LENGTH = 8
    MAX_LENGTH = 128
    ALLOWED_CHARS = re.compile(r'^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{}|;:,.<>?]+$')

    @classmethod
    def validate(cls, password: str) -> Tuple[bool, str]:
        """
        Validate password against requirements.

        Args:
            password: The password to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not password:
            return False, "Password is required"

        if len(password) < cls.MIN_LENGTH:
            return False, f"Password must be at least {cls.MIN_LENGTH} characters"

        if len(password) > cls.MAX_LENGTH:
            return False, f"Password must not exceed {cls.MAX_LENGTH} characters"

        if not cls.ALLOWED_CHARS.match(password):
            return False, "Password contains invalid characters (only a-z, A-Z, 0-9, and common symbols allowed)"

        return True, ""


class PasswordHasher:
    """Handles password hashing with bcrypt."""

    def __init__(self, rounds: int = 12):
        """
        Initialize hasher with bcrypt cost factor.

        Args:
            rounds: Number of hashing rounds (cost factor), default 12
        """
        self.rounds = rounds

    def hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt.

        Args:
            password: Plain text password

        Returns:
            Hashed password as string
        """
        # bcrypt requires bytes
        password_bytes = password.encode('utf-8')

        # Generate salt and hash
        salt = bcrypt.gensalt(rounds=self.rounds)
        hashed = bcrypt.hashpw(password_bytes, salt)

        # Return as string for storage
        return hashed.decode('utf-8')

    def verify_password(self, password: str, hashed: str) -> bool:
        """
        Verify a password against its hash.

        Args:
            password: Plain text password to verify
            hashed: Stored hashed password

        Returns:
            True if password matches, False otherwise
        """
        try:
            password_bytes = password.encode('utf-8')
            hashed_bytes = hashed.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        except Exception:
            return False
