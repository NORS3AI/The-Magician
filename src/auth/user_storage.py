"""User data storage and retrieval."""

import json
import os
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime
import threading


class UserStorage:
    """Manages user data persistence to JSON files."""

    def __init__(self, data_dir: str = "data/users"):
        """
        Initialize user storage.

        Args:
            data_dir: Directory to store user data files
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def _get_user_file(self, username: str) -> Path:
        """Get the file path for a user's data."""
        # Use lowercase username for consistency
        return self.data_dir / f"{username.lower()}.json"

    def _get_index_file(self) -> Path:
        """Get the path to the user index file."""
        return self.data_dir / "_index.json"

    def _load_index(self) -> Dict[str, str]:
        """Load the user index (email -> username mapping)."""
        index_file = self._get_index_file()
        if index_file.exists():
            with open(index_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_index(self, index: Dict[str, str]) -> None:
        """Save the user index."""
        with open(self._get_index_file(), 'w') as f:
            json.dump(index, f, indent=2)

    def user_exists(self, username: str) -> bool:
        """
        Check if a user exists.

        Args:
            username: Username to check

        Returns:
            True if user exists
        """
        return self._get_user_file(username).exists()

    def email_exists(self, email: str) -> bool:
        """
        Check if an email is already registered.

        Args:
            email: Email to check

        Returns:
            True if email exists
        """
        index = self._load_index()
        return email.lower() in index

    def create_user(self, username: str, email: str, password_hash: str) -> Dict:
        """
        Create a new user account.

        Args:
            username: Username
            email: Email address
            password_hash: Hashed password

        Returns:
            User data dict

        Raises:
            ValueError: If user or email already exists
        """
        with self._lock:
            if self.user_exists(username):
                raise ValueError("Username already exists")

            if self.email_exists(email):
                raise ValueError("Email already registered")

            user_data = {
                'username': username,
                'email': email.lower(),
                'password_hash': password_hash,
                'created_at': datetime.utcnow().isoformat(),
                'last_login': None,
                'email_verified': False,
                'active_sessions': [],
                'reset_tokens': []
            }

            # Save user file
            user_file = self._get_user_file(username)
            with open(user_file, 'w') as f:
                json.dump(user_data, f, indent=2)

            # Update index
            index = self._load_index()
            index[email.lower()] = username.lower()
            self._save_index(index)

            return user_data

    def get_user(self, username: str) -> Optional[Dict]:
        """
        Retrieve user data by username.

        Args:
            username: Username to retrieve

        Returns:
            User data dict or None if not found
        """
        user_file = self._get_user_file(username)
        if not user_file.exists():
            return None

        with open(user_file, 'r') as f:
            return json.load(f)

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """
        Retrieve user data by email.

        Args:
            email: Email to search for

        Returns:
            User data dict or None if not found
        """
        index = self._load_index()
        username = index.get(email.lower())
        if username:
            return self.get_user(username)
        return None

    def update_user(self, username: str, updates: Dict) -> bool:
        """
        Update user data.

        Args:
            username: Username to update
            updates: Dictionary of fields to update

        Returns:
            True if updated successfully
        """
        with self._lock:
            user_data = self.get_user(username)
            if not user_data:
                return False

            # Apply updates
            user_data.update(updates)

            # Save back to file
            user_file = self._get_user_file(username)
            with open(user_file, 'w') as f:
                json.dump(user_data, f, indent=2)

            return True

    def list_users(self) -> List[str]:
        """
        List all usernames.

        Returns:
            List of usernames
        """
        users = []
        for file in self.data_dir.glob("*.json"):
            if file.name != "_index.json":
                users.append(file.stem)
        return users
