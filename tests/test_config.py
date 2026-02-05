"""Tests for configuration system."""

import pytest
from src.config.settings import Config, get_default_config, load_config


def test_default_config():
    """Test that default config has expected values."""
    config = get_default_config()
    assert config["debug"] is True
    assert config["game"]["title"] == "The Magician"
    assert config["auth"]["password_min_length"] == 8


def test_config_get():
    """Test Config.get with dot notation."""
    config = Config({"game": {"title": "Test", "nested": {"value": 42}}})
    assert config.get("game.title") == "Test"
    assert config.get("game.nested.value") == 42
    assert config.get("nonexistent", "default") == "default"


def test_config_properties():
    """Test Config property accessors."""
    config = Config(get_default_config())
    assert config.debug is True
    assert config.game_title == "The Magician"
