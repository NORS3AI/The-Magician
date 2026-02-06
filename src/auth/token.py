"""Token generation for sessions and password resets."""

import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Tuple


class TokenGenerator:
    """Generates cryptographically secure tokens for various auth purposes."""

    @staticmethod
    def generate_session_token() -> str:
        """
        Generate a secure random session token.

        Returns:
            128-character hexadecimal token
        """
        return secrets.token_hex(64)

    @staticmethod
    def generate_reset_token() -> str:
        """
        Generate a secure password reset token.

        Returns:
            64-character hexadecimal token
        """
        return secrets.token_hex(32)

    @staticmethod
    def hash_token(token: str) -> str:
        """
        Hash a token for secure storage.

        Args:
            token: The raw token to hash

        Returns:
            SHA-256 hash of the token
        """
        return hashlib.sha256(token.encode('utf-8')).hexdigest()


class TokenManager:
    """Manages token lifecycle including expiration."""

    def __init__(self, expiry_hours: int = 24):
        """
        Initialize token manager.

        Args:
            expiry_hours: Hours until token expires
        """
        self.expiry_hours = expiry_hours

    def create_token_record(self, token: str, user_id: str) -> dict:
        """
        Create a token record for storage.

        Args:
            token: The raw token (will be hashed before storage)
            user_id: User ID this token belongs to

        Returns:
            Token record dict with hashed token, user_id, and expiry
        """
        token_hash = TokenGenerator.hash_token(token)
        expires_at = datetime.utcnow() + timedelta(hours=self.expiry_hours)

        return {
            'token_hash': token_hash,
            'user_id': user_id,
            'created_at': datetime.utcnow().isoformat(),
            'expires_at': expires_at.isoformat(),
            'used': False
        }

    def is_token_valid(self, token_record: dict) -> Tuple[bool, str]:
        """
        Check if a token record is valid.

        Args:
            token_record: The token record to validate

        Returns:
            Tuple of (is_valid, reason)
        """
        if token_record.get('used'):
            return False, "Token has already been used"

        expires_at = datetime.fromisoformat(token_record['expires_at'])
        if datetime.utcnow() > expires_at:
            return False, "Token has expired"

        return True, ""

    def verify_token(self, raw_token: str, token_record: dict) -> bool:
        """
        Verify a raw token against its stored record.

        Args:
            raw_token: The raw token to verify
            token_record: The stored token record

        Returns:
            True if token matches and is valid
        """
        # Check if token matches
        token_hash = TokenGenerator.hash_token(raw_token)
        if token_hash != token_record['token_hash']:
            return False

        # Check if token is still valid
        is_valid, _ = self.is_token_valid(token_record)
        return is_valid

    def mark_token_used(self, token_record: dict) -> dict:
        """
        Mark a token as used.

        Args:
            token_record: The token record to mark

        Returns:
            Updated token record
        """
        token_record['used'] = True
        token_record['used_at'] = datetime.utcnow().isoformat()
        return token_record
