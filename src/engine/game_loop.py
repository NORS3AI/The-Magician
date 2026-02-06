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
from ..character import PlayerCharacter, CoreAttributes
from ..combat import Battle, BattleResult, create_goblin, create_orc

logger = logging.getLogger(__name__)


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
        self.player: Optional[PlayerCharacter] = None
        self.current_user: Optional[str] = None
        self.current_battle: Optional[Battle] = None

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
                elif state == GameState.COMBAT:
                    self._handle_combat()
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

        # Create character with attributes from data
        attributes = CoreAttributes.from_dict(character_data.get('base_stats', {}))
        self.player = PlayerCharacter(
            username=self.current_user,
            character_name=character_name,
            path=character_name,
            attributes=attributes,
            level=character_data.get('level', 1),
            xp=0
        )

        # Load starting inventory
        starting_inventory = character_data.get('starting_inventory', [])
        self.player.inventory = starting_inventory

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
            self._start_combat()
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

        # Get XP progress
        xp_info = self.player.get_xp_progress()

        self.output.print_section(f"{self.player.character_name.title()} - Level {self.player.level}")

        # Core attributes
        stats_display = {
            "Strength": self.player.attributes.strength,
            "Constitution": self.player.attributes.constitution,
            "Agility": self.player.attributes.agility,
            "Intelligence": self.player.attributes.intelligence,
            "Willpower": self.player.attributes.willpower,
            "Charisma": self.player.attributes.charisma,
        }

        self.output.print_stats(stats_display)
        print()

        # Derived stats
        derived_display = {
            "Health": f"{self.player.derived_stats.current_health}/{self.player.derived_stats.max_health}",
            "Mana": f"{self.player.derived_stats.current_mana}/{self.player.derived_stats.max_mana}",
            "Stamina": f"{self.player.derived_stats.current_stamina}/{self.player.derived_stats.max_stamina}",
            "Carry Capacity": f"{self.player.derived_stats.carry_capacity} lbs",
            "Initiative": self.player.derived_stats.initiative,
        }

        self.output.print_stats(derived_display)
        print()

        # Experience
        xp_display = {
            "Total XP": xp_info['total_xp'],
            "Progress to Next Level": f"{xp_info['progress_xp']}/{xp_info['needed_xp']} ({xp_info['percentage']:.1f}%)",
        }

        if self.player.unspent_stat_points > 0:
            xp_display["Unspent Stat Points"] = self.player.unspent_stat_points

        self.output.print_stats(xp_display)
        print()

        # Abilities
        if self.player.abilities:
            self.output.print_colored("Abilities:", Color.YELLOW, Style.BOLD)
            for ability in self.player.abilities:
                print(f"  • {ability}")
            print()

        self.output.pause()
        self.state_machine.go_back()

    def _start_combat(self):
        """Initiate a combat encounter."""
        if not self.player:
            return

        # For testing, create a goblin encounter
        # TODO: Make this dynamic based on location/story
        enemies = [create_goblin(level=self.player.level)]

        self.current_battle = Battle(self.player, enemies)
        battle_start = self.current_battle.start()

        self.output.clear()
        self.output.print_section("COMBAT!")
        self.output.print_error(battle_start['message'])
        self.output.pause()

        self.state_machine.transition_to(GameState.COMBAT)

    def _handle_combat(self):
        """Handle combat state."""
        if not self.current_battle or not self.player:
            self.state_machine.transition_to(GameState.PLAYING)
            return

        # Check if battle is over
        if self.current_battle.result != BattleResult.ONGOING:
            self._end_combat()
            return

        # Show battle state
        self.output.clear()
        self.output.print_section("COMBAT - Turn {}".format(self.current_battle.turn_number + 1))

        # Show player status
        player_health = f"{self.player.derived_stats.current_health}/{self.player.derived_stats.max_health}"
        player_mana = f"{self.player.derived_stats.current_mana}/{self.player.derived_stats.max_mana}"
        player_stamina = f"{self.player.derived_stats.current_stamina}/{self.player.derived_stats.max_stamina}"

        self.output.print_colored(f"Your Status: HP {player_health} | MP {player_mana} | ST {player_stamina}", Color.GREEN)

        # Show enemies
        print("\nEnemies:")
        for i, enemy in enumerate(self.current_battle.enemies):
            if enemy.is_alive():
                enemy_health = f"{enemy.derived_stats.current_health}/{enemy.derived_stats.max_health}"
                self.output.print_colored(
                    f"  {i+1}. {enemy.name} - HP {enemy_health}",
                    Color.RED
                )

        # Show available actions
        print("\nActions:")
        print("  attack <target> - Attack enemy (e.g., 'attack 1')")
        print("  defend - Take defensive stance")
        print("  flee - Attempt to flee")
        print("  inventory - View inventory")
        print()

        # Get player action
        user_input = self.output.prompt("> ")
        command = self.input_handler.parse(user_input)

        if not command:
            return

        # Process combat command
        if command.action == "attack":
            target_index = 0
            if command.targets:
                try:
                    target_index = int(command.targets[0]) - 1
                except ValueError:
                    self.output.print_error("Invalid target number")
                    self.output.pause()
                    return

            result = self.current_battle.player_turn("Attack", target_index)
            self._show_combat_result(result)

            # Enemy turns
            if self.current_battle.result == BattleResult.ONGOING:
                self._execute_enemy_turns()

            self.current_battle.next_turn()

        elif command.action == "defend":
            result = self.current_battle.player_turn("Defend")
            self._show_combat_result(result)

            # Enemy turns
            if self.current_battle.result == BattleResult.ONGOING:
                self._execute_enemy_turns()

            self.current_battle.next_turn()

        elif command.action == "flee":
            result = self.current_battle.attempt_flee()
            self.output.print_info(result['message'])

            if result.get('success'):
                self.output.pause()
                self._end_combat()
            else:
                # Enemy gets free turn
                self._execute_enemy_turns()
                self.current_battle.next_turn()
                self.output.pause()

        elif command.action == "inventory":
            self.state_machine.transition_to(GameState.INVENTORY)

        else:
            self.output.print_error("Unknown combat command")
            self.output.pause()

    def _show_combat_result(self, result: Dict[str, Any]):
        """Display combat action result."""
        if 'error' in result:
            self.output.print_error(result['error'])
        elif 'message' in result:
            self.output.print_info(result['message'])

            if result.get('critical'):
                self.output.print_colored("CRITICAL HIT!", Color.BRIGHT_YELLOW, Style.BOLD)

        self.output.pause()

    def _execute_enemy_turns(self):
        """Execute all enemy turns."""
        for i, enemy in enumerate(self.current_battle.enemies):
            if not enemy.is_alive():
                continue

            result = self.current_battle.enemy_turn(i)

            if result.get('skipped'):
                continue

            self.output.print_warning(result.get('message', 'Enemy acts!'))

            if result.get('critical'):
                self.output.print_colored("Enemy CRITICAL HIT!", Color.BRIGHT_RED, Style.BOLD)

            self.output.pause()

            # Check if player died
            if self.player.derived_stats.current_health <= 0:
                self.current_battle.result = BattleResult.DEFEAT
                break

    def _end_combat(self):
        """Handle end of combat."""
        if not self.current_battle:
            return

        self.output.clear()
        self.output.print_section("COMBAT ENDED")

        if self.current_battle.result == BattleResult.VICTORY:
            rewards = self.current_battle.get_battle_state().get('rewards', {})
            self.output.print_success("Victory!")

            if 'rewards' in self.current_battle.__dict__ or hasattr(self.current_battle, '_calculate_rewards'):
                rewards = self.current_battle._calculate_rewards()
                xp_gained = rewards.get('xp', 0)
                gold_gained = rewards.get('gold', 0)

                self.output.print_info(f"You gained {xp_gained} XP and {gold_gained} gold!")

                # Award XP
                level_up_info = self.player.gain_xp(xp_gained)
                if level_up_info:
                    self.output.print_success(f"LEVEL UP! You are now level {level_up_info['new_level']}!")
                    self.output.print_info(f"You gained {level_up_info['stat_points_gained']} stat points!")

        elif self.current_battle.result == BattleResult.DEFEAT:
            self.output.print_error("You have been defeated!")
            # TODO: Handle death/respawn

        elif self.current_battle.result == BattleResult.FLED:
            self.output.print_warning("You fled from combat.")

        self.output.pause()
        self.current_battle = None
        self.state_machine.transition_to(GameState.PLAYING)

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
