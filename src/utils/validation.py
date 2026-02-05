"""Input validation utilities for usernames, emails, and other fields."""

import re
from typing import Tuple


class UsernameValidator:
    """Validates username requirements."""

    MIN_LENGTH = 3
    MAX_LENGTH = 20
    ALLOWED_CHARS = re.compile(r'^[a-zA-Z0-9_]+$')

    @classmethod
    def validate(cls, username: str) -> Tuple[bool, str]:
        """
        Validate username against requirements.

        Args:
            username: The username to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not username:
            return False, "Username is required"

        if len(username) < cls.MIN_LENGTH:
            return False, f"Username must be at least {cls.MIN_LENGTH} characters"

        if len(username) > cls.MAX_LENGTH:
            return False, f"Username must not exceed {cls.MAX_LENGTH} characters"

        if not cls.ALLOWED_CHARS.match(username):
            return False, "Username can only contain letters, numbers, and underscores"

        return True, ""


class EmailValidator:
    """Validates email format."""

    # Simple but effective email regex
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

    @classmethod
    def validate(cls, email: str) -> Tuple[bool, str]:
        """
        Validate email format.

        Args:
            email: The email to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not email:
            return False, "Email is required"

        if not cls.EMAIL_REGEX.match(email):
            return False, "Invalid email format"

        if len(email) > 254:  # RFC 5321
            return False, "Email address is too long"

        return True, ""
