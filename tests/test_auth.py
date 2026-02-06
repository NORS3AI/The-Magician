"""Unit tests for authentication system."""

import pytest
import tempfile
import shutil
from pathlib import Path

from src.auth import (
    AccountManager,
    PasswordHasher,
    PasswordValidator,
    TokenGenerator,
    TokenManager,
    UserStorage,
    EmailService
)
from src.utils.validation import UsernameValidator, EmailValidator


class TestPasswordValidator:
    """Test password validation."""

    def test_valid_password(self):
        valid, error = PasswordValidator.validate("MyPassword123!")
        assert valid is True
        assert error == ""

    def test_too_short(self):
        valid, error = PasswordValidator.validate("short")
        assert valid is False
        assert "at least 8" in error

    def test_invalid_characters(self):
        valid, error = PasswordValidator.validate("password日本語")
        assert valid is False
        assert "invalid characters" in error.lower()

    def test_empty_password(self):
        valid, error = PasswordValidator.validate("")
        assert valid is False
        assert "required" in error.lower()


class TestPasswordHasher:
    """Test password hashing."""

    def test_hash_password(self):
        hasher = PasswordHasher()
        password = "TestPassword123"
        hashed = hasher.hash_password(password)

        assert hashed != password
        assert len(hashed) > 0

    def test_verify_correct_password(self):
        hasher = PasswordHasher()
        password = "TestPassword123"
        hashed = hasher.hash_password(password)

        assert hasher.verify_password(password, hashed) is True

    def test_verify_incorrect_password(self):
        hasher = PasswordHasher()
        password = "TestPassword123"
        hashed = hasher.hash_password(password)

        assert hasher.verify_password("WrongPassword", hashed) is False


class TestTokenGenerator:
    """Test token generation."""

    def test_generate_session_token(self):
        token1 = TokenGenerator.generate_session_token()
        token2 = TokenGenerator.generate_session_token()

        assert len(token1) == 128  # 64 bytes * 2 hex chars
        assert len(token2) == 128
        assert token1 != token2  # Should be unique

    def test_generate_reset_token(self):
        token1 = TokenGenerator.generate_reset_token()
        token2 = TokenGenerator.generate_reset_token()

        assert len(token1) == 64  # 32 bytes * 2 hex chars
        assert len(token2) == 64
        assert token1 != token2

    def test_hash_token(self):
        token = "test_token_12345"
        hashed1 = TokenGenerator.hash_token(token)
        hashed2 = TokenGenerator.hash_token(token)

        assert hashed1 == hashed2  # Same input = same hash
        assert len(hashed1) == 64  # SHA-256 produces 64 hex chars


class TestTokenManager:
    """Test token management."""

    def test_create_token_record(self):
        manager = TokenManager(expiry_hours=24)
        token = "test_token"
        user_id = "testuser"

        record = manager.create_token_record(token, user_id)

        assert record['user_id'] == user_id
        assert record['used'] is False
        assert 'token_hash' in record
        assert 'created_at' in record
        assert 'expires_at' in record

    def test_token_validation(self):
        manager = TokenManager(expiry_hours=24)
        token = "test_token"
        record = manager.create_token_record(token, "testuser")

        is_valid, reason = manager.is_token_valid(record)
        assert is_valid is True
        assert reason == ""

    def test_mark_token_used(self):
        manager = TokenManager()
        token = "test_token"
        record = manager.create_token_record(token, "testuser")

        updated = manager.mark_token_used(record)

        assert updated['used'] is True
        assert 'used_at' in updated


class TestUsernameValidator:
    """Test username validation."""

    def test_valid_username(self):
        valid, error = UsernameValidator.validate("valid_user123")
        assert valid is True
        assert error == ""

    def test_too_short(self):
        valid, error = UsernameValidator.validate("ab")
        assert valid is False
        assert "at least 3" in error

    def test_too_long(self):
        valid, error = UsernameValidator.validate("a" * 21)
        assert valid is False
        assert "not exceed 20" in error

    def test_invalid_characters(self):
        valid, error = UsernameValidator.validate("user-name!")
        assert valid is False
        assert "letters, numbers, and underscores" in error


class TestEmailValidator:
    """Test email validation."""

    def test_valid_email(self):
        valid, error = EmailValidator.validate("user@example.com")
        assert valid is True
        assert error == ""

    def test_invalid_format(self):
        valid, error = EmailValidator.validate("notanemail")
        assert valid is False
        assert "invalid" in error.lower()

    def test_empty_email(self):
        valid, error = EmailValidator.validate("")
        assert valid is False
        assert "required" in error.lower()


class TestUserStorage:
    """Test user storage."""

    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage directory."""
        temp_dir = tempfile.mkdtemp()
        storage = UserStorage(data_dir=temp_dir)
        yield storage
        shutil.rmtree(temp_dir)

    def test_create_user(self, temp_storage):
        username = "testuser"
        email = "test@example.com"
        password_hash = "hashed_password"

        user_data = temp_storage.create_user(username, email, password_hash)

        assert user_data['username'] == username
        assert user_data['email'] == email.lower()
        assert user_data['password_hash'] == password_hash

    def test_user_exists(self, temp_storage):
        username = "testuser"
        temp_storage.create_user(username, "test@example.com", "hash")

        assert temp_storage.user_exists(username) is True
        assert temp_storage.user_exists("nonexistent") is False

    def test_email_exists(self, temp_storage):
        email = "test@example.com"
        temp_storage.create_user("testuser", email, "hash")

        assert temp_storage.email_exists(email) is True
        assert temp_storage.email_exists("other@example.com") is False

    def test_get_user(self, temp_storage):
        username = "testuser"
        temp_storage.create_user(username, "test@example.com", "hash")

        user_data = temp_storage.get_user(username)

        assert user_data is not None
        assert user_data['username'] == username

    def test_get_user_by_email(self, temp_storage):
        email = "test@example.com"
        username = "testuser"
        temp_storage.create_user(username, email, "hash")

        user_data = temp_storage.get_user_by_email(email)

        assert user_data is not None
        assert user_data['username'] == username

    def test_duplicate_username(self, temp_storage):
        username = "testuser"
        temp_storage.create_user(username, "test1@example.com", "hash")

        with pytest.raises(ValueError, match="already exists"):
            temp_storage.create_user(username, "test2@example.com", "hash")

    def test_duplicate_email(self, temp_storage):
        email = "test@example.com"
        temp_storage.create_user("user1", email, "hash")

        with pytest.raises(ValueError, match="already registered"):
            temp_storage.create_user("user2", email, "hash")


class TestAccountManager:
    """Test account management."""

    @pytest.fixture
    def temp_account_manager(self):
        """Create account manager with temporary storage."""
        temp_dir = tempfile.mkdtemp()
        storage = UserStorage(data_dir=temp_dir)
        manager = AccountManager(storage=storage)
        yield manager
        shutil.rmtree(temp_dir)

    def test_register_success(self, temp_account_manager):
        success, message, user_data = temp_account_manager.register(
            "testuser",
            "test@example.com",
            "Password123!"
        )

        assert success is True
        assert "successfully" in message.lower()
        assert user_data is not None

    def test_register_invalid_username(self, temp_account_manager):
        success, message, _ = temp_account_manager.register(
            "ab",  # Too short
            "test@example.com",
            "Password123!"
        )

        assert success is False
        assert "at least 3" in message

    def test_register_invalid_password(self, temp_account_manager):
        success, message, _ = temp_account_manager.register(
            "testuser",
            "test@example.com",
            "short"  # Too short
        )

        assert success is False
        assert "at least 8" in message

    def test_login_success(self, temp_account_manager):
        # Register user first
        temp_account_manager.register("testuser", "test@example.com", "Password123!")

        # Attempt login
        success, message, token = temp_account_manager.login("testuser", "Password123!")

        assert success is True
        assert "successful" in message.lower()
        assert token is not None
        assert len(token) > 0

    def test_login_wrong_password(self, temp_account_manager):
        temp_account_manager.register("testuser", "test@example.com", "Password123!")

        success, message, token = temp_account_manager.login("testuser", "WrongPassword")

        assert success is False
        assert "invalid" in message.lower()
        assert token is None

    def test_login_nonexistent_user(self, temp_account_manager):
        success, message, token = temp_account_manager.login("nonexistent", "Password123!")

        assert success is False
        assert token is None

    def test_logout(self, temp_account_manager):
        temp_account_manager.register("testuser", "test@example.com", "Password123!")
        _, _, token = temp_account_manager.login("testuser", "Password123!")

        success, message = temp_account_manager.logout("testuser", token)

        assert success is True

    def test_password_reset_flow(self, temp_account_manager):
        # Register user
        temp_account_manager.register("testuser", "test@example.com", "Password123!")

        # Request reset
        success, message = temp_account_manager.request_password_reset(
            "test@example.com",
            "http://example.com/reset"
        )
        assert success is True

        # Get the reset token from user data (in real scenario, from email)
        user_data = temp_account_manager.storage.get_user("testuser")
        reset_tokens = user_data.get('reset_tokens', [])
        assert len(reset_tokens) > 0

        # Can't easily test actual reset without the raw token,
        # but we can verify the request was processed

    def test_change_password(self, temp_account_manager):
        temp_account_manager.register("testuser", "test@example.com", "OldPassword123!")

        success, message = temp_account_manager.change_password(
            "testuser",
            "OldPassword123!",
            "NewPassword456!"
        )

        assert success is True
        assert "successfully" in message.lower()

        # Verify can login with new password
        success, _, _ = temp_account_manager.login("testuser", "NewPassword456!")
        assert success is True

        # Verify cannot login with old password
        success, _, _ = temp_account_manager.login("testuser", "OldPassword123!")
        assert success is False
