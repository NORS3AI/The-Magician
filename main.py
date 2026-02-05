#!/usr/bin/env python3
"""
The-Magician: A Text Adventure RPG
Based on Raymond E. Feist's Magician series

Entry point for the game.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.engine.game_loop import GameLoop
from src.config.settings import load_config


def main():
    """Main entry point for The-Magician."""
    print("=" * 60)
    print("  THE MAGICIAN")
    print("  A Text Adventure RPG")
    print("  Based on the works of Raymond E. Feist")
    print("=" * 60)
    print()

    # Load configuration
    config = load_config()

    # Initialize and run game loop
    game = GameLoop(config)
    game.run()


if __name__ == "__main__":
    main()
