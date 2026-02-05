"""Account management: registration, login, logout, and password reset."""

from datetime import datetime
from typing import Optional, Tuple, Dict

from .password import PasswordValidator, PasswordHasher
from .token import TokenGenerator, TokenManager
from .user_storage import UserStorage
from .email_service import EmailService
from ..utils.validation import UsernameValidator, EmailValidator


class AccountManager:
    """Manages user accounts and authentication."""

    def __init__(
        self,
        storage: Optional[UserStorage] = None,
        password_hasher: Optional[PasswordHasher] = None,
        token_manager: Optional[TokenManager] = None,
        email_service: Optional[EmailService] = None
    ):
        """
        Initialize account manager with required services.

        Args:
            storage: User storage instance
            password_hasher: Password hasher instance
            token_manager: Token manager instance
            email_service: Email service instance
        """
        self.storage = storage or UserStorage()
        self.password_hasher = password_hasher or PasswordHasher()
        self.token_manager = token_manager or TokenManager()
        self.email_service = email_service or EmailService(mode="dev")

    def register(self, username: str, email: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Register a new user account.

        Args:
            username: Desired username
            email: Email address
            password: Plain text password

        Returns:
            Tuple of (success, message, user_data)
        """
        # Validate username
        valid, error = UsernameValidator.validate(username)
        if not valid:
            return False, error, None

        # Validate email
        valid, error = EmailValidator.validate(email)
        if not valid:
            return False, error, None

        # Validate password
        valid, error = PasswordValidator.validate(password)
        if not valid:
            return False, error, None

        # Check if user already exists
        if self.storage.user_exists(username):
            return False, "Username already taken", None

        if self.storage.email_exists(email):
            return False, "Email already registered", None

        # Hash password
        password_hash = self.password_hasher.hash_password(password)

        # Create user
        try:
            user_data = self.storage.create_user(username, email, password_hash)

            # Send welcome email
            self.email_service.send_welcome_email(email, username)

            return True, "Account created successfully", user_data

        except Exception as e:
            return False, f"Failed to create account: {str(e)}", None

    def login(self, username: str, password: str) -> Tuple[bool, str, Optional[str]]:
        """
        Authenticate user and create session.

        Args:
            username: Username
            password: Plain text password

        Returns:
            Tuple of (success, message, session_token)
        """
        # Get user data
        user_data = self.storage.get_user(username)
        if not user_data:
            return False, "Invalid username or password", None

        # Verify password
        if not self.password_hasher.verify_password(password, user_data['password_hash']):
            return False, "Invalid username or password", None

        # Generate session token
        session_token = TokenGenerator.generate_session_token()
        token_record = self.token_manager.create_token_record(session_token, username)

        # Update user's active sessions
        active_sessions = user_data.get('active_sessions', [])
        active_sessions.append(token_record)

        # Update last login time
        updates = {
            'last_login': datetime.utcnow().isoformat(),
            'active_sessions': active_sessions
        }
        self.storage.update_user(username, updates)

        return True, "Login successful", session_token

    def logout(self, username: str, session_token: str) -> Tuple[bool, str]:
        """
        Logout user and invalidate session.

        Args:
            username: Username
            session_token: Session token to invalidate

        Returns:
            Tuple of (success, message)
        """
        user_data = self.storage.get_user(username)
        if not user_data:
            return False, "User not found"

        # Find and remove the session
        active_sessions = user_data.get('active_sessions', [])
        token_hash = TokenGenerator.hash_token(session_token)

        updated_sessions = [
            s for s in active_sessions
            if s['token_hash'] != token_hash
        ]

        self.storage.update_user(username, {'active_sessions': updated_sessions})
        return True, "Logout successful"

    def verify_session(self, username: str, session_token: str) -> bool:
        """
        Verify if a session token is valid.

        Args:
            username: Username
            session_token: Session token to verify

        Returns:
            True if session is valid
        """
        user_data = self.storage.get_user(username)
        if not user_data:
            return False

        active_sessions = user_data.get('active_sessions', [])
        token_hash = TokenGenerator.hash_token(session_token)

        for session in active_sessions:
            if session['token_hash'] == token_hash:
                is_valid, _ = self.token_manager.is_token_valid(session)
                return is_valid

        return False

    def request_password_reset(self, email: str, reset_url: str) -> Tuple[bool, str]:
        """
        Request a password reset.

        Args:
            email: Email address
            reset_url: Base URL for reset page

        Returns:
            Tuple of (success, message)
        """
        # Get user by email
        user_data = self.storage.get_user_by_email(email)

        # Don't reveal if email exists or not (security)
        if not user_data:
            return True, "If the email exists, a reset link has been sent"

        # Generate reset token
        reset_token = TokenGenerator.generate_reset_token()
        token_record = self.token_manager.create_token_record(reset_token, user_data['username'])

        # Store reset token
        reset_tokens = user_data.get('reset_tokens', [])
        reset_tokens.append(token_record)
        self.storage.update_user(user_data['username'], {'reset_tokens': reset_tokens})

        # Send reset email
        self.email_service.send_password_reset(
            email,
            user_data['username'],
            reset_token,
            reset_url
        )

        return True, "If the email exists, a reset link has been sent"

    def reset_password(self, reset_token: str, new_password: str) -> Tuple[bool, str]:
        """
        Reset password using a reset token.

        Args:
            reset_token: Password reset token
            new_password: New password

        Returns:
            Tuple of (success, message)
        """
        # Validate new password
        valid, error = PasswordValidator.validate(new_password)
        if not valid:
            return False, error

        # Find user with this reset token
        token_hash = TokenGenerator.hash_token(reset_token)

        for username in self.storage.list_users():
            user_data = self.storage.get_user(username)
            if not user_data:
                continue

            reset_tokens = user_data.get('reset_tokens', [])
            for token_record in reset_tokens:
                if token_record['token_hash'] == token_hash:
                    # Verify token is valid
                    if not self.token_manager.verify_token(reset_token, token_record):
                        return False, "Invalid or expired reset token"

                    # Hash new password
                    new_password_hash = self.password_hasher.hash_password(new_password)

                    # Mark token as used
                    token_record = self.token_manager.mark_token_used(token_record)

                    # Update password and tokens
                    self.storage.update_user(username, {
                        'password_hash': new_password_hash,
                        'reset_tokens': reset_tokens
                    })

                    return True, "Password reset successfully"

        return False, "Invalid or expired reset token"

    def request_username_reminder(self, email: str) -> Tuple[bool, str]:
        """
        Send username reminder to email.

        Args:
            email: Email address

        Returns:
            Tuple of (success, message)
        """
        user_data = self.storage.get_user_by_email(email)

        # Don't reveal if email exists or not (security)
        if not user_data:
            return True, "If the email exists, a username reminder has been sent"

        # Send reminder email
        self.email_service.send_username_reminder(email, user_data['username'])

        return True, "If the email exists, a username reminder has been sent"

    def change_password(self, username: str, current_password: str, new_password: str) -> Tuple[bool, str]:
        """
        Change user's password (when logged in).

        Args:
            username: Username
            current_password: Current password
            new_password: New password

        Returns:
            Tuple of (success, message)
        """
        # Get user data
        user_data = self.storage.get_user(username)
        if not user_data:
            return False, "User not found"

        # Verify current password
        if not self.password_hasher.verify_password(current_password, user_data['password_hash']):
            return False, "Current password is incorrect"

        # Validate new password
        valid, error = PasswordValidator.validate(new_password)
        if not valid:
            return False, error

        # Hash new password
        new_password_hash = self.password_hasher.hash_password(new_password)

        # Update password
        self.storage.update_user(username, {'password_hash': new_password_hash})

        return True, "Password changed successfully"
