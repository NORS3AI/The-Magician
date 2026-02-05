"""Main game loop and state management."""

from enum import Enum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.config.settings import Config


class GameState(Enum):
    """Possible game states."""
    MAIN_MENU = auto()
    LOGIN = auto()
    REGISTER = auto()
    CHARACTER_SELECT = auto()
    PLAYING = auto()
    COMBAT = auto()
    DIALOGUE = auto()
    INVENTORY = auto()
    PAUSE = auto()
    QUIT = auto()


class GameLoop:
    """Main game loop controller."""

    def __init__(self, config: "Config"):
        self.config = config
        self.state = GameState.MAIN_MENU
        self.running = False
        self.player = None

    def run(self):
        """Start the main game loop."""
        self.running = True

        while self.running:
            if self.state == GameState.MAIN_MENU:
                self._handle_main_menu()
            elif self.state == GameState.LOGIN:
                self._handle_login()
            elif self.state == GameState.REGISTER:
                self._handle_register()
            elif self.state == GameState.CHARACTER_SELECT:
                self._handle_character_select()
            elif self.state == GameState.PLAYING:
                self._handle_playing()
            elif self.state == GameState.QUIT:
                self._handle_quit()
            else:
                self._handle_main_menu()

    def _handle_main_menu(self):
        """Display and handle main menu."""
        print()
        print("MAIN MENU")
        print("-" * 40)
        print("1. Login")
        print("2. Register")
        print("3. Quit")
        print()

        choice = input("Enter choice: ").strip()

        if choice == "1":
            self.state = GameState.LOGIN
        elif choice == "2":
            self.state = GameState.REGISTER
        elif choice == "3":
            self.state = GameState.QUIT
        else:
            print("Invalid choice. Please try again.")

    def _handle_login(self):
        """Handle user login."""
        print()
        print("LOGIN")
        print("-" * 40)
        print("[Login system not yet implemented]")
        print()

        # Placeholder - will integrate with auth system
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        if username and password:
            print(f"Welcome back, {username}! (Demo mode)")
            self.state = GameState.CHARACTER_SELECT
        else:
            print("Login cancelled.")
            self.state = GameState.MAIN_MENU

    def _handle_register(self):
        """Handle user registration."""
        print()
        print("REGISTER NEW ACCOUNT")
        print("-" * 40)
        print("[Registration system not yet implemented]")
        print()

        # Placeholder - will integrate with auth system
        username = input("Choose username: ").strip()
        email = input("Email: ").strip()
        password = input("Password (min 8 chars): ").strip()

        if username and email and len(password) >= 8:
            print(f"Account created for {username}! (Demo mode)")
            self.state = GameState.MAIN_MENU
        else:
            print("Registration cancelled or invalid input.")
            self.state = GameState.MAIN_MENU

    def _handle_character_select(self):
        """Handle character/path selection."""
        print()
        print("CHOOSE YOUR PATH")
        print("-" * 40)
        print()
        print("Two boys from Crydee will shape the fate of two worlds.")
        print("Choose whose journey you will follow:")
        print()
        print("1. TOMAS - The Warrior")
        print("   Follow the path of martial prowess and ancient power.")
        print("   Face the Tsurani invasion and discover the secrets")
        print("   of the Valheru.")
        print()
        print("2. PUG - The Mage")
        print("   Follow the path of magic and knowledge.")
        print("   From apprentice to master, across two worlds,")
        print("   become the greatest magician of the age.")
        print()
        print("0. Back to Main Menu")
        print()

        choice = input("Enter choice: ").strip()

        if choice == "1":
            print()
            print("You have chosen the path of TOMAS.")
            print("[Story not yet implemented]")
            self.state = GameState.PLAYING
        elif choice == "2":
            print()
            print("You have chosen the path of PUG.")
            print("[Story not yet implemented]")
            self.state = GameState.PLAYING
        elif choice == "0":
            self.state = GameState.MAIN_MENU
        else:
            print("Invalid choice.")

    def _handle_playing(self):
        """Handle main gameplay."""
        print()
        print("GAMEPLAY")
        print("-" * 40)
        print("[Gameplay not yet implemented]")
        print()
        print("Commands: quit, menu, help")
        print()

        command = input("> ").strip().lower()

        if command in ("quit", "exit", "q"):
            self.state = GameState.QUIT
        elif command in ("menu", "m"):
            self.state = GameState.MAIN_MENU
        elif command == "help":
            print("Available commands: quit, menu, help")
        else:
            print(f"Unknown command: {command}")

    def _handle_quit(self):
        """Handle game exit."""
        print()
        print("Thank you for playing The Magician!")
        print("May your journey through Midkemia continue...")
        print()
        self.running = False
