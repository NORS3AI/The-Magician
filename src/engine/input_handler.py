"""Input handling and command parsing."""

import re
from typing import Optional, List, Tuple, Dict


class ParsedCommand:
    """Represents a parsed command from user input."""

    def __init__(self, action: str, targets: List[str], modifiers: Dict[str, str]):
        """
        Initialize parsed command.

        Args:
            action: The main action/verb (e.g., "look", "take", "attack")
            targets: List of target objects (e.g., ["sword"], ["orc", "with", "bow"])
            modifiers: Dict of modifiers (e.g., {"direction": "north"})
        """
        self.action = action.lower()
        self.targets = [t.lower() for t in targets]
        self.modifiers = {k.lower(): v.lower() for k, v in modifiers.items()}

    def has_target(self, target: str) -> bool:
        """
        Check if command targets a specific object.

        Args:
            target: Target name to check

        Returns:
            True if target is in targets list
        """
        return target.lower() in self.targets

    def get_modifier(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get a modifier value.

        Args:
            key: Modifier key
            default: Default value if not found

        Returns:
            Modifier value or default
        """
        return self.modifiers.get(key.lower(), default)

    def __str__(self) -> str:
        """String representation of command."""
        parts = [f"Action: {self.action}"]
        if self.targets:
            parts.append(f"Targets: {', '.join(self.targets)}")
        if self.modifiers:
            parts.append(f"Modifiers: {self.modifiers}")
        return " | ".join(parts)


class InputHandler:
    """Handles and parses user input."""

    # Common prepositions to filter out
    PREPOSITIONS = {'with', 'using', 'to', 'from', 'at', 'in', 'on', 'by'}

    # Direction mappings
    DIRECTIONS = {
        'n': 'north', 'north': 'north',
        's': 'south', 'south': 'south',
        'e': 'east', 'east': 'east',
        'w': 'west', 'west': 'west',
        'ne': 'northeast', 'northeast': 'northeast',
        'nw': 'northwest', 'northwest': 'northwest',
        'se': 'southeast', 'southeast': 'southeast',
        'sw': 'southwest', 'southwest': 'southwest',
        'u': 'up', 'up': 'up',
        'd': 'down', 'down': 'down'
    }

    def __init__(self):
        """Initialize input handler."""
        self.command_aliases: Dict[str, str] = {
            # Movement
            'go': 'move',
            'walk': 'move',
            'run': 'move',
            'travel': 'move',

            # Examination
            'l': 'look',
            'examine': 'look',
            'inspect': 'look',
            'check': 'look',

            # Inventory
            'i': 'inventory',
            'inv': 'inventory',
            'items': 'inventory',

            # Take/Drop
            'get': 'take',
            'grab': 'take',
            'pick': 'take',
            'pickup': 'take',
            'discard': 'drop',
            'throw': 'drop',

            # Combat
            'fight': 'attack',
            'hit': 'attack',
            'strike': 'attack',
            'kill': 'attack',

            # Talking
            'speak': 'talk',
            'chat': 'talk',
            'converse': 'talk',

            # Using items
            'consume': 'use',
            'drink': 'use',
            'eat': 'use',
            'apply': 'use',

            # Stats
            'status': 'stats',
            'character': 'stats',

            # Help
            'h': 'help',
            '?': 'help',

            # Quit
            'exit': 'quit',
            'q': 'quit',
            'logout': 'quit',
        }

    def parse(self, user_input: str) -> Optional[ParsedCommand]:
        """
        Parse user input into a command.

        Args:
            user_input: Raw user input string

        Returns:
            ParsedCommand object or None if invalid
        """
        if not user_input or not user_input.strip():
            return None

        # Normalize input
        text = user_input.strip().lower()

        # Handle special single-word commands first
        if text in self.DIRECTIONS:
            return ParsedCommand(
                action='move',
                targets=[],
                modifiers={'direction': self.DIRECTIONS[text]}
            )

        # Split into words
        words = text.split()
        if not words:
            return None

        # First word is the action
        action = words[0]

        # Resolve aliases
        action = self.command_aliases.get(action, action)

        # Parse targets and modifiers
        targets = []
        modifiers = {}

        i = 1
        while i < len(words):
            word = words[i]

            # Check if it's a direction
            if word in self.DIRECTIONS:
                modifiers['direction'] = self.DIRECTIONS[word]
                i += 1
                continue

            # Skip prepositions
            if word in self.PREPOSITIONS:
                i += 1
                continue

            # Otherwise, it's a target
            targets.append(word)
            i += 1

        return ParsedCommand(action, targets, modifiers)

    def normalize_direction(self, direction: str) -> Optional[str]:
        """
        Normalize a direction string.

        Args:
            direction: Direction input

        Returns:
            Normalized direction or None
        """
        return self.DIRECTIONS.get(direction.lower())

    def is_movement_command(self, command: ParsedCommand) -> bool:
        """
        Check if command is a movement command.

        Args:
            command: Parsed command

        Returns:
            True if command is movement-related
        """
        return (
            command.action == 'move' or
            command.get_modifier('direction') is not None
        )

    def extract_number(self, text: str) -> Optional[int]:
        """
        Extract a number from text.

        Args:
            text: Text containing a number

        Returns:
            Extracted number or None
        """
        match = re.search(r'\d+', text)
        return int(match.group()) if match else None

    def split_compound_targets(self, targets: List[str]) -> List[str]:
        """
        Split compound targets like "wooden_sword" into ["wooden", "sword"].

        Args:
            targets: List of target strings

        Returns:
            Expanded list of targets
        """
        result = []
        for target in targets:
            if '_' in target:
                result.extend(target.split('_'))
            else:
                result.append(target)
        return result

    def validate_command(self, command: ParsedCommand, valid_actions: List[str]) -> bool:
        """
        Validate if command action is in list of valid actions.

        Args:
            command: Parsed command
            valid_actions: List of valid action names

        Returns:
            True if command is valid
        """
        return command.action in valid_actions
