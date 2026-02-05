"""Game configuration and settings management."""

import os
from pathlib import Path
from typing import Any

import yaml


# Base paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
CONFIG_DIR = BASE_DIR / "config"


class Config:
    """Game configuration container."""

    def __init__(self, data: dict[str, Any] | None = None):
        self._data = data or {}

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        keys = key.split(".")
        value = self._data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if value is None:
                return default
        return value

    @property
    def debug(self) -> bool:
        return self.get("debug", False)

    @property
    def game_title(self) -> str:
        return self.get("game.title", "The Magician")

    @property
    def data_dir(self) -> Path:
        return DATA_DIR

    @property
    def save_dir(self) -> Path:
        return DATA_DIR / "saves"

    @property
    def users_dir(self) -> Path:
        return DATA_DIR / "users"


def load_config(config_path: Path | None = None) -> Config:
    """Load configuration from YAML file."""
    if config_path is None:
        config_path = CONFIG_DIR / "game.yaml"

    if config_path.exists():
        with open(config_path, "r") as f:
            data = yaml.safe_load(f) or {}
    else:
        data = get_default_config()

    return Config(data)


def get_default_config() -> dict[str, Any]:
    """Return default configuration."""
    return {
        "debug": True,
        "game": {
            "title": "The Magician",
            "version": "0.1.0",
        },
        "auth": {
            "token_expiry_hours": 24,
            "password_min_length": 8,
            "bcrypt_rounds": 12,
        },
        "display": {
            "text_speed": "normal",
            "use_colors": True,
        },
    }
