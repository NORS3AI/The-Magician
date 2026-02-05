"""Data loading utilities for game content."""

import json
import yaml
from pathlib import Path
from typing import Any, Dict, Optional, Union
import logging

logger = logging.getLogger(__name__)


class DataLoader:
    """Loads game data from JSON and YAML files."""

    def __init__(self, data_dir: Union[str, Path] = "data"):
        """
        Initialize data loader.

        Args:
            data_dir: Root directory for game data files
        """
        self.data_dir = Path(data_dir)
        self._cache: Dict[str, Any] = {}
        self.use_cache = True

    def load_json(self, file_path: Union[str, Path], use_cache: bool = True) -> Optional[Dict]:
        """
        Load data from a JSON file.

        Args:
            file_path: Path to JSON file (relative to data_dir or absolute)
            use_cache: Whether to use cached data if available

        Returns:
            Parsed JSON data or None if file doesn't exist
        """
        # Convert to Path object
        path = Path(file_path)

        # If not absolute, make it relative to data_dir
        if not path.is_absolute():
            path = self.data_dir / path

        # Check cache
        cache_key = str(path)
        if use_cache and self.use_cache and cache_key in self._cache:
            logger.debug(f"Loading from cache: {path}")
            return self._cache[cache_key]

        # Check if file exists
        if not path.exists():
            logger.warning(f"File not found: {path}")
            return None

        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Cache the data
            if self.use_cache:
                self._cache[cache_key] = data

            logger.debug(f"Loaded JSON: {path}")
            return data

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {path}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error loading {path}: {e}")
            return None

    def load_yaml(self, file_path: Union[str, Path], use_cache: bool = True) -> Optional[Dict]:
        """
        Load data from a YAML file.

        Args:
            file_path: Path to YAML file (relative to data_dir or absolute)
            use_cache: Whether to use cached data if available

        Returns:
            Parsed YAML data or None if file doesn't exist
        """
        # Convert to Path object
        path = Path(file_path)

        # If not absolute, make it relative to data_dir
        if not path.is_absolute():
            path = self.data_dir / path

        # Check cache
        cache_key = str(path)
        if use_cache and self.use_cache and cache_key in self._cache:
            logger.debug(f"Loading from cache: {path}")
            return self._cache[cache_key]

        # Check if file exists
        if not path.exists():
            logger.warning(f"File not found: {path}")
            return None

        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            # Cache the data
            if self.use_cache:
                self._cache[cache_key] = data

            logger.debug(f"Loaded YAML: {path}")
            return data

        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML in {path}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error loading {path}: {e}")
            return None

    def load_character(self, character_name: str) -> Optional[Dict]:
        """
        Load character data.

        Args:
            character_name: Name of character (e.g., "tomas", "pug")

        Returns:
            Character data dict or None
        """
        file_path = f"characters/{character_name}_base.json"
        return self.load_json(file_path)

    def load_enemy(self, enemy_name: str) -> Optional[Dict]:
        """
        Load enemy data.

        Args:
            enemy_name: Name of enemy

        Returns:
            Enemy data dict or None
        """
        enemies_data = self.load_json("enemies/enemies.json")
        if enemies_data and enemy_name in enemies_data:
            return enemies_data[enemy_name]
        return None

    def load_item(self, item_name: str) -> Optional[Dict]:
        """
        Load item data.

        Args:
            item_name: Name of item

        Returns:
            Item data dict or None
        """
        # Try different item files
        for category in ["weapons", "armor", "consumables", "key_items"]:
            items_data = self.load_json(f"items/{category}.json")
            if items_data and item_name in items_data:
                return items_data[item_name]
        return None

    def load_location(self, location_id: str) -> Optional[Dict]:
        """
        Load location data.

        Args:
            location_id: Location identifier

        Returns:
            Location data dict or None
        """
        locations_data = self.load_json("story/locations.json")
        if locations_data and location_id in locations_data:
            return locations_data[location_id]
        return None

    def load_npc(self, npc_id: str) -> Optional[Dict]:
        """
        Load NPC data.

        Args:
            npc_id: NPC identifier

        Returns:
            NPC data dict or None
        """
        npcs_data = self.load_json("story/npcs.json")
        if npcs_data and npc_id in npcs_data:
            return npcs_data[npc_id]
        return None

    def clear_cache(self) -> None:
        """Clear the data cache."""
        self._cache.clear()
        logger.debug("Data cache cleared")

    def invalidate(self, file_path: Union[str, Path]) -> None:
        """
        Invalidate a specific cached file.

        Args:
            file_path: Path to file to invalidate
        """
        path = Path(file_path)
        if not path.is_absolute():
            path = self.data_dir / path

        cache_key = str(path)
        if cache_key in self._cache:
            del self._cache[cache_key]
            logger.debug(f"Invalidated cache for: {path}")

    def preload(self, file_paths: list) -> None:
        """
        Preload multiple files into cache.

        Args:
            file_paths: List of file paths to preload
        """
        for file_path in file_paths:
            path = Path(file_path)
            if path.suffix in ['.json', '.JSON']:
                self.load_json(file_path)
            elif path.suffix in ['.yaml', '.yml', '.YAML', '.YML']:
                self.load_yaml(file_path)

    def get_cache_stats(self) -> Dict[str, int]:
        """
        Get cache statistics.

        Returns:
            Dict with cache stats
        """
        return {
            'cached_files': len(self._cache),
            'cache_enabled': self.use_cache
        }
