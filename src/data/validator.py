"""Data validation for game content."""

from typing import Any, Dict, List, Optional, Set
import logging

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Raised when data validation fails."""
    pass


class DataValidator:
    """Validates game data structures."""

    # Required fields for different data types
    CHARACTER_SCHEMA = {
        'required': {'name', 'path_type', 'base_stats', 'starting_inventory'},
        'optional': {'description', 'special_abilities', 'level'}
    }

    ENEMY_SCHEMA = {
        'required': {'name', 'type', 'health', 'stats'},
        'optional': {'description', 'loot', 'abilities', 'weaknesses'}
    }

    ITEM_SCHEMA = {
        'required': {'name', 'type', 'description'},
        'optional': {'value', 'weight', 'effects', 'requirements', 'stackable'}
    }

    LOCATION_SCHEMA = {
        'required': {'id', 'name', 'description'},
        'optional': {'exits', 'npcs', 'items', 'enemies', 'events'}
    }

    NPC_SCHEMA = {
        'required': {'id', 'name', 'description'},
        'optional': {'dialogue', 'shop', 'quests', 'relationship'}
    }

    STATS_SCHEMA = {
        'required': {'strength', 'constitution', 'agility', 'intelligence', 'willpower', 'charisma'},
        'optional': {}
    }

    def validate_character(self, data: Dict) -> bool:
        """
        Validate character data.

        Args:
            data: Character data dict

        Returns:
            True if valid

        Raises:
            ValidationError: If validation fails
        """
        self._validate_schema(data, self.CHARACTER_SCHEMA, "Character")

        # Validate base_stats
        if 'base_stats' in data:
            self.validate_stats(data['base_stats'])

        # Validate starting_inventory is a list
        if 'starting_inventory' in data:
            if not isinstance(data['starting_inventory'], list):
                raise ValidationError("starting_inventory must be a list")

        return True

    def validate_enemy(self, data: Dict) -> bool:
        """
        Validate enemy data.

        Args:
            data: Enemy data dict

        Returns:
            True if valid

        Raises:
            ValidationError: If validation fails
        """
        self._validate_schema(data, self.ENEMY_SCHEMA, "Enemy")

        # Validate health is positive
        if data.get('health', 0) <= 0:
            raise ValidationError("Enemy health must be positive")

        # Validate stats
        if 'stats' in data:
            self.validate_stats(data['stats'])

        return True

    def validate_item(self, data: Dict) -> bool:
        """
        Validate item data.

        Args:
            data: Item data dict

        Returns:
            True if valid

        Raises:
            ValidationError: If validation fails
        """
        self._validate_schema(data, self.ITEM_SCHEMA, "Item")

        # Validate item type is known
        valid_types = {'weapon', 'armor', 'consumable', 'key_item', 'tool', 'valuable'}
        if data.get('type') not in valid_types:
            raise ValidationError(f"Invalid item type: {data.get('type')}")

        # Validate numeric fields
        if 'value' in data and data['value'] < 0:
            raise ValidationError("Item value cannot be negative")

        if 'weight' in data and data['weight'] < 0:
            raise ValidationError("Item weight cannot be negative")

        return True

    def validate_location(self, data: Dict) -> bool:
        """
        Validate location data.

        Args:
            data: Location data dict

        Returns:
            True if valid

        Raises:
            ValidationError: If validation fails
        """
        self._validate_schema(data, self.LOCATION_SCHEMA, "Location")

        # Validate exits are valid directions
        if 'exits' in data:
            valid_directions = {'north', 'south', 'east', 'west', 'northeast',
                              'northwest', 'southeast', 'southwest', 'up', 'down'}
            for direction in data['exits'].keys():
                if direction not in valid_directions:
                    raise ValidationError(f"Invalid exit direction: {direction}")

        return True

    def validate_npc(self, data: Dict) -> bool:
        """
        Validate NPC data.

        Args:
            data: NPC data dict

        Returns:
            True if valid

        Raises:
            ValidationError: If validation fails
        """
        self._validate_schema(data, self.NPC_SCHEMA, "NPC")
        return True

    def validate_stats(self, data: Dict) -> bool:
        """
        Validate character/enemy stats.

        Args:
            data: Stats data dict

        Returns:
            True if valid

        Raises:
            ValidationError: If validation fails
        """
        self._validate_schema(data, self.STATS_SCHEMA, "Stats")

        # Validate all stats are positive numbers
        for stat_name, stat_value in data.items():
            if not isinstance(stat_value, (int, float)):
                raise ValidationError(f"Stat {stat_name} must be a number")
            if stat_value < 0:
                raise ValidationError(f"Stat {stat_name} cannot be negative")

        return True

    def _validate_schema(self, data: Dict, schema: Dict, data_type: str) -> None:
        """
        Validate data against a schema.

        Args:
            data: Data to validate
            schema: Schema definition with 'required' and 'optional' sets
            data_type: Type name for error messages

        Raises:
            ValidationError: If validation fails
        """
        if not isinstance(data, dict):
            raise ValidationError(f"{data_type} data must be a dictionary")

        required_fields = schema['required']
        optional_fields = schema.get('optional', set())
        all_valid_fields = required_fields | optional_fields

        # Check for missing required fields
        missing = required_fields - set(data.keys())
        if missing:
            raise ValidationError(f"{data_type} missing required fields: {missing}")

        # Check for unknown fields
        unknown = set(data.keys()) - all_valid_fields
        if unknown:
            logger.warning(f"{data_type} has unknown fields: {unknown}")

    def validate_batch(self, data_items: List[Dict], validator_func: callable) -> Dict[str, List[str]]:
        """
        Validate multiple items and collect errors.

        Args:
            data_items: List of data items to validate
            validator_func: Validation function to use

        Returns:
            Dict with 'valid' and 'errors' lists
        """
        results = {
            'valid': [],
            'errors': []
        }

        for i, item in enumerate(data_items):
            try:
                validator_func(item)
                results['valid'].append(item.get('name', f'Item {i}'))
            except ValidationError as e:
                results['errors'].append(f"Item {i}: {str(e)}")

        return results

    def validate_file_data(self, data: Dict, data_type: str) -> bool:
        """
        Validate entire data file based on type.

        Args:
            data: Data to validate
            data_type: Type of data ('character', 'enemy', 'item', etc.)

        Returns:
            True if all data is valid

        Raises:
            ValidationError: If validation fails
        """
        validators = {
            'character': self.validate_character,
            'enemy': self.validate_enemy,
            'item': self.validate_item,
            'location': self.validate_location,
            'npc': self.validate_npc,
            'stats': self.validate_stats
        }

        validator = validators.get(data_type.lower())
        if not validator:
            raise ValidationError(f"Unknown data type: {data_type}")

        # If data is a dict of items, validate each one
        if isinstance(data, dict) and not any(key in self.CHARACTER_SCHEMA['required'] for key in data.keys()):
            errors = []
            for key, value in data.items():
                try:
                    validator(value)
                except ValidationError as e:
                    errors.append(f"{key}: {str(e)}")

            if errors:
                raise ValidationError(f"Validation errors:\n" + "\n".join(errors))
        else:
            # Single item validation
            validator(data)

        return True
