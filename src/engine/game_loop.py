"""Main game loop and state management."""

from typing import Optional, Dict, Any
import logging

from .state_machine import StateMachine, GameState
from .output import OutputFormatter, Color, Style
from .input_handler import InputHandler, ParsedCommand
from .commands import CommandRegistry, CommandDefinition

from ..config.settings import Settings
from ..data import DataLoader
from ..auth import AccountManager

logger = logging.getLogger(__name__)


class Player:
    """Player character state."""

    def __init__(self, username: str, character_name: str, character_data: Dict):
        """
        Initialize player.

        Args:
            username: Account username
            character_name: Character name (tomas/pug)
            character_data: Character stats and info
        """
        self.username = username
        self.character_name = character_name
        self.data = character_data
        self.level = character_data.get('level', 1)
        self.stats = character_data.get('base_stats', {})
        self.inventory = character_data.get('starting_inventory', [])
        self.location = "crydee"  # Starting location
        self.health = self._calculate_max_health()
        self.mana = self._calculate_max_mana()

    def _calculate_max_health(self) -> int:
        """Calculate max health from constitution."""
        return 50 + (self.stats.get('constitution', 10) * 5)

    def _calculate_max_mana(self) -> int:
        """Calculate max mana from willpower."""
        return 30 + (self.stats.get('willpower', 10) * 3)


class GameLoop:
    """Main game loop controller."""

    def __init__(self, config: Optional[Settings] = None):
        """
        Initialize game loop.

        Args:
            config: Game configuration
        """
        self.config = config or Settings()
        self.state_machine = StateMachine()
        self.output = OutputFormatter(
            use_colors=self.config.get('display.use_colors', True),
            clear_screen=self.config.get('display.clear_screen', True)
        )
        self.input_handler = InputHandler()
        self.command_registry = CommandRegistry()
        self.data_loader = DataLoader()
        self.account_manager = AccountManager()

        self.running = False
        self.player: Optional[Player] = None
        self.current_user: Optional[str] = None

    def run(self):
        """Start the main game loop."""
        self.running = True
        self.output.print_title("THE MAGICIAN")
        self.output.print_story(
            "A Text Adventure RPG based on Raymond E. Feist's Riftwar Saga",
            indent=10
        )

        while self.running:
            try:
                state = self.state_machine.current_state

                if state == GameState.MAIN_MENU:
                    self._handle_main_menu()
                elif state == GameState.LOGIN:
                    self._handle_login()
                elif state == GameState.REGISTER:
                    self._handle_register()
                elif state == GameState.CHARACTER_SELECT:
                    self._handle_character_select()
                elif state == GameState.PLAYING:
                    self._handle_playing()
                elif state == GameState.INVENTORY:
                    self._handle_inventory()
                elif state == GameState.STATS:
                    self._handle_stats()
                elif state == GameState.PAUSE:
                    self._handle_pause()
                elif state == GameState.QUIT:
                    self._handle_quit()
                else:
                    self.output.print_error(f"Unknown state: {state}")
                    self.state_machine.transition_to(GameState.MAIN_MENU)

            except KeyboardInterrupt:
                print()
                if self.output.confirm("Are you sure you want to quit?"):
                    self.state_machine.transition_to(GameState.QUIT)
                else:
                    continue

            except Exception as e:
                logger.error(f"Error in game loop: {e}", exc_info=True)
                self.output.print_error(f"An error occurred: {e}")
                self.output.pause()

    def _handle_main_menu(self):
        """Display and handle main menu."""
        self.output.print_section("MAIN MENU")

        options = []
        if self.current_user:
            options.extend([
                f"Continue as {self.current_user}",
                "Logout",
                "Quit"
            ])
            self.output.print_menu("", options, numbered=True)
            choice = self.output.prompt("> ")

            if choice == "1":
                self.state_machine.transition_to(GameState.CHARACTER_SELECT)
            elif choice == "2":
                self.current_user = None
                self.player = None
                self.output.print_success("Logged out successfully")
                self.output.pause()
            elif choice == "3":
                self.state_machine.transition_to(GameState.QUIT)
        else:
            options.extend([
                "Login",
                "Register",
                "Quit"
            ])
            self.output.print_menu("", options, numbered=True)
            choice = self.output.prompt("> ")

            if choice == "1":
                self.state_machine.transition_to(GameState.LOGIN)
            elif choice == "2":
                self.state_machine.transition_to(GameState.REGISTER)
            elif choice == "3":
                self.state_machine.transition_to(GameState.QUIT)

    def _handle_login(self):
        """Handle user login."""
        self.output.print_section("LOGIN")

        username = self.output.prompt("Username: ")
        password = self.output.prompt("Password: ")

        if not username or not password:
            self.output.print_warning("Login cancelled")
            self.state_machine.transition_to(GameState.MAIN_MENU)
            return

        success, message, token = self.account_manager.login(username, password)

        if success:
            self.current_user = username
            self.output.print_success(f"Welcome back, {username}!")
            self.output.pause()
            self.state_machine.transition_to(GameState.CHARACTER_SELECT)
        else:
            self.output.print_error(message)
            self.output.pause()
            self.state_machine.transition_to(GameState.MAIN_MENU)

    def _handle_register(self):
        """Handle user registration."""
        self.output.print_section("REGISTER NEW ACCOUNT")

        username = self.output.prompt("Choose username: ")
        email = self.output.prompt("Email: ")
        password = self.output.prompt("Password (min 8 chars): ")

        if not username or not email or not password:
            self.output.print_warning("Registration cancelled")
            self.state_machine.transition_to(GameState.MAIN_MENU)
            return

        success, message, user_data = self.account_manager.register(username, email, password)

        if success:
            self.current_user = username
            self.output.print_success("Account created successfully!")
            self.output.pause()
            self.state_machine.transition_to(GameState.CHARACTER_SELECT)
        else:
            self.output.print_error(message)
            self.output.pause()
            self.state_machine.transition_to(GameState.MAIN_MENU)

    def _handle_character_select(self):
        """Handle character/path selection."""
        self.output.print_section("CHOOSE YOUR PATH")

        self.output.print_story(
            "Two boys from Crydee will shape the fate of two worlds.\n"
            "Choose whose journey you will follow:"
        )

        self.output.print_colored("1. TOMAS - The Warrior", Color.RED, Style.BOLD)
        self.output.print_story(
            "Follow the path of martial prowess and ancient power.\n"
            "Face the Tsurani invasion and discover the secrets of the Valheru.",
            indent=3
        )

        self.output.print_colored("2. PUG - The Mage", Color.BLUE, Style.BOLD)
        self.output.print_story(
            "Follow the path of magic and knowledge.\n"
            "From apprentice to master, across two worlds,\n"
            "become the greatest magician of the age.",
            indent=3
        )

        print("0. Back to Main Menu\n")

        choice = self.output.prompt("> ")

        if choice == "1":
            self._create_player("tomas")
        elif choice == "2":
            self._create_player("pug")
        elif choice == "0":
            self.state_machine.transition_to(GameState.MAIN_MENU)
        else:
            self.output.print_error("Invalid choice")

    def _create_player(self, character_name: str):
        """
        Create player character.

        Args:
            character_name: Character to create (tomas/pug)
        """
        character_data = self.data_loader.load_character(character_name)
        if not character_data:
            self.output.print_error(f"Failed to load character data for {character_name}")
            return

        self.player = Player(self.current_user, character_name, character_data)

        self.output.clear()
        self.output.print_success(f"You have chosen the path of {character_name.upper()}")
        self.output.print_story(
            f"\nYour journey begins in Crydee, a small town on the western frontier of the Kingdom...",
            indent=2
        )
        self.output.pause()

        self.state_machine.transition_to(GameState.PLAYING)

    def _handle_playing(self):
        """Handle main gameplay."""
        if not self.player:
            self.state_machine.transition_to(GameState.MAIN_MENU)
            return

        # Display location (simplified for now)
        self.output.print_section(f"Location: {self.player.location.title()}")
        self.output.print_story(
            "You stand in the courtyard of Castle Crydee. "
            "The sounds of daily life echo around you."
        )

        # Get command
        user_input = self.output.prompt("> ")
        command = self.input_handler.parse(user_input)

        if not command:
            return

        # Process command
        self._process_command(command)

    def _process_command(self, command: ParsedCommand):
        """
        Process a parsed command.

        Args:
            command: Parsed command to execute
        """
        action = command.action

        # System commands
        if action == "quit":
            self.state_machine.transition_to(GameState.QUIT)
        elif action == "menu":
            if self.output.confirm("Return to main menu?"):
                self.state_machine.transition_to(GameState.MAIN_MENU)
        elif action == "help":
            self._show_help(command.targets[0] if command.targets else None)
        elif action == "inventory":
            self.state_machine.transition_to(GameState.INVENTORY)
        elif action == "stats":
            self.state_machine.transition_to(GameState.STATS)

        # Gameplay commands
        elif action == "look":
            self._cmd_look(command)
        elif action == "move":
            self._cmd_move(command)
        elif action == "take":
            self.output.print_info("Take command not yet implemented")
        elif action == "drop":
            self.output.print_info("Drop command not yet implemented")
        elif action == "use":
            self.output.print_info("Use command not yet implemented")
        elif action == "attack":
            self.output.print_info("Combat not yet implemented")
        elif action == "talk":
            self.output.print_info("Dialogue not yet implemented")

        else:
            # Check if it's a valid command
            cmd_def = self.command_registry.get_command(action)
            if cmd_def:
                self.output.print_info(f"{cmd_def.description} - Not yet implemented")
            else:
                self.output.print_error(f"Unknown command: {action}")
                self.output.print_info("Type 'help' for available commands")

    def _cmd_look(self, command: ParsedCommand):
        """Handle look command."""
        if not command.targets:
            self.output.print_story(
                "You stand in the courtyard of Castle Crydee. "
                "The castle walls rise high above you. To the north is the keep, "
                "to the east are the stables, and to the west lies the training ground."
            )
        else:
            target = " ".join(command.targets)
            self.output.print_info(f"You examine the {target}, but see nothing special.")

    def _cmd_move(self, command: ParsedCommand):
        """Handle move command."""
        direction = command.get_modifier('direction')
        if not direction:
            self.output.print_error("Move where? Specify a direction.")
            return

        self.output.print_info(f"You head {direction}... (Movement not yet fully implemented)")

    def _show_help(self, command_name: Optional[str]):
        """
        Show help information.

        Args:
            command_name: Specific command to get help for, or None for all
        """
        help_text = self.command_registry.format_help(command_name)
        self.output.print_section("HELP")
        print(help_text)
        print()
        self.output.pause()

    def _handle_inventory(self):
        """Handle inventory screen."""
        if not self.player:
            self.state_machine.go_back()
            return

        self.output.print_section(f"{self.player.character_name.title()}'s Inventory")

        if not self.player.inventory:
            self.output.print_info("Your inventory is empty.")
        else:
            for item in self.player.inventory:
                item_name = item.get('item', 'Unknown')
                quantity = item.get('quantity', 1)
                self.output.print_colored(f"  • {item_name} x{quantity}", Color.YELLOW)

        print()
        self.output.pause()
        self.state_machine.go_back()

    def _handle_stats(self):
        """Handle stats display."""
        if not self.player:
            self.state_machine.go_back()
            return

        self.output.print_section(f"{self.player.character_name.title()} - Level {self.player.level}")

        stats_display = {
            "Strength": self.player.stats.get('strength', 0),
            "Constitution": self.player.stats.get('constitution', 0),
            "Agility": self.player.stats.get('agility', 0),
            "Intelligence": self.player.stats.get('intelligence', 0),
            "Willpower": self.player.stats.get('willpower', 0),
            "Charisma": self.player.stats.get('charisma', 0),
            "",
            "Health": f"{self.player.health}/{self.player.health}",
            "Mana": f"{self.player.mana}/{self.player.mana}",
        }

        self.output.print_stats(stats_display)
        print()
        self.output.pause()
        self.state_machine.go_back()

    def _handle_pause(self):
        """Handle pause menu."""
        self.output.print_section("PAUSED")

        options = [
            "Resume",
            "Save Game",
            "Return to Main Menu",
            "Quit"
        ]

        self.output.print_menu("", options, numbered=True)
        choice = self.output.prompt("> ")

        if choice == "1":
            self.state_machine.go_back()
        elif choice == "2":
            self.output.print_info("Save functionality not yet implemented")
            self.output.pause()
        elif choice == "3":
            if self.output.confirm("Return to main menu? (Unsaved progress will be lost)"):
                self.state_machine.transition_to(GameState.MAIN_MENU)
        elif choice == "4":
            if self.output.confirm("Quit game? (Unsaved progress will be lost)"):
                self.state_machine.transition_to(GameState.QUIT)

    def _handle_quit(self):
        """Handle game exit."""
        print()
        self.output.print_colored(
            "Thank you for playing The Magician!",
            Color.BRIGHT_CYAN,
            Style.BOLD
        )
        self.output.print_story(
            "May your journey through Midkemia continue...",
            indent=5
        )
        print()
        self.running = False
