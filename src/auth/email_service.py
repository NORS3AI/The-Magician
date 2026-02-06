"""Email service for password resets and account notifications."""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class EmailService:
    """Email service for sending authentication-related emails."""

    def __init__(self, mode: str = "dev"):
        """
        Initialize email service.

        Args:
            mode: "dev" for logging only, "production" for actual SMTP
        """
        self.mode = mode

    def send_password_reset(self, email: str, username: str, reset_token: str, reset_url: str) -> bool:
        """
        Send password reset email.

        Args:
            email: Recipient email
            username: Username
            reset_token: Password reset token
            reset_url: Base URL for reset (token will be appended)

        Returns:
            True if email sent successfully
        """
        reset_link = f"{reset_url}?token={reset_token}"

        if self.mode == "dev":
            logger.info("=" * 60)
            logger.info("PASSWORD RESET EMAIL (DEV MODE)")
            logger.info("=" * 60)
            logger.info(f"To: {email}")
            logger.info(f"Subject: Password Reset Request - The Magician")
            logger.info("")
            logger.info(f"Hello {username},")
            logger.info("")
            logger.info("You have requested to reset your password for The Magician.")
            logger.info("Click the link below to reset your password:")
            logger.info("")
            logger.info(f"    {reset_link}")
            logger.info("")
            logger.info("This link will expire in 24 hours.")
            logger.info("")
            logger.info("If you did not request this reset, please ignore this email.")
            logger.info("=" * 60)
            return True
        else:
            # Production SMTP implementation would go here
            # For now, we'll use dev mode
            logger.warning("Production email not yet implemented, using dev mode")
            return self.send_password_reset(email, username, reset_token, reset_url)

    def send_username_reminder(self, email: str, username: str) -> bool:
        """
        Send username reminder email.

        Args:
            email: Recipient email
            username: Username to remind

        Returns:
            True if email sent successfully
        """
        if self.mode == "dev":
            logger.info("=" * 60)
            logger.info("USERNAME REMINDER EMAIL (DEV MODE)")
            logger.info("=" * 60)
            logger.info(f"To: {email}")
            logger.info(f"Subject: Username Reminder - The Magician")
            logger.info("")
            logger.info("Hello,")
            logger.info("")
            logger.info("You have requested a username reminder for The Magician.")
            logger.info("")
            logger.info(f"Your username is: {username}")
            logger.info("")
            logger.info("If you did not request this reminder, please ignore this email.")
            logger.info("=" * 60)
            return True
        else:
            logger.warning("Production email not yet implemented, using dev mode")
            return self.send_username_reminder(email, username)

    def send_welcome_email(self, email: str, username: str) -> bool:
        """
        Send welcome email to new users.

        Args:
            email: Recipient email
            username: New username

        Returns:
            True if email sent successfully
        """
        if self.mode == "dev":
            logger.info("=" * 60)
            logger.info("WELCOME EMAIL (DEV MODE)")
            logger.info("=" * 60)
            logger.info(f"To: {email}")
            logger.info(f"Subject: Welcome to The Magician!")
            logger.info("")
            logger.info(f"Welcome {username}!")
            logger.info("")
            logger.info("Thank you for joining The Magician, a text adventure RPG based on")
            logger.info("Raymond E. Feist's Riftwar Saga.")
            logger.info("")
            logger.info("Choose your path:")
            logger.info("  - Tomas: The Warrior Path")
            logger.info("  - Pug: The Mage Path")
            logger.info("")
            logger.info("May your journey be filled with adventure!")
            logger.info("=" * 60)
            return True
        else:
            logger.warning("Production email not yet implemented, using dev mode")
            return self.send_welcome_email(email, username)
