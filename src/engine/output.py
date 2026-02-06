"""Text output and formatting utilities."""

import os
import sys
from enum import Enum
from typing import Optional, List


class Color(Enum):
    """ANSI color codes for terminal output."""
    RESET = "\033[0m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"


class Style(Enum):
    """ANSI style codes."""
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"


class OutputFormatter:
    """Handles text output with formatting and colors."""

    def __init__(self, use_colors: bool = True, clear_screen: bool = True):
        """
        Initialize output formatter.

        Args:
            use_colors: Whether to use ANSI colors
            clear_screen: Whether to support clear screen functionality
        """
        self.use_colors = use_colors and self._supports_color()
        self.clear_screen_enabled = clear_screen

    def _supports_color(self) -> bool:
        """
        Check if terminal supports colors.

        Returns:
            True if colors are supported
        """
        # Check if stdout is a terminal
        if not hasattr(sys.stdout, 'isatty') or not sys.stdout.isatty():
            return False

        # Check for NO_COLOR environment variable
        if os.environ.get('NO_COLOR'):
            return False

        # Windows typically doesn't support ANSI colors without special setup
        if sys.platform == 'win32':
            return False

        return True

    def colorize(self, text: str, color: Color, style: Optional[Style] = None) -> str:
        """
        Apply color and style to text.

        Args:
            text: Text to colorize
            color: Color to apply
            style: Optional style to apply

        Returns:
            Formatted text string
        """
        if not self.use_colors:
            return text

        result = color.value
        if style:
            result += style.value
        result += text + Color.RESET.value

        return result

    def print_colored(self, text: str, color: Color, style: Optional[Style] = None) -> None:
        """
        Print colored text.

        Args:
            text: Text to print
            color: Color to use
            style: Optional style
        """
        print(self.colorize(text, color, style))

    def print_title(self, text: str) -> None:
        """
        Print a title (centered, styled).

        Args:
            text: Title text
        """
        width = 60
        border = "=" * width

        self.print_colored(border, Color.CYAN, Style.BOLD)
        centered = text.center(width)
        self.print_colored(centered, Color.BRIGHT_CYAN, Style.BOLD)
        self.print_colored(border, Color.CYAN, Style.BOLD)
        print()

    def print_section(self, text: str) -> None:
        """
        Print a section header.

        Args:
            text: Section text
        """
        print()
        self.print_colored(text, Color.YELLOW, Style.BOLD)
        self.print_colored("-" * len(text), Color.YELLOW)
        print()

    def print_error(self, text: str) -> None:
        """
        Print an error message.

        Args:
            text: Error text
        """
        self.print_colored(f"ERROR: {text}", Color.RED, Style.BOLD)

    def print_success(self, text: str) -> None:
        """
        Print a success message.

        Args:
            text: Success text
        """
        self.print_colored(f"✓ {text}", Color.GREEN, Style.BOLD)

    def print_warning(self, text: str) -> None:
        """
        Print a warning message.

        Args:
            text: Warning text
        """
        self.print_colored(f"⚠ {text}", Color.YELLOW)

    def print_info(self, text: str) -> None:
        """
        Print an info message.

        Args:
            text: Info text
        """
        self.print_colored(f"ℹ {text}", Color.CYAN)

    def print_story(self, text: str, indent: int = 0) -> None:
        """
        Print story text (narrative descriptions).

        Args:
            text: Story text
            indent: Number of spaces to indent
        """
        indentation = " " * indent
        for line in text.split('\n'):
            if line.strip():
                print(f"{indentation}{line}")
        print()

    def print_dialogue(self, speaker: str, text: str) -> None:
        """
        Print dialogue from an NPC.

        Args:
            speaker: Name of the speaker
            text: Dialogue text
        """
        self.print_colored(f"{speaker}:", Color.MAGENTA, Style.BOLD)
        print(f'  "{text}"')
        print()

    def print_menu(self, title: str, options: List[str], numbered: bool = True) -> None:
        """
        Print a menu with options.

        Args:
            title: Menu title
            options: List of menu options
            numbered: Whether to number the options
        """
        self.print_section(title)

        for i, option in enumerate(options, 1):
            if numbered:
                print(f"  {i}. {option}")
            else:
                print(f"  • {option}")
        print()

    def print_box(self, text: str, width: int = 60) -> None:
        """
        Print text in a box.

        Args:
            text: Text to box
            width: Box width
        """
        border = "+" + "-" * (width - 2) + "+"

        print(border)
        for line in text.split('\n'):
            padding = width - len(line) - 4
            print(f"| {line}{' ' * padding} |")
        print(border)

    def print_stats(self, stats: dict) -> None:
        """
        Print character stats in a formatted way.

        Args:
            stats: Dictionary of stat name to value
        """
        max_key_length = max(len(k) for k in stats.keys()) if stats else 0

        for key, value in stats.items():
            key_padded = key.ljust(max_key_length)
            self.print_colored(f"  {key_padded}: ", Color.CYAN)
            print(f"{value}")

    def clear(self) -> None:
        """Clear the screen."""
        if not self.clear_screen_enabled:
            return

        # Clear command depends on OS
        if os.name == 'nt':  # Windows
            os.system('cls')
        else:  # Unix/Linux/Mac
            os.system('clear')

    def prompt(self, text: str, color: Color = Color.BRIGHT_WHITE) -> str:
        """
        Display a prompt and get user input.

        Args:
            text: Prompt text
            color: Color for prompt

        Returns:
            User input string
        """
        prompt_text = self.colorize(text, color)
        return input(prompt_text).strip()

    def confirm(self, text: str) -> bool:
        """
        Ask for yes/no confirmation.

        Args:
            text: Question text

        Returns:
            True if user confirmed
        """
        response = self.prompt(f"{text} (y/n): ", Color.YELLOW).lower()
        return response in ('y', 'yes')

    def pause(self, text: str = "Press Enter to continue...") -> None:
        """
        Pause and wait for user to press Enter.

        Args:
            text: Pause message
        """
        self.prompt(text, Color.BRIGHT_BLACK)

    def print_divider(self, char: str = "-", width: int = 60) -> None:
        """
        Print a divider line.

        Args:
            char: Character to use for divider
            width: Width of divider
        """
        self.print_colored(char * width, Color.BRIGHT_BLACK)
