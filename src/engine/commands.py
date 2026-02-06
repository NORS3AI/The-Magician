"""Command definitions and registry."""

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from .input_handler import ParsedCommand


class CommandCategory(Enum):
    """Categories of commands."""
    MOVEMENT = "Movement"
    INTERACTION = "Interaction"
    INVENTORY = "Inventory"
    COMBAT = "Combat"
    INFO = "Information"
    SYSTEM = "System"


@dataclass
class CommandDefinition:
    """Definition of a game command."""
    name: str
    description: str
    category: CommandCategory
    aliases: List[str]
    usage: str
    examples: List[str]
    requires_target: bool = False

    def matches(self, action: str) -> bool:
        """
        Check if action matches this command.

        Args:
            action: Action string to check

        Returns:
            True if action matches command name or aliases
        """
        action_lower = action.lower()
        return action_lower == self.name or action_lower in self.aliases


class CommandRegistry:
    """Registry of all available commands."""

    def __init__(self):
        """Initialize command registry."""
        self.commands: Dict[str, CommandDefinition] = {}
        self._register_default_commands()

    def _register_default_commands(self):
        """Register all default game commands."""

        # Movement commands
        self.register(CommandDefinition(
            name="move",
            description="Move in a direction",
            category=CommandCategory.MOVEMENT,
            aliases=["go", "walk", "run", "travel"],
            usage="move <direction>",
            examples=["move north", "go east", "n", "south"],
            requires_target=False
        ))

        # Examination commands
        self.register(CommandDefinition(
            name="look",
            description="Look at your surroundings or examine an object",
            category=CommandCategory.INTERACTION,
            aliases=["l", "examine", "inspect", "check"],
            usage="look [target]",
            examples=["look", "look sword", "examine door", "l"],
            requires_target=False
        ))

        # Inventory commands
        self.register(CommandDefinition(
            name="inventory",
            description="View your inventory",
            category=CommandCategory.INVENTORY,
            aliases=["i", "inv", "items"],
            usage="inventory",
            examples=["inventory", "i", "inv"],
            requires_target=False
        ))

        self.register(CommandDefinition(
            name="take",
            description="Pick up an item",
            category=CommandCategory.INVENTORY,
            aliases=["get", "grab", "pick", "pickup"],
            usage="take <item>",
            examples=["take sword", "get potion", "pickup key"],
            requires_target=True
        ))

        self.register(CommandDefinition(
            name="drop",
            description="Drop an item from inventory",
            category=CommandCategory.INVENTORY,
            aliases=["discard", "throw"],
            usage="drop <item>",
            examples=["drop sword", "discard torch"],
            requires_target=True
        ))

        self.register(CommandDefinition(
            name="use",
            description="Use an item",
            category=CommandCategory.INVENTORY,
            aliases=["consume", "drink", "eat", "apply"],
            usage="use <item> [on target]",
            examples=["use potion", "use key on door", "eat bread"],
            requires_target=True
        ))

        self.register(CommandDefinition(
            name="equip",
            description="Equip a weapon or armor",
            category=CommandCategory.INVENTORY,
            aliases=["wear", "wield"],
            usage="equip <item>",
            examples=["equip sword", "wear armor", "wield staff"],
            requires_target=True
        ))

        self.register(CommandDefinition(
            name="unequip",
            description="Unequip a weapon or armor",
            category=CommandCategory.INVENTORY,
            aliases=["remove", "unwield"],
            usage="unequip <item>",
            examples=["unequip sword", "remove armor"],
            requires_target=True
        ))

        # Combat commands
        self.register(CommandDefinition(
            name="attack",
            description="Attack an enemy",
            category=CommandCategory.COMBAT,
            aliases=["fight", "hit", "strike", "kill"],
            usage="attack <target>",
            examples=["attack orc", "fight troll", "strike goblin"],
            requires_target=True
        ))

        self.register(CommandDefinition(
            name="defend",
            description="Take a defensive stance",
            category=CommandCategory.COMBAT,
            aliases=["block", "guard", "parry"],
            usage="defend",
            examples=["defend", "block", "guard"],
            requires_target=False
        ))

        self.register(CommandDefinition(
            name="flee",
            description="Attempt to escape from combat",
            category=CommandCategory.COMBAT,
            aliases=["escape", "run away"],
            usage="flee [direction]",
            examples=["flee", "flee north", "escape"],
            requires_target=False
        ))

        self.register(CommandDefinition(
            name="cast",
            description="Cast a spell (Pug path)",
            category=CommandCategory.COMBAT,
            aliases=["spell"],
            usage="cast <spell> [on target]",
            examples=["cast fireball on orc", "cast heal", "spell shield"],
            requires_target=True
        ))

        # Interaction commands
        self.register(CommandDefinition(
            name="talk",
            description="Talk to an NPC",
            category=CommandCategory.INTERACTION,
            aliases=["speak", "chat", "converse"],
            usage="talk to <npc>",
            examples=["talk to merchant", "speak with guard", "chat"],
            requires_target=False
        ))

        self.register(CommandDefinition(
            name="open",
            description="Open a door or container",
            category=CommandCategory.INTERACTION,
            aliases=["unlock"],
            usage="open <object>",
            examples=["open door", "open chest"],
            requires_target=True
        ))

        self.register(CommandDefinition(
            name="close",
            description="Close a door or container",
            category=CommandCategory.INTERACTION,
            aliases=["shut"],
            usage="close <object>",
            examples=["close door", "shut chest"],
            requires_target=True
        ))

        self.register(CommandDefinition(
            name="rest",
            description="Rest to recover health and stamina",
            category=CommandCategory.INTERACTION,
            aliases=["sleep", "camp"],
            usage="rest",
            examples=["rest", "sleep", "camp"],
            requires_target=False
        ))

        # Information commands
        self.register(CommandDefinition(
            name="stats",
            description="View your character stats",
            category=CommandCategory.INFO,
            aliases=["status", "character", "char"],
            usage="stats",
            examples=["stats", "status", "character"],
            requires_target=False
        ))

        self.register(CommandDefinition(
            name="help",
            description="Display help information",
            category=CommandCategory.SYSTEM,
            aliases=["h", "?", "commands"],
            usage="help [command]",
            examples=["help", "help attack", "commands"],
            requires_target=False
        ))

        # System commands
        self.register(CommandDefinition(
            name="save",
            description="Save your game",
            category=CommandCategory.SYSTEM,
            aliases=[],
            usage="save",
            examples=["save"],
            requires_target=False
        ))

        self.register(CommandDefinition(
            name="load",
            description="Load a saved game",
            category=CommandCategory.SYSTEM,
            aliases=[],
            usage="load",
            examples=["load"],
            requires_target=False
        ))

        self.register(CommandDefinition(
            name="quit",
            description="Quit the game",
            category=CommandCategory.SYSTEM,
            aliases=["exit", "q", "logout"],
            usage="quit",
            examples=["quit", "exit", "q"],
            requires_target=False
        ))

        self.register(CommandDefinition(
            name="menu",
            description="Return to main menu",
            category=CommandCategory.SYSTEM,
            aliases=["m"],
            usage="menu",
            examples=["menu", "m"],
            requires_target=False
        ))

    def register(self, command: CommandDefinition) -> None:
        """
        Register a command.

        Args:
            command: Command definition to register
        """
        self.commands[command.name] = command

    def get_command(self, action: str) -> Optional[CommandDefinition]:
        """
        Get command definition by action.

        Args:
            action: Action string (name or alias)

        Returns:
            CommandDefinition if found, None otherwise
        """
        action_lower = action.lower()

        # Check direct name match first
        if action_lower in self.commands:
            return self.commands[action_lower]

        # Check aliases
        for cmd in self.commands.values():
            if cmd.matches(action_lower):
                return cmd

        return None

    def get_commands_by_category(self, category: CommandCategory) -> List[CommandDefinition]:
        """
        Get all commands in a category.

        Args:
            category: Command category

        Returns:
            List of commands in category
        """
        return [cmd for cmd in self.commands.values() if cmd.category == category]

    def get_all_commands(self) -> List[CommandDefinition]:
        """
        Get all registered commands.

        Returns:
            List of all command definitions
        """
        return list(self.commands.values())

    def get_command_names(self) -> List[str]:
        """
        Get list of all command names.

        Returns:
            List of command names
        """
        return list(self.commands.keys())

    def is_valid_command(self, action: str) -> bool:
        """
        Check if action is a valid command.

        Args:
            action: Action to check

        Returns:
            True if valid command
        """
        return self.get_command(action) is not None

    def format_help(self, command_name: Optional[str] = None) -> str:
        """
        Format help text for a command or all commands.

        Args:
            command_name: Specific command to get help for, or None for all

        Returns:
            Formatted help text
        """
        if command_name:
            cmd = self.get_command(command_name)
            if not cmd:
                return f"Unknown command: {command_name}"

            lines = [
                f"Command: {cmd.name}",
                f"Description: {cmd.description}",
                f"Usage: {cmd.usage}",
                f"Category: {cmd.category.value}",
            ]

            if cmd.aliases:
                lines.append(f"Aliases: {', '.join(cmd.aliases)}")

            if cmd.examples:
                lines.append("Examples:")
                for example in cmd.examples:
                    lines.append(f"  - {example}")

            return "\n".join(lines)

        else:
            # Show all commands organized by category
            lines = ["Available Commands:", ""]

            for category in CommandCategory:
                cmds = self.get_commands_by_category(category)
                if cmds:
                    lines.append(f"{category.value}:")
                    for cmd in sorted(cmds, key=lambda c: c.name):
                        alias_text = f" ({', '.join(cmd.aliases)})" if cmd.aliases else ""
                        lines.append(f"  {cmd.name}{alias_text} - {cmd.description}")
                    lines.append("")

            lines.append("Type 'help <command>' for detailed information about a specific command.")
            return "\n".join(lines)
